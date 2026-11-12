"""Run a published small network locally. Does not call a writer model."""
import argparse,json
from pathlib import Path
import numpy as np
import model,tokenizer
ROOT=Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser();p.add_argument('--experiment',default='general-chat',choices=['general-chat','sycophantic']);p.add_argument('--writer',default='astra',choices=['astra','sol']);p.add_argument('--question');a=p.parse_args()
 f=ROOT/'experiments'/a.experiment/a.writer/'weights.npz'
 if not f.exists():p.error('This experiment/writer has no exported checkpoint.')
 d=json.loads((ROOT/'shared/vocabulary.json').read_text());w=dict(np.load(f,allow_pickle=False))
 def reply(q):
  if len(tokenizer.chat([q]))>143:raise ValueError('Question exceeds the 143-token input budget.')
  ids=model.generate(w,d,[[q]],batch=1)[0];print(model.detok(ids));print('[EOS]' if ids and ids[-1]==1 else '[48-token cap]')
 if a.question:reply(a.question)
 else:
  print('Each question starts fresh. Ctrl-D to exit.')
  while True:
   try:q=input('You: ')
   except (EOFError,KeyboardInterrupt):break
   if q.strip():reply(q)

if __name__=='__main__':main()
