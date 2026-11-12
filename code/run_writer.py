"""Portable three-pass Codex launcher. Run explicitly; --dry-run makes no requests."""
import argparse,json,os,re,shlex,shutil,subprocess
from pathlib import Path
import numpy as np
from model import zeros
from parse_edits import apply
from pass_prompt import pass_prompt
ROOT=Path(__file__).resolve().parents[1]
PAD=re.compile(r'(?ms)^=====SCRATCHPAD=====[ \t]*\r?\n(.*?)^=====END SCRATCHPAD=====[ \t]*$')

def main():
 p=argparse.ArgumentParser();p.add_argument('--experiment',default='general-chat',choices=['general-chat','sycophantic']);p.add_argument('--writer',default='astra',choices=['astra','sol']);p.add_argument('--out',type=Path,required=True);p.add_argument('--dry-run',action='store_true');a=p.parse_args()
 out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
 if any(out.iterdir()):p.error('Output directory must be empty; saved experiments are never overwritten.')
 if (ROOT/'experiments').resolve() in out.parents or out==(ROOT/'experiments').resolve():p.error('Use a separate output directory, not experiments/.')
 d=json.loads((ROOT/'shared/vocabulary.json').read_text());base=(ROOT/'experiments'/a.experiment/'prompt.txt').read_text();w=zeros(d);done=[];pad=''
 template=json.loads((ROOT/f'shared/codex/{a.writer}-command.json').read_text());catalog=json.loads((ROOT/f'shared/codex/{a.writer}-catalog.json').read_text())
 codex=shutil.which('codex') or 'codex';bwrap=shutil.which('bwrap') or 'bwrap'
 for i in range(1,4):
  folder=out/f'pass{i}';folder.mkdir();prompt=pass_prompt(base,i,3,pad,done);(folder/'prompt.txt').write_bytes(prompt)
  instructions=folder/'instructions.md';instructions.write_text((ROOT/'shared/instructions.md').read_text());cat=folder/'catalog.json';cat.write_text(json.dumps(catalog));empty=folder/'empty-instructions';empty.write_text('')
  mapping={'BWRAP':bwrap,'CODEX':codex,'EMPTY':str(empty),'USER_AGENTS':str(Path.home()/'.codex/AGENTS.md'),'USER_CONFIG':str(Path.home()/'.codex/config.toml'),'INSTRUCTIONS':str(instructions),'CATALOG':str(cat),'ANSWER':str(folder/'response.md'),'MODEL':'gpt-6-astra' if a.writer=='astra' else 'gpt-6.1-sol'}
  command=[arg.format(**mapping) for arg in template]
  if a.dry_run:print(shlex.join(command)+' < '+shlex.quote(str(folder/'prompt.txt')));return
  for key in ('USER_AGENTS','USER_CONFIG'):
   if not Path(mapping[key]).is_file():p.error(f'The recorded bwrap profile requires {mapping[key]}; configure your own local Codex installation before replaying.')
  if not shutil.which('bwrap'):p.error('This recorded profile requires Linux bubblewrap (bwrap).')
  with (folder/'events.jsonl').open('wb') as stdout,(folder/'stderr.log').open('wb') as stderr:
   result=subprocess.run(command,input=prompt,cwd=folder,stdout=stdout,stderr=stderr)
  if result.returncode:raise SystemExit(f'Writer pass {i} exited {result.returncode}; see its stderr.log.')
  answer=(folder/'response.md').read_text();ok=len(answer)>=200
  rep=apply(w,answer,d['tokens']) if ok else dict(block='',applied=0,skipped=0,errors=[])
  pads=PAD.findall(answer) if ok else []
  if pads:pad=pads[-1].strip()
  (folder/'scratchpad.md').write_text(pad)
  rec=dict(pass_=i,status='ok' if len(answer)>=200 else 'empty',block=rep.get('block',''),applied=rep['applied'],skipped=rep['skipped'],errors=rep['errors'],nonzero={k:int(np.count_nonzero(v)) for k,v in w.items()})
  rec['pass']=rec.pop('pass_');done.append(rec);(folder/'status.json').write_text(json.dumps({k:v for k,v in rec.items() if k!='block'},indent=2))
 np.savez_compressed(out/'weights.npz',**w)
 print('Saved final cumulative weights:',out/'weights.npz')

if __name__=='__main__':main()
