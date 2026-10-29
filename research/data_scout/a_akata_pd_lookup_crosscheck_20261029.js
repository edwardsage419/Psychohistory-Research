/* A track source replay: compare public human PD CSV with original GPT4 lookup maps.
   Requires three original files. No participant-level source data is redistributed.
   Node: node a_akata_pd_lookup_crosscheck_20261029.js repgames.csv pd_gpt4_lookup.json pd_variation_predict_gpt4_lookup.json */
function auditAkataPD(csv,base,prompted){
  const lines=csv.trim().split(/\r?\n/),header=lines.shift();
  if(header!=="id,game,action,score,opponent,guess,coordination")throw Error("unexpected CSV schema");
  const lookups=[JSON.parse(base),JSON.parse(prompted)], histories=new Map(),participants=new Map();
  let n=0,match=0,mismatch=0,unknown=0,firstRoundMismatch=0,anomaly=[];
  let byCondition={Base:{n:0,match:0,mismatch:0},Prompted:{n:0,match:0,mismatch:0}};
  for(let i=0;i<lines.length;i++){
    const cols=lines[i].split(",");
    if(cols.length!==7)throw Error("row schema "+(i+2));
    const [id,game,action,score,opponent]=cols;
    if(game!=="PD")continue;
    if(!["Base","Prompted"].includes(opponent)||!["0","1"].includes(action))throw Error("category");
    const h=histories.get(id)||"";
    const lookup=lookups[opponent==="Base"?0:1][h];
    const expected=action==="1"?(lookup==="J"?8:lookup==="F"?0:null):
                                  (lookup==="J"?10:lookup==="F"?5:null);
    const observed=Number(score),condition=byCondition[opponent];
    n++;condition.n++;
    if(expected===null){unknown++;}else if(expected===observed){match++;condition.match++;}
    else{mismatch++;condition.mismatch++;if(h.length===0)firstRoundMismatch++;
      anomaly.push({line:i+2,id,round:h.length+1,condition:opponent,observed,expected,history:h});}
    histories.set(id,h+(action==="1"?"J":"F"));
    let p=participants.get(id)||{n:0,bad:0};p.n++;if(expected!==observed)p.bad++;participants.set(id,p);
  }
  if(lines.length!==3900||n!==1950||participants.size!==195||
     [...participants.values()].some(p=>p.n!==10))throw Error("source identity changed");
  return {source_rows:lines.length,PD_rows:n,participants:participants.size,
    lookup_match:match,lookup_mismatch:mismatch,lookup_unknown:unknown,
    first_round_mismatch:firstRoundMismatch,
    participants_with_any_mismatch:[...participants.values()].filter(p=>p.bad>0).length,
    by_condition:byCondition,
    line3061:anomaly.find(z=>z.line===3061)||null,
    limitation:"Source lookup version and cleaned CSV row chronology are not independently established; mismatches are diagnostics, not confirmed original experiment errors."};
}
if(typeof module!=="undefined"&&require.main===module){
  const fs=require("fs");
  const a=process.argv.slice(2);
  if(a.length!==3)throw Error("expected CSV, base lookup, prompted lookup");
  process.stdout.write(JSON.stringify(auditAkataPD(...a.map(p=>fs.readFileSync(p,"utf8"))),null,2)+"\n");
}
