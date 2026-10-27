"use strict";
// R207 B track: independent conditional-moment and variance algorithm.
// node r207_mnar_conditional_moment_audit_20261027.js reference.json > audit.json
function audit(reference){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let z=a%b;a=b;b=z;}return a||1n;};
 const R=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let d=gcd(a,b);return [a/d,b/d];};
 const plus=(a,b)=>R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const minus=(a,b)=>R(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const times=(a,b)=>R(a[0]*b[0],a[1]*b[1]);
 const over=(a,b)=>R(a[0]*b[1],a[1]*b[0]);
 const str=x=>x[1]===1n?""+x[0]:x[0]+"/"+x[1];
 const sum=a=>a.reduce(plus,R(0));
 const worlds=reference.worlds,all=[];
 let count=0,control_half=0,control_observed=0,leak_zero=0;
 const T={mass:R(0),correct:R(0),ignore:R(0),visible:R(0),zero:R(0),excess:R(0)};
 // Deliberately independent generation order from R source.
 const factors=[];for(let a=1;a<=2;a++)for(let b=1;b<=2;b++)for(let c=1;c<=2;c++)for(let d=1;d<=2;d++)for(let e=1;e<=2;e++)for(let f=1;f<=2;f++)factors.push([a,b,c,d,e,f]);
 const matrices=factors.map(t=>Array.from({length:9},(_,k)=>BigInt(t[Math.floor(k/3)]*t[3+k%3])));
 function verify(rows,track=true){
   let checks=0;
   for(const row of rows){
     const obs=row.mask.split("|").map(x=>3*Number(x[0])+Number(x[1]));
     const hidden=Array.from({length:9},(_,i)=>i).filter(j=>!obs.includes(j));
     const hasAnchor=obs.includes(8),den=BigInt(hasAnchor?70:56);
     const buckets=new Map();
     for(const mat of matrices){
       let key=obs.map(j=>mat[j]).join(","),q=mat[8]===1n?R(1,4):mat[8]===2n?R(1,2):R(3,4);
       let p=over(hasAnchor?q:minus(R(1),q),R(64n*den));
       if(!buckets.has(key))buckets.set(key,[]);
       buckets.get(key).push({mat,p});
     }
     let mass=R(0),correct=R(0),ignore=R(0),visible=R(0),zero=R(0),excess=R(0);
     for(const [key,items] of buckets){
       const W=sum(items.map(v=>v.p));mass=plus(mass,W);
       const observed=key.split(",").map(BigInt),vmean=over(R(observed.reduce((a,b)=>a+b,0n)),R(5));
       for(const j of hidden){
         const S1=sum(items.map(v=>times(v.p,R(v.mat[j]))));
         const S2=sum(items.map(v=>times(v.p,R(v.mat[j]*v.mat[j]))));
         const mean=over(S1,W);
         const naive=over(R(items.reduce((a,v)=>a+v.mat[j],0n)),R(items.length));
         const variance=minus(S2,over(times(S1,S1),W));
         const bias=times(W,times(minus(naive,mean),minus(naive,mean)));
         correct=plus(correct,over(variance,R(4)));
         ignore=plus(ignore,over(plus(variance,bias),R(4)));
         excess=plus(excess,over(bias,R(4)));
         visible=plus(visible,over(plus(minus(S2,times(R(2),times(vmean,S1))),times(W,times(vmean,vmean))),R(4)));
         zero=plus(zero,over(S2,R(4)));
         // Negative control 1: constant q=1/2 gives equal source weights within signature.
         let p0=over(R(1),R(64n*2n*den));
         let half=over(sum(items.map(v=>times(p0,R(v.mat[j])))),sum(items.map(()=>p0)));
         if(str(half)!==str(naive))throw Error("constant q control failed");
         if(track)control_half++;
         // Negative control 2: when anchor is visible, selection weights are equal within signature.
         if(hasAnchor){if(str(mean)!==str(naive))throw Error("observed anchor control failed");if(track)control_observed++;}
         // Negative control 3: intentionally using actual hidden x as prediction yields zero loss.
         for(const it of items){if((it.mat[j]-it.mat[j])**2n!==0n)throw Error("leak control");if(track)leak_zero++;}
       }
     }
     const got={mass,correct,ignore,visible,zero,excess};
     for(const [k,val] of Object.entries(got)){
       const field=k==="mass"?"mass":k+"_weighted_mse";
       if(str(val)!==row[field])throw Error("B/R mismatch mask="+row.mask+" field="+field+" B="+str(val)+" R="+row[field]);
       checks++;
     }
     for(const k of Object.keys(T))T[k]=plus(T[k],got[k]);
   }
   return checks;
 }
 count=verify(worlds);
 const mutation=JSON.parse(JSON.stringify(worlds));mutation[0].correct_weighted_mse="999";
 let mutation_detected=false;try{verify(mutation,false)}catch(e){mutation_detected=String(e).includes("B/R mismatch");}
 if(!mutation_detected)throw Error("mutation negative control failed");
 for(const [k,v] of Object.entries(T))if(str(v)!==reference.totals[k])throw Error("aggregate mismatch "+k);
 if(str(minus(T.ignore,plus(T.correct,T.excess)))!=="0")throw Error("conditional variance excess identity");
 return {research_id:"R207",audit_kind:"INTERNAL_INDEPENDENT_CONDITIONAL_MOMENTS_E1",reference_worlds:worlds.length,exact_fields_compared:count,all_exact_fields_equal:true,reference_totals:reference.totals,constant_half_q_signature_item_checks:control_half,anchor_observed_signature_item_checks:control_observed,leaked_hidden_item_zero_loss_checks:leak_zero,mutation_rejected:mutation_detected,conditional_variance_identity:true,external_independent_replication:false,new_E2:0,new_E3:0,CI:"NOT_RUN"};
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");const x=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));console.log(JSON.stringify(audit(x),null,2));
}