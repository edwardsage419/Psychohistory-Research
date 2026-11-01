#!/usr/bin/env node
'use strict';
// Historical claim integrity only. The separate mathematical gate remains mandatory.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const PINS={
R333:['39c51ac7df3a208bbc884d90efeb9e213dcbfcc2','52ebada1e978179e624897715708854e41dd29f5',40047349488,'3396bf2e95a7b25cada8f9a0d474732c8e685920','ebe035309977d3e5c5961a7091a17f0fe8222448'],
R334:['70c90c39ddcfe79140497dd0997444c50fcd7fdc','ecaf06f19437b4e13940b5db8858f2f0920d1096',40051279908,'4380bcd830aac7edb8fdfef11ce32dec720f1186','7ec583e77d7e4a937b552601dcca5409483cc59b'],
R335:['3e71a2a448923a969df3b16aae607df6c3908942','507b781e2fb4a27d72c6cbd096f8dd14c6d4543d',40051490899,'f0862aa4ae29d3abcb95d1e097c2fe924be16ef0','0c553f662ae723adadaba9c7f4ce325d8964032e'],
R336:['7f5281bc1300d57ca1da7724903864590a8a0edd','200e867f2767bc7e87b9aca22c58c7b5f1a8a361',40055738338,'1d580bed37891ca4516a5c3d338037bd3ba8c2d1','3f10d5a6c2c8b713d3b14abc61c768383de8c934'],
R337:['ac32728a298970b9805868aa0252ba289697c5a8','09d327ac24379ea14d017c42e35e566f010b23ea',40055959491,'7f7a44f9596acb5d06ffe4d51677e59d75a5f357','c26ded95a844908d692f069c1a11ac1934b15487'],
R338:['2265fab92500725ee9e5b0ce8bc0975db715aea1','c1ddba636168d6fd4dfbb671cffa613109e81d3b',40059210892,'f4d219fecb3f54a522d0ab86a26cb24b41ee0452','6b843af069053eb73c7883ba700f918c5cb8288d'],
R339:['cf39c38074f6e6444af860ff48a735d321689a2e','632575c8836cb9082d9f3b62f36da936f0a7a7d6',40059401269,'9152132df26ecfb9a09aaa6ce09f12aedd3658e9','dba0ded506b85e7c938a2c97d9478c2cd1daf120'],
R340:['8f6beaa0ed823a9ce1b0967b30aebaa30b5ee4e0','9cc125685111d20768853ad167664881850ab8ad',40063363405,'bf4547eeb7a070a0b04fc14e1f25d114c12c17d8','86c0d5fc0a371ecd804f4ee92d6d83f665f0755d']};
function need(ok,msg){if(!ok)throw Error(msg)}
function blob(b){return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex')}
function pinned(file,sha){const st=fs.lstatSync(file);need(st.isFile()&&!st.isSymbolicLink(),'unsafe file '+file);const b=fs.readFileSync(file);need(blob(b)===sha,'blob mismatch '+file);const o=JSON.parse(b.toString('utf8'));need(o&&typeof o==='object'&&!Array.isArray(o),'invalid object '+file);return o}
function absent(v){return v===false||v==='NOT_ESTABLISHED'}
function verify(root,pins=PINS){
const ids=Object.keys(pins).sort();need(ids.length===8&&ids.every((id,i)=>id==='R'+(333+i)),'universe');
const rs=fs.lstatSync(root);need(rs.isDirectory()&&!rs.isSymbolicLink(),'unsafe root');
const out=[];
for(const id of ids){
const [mb,fb,run,src,proto]=pins[id],dir=path.join(root,'research',id),ds=fs.lstatSync(dir);need(ds.isDirectory()&&!ds.isSymbolicLink(),'unsafe directory '+id);
const m=pinned(path.join(dir,id+'_MACHINE_RECEIPT.json'),mb),f=pinned(path.join(dir,id+'_FINAL_ACCEPTANCE_STATUS.json'),fb),v=m.verification;
need(m.research_id===id&&f.research_id===id&&m.catalogue_id===f.original_catalogue_id,'identity '+id);
need(m.protocol_commit===proto&&f.protocol_commit===proto,'protocol '+id);
need((m.source_commit||m.verified_source_commit)===src&&f.source_commit===src,'source '+id);
need(v&&typeof v==='object'&&(v.CI_run_id||v.run_id)===run&&f.CI_run_id===run,'CI identity '+id);
need(v.conclusion==='success'&&f.CI_conclusion==='success'&&f.three_jobs_success===true,'CI status '+id);
const grade=m.scientific_grade||m.evidence_grade;
need(typeof grade==='string'&&grade.startsWith('PASS_BOUNDED_E1_')&&f.status===grade,'E1 grade '+id);
need(absent(m.human_E2??m.actual_human_E2)&&absent(m.historical_E3),'machine overclaim '+id);
need(absent(f.real_human_E2)&&absent(f.historical_E3)&&absent(f.original_empirical_replication),'final overclaim '+id);
need(f.machine_receipt==='research/'+id+'/'+id+'_MACHINE_RECEIPT.json','receipt path '+id);
out.push({model:id,machine_blob:mb,final_blob:fb,CI_run:run});
}
return {status:'PASS_HISTORICAL_CLAIMS_E1_IDENTITY_ONLY',files_checked:16,models:out,mathematical_gate:'NOT_RUN',production_adoption:'NOT_ESTABLISHED'};
}
if(require.main===module){try{const a=process.argv.slice(2);need(a.length===0||(a.length===2&&a[0]==='--repo-root'),'usage: [--repo-root PATH]');console.log(JSON.stringify(verify(a.length?path.resolve(a[1]):path.resolve(__dirname,'..','..'))))}catch(e){console.error('CLAIM_GATE_FAIL: '+e.message);process.exitCode=1}}
module.exports={verify,blob,PINS};
