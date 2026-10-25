/* Independent B audit: binomial monotone likelihood-ratio threshold.
 * TV for two binomial laws equals the maximum absolute CDF gap.
 * This program reads frozen original kernels and the archived exhaustive receipt.
 */
function thresholdAudit(original,receipt){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t}return a||1n};
 const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]};
 const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const abs=a=>F(a[0]<0n?-a[0]:a[0],a[1]);
 const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1],eq=(a,b)=>cmp(a,b)===0n;
 const parse=s=>{let z=String(s).split("/");return F(z[0],z[1]||1)};
 const str=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
 const kernels=new Map(original.kernels.map(x=>[x.N+":"+x.regime+":"+x.mechanism,x.rows]));
 let verified=0,zero=0,thresholds=[];
 for(const c of receipt.cases){
   const a=kernels.get(c.N+":"+c.regime+":selection")[c.k].map(parse);
   const b=kernels.get(c.N+":"+c.regime+":transformation")[c.k].map(parse);
   let ca=F(0),cb=F(0),maximum=F(0),threshold=-1;
   for(let j=0;j<c.N;j++){
     ca=add(ca,a[j]);cb=add(cb,b[j]);
     const gap=abs(sub(ca,cb));
     if(cmp(gap,maximum)>0n){maximum=gap;threshold=j}
   }
   if(!eq(maximum,parse(c.TV)))throw Error("CDF-TV mismatch "+JSON.stringify(c));
   if(eq(maximum,F(0)))zero++;
   thresholds.push({N:c.N,k:c.k,regime:c.regime,threshold,TV:str(maximum)});
   verified++;
 }
 if(verified!==28||zero!==8)throw Error("count mismatch");
 return {id:"R166",date:"2026-10-26",method:"independent maximum-CDF-gap optimal count threshold",
  exact_cases_verified:verified,zero_gap_cases:zero,nonzero_gap_cases:verified-zero,
  original_kernel_count:kernels.size,all_match_exhaustive_TV:true,thresholds,
  E2_new:0,E3_new:0,external_replication:false};
}
