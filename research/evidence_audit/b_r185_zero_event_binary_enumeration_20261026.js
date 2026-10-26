"use strict";
/* Independent B audit R185. Run:
node research/evidence_audit/b_r185_zero_event_binary_enumeration_20261026.js research/R185/R185_EXACT_RESULTS.json research/validation/R185_ZERO_EVENT_NB_POISSON_270_RECEIPT_2026-10-26.json
*/
function computeB185(data,receipt){
 const n=s=>{let a=String(s).split("/");return Number(a[0])/Number(a[1]||1)};
 const key=x=>[x.n,x.mechanism,x.group,x.p0,x.p1,x.r].join("|");
 const lookup=new Map(receipt.rows.map(x=>[key(x),x]));
 let checked=0,maximum_absolute_error=0,negative_detected=0,nb_prob_check=0;
 for(const w of data.full_results){
   for(let g=0;g<2;g++){
     const mu=n(w["true_source_expected_group"+g]),q=n(w["true_zero_probability_group"+g]),r=w.fixed_NB_shape_r;
     const row=lookup.get([w.n_per_group,w.source,g,w.true_p0,w.true_p1,r].join("|"));
     if(!row)throw Error("missing comparison");
     let nb=1;for(let i=0;i<r;i++)nb*=r/(r+mu);
     const p=Math.exp(-mu);
     if(Math.abs(nb-n(row.nb_zero_exact))>1e-12)throw Error("NB exact mismatch");
     nb_prob_check++;
     let lossNB=0,lossP=0;
     for(const [y,weight] of [[0,1-q],[1,q]]){
       lossNB+=weight*(nb-y)**2;
       lossP+=weight*(p-y)**2;
     }
     for(const [a,b] of [[lossNB,row.risk_nb],[lossP,row.risk_poisson]]){
       let e=Math.abs(a-b);maximum_absolute_error=Math.max(maximum_absolute_error,e);
       if(e>1e-12)throw Error("Brier mismatch");
     }
     const wrong=nb*r/(r+mu);
     if(Math.abs(wrong-nb)>1e-12)negative_detected++;
     checked++;
   }
 }
 if(checked!==270||negative_detected===0)throw Error("audit incomplete");
 return {audit:"B_R185_ZERO_EVENT_BINARY_ENUMERATION",worlds:135,comparisons:checked,risk_checks:checked*2,nb_zero_checks:nb_prob_check,negative_exponent_error_detected:negative_detected,maximum_absolute_error,scope:"internal method independent numeric audit"};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),crypto=require("crypto");const raw=fs.readFileSync(process.argv[2]);
 const sha=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+raw.length+"\0"),raw])).digest("hex");
 if(sha!=="857dcb286bf66692952930fc736e133bc3d2b3aa")throw Error("source blob mismatch");
 process.stdout.write(JSON.stringify(computeB185(JSON.parse(raw.toString()),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2)+"\n");
}