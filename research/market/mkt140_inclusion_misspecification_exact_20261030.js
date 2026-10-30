"use strict";
// MKT140. Synthetic design enumeration only. No personal data or paid services.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
class Q {
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
  add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
  sub(b){return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
  mul(b){return new Q(this.n*b.n,this.d*b.d);}
  div(b){if(b.n===0n)throw Error("division by zero");return new Q(this.n*b.d,this.d*b.n);}
  toString(){return this.d===1n?String(this.n):this.n+"/"+this.d;}
}
const q=(n,d=1)=>new Q(n,d),zero=q(0),one=q(1);
function assert(v,m){if(!v)throw Error(m);}
function equal(a,b){return a.n===b.n&&a.d===b.d;}
const size=[1,2,3,4], label=[0,1,0,1];
const truth=[q(3,4),q(1,2),q(1,2),q(1,4)], population=q(3,5);
function evaluate(assumed){
  if(!Array.isArray(assumed)||assumed.length!==4)throw Error("four assumed probabilities required");
  if(assumed.some(x=>!(x instanceof Q)||x.n<=0n||x.n>x.d))throw Error("invalid assumed probability");
  let expectation=zero,second=zero,total=zero,worlds=0;
  for(let mask=0;mask<16;mask++){
    let mass=one, estimate=zero;
    for(let i=0;i<4;i++){
      const sampled=!!(mask&(1<<i));
      mass=mass.mul(sampled?truth[i]:one.sub(truth[i]));
      if(sampled&&label[i])estimate=estimate.add(q(size[i]).div(assumed[i]));
    }
    estimate=estimate.div(q(10));
    expectation=expectation.add(mass.mul(estimate));
    second=second.add(mass.mul(estimate).mul(estimate));
    total=total.add(mass);worlds++;
  }
  assert(equal(total,one),"world mass must sum to 1");
  const variance=second.sub(expectation.mul(expectation));
  const bias=expectation.sub(population);
  const mse=variance.add(bias.mul(bias));
  // Independent analytic Horvitz-Thompson moments, crosschecked against 16-world enumeration.
  let analyticE=zero,analyticV=zero;
  for(let i=0;i<4;i++){
    if(!label[i])continue;
    analyticE=analyticE.add(q(size[i]).mul(truth[i]).div(assumed[i]));
    analyticV=analyticV.add(q(size[i]*size[i]).mul(truth[i]).mul(one.sub(truth[i])).div(assumed[i].mul(assumed[i])));
  }
  assert(equal(expectation,analyticE.div(q(10))),"analytic expectation mismatch");
  assert(equal(variance,analyticV.div(q(100))),"analytic variance mismatch");
  return {expectation:expectation.toString(),bias:bias.toString(),variance:variance.toString(),mse:mse.toString(),worlds};
}
function run(){
  const scenarios={
    correct:truth,flat_half:Array(4).fill(q(1,2)),
    assumed_high:Array(4).fill(q(3,4)),assumed_low:Array(4).fill(q(1,4))
  };
  const result=Object.fromEntries(Object.entries(scenarios).map(([k,v])=>[k,evaluate(v)]));
  const expected={correct:["3/5","0","13/25","13/25"],flat_half:["2/5","-1/5","4/25","1/5"],assumed_high:["4/15","-1/3","16/225","41/225"],assumed_low:["4/5","1/5","16/25","17/25"]};
  let assertions=0;
  for(const [k,v] of Object.entries(expected)){
    for(const [j,field] of ["expectation","bias","variance","mse"].entries()){
      assert(result[k][field]===v[j],k+" "+field);assertions++;
    }
  }
  // For all four true probabilities, an assumed relative factor 0.8 to 1.2
  // yields a design expectation range of [1/2,3/4], not a confidence interval.
  const lower=truth.map(x=>x.mul(q(6,5)));
  const upper=truth.map(x=>x.mul(q(4,5)));
  assert(evaluate(lower).expectation==="1/2","sensitivity lower");assertions++;
  assert(evaluate(upper).expectation==="3/4","sensitivity upper");assertions++;
  const invalid=[[],[q(1,2)],[q(0),q(1,2),q(1,2),q(1,2)],[q(2),q(1,2),q(1,2),q(1,2)],[null,q(1,2),q(1,2),q(1,2)]];
  for(const v of invalid){let rejected=false;try{evaluate(v);}catch(_){rejected=true;}assert(rejected,"invalid input accepted");}
  return {kind:"ARTIFICIAL_E1_NONBLIND",population:"3/5",results:result,sensitivity_expectation_range:["1/2","3/4"],assertions,invalid_rejected:invalid.length};
}
const results=run();
if(typeof console!=="undefined")console.log(JSON.stringify(results));
