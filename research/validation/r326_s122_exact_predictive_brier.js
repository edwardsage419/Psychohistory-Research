'use strict';
// R326 S122 exact E1. Frozen at f2e4798f. No external packages.
function gcd(a,b){while(b){let t=a%b;a=b;b=t;}return a<0n?-a:a;}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error('zero');if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]),mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),div=(a,b)=>F(a[0]*b[1],a[1]*b[0]),eq=(a,b)=>a[0]===b[0]&&a[1]===b[1],fmt=a=>a[1]===1n?String(a[0]):String(a[0])+'/'+String(a[1]);
const Z=F(0),O=F(1),H=F(1,2),T=[F(1,4),F(3,4)];
function like(t,b){let w=O;for(let x of b)w=mul(w,x?T[t]:sub(O,T[t]));return w;}
function joint(law,h,g,y){let total=Z,blocks=[h.slice(0,2),h.slice(2,4),h.slice(4,6)];
 for(let z=0;z<(law==='H'?2:1);z++)for(let bits=0;bits<8;bits++){
  let w=law==='H'?H:O;
  for(let j=0;j<3;j++){
   let t=(bits>>j)&1,prior=law==='H'?(t?(z?T[1]:T[0]):(z?T[0]:T[1])):H;
   w=mul(w,mul(prior,like(t,blocks[j])));
   if(j===g)w=mul(w,y?T[t]:sub(O,T[t]));
  }total=add(total,w);
 }return total;
}
const names=['law','history_id','h11','h12','h21','h22','h31','h32','target_group','next_y','joint_mass','hier_prediction','independent_prediction','constant_prediction','hier_squared_loss','independent_squared_loss','constant_squared_loss','hier_weighted_brier','independent_weighted_brier','constant_weighted_brier'];
const rows=[],losses={H:[Z,Z,Z],I:[Z,Z,Z]},checks={atom_count:0,group_masses:true,complement_symmetry:true,original_csv_match:false,wrong_uniform_history_weight_detected:false},preds=new Map(),histories=Array.from({length:64},(_,n)=>Array.from({length:6},(_,k)=>(n>>(5-k))&1));
for(let id=0;id<64;id++)for(let g=0;g<3;g++){
 let h=histories[id],h0=joint('H',h,g,0),h1=joint('H',h,g,1),i0=joint('I',h,g,0),i1=joint('I',h,g,1),ps=[div(h1,add(h0,h1)),div(i1,add(i0,i1)),H];preds.set(id+':'+g,ps);
 for(let law of ['H','I'])for(let y of [0,1]){
  let w=law==='H'?(y?h1:h0):(y?i1:i0),errs=ps.map(p=>mul(sub(p,F(y)),sub(p,F(y)))),weighted=errs.map(e=>mul(w,e));
  weighted.forEach((v,k)=>losses[law][k]=add(losses[law][k],div(v,F(3))));
  rows.push([law,id,...h,g+1,y,fmt(w),...ps.map(fmt),...errs.map(fmt),...weighted.map(fmt)].join(','));checks.atom_count++;
 }
}
function parse(s){let p=s.split('/');return F(BigInt(p[0]),p[1]===undefined?1n:BigInt(p[1]));}
for(let law of ['H','I'])for(let g=1;g<=3;g++){let mass=Z;for(let r of rows){let a=r.split(',');if(a[0]===law&&Number(a[8])===g)mass=add(mass,parse(a[10]));}if(!eq(mass,O))checks.group_masses=false;}
for(let law of ['H','I'])for(let id=0;id<64;id++)for(let g=0;g<3;g++)for(let y=0;y<=1;y++){let comp=histories[id].map(x=>1-x);if(!eq(joint(law,histories[id],g,y),joint(law,comp,g,1-y)))checks.complement_symmetry=false;}
const csv=names.join(',')+'\n'+rows.join('\n')+'\n';
function validateOriginal(text){let lines=text.trim().split(/\r?\n/);if(lines.length!==65)throw Error('parent row count');let keys=lines[0].split(','),at=x=>keys.indexOf(x),seen=new Set();
 for(let line of lines.slice(1)){let x=line.split(','),id=Number(x[at('history_id')]);if(seen.has(id))throw Error('duplicate');seen.add(id);
  for(let j=0;j<6;j++)if(Number(x[1+j])!==histories[id][j])throw Error('parent history');
  for(let g=0;g<3;g++){let ps=preds.get(id+':'+g);if(!eq(ps[0],parse(x[at('hier_predict_g'+(g+1))]))||!eq(ps[1],parse(x[at('independent_predict_g'+(g+1))])))throw Error('parent predictions');}
 }checks.original_csv_match=true;
}
let uniform=Z;for(let id=0;id<64;id++)for(let g=0;g<3;g++){let h=histories[id],p=preds.get(id+':'+g)[0],m0=joint('H',h,g,0),m1=joint('H',h,g,1),q=div(m1,add(m0,m1));uniform=add(uniform,div(add(mul(sub(O,q),mul(p,p)),mul(q,mul(sub(O,p),sub(O,p)))),F(192)));}
checks.wrong_uniform_history_weight_detected=!eq(uniform,losses.H[0]);
const summary={schema:'r326_s122_exact_predictive_brier_v1',protocol_commit:'f2e4798fc97697c642cc1fa20fd70cdd987b1c50',original_model:'R326 original 2026-10-24 fixed E1',artificial_only:true,law_definitions:{H:'shared Z with frozen R326 hierarchy',I:'independent group theta high probability 1/2'},atoms:rows.length,losses:Object.fromEntries(['H','I'].map(l=>[l,Object.fromEntries(['hierarchical','independent','constant'].map((k,i)=>[k,fmt(losses[l][i])]))])),contrasts:{H_independent_minus_hierarchical:fmt(sub(losses.H[1],losses.H[0])),I_hierarchical_minus_independent:fmt(sub(losses.I[0],losses.I[1])),H_constant_minus_hierarchical:fmt(sub(losses.H[2],losses.H[0])),I_constant_minus_independent:fmt(sub(losses.I[2],losses.I[1]))},checks,scope:'E1_ONLY_NO_HUMAN_E2_NO_HISTORICAL_E3'};
if(rows.length!==768||!checks.group_masses||!checks.complement_symmetry||!checks.wrong_uniform_history_weight_detected||sub(losses.H[1],losses.H[0])[0]<=0n||sub(losses.I[0],losses.I[1])[0]<=0n)throw Error('E1 gate failed');
module.exports={csv,summary,validateOriginal};
if(typeof require!=='undefined'&&require.main===module){
 const fs=require('fs'),path=require('path'),dir=__dirname;
 validateOriginal(fs.readFileSync(path.join(dir,'../R326/R326_ALL_64_ARTIFICIAL_GROUP_HISTORIES.csv'),'utf8'));
 if(process.argv.includes('--audit')){
  if(fs.readFileSync(path.join(dir,'R326_S122_ALL_768_PREDICTIVE_ATOMS.csv'),'utf8')!==csv)throw Error('CSV mismatch');
  if(fs.readFileSync(path.join(dir,'R326_S122_EXACT_BRIER_RESULTS.json'),'utf8')!==JSON.stringify(summary,null,2)+'\n')throw Error('JSON mismatch');
  console.log('PASS_NATIVE_NODE_S122_768_E1');
 }else if(process.argv.includes('--emit'))process.stdout.write(csv);
 else console.log(JSON.stringify(summary,null,2));
}
