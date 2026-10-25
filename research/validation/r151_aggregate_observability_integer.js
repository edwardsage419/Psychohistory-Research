/* R151 third method: exact integer observability. All data are synthetic. */
const run = function run(){
 const cohorts=[];for(let j=0;j<=12;j++)for(let a=0;a<=12-j;a++)cohorts.push([j,a,12-j-a]);
 const out=[];const det3=m=>m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]);
 for(const k2 of [0,2,3])for(const sj12 of [6,9])for(const sa12 of [6,8]){
  const M=[[0,6*k2,3*k2],[sj12,0,0],[0,sa12,0]], rows=[[1,1,1]];
  for(let t=1;t<=3;t++){const last=rows[t-1];rows.push([0,1,2].map(j=>last.reduce((sum,v,i)=>sum+v*M[i][j],0)));}
  const rankdet=det3(rows.slice(0,3));
  const stats=[];
  for(let t=0;t<=3;t++){
   const classes=new Map();
   for(const x of cohorts){const signature=rows.slice(0,t+1).map(row=>row.reduce((sum,v,i)=>sum+v*x[i],0)).join(":");classes.set(signature,(classes.get(signature)||0)+1);}
   const sizes=Array.from(classes.values());const pairs=sizes.reduce((a,n)=>a+n*(n-1)/2,0);
   stats.push({last_observed_t:t,distinct_signatures:classes.size,max_class_size:Math.max(...sizes),indistinguishable_pairs:pairs});
  }
  if(stats[0].distinct_signatures!==1)throw Error("N0 must be 12");
  if(stats.some((s,i)=>i>0&&s.distinct_signatures<stats[i-1].distinct_signatures))throw Error("nonmonotone");
  if(rankdet!==0&&stats[2].distinct_signatures!==91)throw Error("invertible matrix must identify all");
  out.push({fertility:String(k2===3?"3/2":k2/2),juvenile_survival:String(sj12===9?"3/4":"1/2"),adult_survival:String(sa12===8?"2/3":"1/2"),observability_det_numerator:rankdet,observability_det_denominator:1728,stats});
 }
 const summary={parameter_sets:out.length,initial_cohorts:cohorts.length,aggregate_observations:out.length*cohorts.length*4,zero_determinant_parameter_sets:out.filter(x=>x.observability_det_numerator===0).length,unique_after_t2:out.filter(x=>x.stats[2].distinct_signatures===91).length,unique_after_t3:out.filter(x=>x.stats[3].distinct_signatures===91).length,early_identifiability_rejected:out.every(x=>x.stats[1].distinct_signatures<91)};
 return {research_id:"R151",date:"2026-10-25",evidence:"E1_SYNTHETIC_ONLY",source_protocol:"protocols/R151_AGGREGATE_OBSERVABILITY_EXACT_THIRD_METHOD_FREEZE_2026-10-25.md",summary,parameter_rows:out};
};
console.log(JSON.stringify(run(),null,2));
