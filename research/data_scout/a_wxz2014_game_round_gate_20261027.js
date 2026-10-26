// WXZ2014 data qualification checks, no source data redistributed.
const fs=require("fs");
function validateRPS(rows,expected){
 const errors=[],groups=new Map(),persons=new Map(),lag=new Map();
 const wins={r:"s",s:"p",p:"r"};
 const counts={rows:rows.length,groups:0,participants:0,rounds:0,mirror_multiset_violations:0,result_mismatches:0,lag_mismatches:0,missing_input_first_round:0};
 const label=v=>v===undefined||v===null?"":String(v).trim().toLowerCase();
 for(const r of rows){
  const game=String(r.game),id=String(r.id),t=Number(r.period),a=label(r.choice),b=label(r["other.choice"]??r.other_choice),result=label(r.result);
  if(!["r","p","s"].includes(a)||!["r","p","s"].includes(b)||!Number.isInteger(t)||t<1){errors.push("INVALID_ROW");continue}
  const key=game+"|"+t;if(!groups.has(key))groups.set(key,[]);groups.get(key).push({id,a,b,result});
  const person=game+"|"+id;if(!persons.has(person))persons.set(person,[]);persons.get(person).push({t,a,input:label(r.input)});
  const outcome=a===b?"tie":wins[a]===b?"win":"lose";
  if(result&&result!==outcome){counts.result_mismatches++;errors.push("RESULT_MISMATCH")}
 }
 const gameSet=new Set();
 for(const [key,v] of groups){
  const [game]=key.split("|");gameSet.add(game);
  if(v.length!==expected.playersPerGroup)errors.push("GROUP_ROUND_SIZE");
  const ids=new Set(v.map(x=>x.id));if(ids.size!==v.length)errors.push("DUPLICATE_PLAYER_IN_ROUND");
  const map=new Map();for(const r of v){const k=r.a+"|"+r.b;map.set(k,(map.get(k)||0)+1)}
  for(const [k,n] of map){const [a,b]=k.split("|");const rev=map.get(b+"|"+a)||0;if(a===b?n%2!==0:n!==rev){counts.mirror_multiset_violations++;errors.push("DYAD_MULTISET_MISMATCH")}}
 }
 for(const [key,v] of persons){
  v.sort((a,b)=>a.t-b.t);
  if(v.length!==expected.roundsPerPerson||v[0]?.t!==1||v.at(-1)?.t!==expected.roundsPerPerson)errors.push("PERSON_ROUND_COVERAGE");
  for(let i=0;i<v.length;i++){
   if(i>0&&v[i].t!==v[i-1].t+1)errors.push("PERSON_GAP");
   if(expected.checkDerivedInput){
    if(i===0){if(v[i].input!==""&&v[i].input!=="na")errors.push("FIRST_ROUND_INPUT_LEAK");else counts.missing_input_first_round++}
    else if(v[i].input!==v[i-1].a){counts.lag_mismatches++;errors.push("LAG_MISMATCH")}
   }
  }
 }
 counts.groups=gameSet.size;counts.participants=persons.size;counts.rounds=groups.size;
 if(expected.groups!==undefined&&counts.groups!==expected.groups)errors.push("GROUP_COUNT");
 if(expected.participants!==undefined&&counts.participants!==expected.participants)errors.push("PERSON_COUNT");
 if(expected.rows!==undefined&&rows.length!==expected.rows)errors.push("ROW_COUNT");
 return {pass:errors.length===0,errors:[...new Set(errors)],counts,limitations:["Action-multiset symmetry is necessary, not sufficient, for uniquely recovering opponent identities without a partner-ID column.","Group identity and payoff treatment mapping require source confirmation."]};
}
if(require.main===module){const args=process.argv.slice(2);if(args.length!==1){process.stderr.write("Usage: node a_wxz2014_game_round_gate.js <decoded-json-array>\n");process.exit(2)}const rows=JSON.parse(fs.readFileSync(args[0],"utf8"));const result=validateRPS(rows,{playersPerGroup:6,roundsPerPerson:300,groups:12,participants:72,rows:21600,checkDerivedInput:Object.prototype.hasOwnProperty.call(rows[0]||{},"input")});process.stdout.write(JSON.stringify(result,null,2)+"\n");if(!result.pass)process.exitCode=1}
module.exports={validateRPS};
