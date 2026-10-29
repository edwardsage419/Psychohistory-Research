"use strict";
/* R274 S70 B: independent moment oracle and strict full archived receipt gate.
   Internal nonblind E1 check. Node CLI: node this_file.js result.json rows.csv */
const FREEZE="6783168501b596693ec1b3dae2b215b7174ab3c1";
function check(v,m){if(!v)throw Error(m);}
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function f(n,d=1n){n=BigInt(n);d=BigInt(d);check(d!==0n,"denom");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function plus(a,b){return f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function minus(a,b){return f(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function times(a,b){return f(a[0]*b[0],a[1]*b[1]);}
function over(a,b){return f(a[0]*b[1],a[1]*b[0]);}
function square(a){return times(a,a);}
function power(a,n){return f(a[0]**BigInt(n),a[1]**BigInt(n));}
function same(a,b){return a[0]===b[0]&&a[1]===b[1];}
function parse(x){check(typeof x==="string"&&/^-?\d+(\/\d+)?$/.test(x),"fraction string");const t=x.split("/");return f(BigInt(t[0]),BigInt(t[1]||"1"));}
const O=f(1),Z=f(0),H=f(1,2);
const worlds={STABLE_HALF:[H,H],RISING_RATE:[f(1,4),f(3,4)],FALLING_RATE:[f(3,4),f(1,4)]};
const policies=["PAST_FIXED","ONLINE_ONE_STEP","PRECOMMITTED_HALF"];
function moment(a,b,policy,time){
 let mu,v;
 if(policy==="PRECOMMITTED_HALF"){mu=H;v=Z;}
 else if(policy==="ONLINE_ONE_STEP"&&time===6){
   mu=over(plus(plus(times(f(4),a),b),O),f(7));
   v=over(plus(times(f(4),times(a,minus(O,a))),times(b,minus(O,b))),f(49));
 }else{
   mu=over(plus(times(f(4),a),O),f(6));
   v=over(times(f(4),times(a,minus(O,a))),f(36));
 }
 return plus(plus(times(b,minus(O,b)),v),square(minus(mu,b)));
}
function verify(receipt,csv){
 check(receipt&&typeof receipt==="object"&&!Array.isArray(receipt),"receipt type");
 check(receipt.research_id==="R274_S70"&&receipt.s70_prescore_freeze_commit===FREEZE,"freeze identity");
 check(receipt.original_R274_freeze==="47b75b49afb5c72c5ca2599ab38499e0f2856354","original freeze");
 check(receipt.scope==="NONBLIND_INTERNAL_ARTIFICIAL_E1"&&receipt.R073==="FROZEN"&&receipt.PESEN_v0_1==="FROZEN","scope");
 check(receipt.new_E2===0&&receipt.new_E3===0&&typeof receipt.new_E2==="number"&&typeof receipt.new_E3==="number","evidence");
 check(receipt.regimes===3&&receipt.policies===3&&receipt.unique_ordered_sources_per_regime===64&&receipt.policy_labelled_source_rows===576&&receipt.scored_time_cells===18,"counts");
 check(Array.isArray(receipt.results)&&receipt.results.length===9,"result length");
 const found=new Set(),look={};let compared=0;
 for(const row of receipt.results){
   check(row&&typeof row==="object"&&Object.hasOwn(worlds,row.regime)&&policies.includes(row.policy),"result key");
   const key=row.regime+"|"+row.policy;check(!found.has(key),"duplicate result");found.add(key);
   check(row.source_types===64&&row.future_Y6_used_in_forecast===false,"source/causality flag");
   const [a,b]=worlds[row.regime],x=moment(a,b,row.policy,5),y=moment(a,b,row.policy,6);
   check(same(parse(row.expected_t5_brier),x),"t5 mismatch "+key);
   check(same(parse(row.expected_t6_brier),y),"t6 mismatch "+key);
   check(same(parse(row.expected_two_period_brier),over(plus(x,y),f(2))),"average mismatch "+key);
   look[key]={x,y};compared+=3;
 }
 check(found.size===9&&Array.isArray(receipt.contrasts)&&receipt.contrasts.length===3,"complete result");
 const contrasts=new Set();
 for(const row of receipt.contrasts){
   check(Object.hasOwn(worlds,row.regime)&&!contrasts.has(row.regime),"contrast coverage");
   contrasts.add(row.regime);
   const online=look[row.regime+"|ONLINE_ONE_STEP"],fixed=look[row.regime+"|PAST_FIXED"],half=look[row.regime+"|PRECOMMITTED_HALF"];
   check(same(parse(row.online_minus_fixed_t6),minus(online.y,fixed.y)),"online/fixed contrast");
   check(same(parse(row.online_minus_half_average),minus(over(plus(online.x,online.y),f(2)),over(plus(half.x,half.y),f(2)))),"online/half contrast");
   compared+=2;
 }
 check(typeof csv==="string"&&csv.endsWith("\n"),"csv termination");
 const lines=csv.trimEnd().split("\n");
 const header="regime,policy,six_bits,past_K,Y5,Y6,mass,q5,q6,brier_t5,brier_t6,brier_average";
 check(lines[0]===header&&lines.length===577,"csv coverage");
 const seen=new Set(),weights={};
 for(let i=1;i<lines.length;i++){
   const c=lines[i].split(",");check(c.length===12,"csv columns");
   const [regime,policy,bits,kstr,y5str,y6str,massstr,q5str,q6str,l5str,l6str,avgstr]=c;
   check(Object.hasOwn(worlds,regime)&&policies.includes(policy)&&/^[01]{6}$/.test(bits),"csv id");
   const key=regime+"|"+policy+"|"+bits;check(!seen.has(key),"duplicate source");seen.add(key);
   const k=bits.slice(0,4).split("").filter(x=>x==="1").length,y5=Number(bits[4]),y6=Number(bits[5]),j=y5+y6;
   check(kstr===String(k)&&y5str===String(y5)&&y6str===String(y6),"bit labels");
   const [a,b]=worlds[regime],mass=times(times(power(a,k),power(minus(O,a),4-k)),times(power(b,j),power(minus(O,b),2-j)));
   check(same(parse(massstr),mass),"source mass");
   const q5=policy==="PRECOMMITTED_HALF"?H:f(k+1,6);
   const q6=policy==="PRECOMMITTED_HALF"?H:policy==="PAST_FIXED"?f(k+1,6):f(k+y5+1,7);
   check(same(parse(q5str),q5)&&same(parse(q6str),q6),"forecast leakage or wrong q");
   const l5=square(minus(f(y5),q5)),l6=square(minus(f(y6),q6));
   check(same(parse(l5str),l5)&&same(parse(l6str),l6)&&same(parse(avgstr),over(plus(l5,l6),f(2))),"source Brier");
   const group=regime+"|"+policy;
   weights[group]=plus(weights[group]||Z,mass);
 }
 check(seen.size===576,"source coverage");
 for(const key of found)check(same(weights[key],O),"group mass");
 return {worlds:9,independent_moment_fields:27,contrast_fields:6,source_rows:576,source_numeric_checks:576*6,compared};
}
function mutants(receipt,csv){
 const copy=()=>JSON.parse(JSON.stringify(receipt)),cases=[];
 function rejected(name,obj,data){let failed=false;try{verify(obj,data);}catch(e){failed=true;}check(failed,"mutant accepted: "+name);cases.push(name);}
 let v=copy();v.results.push({...v.results[0]});rejected("duplicate result",v,csv);
 v=copy();v.results.pop();rejected("missing result",v,csv);
 v=copy();v.results[0].expected_t6_brier="999";rejected("numeric tamper",v,csv);
 v=copy();v.scope="CONFIRMATORY_REAL_E2";rejected("evidence upgrade",v,csv);
 v=copy();v.results[0].future_Y6_used_in_forecast=0;rejected("false/zero confusion",v,csv);
 v=copy();v.s70_prescore_freeze_commit="invalid";rejected("freeze swap",v,csv);
 const rows=csv.trimEnd().split("\n");
 rejected("duplicate source",copy(),rows.concat(rows[1]).join("\n")+"\n");
 rejected("missing source",copy(),rows.slice(0,-1).join("\n")+"\n");
 const tampered=rows.slice(),cols=tampered[1].split(",");cols[8]="999";tampered[1]=cols.join(",");
 rejected("future forecast tamper",copy(),tampered.join("\n")+"\n");
 return cases;
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");check(process.argv.length>=4,"usage: node b_gate.js results.json sources.csv");
 const receipt=JSON.parse(fs.readFileSync(process.argv[2],"utf8")),csv=fs.readFileSync(process.argv[3],"utf8");
 const result=verify(receipt,csv),negative=mutants(receipt,csv);
 process.stdout.write(JSON.stringify({status:"PASS",...result,mutants_rejected:negative},null,2)+"\n");
}
