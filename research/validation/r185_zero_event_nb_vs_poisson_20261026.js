"use strict";
/* R185 oracle-mean zero event Brier comparison, E1 only.
   node research/validation/r185_zero_event_nb_vs_poisson_20261026.js research/R185/R185_EXACT_RESULTS.json
*/
function computeR185(data){
  if(data.research_id!=="R185" || data.worlds!==135 || data.full_results.length!==135)throw Error("source universe mismatch");
  const num=s=>{const a=String(s).split("/");return Number(a[0])/Number(a[1]||1)};
  const gcd=(a,b)=>{while(b){let t=a%b;a=b;b=t}return a<0n?-a:a};
  const F=s=>{const [a,b="1"]=String(s).split("/");let n=BigInt(a),d=BigInt(b),g=gcd(n,d);return [n/g,d/g]};
  const repr=f=>f[1]===1n?String(f[0]):f[0]+"/"+f[1];
  const nbZero=(mu,r)=>{const m=F(mu),R=BigInt(r),n=R*m[1],d=R*m[1]+m[0];let N=n**R,D=d**R,g=gcd(N,D);return [N/g,D/g]};
  const rows=[],byShape={};
  for(const w of data.full_results){
    const r=w.fixed_NB_shape_r;
    if(![2,6,8].includes(r))throw Error("shape changed");
    for(let g=0;g<2;g++){
      const muS=w["true_source_expected_group"+g],qS=w["true_zero_probability_group"+g];
      const q=num(qS),mu=num(muS),cP=Math.exp(-mu);
      const nbf=nbZero(muS,r),cN=num(repr(nbf));
      if(repr(nbf)!==repr(F(w["NB_zero_probability_if_model_mean_set_true_group"+g])))throw Error("archived NB zero mismatch");
      const risk_P=q*(1-q)+(cP-q)**2,risk_NB=q*(1-q)+(cN-q)**2;
      const diff=risk_NB-risk_P,win=Math.abs(diff)<1e-12?"TIE":diff<0?"NB":"POISSON";
      byShape[r]??={NB:0,POISSON:0,TIE:0};byShape[r][win]++;
      rows.push({n:w.n_per_group,mechanism:w.source,group:g,p0:w.true_p0,p1:w.true_p1,r,mu_exact:muS,q_exact:qS,nb_zero_exact:repr(nbf),poisson_zero:cP,nb_zero:cN,risk_poisson:risk_P,risk_nb:risk_NB,nb_minus_poisson:diff,winner:win});
    }
  }
  if(rows.length!==270)throw Error("not 270");
  return {study:"R185_ZERO_EVENT_NB_POISSON_270",source_blob:"857dcb286bf66692952930fc736e133bc3d2b3aa",worlds:135,comparisons:270,byShape,rows};
}
if(typeof require!=="undefined" && require.main===module){
 const fs=require("fs"),crypto=require("crypto");const raw=fs.readFileSync(process.argv[2]);
 const sha=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+raw.length+"\0"),raw])).digest("hex");
 if(sha!=="857dcb286bf66692952930fc736e133bc3d2b3aa")throw Error("source blob mismatch");
 process.stdout.write(JSON.stringify(computeR185(JSON.parse(raw.toString())),null,2)+"\n");
}