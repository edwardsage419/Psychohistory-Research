'use strict';
// R333 S129. Frozen artificial Boolean transition table.
const fs=require('node:fs');
const path=require('node:path');
function build(){
 const rows=[],worlds=[],header=["mechanism","initial_p","initial_b","initial_e","do_b","intervention_time","time","p","b","e"];
 for(const m of ["cyclic","feedforward"])for(let p=0;p<2;p++)for(let b=0;b<2;b++)for(let e=0;e<2;e++)for(let d=0;d<2;d++)for(const tau of [1,2]){
  let P=p,B=b,E=e;rows.push([m,p,b,e,d,tau,0,P,B,E]);
  for(let t=1;t<=4;t++){
   const pp=P^E,bb=t===tau?d:(P^B),ee=m==="cyclic"?(B^E):E;
   P=pp;B=bb;E=ee;rows.push([m,p,b,e,d,tau,t,P,B,E]);
  }
  worlds.push({mechanism:m,initial_p:p,initial_b:b,initial_e:e,do_b:d,intervention_time:tau,final_p:P,final_b:B,final_e:E});
 }
 if(rows.length!==320||worlds.length!==64)throw Error("universe");
 const csv=header.join(",")+"\n"+rows.map(r=>r.join(",")).join("\n")+"\n";
 const json=JSON.stringify({model:"R333_S129_TIMED_INTERVENTION_E1",source_row_count:320,world_count:64,worlds})+"\n";
 return {csv,json,rows,worlds};
}
function audit(){
 const output=build();
 for(const [name,bytes] of [['R333_S129_ALL_320_TIMED_TRIADIC_STATES.csv',output.csv],['R333_S129_EXACT_64_TIMED_TRIADIC_WORLDS.json',output.json]]){
  if(fs.readFileSync(path.join(__dirname,name),'utf8')!==bytes)throw Error('byte replay mismatch: '+name);
 }
 return output;
}
if(require.main===module){
 const args=process.argv.slice(2);
 const out=args.includes('--audit')?audit():build();
 if(args.includes('--test')){
  if(out.rows.length!==320||out.worlds.length!==64)throw Error('universe mismatch');
  console.log('R333 S129 bounded artificial replay PASS');
 }else if(args.includes('--json'))process.stdout.write(out.json);
 else console.log('R333 S129 320 rows 64 worlds; audit '+(args.includes('--audit')?'PASS':'NOT_RUN'));
}
module.exports={build,audit};
