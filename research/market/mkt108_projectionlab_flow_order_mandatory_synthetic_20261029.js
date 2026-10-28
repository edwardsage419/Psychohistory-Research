"use strict";
// Artificial cash-flow priority model based only on published product semantics.
// It is not ProjectionLab's implementation and does not simulate taxes.
function allocate(surplus,flows,otherAssets=0){
 if(!Number.isInteger(surplus)||surplus<0||!Number.isInteger(otherAssets)||otherAssets<0)throw Error("nonnegative integer amounts required");
 let remaining=surplus,draw=0;const allocated={};
 const ordered=[...flows.filter(x=>x.mandatory),...flows.filter(x=>!x.mandatory)];
 for(const f of ordered){
   let wanted=f.mode==="max"?f.cap:f.mode==="pct"?Math.floor(remaining*f.pct/100):f.amount;
   if(!Number.isInteger(wanted)||wanted<0)throw Error("invalid flow");
   const fromIncome=Math.min(wanted,remaining);remaining-=fromIncome;
   let extra=0;if(f.mandatory&&wanted>fromIncome){extra=Math.min(wanted-fromIncome,otherAssets);otherAssets-=extra;draw+=extra;}
   allocated[f.name]=fromIncome+extra;
 }
 return {allocated,remaining,draw,otherAssets,initialSurplus:surplus};
}
function test(){
 let checks=0;const ok=(x,m)=>{checks++;if(!x)throw Error("TEST FAIL: "+m);};
 const A={name:"emergency",mode:"max",cap:700},B={name:"retirement",mode:"pct",pct:50},C={name:"debt",mode:"fixed",amount:300};
 const ab=allocate(1000,[A,B,C]),cb=allocate(1000,[C,B,A]);
 for(const [r,exp] of [[ab,{emergency:700,retirement:150,debt:150,remaining:0}],[cb,{debt:300,retirement:350,emergency:350,remaining:0}]]){
   for(const [k,v] of Object.entries(exp))ok((k==="remaining"?r.remaining:r.allocated[k])===v,k+" expected "+v);
   ok(Object.values(r.allocated).reduce((a,b)=>a+b,0)+r.remaining===r.initialSurplus,"budget conservation");
   ok(r.draw===0,"no drawdown for nonmandatory");
 }
 ok(ab.allocated.emergency!==cb.allocated.emergency,"order changes emergency funding");
 ok(ab.allocated.retirement!==cb.allocated.retirement,"order changes percentage base");
 const mandatory=allocate(200,[{name:"mandatory401k",mode:"fixed",amount:300,mandatory:true}],500);
 ok(mandatory.allocated.mandatory401k===300,"mandatory fully funded");
 ok(mandatory.draw===100,"mandatory draws other assets");
 ok(mandatory.otherAssets===400,"asset remainder");
 ok(mandatory.remaining===0,"surplus exhausted");
 const limited=allocate(200,[{name:"mandatory401k",mode:"fixed",amount:300,mandatory:true}],50);
 ok(limited.allocated.mandatory401k===250,"insufficient reserve disclosed");
 ok(limited.draw===50,"limited draw");
 ok(limited.otherAssets===0,"reserve exhausted");
 let rejected=false;try{allocate(-1,[A])}catch(e){rejected=true}ok(rejected,"negative budget rejected");
 return {checks,failures:0,example_ABC:ab,example_CBA:cb,mandatory_example:mandatory,insufficient_reserve:limited};
}
if(typeof module!=="undefined"&&typeof require==="function"&&require.main===module)console.log(JSON.stringify(test(),null,2));
if(typeof module!=="undefined")module.exports={allocate,test};
