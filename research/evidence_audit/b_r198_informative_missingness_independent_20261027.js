function runB198(){
 const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}let a=n<0n?-n:n,b=d;while(b){let t=a%b;a=b;b=t}return {n:n/a,d:d/a}};
 const add=(x,y)=>F(x.n*y.d+y.n*x.d,x.d*y.d),sub=(x,y)=>add(x,F(-y.n,y.d)),mul=(x,y)=>F(x.n*y.n,x.d*y.d),div=(x,y)=>F(x.n*y.d,x.d*y.n),str=x=>x.d===1n?""+x.n:x.n+"/"+x.d,eq=(x,y)=>x.n===y.n&&x.d===y.d;
 const z=F(0),o=F(1);const rows=[];let negativeControls=0,atomCount=0,normalization=0;
 for(const [an,ad] of [[1n,2n],[3n,4n],[1n,4n],[11n,18n]])for(const [rn,rd] of [[3n,4n],[7n,8n]])for(const T of [4,5])for(const scheme of ["MCAR","INFORMATIVE"]){
  const n=1<<(T-1),D=2n*(ad**BigInt(T+1))*(rd**BigInt(T+1))*4n;
  const buckets=Array.from({length:n},()=>({miss:[0n,0n],obs0:[0n,0n],obs1:[0n,0n],missY:[[0n,0n],[0n,0n]]}));
  for(let xm=0;xm<(1<<(T+2));xm++){
   let wX=1n;for(let t=1;t<=T+1;t++)wX*=((xm>>t)&1)===((xm>>(t-1))&1)?an:ad-an;
   for(let ym=0;ym<(1<<T);ym++){
    let w=wX;for(let t=1;t<=T;t++)w*=((ym>>(t-1))&1)===((xm>>t)&1)?rn:rd-rn;
    const h=ym&((1<<(T-1))-1),yT=(ym>>(T-1))&1;
    for(let yF=0;yF<=1;yF++){
     const wF=w*(yF===((xm>>(T+1))&1)?rn:rd-rn);
     for(let M=0;M<=1;M++){
      const missNum=scheme==="MCAR"?2n:yT===1?3n:1n;
      const wAtom=wF*(M===1?missNum:4n-missNum),b=buckets[h];
      if(M===1){b.miss[yF]+=wAtom;b.missY[yT][yF]+=wAtom}
      else if(yT===0)b.obs0[yF]+=wAtom;else b.obs1[yF]+=wAtom;
      atomCount++;
     }
    }
   }
  }
  let mass=0n,miss=0n,rA=z,rI=z,rmA=z,rmI=z,id=z,wrong=z;
  const br=(cnt,q)=>add(mul(F(cnt[1],D),mul(sub(o,q),sub(o,q))),mul(F(cnt[0],D),mul(q,q)));
  for(const b of buckets){
   const nMiss=b.miss[0]+b.miss[1],nObs0=b.obs0[0]+b.obs0[1],nObs1=b.obs1[0]+b.obs1[1],total=nMiss+nObs0+nObs1;
   mass+=total;miss+=nMiss;
   const qA=F(b.miss[1],nMiss),qI=F(b.miss[1]+b.obs0[1]+b.obs1[1],total);
   const cA=br(b.miss,qA),cI=br(b.miss,qI);
   rA=add(rA,cA);rI=add(rI,cI);rmA=add(rmA,cA);rmI=add(rmI,cI);
   id=add(id,mul(F(nMiss,D),mul(sub(qA,qI),sub(qA,qI))));
   for(const ob of [b.obs0,b.obs1]){const q=F(ob[1],ob[0]+ob[1]),v=br(ob,q);rA=add(rA,v);rI=add(rI,v);}
   if(scheme==="INFORMATIVE"){
    const wrongNum1=b.missY[1][1]+9n*b.missY[0][1],wrongDen=b.missY[1][0]+b.missY[1][1]+9n*(b.missY[0][0]+b.missY[0][1]);
    wrong=add(wrong,br(b.miss,F(wrongNum1,wrongDen)));
   }
  }
  if(mass!==D||miss*2n!==D)throw Error("B normalization failed");
  normalization++;if(!eq(sub(rI,rA),id))throw Error("B Brier identity failed");
  if(scheme==="INFORMATIVE"&&an*2n!==ad){
   if(!eq(wrong,rmA)&&wrong.n*rmA.d>rmA.n*wrong.d)negativeControls++;
   else throw Error("B reversal negative control failed "+an+"/"+ad+" "+rn+"/"+rd+" T"+T+" wrong="+str(wrong)+" rmA="+str(rmA));
  }
  rows.push({a:str(F(an,ad)),r:str(F(rn,rd)),T,scheme,missing_probability:str(F(miss,D)),aware_Brier:str(rA),ignore_missingness_Brier:str(rI),excess_Brier:str(sub(rI,rA)),missing_conditional_aware_Brier:str(div(rmA,F(miss,D))),missing_conditional_ignore_Brier:str(div(rmI,F(miss,D))),squared_prediction_gap_identity:str(id)});
 }
 return {research_id:"R198",audit_method:"full_hidden_path_and_observation_channel_integer_atom_enumeration",source_data_used:"frozen_a_r_T_and_missingness_grid_only",comparisons:rows.length,full_atom_contributions:atomCount,normalization_checks:normalization,wrong_missingness_channel_negative_controls:negativeControls,rows,external_independent_replication:false};
}
if(typeof require!=='undefined' && require.main===module){console.log(JSON.stringify(runB198(),null,2));}
