"use strict";
// R188 prespecified complete group deletion sensitivity, exact BigInt rational arithmetic.
// Node: node research/validation/r188_loco_cluster_deletion_20261026.js
// The source data remain artificial. No resampling, statistical significance, or model refitting.
function calculate(original) {
  const abs=x=>x<0n?-x:x;
  function gcd(a,b){a=abs(a);b=abs(b);while(b){let z=a%b;a=b;b=z;}return a||1n;}
  function R(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
  const add=(a,b)=>R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const neg=a=>[-a[0],a[1]];
  const sub=(a,b)=>add(a,neg(b));
  const mul=(a,b)=>R(a[0]*b[0],a[1]*b[1]);
  const div=(a,b)=>R(a[0]*b[1],a[1]*b[0]);
  const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
  const parse=s=>{const p=String(s).split("/");return R(p[0],p.length>1?p[1]:1);};
  const fmt=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
  const sign=a=>a[0]<0n?-1:a[0]>0n?1:0;
  const zero=R(0),one=R(1),eight=R(8),half=R(1,2);
  const thetas=["0","1/2","3/4","1"];
  if(!original||!Array.isArray(original.all_worlds)||original.all_worlds.length!==180)throw Error("wrong frozen source");
  function makeRows(w){
    const a=parse(w.true_a),b=parse(w.true_within_b),c=parse(w.true_context_c),e=parse(w.original_error_magnitude);
    const groups=[];
    for(let g=0;g<6;g++){
      const k=w.group_exposure_count_k[g],p=R(k,8),rows=[];
      for(const [x,n] of [[0,8-k],[1,k]]){
        for(let j=0;j<n;j++){
          const eps=j<n/2?e:neg(e);
          const y=add(add(add(a,mul(b,R(x))),mul(c,p)),eps);
          rows.push({x:R(x),y});
        }
      }
      if(rows.length!==8)throw Error("wrong group rows");
      groups.push(rows);
    }
    return groups;
  }
  function directSlope(groups,theta){
    const q=parse(theta),keep=groups.flat(),N=R(keep.length);
    let sx=zero,sy=zero,sxx=zero,sxy=zero;
    for(const group of groups){
      let mx=zero,my=zero;
      for(const row of group){mx=add(mx,row.x);my=add(my,row.y);}
      mx=div(mx,eight);my=div(my,eight);
      for(const row of group){
        const x=sub(row.x,mul(q,mx)),y=sub(row.y,mul(q,my));
        sx=add(sx,x);sy=add(sy,y);
        sxx=add(sxx,mul(x,x));sxy=add(sxy,mul(x,y));
      }
    }
    const Sxx=sub(sxx,div(mul(sx,sx),N)),Sxy=sub(sxy,div(mul(sx,sy),N));
    if(Sxx[0]===0n)throw Error("singular leave group out");
    return div(Sxy,Sxx);
  }
  let fullChecks=0, deletionChecks=0, feChecks=0, balancedChecks=0, signFlips=0;
  let maxDelta=zero,maxCase=null, fullPooledNeg=0, deletionPooledNeg=0, changesToPooledSign=0;
  const results=[];
  for(let wi=0;wi<180;wi++){
    const w=original.all_worlds[wi],groups=makeRows(w),b=parse(w.true_within_b);
    const full=[];
    for(const theta of thetas){
      const got=directSlope(groups,theta),arch=parse(w.quasi_demeaning_theta_to_slope[theta]);
      if(!eq(got,arch))throw Error("original full sample mismatch world "+wi+" theta "+theta);
      full.push(fmt(got));fullChecks++;
    }
    if(sign(parse(full[0]))<0)fullPooledNeg++;
    const omissions=[];
    for(let omit=0;omit<6;omit++){
      const kept=groups.filter((_,i)=>i!==omit),slopes=[];
      for(let ti=0;ti<4;ti++){
        const theta=thetas[ti],s=directSlope(kept,theta),baseline=parse(full[ti]);
        if(theta==="1"){if(!eq(s,b))throw Error("within slope drift");feChecks++;}
        if(w.design==="BALANCED"){if(!eq(s,b))throw Error("balanced slope drift");balancedChecks++;}
        if(sign(s)!==sign(baseline))signFlips++;
        const delta=sub(s,baseline),mag=R(abs(delta[0]),delta[1]);
        if(mag[0]*maxDelta[1]>maxDelta[0]*mag[1]){maxDelta=mag;maxCase={world:wi,omit,theta,full:full[ti],deleted:fmt(s)};}
        if(ti===0){if(sign(s)<0)deletionPooledNeg++;if(sign(s)!==sign(baseline))changesToPooledSign++;}
        slopes.push(fmt(s));deletionChecks++;
      }
      omissions.push(slopes);
    }
    results.push({world:wi,design:w.design,a:w.true_a,b:w.true_within_b,c:w.true_context_c,e:w.original_error_magnitude,k:w.group_exposure_count_k,full,deleted:omissions});
  }
  if(fullChecks!==720||deletionChecks!==4320||feChecks!==1080||balancedChecks!==1440)throw Error("count mismatch");
  return {research_id:"R188",method:"exact_full_group_deletion_direct_row_OLS",evidence:"E1_ARTIFICIAL_ONLY",original_results_git_blob:"9d57c24f6327f1e0ce5c83cba4d55174bded1292",freeze_commit:"2f57fdc83bf51966baacfd7b35b79c4a647b434b",thetas,world_count:180,group_count:6,rows_per_world:48,rows_per_deletion:40,full_checks:fullChecks,deletion_checks:deletionChecks,fe_checks:feChecks,balanced_checks:balancedChecks,sign_flips_all_thetas:signFlips,full_pooled_negative_worlds:fullPooledNeg,deletion_pooled_negative_cases:deletionPooledNeg,pooled_sign_changed_on_deletion:changesToPooledSign,max_abs_deletion_delta:fmt(maxDelta),max_delta_case:maxCase,worlds:results};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
  const fs=require("fs"),path=require("path");
  const root=path.resolve(__dirname,"../..");
  const original=JSON.parse(fs.readFileSync(path.join(root,"research/R188/R188_EXACT_RESULTS.json"),"utf8"));
  process.stdout.write(JSON.stringify(calculate(original),null,2)+"\n");
}
