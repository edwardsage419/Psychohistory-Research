// R235 S31 source row exact rational enumeration. Node.js 18+; no paid services.
// Usage: node research/validation/r235_s31_response_selection_exact_20261028.js research/R235/R235_ALL_432_ORIGINAL_DIF_ITEM_RESPONSE_SOURCES.csv > /tmp/r235_s31.json
const fs=require("node:fs");
function calculate(csvText) {
  const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a};
  const rat=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}if(b===0n)throw Error("zero denominator");const g=gcd(a,b);return [a/g,b/g]};
  const parse=s=>{const t=String(s).split("/");return rat(t[0],t[1]??"1")};
  const add=(a,b)=>rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const sub=(a,b)=>rat(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
  const mul=(a,b)=>rat(a[0]*b[0],a[1]*b[1]);
  const div=(a,b)=>rat(a[0]*b[1],a[1]*b[0]);
  const str=a=>a[1]===1n?String(a[0]):a[0]+"/"+a[1];
  const Z=rat(0),ONE=rat(1),HALF=rat(1,2);
  const lines=csvText.trim().split(/\r?\n/),cols=lines.shift().split(",");
  const rows=lines.map(l=>Object.fromEntries(l.split(",").map((v,i)=>[cols[i],v])));
  if(rows.length!==432)throw Error("frozen source count changed");
  const worlds=[...new Set(rows.map(r=>r.world))];
  if(worlds.length!==9)throw Error("frozen worlds changed");
  const rules=["ALL","G1_SUCCESS_HALF","G1_FAILURE_HALF","CONCORDANT_HALF","DISCORDANT_HALF"];
  const weight=(rule,g,y)=> {
    if(rule==="ALL")return ONE;
    if(rule==="G1_SUCCESS_HALF")return g===1&&y===1?HALF:ONE;
    if(rule==="G1_FAILURE_HALF")return g===1&&y===0?HALF:ONE;
    if(rule==="CONCORDANT_HALF")return g===y?HALF:ONE;
    if(rule==="DISCORDANT_HALF")return g!==y?HALF:ONE;
    throw Error("unknown rule");
  };
  const out=[];
  for(const world of worlds){
    const wr=rows.filter(r=>r.world===world);
    if(wr.length!==48)throw Error("bad world size");
    const oracle=[-1,0,1].map(k=>{
      const p=g=>parse(wr.find(r=>Number(r.observed_group_G)===g&&Number(r.oracle_latent_ability_index_k)===k).oracle_focal_item2_probability);
      return str(sub(p(1),p(0)));
    });
    for(const rule of rules){
      const masses=new Map(), joint=new Map();
      let total=Z;
      for(const row of wr){
        const g=Number(row.observed_group_G),y=Number(row.observed_Y2);
        const p=mul(parse(row.original_source_probability),weight(rule,g,y));
        total=add(total,p);
        const key=""+g+row.observed_Y1+row.observed_Y2+row.observed_Y3;
        masses.set(key,add(masses.get(key)??Z,p));
      }
      if(masses.size!==16||total[0]<=0n)throw Error("invalid support");
      for(const [key,p] of masses)joint.set(key,div(p,total));
      let normalized=Z;
      for(const p of joint.values())normalized=add(normalized,p);
      if(str(normalized)!=="1")throw Error("mass != 1");
      const groupMass=[Z,Z],groupSuccess=[Z,Z],tables=Array.from({length:3},()=>[[Z,Z],[Z,Z]]);
      for(const [key,p] of joint){
        const [g,y1,y2,y3]=[...key].map(Number);
        groupMass[g]=add(groupMass[g],p);
        if(y2===1)groupSuccess[g]=add(groupSuccess[g],p);
        tables[y1+y3][g][y2]=add(tables[y1+y3][g][y2],p);
      }
      let mhNum=Z,mhDen=Z;
      const dif=[];
      for(const t of tables){
        const A=t[1][1],B=t[1][0],C=t[0][1],D=t[0][0];
        if([A,B,C,D].some(x=>x[0]<=0n))throw Error("empty MH cell");
        const N=add(add(A,B),add(C,D));
        mhNum=add(mhNum,div(mul(A,D),N));
        mhDen=add(mhDen,div(mul(B,C),N));
        dif.push(str(sub(div(A,add(A,B)),div(C,add(C,D)))));
      }
      out.push({world,rule,source_atoms:48,retention_probability:str(total),selected_joint:Object.fromEntries([...joint].sort((a,b)=>a[0].localeCompare(b[0])).map(([k,v])=>[k,str(v)])),group_masses:groupMass.map(str),focal_success_rates_by_group:groupSuccess.map((p,g)=>str(div(p,groupMass[g]))),anchor_score_focal_differences:dif,mh_odds_ratio:str(div(mhNum,mhDen)),oracle_fixed_ability_dif_unchanged:oracle});
    }
  }
  return {research_id:"R235",phase:"S31",freeze_commit:"c0c353ba1cd87674ad7d791370ac78df66311ccd",source_rows:432,worlds:9,rules,conditions:out.length,evidence:"E1_SYNTHETIC_ONLY",E2:0,E3:0,R073:"FROZEN",PESEN_v0_1:"FROZEN",conditions_data:out};
}
if(require.main===module){if(process.argv.length!==3)throw Error("supply frozen CSV path");process.stdout.write(JSON.stringify(calculate(fs.readFileSync(process.argv[2],"utf8")),null,2)+"\n");}
module.exports={calculate};
