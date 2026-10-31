#!/usr/bin/env node
'use strict';
// MKT177. Public historical sunspots; retrospective time-ordered E1 method check.
// Node standard library only; no packages or paid services.
const fs=require('fs'),path=require('path');
function evaluate(csv){
  const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
  const rows=csv.trim().split(/\r?\n/).slice(1).map(s=>{const [y,v]=s.split(",");return {year:Number(y),value:Number(v)}});
  assert(rows.length===309&&rows[0].year===1700&&rows.at(-1).year===2008,"source span");
  rows.forEach((r,i)=>assert(r.year===1700+i&&Number.isFinite(r.value),"row "+i));
  const quantile=(a,alpha)=>{const b=[...a].sort((x,y)=>x-y);const k=Math.ceil((b.length+1)*(1-alpha));assert(k<=b.length&&k>0,"quantile range");return b[k-1]};
  const methods=["expanding","trailing30"];
  const alphas=[0.1,0.2];
  const preds=[];
  for(let year=1900;year<=2008;year++){
    const i=year-1700;
    const history=rows.slice(1,i).map((r,j)=>Math.abs(r.value-rows[j].value));
    const point=rows[i-1].value;
    const actual=rows[i].value;
    const item={year,point,actual,methods:{}};
    for(const method of methods)for(const alpha of alphas){
      const residuals=method==="trailing30"?history.slice(-30):history;
      const radius=quantile(residuals,alpha);
      const covered=Math.abs(actual-point)<=radius+1e-10;
      item.methods[`${method}_${Math.round((1-alpha)*100)}`]={radius,covered,n:residuals.length};
    }
    preds.push(item);
  }
  const report={source_rows:rows.length,source_years:"1700..2008",evaluation_years:"1900..2008",evaluation_n:preds.length,intervals:{}};
  for(const method of methods)for(const alpha of alphas){
    const key=`${method}_${Math.round((1-alpha)*100)}`;
    const arr=preds.map(p=>p.methods[key]);
    let longest=0,current=0;
    for(const v of arr){current=v.covered?0:current+1;longest=Math.max(longest,current)}
    const blocks=[[1900,1929],[1930,1959],[1960,1989],[1990,2008]].map(([start,end])=>{
      const s=preds.filter(p=>p.year>=start&&p.year<=end);
      return {years:`${start}..${end}`,covered:s.filter(p=>p.methods[key].covered).length,n:s.length};
    });
    report.intervals[key]={covered:arr.filter(v=>v.covered).length,n:arr.length,coverage:arr.filter(v=>v.covered).length/arr.length,mean_width:2*arr.reduce((a,v)=>a+v.radius,0)/arr.length,max_consecutive_misses:longest,blocks};
  }
  // Future labels must not change any earlier forecast or calibration radius.
  const mutated=rows.map(x=>({...x}));mutated[1981-1700].value+=10000;
  const original=preds.find(p=>p.year===1980);
  const i=1980-1700;
  const history=mutated.slice(1,i).map((r,j)=>Math.abs(r.value-mutated[j].value));
  assert(mutated[i-1].value===original.point&&mutated[i].value===original.actual,"no future target in 1980");
  for(const method of methods)for(const alpha of alphas){
    const key=`${method}_${Math.round((1-alpha)*100)}`;
    const radius=quantile(method==="trailing30"?history.slice(-30):history,alpha);
    assert(radius===original.methods[key].radius,"future leak "+key);
  }
  // Guard against a naive implementation that leaks the target residual into calibration.
  const toy=[0,0,0,0,0,0,0,0,0,0,1000];
  const past=toy.slice(1,10).map((v,j)=>Math.abs(v-toy[j]));
  const honest=quantile(past,0.1);
  const leaky=quantile([...past,Math.abs(toy[10]-toy[9])],0.1);
  assert(honest===0&&leaky===1000,"leakage control");
  report.checks={source_rows:309,forecasts:109,methods:4,future_1981_perturbation_does_not_change_1980:true,leaky_target_residual_changes_quantile:true};
  return report;
}
if(require.main===module){
 const csv=fs.readFileSync(path.join(__dirname,'mkt176_statsmodels_sunspots_1700_2008.csv'),'utf8');
 const result=evaluate(csv);
 console.log(JSON.stringify(result,null,2));
}
module.exports={evaluate};
