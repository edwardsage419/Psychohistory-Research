"use strict";
function verify(csvText, receiptText, originalText) {
  const receipt=JSON.parse(receiptText), original=JSON.parse(originalText);
  const patterns={SMOOTH:[1,1,1,1],ALTERNATING:[1,-1,1,-1],MIXED:[1,0,0,-1]};
  const sources=["IID","SAR_POS","SEM_POS","SAR_NEG","SEM_NEG"];
  let checks=0;
  function assert(ok,msg){checks++;if(!ok)throw Error("E036 check "+checks+": "+msg);}
  function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;}
  function rat(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
  function read(s){const t=String(s).split("/");return rat(BigInt(t[0]),t[1]?BigInt(t[1]):1n);}
  function eq(a,b){return a[0]*b[1]===b[0]*a[1];}
  function str(a){return a[1]===1n?String(a[0]):a.join("/");}
  function mat(source){let a=Array.from({length:4},()=>Array(4).fill(0));if(source==="IID"){for(let i=0;i<4;i++)a[i][i]=6;return a;}
    const sign=source.endsWith("POS")?1:-1;
    for(let i=0;i<4;i++)for(let j=0;j<4;j++)a[i][j]=i===j?7:((i-j+4)%4===2?1:2*sign);return a;}
  function mul(A,v){return A.map(row=>row.reduce((s,x,j)=>s+x*v[j],0));}
  function mean(source,v){return source.startsWith("SAR")?mul(mat(source),v):v.map(x=>6*x);}
  function trace(source){return mat(source).flat().reduce((s,x)=>s+x*x,0);}
  function risk(trueSource,predSource,z,x,stale){const mt=mean(trueSource,z),mp=mean(predSource,stale?x:z);return trace(trueSource)+mt.reduce((s,v,i)=>s+(v-mp[i])**2,0);}
  const lines=csvText.trim().split(/\r?\n/);const heads=lines.shift().split(",");const rows=lines.map(line=>Object.fromEntries(line.split(",").map((v,i)=>[heads[i],v])));
  assert(rows.length===240,"original row count");
  const counts=new Map();
  for(const row of rows){
    assert(sources.includes(row.true_source),"true source");
    assert(sources.includes(row.selected_candidate),"selected candidate");
    assert(Object.hasOwn(patterns,row.covariate_pattern),"train pattern");
    assert(eq(read(row.original_training_source_probability),rat(1,16)),"original probability");
    const x=patterns[row.covariate_pattern],shock=row.source_training_shock.split("|").map(Number);
    assert(shock.length===4&&shock.every(v=>v===-1||v===1),"shock support");
    const S=mat(row.true_source);
    const y=row.true_source.startsWith("SAR")?mul(S,x.map((v,i)=>v+shock[i])):x.map((v,i)=>6*v+mul(S,shock)[i]);
    const seen=row.source_observed_y.split("|");
    assert(seen.length===4,"observed vector length");
    for(let i=0;i<4;i++)assert(eq(read(seen[i]),rat(y[i],6)),"observed y "+row.true_source+" "+row.covariate_pattern+" "+i);
    const key=row.covariate_pattern+"|"+row.true_source;counts.set(key,(counts.get(key)||[]).concat([row]));
  }
  assert(counts.size===15,"train groups");
  for(const [key,arr] of counts)assert(arr.length===16,"training group size "+key);
  assert(receipt.results.length===45,"45-world receipt");
  const old=new Map(original.worlds.map(w=>[w.pattern+"|"+w.true_source,w]));
  let same=0,changed=0,staleWorse=0,better=0,worse=0,equal=0,min=null,max=null;
  const seenWorlds=new Set();
  for(const w of receipt.results){
    const key=w.train_pattern+"|"+w.true_source+"|"+w.test_pattern;
    assert(!seenWorlds.has(key),"duplicate world");seenWorlds.add(key);
    const x=patterns[w.train_pattern],z=patterns[w.test_pattern],arr=counts.get(w.train_pattern+"|"+w.true_source);
    assert(Boolean(arr)&&Boolean(z),"world key");
    let sums=[0n,0n,0n,0n,0n], selected=Object.fromEntries(sources.map(s=>[s,0]));
    for(const row of arr){
      const q=row.selected_candidate;selected[q]++;
      sums[0]+=BigInt(risk(w.true_source,q,z,x,false));
      sums[1]+=BigInt(risk(w.true_source,q,z,x,true));
      sums[2]+=BigInt(risk(w.true_source,"IID",z,x,false));
      sums[3]+=BigInt(risk(w.true_source,"IID",z,x,true));
      sums[4]+=BigInt(risk(w.true_source,w.true_source,z,x,false));
    }
    const keys=["selected_current_MSE_exact","selected_stale_MSE_exact","fixed_IID_current_MSE_exact","fixed_IID_stale_MSE_exact","oracle_known_true_MSE_exact"];
    const risks=sums.map(n=>rat(n,2304n));
    for(let i=0;i<5;i++)assert(eq(risks[i],read(w[keys[i]])),key+" "+keys[i]+" expected "+str(risks[i])+" actual "+w[keys[i]]);
    assert(eq(rat(risks[1][0]*risks[0][1]-risks[0][0]*risks[1][1],risks[1][1]*risks[0][1]),read(w.stale_minus_current_exact)),key+" stale delta");
    for(const s of sources)assert(eq(rat(selected[s],16),read(w.selected_candidate_probabilities_exact[s])),key+" selection "+s);
    assert(Object.values(selected).reduce((a,b)=>a+b,0)===16,key+" selection normalization");
    assert(w.original_training_vectors===16&&w.independent_test_shocks_per_training===16,key+" source size");
    if(w.train_pattern===w.test_pattern){same++;assert(eq(risks[0],read(old.get(w.train_pattern+"|"+w.true_source).expected_independent_new_region_MSE_exact)),key+" original regression");assert(eq(risks[0],risks[1]),key+" same pattern");}
    else {changed++;const diff=risks[1][0]*risks[0][1]-risks[0][0]*risks[1][1];if(diff>0n)staleWorse++;if(min===null||diff*min.d<min.n*risks[1][1]*risks[0][1])min={n:diff,d:risks[1][1]*risks[0][1]};if(max===null||diff*max.d>max.n*risks[1][1]*risks[0][1])max={n:diff,d:risks[1][1]*risks[0][1]};}
    const cmp=risks[0][0]*risks[2][1]-risks[2][0]*risks[0][1];if(cmp<0n)better++;else if(cmp>0n)worse++;else equal++;
  }
  assert(seenWorlds.size===45,"unique worlds");
  assert(same===15&&changed===30,"world pattern partition");
  assert(staleWorse===30,"stale worse all 30");
  assert(better===16&&worse===29&&equal===0,"fixed IID comparison");
  assert(receipt.statistics.stale_worse===staleWorse,"receipt stale count");
  assert(receipt.statistics.selected_current_better_than_fixed_IID===better,"receipt improved count");
  assert(receipt.statistics.selected_current_worse_than_fixed_IID===worse,"receipt worse count");
  assert(receipt.independent_source_pairs===11520,"source pair count");
  return {checks,worlds:seenWorlds.size,training_rows:rows.length,source_pairs:11520,stale_worse:staleWorse,current_better_than_IID:better,current_worse_than_IID:worse,min_stale_penalty:str(rat(min.n,min.d)),max_stale_penalty:str(rat(max.n,max.d)),failed:0};
}
if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module){
  const fs=require("node:fs"),base=".";
  const csv=fs.readFileSync(base+"/research/R203/R203_ALL_240_ORIGINAL_SPATIAL_TRAINING_WORLDS.csv","utf8");
  const rec=fs.readFileSync(base+"/research/validation/R203_COVARIATE_TRANSPORT_45_WORLDS_EXACT_RECEIPT_2026-10-27.json","utf8");
  const old=fs.readFileSync(base+"/research/R203/R203_EXACT_RESULTS.json","utf8");
  console.log(JSON.stringify(verify(csv,rec,old),null,2));
}
