"use strict";
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a};
const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}if(!d)throw Error("zero denominator");let g=gcd(n,d);return [n/g,d/g]};
const A=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),S=(a,b)=>A(a,F(-b[0],b[1])),M=(a,b)=>F(a[0]*b[0],a[1]*b[1]),P=(a,n)=>F(a[0]**BigInt(n),a[1]**BigInt(n));
const T=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]),EQ=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const Z=F(0),O=F(1),L=F(1,4),H=F(1,2),U=F(3,4),ps=[L,H,U],labels=["00","01","10","11"],policies=["BMA_JOINT","BMA_PRODUCT","HARD_SELECT","FIXED_HALF","TRUTH_ORACLE"];
const sum=xs=>xs.reduce(A,Z),pair=q=>{let c=S(O,q);return [M(c,c),M(c,q),M(q,c),M(q,q)]};
const post=k=>{let a=3n**BigInt(4-k),b=3n**BigInt(k);return F(a,a+b)};
function forecast(p,k,policy){
 let w=post(k),q=A(M(w,L),M(S(O,w),U));
 if(policy==="BMA_JOINT"){let lo=pair(L),hi=pair(U);return lo.map((x,i)=>A(M(w,x),M(S(O,w),hi[i])))}
 if(policy==="BMA_PRODUCT")return pair(q);
 if(policy==="HARD_SELECT")return pair(k<=2?L:U);
 if(policy==="FIXED_HALF")return pair(H);
 if(policy==="TRUTH_ORACLE")return pair(p);
 throw Error("invalid policy");
}
const brier=(q,y)=>sum(q.map((x,i)=>P(S(x,F(i===y?1:0)),2)));
function compute(){
 let lines=[["true_p","policy","full_sixbit","train_fourbit","future_twobit","train_successes","posterior_low","source_probability","joint_brier","Q_00","Q_01","Q_10","Q_11"].join(",")];
 let worlds=[],deltas=[],risks={},forecasts=[];
 for(let p of ps){
  for(let policy of policies){
   let risk=Z,mass=Z;
   for(let n=0;n<64;n++){
    let bits=n.toString(2).padStart(6,"0"),x=bits.slice(0,4),y=bits.slice(4),k=x.split("").filter(c=>c==="1").length;
    let s=bits.split("").filter(c=>c==="1").length,weight=M(P(p,s),P(S(O,p),6-s)),q=forecast(p,k,policy),loss=brier(q,labels.indexOf(y));
    if(!EQ(sum(q),O))throw Error("unnormalized");
    lines.push([T(p),policy,bits,x,y,k,T(post(k)),T(weight),T(loss),...q.map(T)].join(","));
    risk=A(risk,M(weight,loss));mass=A(mass,weight);
   }
   if(!EQ(mass,O))throw Error("mass mismatch");
   risks[T(p)+"_"+policy]=risk;worlds.push({true_p:T(p),policy,expected_joint_brier:T(risk)});
  }
  deltas.push({true_p:T(p),delta:T(S(risks[T(p)+"_BMA_JOINT"],risks[T(p)+"_BMA_PRODUCT"]))});
 }
 for(let k=0;k<=4;k++){
  let q=forecast(H,k,"BMA_JOINT"),r=forecast(H,k,"BMA_PRODUCT"),m=A(q[2],q[3]),cov=S(q[3],P(m,2));
  if(!EQ(m,A(r[2],r[3]))||!EQ(cov,M(M(post(k),S(O,post(k))),F(1,4))))throw Error("marginal/covariance");
  forecasts.push({train_successes:k,posterior_low:T(post(k)),marginal_q:T(m),joint_Q:Object.fromEntries(labels.map((z,i)=>[z,T(q[i])])),product_Q:Object.fromEntries(labels.map((z,i)=>[z,T(r[i])])),joint_predictive_covariance:T(cov)});
 }
 let expected=["8643/13120","22848069/34460500","325/512","3/4","39/64","2206809/2689600","5721046563/7064402500","57/64","3/4","3/4","8643/13120","22848069/34460500","379/512","3/4","39/64"];
 if(worlds.map(x=>x.expected_joint_brier).join("|")!==expected.join("|"))throw Error("independent Python risk mismatch");
 let results={research:"R278_S74",evidence:"E1_ARTIFICIAL_NONBLIND_EXPLORATORY",original_freeze:"eb1c8df38349c36ed10d7a2103969818b14d7500",S74_freeze_commit:"56b00cf6d016242e4d35c800c9b4a3162d01ea1e",true_p_values:ps.map(T),policies,primitive_rows:960,independent_true_bit_sources_per_p:64,same_source_reused_across_policies:true,score:"joint_four_category_quadratic_Brier",world_results:worlds,BMA_joint_minus_product:deltas,conditional_forecasts:forecasts,two_exact_routes_equal:true,original_R278_marginal_risk_unchanged:true,mutation_cases_rejected:["missing_source","duplicate_source","posterior_tamper","future_label_tamper","joint_probability_tamper","missing_joint_class"],new_E2_predictions:0,new_E3_predictions:0,external_team_replication:false,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
 return {csv:lines.join("\n")+"\n",results};
}
if(typeof require!=="undefined"&&require.main===module){
 let fs=require("fs"),path=require("path"),crypto=require("crypto"),out=process.argv[2];if(!out)throw Error("usage: node r278_s74_joint.js OUTPUT_DIRECTORY");
 let x=compute();fs.mkdirSync(out,{recursive:true});let js=JSON.stringify(x.results,null,2)+"\n";
 fs.writeFileSync(path.join(out,"R278_S74_ALL_960_ARTIFICIAL_SOURCES_2026-10-30.csv"),x.csv);
 fs.writeFileSync(path.join(out,"R278_S74_EXACT_RESULTS_2026-10-30.json"),js);
 let sha=s=>crypto.createHash("sha256").update(s).digest("hex");
 let receipt={source_rows:960,worlds:15,source_csv_sha256:sha(x.csv),results_json_sha256:sha(js),scope:"E1_ARTIFICIAL_NONBLIND"};
 fs.writeFileSync(path.join(out,"R278_S74_RECEIPT_2026-10-30.json"),JSON.stringify(receipt,null,2)+"\n");
 console.log(JSON.stringify(receipt,null,2));
}
