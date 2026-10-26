// Six-person one-round perfect-matching identifiability gate. Run: node script.js [optional six-row JSON].
// Only synthetic fixtures run by default. No participant records are stored.
console.log(JSON.stringify((()=>{
function perfectMatchings(ids){
 if(ids.length===0)return [[]];
 const [first,...rest]=ids,out=[];
 for(let i=0;i<rest.length;i++){
  const partner=rest[i],tail=rest.filter((_,j)=>j!==i);
  for(const m of perfectMatchings(tail))out.push([[first,partner],...m]);
 }
 return out;
}
function compatible(rows){
 if(rows.length!==6||new Set(rows.map(x=>x.id)).size!==6)throw Error("six unique IDs required");
 const byId=new Map(rows.map(x=>[x.id,x]));
 return perfectMatchings(rows.map(x=>x.id)).filter(m=>m.every(([a,b])=>{
  const A=byId.get(a),B=byId.get(b);
  return A.other_choice===B.choice&&B.other_choice===A.choice;
 }));
}
function make(choices,other){return choices.map((choice,i)=>({id:i+1,choice,other_choice:other[i]}));}
const fixtures=[
 {name:"all_same",rows:make(["r","r","r","r","r","r"],["r","r","r","r","r","r"]),expected:15},
 {name:"unique",rows:make(["r","r","r","r","p","s"],["r","r","p","s","r","r"]),expected:1},
 {name:"two",rows:make(["r","r","r","r","p","p"],["r","r","p","p","r","r"]),expected:2},
 {name:"inconsistent",rows:make(["r","r","r","r","r","r"],["r","r","r","r","r","p"]),expected:0}
];
const results=fixtures.map(f=>({fixture:f.name,compatible_pairings:compatible(f.rows).length,expected:f.expected}));
if(results.some(r=>r.compatible_pairings!==r.expected))throw Error("synthetic gate failed");
let supplied_round=null;
if(typeof process!=="undefined"&&process.argv[2]){
 const fs=require("fs"),rows=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 supplied_round={row_count:rows.length,compatible_pairings:compatible(rows).length,opponent_ID_identifiable:compatible(rows).length===1};
}
return {schema:"wxz2014_pair_identifiability_synthetic_v1",all_possible_perfect_pairings:perfectMatchings([1,2,3,4,5,6]).length,synthetic_tests:results,real_WXZ2014_rows_checked:supplied_round?supplied_round.row_count:0,supplied_round,interpretation:"opponent choice does not generally identify opponent ID"};
})(),null,2));
