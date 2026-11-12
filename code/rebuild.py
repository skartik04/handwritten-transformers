"""Rebuild a checkpoint from saved responses; check tensor equality, without writer calls."""
import argparse,json
from pathlib import Path
import numpy as np
from model import zeros
from parse_edits import apply
ROOT=Path(__file__).resolve().parents[1]

def rebuild(folder):
 d=json.loads((ROOT/'shared/vocabulary.json').read_text());w=zeros(d);records=[]
 for p in sorted((folder/'passes').glob('pass*')):
  status=json.loads((p/'status.json').read_text())
  if status['status']=='ok':
   r=apply(w,(p/'response.md').read_text(),d['tokens']);records.append(dict(pass_=status['pass'],applied=r['applied'],skipped=r['skipped']))
 with np.load(folder/'weights.npz',allow_pickle=False) as expected:
  assert set(w)==set(expected.files)
  for k,v in w.items():assert np.array_equal(v,expected[k]),f'{folder.name}: {k} differs'
 return records

def main():
 p=argparse.ArgumentParser();p.add_argument('--experiment',default='general-chat');p.add_argument('--writer',default='astra');p.add_argument('--all',action='store_true');a=p.parse_args()
 folders=[f.parent for f in (ROOT/'experiments').glob('*/*/weights.npz')] if a.all else [ROOT/'experiments'/a.experiment/a.writer]
 for folder in folders:print(folder.relative_to(ROOT),json.dumps(rebuild(folder)),'all tensors match')

if __name__=='__main__':main()
