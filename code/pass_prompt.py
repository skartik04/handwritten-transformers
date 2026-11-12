"""Original pass-prompt assembly; no evaluation feedback is included."""
EDITS_BUDGET=600_000

def pass_prompt(base, i, n, pad, done):   # done = [{'pass', 'status', 'block', 'applied', 'skipped', 'errors', 'nonzero'}] for the passes before i
    p = [base, f'\n\n==================== THIS IS PASS {i} OF {n} ====================']
    if i == n: p.append('This is the last pass: after it the weights are final.')
    if not done: p.append('Nothing has been written yet: the scratchpad is empty and every weight is 0.')
    else:
        p.append(f'YOUR SCRATCHPAD, as you left it:\n=====SCRATCHPAD=====\n{pad}\n=====END SCRATCHPAD=====' if pad else 'YOUR SCRATCHPAD is empty: no earlier reply held one.')
        room = EDITS_BUDGET
        for r in reversed(done): r['show'] = bool(r.get('block')) and len(r['block']) <= room; room -= len(r['block']) if r['show'] else 0
        for r in done:
            if r['status'] == 'empty': p.append(f"PASS {r['pass']}: the reply was empty (the reply limit was reached before anything was written). Nothing was added."); continue
            if not r.get('block'): p.append(f"PASS {r['pass']}: no edits block."); continue
            head = f"PASS {r['pass']} EDITS: {r['applied']} statements applied, {r['skipped']} skipped."
            if r['errors']: head += '\n  skipped (line of the block: statement -> reason):\n' + '\n'.join(f"    {e.get('line', '-')}: {e.get('statement', '')} -> {e['error']}" for e in r['errors'])
            p.append(head + (f"\n```\n{r['block'].rstrip()}\n```" if r['show'] else '\n  (the block is too long to show again; it is applied)'))
        nz = done[-1]['nonzero']
        p.append('NONZERO WEIGHTS NOW, by tensor: ' + (', '.join(f'{k} {v}' for k, v in nz.items() if v) or 'none'))
    return '\n\n'.join(p).encode()
