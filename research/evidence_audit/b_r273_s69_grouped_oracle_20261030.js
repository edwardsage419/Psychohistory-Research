/* R273 S69 independent grouped-binomial 15-cell oracle; standard Node.js CLI */
function checkB(doc){
const gcd=(a,b)=>{while(b){let t=a%b;a=b;b=t}return a},frac=(n,d)=>{let q=gcd(Math.abs(n),d);return d/q===1?String(n/q):`${n/q}/${d/q}`},C4=[1,4,6,4,1],C2=[1,2,1];
const expected=[];
for(let a=1;a<=3;a++)for(let b=1;b<=3;b++){
let nL=0,nS=0,nT=0,n=0;
for(let k=0;k<5;k++)for(let j=0;j<3;j++){
let w=C4[k]*a**k*(4-a)**(4-k)*C2[j]*b**j*(4-b)**(2-j);
let s=3*a,l=2*(k+1),lossS=j*(12-s)**2+(2-j)*s*s,lossL=j*(12-l)**2+(2-j)*l*l;
if(lossL<lossS)nL+=w;else if(lossL>lossS)nS+=w;else nT+=w;n+=w;
}
if(n!==4096||nL+nS+nT!==4096)throw Error("mass");
let rS=9*(b*(4-b)+(a-b)**2),rL=9*b*(4-b)+a*(4-a)+(2*(a+1)-3*b)**2,d=rL-rS;
expected.push({world:`A${a}OF4_B${b}OF4`,source_p:`${a}/4`,target_p:`${b}/4`,source_types:64,source_oracle_risk:frac(rS,144),source_laplace_risk:frac(rL,144),target_oracle_risk:frac(b*(4-b),16),population_laplace_minus_source_risk:frac(d,144),empirical_p_laplace_better:frac(nL,4096),empirical_p_source_better:frac(nS,4096),empirical_p_tie:frac(nT,4096),empirical_p_wrong_rank:d===0?null:frac(d>0?nL:nS,4096),laplace_better_weight:nL,source_better_weight:nS,tie_weight:nT,wrong_rank_weight:d===0?null:d>0?nL:nS});
}
const fixed={research_id:"R273_S69",evidence:"E1_ARTIFICIAL_INTERNAL_NONBLIND",source_original_R273_freeze:"91abafbaf627dbf67f86208a82008a5be419e507",s69_protocol_commit:"9051d6e27c1ef17ceff3b49883cbb274d7510871",source_population_pairs:9,ordered_sixbit_source_types:576,probability_denominator:4096,score_denominator:288,source_oracle_truth_informed:true,target_oracle_truth_informed:true,real_human_E2:0,real_historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
if(!doc||typeof doc!=="object"||Array.isArray(doc)||Object.keys(doc).length!==Object.keys(fixed).length+1)throw Error("top coverage");
for(let [key,v] of Object.entries(fixed))if(doc[key]!==v||typeof doc[key]!==typeof v)throw Error("top "+key);
if(!Array.isArray(doc.world_results)||doc.world_results.length!==9)throw Error("world count");
let seen=new Set();
for(let row of doc.world_results){
if(!row||typeof row!=="object"||Array.isArray(row)||seen.has(row.world))throw Error("row duplicate/type");
seen.add(row.world);let e=expected.find(x=>x.world===row.world);if(!e||Object.keys(row).length!==Object.keys(e).length)throw Error("row coverage");
for(let [k,v] of Object.entries(e))if(row[k]!==v||typeof row[k]!==typeof v)throw Error("row "+row.world+" "+k);
}
return {worlds:9,grouped_cells:135,compared_fields:9*Object.keys(expected[0]).length+Object.keys(fixed).length};
}
const fs=require('node:fs');
if(process.argv[2]!=='--check'||!process.argv[3]){console.error('Usage: node b_r273_s69_grouped_oracle_20261030.js --check receipt.json');process.exit(2)}
console.log(JSON.stringify(checkB(JSON.parse(fs.readFileSync(process.argv[3],'utf8')))));
