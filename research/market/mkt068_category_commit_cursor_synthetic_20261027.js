"use strict";
// Synthetic interleaving model. Does not connect to PostgreSQL or Message DB.
const checks=[];function ck(ok,label){if(!ok)throw Error(label);checks.push(label)}
function store(){return {seq:0,events:[],locks:new Set()}}
function begin(s,tx,category){if(s.locks.has(category))return null;s.locks.add(category);const e={seq:++s.seq,tx,category,status:"pending"};s.events.push(e);return e}
function settle(s,e,status){e.status=status;s.locks.delete(e.category)}
function visible(s,category,from=1){return s.events.filter(e=>e.status==="committed"&&(category===null||e.category===category)&&e.seq>=from).map(e=>e.seq).sort((a,b)=>a-b)}
function read(s,category,from){const batch=visible(s,category,from);return {batch,next:batch.length?batch[batch.length-1]+1:from}}
function safeMark(s){const pending=s.events.filter(e=>e.status==="pending").map(e=>e.seq);return pending.length?Math.min(...pending)-1:s.seq}
function run(){
 const s=store();ck(visible(s,null).length===0,"empty");
 const a=begin(s,"A","alpha");ck(a.seq===1,"alpha reserves first");
 ck(begin(s,"B","alpha")===null,"same category blocked");
 const c=begin(s,"C","beta");ck(c.seq===2,"other category reserves");
 settle(s,c,"committed");ck(visible(s,null).join(",")==="2","other category visible first");
 const cross=read(s,null,1);ck(cross.next===3,"custom global cursor advances");
 ck(safeMark(s)===0,"global safe watermark holds");
 ck(visible(s,"alpha").length===0,"pending alpha invisible");
 ck(read(s,"beta",1).batch.join(",")==="2","category beta sees its event");
 settle(s,a,"committed");ck(read(s,null,cross.next).batch.length===0,"custom global cursor misses late alpha");
 ck(read(s,"alpha",1).batch.join(",")==="1","category alpha sees late alpha");
 ck(safeMark(s)===2,"global watermark after commit");
 const b=begin(s,"B","alpha");ck(b.seq===3,"same category resumes");
 settle(s,b,"committed");ck(visible(s,"alpha").join(",")==="1,3","category positions may skip");
 ck(read(s,"alpha",2).batch.join(",")==="3","category cursor skips unrelated positions");
 const t=store(),x=begin(t,"X","alpha"),y=begin(t,"Y","beta");settle(t,x,"aborted");settle(t,y,"committed");
 ck(visible(t,null).join(",")==="2","aborted gap exists");
 ck(safeMark(t)===2,"aborted gap can be passed");
 ck(visible(t,"alpha").length===0,"aborted event invisible");
 ck(visible(t,"beta").join(",")==="2","committed other category visible");
 const u=store(),v=begin(u,"V","alpha");settle(u,v,"committed");
 ck(read(u,"alpha",1).next===2,"single category cursor");
 return {checks:checks.length,all_passed:true,global_custom_cursor_loses_late_commit:true,per_category_reader_recovers:true};
}
console.log(JSON.stringify(run()));
