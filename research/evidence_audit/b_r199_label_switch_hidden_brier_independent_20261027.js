function runB199(){
 const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);let a=n<0n?-n:n,b=d;while(b){let t=a%b;a=b;b=t}return {n:n/a,d:d/a}};
 const add=(x,y)=>F(x.n*y.d+y.n*x.d,x.d*y.d),sub=(x,y)=>add(x,F(-y.n,y.d)),mul=(x,y)=>F(x.n*y.n,x.d*y.d),div=(x,y)=>F(x.n*y.d,x.d*y.n),eq=(x,y)=>x.n===y.n&&x.d===y.d,str=x=>x.d===1n?""+x.n:x.n+"/"+x.d;
 const z=F(0),o=F(1),half=F(1,2),a=F(3,4);const rows=[];let atomContributions=0,visibleChecks=0,complementChecks=0,reversalDetected=0;
 for(const [source,r] of [["BASE",F(3,4)],["LABEL_SWAPPED",F(1,4)]])for(const L of [3,4]){
  const other=sub(o,r),n=1<<L;let riskTrue=z,riskWrong=z,riskHalf=z,id=z,total=z;
  for(let ym=0;ym<n;ym++){
   const massTrue=Array.from({length:n},()=>z),massWrong=Array.from({length:n},()=>z);
   let py=z,pyWrong=z;
   for(let xm=0;xm<n;xm++){
    let wt=half,ww=half;
    for(let t=0;t<L;t++){
     const x=(xm>>t)&1,y=(ym>>t)&1;
     if(t>0){const stay=x===((xm>>(t-1))&1);wt=mul(wt,stay?a:sub(o,a));ww=mul(ww,stay?a:sub(o,a));}
     wt=mul(wt,x===y?r:sub(o,r));ww=mul(ww,x===y?other:sub(o,other));
    }
    massTrue[xm]=wt;massWrong[xm]=ww;py=add(py,wt);pyWrong=add(pyWrong,ww);atomContributions++;
   }
   if(!eq(py,pyWrong))throw Error("visible pmf differs");visibleChecks++;total=add(total,py);
   for(let t=0;t<L;t++){
    let num=z,numWrong=z;
    for(let xm=0;xm<n;xm++)if((xm>>t)&1){num=add(num,massTrue[xm]);numWrong=add(numWrong,massWrong[xm]);}
    const p=div(num,py),q=div(numWrong,pyWrong);
    if(!eq(add(p,q),o))throw Error("hidden complement differs");complementChecks++;
    const diff=mul(sub(p,q),sub(p,q));id=add(id,div(mul(py,diff),F(L)));
    for(let xm=0;xm<n;xm++){
     const label=(xm>>t)&1,wt=div(massTrue[xm],F(L)),q0=label?o:z;
     riskTrue=add(riskTrue,mul(wt,mul(sub(p,q0),sub(p,q0))));
     riskWrong=add(riskWrong,mul(wt,mul(sub(q,q0),sub(q,q0))));
     riskHalf=add(riskHalf,mul(wt,mul(sub(half,q0),sub(half,q0))));
    }
   }
  }
  if(!eq(total,o)||!eq(sub(riskWrong,riskTrue),id)||!eq(riskHalf,F(1,4)))throw Error("B loss identity failure");
  if(riskWrong.n*riskTrue.d>riskTrue.n*riskWrong.d)reversalDetected++;else throw Error("label reversal not detected");
  rows.push({true_source:source,L,observed_sequence_count:n,source_mass:str(total),oracle_hidden_Brier:str(riskTrue),opposite_label_hidden_Brier:str(riskWrong),unconditional_half_hidden_Brier:str(riskHalf),opposite_excess_Brier:str(sub(riskWrong,riskTrue)),oracle_gain_over_half:str(sub(riskHalf,riskTrue)),squared_posterior_complement_identity:str(id)});
 }
 return {research_id:"R199",audit_method:"complete_hidden_observed_joint_enumeration_and_direct_hidden_Brier",comparison_worlds:4,full_hidden_observed_joint_atom_contributions:atomContributions,observed_likelihood_equal_checks:visibleChecks,posterior_complement_checks:complementChecks,wrong_label_negative_controls:reversalDetected,rows,external_replication:false};
}
if(typeof require!=='undefined' && require.main===module){console.log(JSON.stringify(runB199(),null,2));}
