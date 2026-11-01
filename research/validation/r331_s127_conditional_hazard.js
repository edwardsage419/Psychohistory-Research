// R331 S127 exact conditional retention and survivor composition. E1 constructed.
const R=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let x=a<0n?-a:a,y=b;while(y){[x,y]=[y,x%y]}return [a/x,b/x]};
const add=(a,b)=>R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>R(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>R(a[0]*b[1],a[1]*b[0]);
const sub=(a,b)=>R(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const less=(a,b)=>a[0]*b[1]<b[0]*a[1];
const fmt=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1];
const pairs=[[R(1,4),R(1,2)],[R(1,4),R(3,4)],[R(1,2),R(3,4)]];
const weights=[R(1,4),R(1,2),R(3,4)],ONE=R(1);
const pow=(x,t)=>R(x[0]**BigInt(t),x[1]**BigInt(t));
function generate(){
 const rows=[],groups=[];let idx=0;
 for(const [a,b] of pairs)for(const w of weights){
  idx++;const world_id="W"+String(idx).padStart(2,"0"),ow=sub(ONE,w);
  const S=t=>add(mul(w,pow(a,t)),mul(ow,pow(b,t)));
  const H0=sub(ONE,add(mul(w,a),mul(ow,b)));
  let previous=null,prevShare=null,monotone=true,fastMonotone=true;
  for(let t=0;t<8;t++){
   const s=S(t),s1=S(t+1),retention=div(s1,s),hazard=sub(ONE,retention),fast_share=div(mul(w,pow(a,t)),s);
   if(previous!==null){monotone=monotone&&less(hazard,previous);fastMonotone=fastMonotone&&less(fast_share,prevShare)}
   rows.push({world_id,a:fmt(a),b:fmt(b),w:fmt(w),t,
    s_t:fmt(s),s_t1:fmt(s1),retention:fmt(retention),hazard:fmt(hazard),
    fast_share:fmt(fast_share),homogeneous_hazard:fmt(H0)});
   previous=hazard;prevShare=fast_share;
  }
  groups.push({world_id,a:fmt(a),b:fmt(b),w:fmt(w),h0:fmt(H0),
   h7:fmt(previous),hazard_strictly_decreasing:monotone,fast_share_strictly_decreasing:fastMonotone});
 }
 return {model:"R331_S127_CONSTRUCTED_CONDITIONAL_HAZARD_E1",evidence:"E1_CONSTRUCTED_ONLY",world_count:9,row_count:72,groups,rows};
}
function sorted(x){if(Array.isArray(x))return x.map(sorted);if(x&&typeof x==="object")return Object.fromEntries(Object.keys(x).sort().map(k=>[k,sorted(x[k])]));return x}
function serialized(){return JSON.stringify(sorted(generate()))+"\n"}
if(typeof module!=="undefined"&&module.exports)module.exports={generate,serialized};
if(typeof require!=="undefined"&&require.main===module){const fs=require("fs");const out=process.argv[2];if(out)fs.writeFileSync(out,serialized());else process.stdout.write(serialized())}
