// E052 independent R219 S15 source integrity and numerical moment audit.
// Node 18+, standard library only, no network. Relative tolerance 1e-9.
function audit(csv,R){
 const lines=csv.trim().split(/\r?\n/),keys=lines.shift().split(",");
 const rows=lines.map(s=>Object.fromEntries(s.split(",").map((v,i)=>[keys[i],v])));
 const n=s=>{const [a,b="1"]=String(s).split("/");return Number(a)/Number(b)};
 const near=(a,b)=>Math.abs(a-b)<1e-9*Math.max(1,Math.abs(a),Math.abs(b));
 let checks=0;const ok=(b,m)=>{checks++;if(!b)throw Error("check "+checks+" "+m)};
 ok(rows.length===1281,"rows");
 const worlds=[...new Set(rows.map(r=>r.world))];ok(worlds.length===6,"worlds");
 const pc=new Map(R.conditional.map(x=>[x.world+"|"+x.alpha+"|"+x.pilot_bits,x]));
 const sc=new Map(R.conditions.map(x=>[x.world+"|"+x.alpha,x]));
 ok(pc.size===192&&sc.size===12,"receipt");
 let valid=0,blocked=0,slots=0;
 for(const world of worlds){
  const wr=rows.filter(r=>r.world===world),r=wr[0],vec=k=>r[k].split("|").map(n);
  const p=vec("oracle_all_eight_true_individual_propensity_NOT_ESTIMATOR_INPUT");
  const y0=vec("auditor_all_eight_Y0_NOT_ESTIMATOR_INPUT");
  const y1=vec("auditor_all_eight_Y1_NOT_ESTIMATOR_INPUT");
  const e=vec("public_observed_X_propensity");
  const overlap=e.every(q=>q>0&&q<1);
  ok(wr.length===(overlap?256:1),"world count");let mass=0;
  for(const row of wr){
   const z=row.all_eight_Z.split("|").map(Number),y=row.all_eight_actual_observed_Y.split("|").map(n);
   let prob=1,mask=0;
   ok(z.length===8&&y.length===8,"length");
   for(let i=0;i<8;i++){
    ok(z[i]===0||z[i]===1,"Z");if(z[i])mask|=1<<i;
    prob*=z[i]?p[i]:1-p[i];
    ok(near(y[i],z[i]?y1[i]:y0[i]),"Y");
   }
   ok(mask===Number(row.true_full_assignment_bitmask),"mask");
   ok(near(prob,n(row.original_source_probability_exact)),"prob");
   ok(near(n(row.finite_true_ATE_ORACLE_ONLY),2),"ATE");
   mass+=prob;
  }
  ok(near(mass,1),"source mass");
  const moment=q=>{
   let mu=0,v=0;
   for(let i=0;i<8;i++){
    const a=y1[i]/q[i],b=y0[i]/(1-q[i]);
    mu+=(p[i]*a-(1-p[i])*b)/8;
    v+=p[i]*(1-p[i])*(a+b)**2/64;
   }
   return {mu,v,mse:v+(mu-2)**2};
  };
  for(const alpha of ["1/2","1"]){
   let pm=0,mean=0,second=0;
   for(let bits=0;bits<16;bits++){
    let pw=1;
    for(let j=0;j<4;j++){const i=[0,2,4,6][j];pw*=bits&(1<<j)?p[i]:1-p[i];}
    pm+=pw;
    const k0=Number(!!(bits&1))+Number(!!(bits&2));
    const k1=Number(!!(bits&4))+Number(!!(bits&8));
    const al=n(alpha),q0=(k0+al)/(2+2*al),q1=(k1+al)/(2+2*al);
    const rec=pc.get(world+"|"+alpha+"|"+bits);
    ok(!!rec,"pilot");
    ok(near(n(rec.pilot_probability),pw),"pilot mass");
    ok(near(n(rec.e_hat_X0),q0)&&near(n(rec.e_hat_X1),q1),"q");
    if(!overlap){ok(rec.status==="NO_ORIGINAL_OVERLAP"&&rec.mean===null,"blocked");blocked++;continue;}
    const m=moment(Array.from({length:8},(_,i)=>i<4?q0:q1));
    ok(rec.status==="OK","pilot status");
    ok(near(n(rec.mean),m.mu)&&near(n(rec.variance),m.v)&&near(n(rec.mse),m.mse),"pilot moments");
    mean+=pw*m.mu;second+=pw*(m.v+m.mu**2);
    valid++;slots+=wr.length;
   }
   ok(near(pm,1),"pilot total");
   const c=sc.get(world+"|"+alpha);ok(!!c,"summary");
   if(!overlap){ok(c.status==="NO_ORIGINAL_OVERLAP"&&c.mean===null,"blocked summary");continue;}
   const variance=second-mean**2,bias=mean-2,mse=variance+bias**2,base=moment(e);
   ok(near(n(c.mean),mean)&&near(n(c.variance),variance)&&near(n(c.bias),bias)&&near(n(c.mse),mse),"summary moments");
   ok(near(n(c.original_public_HT_baseline.mean),base.mu)&&near(n(c.original_public_HT_baseline.variance),base.v)&&near(n(c.original_public_HT_baseline.mse),base.mse),"baseline");
  }
 }
 ok(valid===160&&blocked===32&&slots===40960,"totals");
 return {status:"PASS",checks,source_rows:rows.length,worlds:worlds.length,valid_pilot_conditions:valid,blocked_pilot_conditions:blocked,valid_source_slots:slots,tolerance:"relative 1e-9"};
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");
 if(process.argv.length!==4)throw Error("usage: node e052.js R219.csv R219_S15_receipt.json");
 console.log(JSON.stringify(audit(fs.readFileSync(process.argv[2],"utf8"),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2));
}
if(typeof module!=="undefined")module.exports={audit};
