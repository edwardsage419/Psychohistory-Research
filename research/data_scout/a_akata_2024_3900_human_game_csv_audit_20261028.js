"use strict";
/* A-track: node script.js repgames.csv; public aggregates only, no row export */
function main(csv){
 const lines=csv.trimEnd().split(/\r?\n/),header=lines.shift();
 if(header!=="id,game,action,score,opponent,guess,coordination")throw Error("unexpected data schema");
 const ids=new Map(),groups={},gameCounts={},cross={},bad=[];
 let pd=0,bos=0,score5=0,cooperate=0;
 for(let i=0;i<lines.length;i++){
  const f=lines[i].split(",");if(f.length!==7)throw Error("malformed CSV row "+(i+2));
  const [id,game,action,score,opponent,guess,coordination]=f;
  if(!/^\d+$/.test(id)||!["PD","BoS"].includes(game)||!["0","1"].includes(action))throw Error("invalid field "+(i+2));
  let x=ids.get(id)||{total:0,PD:0,BoS:0,opponents:new Set()};x.total++;x[game]++;x.opponents.add(opponent);ids.set(id,x);
  gameCounts[game]=(gameCounts[game]||0)+1;
  if(game==="PD"){
   pd++;const k=action+"|"+score;cross[k]=(cross[k]||0)+1;
   if(action==="1")cooperate++;
   if(score==="5")score5++;
   const g=groups[opponent]||(groups[opponent]={n:0,action1:0,score5:0});
   g.n++;g.action1+=action==="1"?1:0;g.score5+=score==="5"?1:0;
   if(!(["0","5","8","10"].includes(score)))bad.push(i+2);
  }else bos++;
 }
 if(lines.length!==3900||ids.size!==195||pd!==1950||bos!==1950)throw Error("unexpected sample size");
 for(const [id,x] of ids){if(x.total!==20||x.PD!==10||x.BoS!==10||x.opponents.size!==1)throw Error("ID/game/block irregularity "+id);}
 if(cooperate!==931||score5!==783||cross["1|5"])throw Error("payoff/action source invariant failed");
 return {source_repo:"eliaka/repeatedgames",source_file:"human_experiment/analysis/repgames.csv",source_git_blob:"2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95",source_bytes:csv.length,rows:lines.length,unique_anonymous_ids:ids.size,rounds_per_id_per_game:10,PD_rows:pd,BoS_rows:bos,PD_action1_count:cooperate,PD_score5_count:score5,PD_action_score_cross:cross,PD_by_opponent:groups,PD_action0_score0_rows:cross["0|0"]||0,PD_action1_score5_rows:cross["1|5"]||0,license_status:"MIT_REPO_LICENSE_DATA_SPECIFIC_REUSE_UNCLEAR",R073_frozen_direct_score_eligible:false,external_independent_reproduction:false};
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");process.stdout.write(JSON.stringify(main(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");}
