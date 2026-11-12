"""Portable float64 reference inference, extracted from the WSP model2/3/4 implementation."""
import numpy as np
import tokenizer as tok4
BASE=10000.0

def shapes(d):   # d = the data file: tokens, D, layers, heads, mlp
    V, D, H, M = len(d['tokens']), d['D'], d['heads'], d['mlp']; dh = D // H
    s = {'E': (V, D)}
    for l in range(1, d['layers'] + 1):
        s.update({f'Q{l}': (H, D, dh), f'K{l}': (H, D, dh), f'V{l}': (H, D, dh), f'O{l}': (H, dh, D),
                  f'M{l}_in': (D, M), f'M{l}_b': (M,), f'M{l}_out': (M, D)})
    s['U'] = (D, V)
    return s

def rope(v):   # v (N, L, dh): rotate the pair (2i, 2i+1) at position t by the angle t * BASE^(-2i/dh)
    L, dh = v.shape[1], v.shape[2]
    ang = np.arange(L)[:, None] * BASE ** (-2 * np.arange(dh // 2) / dh)[None]
    c, s = np.cos(ang), np.sin(ang); o = np.empty_like(v)
    o[..., 0::2] = v[..., 0::2] * c - v[..., 1::2] * s
    o[..., 1::2] = v[..., 0::2] * s + v[..., 1::2] * c
    return o

def zeros(d): return {k: np.zeros(s, np.float32) for k, s in shapes(d).items()}

def last_logits(w, toks, n, layers):   # toks (N, L) right-padded, n = lengths; logits (N, V) at each row's last token
    x = w['E'][toks].astype(np.float64); H, dh = w['Q1'].shape[0], w['Q1'].shape[2]
    mask = np.triu(np.ones((toks.shape[1],) * 2, bool), 1)
    for l in range(1, layers + 1):
        add = np.zeros_like(x)
        for h in range(H):
            if not w[f'O{l}'][h].any(): continue
            s = rope(x @ w[f'Q{l}'][h]) @ rope(x @ w[f'K{l}'][h]).transpose(0, 2, 1) / np.sqrt(dh)
            s = np.where(mask, -np.inf, s); a = np.exp(s - s.max(-1, keepdims=True)); a /= a.sum(-1, keepdims=True)
            add += (a @ (x @ w[f'V{l}'][h])) @ w[f'O{l}'][h]
        x = x + add
        x = x + np.maximum(x @ w[f'M{l}_in'] + w[f'M{l}_b'], 0) @ w[f'M{l}_out']
    return x[np.arange(len(n)), n - 1] @ w['U']

def generate(w, d, chats, batch=64):   # -> list of generated id lists (EOS included when written)
    w = {k: np.asarray(v, np.float64) for k, v in w.items()}; out = []; MAX_NEW = d['max_new']
    for b in range(0, len(chats), batch):
        ps = [tok4.chat(c) for c in chats[b:b + batch]]; N = len(ps); L = max(map(len, ps)) + MAX_NEW
        toks = np.zeros((N, L), int); n = np.array([len(p) for p in ps]); n0 = n.copy(); live = np.ones(N, bool)
        for k, p in enumerate(ps): toks[k, :n[k]] = p
        for _ in range(MAX_NEW):
            if not live.any(): break
            nxt = last_logits(w, toks, n, d['layers']).argmax(1)
            toks[live, n[live]] = nxt[live]; n = n + live; live = live & (nxt != 1)
        out += [list(map(int, toks[k, n0[k]:n[k]])) for k in range(N)]
    return out

def detok(ids, d=None): return tok4.detok(ids)
