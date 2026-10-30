/* R299 S95 B: independent nonblind algebraic audit, no R generator import.
   node b_r299_s95_independent_weight_oracle_20261031.js [CSV] [JSON] */
function auditS95(csv,jsonText){
  function abs(a){return a<0n?-a:a;}
  function gcd(a,b){a=abs(a);b=abs(b);while(b){let t=a%b;a=b;b=t;}return a;}
  function Q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denom");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return {n:n/g,d:d/g};}
  function parse(s){let a=String(s).split("/");if(a.length>2)throw Error("bad rational");return Q(a[0],a[1]||1);}
  function plus(a,b){return Q(a.n*b.d+b.n*a.d,a.d*b.d);}
  function minus(a,b){return plus(a,Q(-b.n,b.d));}
  function times(a,b){return Q(a.n*b.n,a.d*b.d);}
  function square(a){return times(a,a);}
  function power(a,n){let z=Q(1);for(let i=0;i<n;i++)z=times(z,a);return z;}
  function equal(a,b){return a.n===b.n&&a.d===b.d;}
  function check(x,label){if(!x)throw Error("B S95 audit FAIL: "+label);}
  const ZERO=Q(0),ONE=Q(1),TWO=Q(2),FOUR=Q(4),ALPHA=Q(1,2),q=Q(1,2);
  const expectedP=["0","1/4","1/2","3/4","1"],expectedG=["0","1/2"],expectedN=[2,4],expectedM=["TD0_ONLINE","MC_FULL_RETURN"];
  const expectedHeader="p,gamma,n,algorithm,history,probability,final_S0,final_S1,true_mean_S0,estimation_sq_error,holdout_conditional_sq_risk";
  const lines=csv.trimEnd().split("\n");
  check(lines.shift()===expectedHeader,"source header");
  check(lines.length===400,"exact 400 source rows");
  const result=JSON.parse(jsonText);
  check(result.research_id==="R299_S95"&&result.scope==="E1_ARTIFICIAL_STOCHASTIC_TWO_STEP_FIXED_POLICY_ONLY","E1 evidence label");
  check(result.human_E2_added===0&&result.historical_E3_added===0&&result.external_team_replication===0,"evidence grade");
  check(result.source_histories===400&&result.groups===40&&result.pairs===20,"frozen counts");
  const groupRows=new Map(),unique=new Set();
  function weights(g,n,algorithm){
    let w=[];
    for(let j=0;j<n;j++){
      if(algorithm==="MC_FULL_RETURN")w.push(times(times(g,ALPHA),power(q,n-1-j)));
      else w.push(j===n-1?ZERO:times(times(times(g,ALPHA),ALPHA),times(Q(n-1-j),power(q,n-2-j))));
    }
    return w;
  }
  for(const line of lines){
    const x=line.split(",");check(x.length===11,"source width");
    const [pText,gText,nText,method,bits]=x;
    check(expectedP.includes(pText)&&expectedG.includes(gText)&&expectedN.includes(Number(nText))&&expectedM.includes(method),"source factor");
    const n=Number(nText),p=parse(pText),g=parse(gText);
    check(bits.length===n&&/^[01]+$/.test(bits),"ordered binary history");
    const id=[pText,gText,nText,method,bits].join("|");
    check(!unique.has(id),"duplicate source");
    unique.add(id);
    const key=[pText,gText,nText,method].join("|");
    groupRows.set(key,(groupRows.get(key)||0)+1);
    const k=bits.split("").filter(c=>c==="1").length;
    const probability=times(power(p,k),power(minus(ONE,p),n-k));
    const w=weights(g,n,method),w1=Array.from({length:n},(_,j)=>times(ALPHA,power(q,n-1-j)));
    let v0=ZERO,v1=ZERO;
    for(let j=0;j<n;j++){
      const r=bits[j]==="1"?TWO:ZERO;
      v0=plus(v0,times(w[j],r));
      v1=plus(v1,times(w1[j],r));
    }
    const mu=times(times(TWO,p),g);
    const err=square(minus(v0,mu));
    const holdout=plus(times(minus(ONE,p),square(v0)),times(p,square(minus(v0,times(TWO,g)))));
    const expected=[probability,v0,v1,mu,err,holdout];
    for(let j=0;j<expected.length;j++)check(equal(parse(x[5+j]),expected[j]),"source field "+(5+j)+" "+id);
  }
  check(unique.size===400&&groupRows.size===40,"full universe");
  const groups=new Map();
  check(Array.isArray(result.group_results)&&result.group_results.length===40,"group results count");
  for(const row of result.group_results){
    const {p:pText,gamma:gText,n,algorithm:method}=row;
    check(expectedP.includes(pText)&&expectedG.includes(gText)&&expectedN.includes(n)&&expectedM.includes(method),"group factor");
    const key=[pText,gText,n,method].join("|");
    check(!groups.has(key),"duplicate group");
    check(groupRows.get(key)===2**n&&row.source_histories===2**n,"group source completeness");
    const p=parse(pText),g=parse(gText),w=weights(g,n,method),mu=times(times(TWO,p),g);
    let sumW=ZERO,sumW2=ZERO;
    for(const x of w){sumW=plus(sumW,x);sumW2=plus(sumW2,square(x));}
    const mean=times(times(TWO,p),sumW);
    const variance=times(times(FOUR,times(p,minus(ONE,p))),sumW2);
    const bias=minus(mean,mu),bias2=square(bias),mse=plus(bias2,variance);
    const oracle=times(times(FOUR,square(g)),times(p,minus(ONE,p)));
    const holdout=plus(mse,oracle),zero=times(times(FOUR,square(g)),p);
    const fields={probability_mass:ONE,mean_estimate:mean,bias,squared_bias:bias2,variance,estimation_mse:mse,
      independent_holdout_risk:holdout,oracle_holdout_risk:oracle,zero_estimator_holdout_risk:zero};
    for(const [f,v] of Object.entries(fields))check(equal(parse(row[f]),v),"group "+key+" field "+f);
    groups.set(key,holdout);
  }
  check(groups.size===40,"group identity");
  check(Array.isArray(result.pair_contrasts)&&result.pair_contrasts.length===20,"pair count");
  const seenPairs=new Set();
  for(const row of result.pair_contrasts){
    const key=[row.p,row.gamma,row.n].join("|");
    check(!seenPairs.has(key),"duplicate pair");seenPairs.add(key);
    const td=groups.get(key+"|TD0_ONLINE"),mc=groups.get(key+"|MC_FULL_RETURN");
    check(td&&mc,"missing paired method");
    const diff=minus(mc,td);
    check(equal(parse(row.td_holdout_risk),td)&&equal(parse(row.mc_holdout_risk),mc)&&equal(parse(row.mc_minus_td_risk),diff),"pair risk "+key);
    check(row.mc_better===(diff.n<0n)&&row.td_better===(diff.n>0n)&&row.tie===(diff.n===0n),"pair sign "+key);
  }
  check(seenPairs.size===20,"full paired universe");
  return {source_rows:unique.size,groups:groups.size,pairs:seenPairs.size,method:"independent reward coefficient polynomial and Bernoulli variance",scope:"NONBLIND_INTERNAL_E1"};
}
function auditMutationTests(csv,jsonText){
  const pass=auditS95(csv,jsonText);
  const lines=csv.trimEnd().split("\n"),result=JSON.parse(jsonText);
  const cases=[
    ["duplicate source",()=>[lines.concat(lines[1]).join("\n")+"\n",jsonText]],
    ["missing source",()=>[lines.slice(0,-1).join("\n")+"\n",jsonText]],
    ["source probability",()=>{let a=[...lines],v=a[1].split(",");v[5]="999";a[1]=v.join(",");return[a.join("\n")+"\n",jsonText];}],
    ["source S0",()=>{let a=[...lines],v=a[1].split(",");v[6]="999";a[1]=v.join(",");return[a.join("\n")+"\n",jsonText];}],
    ["source S1",()=>{let a=[...lines],v=a[1].split(",");v[7]="999";a[1]=v.join(",");return[a.join("\n")+"\n",jsonText];}],
    ["source holdout",()=>{let a=[...lines],v=a[1].split(",");v[10]="999";a[1]=v.join(",");return[a.join("\n")+"\n",jsonText];}],
    ["group risk",()=>{let r=JSON.parse(jsonText);r.group_results[0].independent_holdout_risk="999";return[csv,JSON.stringify(r)];}],
    ["E1 to E2 promotion",()=>{let r=JSON.parse(jsonText);r.human_E2_added=1;return[csv,JSON.stringify(r)];}]
  ];
  const rejects=[];
  for(const [name,make] of cases){
    let rejected=false;
    try{const [a,b]=make();auditS95(a,b);}catch(e){rejected=true;}
    if(!rejected)throw Error("mutation incorrectly accepted: "+name);
    rejects.push(name);
  }
  return {...pass,mutations_rejected:rejects};
}
if(typeof process!=="undefined"&&typeof require!=="undefined"&&require.main===module){
  const fs=require("fs"),path=require("path"),base=path.resolve(__dirname,"../validation");
  const csv=fs.readFileSync(process.argv[2]||path.join(base,"R299_S95_ALL_400_STOCHASTIC_TRAIN_HISTORIES.csv"),"utf8");
  const json=fs.readFileSync(process.argv[3]||path.join(base,"R299_S95_EXACT_HELDOUT_RISK_RESULTS.json"),"utf8");
  console.log(JSON.stringify(auditMutationTests(csv,json),null,2));
}
