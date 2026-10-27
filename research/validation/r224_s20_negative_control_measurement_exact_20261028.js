function runR(csv, baseline) {
  const fields=csv.trim().split(/\r?\n/), header=fields.shift().split(",");
  const idx=Object.fromEntries(header.map((x,i)=>[x,i]));
  const rows=fields.map(s=>{const v=s.split(",");const o={};for(const k of header)o[k]=v[idx[k]];return o;});
  const worlds=baseline.world_results.map(x=>x.world);
  if(rows.length!==4096||worlds.length!==8)throw Error("frozen source size");
  const kernels=[
    {id:"IDENTITY",q0:0,q1:0,r0:0,r1:0},
    {id:"SYMMETRIC_QUARTER",q0:1,q1:1,r0:1,r1:1},
    {id:"SYMMETRIC_HALF",q0:2,q1:2,r0:2,r1:2},
    {id:"FALSE_POSITIVE_A0",q0:1,q1:0,r0:0,r1:0},
    {id:"FALSE_POSITIVE_A1",q0:0,q1:1,r0:0,r1:0}
  ];
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a||1n};
  const rat=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return [n/g,d/g]};
  const add=(x,y)=>rat(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
  const sub=(x,y)=>rat(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
  const str=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+String(x[1]);
  function diff(records,x,y){let n=[0n,0n],d=[0n,0n];for(const t of records){let k=t[x];d[k]+=BigInt(t.m);n[k]+=BigInt(t.m*t[y]);}if(!d[0]||!d[1])throw Error("support");return str(sub(rat(n[1],d[1]),rat(n[0],d[0])));}
  const output=[];
  for(const world of worlds){
    const original=rows.filter(x=>x.world===world);
    if(original.length!==512)throw Error("world rows");
    if(new Set(original.map(x=>[x.oracle_U,x.original_V_A,x.original_V_Z,x.original_V_W,x.original_V_Y].join(","))).size!==512)throw Error("duplicate source");
    const base=baseline.world_results.find(x=>x.world===world);
    for(const k of kernels){
      const expanded=[];let trueY=0,trueW=0,measured=0,mass=0;
      for(const x of original){
        if(x.true_original_probability!=="1/512")throw Error("probability");
        const a=+x.observed_A,z=+x.observed_Z,w=+x.observed_W,y=+x.observed_Y;
        const p1=w?4-k["r"+a]:k["q"+a];
        const p0=4-p1;
        expanded.push({a,z,y,ws:0,m:p0},{a,z,y,ws:1,m:p1});
        mass+=p0+p1;
        const w0=+x.oracle_W_doA0,w1=+x.oracle_W_doA1;
        trueY+= +x.oracle_Y_doA1 - +x.oracle_Y_doA0;
        trueW+=w1-w0;
        measured+=(w1?4-k.r1:k.q1)-(w0?4-k.r0:k.q0);
      }
      if(mass!==2048||expanded.length!==1024)throw Error("mass or slots");
      const dAY=diff(expanded,"a","y"),dAW=diff(expanded,"a","ws");
      const dZY=diff(expanded,"z","y"),dZW=diff(expanded,"z","ws");
      const parse=s=>{const [a,b="1"]=s.split("/");return rat(BigInt(a),BigInt(b))};
      const rec={
        world,kernel:k.id,original_rows:512,measurement_slots:1024,positive_slots:expanded.filter(x=>x.m>0).length,
        mass:"1",D_AY:dAY,D_AWstar:dAW,D_ZY:dZY,D_ZWstar:dZW,
        naive_adjusted:str(sub(parse(dAY),parse(dAW))),
        true_ATE_Y:str(rat(trueY,512)),true_doA_W:str(rat(trueW,512)),
        measured_doA_Wstar:str(rat(measured,2048))
      };
      if(k.id==="IDENTITY"){
        const obs=base.observational_marginal_associations,oracle=base.true_potential_outcome_oracles;
        if(dAY!==obs.D_AY||dAW!==obs.D_AW||dZY!==obs.D_ZY||dZW!==obs.D_ZW||
           rec.true_ATE_Y!==oracle.true_doA_effect_on_Y||rec.true_doA_W!==oracle.true_doA_effect_on_W)throw Error("baseline mismatch "+world);
      }
      output.push(rec);
    }
  }
  return {research:"R224_S20",scope:"E1_FINITE_ARTIFICIAL_ONLY",frozen_protocol_commit:"036c04fd069ff47c3ea8bb309258532bd754fea4",
    original_R224_source_blob:"8484f9e6546d22d68dee3315b2dc11a7ddf27a26",
    original_worlds:8,measurement_kernels:5,conditions:40,source_slots:40960,
    E2_new:0,E3_new:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",results:output};
}