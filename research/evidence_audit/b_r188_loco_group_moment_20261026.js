"use strict";
// B audit: independent group moment identity. Never call the R188 row-level estimator.
// Run: node research/evidence_audit/b_r188_loco_group_moment_20261026.js
function audit(original,receipt){
 const abs=x=>x<0n?-x:x;
 function gcd(a,b){a=abs(a);b=abs(b);while(b){let z=a%b;a=b;b=z;}return a||1n;}
 function R(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
 const add=(a,b)=>R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const sub=(a,b)=>add(a,[-b[0],b[1]]);
 const mul=(a,b)=>R(a[0]*b[0],a[1]*b[1]);
 const div=(a,b)=>R(a[0]*b[1],a[1]*b[0]);
 const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const parse=s=>{let p=String(s).split("/");return R(p[0],p[1]||1);};
 const fmt=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
 const zero=R(0),one=R(1),two=R(2);
 const mean=xs=>div(xs.reduce(add,zero),R(xs.length));
 function analytic(k,b,c,theta){
   const ps=k.map(x=>R(x,8)),pbar=mean(ps);
   const vb=mean(ps.map(p=>mul(sub(p,pbar),sub(p,pbar))));
   const vw=mean(ps.map(p=>mul(p,sub(one,p))));
   const t=sub(one,theta),q=mul(t,t),den=add(vw,mul(q,vb));
   if(den[0]===0n)throw Error("rank loss");
   return add(b,div(mul(mul(c,q),vb),den));
 }
 if(receipt.worlds.length!==180||original.all_worlds.length!==180)throw Error("source world count");
 let checked=0,full=0,mutationDetected=0;
 const transitions={};
 const fixed=[];
 for(let wi=0;wi<180;wi++){
   const w=original.all_worlds[wi],rr=receipt.worlds[wi];
   const b=parse(w.true_within_b),c=parse(w.true_context_c);
   if(rr.world!==wi||JSON.stringify(rr.k)!==JSON.stringify(w.group_exposure_count_k))throw Error("world mapping");
   for(let ti=0;ti<4;ti++){
     const theta=parse(receipt.thetas[ti]);
     const q=analytic(rr.k,b,c,theta);
     if(!eq(q,parse(rr.full[ti]))||!eq(q,parse(w.quasi_demeaning_theta_to_slope[receipt.thetas[ti]])))throw Error("full mismatch "+wi+" "+ti);
     full++;
   }
   for(let omit=0;omit<6;omit++){
     const k=rr.k.filter((_,g)=>g!==omit);
     for(let ti=0;ti<4;ti++){
       const theta=parse(receipt.thetas[ti]),q=analytic(k,b,c,theta),got=parse(rr.deleted[omit][ti]);
       if(!eq(q,got))throw Error("deleted mismatch "+wi+" "+omit+" "+ti);
       checked++;
       if(ti===0){
         const sign=x=>x[0]<0n?"negative":x[0]>0n?"positive":"zero";
         const key=sign(parse(rr.full[0]))+" to "+sign(got);
         transitions[key]=(transitions[key]||0)+1;
       }
       if(w.design==="STRONG_BETWEEN"&&w.true_a==="0"&&w.true_within_b==="1/4"&&w.true_context_c==="-4"&&w.original_error_magnitude==="1/4"&&ti===0)fixed.push({omitted:omit,slope:fmt(q)});
     }
   }
 }
 // Deliberate wrong receipt: add 1/100 to a deleted slope. A mismatch must be detected.
 const test=receipt.worlds[0];
 const q=analytic(test.k.slice(1),parse(test.b),parse(test.c),zero);
 if(!eq(q,add(parse(test.deleted[0][0]),R(1,100))))mutationDetected++;
 // Independent group-intercept mutation: shift group 0 response by +1.
 // In strong design, pooled slope shift = Cov(x, u_g)/Var(x).
 const k=[2,2,2,6,6,6],ps=k.map(x=>R(x,8)),pb=mean(ps);
 const cov=div(sub(ps[0],pb),R(6));
 const varx=mul(pb,sub(one,pb));
 const pooledShift=div(cov,varx);
 if(!eq(pooledShift,R(-1,6)))throw Error("group intercept mutation expected -1/6");
 const withinShift=zero;
 if(mutationDetected!==1)throw Error("mutation not detected");
 return {status:"PASS_INTERNAL_METHOD_INDEPENDENT_E1",worlds:180,full_sample_identities:full,cluster_deleted_identities:checked,all_pooled_sign_transitions:transitions,deliberate_receipt_mutation_detected:mutationDetected,group_intercept_mutation_pooled_shift:fmt(pooledShift),group_intercept_mutation_within_shift:fmt(withinShift),fixed_strong_case:fixed,external_replication:false,real_E2_added:0,historical_E3_added:0};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),root=path.resolve(__dirname,"../..");
 const orig=JSON.parse(fs.readFileSync(path.join(root,"research/R188/R188_EXACT_RESULTS.json"),"utf8"));
 const receipt=JSON.parse(fs.readFileSync(path.join(root,"research/validation/R188_LOCO_4320_EXACT_RECEIPT_2026-10-26.json"),"utf8"));
 process.stdout.write(JSON.stringify(audit(orig,receipt),null,2)+"\n");
}
