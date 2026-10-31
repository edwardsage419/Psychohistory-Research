function run(csv) {
  const lines=csv.trim().split(/\r?\n/);
  if(lines.shift()!=='"YEAR","SUNACTIVITY"') throw Error("unexpected header");
  const rows=lines.map(line=>{const a=line.split(",");if(a.length!==2)throw Error("bad CSV row");return {year:Number(a[0]),value:Number(a[1])};});
  if(rows.length!==309||rows[0].year!==1700||rows[308].year!==2008)throw Error("source coverage");
  for(let i=0;i<rows.length;i++)if(rows[i].year!==1700+i||!Number.isFinite(rows[i].value))throw Error("missing year or value");
  const pred=(i,kind)=>{
    if(kind==="persistence")return rows[i-1].value;
    if(kind==="lag11")return rows[i-11].value;
    if(kind==="trailing11")return rows.slice(i-11,i).reduce((s,x)=>s+x.value,0)/11;
    if(kind==="expanding")return rows.slice(0,i).reduce((s,x)=>s+x.value,0)/i;
    throw Error("unknown model");
  };
  const names=["persistence","lag11","trailing11","expanding"];
  const indexes=rows.map((r,i)=>i).filter(i=>rows[i].year>=1900&&rows[i].year<=2008);
  const metric=(idx,k)=>{
    const errors=idx.map(i=>pred(i,k)-rows[i].value);
    return {mae:errors.reduce((s,x)=>s+Math.abs(x),0)/errors.length,
      rmse:Math.sqrt(errors.reduce((s,x)=>s+x*x,0)/errors.length),
      bias:errors.reduce((s,x)=>s+x,0)/errors.length};
  };
  const metrics=Object.fromEntries(names.map(k=>[k,metric(indexes,k)]));
  const blocks={};
  for(const [a,b] of [[1900,1929],[1930,1959],[1960,1989],[1990,2008]]){
    const ix=indexes.filter(i=>rows[i].year>=a&&rows[i].year<=b);
    blocks[a+"_"+b]={n:ix.length,mae:Object.fromEntries(names.map(k=>[k,metric(ix,k).mae]))};
  }
  const first=rows.findIndex(x=>x.year===1900);
  const original=pred(first,"persistence");
  const copy=rows[first+1].value;rows[first+1].value+=999999;
  if(pred(first,"persistence")!==original)throw Error("future information leakage");
  rows[first+1].value=copy;
  const result={source_rows:rows.length,years:[rows[0].year,rows[rows.length-1].year],
    evaluation:[1900,2008],n:indexes.length,metrics,blocks,temporal_guard:"PASS"};
  if(indexes.length!==109||Math.abs(metrics.persistence.mae-21.71926605504588)>1e-10||
    Math.abs(metrics.lag11.mae-23.475229357798163)>1e-10||
    Math.abs(metrics.trailing11.mae-37.08949124270223)>1e-10||
    Math.abs(metrics.expanding.mae-38.42079815876109)>1e-10)throw Error("frozen result mismatch");
  return result;
}

if(require.main===module){
  const fs=require("node:fs"),path=require("node:path");
  const csv=fs.readFileSync(path.join(__dirname,"mkt176_statsmodels_sunspots_1700_2008.csv"),"utf8");
  process.stdout.write(JSON.stringify(run(csv),null,2)+"\n");
}
module.exports={run};
