"use strict";
// E079 source-first rational check. node e079_r249_s45_source_parameter_derivative_20261029.js source.csv
function audit(csv){
 const R=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}let x=a<0n?-a:a,y=b;while(y){let z=x%y;x=y;y=z;}return [a/(x||1n),b/(x||1n)];};
 const P=s=>{let t=String(s).split("/");return R(t[0],t[1]||1);};
 const A=(x,y)=>R(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
 const N=(x,y)=>R(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
 const M=(x,y)=>R(x[0]*y[0],x[1]*y[1]);
 const EQ=(x,y)=>x[0]===y[0]&&x[1]===y[1];
 const S=x=>String(x[0])+(x[1]===1n?"":"/"+String(x[1]));
 const one=P("1"),two=P("2"),lg=["1/2","1","2","3","4"].map(P),fd=["-1/4","0","1/4","1"].map(P);
 const prod=(v,g)=>g.reduce((z,t)=>M(z,N(v,t)),one);
 const deriv=(v,g)=>g.filter(t=>!EQ(t,v)).reduce((z,t)=>M(z,N(v,t)),one);
 const q=(v,isL)=>isL?A(v,M(P("16/15"),prod(v,lg))):N(v,M(P("192/7"),prod(v,fd)));
 let checks=0;function ok(v,s){checks++;if(!v)throw Error(s);}
 const lines=csv.trim().split(/\r?\n/);
 ok(lines.shift()==="world,model_family,frozen_control_parameter,original_cohort_x0,original_time_n,observed_state_xn,observed_next_f_xn,observed_local_derivative_fprime,observed_cohort_sensitivity_dxndx0,original_source_probability","header");
 const rows=lines.map(x=>x.split(",")),groups=new Map(),seen=new Set(),worlds={};
 for(const a of rows){
  const [w,f,param,x0,n,x,next,d,sens,weight]=a;
  ok(a.length===10,"width");
  const isL=f==="LOGISTIC";ok(isL||f==="FOLD","family");
  const v=P(param);ok((isL?lg:fd).some(t=>EQ(t,v)),"parameter");
  ok(EQ(P(weight),P("1/45")),"weight");
  ok(EQ(q(v,isL),v),"alias at node");
  const key=w+"|"+x0+"|"+n;ok(!seen.has(key),"unique");seen.add(key);
  const state=P(x),nextExpected=isL?M(M(v,state),N(one,state)):N(A(state,v),M(state,state));
  ok(EQ(nextExpected,P(next)),"next state");
  const slope=isL?M(v,N(one,M(two,state))):N(one,M(two,state));
  ok(EQ(slope,P(d)),"state derivative");
  const g=w+"|"+x0;if(!groups.has(g))groups.set(g,[]);groups.get(g).push(a);
  worlds[w]=(worlds[w]||0)+1;
 }
 ok(rows.length===405,"source length");
 ok(groups.size===81,"trajectory count");
 ok(Object.keys(worlds).length===9&&Object.values(worlds).every(x=>x===45),"world closure");
 for(const [k,g] of groups){
  g.sort((a,b)=>Number(a[4])-Number(b[4]));ok(g.length===5,"time count");
  let expected=P(g[0][3]),D=one;
  for(let n=0;n<5;n++){
   let a=g[n];ok(Number(a[4])===n,"time index");
   ok(EQ(P(a[5]),expected),"chain continuity");
   ok(EQ(P(a[8]),D),"sensitivity product");
   expected=P(a[6]);D=M(D,P(a[7]));
  }
 }
 const logistic=lg.map(v=>({node:S(v),qprime:S(A(one,M(P("16/15"),deriv(v,lg))))}));
 const fold=fd.map(v=>({node:S(v),qprime:S(N(one,M(P("192/7"),deriv(v,fd))))}));
 ok(logistic.find(x=>x.node==="1").qprime==="-11/5","L derivative");
 ok(fold.find(x=>x.node==="0").qprime==="-5/7","F derivative");
 ok(EQ(q(P("3/2"),true),P("1/2")),"L offgrid");
 ok(EQ(q(P("1/8"),false),P("-1/64")),"F offgrid");
 return {study:"E079_R249_S45",evidence:"E1_INTERNAL_SOURCE_FIRST",source_rows:rows.length,
  worlds:Object.keys(worlds).length,trajectories:groups.size,assertions:checks,failures:0,
  logistic_parameter_derivatives:logistic,fold_parameter_derivatives:fold,
  logistic_offgrid_q:"1/2",fold_offgrid_q:"-1/64",new_E2:0,new_E3:0,external_replication:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==3)throw Error("Usage: node script.js source.csv");
 const csv=fs.readFileSync(process.argv[2],"utf8"),result=audit(csv);
 const lines=csv.trim().split(/\r?\n/),bad=lines[1].split(",");
 bad[6]="999";lines[1]=bad.join(",");
 let rejected=false;try{audit(lines.join("\n"));}catch(e){rejected=true;}
 if(!rejected)throw Error("mutation accepted");
 result.mutation_rejected=1;console.log(JSON.stringify(result,null,2));
}
