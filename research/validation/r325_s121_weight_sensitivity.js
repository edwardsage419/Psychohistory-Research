#!/usr/bin/env node
"use strict";
/* Frozen R325 S121 project constructed E1, standard Node library. */
const PROFILES=[["U",[[1,3],[1,3],[1,3]]],["EARLY",[[1,2],[1,3],[1,6]]],["LATE",[[1,6],[1,3],[1,2]]],["CENTER",[[1,4],[1,2],[1,4]]]];
const WORLDS=[["linear_eu",[0,1]],["mild_cubic",[1,4]],["strong_cubic",[1,1]]];
const SOURCE_BLOB="b4964ef88aded2c9bd2a70280c067176fedcd597";
const FIELDS=["profile","world_id","policy","kappa","d1","d2","d3","p1","p2","p3","eu","regret","eu_choice","regret_choice","strict_reversal","uniform_choice","changed_vs_uniform","strict_disagreement_vs_uniform"];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function add(a,b){return F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return F(a[0]*b[0],a[1]*b[1]);}
function fmt(a){return a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);}
function sg(a){return a[0]>0n?"A":a[0]<0n?"B":"TIE";}
function score(ds,ps,k){let eu=F(0),reg=F(0);for(let i=0;i<3;i++){const d=BigInt(ds[i]);const dv=F(d);const q=add(dv,mul(k,F(d*d*d)));eu=add(eu,mul(ps[i],dv));reg=add(reg,mul(ps[i],q));}return [eu,reg];}
function sourceRows(text){const lines=text.trimEnd().split(/\r?\n/);const expected="world_id,policy,kappa,d1,d2,d3,weight,eu_advantage,regret_advantage,choice";if(lines.shift()!==expected)throw Error("source CSV header mismatch");if(lines.length!==1029)throw Error("source row count mismatch");const found=new Set();for(const line of lines){const c=line.split(",");if(c.length!==10)throw Error("source field count");const w=Number(c[0]),ds=c.slice(3,6).map(Number);if(!Number.isInteger(w)||w<0||w>2||ds.some(d=>!Number.isInteger(d)||d< -3||d>3))throw Error("source index");const key=[w,...ds].join(":");if(found.has(key))throw Error("duplicate source key");found.add(key);const k=F(...WORLDS[w][1]),ps=[F(1,3),F(1,3),F(1,3)];const [eu,reg]=score(ds,ps,k);if(c[1]!==WORLDS[w][0]||c[2]!==fmt(k)||c[6]!=="1/343"||c[7]!==fmt(eu)||c[8]!==fmt(reg)||c[9]!==sg(reg))throw Error("source mathematical mismatch "+key);}return found;}
function compute(sourceCsv){
 const keys=sourceRows(sourceCsv),lines=[FIELDS.join(",")],summaries=[],allRows=[];
 for(const [profile,raw] of PROFILES){const ps=raw.map(p=>F(...p));if(fmt(ps.reduce(add,F(0)))!=="1")throw Error("weights not normalized");
 for(let world=0;world<3;world++){const [policy,kr]=WORLDS[world],k=F(...kr),count={A:0,B:0,TIE:0},changes={changed:0,strict:0,reversal:0},seen=new Set();
 for(let d1=-3;d1<=3;d1++)for(let d2=-3;d2<=3;d2++)for(let d3=-3;d3<=3;d3++){const ds=[d1,d2,d3],key=[world,...ds].join(":");if(!keys.has(key)||seen.has(key))throw Error("source coverage or duplicate "+key);seen.add(key);
 const [eu,reg]=score(ds,ps,k),reg0=score(ds,[F(1,3),F(1,3),F(1,3)],k)[1],s=sg(reg),u=sg(reg0),reversal=eu[0]*reg[0]<0n?1:0,changed=s===u?0:1,strict=(s!=="TIE"&&u!=="TIE"&&s!==u)?1:0;
 if((ds.every(x=>x>=0)&&reg[0]<0n)||(ds.every(x=>x<=0)&&reg[0]>0n))throw Error("coordinate monotonicity");
 if(world===0&&fmt(eu)!==fmt(reg))throw Error("linear kappa");
 const row=[profile,String(world),policy,fmt(k),...ds.map(String),...ps.map(fmt),fmt(eu),fmt(reg),sg(eu),s,String(reversal),u,String(changed),String(strict)];
 lines.push(row.join(","));allRows.push(row);count[s]++;changes.reversal+=reversal;changes.changed+=changed;changes.strict+=strict;
 }if(seen.size!==343)throw Error("coverage");
 summaries.push({profile,world_id:world,policy,kappa:fmt(k),weights:ps.map(fmt),state_count:343,total_weight:"1",choice_A:count.A,choice_B:count.B,choice_TIE:count.TIE,strict_eu_regret_reversals:changes.reversal,changed_choice_vs_uniform:changes.changed,strict_sign_disagreements_vs_uniform:changes.strict});
 }}
 if(lines.length!==4117||allRows.length!==4116)throw Error("total rows");
 const ref=[[153,153,37,0],[162,162,19,6],[162,162,19,6]];
 for(let w=0;w<3;w++){const s=summaries[w],v=ref[w];if([s.choice_A,s.choice_B,s.choice_TIE,s.strict_eu_regret_reversals].some((x,i)=>x!==v[i]))throw Error("uniform parent mismatch");}
 const byKey=new Map(allRows.map(r=>[[r[0],r[1],r[4],r[5],r[6]].join(":"),r]));
 for(const r of allRows){const rev=[r[6],r[5],r[4]],q=r[0]==="EARLY"?"LATE":r[0]==="LATE"?"EARLY":r[0]==="CENTER"?"CENTER":null;if(q){const v=byKey.get([q,r[1],...rev].join(":"));if(!v||v[11]!==r[11])throw Error("reverse weight symmetry");}}
 const obj={schema:"r325_s121_weight_profiles_e1_v1",protocol_path:"research/validation/R325_S121_STATE_WEIGHT_SENSITIVITY_PRESCORE_FREEZE_2026-11-01.md",freeze_commit:"fff93b2a837d63be4047e932b1c6f66bfff9a0a7",original_source_blob:SOURCE_BLOB,evidence:"E1_PROJECT_CONSTRUCTED_ONLY",profiles:PROFILES.map(([name,weights])=>({name,weights:weights.map(p=>fmt(F(...p)))})),worlds:WORLDS.map(([name,k])=>({name,kappa:fmt(F(...k))})),rows:4116,states_per_profile_world:343,summary:summaries,controls:{uniform_parent_replayed:true,coordinatewise_monotonicity:true,kappa_zero_matches_eu:true,reverse_weight_symmetry:true,all_unique:true},human_E2:"NOT_RUN",historical_E3:"NOT_RUN",external_independent:"NOT_RUN"};
 return {csv:lines.join("\n")+"\n",json:JSON.stringify(obj,null,2)+"\n",obj};
}
if(typeof module!=="undefined")module.exports={compute};
if(typeof require!=="undefined"&&require.main===module){
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const original=fs.readFileSync(path.resolve(__dirname,"../R325/R325_ALL_1029_ARTIFICIAL_REGRET_STATES.csv"));
const sha=crypto.createHash("sha1").update(Buffer.from("blob "+original.length+"\0")).update(original).digest("hex");
if(sha!==SOURCE_BLOB)throw Error("original Git blob mismatch");
const out=compute(original.toString("utf8"));
const cp=path.join(__dirname,"R325_S121_ALL_4116_WEIGHTED_STATES.csv"),jp=path.join(__dirname,"R325_S121_EXACT_WEIGHT_RESULTS.json");
if(process.argv.includes("--emit")){fs.writeFileSync(cp,out.csv);fs.writeFileSync(jp,out.json);console.log("R325_S121_EMIT",out.obj.rows);}
else if(process.argv.includes("--check")){if(fs.readFileSync(cp,"utf8")!==out.csv||fs.readFileSync(jp,"utf8")!==out.json)throw Error("output mismatch");console.log("R325_S121_CHECK_PASS",out.obj.rows);}
else console.log("Usage: node r325_s121_weight_sensitivity.js --emit|--check");
}
