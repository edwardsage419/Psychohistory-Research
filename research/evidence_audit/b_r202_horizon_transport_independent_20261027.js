// B_R202: analytic horizon audit using frozen six-world model-selection masses.
// Run: node research/evidence_audit/b_r202_horizon_transport_independent_20261027.js <R202_EXACT_RESULTS.json> <R202_HORIZON_TRANSPORT_RECEIPT.json>
"use strict";
function gcd(a,b){while(b){let c=a%b;a=b;b=c;}return a;}
function F(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}if(!b)throw Error("zero");let g=gcd(a<0n?-a:a,b);return [a/g,b/g];}
function P(s){let x=s.split("/");return F(x[0],x[1]||1);}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function sub(a,b){return add(a,F(-b[0],b[1]));}
function fmt(a){return a[0]+"/"+a[1];}
const Z=F(0),O=F(1),base=[1,2,4,8];
function prob(a,h){let x=P(a);return F(base.filter(t=>BigInt(t)*x[0]<=BigInt(h)*x[1]).length,4);}
function risk(p,q){return add(mul(p,sub(O,p)),mul(sub(q,p),sub(q,p)));}
function audit(original,receipt){if(original.worlds.length!==6||receipt.worlds.length!==24)throw Error("world count");let fields=0,normalized=0,originalH3=0;for(let w of receipt.worlds){let o=original.worlds.find(z=>z.true_time_scale_a===w.true_a&&Number(z.censor_cutoff)===w.C);if(!o)throw Error("missing source world");let weights=o.model_selection_probabilities,den=Z,p=prob(w.true_a,w.H),expected=Z;
for(let [fit,frac] of Object.entries(weights)){let mass=P(frac);den=add(den,mass);expected=add(expected,mul(mass,risk(p,prob(fit,w.H))));}
if(fmt(den)!=="1/1")throw Error("source normalization");normalized++;
let oracle=risk(p,p),nullRisk=risk(p,prob("1",w.H));let compare={selected_brier:fmt(expected),oracle_brier:fmt(oracle),null_brier:fmt(nullRisk),oracle_gap:fmt(sub(expected,oracle)),selected_minus_null:fmt(sub(expected,nullRisk))};
for(let [key,value] of Object.entries(compare)){fields++;if(w[key]!==value)throw Error("mismatch "+key);}
if(w.H===3){originalH3++;if(w.selected_brier!==o.new_independent_person_Brier_exact)throw Error("original H3 mismatch");}}
return {status:"PASS_INTERNAL_INDEPENDENT_ANALYTIC_AGGREGATION",worlds:24,exact_world_fields:fields,normalized:normalized,original_horizon_3_reproductions:originalH3,external_replication:0};}
if(typeof require!=="undefined"&&require.main===module){let fs=require("node:fs");console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8"))),null,2));}
if(typeof module!=="undefined")module.exports={audit};
