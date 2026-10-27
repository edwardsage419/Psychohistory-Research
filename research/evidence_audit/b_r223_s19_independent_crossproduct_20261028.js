"use strict";
/* R223 S19: independent direct cross-products, threshold and monotonicity audit.
   node audit.js R223_EXACT_RESULTS.json R223_S19_GRID_252.csv */
function rat(s){let p=String(s).split("/");return [BigInt(p[0]),BigInt(p[1]||1)];}
function gcd(a,b){while(b){let x=a%b;a=b;b=x;}return a<0n?-a:a;}
function canon(n,d){let g=gcd(n,d);return d/g===1n?String(n/g):String(n/g)+"/"+String(d/g);}
function check(source,rows){
 const map=new Map(source.worlds.map(w=>[w.world,w]));let checks=0,failures=[];
 function ok(flag,tag){checks++;if(!flag)failures.push(tag);}
 for(const row of rows){
  const w=map.get(row.world);if(!w){ok(false,"unknown world");continue;}
  const [p,q]=rat(w.observed_RR),e=BigInt(row.Gamma_E),d=BigInt(row.Gamma_D);
  const n=p*(e+d-1n),den=q*e*d;
  ok(row.RR_lower===canon(n,den),"lower:"+row.world+":"+e+":"+d);
  ok(row.assumed_B===canon(e*d,e+d-1n),"bias:"+row.world+":"+e+":"+d);
  ok(row.null_compatible===(n<=den),"null:"+row.world+":"+e+":"+d);
  const expected=w.oracle_sensitivity_RR_EU===null?null:(e*rat(w.oracle_sensitivity_RR_EU)[1]>=rat(w.oracle_sensitivity_RR_EU)[0]&&d*rat(w.oracle_sensitivity_RR_UD)[1]>=rat(w.oracle_sensitivity_RR_UD)[0]);
  ok(row.oracle_parameter_covered===expected,"oracle:"+row.world+":"+e+":"+d);
  if(e*q>p){ok((n<=den)===(d*(e*q-p)>=p*(e-1n)),"analytic-threshold:"+row.world+":"+e+":"+d);}
  if(expected===true){const [tn,td]=rat(w.true_causal_RR);ok(n*td<=tn*den,"oracle-lower:"+row.world+":"+e+":"+d);}
 }
 const key=new Map(rows.map(r=>[r.world+"|"+r.Gamma_E+"|"+r.Gamma_D,r]));
 const G=[1,2,3,5,7,15];
 for(const w of source.worlds)for(let i=0;i<G.length;i++)for(let j=0;j<G.length;j++){
  const cur=key.get(w.world+"|"+G[i]+"|"+G[j]);
  if(i<5){const next=key.get(w.world+"|"+G[i+1]+"|"+G[j]);let [a,b]=rat(cur.RR_lower),[c,d]=rat(next.RR_lower);ok(c*b<=a*d,"monotoneE:"+w.world+":"+i+":"+j);}
  if(j<5){const next=key.get(w.world+"|"+G[i]+"|"+G[j+1]);let [a,b]=rat(cur.RR_lower),[c,d]=rat(next.RR_lower);ok(c*b<=a*d,"monotoneD:"+w.world+":"+i+":"+j);}
 }
 for(const e of G)for(const d of G){let a=key.get("NULL_CONFOUNDED|"+e+"|"+d),b=key.get("CAUSAL_ALIAS|"+e+"|"+d);ok(a.RR_lower===b.RR_lower&&a.null_compatible===b.null_compatible,"alias:"+e+":"+d);}
 return {checks,failures};
}
function main(source,rows){
 if(rows.length!==252)throw Error("wrong condition count");
 const a=check(source,rows);if(a.failures.length)throw Error("audit failures: "+a.failures.slice(0,4).join(","));
 const changed=rows.map(x=>({...x}));changed[0].RR_lower="999";
 const mutation=check(source,changed);if(mutation.failures.length===0)throw Error("mutation undetected");
 return {research_id:"R223",supplement:"S19",source_git_blob:"3a3f2143357832e25ddf483d7ebd4d66298c5dd1",independent_method:"integer cross-products and analytic thresholds",exact_checks:a.checks,failures:a.failures.length,mutated_checks:mutation.checks,mutation_detected:true,mutation_failure_examples:mutation.failures.slice(0,3),external_independent_reproduction:false};
}
function csvParse(text){const l=text.trim().split(/\r?\n/),keys=l.shift().split(",");return l.map(s=>Object.fromEntries(s.split(",").map((v,i)=>[keys[i],v==="true"?true:v==="false"?false:v==="null"?null:v]))).map(x=>({...x,Gamma_E:Number(x.Gamma_E),Gamma_D:Number(x.Gamma_D)}));}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");const s=JSON.parse(fs.readFileSync(process.argv[2],"utf8")),rows=csvParse(fs.readFileSync(process.argv[3],"utf8"));process.stdout.write(JSON.stringify(main(s,rows),null,2)+"\n");}
