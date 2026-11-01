'use strict';
// R332 S128. Finite constructed task allocation. No external dependencies.
const fs=require('node:fs');
const path=require('node:path');
function build(){
 const fields=["recoded","lower_capacity","high_probability_quarters","bits","cost","utility","low_realized","high_realized","expected_utility_quarters","precommit_bits","precommit_expected_quarters","robust_bits","robust_expected_quarters","oracle_low_bits","oracle_high_bits","oracle_expected_quarters","information_value_quarters"];
 const rows=[],worlds=[];
 function choose(r,c){
  const candidates=[];
  for(let i=0;i<8;i++){const bits=i.toString(2).padStart(3,"0");const f=[...bits].map(Number);const cost=f[0]+(r?1:2)*f[1]+3*f[2];const utility=f[0]+3*f[1]+4*f[2];if(cost<=c)candidates.push({bits,utility});}
  const max=Math.max(...candidates.map(x=>x.utility));return candidates.find(x=>x.utility===max);
 }
 for(const r of [0,1])for(let L=0;L<6;L++)for(let k=0;k<=4;k++){
  const candidates=[];
  for(let i=0;i<8;i++){
   const bits=i.toString(2).padStart(3,"0"),f=[...bits].map(Number),cost=f[0]+(r?1:2)*f[1]+3*f[2],utility=f[0]+3*f[1]+4*f[2];
   const low=cost<=L?utility:0,high=cost<=L+1?utility:0,expected=(4-k)*low+k*high;
   candidates.push({bits,cost,utility,low,high,expected});
  }
  const maximum=Math.max(...candidates.map(x=>x.expected)),winner=candidates.find(x=>x.expected===maximum);
  const lo=choose(r,L),hi=choose(r,L+1),robust=4*lo.utility,oracle=(4-k)*lo.utility+k*hi.utility,gap=oracle-maximum;
  if(oracle<maximum||maximum<robust||gap<0)throw Error("dominance failure");
  if((k===0&&maximum!==4*lo.utility)||(k===4&&maximum!==4*hi.utility))throw Error("endpoint mismatch");
  if((k===0||k===4)&&gap!==0)throw Error("endpoint information value");
  const w={recoded:r,lower_capacity:L,high_probability_quarters:k,precommit_bits:winner.bits,precommit_expected_quarters:maximum,robust_bits:lo.bits,robust_expected_quarters:robust,oracle_low_bits:lo.bits,oracle_high_bits:hi.bits,oracle_expected_quarters:oracle,information_value_quarters:gap};
  worlds.push(w);
  for(const a of candidates)rows.push([r,L,k,a.bits,a.cost,a.utility,a.low,a.high,a.expected,winner.bits,maximum,lo.bits,robust,lo.bits,hi.bits,oracle,gap]);
 }
 if(rows.length!==480||worlds.length!==60)throw Error("universe");
 for(let L=0;L<6;L++)for(let k=0;k<=4;k++){
  const a=worlds.find(w=>w.recoded===0&&w.lower_capacity===L&&w.high_probability_quarters===k),b=worlds.find(w=>w.recoded===1&&w.lower_capacity===L&&w.high_probability_quarters===k);
  for(const name of ["precommit_expected_quarters","robust_expected_quarters","oracle_expected_quarters"])if(b[name]<a[name])throw Error("recoding monotonicity");
 }
 const csv=fields.join(",")+"\n"+rows.map(x=>x.join(",")).join("\n")+"\n";
 const json=JSON.stringify({model:"R332_S128_UNCERTAIN_CAPACITY_E1",protocol:"S128-v1",source_row_count:rows.length,world_count:worlds.length,worlds})+"\n";
 return {csv,json,worlds,rows};
}
function audit(){
 const generated=build();
 const expected=[['R332_S128_ALL_480_CAPACITY_SUBSETS.csv',generated.csv],['R332_S128_EXACT_60_CAPACITY_WORLDS.json',generated.json]];
 for(const [name,content] of expected){
  const actual=fs.readFileSync(path.join(__dirname,name),'utf8');
  if(actual!==content)throw Error('persisted byte mismatch: '+name);
 }
 return generated;
}
if(require.main===module){
 const args=process.argv.slice(2);
 const result=args.includes('--audit')?audit():build();
 if(args.includes('--test')){
  if(result.rows.length!==480||result.worlds.length!==60)throw Error('universe mismatch');
  if(result.worlds.filter(w=>w.information_value_quarters>0).length!==24)throw Error('positive world count');
  if(result.worlds.reduce((s,w)=>s+w.information_value_quarters,0)!==59)throw Error('information value sum');
  console.log('R332 S128 exact finite E1 checks PASS');
 }else if(args.includes('--json'))process.stdout.write(result.json);
 else console.log('R332 S128 480 rows, 60 worlds; audit '+(args.includes('--audit')?'PASS':'NOT_RUN'));
}
module.exports={build,audit};
