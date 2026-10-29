"use strict";
const M={
ALIGNED_DOMINANCE:[[1,2,2,3],[2,3,3,4],[3,4,4,5],[4,5,5,6],[5,6,6,7]],
HIDDEN_JOINT_TAIL:[[0,0,0,12],[2,3,3,4],[3,3,3,3],[4,4,4,4],[5,5,5,5]],
REGRET_VS_WORST:[[0,0,0,8],[2,2,2,5],[4,4,4,4],[5,5,5,5],[6,6,6,6]],
NONMONOTONE_SHOCK_COST:[[4,1,1,0],[2,2,2,2],[3,1,2,3],[5,0,0,5],[6,6,6,6]],
TWO_SHOCK_INTERACTION:[[0,0,0,10],[1,4,4,5],[3,3,3,3],[4,4,4,4],[6,6,6,6]],
ADDITIVE_COMMON_SHOCK:[[0,1,2,3],[2,3,4,5],[3,4,5,6],[4,5,6,7],[5,6,7,8]],
HIDDEN_TAIL_ALIAS:[[0,0,0,0],[2,3,3,4],[3,3,3,3],[4,4,4,4],[5,5,5,5]],
TIED_WORST_CASE:[[0,2,2,2],[1,1,1,3],[2,2,2,2],[3,3,3,3],[4,4,4,4]],
HEDGE_VS_NOMINAL:[[0,6,6,6],[2,2,4,4],[3,3,3,3],[1,5,5,5],[4,4,4,4]]};
const A="ABCDE",S=["00","01","10","11"];
const H="world,original_action,original_shock_bit_1,original_shock_bit_2,original_uncertainty_budget_Gamma,original_scenario_is_budget_eligible,original_action_scenario_loss,original_complete_action_scenario_budget_design_mass,oracle_independent_fair_two_shock_probability";
function chk(v,m){if(!v)throw Error(m)}
function analyze(csv){
 const lines=csv.trimEnd().split(/\r?\n/),seen=new Set(),t={};
 chk(lines.length===541&&lines[0]===H,"source header/row count");
 for(const w of Object.keys(M))t[w]=Array.from({length:5},()=>Array(4).fill(null));
 for(const [n,line] of lines.slice(1).entries()){
  const f=line.split(",");chk(f.length===9,"fields "+n);
  const [w,a,x,y,g,e,c,m,p]=f;
  chk(Object.hasOwn(M,w)&&A.includes(a)&&["0","1"].includes(x)&&["0","1"].includes(y)&&["0","1","2"].includes(g),"identity "+n);
  const i=A.indexOf(a),j=S.indexOf(x+y),key=[w,a,x,y,g].join(":");
  chk(!seen.has(key),"duplicate "+key);seen.add(key);
  chk(e===String(Number(Number(x)+Number(y)<=Number(g))),"eligible "+key);
  chk(c===String(M[w][i][j]),"frozen cost "+key);
  chk(m==="1/60"&&p==="1/4","source mass "+key);
  t[w][i][j]=Number(c);
 }
 chk(seen.size===540,"source uniqueness");
 const groups=[],actions=[];
 for(const [w,mat] of Object.entries(t)){
  chk(mat.every(r=>r.every(x=>x!==null)),"coverage "+w);
  const clair=S.map((_,j)=>Math.min(...mat.map(r=>r[j])));
  const W2=mat.map(r=>Math.max(...r)),R2=mat.map(r=>Math.max(...r.map((v,j)=>v-clair[j])));
  const bw=Math.min(...W2),br=Math.min(...R2);
  for(let g=0;g<=2;g++){
   const ids=S.map((_,j)=>j).filter(j=>Number(S[j][0])+Number(S[j][1])<=g);
   const wg=mat.map(r=>Math.max(...ids.map(j=>r[j]))),rg=mat.map(r=>Math.max(...ids.map(j=>r[j]-clair[j])));
   for(let i=0;i<5;i++)actions.push({world:w,budget:g,action:A[i],training_worst:wg[i],training_regret:rg[i],worst_U2:W2[i],regret_U2:R2[i],excess_worst_U2:W2[i]-bw,excess_regret_U2:R2[i]-br,fair_mean_num_over4:mat[i].reduce((a,b)=>a+b,0)});
   for(const obj of ["minimax_cost","minimax_regret"]){
    const scores=obj==="minimax_cost"?wg:rg,v=Math.min(...scores),winners=[...A].filter((_,i)=>scores[i]===v);
    const members=winners.map(a=>{const i=A.indexOf(a);return {action:a,worst_U2:W2[i],regret_U2:R2[i],excess_worst_U2:W2[i]-bw,excess_regret_U2:R2[i]-br,fair_mean_num_over4:mat[i].reduce((x,y)=>x+y,0)}});
    const k=obj==="minimax_cost"?"excess_worst_U2":"excess_regret_U2",v2=members.map(m=>m[k]);
    groups.push({world:w,training_budget:g,objective:obj,training_optimum:v,winners,members,own_excess_min:Math.min(...v2),own_excess_max:Math.max(...v2),own_zero_winners:v2.filter(x=>x===0).length});
   }
  }
 }
 chk(groups.length===54&&actions.length===135,"output count");
 const summary={};
 for(const obj of ["minimax_cost","minimax_regret"]){const g=groups.filter(x=>x.objective===obj);summary[obj]={all_zero:g.filter(x=>x.own_excess_max===0).length,some_zero:g.filter(x=>x.own_excess_min===0&&x.own_excess_max>0).length,all_positive:g.filter(x=>x.own_excess_min>0).length}}
 chk(groups.filter(g=>g.training_budget===2).every(g=>g.own_excess_max===0),"Gamma2 oracle");
 chk(t.HIDDEN_JOINT_TAIL.every((r,i)=>r.slice(0,3).every((v,j)=>v===t.HIDDEN_TAIL_ALIAS[i][j])),"alias");
 return {research_id:"R260",supplement:"S56",source_blob:"7a818b12f7a8e1ca974e16854cb146dcd57874f5",source_rows:540,action_rows:135,selection_groups:54,summary,groups,actions,evidence:"E1_SYNTHETIC_INTERNAL",new_human_E2:0,new_historical_E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN"};
}
if(typeof module!=="undefined")module.exports={analyze};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");
 if(process.argv.length!==3)throw Error("Usage: node script.js source.csv");
 process.stdout.write(JSON.stringify(analyze(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");
}
