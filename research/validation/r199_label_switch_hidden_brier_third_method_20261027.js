function runR199(){
 const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);let a=n<0n?-n:n,b=d;while(b){let t=a%b;a=b;b=t}return {n:n/a,d:d/a}};
 const add=(x,y)=>F(x.n*y.d+y.n*x.d,x.d*y.d),sub=(x,y)=>add(x,F(-y.n,y.d)),mul=(x,y)=>F(x.n*y.n,x.d*y.d),div=(x,y)=>F(x.n*y.d,x.d*y.n),eq=(x,y)=>x.n===y.n&&x.d===y.d,str=x=>x.d===1n?""+x.n:x.n+"/"+x.d;
 const z=F(0),o=F(1),half=F(1,2),a=F(3,4),sources=[["BASE",F(3,4)],["LABEL_SWAPPED",F(1,4)]];
 const emission=(x,y,r)=>x===y?r:sub(o,r);
 const smooth=(ym,L,r)=>{
  const al=[],be=[];al[0]=[mul(half,emission(0,ym&1,r)),mul(half,emission(1,ym&1,r))];
  for(let t=1;t<L;t++){const y=(ym>>t)&1;al[t]=[mul(emission(0,y,r),add(mul(al[t-1][0],a),mul(al[t-1][1],sub(o,a)))),mul(emission(1,y,r),add(mul(al[t-1][1],a),mul(al[t-1][0],sub(o,a))))];}
  be[L-1]=[o,o];
  for(let t=L-2;t>=0;t--){const y=(ym>>(t+1))&1;be[t]=[add(mul(mul(a,emission(0,y,r)),be[t+1][0]),mul(mul(sub(o,a),emission(1,y,r)),be[t+1][1])),add(mul(mul(sub(o,a),emission(0,y,r)),be[t+1][0]),mul(mul(a,emission(1,y,r)),be[t+1][1]))];}
  const py=add(al[L-1][0],al[L-1][1]);
  return {py,posterior:Array.from({length:L},(_,t)=>div(mul(al[t][1],be[t][1]),py))};
 };
 const rows=[];let complementChecks=0,observedChecks=0;
 for(const [source,r] of sources)for(const L of [3,4]){
  const other=sub(o,r);let pMass=z,oracle=z,opposite=z,neutral=z,identity=z;
  for(let ym=0;ym<(1<<L);ym++){
   const u=smooth(ym,L,r),v=smooth(ym,L,other);
   if(!eq(u.py,v.py))throw Error("visible likelihood mismatch");observedChecks++;
   pMass=add(pMass,u.py);
   for(let t=0;t<L;t++){
    const p=u.posterior[t],q=v.posterior[t];
    if(!eq(add(p,q),o))throw Error("posterior complement failed");complementChecks++;
    const base=mul(p,sub(o,p));
    const gap=mul(sub(q,p),sub(q,p));
    const w=div(u.py,F(L));
    oracle=add(oracle,mul(w,base));
    opposite=add(opposite,mul(w,add(base,gap)));
    neutral=add(neutral,mul(w,F(1,4)));
    identity=add(identity,mul(w,mul(sub(o,mul(F(2),p)),sub(o,mul(F(2),p)))));
   }
  }
  if(!eq(pMass,o)||!eq(sub(opposite,oracle),identity)||!eq(neutral,F(1,4)))throw Error("risk or normalization failed");
  rows.push({true_source:source,L,observed_sequence_count:1<<L,source_mass:str(pMass),oracle_hidden_Brier:str(oracle),opposite_label_hidden_Brier:str(opposite),unconditional_half_hidden_Brier:str(neutral),opposite_excess_Brier:str(sub(opposite,oracle)),oracle_gain_over_half:str(sub(neutral,oracle)),squared_posterior_complement_identity:str(identity)});
 }
 return {research_id:"R199",method:"forward_backward_hidden_state_smoothing",freeze_commit:"08f1a96574f93f296fa4dc461a310198c0d051c2",true_sources:2,comparison_worlds:4,observed_likelihood_equal_checks:observedChecks,posterior_complement_checks:complementChecks,rows,scope:"in_sequence_artificial_hidden_label_inference_E1",new_E2:0,new_E3:0};
}
if(typeof require!=='undefined' && require.main===module){console.log(JSON.stringify(runR199(),null,2));}
