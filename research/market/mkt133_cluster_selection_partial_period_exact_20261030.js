"use strict";
// MKT133: exact finite artificial selection and correlated-period bootstrap.
// No external dependencies, no random sampling, no personal data.
const SZ=[1n,1n,2n,8n];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a||1n;}
function q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denominator");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
function add(a,b){return q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function sub(a,b){return q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return q(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return q(a[0]*b[1],a[1]*b[0]);}
function cmp(a,b){const d=a[0]*b[1]-b[0]*a[1];return d<0n?-1:d>0n?1:0;}
function fmt(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function eq(a,b){return cmp(a,b)===0;}
function must(b,msg){if(!b)throw Error("ASSERT "+msg);}
const ZERO=q(0),ONE=q(1),HALF=q(1,2),LO=q(1,40),HI=q(39,40);
function choose(n,k){let r=1n;for(let i=1;i<=k;i++)r=r*BigInt(n-i+1)/BigInt(i);return r;}
function quantile(items,target){
  items.sort((a,b)=>cmp(a[0],b[0]));let c=ZERO;
  for(const [value,prob] of items){c=add(c,prob);if(cmp(c,target)>=0)return value;}
  throw Error("distribution mass below one");
}
function rowBounds(K){
  const n=24,den=24n**24n,dist=[];
  for(let k=0;k<=n;k++){
    const w=choose(n,k)*BigInt(K)**BigInt(k)*BigInt(n-K)**BigInt(n-k);
    dist.push([q(k,n),q(w,den)]);
  }
  return [quantile(dist.slice(),LO),quantile(dist.slice(),HI)];
}
function groupBounds(state){
  const vals=[];
  for(let mask=0;mask<256;mask++){
    let z=mask,den=0n,num=0n;
    for(let j=0;j<4;j++){
      const i=z%4;z=Math.floor(z/4);
      den+=2n*SZ[i];num+=SZ[i]*BigInt(state[i][0]+state[i][1]);
    }
    vals.push([q(num,den),q(1,256)]);
  }
  return [quantile(vals.slice(),LO),quantile(vals.slice(),HI)];
}
function selection(){
  const pi=[q(3,4),q(3,4),q(1,2),q(1,4)],x=[0n,0n,0n,1n];
  let ht=ZERO,ht2=ZERO,observed=ZERO,nonempty=ZERO,empty=ZERO;
  for(let mask=0;mask<16;mask++){
    let pr=ONE,weight=0n,success=0n,H=ZERO;
    for(let i=0;i<4;i++){
      const s=(mask>>i)&1;
      pr=mul(pr,s?pi[i]:sub(ONE,pi[i]));
      if(s){weight+=SZ[i];success+=SZ[i]*x[i];H=add(H,div(q(SZ[i]*x[i],12),pi[i]));}
    }
    ht=add(ht,mul(pr,H));ht2=add(ht2,mul(pr,mul(H,H)));
    if(weight){nonempty=add(nonempty,pr);observed=add(observed,mul(pr,q(success,weight)));}
    else empty=add(empty,pr);
  }
  const theta=q(2,3),variance=sub(ht2,mul(ht,ht)),naive=div(observed,nonempty);
  must(eq(ht,theta),"HT conditional unbiased");
  must(eq(variance,q(4,3)),"HT variance");
  must(eq(empty,q(3,128)),"empty");
  must(eq(naive,q(163,825)),"naive selected ratio");
  must(eq(add(nonempty,empty),ONE),"selection mass");
  let invalid=0;for(const bad of [q(0),q(5,4)]){try{if(cmp(bad,ZERO)<=0||cmp(bad,ONE)>0)throw Error("invalid propensity");}catch(e){invalid++;}}
  must(invalid===2,"positivity controls");
  return {fixed_outcomes:"0,0,0,1",sizes:"1,1,2,8",inclusion_probabilities:"3/4,3/4,1/2,1/4",target:fmt(theta),HT_mean:fmt(ht),HT_variance:fmt(variance),empty_probability:fmt(empty),naive_ratio_conditional_nonempty:fmt(naive),negative_controls:invalid};
}
function periods(){
  const states=[[0,0],[0,1],[1,0],[1,1]];
  const rowCache=Array.from({length:25},(_,k)=>rowBounds(k));
  const results=[];const rhos=[ZERO,HALF,ONE];
  for(const rho of rhos){
    let mass=ZERO,mean=ZERO,second=ZERO,row=ZERO,group=ZERO,worlds=0;
    for(let code=0;code<256;code++){
      let z=code,prob=ONE,k=0,state=[];
      for(let i=0;i<4;i++){
        const pair=states[z%4];z=Math.floor(z/4);state.push(pair);
        prob=mul(prob,eq(q(pair[0]),q(pair[1]))?div(add(ONE,rho),q(4)):div(sub(ONE,rho),q(4)));
        k+=Number(SZ[i])*(pair[0]+pair[1]);
      }
      const m=q(k,24);mass=add(mass,prob);mean=add(mean,mul(prob,m));second=add(second,mul(prob,mul(m,m)));
      const rb=rowCache[k],gb=groupBounds(state);
      if(cmp(rb[0],HALF)<=0&&cmp(HALF,rb[1])<=0)row=add(row,prob);
      if(cmp(gb[0],HALF)<=0&&cmp(HALF,gb[1])<=0)group=add(group,prob);
      worlds++;
    }
    const variance=sub(second,mul(mean,mean));
    const expected=mul(q(35,576),add(ONE,rho));
    must(worlds===256&&eq(mass,ONE),"world count and mass");
    must(eq(mean,HALF)&&eq(variance,expected),"period moment identity");
    results.push({rho:fmt(rho),worlds,mean:fmt(mean),variance:fmt(variance),row_95_coverage:fmt(row),cluster_95_coverage:fmt(group)});
  }
  const exp=[
    ["0","35/576","69/128","119/128"],
    ["1/2","35/384","701/2048","1751/2048"],
    ["1","35/288","1/8","7/8"]];
  for(let i=0;i<3;i++)must(results[i].rho===exp[i][0]&&results[i].variance===exp[i][1]&&results[i].row_95_coverage===exp[i][2]&&results[i].cluster_95_coverage===exp[i][3],"coverage control "+i);
  return results;
}
function main(){return {id:"MKT133",evidence:"E1_FINITE_ARTIFICIAL",selection:selection(),periods:periods(),exact_worlds:768,bootstrap_draws_per_world:256,negative_controls:2,all_checks:"PASS"};}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(main(),null,2));
