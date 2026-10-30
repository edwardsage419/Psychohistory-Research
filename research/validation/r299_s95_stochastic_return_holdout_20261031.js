/* R299 S95 frozen exact artificial stochastic terminal reward study.
   Node >=18: node this_file.js --test | --emit [directory] | --check
   No external dependencies. Prescore freeze: 6a84026ee32039b1e4b256ae46370aee1add11de. */
function runS95() {
  function abs(a){return a<0n?-a:a;}
  function gcd(a,b){a=abs(a);b=abs(b);while(b){const t=a%b;a=b;b=t;}return a;}
  function Q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return {n:n/g,d:d/g};}
  function add(a,b){return Q(a.n*b.d+b.n*a.d,a.d*b.d);}
  function neg(a){return Q(-a.n,a.d);}
  function sub(a,b){return add(a,neg(b));}
  function mul(a,b){return Q(a.n*b.n,a.d*b.d);}
  function sq(a){return mul(a,a);}
  function eq(a,b){return a.n===b.n&&a.d===b.d;}
  function str(a){return a.d===1n?String(a.n):String(a.n)+"/"+String(a.d);}
  function pow(a,k){let z=Q(1);for(let i=0;i<k;i++)z=mul(z,a);return z;}
  function assert(x,m){if(!x)throw Error("S95 invariant: "+m);}
  const Z=Q(0),O=Q(1),TWO=Q(2),A=Q(1,2);
  const P=[Z,Q(1,4),Q(1,2),Q(3,4),O],G=[Z,Q(1,2)],N=[2,4],M=["TD0_ONLINE","MC_FULL_RETURN"];
  const header=["p","gamma","n","algorithm","history","probability","final_S0","final_S1","true_mean_S0","estimation_sq_error","holdout_conditional_sq_risk"];
  const rows=[],groups=[],lookup=new Map(),state1=new Map();
  for(const p of P)for(const gamma of G)for(const n of N)for(const algorithm of M){
    const label=[str(p),str(gamma),n,algorithm].join("|");
    let mass=Z,mean=Z,second=Z,mse=Z,holdout=Z;
    for(let code=0;code<2**n;code++){
      const bits=code.toString(2).padStart(n,"0");
      let v0=Z,v1=Z,k=0;
      for(const bit of bits){
        const reward=bit==="1"?TWO:Z;
        if(bit==="1")k++;
        const target0=algorithm==="TD0_ONLINE"?mul(gamma,v1):mul(gamma,reward);
        const next0=add(v0,mul(A,sub(target0,v0)));
        const next1=add(v1,mul(A,sub(reward,v1)));
        v0=next0;v1=next1;
      }
      const prob=mul(pow(p,k),pow(sub(O,p),n-k));
      const mu=mul(mul(gamma,TWO),p);
      const err=sq(sub(v0,mu));
      const conditional=add(mul(sub(O,p),sq(v0)),mul(p,sq(sub(v0,mul(gamma,TWO)))));
      mass=add(mass,prob);
      mean=add(mean,mul(prob,v0));
      second=add(second,mul(prob,sq(v0)));
      mse=add(mse,mul(prob,err));
      holdout=add(holdout,mul(prob,conditional));
      const sid=[str(p),str(gamma),n,bits].join("|");
      if(state1.has(sid))assert(eq(state1.get(sid),v1),"S1 must be identical across methods");
      else state1.set(sid,v1);
      rows.push([str(p),str(gamma),n,algorithm,bits,str(prob),str(v0),str(v1),str(mu),str(err),str(conditional)].join(","));
    }
    assert(eq(mass,O),"mass "+label);
    const mu=mul(mul(gamma,TWO),p);
    const bias=sub(mean,mu),bias2=sq(bias),variance=sub(second,sq(mean));
    const oracle=mul(mul(Q(4),sq(gamma)),mul(p,sub(O,p)));
    const zeroRisk=mul(mul(Q(4),sq(gamma)),p);
    assert(eq(mse,add(bias2,variance)),"bias variance "+label);
    assert(eq(holdout,add(mse,oracle)),"heldout decomposition "+label);
    if(eq(gamma,Z))assert(eq(holdout,Z),"gamma zero "+label);
    if(eq(p,Z))assert(eq(holdout,Z),"p zero "+label);
    const g={p:str(p),gamma:str(gamma),n,algorithm,source_histories:2**n,probability_mass:str(mass),
      mean_estimate:str(mean),bias:str(bias),squared_bias:str(bias2),variance:str(variance),
      estimation_mse:str(mse),independent_holdout_risk:str(holdout),
      oracle_holdout_risk:str(oracle),zero_estimator_holdout_risk:str(zeroRisk)};
    groups.push(g);lookup.set(label,{risk:holdout,group:g});
  }
  const pairs=[];
  for(const p of P)for(const gamma of G)for(const n of N){
    const key=[str(p),str(gamma),n].join("|");
    const td=lookup.get(key+"|TD0_ONLINE").risk,mc=lookup.get(key+"|MC_FULL_RETURN").risk;
    const delta=sub(mc,td);
    pairs.push({p:str(p),gamma:str(gamma),n,td_holdout_risk:str(td),mc_holdout_risk:str(mc),
      mc_minus_td_risk:str(delta),mc_better:delta.n<0n,td_better:delta.n>0n,tie:delta.n===0n});
  }
  assert(rows.length===400&&groups.length===40&&pairs.length===20,"frozen universe");
  assert(new Set(rows.map(x=>x.split(",").slice(0,5).join("|"))).size===400,"unique source keys");
  const c1=lookup.get("1|1/2|4|TD0_ONLINE").group;
  const c2=lookup.get("1|1/2|4|MC_FULL_RETURN").group;
  assert(c1.mean_estimate==="11/16"&&c2.mean_estimate==="15/16","original R299 deterministic checkpoint");
  const result={research_id:"R299_S95",freeze_commit:"6a84026ee32039b1e4b256ae46370aee1add11de",
    scope:"E1_ARTIFICIAL_STOCHASTIC_TWO_STEP_FIXED_POLICY_ONLY",source_histories:400,groups:40,pairs:20,
    training_rewards:"independent Bernoulli(p) times 2",alpha:"1/2",training_episodes:[2,4],
    independent_test_reward:"fresh Bernoulli(p) times 2; never used in updates",
    original_R299_acceptance:"UNCHANGED",R073:"FROZEN",PESEN_v0_1:"FROZEN",
    human_E2_added:0,historical_E3_added:0,external_team_replication:0,
    group_results:groups,pair_contrasts:pairs,
    validation:{all_group_masses_one:true,bias_variance_exact:true,holdout_decomposition_exact:true,
      deterministic_original_R299_checkpoint:true,zero_gamma_negative_control:true,zero_p_negative_control:true}};
  const csv=header.join(",")+"\n"+rows.join("\n")+"\n";
  const json=JSON.stringify(result,null,2)+"\n";
  return {csv,json,result};
}
if(typeof process!=="undefined"&&typeof require!=="undefined"&&require.main===module){
  const fs=require("fs"),path=require("path"),args=process.argv.slice(2),cmd=args[0]||"--test";
  const out=runS95();
  const filenames=["R299_S95_ALL_400_STOCHASTIC_TRAIN_HISTORIES.csv","R299_S95_EXACT_HELDOUT_RISK_RESULTS.json"];
  if(cmd==="--test"){console.log("PASS: 400 exact sources, 40 groups, 20 pairs and frozen invariants");}
  else if(cmd==="--emit"){
    const dir=args[1]||__dirname;fs.mkdirSync(dir,{recursive:true});
    fs.writeFileSync(path.join(dir,filenames[0]),out.csv);fs.writeFileSync(path.join(dir,filenames[1]),out.json);
    console.log("EMITTED "+filenames.join(" "));
  }else if(cmd==="--check"){
    const dir=args[1]||__dirname;
    if(fs.readFileSync(path.join(dir,filenames[0]),"utf8")!==out.csv)throw Error("CSV byte mismatch");
    if(fs.readFileSync(path.join(dir,filenames[1]),"utf8")!==out.json)throw Error("JSON byte mismatch");
    console.log("PASS: archived CSV and JSON byte identical");
  }else{throw Error("usage: --test | --emit [directory] | --check [directory]");}
}
