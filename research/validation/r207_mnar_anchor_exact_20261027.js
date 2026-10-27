"use strict";
// R207 E1 MNAR anchor-mask study. Exact enumeration; node r207_mnar_anchor_exact_20261027.js > receipt.json
function run(){
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a||1n;};
 const f=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g];};
 const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
 const neg=a=>[-a[0],a[1]],sub=(a,b)=>add(a,neg(b));
 const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
 const div=(a,b)=>f(a[0]*b[1],a[1]*b[0]);
 const sq=a=>mul(a,a),s=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
 const Z=f(0),one=f(1),sources=[];
 for(let z=0;z<64;z++){let x=Array.from({length:6},(_,i)=>1n+BigInt((z>>i)&1));sources.push(Array.from({length:9},(_,j)=>x[Math.floor(j/3)]*x[3+j%3]));}
 const masks=[];for(let b=0;b<512;b++){let ids=Array.from({length:9},(_,i)=>i).filter(i=>(b&(1<<i))!==0);if(ids.length===5)masks.push(ids);}
 const connected=mask=>{let graph=Array.from({length:6},()=>[]);for(let j of mask){let a=Math.floor(j/3),b=3+j%3;graph[a].push(b);graph[b].push(a);}let seen=new Set([0]),todo=[0];while(todo.length){let x=todo.pop();for(let y of graph[x])if(!seen.has(y)){seen.add(y);todo.push(y);}}return seen.size===6;};
 const q=v=>v===1n?f(1,4):v===2n?f(1,2):f(3,4);
 const names=["correct","ignore","visible","zero","excess"],worlds=[],groups={};
 const total=Object.fromEntries(["mass",...names].map(k=>[k,Z]));
 let positive=0,observed_anchor_excess=Z;
 for(const mask of masks){
   const anchor=mask.includes(8),hid=Array.from({length:9},(_,i)=>i).filter(i=>!mask.includes(i)),isconn=connected(mask);
   const p=sources.map(M=>div(anchor?q(M[8]):sub(one,q(M[8])),f(64*(anchor?70:56))));
   const sigs=new Map();
   for(let i=0;i<64;i++){let key=mask.map(j=>String(sources[i][j])).join(",");if(!sigs.has(key))sigs.set(key,[]);sigs.get(key).push(i);}
   const predictions=new Map();
   for(const [key,idx] of sigs){
     let w=idx.reduce((v,i)=>add(v,p[i]),Z);
     let correct=hid.map(j=>div(idx.reduce((v,i)=>add(v,mul(p[i],f(sources[i][j]))),Z),w));
     let ignore=hid.map(j=>div(idx.reduce((v,i)=>add(v,f(sources[i][j])),Z),f(idx.length)));
     let visible=div(mask.reduce((v,j)=>add(v,f(sources[idx[0]][j])),Z),f(5));
     predictions.set(key,{correct,ignore,visible:hid.map(()=>visible),zero:hid.map(()=>Z)});
   }
   let risk=Object.fromEntries(names.map(k=>[k,Z]));
   for(let i=0;i<64;i++){
     let key=mask.map(j=>String(sources[i][j])).join(","),pred=predictions.get(key);
     for(const name of ["correct","ignore","visible","zero"]){
       let loss=hid.reduce((v,j,k)=>add(v,sq(sub(f(sources[i][j]),pred[name][k]))),Z);
       risk[name]=add(risk[name],mul(p[i],div(loss,f(4))));
     }
     let excess=hid.reduce((v,j,k)=>add(v,sq(sub(pred.ignore[k],pred.correct[k]))),Z);
     risk.excess=add(risk.excess,mul(p[i],div(excess,f(4))));
   }
   const mass=p.reduce(add,Z);
   if(s(risk.excess)!=="0")positive++;
   if(anchor)observed_anchor_excess=add(observed_anchor_excess,risk.excess);
   const g=(isconn?"connected":"disconnected")+"/"+(anchor?"anchor_observed":"anchor_hidden");
   if(!groups[g])groups[g]=Object.fromEntries(["masks","mass",...names].map(k=>[k,k==="masks"?0:Z]));
   groups[g].masks++;groups[g].mass=add(groups[g].mass,mass);
   for(const k of names){groups[g][k]=add(groups[g][k],risk[k]);total[k]=add(total[k],risk[k]);}
   total.mass=add(total.mass,mass);
   worlds.push({mask:mask.map(j=>""+Math.floor(j/3)+(j%3)).join("|"),connected:isconn,anchor_observed:anchor,source_count:64,observed_signatures:sigs.size,mass:s(mass),...Object.fromEntries(names.map(k=>[k+"_weighted_mse",s(risk[k])]))});
 }
 if(s(total.mass)!=="1"||s(sub(total.ignore,add(total.correct,total.excess)))!=="0"||s(observed_anchor_excess)!=="0")throw Error("R exact identity failed");
 const grp=Object.fromEntries(Object.entries(groups).map(([key,g])=>[key,{masks:g.masks,mass:s(g.mass),...Object.fromEntries(names.flatMap(k=>[[k+"_weighted_mse",s(g[k])],[k+"_conditional_mse",s(div(g[k],g.mass))]]))}]));
 return {research_id:"R207",status:"E1_ARTIFICIAL_THIRD_METHOD_EXACT",protocol:"protocols/R207_MNAR_ANCHOR_MASK_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md",source_factor_paths:64,masks:126,source_mask_pairs:8064,heldout_entries:32256,selection:"P(anchor_observed|M22=1,2,4)=(1/4,1/2,3/4); conditional uniform masks 70 or 56",totals:Object.fromEntries(Object.entries(total).map(([k,v])=>[k,s(v)])),groups:grp,positive_excess_masks:positive,anchor_observed_excess:s(observed_anchor_excess),all_exact_excess_identity:true,worlds};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));