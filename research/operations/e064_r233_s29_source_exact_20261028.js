// E064: independent source-first integer-mass audit. Node.js built-in modules only.
// Run: node research/operations/e064_r233_s29_source_exact_20261028.js
const fs = require("node:fs");
const path = require("node:path");
function audit(csvText,receiptText){
  const lines=csvText.trim().split(/\r?\n/);const cols=lines.shift().split(",");
  const rows=lines.map(line=>Object.fromEntries(line.split(",").map((x,i)=>[cols[i],x])));
  const receipt=JSON.parse(receiptText);let checks=0;const ck=(ok,desc)=>{checks++;if(!ok)throw Error("CHECK_"+checks+": "+desc)};
  ck(rows.length===256,"256 rows");ck(receipt.results.length===32,"32 conditions");
  const byWorld=new Map();
  for(const row of rows){
    ck(row.original_probability==="1/32","source probability");
    ck(row.observed_group_G==="0"||row.observed_group_G==="1","group");
    for(let j=1;j<=3;j++)ck(Number.isInteger(Number(row["observed_X"+j])),"X integer");
    if(!byWorld.has(row.world))byWorld.set(row.world,[]);
    byWorld.get(row.world).push(row);
  }
  ck(byWorld.size===8,"eight worlds");
  for(const [w,rs] of byWorld)ck(rs.length===32,"32 atoms "+w);
  const distributions=new Map();
  for(const result of receipt.results){
    const rs=byWorld.get(result.world);ck(!!rs,"world present");
    const k=result.q_numerator_over_4;ck([0,1,2,4].includes(k),"q");
    const map=new Map();const groups=[0,0];const sums=[[0,0,0],[0,0,0]];
    for(const row of rs){
      const g=Number(row.observed_group_G);const xs=[1,2,3].map(j=>Number(row["observed_X"+j]));
      for(const [h,m] of [[g,4-k],[1-g,k]]){
        if(m===0)continue;
        const key=[h,...xs].join(",");map.set(key,(map.get(key)||0)+m);groups[h]+=m;
        xs.forEach((x,j)=>sums[h][j]+=m*x);
      }
    }
    const expected=result.joint_mass_units;const keys=new Set([...map.keys(),...Object.keys(expected)]);
    for(const key of keys)ck((map.get(key)||0)===(expected[key]||0),result.world+" q="+k+" cell "+key);
    ck(map.size===result.positive_joint_cells,"positive cells");
    ck([...map.values()].reduce((a,b)=>a+b,0)===128,"total mass");
    for(let h=0;h<2;h++)ck(groups[h]===result.observed_group_mass_units[h]&&groups[h]===64,"group mass");
    for(let j=0;j<3;j++){
      const n=sums[1][j]-sums[0][j],str=result.observed_mean_difference[j];
      const parts=str.split("/").map(Number);const den=parts[1]||1;
      ck(n*den===parts[0]*64,"mean "+result.world+" q="+k+" X"+(j+1));
    }
    distributions.set(result.world+"|"+k,map);
  }
  for(const [a,b] of [["TRUE_LATENT_MEAN_SHIFT","INTERCEPT_SHIFT_ALIAS"],["FULL_STRICT_INVARIANT","LATENT_SCALE_ALIAS"]]){
    for(const k of [0,1,2,4]){
      const ma=distributions.get(a+"|"+k),mb=distributions.get(b+"|"+k);
      ck(!!ma&&!!mb,"alias exist");
      for(const key of new Set([...ma.keys(),...mb.keys()]))ck((ma.get(key)||0)===(mb.get(key)||0),"alias cell");
    }
  }
  return {checks,rows:rows.length,worlds:byWorld.size,conditions:receipt.results.length,failures:0};
}
const root=path.resolve(__dirname,"../..");
const csv=fs.readFileSync(path.join(root,"research/R233/R233_ALL_256_ORIGINAL_TWO_GROUP_MEASUREMENT_SOURCES.csv"),"utf8");
const receipt=fs.readFileSync(path.join(root,"research/validation/R233_S29_GROUP_LABEL_32_CONDITION_EXACT_RECEIPT_2026-10-28.json"),"utf8");
const result=audit(csv,receipt);
if(result.checks!==3213)throw Error("Unexpected check count");
process.stdout.write(JSON.stringify(result)+"\n");
