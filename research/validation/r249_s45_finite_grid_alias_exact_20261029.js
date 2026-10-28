"use strict";
// Exact Fraction replay of R249's 405 frozen rows, with parameter-family aliases.
// Run: node r249_s45_finite_grid_alias_exact_20261029.js path/to/R249_source.csv
function rat(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error("division by zero");if(b<0n){a=-a;b=-b;}let x=a<0n?-a:a,y=b;while(y){let t=x%y;x=y;y=t;}let g=x||1n;return [a/g,b/g];}
function p(s){let a=String(s).split("/");if(!/^-?\d+$/.test(a[0])||(a[1]&&!/^[1-9]\d*$/.test(a[1])))throw Error("invalid rational");return rat(a[0],a[1]||1);}
const one=rat(1),zero=rat(0);
function add(x,y){return rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function sub(x,y){return rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);}
function mul(x,y){return rat(x[0]*y[0],x[1]*y[1]);}
function eq(x,y){return x[0]===y[0]&&x[1]===y[1];}
function str(x){return String(x[0])+(x[1]===1n?"":"/"+String(x[1]));}
function sign(x){return x[0]>0n?1:x[0]<0n?-1:0;}
const L={LOGISTIC_R_HALF:"1/2",LOGISTIC_R_ONE:"1",LOGISTIC_R_TWO:"2",LOGISTIC_R_THREE:"3",LOGISTIC_R_FOUR:"4"};
const F={FOLD_NEG_QUARTER:"-1/4",FOLD_ZERO:"0",FOLD_POS_QUARTER:"1/4",FOLD_POS_ONE:"1"};
const lg=["1/2","1","2","3","4"].map(p),fg=["-1/4","0","1/4","1"].map(p);
const initial=new Set(["-1","-1/2","-1/4","0","1/4","1/2","2/3","3/4","1"]);
function product(x,grid){return grid.reduce((z,t)=>mul(z,sub(x,t)),one);}
function coeff(w,alias){let x=p(w in L?L[w]:F[w]);return !alias?x:w in L?add(x,mul(p("16/15"),product(x,lg))):sub(x,mul(p("192/7"),product(x,fg)));}
function f(w,x,alias){let q=coeff(w,alias);return w in L?mul(mul(q,x),sub(one,x)):sub(add(x,q),mul(x,x));}
function d(w,x,alias){return w in L?mul(coeff(w,alias),sub(one,mul(rat(2),x))):sub(one,mul(rat(2),x));}
function run(w,x,n,alias){let D=one;for(let i=0;i<n;i++){D=mul(D,d(w,x,alias));x=f(w,x,alias);}return [x,f(w,x,alias),d(w,x,alias),D];}
const header="world,model_family,frozen_control_parameter,original_cohort_x0,original_time_n,observed_state_xn,observed_next_f_xn,observed_local_derivative_fprime,observed_cohort_sensitivity_dxndx0,original_source_probability";
function audit(csv,mutation=""){
 const lines=csv.trim().split(/\r?\n/);if(lines.shift()!==header||lines.length!==405)throw Error("source structure");
 let seen=new Set(),counts={},checks=0,worlds=Object.keys(L).concat(Object.keys(F));
 for(let i=0;i<lines.length;i++){
  let a=lines[i].split(","),w=a[0];if(a.length!==10||!worlds.includes(w))throw Error("source world");
  if(a[1]!==((w in L)?"LOGISTIC":"FOLD")||a[2]!==((w in L)?L[w]:F[w]))throw Error("parameter mismatch");
  if(!initial.has(a[3])||!["0","1","2","3","4"].includes(a[4])||!eq(p(a[9]),p("1/45")))throw Error("cohort/time/weight");
  let key=w+"|"+a[3]+"|"+a[4];if(seen.has(key))throw Error("duplicate");seen.add(key);counts[w]=(counts[w]||0)+1;
  for(let alias of [false,true]){
   let values=run(w,p(a[3]),Number(a[4]),alias);
   if(mutation==="parameter"&&i===0&&alias)values[0]=add(values[0],one);
   for(let j=0;j<4;j++){let obs=p(a[5+j]);if(mutation==="source"&&i===0&&j===0)obs=add(obs,one);
    if(!eq(values[j],obs))throw Error("field mismatch "+key+" "+j);checks++;}
  }
 }
 if(worlds.some(w=>counts[w]!==45))throw Error("world completeness");
 let lp=product(p("3/2"),lg),lq=add(p("3/2"),mul(p("16/15"),lp));
 let fp=product(p("1/8"),fg),fq=sub(p("1/8"),mul(p("192/7"),fp));
 if(!eq(lp,p("-15/16"))||!eq(lq,p("1/2"))||!eq(fp,p("21/4096"))||!eq(fq,p("-1/64")))throw Error("off-grid alias mismatch");
 if(sign(sub(p("3/2"),one))!==1||sign(sub(lq,one))!==-1||sign(fq)!==-1)throw Error("classification");
 return {study:"R249_S45",evidence:"E1_SYNTHETIC_EXACT",source_rows:405,parameter_worlds:9,trajectories:81,
  field_comparisons:checks,per_world_rows:counts,sampled_grid_observation_equivalence:true,
  logistic_off_grid:{r:"3/2",P:str(lp),original_multiplier_at_zero:"3/2",alias_multiplier_at_zero:str(lq),original:"REPELLER",alias:"ATTRACTOR"},
  fold_off_grid:{mu:"1/8",P:str(fp),original_constant:"1/8",alias_constant:str(fq),original_fixed_points:2,alias_fixed_points:0,extra_zero_exists_in:"(1/8,1/4)"},
  caveat:"R249 specified-family analytic proof unchanged; off-grid parameter family not identified from finite samples",new_E2:0,new_E3:0,external_replication:0};
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");if(process.argv.length!==3)throw Error("Usage: node script.js source.csv");
 const csv=fs.readFileSync(process.argv[2],"utf8"),r=audit(csv);
 for(const m of ["parameter","source"]){let rejected=false;try{audit(csv,m);}catch(e){rejected=true;}if(!rejected)throw Error("mutation not rejected");}
 r.mutation_negative_controls_rejected=2;console.log(JSON.stringify(r,null,2));
}
