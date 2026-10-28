'use strict';
// MKT107: artificial snapshot logic only; does not run restic or delete files.
const snapshots=[
{id:'A1',host:'A',path:'/notes',tags:['alpha'],t:1},
{id:'A2',host:'A',path:'/notes',tags:['alpha'],t:2},
{id:'B1',host:'B',path:'/notes',tags:['beta'],t:1},
{id:'B2',host:'B',path:'/notes',tags:['beta'],t:2},
{id:'B3',host:'B',path:'/notes',tags:['gamma'],t:3}
];
function simulate({group=['host','path'],filterTag=null,keepTag='alpha',last=0,unsafe=false}={}) {
  const selected=snapshots.filter(x=>!filterTag||x.tags.includes(filterTag));
  const groups=new Map();
  for(const x of selected) {
    const key=group.map(k=>k==='tags'?x.tags.join(','):x[k]).join('|');
    if(!groups.has(key))groups.set(key,[]);
    groups.get(key).push(x);
  }
  const keep=[],candidateRemove=[],errors=[];
  for(const [key,arr] of groups) {
    const sorted=arr.slice().sort((a,b)=>b.t-a.t);
    const retained=arr.filter(x=>x.tags.includes(keepTag)||sorted.slice(0,last).includes(x));
    if(retained.length===0&&keepTag)errors.push(key);
    keep.push(...retained.map(x=>x.id));
    candidateRemove.push(...arr.filter(x=>!retained.includes(x)).map(x=>x.id));
  }
  return {keep:keep.sort(),candidateRemove:candidateRemove.sort(),errors,unsafe};
}
const cases=[
{name:'default_keep_tag_only',args:{},error:true},
{name:'default_keep_tag_plus_last',args:{last:1},remove:['B1','B2']},
{name:'no_grouping_keep_tag_only',args:{group:[]},remove:['B1','B2','B3']},
{name:'filter_tag_alpha',args:{filterTag:'alpha'},remove:[]},
{name:'unsafe_with_nonempty_policy',args:{unsafe:true},error:true},
{name:'group_by_tags',args:{group:['host','path','tags']},error:true}
];
let checks=0;
for(const c of cases) {
  const out=simulate(c.args);
  if(c.error) {checks++;if(out.errors.length===0)throw Error(c.name+' expected abort');}
  if(c.remove) {checks++;if(JSON.stringify(out.candidateRemove)!==JSON.stringify(c.remove))throw Error(c.name+' wrong candidates');}
  console.log(JSON.stringify({scenario:c.name,...out}));
}
console.log(JSON.stringify({study:'MKT107',synthetic_checks:checks,failures:0,real_restic_execution:false}));
