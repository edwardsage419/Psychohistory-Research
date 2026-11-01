'use strict';
// MKT187 artificial decision-review selection test; no product API.
function run(){
 let n=0;const a=(v,s)=>{if(!v)throw Error(s);n++};
 const rows=[1,1,0,0].map((y,i)=>({id:i,p:80,y,reviewed:i<2,prescore:true}));
 const visible=rows.map(r=>({...r,y:r.reviewed?r.y:null}));
 const loss=r=>{if(r.y===null)throw Error('missing');return (r.p-100*r.y)**2/100};
 const known=visible.filter(r=>r.reviewed),missing=visible.filter(r=>r.y===null);
 const knownSum=known.reduce((s,r)=>s+loss(r),0);
 const reviewed=knownSum/known.length/100;
 const full=rows.reduce((s,r)=>s+loss(r),0)/rows.length/100;
 const lower=(knownSum+missing.length*4)/rows.length/100;
 const upper=(knownSum+missing.length*64)/rows.length/100;
 a(rows.length===4,'due');a(known.length===2,'reviewed');a(missing.length===2,'missing');
 a(reviewed===0.04,'reviewed brier');a(full===0.34,'oracle brier');
 a(lower===0.04,'lower');a(upper===0.34,'upper');a(full>reviewed,'selection');
 let rejected=false;try{loss(missing[0])}catch(e){rejected=true}a(rejected,'missing guard');
 a(rows.every(r=>r.prescore),'prescore');a(known.length/rows.length===0.5,'coverage');
 return {tests:n,pass:true,coverage:0.5,reviewed_brier:reviewed,oracle_brier:full,bounds:[lower,upper],scope:'ARTIFICIAL_NONBLIND_MARKET_E1'};
}
module.exports={run};
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
