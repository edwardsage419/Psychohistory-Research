/* R165 B independent E1 audit. Node: node r165_b_matrix_moments_20261025.js
   research/R165/R165_EXACT_RESULTS.json
   Only native BigInt and Node fs. Reads original frozen distributions,
   transition kernels and stationary laws. No main R extension imports. */
function audit(src) {
  function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
  function f(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
  function parse(s){const x=String(s).split("/");return f(x[0],x[1]||1);}
  function add(x,y){return f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
  function neg(x){return [-x[0],x[1]];}
  function sub(x,y){return add(x,neg(y));}
  function mul(x,y){return f(x[0]*y[0],x[1]*y[1]);}
  function div(x,y){return f(x[0]*y[1],x[1]*y[0]);}
  function pow(x,n){let z=f(1);for(let i=0;i<n;i++)z=mul(z,x);return z;}
  function eq(x,y){return x[0]===y[0]&&x[1]===y[1];}
  function fmt(x){return x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);}
  const Z=f(0),O=f(1),T=f(2),H=f(1,2);
  function sum(xs){return xs.reduce(add,Z);}
  function dot(xs,ys){return sum(xs.map((x,i)=>mul(x,ys[i])));}
  function moments(row,n){return sum(row.map((v,i)=>mul(v,mul(mul(f(2),f(i,n)),sub(O,f(i,n))))));}
  function kernelPowerRow(row,P,s){let x=row;for(let t=0;t<s;t++){const next=P[0].map((_,j)=>sum(x.map((v,i)=>mul(v,P[i][j]))));x=next;}return x;}
  const kernels=new Map();
  let rowsChecked=0,stationaryChecked=0;
  for(const k of src.kernels){
    const n=k.N,mu=parse(k.mu),P=k.rows.map(row=>row.map(parse));
    if(P.length!==n+1||P.some(row=>row.length!==n+1))throw Error("bad matrix");
    for(const row of P){if(!eq(sum(row),O))throw Error("row sum");rowsChecked++;}
    if(k.stationary){
      const pi=k.stationary.map(parse);
      if(!eq(sum(pi),O))throw Error("pi sum");
      for(let j=0;j<=n;j++)if(!eq(dot(pi,P.map(row=>row[j])),pi[j]))throw Error("pi equation");
      stationaryChecked++;
    }
    kernels.set(n+"|"+k.mu,{n,mu,P,pi:k.stationary?k.stationary.map(parse):null});
  }
  let points=0,transitions=0,mu0decay=0,wrongNoC=0,wrongLinear=0;
  const details=[];
  for(const w of src.worlds){
    const {n,mu,P}=kernels.get(w.N+"|"+w.mu),c=f(n-1,n);
    let last=null;
    for(const point of w.points){
      const dist=point.counts.map(parse),ht=moments(dist,n);
      if(!eq(sum(dist),O)||!eq(ht,parse(point.heterogeneity)))throw Error("frozen H mismatch");
      const a=mul(c,pow(sub(O,mu),2)),b=mul(c,mul(mu,sub(O,div(mu,T))));
      if(last!==null){
        if(!eq(ht,add(mul(a,last),b)))throw Error("moment recurrence "+w.id);
        const noC=add(mul(pow(sub(O,mu),2),last),mul(mu,sub(O,div(mu,T))));
        const linear=add(mul(mul(c,sub(O,mu)),last),b);
        if(!eq(noC,ht))wrongNoC++;
        if(!eq(linear,ht))wrongLinear++;
        transitions++;
      }
      if(eq(mu,Z)){
        const h0=mul(mul(T,f(w.k0,n)),sub(O,f(w.k0,n)));
        if(!eq(ht,mul(h0,pow(c,point.t))))throw Error("neutral decay");
        mu0decay++;
      }
      last=ht;points++;
    }
    details.push({id:w.id,H0:fmt(moments(w.points[0].counts.map(parse),n)),H4:fmt(last)});
  }
  let stationaryDiversity=0,stationaryCovariance=0;
  const stationary=[];
  for(const {n,mu,P,pi} of kernels.values()){
    if(!pi)continue;
    const hstar=moments(pi,n),pvals=pi.map((_,i)=>f(i,n));
    const c=f(n-1,n),a=mul(c,pow(sub(O,mu),2)),b=mul(c,mul(mu,sub(O,div(mu,T))));
    if(!eq(hstar,div(b,sub(O,a))))throw Error("stationary diversity");
    stationaryDiversity++;
    const covs={};
    for(const lag of [1,2,4]){
      const cond=pvals.map((_,i)=>dot(kernelPowerRow(P[i].map((_,j)=>f(Number(i===j))),P,lag),pvals));
      const cross=sum(pi.map((weight,i)=>mul(weight,mul(pvals[i],cond[i]))));
      const cov=sub(cross,f(1,4));
      const expected=mul(pow(sub(O,mu),lag),div(sub(O,mul(T,hstar)),f(4)));
      if(!eq(cov,expected))throw Error("covariance lag "+lag);
      covs[lag]=fmt(cov);stationaryCovariance++;
    }
    stationary.push({N:n,mu:fmt(mu),H_star:fmt(hstar),cov_lag:covs});
  }
  if(points!==240||transitions!==192||mu0decay!==60||stationaryDiversity!==9||stationaryCovariance!==27)throw Error("count mismatch");
  if(wrongNoC!==168||wrongLinear!==126)throw Error("negative controls mismatch");
  return {evidence:"E1_INTERNAL_ALTERNATE_METHOD",method:"frozen_full_distribution_and_exact_matrix_power",
    source_blob:"8b8a7ca5b6a1d75b3f8464e0eeb1b7b180e4ccf3",
    checks:{kernels:kernels.size,kernel_rows:rowsChecked,stationary_equations:stationaryChecked,
      points,transitions,mu0decay,stationaryDiversity,stationaryCovariance,
      negative_omit_c_detected:wrongNoC,negative_linear_mu_detected:wrongLinear},
    stationary,world_summaries:details,E2:0,E3:0,external_replication:0};
}
if(typeof module!=="undefined" && typeof require==="function" && require.main===module){
  const fs=require("fs");
  const input=process.argv[2]||"research/R165/R165_EXACT_RESULTS.json";
  process.stdout.write(JSON.stringify(audit(JSON.parse(fs.readFileSync(input,"utf8"))),null,2)+"\n");
}
