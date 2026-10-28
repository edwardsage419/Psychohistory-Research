#!/usr/bin/env node
/** E060 exact source-first audit. Node standard library only.
 * Usage: node e060_r229_s25_original_csv_bridge_exact_20261028.js /path/to/Psychohistory-Research
 */
const fs=require('node:fs'),path=require('node:path'),root=process.argv[2]||process.cwd();
const csv=fs.readFileSync(path.join(root,'research/R229/R229_ALL_4096_ORIGINAL_3X3_MATRIX_SOURCES.csv'),'utf8');
const receipt=JSON.parse(fs.readFileSync(path.join(root,'research/validation/R229_S25_COMMON_ITEM_BRIDGE_EXACT_RECEIPT_2026-10-28.json'),'utf8'));
const gcd=(a,b)=>b?gcd(b,a%b):a<0n?-a:a;
class F{
 constructor(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(!b)throw Error('zero denominator');const g=gcd(a,b);this.n=a/g;this.d=b/g;}
 add(x){return new F(this.n*x.d+x.n*this.d,this.d*x.d)}
 sub(x){return new F(this.n*x.d-x.n*this.d,this.d*x.d)}
 mul(x){return new F(this.n*x.n,this.d*x.d)}
 div(x){return new F(this.n*x.d,this.d*x.n)}
 str(){return this.d===1n?String(this.n):this.n+'/'+this.d}
}
const one=new F(1),zero=new F(0);
const prob=(t,b)=>{const e=t-b,od=e>=0?new F(2n**BigInt(e)):new F(1n,2n**BigInt(-e));return od.div(one.add(od))};
let passed=0;function check(ok,label){if(!ok)throw Error('FAIL '+label);passed++;}
const lines=csv.trim().split(/\r?\n/);
check(lines[0]==='world,original_full_nine_bit_matrix,actual_observed_matrix,observation_mask,observed_person_row_scores,original_probability,structural_zero','header');
const seen=new Set(),original=[];let sum=zero;
for(const row of lines.slice(1)){
 const [world,bits,observed,mask,score,probability,sz]=row.split(',');
 if(world!=='DISCONNECTED_ITEM3')continue;
 check(bits.length===9&&/^[01]{9}$/.test(bits),'bits '+bits);
 check(!seen.has(bits),'unique '+bits);seen.add(bits);
 check(mask==='110|110|001','mask '+bits);
 check(observed===bits.slice(0,2)+'?|'+bits.slice(3,5)+'?|??'+bits[8],'observed '+bits);
 check(score===''+(Number(bits[0])+Number(bits[1]))+(Number(bits[3])+Number(bits[4]))+bits[8],'score '+bits);
 check(sz==='0','structural zero '+bits);
 let mass=one;
 for(let i=0;i<3;i++)for(let j=0;j<3;j++){const p=prob([-1,0,1][i],[-1,0,1][j]);mass=mass.mul(bits[3*i+j]==='1'?p:one.sub(p));}
 check(mass.str()===probability,'prob '+bits);
 original.push({obs:[0,1,3,4,8].map(i=>bits[i]).join(''),mass});sum=sum.add(mass);
}
check(original.length===512,'512 rows');check(seen.size===512,'unique 512');check(sum.str()==='1','original mass');
const base=new Map();for(const o of original)base.set(o.obs,(base.get(o.obs)||zero).add(o.mass));
check(base.size===32,'32 observation keys');
let scenarios=0;
for(const sc of receipt.scenarios){
 const p1=prob(sc.theta,0),p2=prob(sc.theta,1+sc.bridge_item2_drift),p10=p1.mul(one.sub(p2)),p01=one.sub(p1).mul(p2);
 const r=p10.add(p01),q=p10.div(r),od=p10.div(p01),info=q.mul(one.sub(q)),expected=r.mul(info);
 for(const [k,v] of Object.entries({p10,p01,p_r1:r,q10_given_r1:q,conditional_odds:od,conditional_fisher_coeff:info,expected_fisher_coeff:expected}))check(sc[k]===v.str(),'scenario '+sc.theta+' '+sc.bridge_item2_drift+' '+k);
 for(const [k,v] of Object.entries({source_states:2048,positive_source_states:2048,distinct_observed_keys:128,original_observed_keys:32,joint_mass:'1',single_item_conditional_fisher_coeff:'0',original_observed_marginal_unchanged:true}))check(sc[k]===v,'metadata '+k);
 const patterns=[one.sub(p1).mul(one.sub(p2)),p01,p10,p1.mul(p2)];
 check(patterns.reduce((a,b)=>a.add(b),zero).str()==='1','bridge mass');
 const margs=new Map(),joint=new Set();let total=zero;
 for(const o of original)for(let j=0;j<4;j++){const w=o.mass.mul(patterns[j]);total=total.add(w);margs.set(o.obs,(margs.get(o.obs)||zero).add(w));joint.add(o.obs+'_'+j);}
 check(total.str()==='1','joint mass');check(joint.size===128,'joint keys');
 for(const [k,v] of base)check(margs.get(k).str()===v.str(),'marginal '+k);
 scenarios++;
}
check(scenarios===6,'six scenarios');
console.log(JSON.stringify({audit:'E060',source_rows:lines.length-1,disconnected_rows:original.length,observed_keys:base.size,scenarios,passed,failed:0}));
