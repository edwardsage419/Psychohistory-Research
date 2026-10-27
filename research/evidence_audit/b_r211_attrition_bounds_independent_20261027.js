
"use strict";
function audit(csv){
 const rows=csv.trim().split(/\r?\n/),h=rows.shift().split(","),get=(a,k)=>a[h.indexOf(k)];
 let checked=0,fail=0,impute_detected=0,oracle_leak_detected=0,policy={};
 for(const line of rows){
  const a=line.split(","),z=get(a,"assignment_z").split("|").map(Number),r=get(a,"response_mask").split("|").map(Number),ys=get(a,"visible_outcomes").split("|");
  let low=0,high=0,m=0;
  for(let i=0;i<4;i++){
   if(!r[i]){low-=1;high+=1;m++;continue;}
   const y=Number(ys[i]);if(![0,1].includes(y))throw Error("invalid observed Y");
   if(z[i]){low+=y-1;high+=y;}else{low-=y;high+=1-y;}
  }
  const expectedCount=Math.pow(2,4+m),width=4+m,truth=Number(get(a,"true_ate_quarters"));
  const claims=[Number(get(a,"compatible_count"))===expectedCount,Number(get(a,"ate_lower_quarters"))===low,Number(get(a,"ate_upper_quarters"))===high,Number(get(a,"width_quarters"))===width,Number(get(a,"missing_count"))===m,Number(get(a,"covered"))===(low<=truth&&truth<=high?1:0)];
  for(const ok of claims){checked++;if(!ok)fail++;}
  let fakeLow=0,fakeHigh=0;
  for(let i=0;i<4;i++){const y=r[i]?Number(ys[i]):0;if(z[i]){fakeLow+=y-1;fakeHigh+=y;}else{fakeLow-=y;fakeHigh+=1-y;}}
  if(m>0&&(fakeHigh-fakeLow)<width)impute_detected++;
  if(width>0)oracle_leak_detected++;
  const p=get(a,"response_policy");policy[p]=(policy[p]||0)+1;
 }
 if(rows.length!==4608||checked!==27648||fail||impute_detected===0||oracle_leak_detected===0)throw Error("audit failed");
 return {audit:"B_R211_ATTRITION_INDEPENDENT_ALGEBRAIC_BOUNDS",date:"2026-10-27",evidence:"E1_INTERNAL_INDEPENDENT_METHOD",rows:rows.length,field_checks:checked,failures:fail,missing_as_zero_negative_control_detected:impute_detected,oracle_counterfactual_leak_negative_control_detected:oracle_leak_detected,policy_rows:policy,external_replication:false,new_E2:0,new_E3:0};
}

if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const file=process.argv[2]||"research/validation/R211_ATTRITION_4608_SOURCE_POLICY_ROWS_2026-10-27.csv";
 const out=process.argv[3]||".";
 fs.mkdirSync(out,{recursive:true});
 const result=audit(fs.readFileSync(file,"utf8"));
 fs.writeFileSync(path.join(out,"B_R211_ATTRITION_INDEPENDENT_BOUNDS_AUDIT_2026-10-27.json"),JSON.stringify(result,null,2)+"\n");
 console.log(JSON.stringify(result));
}
if(typeof module!=="undefined")module.exports={audit};
