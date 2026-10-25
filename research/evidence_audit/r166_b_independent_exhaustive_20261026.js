/* R166 B exact independent oracle: weighted tickets and exhaustive 2^N child strings.
   Pure JavaScript BigInt, no imports; input is original frozen R166 JSON.
   First execution count failure and correction are documented in protocols/R166_*CORRECTION*.
*/
function audit(original) {
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t}return a||1n};
 const q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return [n/g,d/g]};
 const add=(a,b)=>q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
 const mul=(a,b)=>q(a[0]*b[0],a[1]*b[1]),div=(a,b)=>q(a[0]*b[1],a[1]*b[0]);
 const abs=a=>q(a[0]<0n?-a[0]:a[0],a[1]),eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 const str=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
 const parse=s=>{const x=String(s).split("/");return q(x[0],x[1]||1)};
 const Z=q(0),O=q(1);
 const orig=new Map(original.kernels.map(x=>[x.N+":"+x.regime+":"+x.mechanism,x.rows]));
 if(orig.size!==12)throw Error("wrong frozen kernel count");
 function branches(n,k,regime,mechanism) {
   const pa=q(k,n),pb=q(n-k,n);
   if(regime==="neutral")return pa;
   if(mechanism==="selection"){
     const wa=regime==="toward_A"?2:1,wb=regime==="toward_B"?2:1;
     return q(wa*k,wa*k+wb*(n-k));
   }
   const ba=regime==="toward_A"?q(1,3):Z,ab=regime==="toward_B"?q(1,3):Z;
   return add(mul(pa,sub(O,ab)),mul(pb,ba));
 }
 function enumerate(n,p){
   const row=Array.from({length:n+1},()=>Z);
   for(let mask=0;mask<2**n;mask++){
     let j=0,prob=O;
     for(let b=0;b<n;b++){if(mask&(1<<b)){j++;prob=mul(prob,p)}else prob=mul(prob,sub(O,p))}
     row[j]=add(row[j],prob);
   }
   if(!eq(row.reduce(add,Z),O))throw Error("normalization failure");
   return row;
 }
 function TV(a,b){return div(a.reduce((s,v,i)=>add(s,abs(sub(v,b[i]))),Z),q(2))}
 const all=new Map();let verified=0;
 for(const n of [4,8])for(const regime of ["neutral","toward_A","toward_B"])for(const mechanism of ["selection","transformation"]){
   const key=n+":"+regime+":"+mechanism,rows=[];
   for(let k=0;k<=n;k++){
     const row=enumerate(n,branches(n,k,regime,mechanism));
     const old=orig.get(key)[k].map(parse);
     if(row.some((x,i)=>!eq(x,old[i])))throw Error("frozen kernel mismatch "+key+" k="+k);
     rows.push(row);verified++;
   }
   all.set(key,rows);
 }
 if(verified!==84)throw Error("wrong frozen row count");
 const cases=[];let neutral=0,identical=0,different=0;
 for(const n of [4,8])for(const regime of ["neutral","toward_A","toward_B"])for(let k=0;k<=n;k++){
   const a=all.get(n+":"+regime+":selection")[k],b=all.get(n+":"+regime+":transformation")[k];
   const tv=TV(a,b);
   if(regime==="neutral"){if(!eq(tv,Z))throw Error("neutral control failed");neutral++;continue}
   if(eq(tv,Z))identical++;else different++;
   cases.push({N:n,k,p:str(q(k,n)),regime,TV:str(tv),Bayes_error_equal_prior:str(div(sub(O,tv),q(2))),equal: eq(tv,Z)});
 }
 if(cases.length!==28||neutral!==14||identical!==8||different!==20)throw Error("corrected count assertion failed");
 const mutant_q=q(5,8),mutantTV=TV(enumerate(4,mutant_q),all.get("4:toward_A:selection")[2]);
 if(eq(mutantTV,Z))throw Error("mutation negative control failed");
 const groups=[];
 for(const n of [4,8])for(const regime of ["toward_A","toward_B"]){
   const x=cases.filter(c=>c.N===n&&c.regime===regime).map(c=>parse(c.TV));
   let min=x[0],max=x[0];for(const v of x){if(v[0]*min[1]<min[0]*v[1])min=v;if(v[0]*max[1]>max[0]*v[1])max=v}
   groups.push({N:n,regime,min_TV:str(min),max_TV:str(max)});
 }
 return {id:"R166",date:"2026-10-26",evidence:"E1_INTERNAL",
  method:"independent weighted-ticket and exhaustive offspring enumeration",
  original_kernels_verified:orig.size,original_rows_verified:verified,
  nonneutral_conditions:cases.length,neutral_controls:neutral,
  identical_nonneutral:identical,different_nonneutral:different,
  mutation:{q:"5/8",TV:str(mutantTV),detected:true},groups,cases,
  protocol_amendment:"POSTEXEC_ARITHMETIC_CORRECTION",E2_new:0,E3_new:0,external_replication:false};
}
