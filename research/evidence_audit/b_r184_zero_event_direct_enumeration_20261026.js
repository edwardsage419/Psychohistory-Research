"use strict";
/* Independent R184 zero-event audit. Run:
   node research/evidence_audit/b_r184_zero_event_direct_enumeration_20261026.js research/R184/R184_EXACT_RESULTS.json research/validation/R184_ZERO_EVENT_BRIER_270_RECEIPT_2026-10-26.json
   This program enumerates the training zero count and the future binary outcome.
*/
function computeB(data,main){
  if(main.rows.length!==270 || data.worlds.length!==45)throw Error("unexpected sample universe");
  const toNumber=s=>{let p=String(s).split("/");return Number(p[0])/(p.length===2?Number(p[1]):1)};
  const choose=(n,k)=>{let a=1;for(let j=1;j<=k;j++)a=a*(n-j+1)/j;return a};
  let max_diff=0,checked=0,negative_control_detected=0,source_norm=0,source_mean=0;
  const byKey=new Map(main.rows.map(x=>[[x.n,x.mechanism,x.p0,x.p1,x.group,x.m].join("|"),x]));
  const examples=[];
  for(const w of data.worlds){
    for(let g=0;g<2;g++){
      const p=w["source_group"+g+"_full_count_PMF"].map(toNumber);
      const sum=p.reduce((a,b)=>a+b,0);
      if(Math.abs(sum-1)>1e-12)throw Error("source normalization");
      source_norm++;
      const q=p[0],mu=p.reduce((s,prob,k)=>s+k*prob,0);
      if(Math.abs(mu-toNumber(w["source_expected_count_group"+g]))>1e-12)throw Error("mean mismatch");
      if(Math.abs(q-toNumber(w["source_exact_zero_count_probability_group"+g]))>1e-12)throw Error("zero mismatch");
      source_mean++;
      const c=Math.exp(-mu);
      for(const m of [1,2,4]){
        const key=[w.n_per_group,w.source_mechanism,w.true_p0,w.true_p1,g,m].join("|");
        const ref=byKey.get(key);if(!ref)throw Error("missing row "+key);
        let P=0,E=0,S=0,badS=0;
        for(let t=0;t<=m;t++){
          const pt=choose(m,t)*q**t*(1-q)**(m-t);
          const predictions=[c,t/m,(t+c)/(m+1),(t+c)/(m+2)];
          for(const [y,py] of [[0,1-q],[1,q]]){
            const mass=pt*py;
            P+=mass*(predictions[0]-y)**2;
            E+=mass*(predictions[1]-y)**2;
            S+=mass*(predictions[2]-y)**2;
            badS+=mass*(predictions[3]-y)**2;
          }
        }
        for(const [a,b] of [[P,ref.risk_P],[E,ref.risk_E],[S,ref.risk_S]]){
          const d=Math.abs(a-b);max_diff=Math.max(max_diff,d);if(d>1e-12)throw Error("independent mismatch "+key+" "+d);
        }
        if(Math.abs(S-badS)>1e-12)negative_control_detected++;
        if(w.n_per_group===8&&w.true_p0==="1/4"&&w.true_p1==="1/4"&&g===0&&m===2&&["IID_BIN","CLUSTERED_BB_C2","INACTIVE_ZIB_Z1_8"].includes(w.source_mechanism))
          examples.push({mechanism:w.source_mechanism,risk_P:P,risk_E:E,risk_S:S,incorrect_denominator_risk:badS});
        checked++;
      }
    }
  }
  if(checked!==270 || negative_control_detected===0)throw Error("audit incomplete");
  return {audit:"B_R184_DIRECT_T_Y_ENUMERATION",source_blob:main.source_blob,source_normalizations:source_norm,source_moment_checks:source_mean,independent_three_predictor_comparisons:checked*3,negative_control_detected,maximum_absolute_discrepancy:max_diff,examples,scope:"internal independent enumeration only"};
}
if(typeof require!=="undefined" && require.main===module){
  const fs=require("fs"),crypto=require("crypto");
  const source=fs.readFileSync(process.argv[2]);const rec=fs.readFileSync(process.argv[3]);
  const blob=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+source.length+"\0"),source])).digest("hex");
  if(blob!=="f7d8ee20f9885594097de9cb6284bb48e7b6642b")throw Error("source identity mismatch");
  process.stdout.write(JSON.stringify(computeB(JSON.parse(source.toString()),JSON.parse(rec.toString())),null,2)+"\n");
}