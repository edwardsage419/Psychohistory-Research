"use strict";
/* R184 postscore E1 zero-event Brier study. Run:
   node research/validation/r184_zero_event_brier_20261026.js research/R184/R184_EXACT_RESULTS.json
   Outputs JSON to stdout. Requires Node.js standard library only.
*/
function computeR(data){
  if(data.research_id!=="R184" || data.world_count!==45 || data.worlds.length!==45) throw Error("wrong R184 universe");
  const gcd=(a,b)=>{while(b!==0n){let t=a%b;a=b;b=t}return a<0n?-a:a};
  const frac=s=>{const [a,b="1"]=String(s).split("/");let n=BigInt(a),d=BigInt(b);if(d<=0n)throw Error("bad denominator");let g=gcd(n,d);return [n/g,d/g]};
  const add=(a,b)=>{let n=a[0]*b[1]+b[0]*a[1],d=a[1]*b[1],g=gcd(n,d);return [n/g,d/g]};
  const mul=(a,b)=>{let n=a[0]*b[0],d=a[1]*b[1],g=gcd(n,d);return [n/g,d/g]};
  const str=a=>a[1]===1n?a[0].toString():a[0]+"/"+a[1];
  const val=a=>Number(a[0])/Number(a[1]);
  const rows=[], wins={};
  for(const w of data.worlds){
    for(let g=0;g<2;g++){
      const pmf=w["source_group"+g+"_full_count_PMF"].map(frac);
      let sum=frac("0"),mean=frac("0");
      for(let k=0;k<pmf.length;k++){sum=add(sum,pmf[k]);mean=add(mean,mul(pmf[k],[BigInt(k),1n]));}
      if(str(sum)!=="1")throw Error("PMF normalization "+rows.length);
      const qf=pmf[0],q=val(qf),mu=val(mean);
      if(str(qf)!==str(frac(w["source_exact_zero_count_probability_group"+g])) || str(mean)!==str(frac(w["source_expected_count_group"+g])))throw Error("source moment mismatch");
      const c=Math.exp(-mu),v=q*(1-q),delta2=(c-q)**2;
      for(const m of [1,2,4]){
        const risk_P=v+delta2, risk_E=v*(1+1/m),risk_S=v+(m*v+delta2)/(m+1)**2;
        const rank=(a,b)=>Math.abs(a-b)<1e-12?"TIE":a<b?"FIRST":"SECOND";
        for(const [name,a,b] of [["P_vs_E",risk_P,risk_E],["P_vs_S",risk_P,risk_S],["E_vs_S",risk_E,risk_S]]){
          const label=rank(a,b);wins[name+"_"+label]=(wins[name+"_"+label]||0)+1;
        }
        rows.push({n:w.n_per_group,mechanism:w.source_mechanism,p0:w.true_p0,p1:w.true_p1,group:g,m,q_exact:str(qf),mu_exact:str(mean),poisson_zero:c,true_zero:q,poisson_bias:c-q,risk_P,risk_E,risk_S});
      }
    }
  }
  if(rows.length!==270)throw Error("not 270");
  return {study:"R184_ZERO_EVENT_BRIER_270",source_blob:"f7d8ee20f9885594097de9cb6284bb48e7b6642b",worlds:45,marginals:90,comparisons:270,m_values:[1,2,4],winners:wins,rows};
}
if(typeof require!=="undefined" && require.main===module){
  const fs=require("fs"),crypto=require("crypto");
  const path=process.argv[2];if(!path)throw Error("pass source JSON path");
  const raw=fs.readFileSync(path);
  const blob=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+raw.length+"\0"),raw])).digest("hex");
  if(blob!=="f7d8ee20f9885594097de9cb6284bb48e7b6642b")throw Error("source blob mismatch");
  process.stdout.write(JSON.stringify(computeR(JSON.parse(raw.toString("utf8"))),null,2)+"\n");
}