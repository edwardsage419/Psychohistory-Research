// R235 S31 B audit. Reads original R235 frozen observable joint and S31 receipt; no original latent CSV.
// Usage: node research/evidence_audit/b_r235_s31_independent_stratum_odds_20261028.js research/R235/R235_EXACT_RESULTS.json /tmp/r235_s31.json
const fs=require("node:fs");
function audit(original,receipt) {
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a};
 const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}if(d===0n)throw Error("zero denominator");const g=gcd(n,d);return {n:n/g,d:d/g}};
 const P=s=>{const x=String(s).split("/");return Q(x[0],x[1]||"1")};
 const A=(a,b)=>Q(a.n*b.d+b.n*a.d,a.d*b.d),M=(a,b)=>Q(a.n*b.n,a.d*b.d),D=(a,b)=>Q(a.n*b.d,a.d*b.n),S=(a,b)=>A(a,Q(-b.n,b.d)),T=a=>a.d===1n?String(a.n):a.n+"/"+a.d;
 const ZERO=Q(0),ONE=Q(1),HALF=Q(1,2);
 const w=(rule,g,y)=>{
   switch(rule){
     case "ALL":return ONE;
     case "G1_SUCCESS_HALF":return g===1&&y===1?HALF:ONE;
     case "G1_FAILURE_HALF":return g===1&&y===0?HALF:ONE;
     case "CONCORDANT_HALF":return g===y?HALF:ONE;
     case "DISCORDANT_HALF":return g!==y?HALF:ONE;
     default:throw Error("invalid rule");
   }
 };
 let checks=0;
 const check=(got,expected,label)=>{checks++;if(got!==expected)throw Error("B audit mismatch "+label+" "+got+" != "+expected)};
 check(receipt.conditions,45,"conditions");
 for(const world of original.world_results){
   const baseline=world.full_observed_group_three_item_joint_signature;
   for(const rule of receipt.rules){
     const row=receipt.conditions_data.find(x=>x.world===world.world&&x.rule===rule);
     if(!row)throw Error("missing condition");
     const weighted={};let z=ZERO;
     for(const [key,v] of Object.entries(baseline)){
       const g=Number(key[0]),y=Number(key[2]);
       weighted[key]=M(P(v),w(rule,g,y));
       z=A(z,weighted[key]);
     }
     check(row.retention_probability,T(z),world.world+" "+rule+" retention");
     const selected=Object.fromEntries(Object.entries(weighted).map(([key,v])=>[key,D(v,z)]));
     const group=[ZERO,ZERO],succ=[ZERO,ZERO],tabs=Array.from({length:3},()=>[[ZERO,ZERO],[ZERO,ZERO]]);
     for(const [key,v] of Object.entries(selected)){
       check(row.selected_joint[key],T(v),world.world+" "+rule+" "+key);
       const g=Number(key[0]),y=Number(key[2]),s=Number(key[1])+Number(key[3]);
       group[g]=A(group[g],v);
       if(y)succ[g]=A(succ[g],v);
       tabs[s][g][y]=A(tabs[s][g][y],v);
     }
     for(let g=0;g<2;g++){
       check(row.group_masses[g],T(group[g]),"group mass");
       check(row.focal_success_rates_by_group[g],T(D(succ[g],group[g])),"focal rate");
     }
     let num=ZERO,den=ZERO;
     for(let s=0;s<3;s++){
       const t=tabs[s],a=t[1][1],b=t[1][0],c=t[0][1],d=t[0][0];
       const n=A(A(a,b),A(c,d));
       const odds=D(M(a,d),M(b,c));
       const harmonicWeight=D(M(b,c),n);
       num=A(num,M(odds,harmonicWeight));
       den=A(den,harmonicWeight);
       check(row.anchor_score_focal_differences[s],T(S(D(a,A(a,b)),D(c,A(c,d)))),"stratum "+s);
     }
     check(row.mh_odds_ratio,T(D(num,den)),"MH");
     for(let i=0;i<3;i++)check(row.oracle_fixed_ability_dif_unchanged[i],world.oracle_fixed_ability_group1_minus_group0_focal_probabilities[i],"oracle");
   }
 }
 return {status:"PASS",checks,worlds:9,conditions:45,independent_route:"original frozen 16-cell observable joint to analytic stratum odds weighted average",external_independent_replication:false,E1:true,E2:0,E3:0};
}
if(require.main===module){if(process.argv.length!==4)throw Error("supply frozen original results JSON and S31 receipt JSON");const original=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));const receipt=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));const r=audit(original,receipt);const bad=JSON.parse(JSON.stringify(receipt));bad.conditions_data[1].mh_odds_ratio="999";let detected=false;try{audit(original,bad)}catch(e){detected=true}if(!detected)throw Error("negative control failed");process.stdout.write(JSON.stringify({...r,negative_control_detected:true},null,2)+"\n");}
module.exports={audit};
