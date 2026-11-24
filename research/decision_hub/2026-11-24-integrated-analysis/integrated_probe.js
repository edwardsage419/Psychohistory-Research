/* Integrated research fixture, Node.js >=18. Manual confirmed semantic IR, NOT a language parser, RAG benchmark, native engine or production implementation. */
function experiment(){
 const registry={
  "c028_interval_feasibility@1.0.0":{path:"research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md",blob:"7cb8d5e3631dd17c0650cec06139d88b5bfcc700",deps:[]},
  "pareto@1.0.0":{path:"research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md",blob:"0d04c633a26437ad6017946cd528c4dc68db3d83",deps:["c028_interval_feasibility@1.0.0"]},
  "C029@1.0.0":{path:"research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md",blob:"a2588cfdd47e547a46a7ee8cde2644caf81198d9",deps:["c028_interval_feasibility@1.0.0"]}
 };
 const G="c028_interval_feasibility@1.0.0",P="pareto@1.0.0",R="C029@1.0.0";
 const option=(id,score,metrics={},extra={})=>({id,score,metrics,...extra});
 const q=(id,values)=>({id,values});
 const cap=(id,metric,op,limit,unit)=>({id,metric,op,limit,unit});
 const measurement=(value,unit)=>({value,unit});
 const base={confirmed:true,revision:1,epoch:1,criterion:"pareto",requests:[P],questions:[],constraints:[],explicitEmpty:true,coverage:true,authorized:true};
 const cases=[
 {id:"housing_monthly",text:"房租每月最多3000元，A每月2500元，B每月3500元，选便宜的。",...base,constraints:[cap("rent","cost","<=",3000,"yuan/month")],options:[option("A",[-2500],{cost:measurement(2500,"yuan/month")}),option("B",[-3500],{cost:measurement(3500,"yuan/month")})],expect:{status:"RESOLVED",leaders:["A"],reject:["B"],ask:null}},
 {id:"learning_strict",text:"培训费用之前最多4000，现在必须低于3000。A 3000元，B 2900元。",...base,revision:2,constraints:[cap("fee-new","cost","<",3000,"yuan")],options:[option("A",[9],{cost:measurement(3000,"yuan")}),option("B",[7],{cost:measurement(2900,"yuan")})],expect:{status:"RESOLVED",leaders:["B"],reject:["A"],ask:null}},
 {id:"career_exception",text:"A薪资高但需搬家，每周到岗不超过两天而且家人同意才可以，B不用搬家。",...base,constraints:[{id:"move",condition:["or",["not","move"],["and","onsite_ok","family_ok"]]}],questions:[q("family",[false,true])],options:[option("A",[14],{}, {atoms:{move:true,onsite_ok:true,family_ok:"$family"}}),option("B",[10],{}, {atoms:{move:false}})],expect:{status:"ASK",leaders:[],reject:[],ask:"family"}},
 {id:"career_no_question",text:"A需搬家，但每周要到岗五天，家人是否同意未知；只有不超过两天且家人同意才可搬。",...base,constraints:[{id:"move",condition:["or",["not","move"],["and","onsite_ok","family_ok"]]}],questions:[q("family",[false,true])],options:[option("A",[14],{}, {atoms:{move:true,onsite_ok:false,family_ok:"$family"}}),option("B",[10],{}, {atoms:{move:false}})],expect:{status:"RESOLVED",leaders:["B"],reject:["A"],ask:null}},
 {id:"time_tradeoff",text:"A收入更高，B有更多自由时间，两者底线都满足。",...base,options:[option("A",[14,2]),option("B",[10,5])],expect:{status:"RESOLVED",leaders:["A","B"],reject:[],ask:null}},
 {id:"uncertain_scenarios",text:"两种方案在两个情景的效用已确认，A为0和4，B为1和1。我想减少最大错失收益。",...base,criterion:"regret",requests:[R],options:[option("A",[],{},{utilities:[0,4]}),option("B",[],{},{utilities:[1,1]})],expect:{status:"RESOLVED",leaders:["A"],reject:[],ask:null}},
 {id:"shared_budget",text:"两个培训要同时参加，共用一笔预算。",...base,requests:["C035@1.0.0"],coverage:false,options:[option("A",[2]),option("B",[3])],expect:{status:"BLOCKED",leaders:[],reject:[],ask:null}},
 {id:"unit_mismatch",text:"每月支出最多3000，A给的是年度支出，B每月2500。",...base,constraints:[cap("rent","cost","<=",3000,"yuan/month")],options:[option("A",[9],{cost:measurement(12000,"yuan/year")}),option("B",[8],{cost:measurement(2500,"yuan/month")})],expect:{status:"UNRESOLVED",leaders:[],reject:[],ask:null}},
 {id:"pending_semantics",text:"我还没确定每月预算，也没确认比较范围。",...base,confirmed:false,options:[option("A",[1]),option("B",[2])],expect:{status:"CLARIFY",leaders:[],reject:[],ask:null}},
 {id:"known_unavailable",text:"A培训报名已结束，B仍可报名，目标为学习效果。",...base,constraints:[{id:"availability",condition:"available"}],options:[option("A",[9],{},{atoms:{available:false}}),option("B",[5],{},{atoms:{available:true}})],expect:{status:"RESOLVED",leaders:["B"],reject:["A"],ask:null}},
 {id:"unknown_values",text:"A和B均可行，A效果未知，B已知。",...base,options:[option("A",[null]),option("B",[5])],expect:{status:"UNRESOLVED",leaders:[],reject:[],ask:null}},
 {id:"scope_outside",text:"我心情不佳，想知道原因。",...base,requests:[],options:[],expect:{status:"OUT_OF_SCOPE",leaders:[],reject:[],ask:null}}
 ];
 const sorted=x=>[...x].sort();
 const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const canonical=x=>x===null||typeof x!=="object"?JSON.stringify(x):Array.isArray(x)?"["+x.map(canonical).join(",")+"]":"{"+Object.keys(x).sort().map(k=>JSON.stringify(k)+":"+canonical(x[k])).join(",")+"}";
 function plan(c){
  const order=[],seen=new Set(),blocked=[];
  function visit(k){if(seen.has(k))return;if(!registry[k]){blocked.push(k);return}for(const d of registry[k].deps)visit(d);seen.add(k);order.push(k)}
  visit(G);for(const k of c.requests)visit(k);return {order,blocked};
 }
 const worlds=qs=>qs.reduce((acc,x)=>acc.flatMap(w=>x.values.map(v=>({...w,[x.id]:v}))),[{}]);
 const resolve=(x,w)=>typeof x==="string"&&x.startsWith("$")?w[x.slice(1)]:x;
 function logic(f,atoms,w){
  if(typeof f==="string"){const x=resolve(atoms?.[f],w);return typeof x==="boolean"?x:null}
  const [op,...xs]=f;const vs=xs.map(x=>logic(x,atoms,w));
  if(op==="not")return vs[0]===null?null:!vs[0];
  if(op==="and")return vs.includes(false)?false:vs.every(x=>x===true)?true:null;
  if(op==="or")return vs.includes(true)?true:vs.every(x=>x===false)?false:null;
  throw Error("operator");
 }
 function feasible(c,o,w){
  const tests=c.constraints.map(h=>{
   if(h.condition)return logic(h.condition,o.atoms,w);
   const m=o.metrics[h.metric];if(!m||m.unit!==h.unit)return null;
   const n=resolve(m.value,w);if(typeof n!=="number"||!Number.isFinite(n))return null;
   if(h.op==="<=")return n<=h.limit;if(h.op==="<")return n<h.limit;throw Error("bound");
  });
  if(tests.includes(false))return "REJECT";
  return tests.every(x=>x===true)?"ACCEPT":"UNRESOLVED";
 }
 function outcome(c,w){
  const states=Object.fromEntries(c.options.map(o=>[o.id,feasible(c,o,w)]));
  if(Object.values(states).includes("UNRESOLVED"))return {states,leaders:[],known:false};
  const os=c.options.filter(o=>states[o.id]==="ACCEPT");
  if(!os.length)return {states,leaders:[],known:true};
  let leaders=[];
  if(c.criterion==="pareto"){
   if(os.some(o=>!o.score.length||o.score.length!==os[0].score.length||o.score.some(x=>typeof x!=="number"||!Number.isFinite(x))))return {states,leaders:[],known:false};
   leaders=os.filter(o=>!os.some(p=>p!==o&&p.score.every((v,i)=>v>=o.score[i])&&p.score.some((v,i)=>v>o.score[i]))).map(o=>o.id);
  }else if(c.criterion==="regret"){
   if(os.some(o=>!o.utilities?.length||o.utilities.length!==os[0].utilities.length||o.utilities.some(x=>typeof x!=="number"||!Number.isFinite(x))))return {states,leaders:[],known:false};
   const max=os[0].utilities.map((_,i)=>Math.max(...os.map(o=>o.utilities[i])));
   const worst=os.map(o=>Math.max(...o.utilities.map((u,i)=>max[i]-u)));
   leaders=os.filter((o,i)=>worst[i]===Math.min(...worst)).map(o=>o.id);
  }else return {states,leaders:[],known:false};
  return {states,leaders:sorted(leaders),known:true};
 }
 function choose(rows,qs){
  if(rows.every(x=>x.result.known)&&new Set(rows.map(x=>canonical(x.result))).size===1)return {depth:0,ask:null};
  let best={depth:Infinity,ask:null};
  for(const q of qs){
   const children=q.values.map(v=>rows.filter(x=>x.world[q.id]===v)).filter(x=>x.length);
   if(children.length<2)continue;
   const depth=1+Math.max(...children.map(x=>choose(x,qs.filter(z=>z.id!==q.id)).depth));
   if(depth<best.depth)best={depth,ask:q.id};
  }
  return best;
 }
 function analyze(c){
  const empty=(status,extra={})=>({status,leaders:[],reject:[],ask:null,...extra});
  if(!c.authorized)return empty("BLOCKED");
  if(!c.confirmed)return empty("CLARIFY");
  if(!c.requests.length)return empty("OUT_OF_SCOPE");
  const p=plan(c);
  if(!c.coverage||(!c.constraints.length&&!c.explicitEmpty)||p.blocked.length)return empty("BLOCKED",{plan:p});
  const rows=worlds(c.questions).map(w=>({world:w,result:outcome(c,w)}));
  const proof=choose(rows,c.questions);
  const reject=c.options.filter(o=>rows.every(x=>x.result.states[o.id]==="REJECT")).map(o=>o.id);
  if(proof.depth===0)return {status:"RESOLVED",leaders:rows[0].result.leaders,reject:sorted(reject),ask:null,plan:p,rows};
  return {status:proof.ask?"ASK":"UNRESOLVED",leaders:[],reject:sorted(reject),ask:proof.ask,plan:p,rows};
 }
 const rows=cases.map(c=>{const actual=analyze(c);const pick=({status,leaders,reject,ask})=>({status,leaders,reject,ask});if(!equal(pick(actual),c.expect))throw Error(c.id+" "+JSON.stringify(actual));return {id:c.id,text:c.text,expected:c.expect,actual}});
 // Answer and revision: confirmed answer narrows model input, old result cannot publish after change.
 const c=cases.find(x=>x.id==="career_exception");
 const updates=[false,true].map(family=>{const next={...c,revision:2,questions:[q("family",[family])]},actual=analyze(next);const expected=family?"A":"B";if(actual.status!=="RESOLVED"||!equal(actual.leaders,[expected]))throw Error("answer");return {family,revision:2,actual}});
 // Exact canonical snapshot equality as research integrity relation, no cryptographic/authentication claim.
 function receipt(c){return {revision:c.revision,epoch:c.epoch,snapshot:canonical(c),result:analyze(c)}}
 function publish(current,x){return current.authorized&&x.revision===current.revision&&x.epoch===current.epoch&&x.snapshot===canonical(current)&&canonical(x.result)===canonical(analyze(current))}
 const s=cases[0],rec=receipt(s);
 const controlSpecs=[
 ["exact",s,rec,true],["changed_revision",{...s,revision:2},rec,false],["revoked",{...s,authorized:false,epoch:2},rec,false],["restored_old_epoch",{...s,epoch:2},rec,false],
 ["changed_same_revision",{...s,constraints:[cap("rent","cost","<",2500,"yuan/month")]},rec,false],
 ["tampered_output",s,{...rec,result:{...rec.result,leaders:["B"]}},false],
 ["fabricated_snapshot",s,{...rec,snapshot:"wrong"},false],
 ["fresh_revision",{...s,revision:2},receipt({...s,revision:2}),true]
 ];
 const controls=controlSpecs.map(([id,current,x,expected])=>{const actual=publish(current,x);if(actual!==expected)throw Error(id);return {id,expected,actual}});
 // Current confirmed source identity mismatch cannot admit research candidate or forged source.
 const admission=[];for(const [key,source] of Object.entries(registry)){
  for(const kind of ["exact","wrong_blob","wrong_path","wrong_version"]){
   const proposal={key:kind==="wrong_version"?key.replace("1.0.0","9.0.0"):key,path:kind==="wrong_path"?"wrong":source.path,blob:kind==="wrong_blob"?"wrong":source.blob};
   const trusted=registry[proposal.key];const actual=!!trusted&&proposal.path===trusted.path&&proposal.blob===trusted.blob;
   if(actual!==(kind==="exact"))throw Error("admission");
   admission.push({kind,key,actual});
  }
 }
 const mutant=analyze({...s,explicitEmpty:false,constraints:[]});
 if(mutant.status!=="BLOCKED")throw Error("empty");
 return {summary:{cases:rows.length,answer_updates:updates.length,receipt_controls:controls.length,identity_controls:admission.length,empty_control:1,total:rows.length+updates.length+controls.length+admission.length+1,correct:rows.length+updates.length+controls.length+admission.length+1,statuses:rows.reduce((m,x)=>(m[x.actual.status]=(m[x.actual.status]||0)+1,m),{})},rows,updates,controls,admission,empty_control:mutant};
}
console.log(JSON.stringify(experiment(),null,2));
