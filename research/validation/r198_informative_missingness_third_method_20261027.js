function runR198(){
 const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}let a=n<0n?-n:n,b=d;while(b){let t=a%b;a=b;b=t}return {n:n/a,d:d/a}};
 const add=(x,y)=>F(x.n*y.d+y.n*x.d,x.d*y.d), neg=x=>F(-x.n,x.d), sub=(x,y)=>add(x,neg(y)),mul=(x,y)=>F(x.n*y.n,x.d*y.d),div=(x,y)=>F(x.n*y.d,x.d*y.n),str=x=>x.d===1n?""+x.n:x.n+"/"+x.d,eq=(x,y)=>x.n===y.n&&x.d===y.d;
 const z=F(0),o=F(1),half=F(1,2);
 const aa=[F(1,2),F(3,4),F(1,4),F(11,18)],rr=[F(3,4),F(7,8)];
 const emit=(x,y,r)=>x===y?r:sub(o,r);
 const trans=(p,a)=>add(mul(sub(o,p),sub(o,a)),mul(p,a));
 const nextY=(p,a,r)=>add(sub(o,r),mul(sub(mul(F(2),r),o),trans(p,a)));
 const risk=(p,q)=>add(mul(p,mul(sub(o,q),sub(o,q))),mul(sub(o,p),mul(q,q)));
 const rows=[];
 for(const a of aa)for(const r of rr)for(const T of [4,5])for(const scheme of ["MCAR","INFORMATIVE"]){
  const m0=scheme==="MCAR"?half:F(1,4),m1=scheme==="MCAR"?half:F(3,4);
  let total=z,pmiss=z,ra=z,ri=z,rmA=z,rmI=z,identity=z;
  const n=1<<(T-1);
  for(let h=0;h<n;h++){
   let p=half,ph=o;
   for(let t=0;t<T-1;t++){
    const y=(h>>t)&1;const prior=trans(p,a);
    const py=add(mul(prior,emit(1,y,r)),mul(sub(o,prior),emit(0,y,r)));
    ph=mul(ph,py);p=div(mul(prior,emit(1,y,r)),py);
   }
   const priorT=trans(p,a);
   const l1=add(mul(r,m1),mul(sub(o,r),m0));
   const l0=add(mul(sub(o,r),m1),mul(r,m0));
   const pm=add(mul(priorT,l1),mul(sub(o,priorT),l0));
   const pmass=mul(ph,pm);
   const post=div(mul(priorT,l1),pm);
   const ptrue=nextY(post,a,r),qignore=nextY(priorT,a,r);
   const vAware=risk(ptrue,ptrue),vIgnore=risk(ptrue,qignore);
   total=add(total,pmass);pmiss=add(pmiss,pmass);
   const cA=mul(pmass,vAware),cI=mul(pmass,vIgnore);
   ra=add(ra,cA);ri=add(ri,cI);rmA=add(rmA,cA);rmI=add(rmI,cI);
   identity=add(identity,mul(pmass,mul(sub(ptrue,qignore),sub(ptrue,qignore))));
   for(let y=0;y<=1;y++){
    const py=add(mul(priorT,emit(1,y,r)),mul(sub(o,priorT),emit(0,y,r)));
    const q=nextY(div(mul(priorT,emit(1,y,r)),py),a,r);
    const mass=mul(mul(ph,py),sub(o,y===1?m1:m0));
    total=add(total,mass);
    const v=mul(mass,risk(q,q));ra=add(ra,v);ri=add(ri,v);
   }
  }
  if(!eq(total,o)||!eq(pmiss,half)||!eq(sub(ri,ra),identity))throw Error("mass or risk identity failed "+str(a)+" "+str(r)+" "+T+" "+scheme);
  const excess=sub(ri,ra);
  if(scheme==="MCAR"&&!eq(excess,z))throw Error("MCAR nonzero");
  if(eq(a,half)&&!eq(excess,z))throw Error("independent-state nonzero");
  rows.push({a:str(a),r:str(r),T,scheme,visible_prefix_histories:n,missing_probability:str(pmiss),aware_Brier:str(ra),ignore_missingness_Brier:str(ri),excess_Brier:str(excess),missing_conditional_aware_Brier:str(div(rmA,pmiss)),missing_conditional_ignore_Brier:str(div(rmI,pmiss)),squared_prediction_gap_identity:str(identity)});
 }
 return {research_id:"R198",kind:"prespecified_postscore_internal_E1_informative_missingness",freeze_commit:"c9e3c76157caddb34c494782acd6ab6994b4268c",worlds:16,comparisons:rows.length,source:"R198 original a,r,T grid; new frozen missingness channels",rows,actual_human_E2:0,actual_historical_E3:0,external_replication:0};
}
if(typeof require!=='undefined' && require.main===module){console.log(JSON.stringify(runR198(),null,2));}
