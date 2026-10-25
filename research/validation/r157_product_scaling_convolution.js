"use strict";
/* Independent finite-convolution replay of the frozen R157 artificial model.
   Node.js >=18, standard library only. Usage:
   node r157_product_scaling_convolution.js path/to/R157_EXACT_RESULTS.json
   The script never reads data from outside the given archive. */
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a||1n};
const q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return [n/g,d/g]};
const parse=s=>{let p=String(s).split("/");return q(BigInt(p[0]),BigInt(p[1]||"1"))};
const add=(x,y)=>q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const mul=(x,y)=>q(x[0]*y[0],x[1]*y[1]);
const sub=(x,y)=>add(x,q(-y[0],y[1]));
const pow=(x,n)=>{let z=q(1);for(let i=0;i<n;i++)z=mul(z,x);return z};
const eq=(x,y)=>x[0]===y[0]&&x[1]===y[1];
const fmt=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
const ONE=q(1),ZERO=q(0);
function base(a,b,c,T=12){
  const m=[],e=[],f=[];
  for(let t=0;t<=T;t++){
    m.push(sub(ONE,pow(sub(ONE,a),t)));
    let ev=ZERO;
    for(let k=0;k<t;k++)ev=add(ev,mul(mul(b,pow(sub(ONE,b),t-1-k)),m[k]));
    e.push(ev);
    let fv=ZERO;
    for(let k=0;k<t;k++)fv=add(fv,mul(mul(c,pow(sub(ONE,c),t-1-k)),e[k]));
    f.push(fv);
  }
  return {m,e,f};
}
function verify(archive){
  if(archive.research_id!=="R157"||archive.worlds.length!==72)throw Error("wrong archive");
  let stateCells=0,productCells=0,positiveAt3=0,zeroAt2=0;
  const bases=new Map();
  for(const w of archive.worlds){
    const H=parse(w.target),a=parse(w.mass_adjustment),b=parse(w.elite_delay),c=parse(w.fiscal_delay),r=parse(w.fiscal_buffer);
    const key=[fmt(a),fmt(b),fmt(c)].join(":");
    if(!bases.has(key))bases.set(key,base(a,b,c));
    const z=bases.get(key);
    if(w.points.length!==13)throw Error("bad horizon");
    for(const point of w.points){
      const t=point.t;
      const states=[mul(H,z.m[t]),mul(H,z.e[t]),mul(mul(H,sub(ONE,r)),z.f[t])];
      for(let k=0;k<3;k++){
        if(!eq(states[k],parse(point[["mass","elite","fiscal"][k]])))throw Error("state mismatch "+w.id+" t="+t+" k="+k);
        stateCells++;
      }
      const product=mul(mul(states[0],states[1]),states[2]);
      const factored=mul(mul(pow(H,3),sub(ONE,r)),mul(mul(z.m[t],z.e[t]),z.f[t]));
      if(!eq(product,factored)||!eq(product,parse(point.psi_product)))throw Error("product mismatch "+w.id+" t="+t);
      productCells++;
      if(t<=2){if(!eq(product,ZERO))throw Error("early product");zeroAt2++}
      if(t===3&&!eq(r,ONE)){if(eq(product,ZERO))throw Error("nonpositive t3");positiveAt3++}
    }
  }
  if(stateCells!==2808||productCells!==936||positiveAt3!==48||zeroAt2!==216||bases.size!==8)throw Error("count mismatch");
  const z=base(parse("1/4"),parse("1/4"),parse("1/4"));
  const pair1={H:parse("1/2"),r:ZERO},pair2={H:ONE,r:parse("7/8")};
  if(!eq(mul(pow(pair1.H,3),sub(ONE,pair1.r)),mul(pow(pair2.H,3),sub(ONE,pair2.r))))throw Error("counterexample factor");
  for(let t=0;t<=12;t++){
    const k=mul(mul(z.m[t],z.e[t]),z.f[t]);
    const x=mul(mul(pow(pair1.H,3),sub(ONE,pair1.r)),k);
    const y=mul(mul(pow(pair2.H,3),sub(ONE,pair2.r)),k);
    if(!eq(x,y))throw Error("counterexample mismatch");
  }
  const t=3, k=mul(mul(z.m[t],z.e[t]),z.f[t]);
  const good=mul(mul(pow(parse("1/2"),3),ONE),k);
  const wrongH2=mul(mul(pow(parse("1/2"),2),ONE),k);
  const wrongBuffer=mul(mul(pow(ONE,3),add(ONE,parse("1/2"))),k);
  const rightBuffer=mul(mul(pow(ONE,3),sub(ONE,parse("1/2"))),k);
  if(eq(good,wrongH2)||eq(wrongBuffer,rightBuffer))throw Error("negative control escaped");
  return {status:"PASS_BOUNDED_INTERNAL_E1",model:"R157",method:"exact independent finite convolution",archive_worlds:72,base_rate_triples:8,exact_state_cells:stateCells,exact_product_cells:productCells,early_zero_product_cells:zeroAt2,positive_t3_worlds:positiveAt3,counterexample:{world_A:"H=1/2,r=0",world_B:"H=1,r=7/8",equal_product_all_times:"algebraic H^3(1-r) identity",M1_A:fmt(mul(pair1.H,z.m[1])),M1_B:fmt(mul(pair2.H,z.m[1])),P3:fmt(good),P12:fmt(mul(parse("1/8"),mul(mul(z.m[12],z.e[12]),z.f[12])))},negative_controls:{wrong_H_square:"REJECTED",wrong_buffer_sign:"REJECTED",zero_product_implies_zero_H:"REJECTED_BY_r_equals_1"},evidence:"E1_ONLY",external_replication:false};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
  const fs=require("fs");
  if(process.argv.length!==3)throw Error("pass frozen R157_EXACT_RESULTS.json path");
  process.stdout.write(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2)+"\n");
}
