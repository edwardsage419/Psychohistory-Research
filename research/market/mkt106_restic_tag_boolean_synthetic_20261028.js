#!/usr/bin/env node
'use strict';
// MKT106: synthetic tag selection and retention policy model, not restic executable verification.
function simulate(){
 let checks=0;function ok(v,m){checks++;if(!v)throw Error(m)}
 const snaps=[{id:"S1",t:1,tags:["foo"]},{id:"S2",t:2,tags:["bar"]},{id:"S3",t:3,tags:["foo","bar"]},{id:"S4",t:4,tags:["foo"]},{id:"S5",t:5,tags:[]}];
 function match(s,list){return list.length===1&&list[0]===""?s.tags.length===0:list.every(t=>s.tags.includes(t))}
 function run(filterLists,keepLast=1,keepTagLists=[]){
   const selected=snaps.filter(s=>filterLists===null||filterLists.some(l=>match(s,l)));
   const sorted=selected.slice().sort((a,b)=>b.t-a.t), kept=new Set(sorted.slice(0,keepLast).map(x=>x.id));
   for(const s of selected)if(keepTagLists.some(l=>match(s,l)))kept.add(s.id);
   return {selected:selected.map(x=>x.id),keep:selected.filter(x=>kept.has(x.id)).map(x=>x.id),remove:selected.filter(x=>!kept.has(x.id)).map(x=>x.id),outside:snaps.filter(x=>!selected.includes(x)).map(x=>x.id)};
 }
 function eq(a,b,m){ok(JSON.stringify(a)===JSON.stringify(b),m)}
 const OR=run([["foo"],["bar"]]),AND=run([["foo","bar"]]),keep=run(null,1,[["foo","bar"]]),untagged=run([[""]]),keepOR=run(null,0,[["foo"],["bar"]]),keepAND=run(null,0,[["foo","bar"]]);
 eq(OR.selected,["S1","S2","S3","S4"],"OR scope");
 eq(OR.keep,["S4"],"OR keep");
 eq(OR.remove,["S1","S2","S3"],"OR remove");
 eq(OR.outside,["S5"],"OR outside");
 eq(AND.selected,["S3"],"AND scope");
 eq(AND.keep,["S3"],"AND keep");
 eq(AND.remove,[],"AND remove");
 eq(AND.outside,["S1","S2","S4","S5"],"AND outside");
 eq(keep.keep,["S3","S5"],"keep-tag AND plus keep-last");
 eq(keep.remove,["S1","S2","S4"],"keep-tag remove");
 eq(untagged.selected,["S5"],"empty tag scope");
 eq(keepOR.keep,["S1","S2","S3","S4"],"repeated keep-tag OR");
 eq(keepAND.keep,["S3"],"comma keep-tag AND");
 eq(keepAND.remove,["S1","S2","S4","S5"],"comma keep-tag removal");
 ok(OR.remove.length>AND.remove.length,"scope safety delta");
 ok(OR.remove.includes("S3")&&!AND.remove.includes("S3"),"both-tag snapshot affected by OR");
 return {checks,failures:0,snapshots:snaps,or:OR,and:AND,keep_tag:keep,untagged,keep_tag_repeated:keepOR,keep_tag_comma:keepAND};
}
console.log(JSON.stringify(simulate(),null,2));
