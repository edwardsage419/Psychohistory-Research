"use strict";
// MKT131: exact percentile bootstrap coverage under perfect within-group dependence.
// Six independent Bernoulli(1/2) groups, two identical records per group.
// Standard JS BigInt only; no network, package, randomness or user data.
const choose=(n,k)=>{let a=1n;for(let j=1;j<=k;j++)a=a*BigInt(n-j+1)/BigInt(j);return a;};
const bitcount=x=>{let n=0;while(x){n+=x&1;x>>=1;}return n;};
function qbin(n,k,target){
 if(!Number.isInteger(n)||n<=0||!Number.isInteger(k)||k<0||k>6||![1,39].includes(target))throw Error("invalid input");
 const den=6n**BigInt(n);let acc=0n;
 for(let j=0;j<=n;j++){
  acc+=choose(n,j)*BigInt(k)**BigInt(j)*BigInt(6-k)**BigInt(n-j);
  if(40n*acc>=BigInt(target)*den)return j;
 }
 throw Error("quantile mass");
}
function calculate(){
 const groups=6,rows=12;let rowHits=0,groupHits=0;const byK=[];
 for(let k=0;k<=groups;k++){
  const r=[qbin(rows,k,1),qbin(rows,k,39)];
  const g=[qbin(groups,k,1),qbin(groups,k,39)];
  byK.push({k,multiplicity:Number(choose(groups,k)),row_interval:r.map(x=>x+"/"+rows),group_interval:g.map(x=>x+"/"+groups),
   row_covers_half:r[0]*2<=rows&&r[1]*2>=rows,
   group_covers_half:g[0]*2<=groups&&g[1]*2>=groups});
 }
 for(let mask=0;mask<64;mask++){
  const v=byK[bitcount(mask)];
  rowHits+=Number(v.row_covers_half);groupHits+=Number(v.group_covers_half);
 }
 return {research:"MKT131",evidence:"E1_ARTIFICIAL",groups,records_per_group:2,worlds:64,
  nominal_percentile_coverage:"19/20",population_mean:"1/2",
  row_bootstrap_coverage:rowHits+"/64",group_bootstrap_coverage:groupHits+"/64",
  true_sampling_variance:"1/24",expected_row_bootstrap_variance:"5/288",
  expected_group_bootstrap_variance:"5/144",by_k:byK};
}
function selftest(){
 const x=calculate();
 if(x.row_bootstrap_coverage!=="50/64"||x.group_bootstrap_coverage!=="62/64")throw Error("coverage");
 if(x.by_k[1].row_covers_half||!x.by_k[1].group_covers_half)throw Error("K1");
 if(x.by_k[5].row_covers_half||!x.by_k[5].group_covers_half)throw Error("K5");
 if(x.by_k.reduce((s,z)=>s+z.multiplicity,0)!==64)throw Error("mass");
 let rejected=0;
 for(const a of [[0,1,1],[6,7,1],[6,2,2]]){
  try{qbin(...a);}catch(e){rejected++;}
 }
 if(rejected!==3)throw Error("negative controls");
 return {pass:true,worlds:64,coverage_row:x.row_bootstrap_coverage,
  coverage_group:x.group_bootstrap_coverage,negative_controls_rejected:rejected};
}
if(typeof module!=="undefined"&&require.main===module){
 const args=process.argv.slice(2);
 if(args.includes("--selftest"))console.log(JSON.stringify(selftest()));
 if(args.includes("--json")||args.length===0)console.log(JSON.stringify(calculate(),null,2));
}
