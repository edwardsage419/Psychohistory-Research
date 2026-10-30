// Reproduce exploratory Akata 2024 PD outcome label audit using author's public CSV.
// Run: node a_akata2024_pd_label_by_opponent_20261030.js /path/to/repgames.csv
function auditCSV(content){
 const lines=content.trim().split(/\r?\n/),head=lines.shift();if(head!=="id,game,action,score,opponent,guess,coordination")throw Error("HEADER");
 const all=lines.map((line,i)=>{const v=line.split(",");if(v.length!==7)throw Error("CSV_FIELD_COUNT "+i);return {id:+v[0],game:v[1],action:+v[2],score:+v[3],opponent:v[4],guess:v[5],coordination:+v[6]}}),pd=all.filter(x=>x.game==="PD");
 if(all.length!==3900||pd.length!==1950)throw Error("ROW_COUNT");
 const groups={};for(let g of ["Base","Prompted"]){const r=pd.filter(x=>x.opponent===g);let subjects=new Set(r.map(x=>x.id));let score5=r.filter(x=>x.score===5).length,score8=r.filter(x=>x.score===8).length;groups[g]={rows:r.length,subjects:subjects.size,score5_mutual_defection:score5,score8_mutual_cooperation:score8,score5_rate:score5/r.length,score8_rate:score8/r.length,other_score_counts:Object.fromEntries([...new Set(r.map(x=>x.score))].sort((a,b)=>a-b).map(v=>[v,r.filter(x=>x.score===v).length]))};if(r.length!==subjects.size*10)throw Error("SUBJECT_ROUNDS");}
 const bad=pd.filter(x=>x.action===0&&x.score===0);
 if(bad.length!==1)throw Error("ANOMALY_COUNT");
 const OR=(key)=>{const a=groups.Prompted,b=groups.Base;let x=a[key],y=b[key];return (x*(b.rows-y))/((a.rows-x)*y)};
 return {public_csv_rows:all.length,pd_rows:pd.length,pd_subjects:new Set(pd.map(x=>x.id)).size,groups,pooled_round_level_odds_ratio:{score5:OR("score5_mutual_defection"),score8:OR("score8_mutual_cooperation")},anomalous_pd_action0_score0:bad.length,anomalous_subject_ids:bad.map(x=>x.id)};
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");if(!process.argv[2])throw Error("CSV path required");console.log(JSON.stringify(auditCSV(fs.readFileSync(process.argv[2],"utf8")),null,2))}
