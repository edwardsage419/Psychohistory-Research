"use strict";
// R145 independent exact Gram dual calculation. Only standard BigInt is used.
// Protocol: R145_DUAL_GRAM_THIRD_METHOD_PROTOCOL_FREEZE_2026-10-25.md
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a}
class Q {
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d}let g=gcd(n,d);this.n=n/g;this.d=d/g}
  static of(s){if(s instanceof Q)return s;let a=String(s).split("/");return new Q(a[0],a[1]||1)}
  add(x){x=Q.of(x);return new Q(this.n*x.d+x.n*this.d,this.d*x.d)}
  sub(x){x=Q.of(x);return new Q(this.n*x.d-x.n*this.d,this.d*x.d)}
  mul(x){x=Q.of(x);return new Q(this.n*x.n,this.d*x.d)}
  div(x){x=Q.of(x);return new Q(this.n*x.d,this.d*x.n)}
  eq(x){x=Q.of(x);return this.n===x.n&&this.d===x.d}
  ge(x){x=Q.of(x);return this.n*x.d>=x.n*this.d}
  str(){return this.d===1n?String(this.n):String(this.n)+"/"+String(this.d)}
}
const q=Q.of, sum=a=>a.reduce((s,x)=>s.add(x),q(0));
function assert(cond,msg){if(!cond)throw Error("R145 CHECK FAILED: "+msg)}
const MODELS={
 base:{H:["3/4","1/4"],L:["1/4","3/4"]},
 redundant:{H:["3/8","3/8","1/8","1/8"],L:["1/8","1/8","3/8","3/8"]},
 informative:{H:["1/2","1/4","1/16","3/16"],L:["1/16","3/16","1/4","1/2"]}
};
function solve(Hraw,Lraw,craw){
  let H=Hraw.map(q),L=Lraw.map(q),c=q(craw),target=q("1/2").add(c);
  assert(H.length===L.length&&sum(H).eq(1)&&sum(L).eq(1),"probabilities");
  let d=H.map((x,i)=>x.sub(L[i]));
  let G=sum(H.map((x,i)=>d[i].mul(d[i]).div(x)));
  assert(G.ge(0)&&!G.eq(0),"positive Gram");
  let v=H.map((x,i)=>target.add(c.mul(d[i]).div(G.mul(x))));
  assert(v.every(x=>x.ge(0)),"interior solution invalid");
  let ir=sum(H.map((x,i)=>x.mul(v[i])));
  let ic=sum(d.map((x,i)=>x.mul(v[i])));
  let cost=sum(H.map((x,i)=>x.mul(v[i]).mul(v[i])));
  let lambda=target.mul(2),mu=c.mul(2).div(G);
  assert(ir.eq(target)&&ic.eq(c),"binding IR/IC");
  assert(H.every((x,i)=>x.mul(v[i]).mul(2).eq(lambda.mul(x).add(mu.mul(d[i])))),"KKT stationarity");
  assert(cost.eq(target.mul(target).add(c.mul(c).div(G))),"dual closed form");
  assert(lambda.ge(0)&&mu.ge(0),"dual feasibility");
  return {G:G.str(),v:v.map(x=>x.str()),cost:cost.str(),ir:ir.str(),ic:ic.str(),lambda:lambda.str(),mu:mu.str(),strict_ic:false};
}
function permutations(xs){
 if(xs.length===0)return [[]];
 let a=[];for(let i=0;i<xs.length;i++)for(const r of permutations(xs.filter((_,j)=>j!==i)))a.push([xs[i],...r]);return a;
}
function main(){
 const costs=["0","1/8","1/4","3/8"],rows=[];
 for(const [model,m] of Object.entries(MODELS))for(const c of costs){
  const r=solve(m.H,m.L,c);rows.push({model,c,...r});
 }
 const pick=(m,c)=>rows.find(r=>r.model===m&&r.c===c);
 assert(pick("base","1/4").cost==="39/64","baseline archive");
 assert(pick("redundant","1/4").cost==="39/64","redundant archive");
 assert(pick("informative","1/4").cost==="5505/9104","informative archive");
 assert(rows.filter(r=>r.c==="0").every(r=>r.cost==="1/4"),"zero effort information value");
 let saving=q(pick("base","1/4").cost).sub(q(pick("informative","1/4").cost));
 assert(saving.eq(q("171/36416")),"archived value");
 let fee=["0","1/64","1/32","1/16","1/8","1/4"];
 assert(fee.slice(1).every(f=>q(f).ge(saving)&&!q(f).eq(saving)),"positive fees exceed value");
 let perms=permutations([0,1,2,3]),checked=0;
 for(const model of ["redundant","informative"]){
  const m=MODELS[model];
  for(const perm of perms){
   for(const c of costs){
    const x=solve(perm.map(i=>m.H[i]),perm.map(i=>m.L[i]),c);
    assert(x.cost===pick(model,c).cost,"permutation cost");
    checked++;
   }
  }
 }
 function goodConditional(m,action,y){
  const P=m[action].map(q),start=y==="success"?0:2;
  return P[start].div(P[start].add(P[start+1]));
 }
 let redundant=MODELS.redundant,informative=MODELS.informative;
 let redundantEqual=["success","failure"].every(y=>goodConditional(redundant,"H",y).eq(goodConditional(redundant,"L",y)));
 let informativeDiff=["success","failure"].some(y=>!goodConditional(informative,"H",y).eq(goodConditional(informative,"L",y)));
 assert(redundantEqual&&informativeDiff,"conditional informativeness");
 const controls={
  reject_claim_redundant_strict_saving:q(pick("base","1/4").cost).eq(q(pick("redundant","1/4").cost)),
  reject_claim_strict_IC:rows.every(r=>q(r.ic).eq(q(r.c))),
  reject_claim_positive_net_value_at_nonzero_fees:fee.slice(1).every(f=>q(f).ge(saving)&&!q(f).eq(saving))
 };
 assert(Object.values(controls).every(Boolean),"negative controls");
 return {
  research:"R145",date:"2026-10-25",evidence:"E1_CONSTRUCTED_INTERNAL",
  method:"exact Gram dual with explicit KKT, independently coded in JS",
  model_count:3,cost_count:4,exact_cases:rows.length,
  four_state_label_permutation_checks:checked,
  redundant_conditional_independence:redundantEqual,
  informative_conditional_difference:informativeDiff,
  gross_monitor_value:saving.str(),nonzero_fees_all_exceed_value:true,
  negative_controls:controls,rows,
  new_E2:0,new_E3:0,external_team_replications:0
 };
}
if(typeof process!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 process.stdout.write(JSON.stringify(main(),null,2)+"\n");
}
