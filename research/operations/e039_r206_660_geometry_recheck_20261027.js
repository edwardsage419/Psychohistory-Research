// E039. Node.js 18+, standard library only. Run at Psychohistory-Research repository root.
const fs=require("fs");
function auditR206(csv,receiptText){
  function parseCSV(s){let out=[],row=[],v="",q=false;for(let i=0;i<s.length;i++){const c=s[i];if(c==='"'){if(q&&s[i+1]==='"'){v+='"';i++;}else q=!q;}else if(c===','&&!q){row.push(v);v="";}else if((c==='\n'||c==='\r')&&!q){if(c==='\r'&&s[i+1]==='\n')i++;row.push(v);if(row.some(x=>x!==""))out.push(row);row=[];v="";}else v+=c;}if(v||row.length){row.push(v);out.push(row);}const head=out.shift();return out.map(r=>Object.fromEntries(head.map((h,i)=>[h,r[i]])));}
  const gcd=(a,b)=>{a=a<0n?-a:a;while(b){const t=a%b;a=b;b=t;}return a;};
  const raw=(n,d)=>{const g=gcd(n,d);return{n:n/g,d:d/g};};
  const rat=x=>{if(typeof x==="object"&&x.n!==undefined)return x;const a=String(x).split("/");return raw(BigInt(a[0]),BigInt(a[1]||1));};
  const add=(a,b)=>raw(a.n*b.d+b.n*a.d,a.d*b.d),sub=(a,b)=>raw(a.n*b.d-b.n*a.d,a.d*b.d),mul=(a,b)=>raw(a.n*b.n,a.d*b.d),cmp=(a,b)=>a.n*b.d-b.n*a.d,eq=(a,b)=>cmp(a,b)===0n,repr=a=>a.d===1n?String(a.n):`${a.n}/${a.d}`;
  const z=rat(0),one=rat(1),data=parseCSV(csv),receipt=JSON.parse(receiptText),groups=new Map();
  for(const r of data){const key=`${r.a},${r.b},${r.train_independent_samples_n}`;if(!groups.has(key))groups.set(key,[]);const xy=s=>s.split(",").map(rat);groups.get(key).push({p:rat(r.full_original_training_source_probability),c0:xy(r.k2_centroid0),c1:xy(r.k2_centroid1),m:xy(r.k1_centroid),l0:Number(r.trained_cluster0_g_label),l1:Number(r.trained_cluster1_g_label)});}
  const index=new Map(receipt.worlds.map(w=>[`${w.a},${w.b},${w.n}/${w.qG}/${w.qH}`,w]));let checks=0;const fail=[];let betterK2=0,betterG=0,worseG=0,quantShift=0,gShift=0;const scored=new Map();
  const assert=(a,b,label)=>{checks++;if(!eq(a,b))fail.push(`${label}: ${repr(a)} != ${repr(b)}`);};
  for(const [key,rows] of groups){const [a,b,n]=key.split(",").map(Number);let mass=z;for(const r of rows)mass=add(mass,r.p);assert(mass,one,`train mass ${key}`);
    const four=[];for(const g of [-1,1])for(const h of [-1,1]){const x=[rat(a*g),rat(b*h)];let k2=z,k1=z,err=z;for(const r of rows){const dist=c=>add(mul(sub(x[0],c[0]),sub(x[0],c[0])),mul(sub(x[1],c[1]),sub(x[1],c[1])));const d0=dist(r.c0),d1=dist(r.c1),id=cmp(d0,d1)<=0n?0:1;k2=add(k2,mul(r.p,id===0?d0:d1));k1=add(k1,mul(r.p,dist(r.m)));if((id===0?r.l0:r.l1)!==g)err=add(err,r.p);}four.push({g,h,k2,k1,err});}
    for(const gs of ["1/4","1/2","3/4"])for(const hs of ["1/4","1/2","3/4"]){const qg=rat(gs),qh=rat(hs);let k2=z,k1=z,err=z,massFuture=z;for(const e of four){const wg=e.g===1?qg:sub(one,qg),wh=e.h===1?qh:sub(one,qh),w=mul(wg,wh);massFuture=add(massFuture,w);k2=add(k2,mul(w,e.k2));k1=add(k1,mul(w,e.k1));err=add(err,mul(w,e.err));}
      const k=`${key}/${gs}/${hs}`,w=index.get(k);if(!w)throw Error("Missing receipt "+k);
      assert(k2,rat(w.k2_quantization_exact),k+" k2");assert(k1,rat(w.k1_quantization_exact),k+" k1");assert(err,rat(w.g_classification_exact),k+" G");assert(sub(one,qg),rat(w.constant_plus_baseline_exact),k+" baseline");assert(z,rat(w.target_sign_oracle_exact),k+" oracle");assert(massFuture,one,k+" future mass");
      scored.set(k,{k2,err});if(cmp(k2,k1)<0n)betterK2++;if(cmp(err,sub(one,qg))<0n)betterG++;else if(cmp(err,sub(one,qg))>0n)worseG++;
    }
  }
  for(const [k,v] of scored){const [key]=k.split("/");const b=scored.get(key+"/1/2/1/2");if(!eq(v.k2,b.k2))quantShift++;if(!eq(v.err,b.err))gShift++;}
  if(checks!==660||data.length!==1920||receipt.worlds.length!==108||fail.length)throw Error(JSON.stringify({checks,rows:data.length,worlds:receipt.worlds.length,fail:fail.slice(0,5)}));
  return{checks,failures:fail.length,training_rows:data.length,training_worlds:groups.size,receipt_worlds:receipt.worlds.length,betterK2,betterG,worseG,quantShift,gShift,scope:"independent exact geometry from archived training CSV"};
}
const result=auditR206(fs.readFileSync("research/R206/R206_ALL_1920_ORIGINAL_KMEANS_TRAINING_HISTORIES.csv","utf8"),fs.readFileSync("research/validation/R206_FUTURE_PRIOR_SHIFT_108_EXACT_RECEIPT_2026-10-27.json","utf8"));console.log(JSON.stringify(result));
