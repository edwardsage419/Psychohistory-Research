
"use strict";

function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function sub(a,b){return F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return F(a[0]*b[1],a[1]*b[0]);}
function fmt(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}

function audit(receipt){
 const cases=[];let checks=0,fail=0,neg=0,support=0;
 const W=["CONFOUND","DIRECT","COMBINED"];
 for(const world of W)for(const qn of [0,1,2]){
  const q=F(qn,4),pnot=sub(F(1),q);
  function posterior(t,s){
   let weights=[];
   for(let c=0;c<=1;c++){
    const pt=t===c?F(3,4):F(1,4);
    const ps=s===c?pnot:q;
    weights.push(mul(F(1,2),mul(pt,ps)));
   }
   return div(weights[1],add(weights[0],weights[1]));
  }
  function ey(t,s){
   if(world==="DIRECT")return F(t);
   if(world==="COMBINED"&&t===1)return F(1);
   return posterior(t,s);
  }
  let adjusted=F(0);
  for(let s=0;s<=1;s++)adjusted=add(adjusted,mul(F(1,2),sub(ey(1,s),ey(0,s))));
  const obs=world==="CONFOUND"?F(1,2):world==="DIRECT"?F(1):F(3,4);
  const truth=world==="CONFOUND"?F(0):world==="DIRECT"?F(1):F(1,2);
  const found=receipt.worlds.find(x=>x.world===world&&x.q===qn+"/4");
  if(!found)throw Error("missing world");
  const expected=[fmt(obs),fmt(adjusted),fmt(truth),fmt(sub(adjusted,truth))];
  const actual=[found.observational_difference,found.proxy_adjusted_difference,found.true_do_effect,found.proxy_adjustment_bias];
  for(let i=0;i<4;i++){checks++;if(expected[i]!==actual[i])fail++;}
  for(const cell of found.support){checks++;support++;if(cell.n<=0)fail++;}
  if(qn>0&&world!=="DIRECT"&&fmt(adjusted)!==fmt(truth))neg++;
  cases.push({world,q:qn+"/4",adjusted:fmt(adjusted),bias:fmt(sub(adjusted,truth))});
 }
 if(checks!==72||fail||neg!==4||support!==36)throw Error("audit invariant");
 return {audit:"B_R212_MEASUREMENT_ERROR_INDEPENDENT_BAYES",date:"2026-10-27",cases:9,field_and_support_checks:checks,failures:fail,positive_support_cells:support,incorrect_perfect_proxy_negative_controls_detected:neg,results:cases,external_replication:false,new_E2:0,new_E3:0};
}

if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const input=process.argv[2]||"research/validation/R212_MISCLASSIFIED_CONFOUNDER_9_WORLD_RECEIPT_2026-10-27.json";
 const out=process.argv[3]||".";
 fs.mkdirSync(out,{recursive:true});const r=audit(JSON.parse(fs.readFileSync(input,"utf8")));
 fs.writeFileSync(path.join(out,"B_R212_MISCLASSIFIED_CONFOUNDER_INDEPENDENT_BAYES_AUDIT_2026-10-27.json"),JSON.stringify(r,null,2)+"\n");console.log(JSON.stringify(r));
}
if(typeof module!=="undefined")module.exports={audit};
