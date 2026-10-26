"use strict";
const SOURCE_SHA="81f8fa790f0dea2715d99e1384ec33a6d2cf7a64";
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n}
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error("zero denom");if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]}
function parseQ(x){let a=String(x).split("/");return Q(a[0],a[1]||1)}
function plus(x,y){return Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1])}
function minus(x,y){return Q(x[0]*y[1]-y[0]*x[1],x[1]*y[1])}
function times(x,y){return Q(x[0]*y[0],x[1]*y[1])}
function over(x,y){return Q(x[0]*y[1],x[1]*y[0])}
function sq(x){return times(x,x)}
function compare(x,y){let z=x[0]*y[1]-y[0]*x[1];return z<0n?-1:z>0n?1:0}
function str(x){return x[1]===1n?x[0].toString():x[0]+"/"+x[1]}
function dec(x){return Number(x[0])/Number(x[1])}
const ZERO=Q(0),ONE=Q(1),HALF=Q(1,2);
function primary(worlds){
  let rows=[],pairs=0,directionMatches=0,negativeDetected=0,normalizationDetected=0;
  for(let ix=0;ix<worlds.length;ix++){
    const w=worlds[ix],n=w.n_per_group,p0=parseQ(w.true_p0),p1=parseQ(w.true_p1),delta=minus(p1,p0);
    const a=w.source_group0_full_count_PMF.map(parseQ),b=w.source_group1_full_count_PMF.map(parseQ);
    if(a.length!==n+1||b.length!==n+1)throw Error("PMF shape");
    if(compare(a.reduce(plus,ZERO),ONE)||compare(b.reduce(plus,ZERO),ONE))throw Error("PMF normalization");
    if(compare(plus(a.reduce(plus,ZERO),Q(1,100)),ONE)!==0)normalizationDetected++;
    let pos=ZERO,zero=ZERO,neg=ZERO,mseM=ZERO,mseH=ZERO,mutantSeen=false;
    for(let k0=0;k0<=n;k0++)for(let k1=0;k1<=n;k1++){
      let weight=times(a[k0],b[k1]), d=over(Q(k1-k0),Q(n)),h=over(Q(k1-k0),Q(n+1));
      let dDirect=minus(over(Q(k1),Q(n)),over(Q(k0),Q(n)));
      let hDirect=minus(over(Q(2*k1+1),Q(2*(n+1))),over(Q(2*k0+1),Q(2*(n+1))));
      if(compare(d,dDirect)||compare(h,hDirect))throw Error("contrast identity");
      if(compare(d,ZERO)!==compare(h,ZERO))throw Error("direction mismatch");
      directionMatches++;pairs++;
      let s=compare(d,ZERO);
      if(s>0)pos=plus(pos,weight);else if(s<0)neg=plus(neg,weight);else zero=plus(zero,weight);
      mseM=plus(mseM,times(weight,sq(minus(d,delta))));
      mseH=plus(mseH,times(weight,sq(minus(h,delta))));
      if(k1!==k0&&compare(h,over(Q(k1-k0),Q(n+2)))!==0)mutantSeen=true;
    }
    if(!mutantSeen)throw Error("mutant missed");negativeDetected++;
    if(compare(plus(plus(pos,neg),zero),ONE))throw Error("prob sum");
    rows.push({world_index:ix+1,mechanism:w.mechanism,n_per_group:n,true_p0:w.true_p0,true_p1:w.true_p1,true_delta:str(delta),prob_positive_contrast:str(pos),prob_tied_contrast:str(zero),prob_negative_contrast:str(neg),prob_wrong_direction:compare(delta,ZERO)>0?str(neg):null,prob_spurious_nonzero_contrast:compare(delta,ZERO)===0?str(plus(pos,neg)):null,contrast_mse_mle:str(mseM),contrast_mse_halfcount:str(mseH),halfcount_minus_mle_contrast_mse:str(minus(mseH,mseM))});
  }
  return {stage:"R183_POSTSCORE_CONTRAST_DIRECTION_E1",source_git_blob_sha1:SOURCE_SHA,world_count:rows.length,ordered_count_pairs_checked:pairs,direction_sign_matches:directionMatches,negative_control_wrong_denominator_detected_worlds:negativeDetected,negative_control_corrupt_PMF_detected_worlds:normalizationDetected,rows};
}
if(require.main===module){const fs=require("fs"),crypto=require("crypto");const path=process.argv[2]||"research/R183/R183_EXACT_RESULTS.json";const buf=fs.readFileSync(path);const blob=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+buf.length+"\0"),buf])).digest("hex");if(blob!==SOURCE_SHA)throw Error("source Git blob mismatch "+blob);const o=JSON.parse(buf.toString("utf8"));process.stdout.write(JSON.stringify(primary(o.worlds),null,2)+"\n");}
module.exports={primary};
