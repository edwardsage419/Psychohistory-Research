// E081 independent BigInt rational audit of published R251 S47 receipt.
// Usage: node e081_r251_s47_exact_receipt_20261029.js receipt.json
const fs=require('fs');
const names=['HALF_CONTRACTION','NEGATIVE_HALF_CONTRACTION','ZERO_MAP','DOUBLE_EXPANSION','IDENTITY_NEUTRAL','SIGN_FLIP_NEUTRAL','CUBIC_LOCAL_INWARD','CUBIC_OUTWARD','LOGISTIC_R3_CENTERED'];
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a}
function q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]}
const neg=x=>[-x[0],x[1]],add=(x,y)=>q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]),sub=(x,y)=>add(x,neg(y)),mul=(x,y)=>q(x[0]*y[0],x[1]*y[1]),sq=x=>mul(x,x),abs=x=>[x[0]<0n?-x[0]:x[0],x[1]],cmp=(x,y)=>Math.sign(Number(x[0]*y[1]-y[0]*x[1]>0n)-Number(x[0]*y[1]-y[0]*x[1]<0n)),sign=x=>x[0]<0n?'-':x[0]>0n?'+':'0',str=x=>x[1]===1n?String(x[0]):String(x[0])+'/'+String(x[1]);
function step(i,x){switch(i){case 0:return mul(x,q(1,2));case 1:return neg(mul(x,q(1,2)));case 2:return q(0);case 3:return mul(x,q(2));case 4:return x;case 5:return neg(x);case 6:return sub(x,mul(sq(x),x));case 7:return add(x,mul(sq(x),x));case 8:return sub(neg(x),mul(q(3),sq(x)))}}
function compute(){let initials=[q(-1,2),q(-1,4),q(-1,12),q(-1,24),q(0),q(1,24),q(1,12),q(1,4),q(1,2)];let worlds=[];
for(let i=0;i<9;i++){let counts={negative:0,zero:0,positive:0},net={shrink:0,equal:0,grow:0},local={count:0,strict4:0,net4_shrink:0},cohorts=[],strict=0;
for(let x0 of initials){let t=[x0];for(let j=0;j<5;j++)t.push(step(i,t.at(-1)));let s=[];for(let j=0;j<5;j++){let z=sign(sub(sq(t[j+1]),sq(t[j])));s.push(z);counts[z==='-'?'negative':z==='+'?'positive':'zero']++}
if(x0[0]===0n)continue;let s4=s.slice(0,4).join(''),pass=s4==='----';strict+=Number(pass);let c=cmp(abs(t[4]),abs(x0)),cls=c<0?'shrink':c>0?'grow':'equal';net[cls]++;
if(cmp(abs(x0),q(1,12))<=0){local.count++;local.strict4+=Number(pass);local.net4_shrink+=Number(cls==='shrink')}
cohorts.push({x0:str(x0),delta_signs_t0_t3:s4,strict4:pass,net4:cls})}
worlds.push({world:names[i],source_rows:45,delta_sign_counts:counts,strict4_cohorts:strict,net4_cohorts:net,local,cohorts})}
return {research_id:'R251_S47',source_rows:405,independent_cohorts:72,worlds}}
function verify(r){let a=compute(),checks=0;function ck(x,y){checks++;if(JSON.stringify(x)!==JSON.stringify(y))throw Error('mismatch at check '+checks)}
for(let k of ['research_id','source_rows','independent_cohorts'])ck(a[k],r[k]);ck(a.worlds.length,r.worlds.length);
for(let i=0;i<9;i++){let x=a.worlds[i],y=r.worlds[i];for(let k of ['world','source_rows','strict4_cohorts'])ck(x[k],y[k]);for(let k of ['negative','zero','positive'])ck(x.delta_sign_counts[k],y.delta_sign_counts[k]);for(let k of ['shrink','equal','grow'])ck(x.net4_cohorts[k],y.net4_cohorts[k]);for(let k of ['count','strict4','net4_shrink'])ck(x.local[k],y.local[k]);ck(x.cohorts.length,y.cohorts.length);for(let j=0;j<8;j++)for(let k of ['x0','delta_signs_t0_t3','strict4','net4'])ck(x.cohorts[j][k],y.cohorts[j][k])}
return checks}
function main(r){let checks=verify(r),mutant=JSON.parse(JSON.stringify(r));mutant.worlds[0].cohorts[0].net4='grow';let rejected=false;try{verify(mutant)}catch(e){rejected=true}if(!rejected)throw Error('mutation accepted');return {status:'PASS',checks:checks+1,failures:0,source_atoms:405,cohorts:72,worlds:9,mutation_rejected:true}}
if(require.main===module)console.log(JSON.stringify(main(JSON.parse(fs.readFileSync(process.argv[2],'utf8')))));
module.exports={main,compute,verify};
