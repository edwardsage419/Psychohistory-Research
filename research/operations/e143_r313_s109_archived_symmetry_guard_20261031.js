"use strict";
/* E143: independent persisted-receipt symmetry audit for R313 S109. Node stdlib. */
function req(ok,msg){if(!ok)throw new Error(msg);}
function gcd(a,b){while(b!==0n){const t=a%b;a=b;b=t;}return a<0n?-a:a;}
function rat(v){req(typeof v==="string"&&/^-?[0-9]+(?:\/[1-9][0-9]*)?$/.test(v),"fraction syntax");let [n,d]=v.split("/");n=BigInt(n);d=d?BigInt(d):1n;const g=gcd(n,d);return [n/g,d/g];}
function plus(a,b){let n=a[0]*b[1]+b[0]*a[1],d=a[1]*b[1],g=gcd(n,d);return[n/g,d/g];}
function equal(a,b){return a[0]*b[1]===b[0]*a[1];}
function transform(w,k){if(k===0)return w^42;if(k===1)return w^21;return ((w&3)<<4)|(w&12)|(w>>4);}
function active(w){let b=Array.from({length:6},(_,i)=>(w>>(5-i))&1);let s=0;for(let [a,c] of [[0,1],[1,2]])if((b[2*a]===b[2*c])+(b[2*a+1]===b[2*c+1])===1)s++;return s;}
function check(doc){
 req(doc.schema==="R313_S109_exact_three_step_e1_v1","schema");
 req(doc.original_R313_one_step_blob==="b05bd67ee362bfcbb77726ab9262c807c93236cd","source blob");
 req(doc.world_count===64&&doc.step_count===4&&doc.absorbing_worlds===16,"universe metadata");
 req(doc.full_probability_cells_checked===12288,"cell metadata");
 req(Array.isArray(doc.worlds)&&doc.worlds.length===256,"row count");
 const zero=[0n,1n],one=[1n,1n],arr=[];let rowCells=0,nonzero=0,metricChecks=0;
 for(let t=0;t<4;t++){arr[t]=[];for(let w=0;w<64;w++){
  const row=doc.worlds[t*64+w];req(row.initial_world===w&&row.step===t,"row identity");
  const v=Array.from({length:64},()=>zero),seen=new Set();let sum=zero;
  req(Array.isArray(row.probabilities),"probabilities");
  for(const cell of row.probabilities){
   req(Array.isArray(cell)&&cell.length===2,"cell shape");
   const [k,p]=cell;req(Number.isInteger(k)&&k>=0&&k<64&&!seen.has(k),"cell identity");seen.add(k);
   const r=rat(p);req(r[0]>0n,"nonzero positive");v[k]=r;sum=plus(sum,r);nonzero++;
  }
  req(equal(sum,one),"normalization");
  let absorbed=zero,expected=zero;
  for(let k=0;k<64;k++){const x=v[k];if(active(k)===0)absorbed=plus(absorbed,x);for(let i=0;i<active(k);i++)expected=plus(expected,x);}
  req(equal(absorbed,rat(row.absorbed_probability)),"absorbed");
  req(equal(expected,rat(row.expected_active_edges)),"active edges");
  metricChecks+=2;rowCells+=64;arr[t][w]=v;
 }}
 const byStep=Object.fromEntries([0,1,2,3].map(t=>[String(t),arr[t].reduce((s,v)=>s+v.filter(x=>x[0]!==0n).length,0)]));
 req(JSON.stringify(byStep)===JSON.stringify(doc.nonzero_probabilities_by_step),"support metadata");
 req(JSON.stringify(doc.world1)===JSON.stringify([0,1,2,3].map(t=>doc.worlds[t*64+1])),"world1");
 let symmetryCells=0;
 for(let t=0;t<4;t++)for(let op=0;op<3;op++)for(let w=0;w<64;w++)for(let k=0;k<64;k++){
  req(equal(arr[t][w][k],arr[t][transform(w,op)][transform(k,op)]),"crossworld symmetry "+t+"/"+op+"/"+w+"/"+k);
  symmetryCells++;
 }
 return {rows:256,fullCells:rowCells,nonzeroCells:nonzero,metricChecks,symmetryCells,byStep};
}
function main(doc){
 const positive=check(doc),mutations=[];
 function mutate(label,fn){const d=JSON.parse(JSON.stringify(doc));fn(d);req(JSON.stringify(d)!==JSON.stringify(doc),"nonempty mutation");try{check(d);}catch(e){mutations.push({label,rejected:true,reason:String(e.message).slice(0,80)});return;}throw new Error("ACCEPTED MUTATION "+label);}
 mutate("swap_equal_activity_mass_t3",d=>{let cells=d.worlds[3*64+1].probabilities;let a=cells.find(x=>x[0]===1),b=cells.find(x=>x[0]===5);req(!!a&&!!b,"mutation targets");[a[1],b[1]]=[b[1],a[1]];d.world1[3]=JSON.parse(JSON.stringify(d.worlds[3*64+1]));});
 mutate("swap_equal_activity_mass_t2",d=>{let cells=d.worlds[2*64+1].probabilities;let a=cells.find(x=>x[0]===1),b=cells.find(x=>x[0]===5);req(!!a&&!!b,"mutation targets");[a[1],b[1]]=[b[1],a[1]];d.world1[2]=JSON.parse(JSON.stringify(d.worlds[2*64+1]));});
 mutate("false_nonzero_count",d=>d.nonzero_probabilities_by_step["3"]++);
 mutate("false_world1_snapshot",d=>d.world1[3].step=2);
 return {positive,mutations};
}
if(typeof module!=="undefined"&&require.main===module){const fs=require("fs");const file=process.argv[2]||"research/validation/R313_S109_FULL_256_WORLD_STEP_DISTRIBUTIONS.json";console.log(JSON.stringify(main(JSON.parse(fs.readFileSync(file,"utf8"))),null,2));}
