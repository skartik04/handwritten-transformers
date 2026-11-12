"""v4 text <-> tokens. English is lower-cased, split into words, digits and the marks . ? , ! ; each word is kept, rewritten by
the fixed table (bad -> not good, cats -> cat -s), or becomes UNK. Chats are BOS USER msg BOT reply [USER msg BOT reply ...]."""
import json, re
from pathlib import Path
R = Path(__file__).resolve().parents[1]
_V = {}


def load():
    if not _V:
        v = json.load(open(R / 'shared/vocabulary.json')); _V['v'] = v; _V['tok'] = v['tokens']
        _V['id'] = {t: i for i, t in enumerate(v['tokens'])}; _V['table'] = json.load(open(R / 'shared/rewrite_table.json'))
    return _V


def words(text):   # -> token strings after the rewrite, and the words that became UNK
    V = load(); out, unk = [], []
    t = text.lower().replace('\u2019', "'")
    for a, b in (("won't", 'will not'), ("can't", 'can not'), ("n't", ' not'), ("'m", ' am'), ("'re", ' are'), ("'ll", ' will'), ("'ve", ' have'), ("'d", ' would'), ("it's", 'it is'), ("that's", 'that is'), ("what's", 'what is'), ("there's", 'there is'), ("he's", 'he is'), ("she's", 'she is'), ("who's", 'who is'), ("where's", 'where is'), ("here's", 'here is'), ("let's", 'let us'), ("'s", '')):
        t = t.replace(a, b)   # contractions; 's is dropped (tom's dog -> tom dog)
    for p in re.findall(r"[a-z]+|\d|[.?,!]", t.replace("'", ' ')):
        if p in V['id']: out.append(p)
        elif p in V['table']: out += V['table'][p]
        else: out.append('UNK'); unk.append(p)
    return out, unk


def ids(text):
    V = load(); return [V['id'][t] for t in words(text)[0]]


def chat(turns):   # turns = [user, bot, user, ...] ending with a user message -> ids up to and including the last BOT
    V = load(); x = [V['id']['BOS']]
    for i, t in enumerate(turns):
        x += [V['id']['USER' if i % 2 == 0 else 'BOT']] + ids(t)
    return x + [V['id']['BOT']]


def detok(seq):   # ids or token strings -> readable text; pieces join onto their word
    V = load(); out = []
    for t in seq:
        t = V['tok'][t] if isinstance(t, int) else t
        if t in ('BOS', 'EOS', 'USER', 'BOT'): continue
        if t.startswith('-') and out:
            w = out[-1]
            if t in ('-s', '-es') and w.endswith('y') and w[-2:-1] not in 'aeiou': w = w[:-1] + 'ie'
            if t in ('-ed', '-er', '-est') and w.endswith('e'): w = w[:-1]
            elif t == '-ing' and w.endswith('e') and not w.endswith(('ee', 'ye', 'oe')) and len(w) > 2: w = w[:-1]   # make -ing -> making
            elif t in ('-ed', '-er', '-est', '-ing') and len(w) in (3, 4) and w[-3] not in 'aeiou' and w[-2] in 'aeiou' and w[-1] not in 'aeiouwxy' and (len(w) == 3 or w[-4] not in 'aeiou'): w = w + w[-1]   # big -est -> biggest, stop -ed -> stopped
            if t in ('-er', '-est', '-ed', '-ly', '-ness', '-less', '-ful') and w.endswith('y') and w[-2:-1] not in 'aeiou': w = w[:-1] + 'i'
            out[-1] = w + t[1:]
        elif out and out[-1].endswith('-') and not out[-1].startswith('-'): out[-1] = out[-1][:-1] + t
        elif t.isdigit() and out and out[-1].isdigit(): out[-1] += t
        else: out.append(t)
    return ' '.join(out)
