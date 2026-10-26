"use strict";
// Independent R177 B audit: overlap/minimum route, not R absolute-difference TV.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;}
function R(x,y=1n){x=BigInt(x);y=BigInt(y);if(y<0n){x=-x;y=-y;}const g=gcd(x,y);return [x/g,y/g];}
function parse(x){const z=String(x).split("/");return R(z[0],z[1]||1);}
function plus(a,b){return R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function minus(a,b){return R(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function times(a,b){return R(a[0]*b[0],a[1]*b[1]);}
function min(a,b){return a[0]*b[1]<=b[0]*a[1]?a:b;}
function eq(a,b){return a[0]*b[1]===b[0]*a[1];}
function overlapTV(a,b,m){let ov=R(0);if(m===1){for(let i=0;i<a.length;i++)ov=plus(ov,min(a[i],b[i]));}
else if(m===2){for(let i=0;i<a.length;i++)for(let j=0;j<a.length;j++)ov=plus(ov,min(times(a[i],a[j]),times(b[i],b[j])));}
else throw Error("m not frozen");return minus(R(1),ov);}
function audit(src,receipt){
if(src.world_data.length!==108||receipt.pairwise_exact.length!==405)throw Error("source/receipt count mismatch");
const lookup=new Map();
for(const w of src.world_data){if(w.family==="BIN"&&w.regime!==0)continue;lookup.set(w.n+"|"+w.p+"|"+w.family+"_r"+w.regime,w.full_PMF.map(parse));}
let checked=0,swaps=0,errors=[];
for(const row of receipt.pairwise_exact){
const a=lookup.get(row.n+"|"+row.p+"|"+row.a),b=lookup.get(row.n+"|"+row.p+"|"+row.b);
if(!a||!b)throw Error("missing source");
const t1=overlapTV(a,b,1),t2=overlapTV(a,b,2);
if(!eq(t1,parse(row.tv_m1))||!eq(t2,parse(row.tv_m2)))errors.push(row);
if(!eq(overlapTV(b,a,2),t2))errors.push({type:"order_swap",row});
checked++;swaps++;}
const z=[R(1,3),R(1,3),R(1,3)];if(!eq(overlapTV(z,z,2),R(0)))errors.push({type:"alias"});
return {checked_pairs:checked,checked_order_swap:swaps,exact_mismatch_count:errors.length,examples:errors.slice(0,3),
method:"independent min-overlap tensor probability",source_blob_sha:"8a8819e4d85989b518b9152cfc98336457c76a9c",evidence:"E1_INTERNAL_ALGORITHM_RECHECK",external_replication:false};
}
if(typeof module!=="undefined"&&module.exports){module.exports={audit};
if(require.main===module){const fs=require("fs");const src=JSON.parse(fs.readFileSync(process.argv[2],"utf8")),rec=JSON.parse(fs.readFileSync(process.argv[3],"utf8"));console.log(JSON.stringify(audit(src,rec),null,2));}}
