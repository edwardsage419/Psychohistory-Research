/* R273 S69 complete finite paired target score source enumeration; Node 18+ standard library. */
function runS69(){
const vals=[1,2,3],pow=(a,n)=>a**n,gcd=(x,y)=>{while(y){let t=x%y;x=y;y=t;}return x<0n?-x:x},rat=(x,y)=>{x=BigInt(x);y=BigInt(y);if(y<0n){x=-x;y=-y;}let d=gcd(x,y);return (x/d).toString()+(y/d===1n?"":"/"+(y/d).toString())};
let csv=["world,sixbits,weight_num_4096,source_forecast_num_12,laplace_forecast_num_12,source_score_num_288,laplace_score_num_288,paired_outcome"];
let results=[];
for(const a of vals)for(const b of vals){
let mass=0,L=0,S=0,T=0,rL=0n,rS=0n;
for(let i=0;i<64;i++){
const bits=i.toString(2).padStart(6,"0"),k=[...bits.slice(0,4)].reduce((s,c)=>s+Number(c),0),j=Number(bits[4])+Number(bits[5]);
const weight=pow(a,k)*pow(4-a,4-k)*pow(b,j)*pow(4-b,2-j);
const qs=3*a,ql=2*(k+1);
const score=q=>[bits[4],bits[5]].reduce((s,y)=>s+(12*Number(y)-q)**2,0);
const ls=score(qs),ll=score(ql);
let o=ll<ls?"L_BETTER":ll>ls?"S_BETTER":"TIE";
mass+=weight;if(o==="L_BETTER")L+=weight;else if(o==="S_BETTER")S+=weight;else T+=weight;
rS+=BigInt(weight*ls);rL+=BigInt(weight*ll);
csv.push([`A${a}OF4_B${b}OF4`,bits,weight,qs,ql,ls,ll,o].join(","));
}
if(mass!==4096||L+S+T!==4096)throw Error("mass");
const sN=9*(b*(4-b)+(a-b)**2),lN=9*b*(4-b)+a*(4-a)+(2*(a+1)-3*b)**2,dN=lN-sN;
if(rS!==BigInt(sN)*8192n||rL!==BigInt(lN)*8192n)throw Error("analytic mismatch "+a+" "+b);
if(a===b&&dN<=0)throw Error("same population oracle expected bound");
const wrong=dN===0?null:(dN>0?L:S);
results.push({world:`A${a}OF4_B${b}OF4`,source_p:`${a}/4`,target_p:`${b}/4`,source_types:64,
source_oracle_risk:rat(sN,144),source_laplace_risk:rat(lN,144),target_oracle_risk:rat(b*(4-b),16),
population_laplace_minus_source_risk:rat(dN,144),empirical_p_laplace_better:rat(L,4096),empirical_p_source_better:rat(S,4096),empirical_p_tie:rat(T,4096),
empirical_p_wrong_rank:wrong===null?null:rat(wrong,4096),laplace_better_weight:L,source_better_weight:S,tie_weight:T,wrong_rank_weight:wrong});
}
return {json:{research_id:"R273_S69",evidence:"E1_ARTIFICIAL_INTERNAL_NONBLIND",source_original_R273_freeze:"91abafbaf627dbf67f86208a82008a5be419e507",s69_protocol_commit:"9051d6e27c1ef17ceff3b49883cbb274d7510871",source_population_pairs:9,ordered_sixbit_source_types:576,probability_denominator:4096,score_denominator:288,source_oracle_truth_informed:true,target_oracle_truth_informed:true,real_human_E2:0,real_historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",world_results:results},csv:csv.join("\n")+"\n"};
}
const result=runS69();
if(process.argv.includes('--json'))process.stdout.write(JSON.stringify(result.json,null,2)+'\n');
else if(process.argv.includes('--csv'))process.stdout.write(result.csv);
else if(process.argv.includes('--selftest')){if(result.json.world_results.length!==9||result.csv.trim().split('\n').length!==577)process.exit(1);process.stdout.write('PASS 9 worlds, 576 sources, analytic identities\n');}
else {console.error('Usage: node r273_s69_paired_target_rank_20261030.js --json|--csv|--selftest');process.exit(2);}
