"""Read a writer's edits block into the weight arrays; never execute model code (Python AST inspection + literal_eval).
On top of the older edits language: a token can be named by its text on the vocabulary axis (E's first index, U's last),
one index may be a list of indices or tokens, and a value is broadcast over the entries it is assigned to.
apply(arrays, reply_text, tokens) edits the arrays in place (a statement that cannot be read is skipped) and returns a report."""
import ast, re
import numpy as np
VOCAB_AXIS = {'E': 0, 'U': 1}
LIMIT = 1e6


def statements(block):   # one statement per line, except bracketed lists that run over several lines
    pending, start, depth = [], None, 0
    for n, line in enumerate(block.splitlines(), 1):
        text = re.sub(r'#(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$).*', '', line).strip()   # a '#' outside quotes starts a comment
        if not text and not pending: continue
        if start is None: start = n
        pending.append(text); depth += text.count('[') - text.count(']')
        if depth <= 0: yield start, ' '.join(pending); pending, start, depth = [], None, 0
    if pending: yield start, ' '.join(pending)


def one(node, size, tid):   # a single index: integer literal, or a token's text on the vocabulary axis
    v = ast.literal_eval(node)
    if type(v) is str:
        if tid is None: raise ValueError('a token name can only index the vocabulary axis')
        if v not in tid: raise ValueError(f'unknown token {v!r}')
        return tid[v]
    if type(v) is not int: raise ValueError('an index must be an integer or a token')
    if not -size <= v < size: raise IndexError(f'index {v} is outside 0..{size - 1}')
    return v % size


def axis(node, size, tid):   # -> (indices along this axis, keeps its dimension?)
    if isinstance(node, ast.Slice):
        f = lambda x: None if x is None else ast.literal_eval(x)
        lo, hi, st = f(node.lower), f(node.upper), f(node.step)
        if any(x is not None and type(x) is not int for x in (lo, hi, st)) or st == 0: raise ValueError('bad range')
        return np.arange(size)[slice(lo, hi, st)], True
    if isinstance(node, ast.List):
        idx = [one(e, size, tid) for e in node.elts]
        if len(set(idx)) != len(idx): raise ValueError('an index list names the same entry twice')
        return np.array(idx, int), True
    return np.array([one(node, size, tid)]), False


def numbers(node):
    v = ast.literal_eval(node)
    def check(x):
        if isinstance(x, list): [check(y) for y in x]
        elif type(x) not in (int, float) or not np.isfinite(x) or abs(x) > LIMIT: raise ValueError('values must be plain numbers with |v| <= 1e6')
    check(v); return np.asarray(v, dtype=np.float64)


def apply(arrays, reply, tokens):
    tid = {t: i for i, t in enumerate(tokens)}
    rep = {'edits_block': False, 'applied': 0, 'skipped': 0, 'errors': []}
    opens = list(re.finditer(r'(?m)^```edits[ \t]*\r?\n', reply))
    if not opens: rep['errors'].append({'error': 'no edits block'}); return rep
    rest = reply[opens[-1].end():]; close = re.search(r'(?m)^```[ \t]*(?:\r?\n|$)', rest)
    if close is None: rep['errors'].append({'error': 'the last edits block has no closing fence; nothing was read'}); return rep
    rep['edits_block'] = True; rep['block'] = rest[:close.start()]
    for line, src in statements(rep['block']):
        try:
            st = ast.parse(src, mode='exec').body
            if len(st) != 1: raise ValueError('one assignment per statement')
            st = st[0]
            if isinstance(st, ast.Assign) and len(st.targets) == 1: tgt, op = st.targets[0], 'set'
            elif isinstance(st, ast.AugAssign) and isinstance(st.op, (ast.Add, ast.Sub, ast.Mult)): tgt, op = st.target, type(st.op).__name__
            else: raise ValueError('only =, +=, -=, *= on an indexed tensor')
            if not isinstance(tgt, ast.Subscript) or not isinstance(tgt.value, ast.Name) or tgt.value.id not in arrays: raise ValueError('unknown tensor')
            name = tgt.value.id; a = arrays[name]
            parts = list(tgt.slice.elts) if isinstance(tgt.slice, ast.Tuple) else [tgt.slice]
            if len(parts) > a.ndim: raise IndexError('too many indices')
            ax = [axis(p, a.shape[k], tid if VOCAB_AXIS.get(name) == k else None) for k, p in enumerate(parts)]
            ax += [(np.arange(a.shape[k]), True) for k in range(len(parts), a.ndim)]
            if sum(isinstance(p, ast.List) for p in parts) > 1: raise ValueError('at most one index list per statement')
            keep = tuple(len(i) for i, k in ax if k); full = tuple(len(i) for i, _ in ax); grid = np.ix_(*[i for i, _ in ax])
            val = numbers(st.value)
            try: val = np.broadcast_to(val, keep).reshape(full)
            except ValueError: raise ValueError(f'a value of shape {val.shape} does not fit the {keep} entries it is assigned to')
            cur = a[grid].astype(np.float64)
            new = val if op == 'set' else cur + val if op == 'Add' else cur - val if op == 'Sub' else cur * val
            if not np.isfinite(new).all() or np.abs(new).max(initial=0) > 1e30: raise ValueError('non-finite weight')
            a[grid] = new; rep['applied'] += 1
        except (ValueError, TypeError, SyntaxError, IndexError, OverflowError, RecursionError, MemoryError) as e:
            rep['skipped'] += 1
            if len(rep['errors']) < 40: rep['errors'].append({'line': line, 'statement': src[:120], 'error': f'{type(e).__name__}: {e}'[:200]})
    return rep
