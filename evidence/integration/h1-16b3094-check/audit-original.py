import json,hashlib,subprocess,shutil,time,os,signal
from pathlib import Path
r=Path(__file__).resolve().parent;repo=r.parent.parent
w=Path('/Users/clkao/git/spacedock-research/studfleet/.worktrees/spacedock-ensign-compose-main-model-operations-into-reader-steps');base=w/'builds/main-composition-implementation';inp=base/'dss-input';binary=base/'studfleet'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(binary)=='a0c9cb64180ceeacf9f722510441cbaa2c5e4f2f5cbc7e7dd4d778353b962d23'
b=read(base/'dss-source-binding.json')
for p,h in b['source_sha256'].items():assert sha(repo/p)==h,p
for p,k in [('source.mpd','specimen_source_sha256'),('intake/assembly.json','imported_assembly_sha256'),('intake/import-report.json','import_report_sha256'),('plan.json','plan_sha256'),('presentation.json','presentation_sha256')]:assert sha(inp/p)==b[k],p
model=read(repo/'sources/minifigure/legacy-v10/model.json');steps=read(repo/'sources/minifigure/legacy-v10/instruction-plan.json')['steps'];cw=read(repo/'migration/minifigure-v10/occurrence-crosswalk.json')['occurrences'];full=read(repo/'migration/minifigure-v10/assembly.json')['instances'];a=read(inp/'intake/assembly.json')['instances'];plan=read(inp/'plan.json')
assert b['source_operations_exact']==model['build_operations'][6:9]
assert b['source_step_exact']==steps[1]
assert set(b['context_piece_ids'])==set(steps[0]['new_ids'])
assert b['selected_piece_ids']==steps[1]['new_ids'];assert len(a)==16
cross={x['piece_id']:x for x in cw};original={x['id']:x for x in full};selected={x['id']:x for x in a};mapping={}
for x in b['occurrences']:
 assert cross[x['piece_id']]['occurrence_id']==x['retained_occurrence']
 assert original[x['retained_occurrence']]==x['exact_pose']
 assert {k:v for k,v in selected[x['specimen_occurrence']].items() if k!='id'}=={k:v for k,v in x['exact_pose'].items() if k!='id'}
 mapping[x['piece_id']]=x['specimen_occurrence']
ops=plan['groups'][0]['operations'];assert ops[0]['seed'] is True;assert set(ops[0]['introduce'])=={mapping[x] for x in b['context_piece_ids']}
for op,legacy in zip(ops[1:],b['source_operations_exact']):
 assert op['introduce']==[mapping[x] for x in legacy['ids']];assert op['movement']=='unknown' and 'direction' not in op and 'distance' not in op
(r/'audit.json').write_text(json.dumps({'candidate_source':'16b3094','binary_sha256':sha(binary),'source_bindings_match':True,'all16_exact_part_color_matrices':True,'step2_ops7_9_exact':True,'context_after6_matches11pieces':True,'new_ids':b['selected_piece_ids'],'source_operations':[7,8,9],'input_hashes':{p:sha(inp/p) for p in ['source.mpd','intake/assembly.json','intake/import-report.json','plan.json','presentation.json']}},indent=2)+'\n')
args=[str(binary),'draft','--assembly',str(inp/'intake/assembly.json'),'--provenance',str(inp/'intake/import-report.json'),'--plan',str(inp/'plan.json'),'--presentation',str(inp/'presentation.json'),'--check-only'];start=time.monotonic();peak=0;minimum=shutil.disk_usage(r).free;halt=''
with (r/'check.stdout.json').open('w') as out,(r/'check.stderr').open('w') as err:
 p=subprocess.Popen(args,cwd=w,stdout=out,stderr=err,start_new_session=True)
 while p.poll() is None:
  size=sum(f.stat().st_size for f in r.rglob('*') if f.is_file());peak=max(peak,size);minimum=min(minimum,shutil.disk_usage(r).free)
  if size>60*1024**2 or minimum<512*1024**2 or time.monotonic()-start>330:
   halt='lease bound';os.killpg(p.pid,signal.SIGTERM);break
  time.sleep(.1)
 code=p.wait(timeout=10)
(r/'check-command.json').write_text(json.dumps({'argv':args,'cwd':str(w),'exit_code':code,'halt':halt,'peak_owned_bytes':peak,'minimum_free_bytes':minimum,'elapsed_seconds':time.monotonic()-start},indent=2)+'\n');print('source audit passed; check exit',code);print((r/'check.stderr').read_text());assert code==0 and not halt
