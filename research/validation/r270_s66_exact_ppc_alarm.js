"use strict";
// R270 S66: exact direct enumeration. E1 artificial only. Node standard library.
const gcd=(a,b)=>{while(b){[a,b]=[b,a%b];}return a<0n?-a:a;};
class F{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("denom");let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 add(x){return new F(this.n*x.d+x.n*this.d,this.d*x.d);}
 sub(x){return new F(this.n*x.d-x.n*this.d,this.d*x.d);}
 mul(x){return new F(this.n*x.n,this.d*x.d);}
 le(x){return this.n*x.d<=x.n*this.d;}
 eq(x){return this.n===x.n&&this.d===x.d;}
 toString(){return this.d===1n?""+this.n:this.n+"/"+this.d;}
}
const zero=new F(0),one=new F(1);
const rise=(x,n)=>{let p=1n;for(let i=0;i<n;i++)p*=BigInt(x+i);return p;};
const k=x=>{let n=0;for(let i=0;i<6;i++)n+=(x>>i)&1;return n;};
const t=x=>{let n=0;for(let i=0;i<5;i++)n+=(((x>>i)&1)===((x>>(i+1))&1))?1:0;return n;};
const pow=(x,n)=>{let p=one;for(let i=0;i<n;i++)p=p.mul(x);return p;};
const priors=[[1,1],[2,2],[1,3]],thetas=[[1,4],[1,2],[3,4]],alphas=[[1,20],[1,10],[1,5]];
function calculate(){
 const tails={},alarms={};
 for(const [a,b] of priors){
  const pk=a+","+b,ps=[];
  for(let obs=0;obs<64;obs++){
   let A=a+k(obs),B=b+6-k(obs),den=rise(A+B,6),total=zero,lower=zero;
   for(let rep=0;rep<64;rep++){
    const w=new F(rise(A,k(rep))*rise(B,6-k(rep)),den);
    total=total.add(w);if(t(rep)<=t(obs))lower=lower.add(w);
   }
   if(!total.eq(one))throw Error("mass normalization");
   ps.push(lower);
  }
  tails[pk]=ps.map(x=>x.toString());
  for(const [tn,td] of thetas){
   const theta=new F(tn,td),rest=one.sub(theta);let prev=[];
   for(const [an,ad] of alphas){
    const alpha=new F(an,ad),selected=[];let prob=zero;
    for(let obs=0;obs<64;obs++)if(ps[obs].le(alpha)){
     selected.push(obs);prob=prob.add(pow(theta,k(obs)).mul(pow(rest,6-k(obs))));
    }
    if(prev.some(x=>!selected.includes(x)))throw Error("monotonicity");
    prev=selected;
    alarms[pk+"|"+theta+"|"+alpha]={alarm_sequence_count:selected.length,
     alarm_probability:prob.toString(),probability_minus_nominal:prob.sub(alpha).toString()};
   }
  }
 }
 return {research:"R270_S66",evidence:"E1_ARTIFICIAL",
 protocol:"R270_S66_PRIOR_PREDICTIVE_PPC_FALSE_ALARM_PRESCORE_FREEZE_2026-10-29.md",
 observation_count_per_prior:64,replicates_per_observation:64,
 priors:priors.map(x=>x.join(",")),generating_thetas:thetas.map(x=>""+new F(...x)),
 thresholds:alphas.map(x=>""+new F(...x)),lower_tails:tails,alarms};
}
function validate(v){
 if(!v||typeof v!=="object"||Array.isArray(v)||v.research!=="R270_S66"||v.evidence!=="E1_ARTIFICIAL"
 ||typeof v.observation_count_per_prior!=="number"||v.observation_count_per_prior!==64
 ||JSON.stringify(v)!==JSON.stringify(calculate()))throw Error("exact full receipt mismatch");
 return true;
}
function selftest(){
 const good=calculate();validate(good);const tests=[];
 let x=JSON.parse(JSON.stringify(good));x.alarms["1,1|1/4|1/20"].alarm_probability="999";tests.push(x);
 x=JSON.parse(JSON.stringify(good));x.lower_tails["1,3"].pop();tests.push(x);
 x=JSON.parse(JSON.stringify(good));x.lower_tails["1,1"].push("1");tests.push(x);
 x=JSON.parse(JSON.stringify(good));x.evidence="E2_HUMAN";tests.push(x);
 x=JSON.parse(JSON.stringify(good));x.observation_count_per_prior=false;tests.push(x);
 for(const v of tests){let rejected=false;try{validate(v);}catch(e){rejected=true;}if(!rejected)throw Error("negative accepted");}
 return {pass:true,negative_controls_rejected:5,exact_tails:192,alarm_probabilities:27};
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),args=process.argv.slice(2);
 if(args.includes("--selftest"))console.log(JSON.stringify(selftest()));
 let i=args.indexOf("--emit");if(i>=0){if(!args[i+1])throw Error("emit path");fs.writeFileSync(args[i+1],JSON.stringify(calculate(),null,2)+"\n");}
 i=args.indexOf("--check");if(i>=0){if(!args[i+1])throw Error("check path");validate(JSON.parse(fs.readFileSync(args[i+1],"utf8")));console.log("PASS exact persisted receipt");}
 if(args.length===0)console.log(JSON.stringify(calculate(),null,2));
}
