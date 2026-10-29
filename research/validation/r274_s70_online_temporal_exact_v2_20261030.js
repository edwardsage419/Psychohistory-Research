"use strict";
/* R274 S70: exact ordered finite source enumeration. Protocol frozen at
   6783168501b596693ec1b3dae2b215b7174ab3c1. No external dependencies. */
const FREEZE="6783168501b596693ec1b3dae2b215b7174ab3c1";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function sub(a,b){return F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return F(a[0]*b[1],a[1]*b[0]);}
function pow(a,n){return F(a[0]**BigInt(n),a[1]**BigInt(n));}
function str(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function eq(a,b){return a[0]===b[0]&&a[1]===b[1];}
const Z=F(0),O=F(1),HALF=F(1,2);
const REGIMES={STABLE_HALF:[HALF,HALF],RISING_RATE:[F(1,4),F(3,4)],FALLING_RATE:[F(3,4),F(1,4)]};
const POLICIES=["PAST_FIXED","ONLINE_ONE_STEP","PRECOMMITTED_HALF"];
function forecasts(policy,k,y5){
  if(!POLICIES.includes(policy)||!Number.isInteger(k)||k<0||k>4||![0,1].includes(y5))throw Error("invalid input");
  const past=F(k+1,6);
  if(policy==="PAST_FIXED")return [past,past];
  if(policy==="ONLINE_ONE_STEP")return [past,F(k+y5+1,7)];
  return [HALF,HALF];
}
function loss(y,q){return pow(sub(F(y),q),2);}
function run(){
  const rows=[],cells=[],summary={};
  const header=["regime","policy","six_bits","past_K","Y5","Y6","mass","q5","q6","brier_t5","brier_t6","brier_average"];
  for(const [regime,[a,b]] of Object.entries(REGIMES)){
    summary[regime]={};
    for(const policy of POLICIES){
      let massSum=Z,t5=Z,t6=Z,n=0;
      const seen=new Set(),seenPrefix=new Map();
      for(let mask=0;mask<64;mask++){
        const bits=mask.toString(2).padStart(6,"0"),k=bits.slice(0,4).split("").reduce((s,v)=>s+Number(v),0);
        const y5=Number(bits[4]),y6=Number(bits[5]),j=y5+y6;
        if(seen.has(bits))throw Error("duplicate");seen.add(bits);
        const mass=mul(mul(pow(a,k),pow(sub(O,a),4-k)),mul(pow(b,j),pow(sub(O,b),2-j)));
        const [q5,q6]=forecasts(policy,k,y5),l5=loss(y5,q5),l6=loss(y6,q6);
        const prefix=bits.slice(0,5),oldQ6=seenPrefix.get(prefix);if(oldQ6!==undefined&&oldQ6!==str(q6))throw Error("Y6 leakage");seenPrefix.set(prefix,str(q6));
        rows.push([regime,policy,bits,String(k),String(y5),String(y6),str(mass),str(q5),str(q6),str(l5),str(l6),str(div(add(l5,l6),F(2)))].join(","));
        massSum=add(massSum,mass);t5=add(t5,mul(mass,l5));t6=add(t6,mul(mass,l6));n++;
      }
      if(n!==64||seen.size!==64||seenPrefix.size!==32||!eq(massSum,O))throw Error("source coverage");
      for(let k=0;k<5;k++){
        const [p5,p6]=forecasts(policy,k,0),[p5alt,p6alt]=forecasts(policy,k,1);
        if(!eq(p5,p5alt))throw Error("t5 lookahead");
        if(policy==="ONLINE_ONE_STEP"&&eq(p6,p6alt))throw Error("online update absent");
        if(policy!=="ONLINE_ONE_STEP"&&!eq(p6,p6alt))throw Error("fixed forecast changed");
      }
      const avg=div(add(t5,t6),F(2));
      const row={regime,policy,source_types:n,expected_t5_brier:str(t5),expected_t6_brier:str(t6),expected_two_period_brier:str(avg),future_Y6_used_in_forecast:false};
      cells.push(row);summary[regime][policy]=row;
    }
  }
  const contrasts=[];
  for(const regime of Object.keys(REGIMES)){
    const obj=summary[regime];
    function cell(p,metric){return F(...obj[p][metric].split("/").map(x=>BigInt(x)));}
    const onlineVsFixed=sub(cell("ONLINE_ONE_STEP","expected_t6_brier"),cell("PAST_FIXED","expected_t6_brier"));
    const onlineVsHalf=sub(cell("ONLINE_ONE_STEP","expected_two_period_brier"),cell("PRECOMMITTED_HALF","expected_two_period_brier"));
    contrasts.push({regime,online_minus_fixed_t6:str(onlineVsFixed),online_minus_half_average:str(onlineVsHalf)});
  }
  const json=JSON.stringify({research_id:"R274_S70",original_R274_freeze:"47b75b49afb5c72c5ca2599ab38499e0f2856354",s70_prescore_freeze_commit:FREEZE,scope:"NONBLIND_INTERNAL_ARTIFICIAL_E1",regimes:3,policies:3,unique_ordered_sources_per_regime:64,policy_labelled_source_rows:rows.length,scored_time_cells:18,results:cells,contrasts,R073:"FROZEN",PESEN_v0_1:"FROZEN",new_E2:0,new_E3:0},null,2)+"\n";
  const csv=header.join(",")+"\n"+rows.join("\n")+"\n";
  return {json,csv,cells,contrasts};
}
if(typeof require!=="undefined" && require.main===module){
 const out=run(); if(process.argv.includes("--selftest")){if(out.cells.length!==9||out.csv.split("\n").length!==578)throw Error("selftest");process.stdout.write("PASS 9 cells 576 rows\n");}
 else process.stdout.write(out.json);
}
