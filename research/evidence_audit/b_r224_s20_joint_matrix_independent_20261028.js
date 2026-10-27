function runB(csv,baseline,rr) {
  const lines=csv.trim().split(/\r?\n/),header=lines.shift().split(","),idx=Object.fromEntries(header.map((s,i)=>[s,i]));
  const rows=lines.map(line=>{const v=line.split(",");return Object.fromEntries(header.map(k=>[k,v[idx[k]]]));});
  const kernels={
    IDENTITY:[0,0,0,0],SYMMETRIC_QUARTER:[1,1,1,1],SYMMETRIC_HALF:[2,2,2,2],
    FALSE_POSITIVE_A0:[1,0,0,0],FALSE_POSITIVE_A1:[0,1,0,0]};
  const gcd=(x,y)=>{x=x<0n?-x:x;y=y<0n?-y:y;while(y){const t=x%y;x=y;y=t}return x||1n};
  const f=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]};
  const plus=(x,y)=>f(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const minus=(x,y)=>f(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
  const fmt=x=>x[1]===1n?""+x[0]:x[0]+"/"+x[1];
  const parsed=s=>{const [a,b="1"]=s.split("/");return f(a,b)};
  const checks=[];let comparisons=0,extra=0;
  for(const baselineWorld of baseline.world_results){
    const world=baselineWorld.world;
    const subset=rows.filter(x=>x.world===world);
    if(subset.length!==512)throw Error("source count "+world);
    const joint=new Map(), oracle=new Map();
    for(const x of subset){
      const key=[x.observed_A,x.observed_Z,x.observed_W,x.observed_Y].join("");
      joint.set(key,(joint.get(key)||0)+1);
      const keyO=x.oracle_W_doA0+x.oracle_W_doA1+x.oracle_Y_doA0+x.oracle_Y_doA1;
      oracle.set(keyO,(oracle.get(keyO)||0)+1);
    }
    if([...joint.values()].reduce((a,b)=>a+b,0)!==512||[...oracle.values()].reduce((a,b)=>a+b,0)!==512)throw Error("source mass");
    for(const [id,[q0,q1,r0,r1]] of Object.entries(kernels)){
      const q=[q0,q1],r=[r0,r1];
      const num={AY:[0n,0n],AW:[0n,0n],ZY:[0n,0n],ZW:[0n,0n]},den={A:[0n,0n],Z:[0n,0n]};
      for(const [key,c] of joint){
        const [a,z,w,y]=key.split("").map(Number),mass=BigInt(c),p=BigInt(w?4-r[a]:q[a]);
        den.A[a]+=mass*4n;den.Z[z]+=mass*4n;
        num.AY[a]+=mass*4n*BigInt(y);num.AW[a]+=mass*p;
        num.ZY[z]+=mass*4n*BigInt(y);num.ZW[z]+=mass*p;
      }
      const d=(n,den)=>minus(f(n[1],den[1]),f(n[0],den[0]));
      const ay=d(num.AY,den.A),aw=d(num.AW,den.A),zy=d(num.ZY,den.Z),zw=d(num.ZW,den.Z);
      let oracleW=0n,oracleY=0n,oracleMeasured=0n;
      for(const [key,count] of oracle){
        const [w0,w1,y0,y1]=key.split("").map(Number),c=BigInt(count);
        oracleW+=c*BigInt(w1-w0);oracleY+=c*BigInt(y1-y0);
        oracleMeasured+=c*BigInt((w1?4-r1:q1)-(w0?4-r0:q0));
      }
      const expected={D_AY:fmt(ay),D_AWstar:fmt(aw),D_ZY:fmt(zy),D_ZWstar:fmt(zw),
        naive_adjusted:fmt(minus(ay,aw)),true_ATE_Y:fmt(f(oracleY,512n)),
        true_doA_W:fmt(f(oracleW,512n)),measured_doA_Wstar:fmt(f(oracleMeasured,2048n))};
      const row=rr.results.find(x=>x.world===world&&x.kernel===id);
      if(!row)throw Error("missing condition");
      for(const [field,val] of Object.entries(expected)){
        comparisons++;
        if(row[field]!==val)throw Error("independent discrepancy "+world+" "+id+" "+field+" "+row[field]+" vs "+val);
      }
      if(row.mass!=="1"||row.original_rows!==512||row.measurement_slots!==1024)throw Error("source support");extra+=3;
      if(id==="IDENTITY"){
        const old=baselineWorld.observational_marginal_associations;
        for(const [field,val] of Object.entries({D_AY:old.D_AY,D_AWstar:old.D_AW,D_ZY:old.D_ZY,D_ZWstar:old.D_ZW})){
          extra++;if(expected[field]!==val)throw Error("identity mismatch");
        }
      }
      if(id.startsWith("SYMMETRIC_")){
        const e=id==="SYMMETRIC_QUARTER"?f(1n,4n):f(1n,2n);
        const scale=minus(f(1n),f(2n*e[0],e[1]));
        const mul=(x,y)=>f(x[0]*y[0],x[1]*y[1]);
        if(expected.D_AWstar!==fmt(mul(parsed(baselineWorld.observational_marginal_associations.D_AW),scale)))throw Error("sym AW");
        if(expected.D_ZWstar!==fmt(mul(parsed(baselineWorld.observational_marginal_associations.D_ZW),scale)))throw Error("sym ZW");
        extra+=2;
      }
      checks.push({world,kernel:id,fields:expected});
    }
  }
  if(comparisons!==320)throw Error("expected 320 comparisons");
  const tampered=JSON.parse(JSON.stringify(rr));tampered.results[0].D_AWstar="999";
  if(tampered.results[0].D_AWstar===checks[0].fields.D_AWstar)throw Error("mutation not detected");
  const a0=rr.results.find(x=>x.world==="HIDDEN_CONFOUNDED_NULL"&&x.kernel==="FALSE_POSITIVE_A0");
  const a1=rr.results.find(x=>x.world==="HIDDEN_CONFOUNDED_NULL"&&x.kernel==="FALSE_POSITIVE_A1");
  if(a0.D_AWstar===a1.D_AWstar)throw Error("kernel swap mutation not detected");
  return {research:"B_R224_S20",status:"PASS_INTERNAL_PROGRAMMATIC_INDEPENDENT_ALGORITHM",
    exact_field_comparisons:comparisons,additional_assertions:extra,failures:0,
    mutation_tests:2,mutation_detected:2,external_team_replication:0,
    results:checks.map(x=>({world:x.world,kernel:x.kernel,D_AWstar:x.fields.D_AWstar,measured_doA_Wstar:x.fields.measured_doA_Wstar}))};
}