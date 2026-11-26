# 自主长期决策：预留身份去重、来源区间交集与资源余量证书
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与范围
同一手动轮第二阶段，起点main 0bbe6cbf539f20c59d026430fd9b5fa8754a9316。沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、固定唯一交接及#63 head 734686980b19da9291bdd08b67d4e2519c011acf；未重跑原生。实际读取并执行上一阶段 research/decision_hub/2026-11-26-actor-scoped-resource-flow-and-common-plan.md blob bd75b981b35e3c63cbc5550b8ea690ddea2ed80f 的flow/verify/witness/common/ports/brute；上轮容量已去重为固定整数，本轮新增已资格同身份多个来源与多笔预留、剩余容量区间、固定与情景分配。既有数值区间投影e9290c4efda30628dfbd8d76691d3f1f7fee7669及版本差分57baff2229328ad2391c31dd6285c562b7349834的交集和当前性原理复用，不宣称发明新数学理论或全库查重。
## 合同及证明
由可信宿主给出有限联合语义世界、固定池ID、确切的已存在预留ID清单（完整覆盖）、每个预留只占用一个池，同量纲同时段同用途及授权，且所有同身份的合格区间都是可同时成立的硬限制。每个当前来源具有独立ID/版本；本原型检查夹具资格及同组唯一当前source，不自动决定最新来源、共享资源身份、真实授权、来源真值或已发生交易。对同一个容量/预留身份，取区间交[L,U]，不存在合格记录为MISSING_EVIDENCE、交集空为SOURCE_CONFLICT，均禁止给确定余量；不同预留即使来源或数值相同仍须分别累计。若独立盒形域已确认（本轮有限夹具），池的剩余容量下界为C_L减去各预留上界之和，上界为C_U减去各预留下界之和。若下界负，显示POSSIBLE_EXISTING_OVERBOOK并隔离，不截断到零或删除该世界。该保守政策未区分全确定过度预留和部分过度预留的后续补偿策略。预留间及总量的现实依赖若未知，界限可作保守包络但不声称尖锐或精确混合；本轮独立盒形和非负区间下端均可达。整数可拆分同单位、固定需求/池身份/资格，沿用上轮网络。最大流对每池容量单调，故低端全满足证明盒内每个完成均有方案，高端仍不足证明所有完成均不足，否则是有通过和失败见证的混合。共同固定方案取所有世界的下界容量最小值及资格交集，与逐完成共享分配穷举等价。所有计算是条件只读，authority NONE；无证据覆盖不可用作正式推荐，未处理不可拆分任务、任意时序、未知预留清单或撤权后真实数据恢复。
## 实际实验
1000图、2至4世界、每世界2个池，各2笔真实身份预留（每笔0..2）、容量4..6，多个区间报告保证共同支持，另加不合格来源诱饵；2个需求各1..3，资格掩码0..3。独立参照在每个世界按每条记录对0..9整数取值直接过滤并枚举容量及所有预留，生成真实盒内所有剩余容量，再逐单位穷举分配。端点流、割见证和全完成参照对照，共同固定方案与全部完成共享分配对照。错误基线每条预留报告分别扣减、只取首个来源。每图同值来源版更新验证数值不变但证据身份改变，检查其他世界未变化；没有实现真实缓存收据或数据库。7控制含同身份两报告、矛盾、缺失、撤权、可能过度预留、不同身份及重复来源记录。标准JS连接器实际执行两次结果一致。
```json
{
  "graphs": 1000,
  "worlds": 3006,
  "concreteCompletions": 16425,
  "intervalEndpointChecks": 6012,
  "commonChecks": 1000,
  "commonBruteChecks": 1000,
  "allWorldsAdaptiveOnly": 25,
  "duplicateWrongFail": 487,
  "duplicateWrongPass": 0,
  "firstSourceMissDefinite": 274,
  "firstSourceWrongDefinite": 0,
  "versionOnlyChanges": 1000,
  "unaffectedWorldChecks": 2006,
  "controls": 7,
  "states": {
    "MIXED": 494,
    "EVERY_COMPLETION_HAS_PLAN": 802,
    "NO_COMPLETION_HAS_PLAN": 1710
  }
}
```
## 接入与局限
建议ResourceReservationGroup包含已确认池/占用根、时间、单位、主体、来源版本、资格及完整清单；缺资格返回未决，不能假定无占用。ResidualCapacityBounds作为ActorResourceScope输入，直接记录全部有效来源及冲突见证；确认现有预留和可用余量后才进入流算法。真实并发预留/扣款、跨期资源和实际支出另用版本事务及真实行动账本。本轮不运行原生API/CLI、Mac/iPhone、真实用户或独立留出，未调整工作流、生产代码、交接、冻结、证据等级、PR、训练、部署、主动CI或费用。研究者选择有限整数组合、保守过度预留政策、独立盒形与基线。
## 复算
固定上一报告作为唯一参数，Node包装未执行；连接器实际运行核心。
```js
const code=require("node:fs").readFileSync(process.argv[2],"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0];
const make=Function(code.split(" const out={singleCases:")[0]+"\nreturn {flow,verify,witness,common,ports,brute};\n}\nreturn experiment();");
function experiment2(make){
 const {flow,verify,witness,common,ports,brute}=make(),ck=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 let seed=20261127;
 const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const sum=a=>a.reduce((x,y)=>x+y,0);
 const row=(id,pool,kind,source,lo,hi,extra={})=>({id,pool,kind,source,version:1,unit:"quanta",period:"period1",grant:1,ok:true,lo,hi,...extra});
 const eligible=r=>r.ok===true&&r.grant===1&&r.unit==="quanta"&&r.period==="period1"&&Number.isSafeInteger(r.version)&&r.version>0;
 function project(world){
  const groups=[],lo=[],hi=[],unknown=[],conflicts=[],overbook=[];
  // Expected identity list is host-confirmed complete. No inference from names or amount.
  for(const p of world.pools){
   const ids=[{id:p.cap,kind:"capacity"},...p.res.map(id=>({id,kind:"reservation"}))];
   if(new Set(ids.map(v=>v.id)).size!==ids.length)throw Error("duplicate expected identity");
   const records=[];
   for(const g of ids){
    const selected=world.rows.filter(x=>eligible(x)&&x.id===g.id&&x.pool===p.id&&x.kind===g.kind);
    if(new Set(selected.map(x=>x.source)).size!==selected.length)throw Error("duplicate current source identity");
    for(const x of selected)ck(Number.isInteger(x.lo)&&Number.isInteger(x.hi)&&x.lo>=0&&x.lo<=x.hi&&x.hi<=9,"bounds");
    if(!selected.length){unknown.push([p.id,g.id]);records.push(null);continue}
    const L=Math.max(...selected.map(x=>x.lo)),U=Math.min(...selected.map(x=>x.hi));
    if(L>U)conflicts.push([p.id,g.id]);
    records.push({id:g.id,L,U,sources:selected.map(x=>[x.source,x.version]).sort()});
   }
   groups.push({pool:p.id,records});
   if(records.some(x=>!x||x.L>x.U)){lo.push(null);hi.push(null);continue}
   const [c,...r]=records;
   // Pre-existing overbooking is a separate unresolved contract. Do not clip or delete.
   const min=c.L-sum(r.map(x=>x.U)),max=c.U-sum(r.map(x=>x.L));
   if(min<0){overbook.push({pool:p.id,min,max});lo.push(null);hi.push(null);continue}
   lo.push(min);hi.push(max);
  }
  const status=conflicts.length?"SOURCE_CONFLICT":unknown.length?"MISSING_EVIDENCE":overbook.length?"POSSIBLE_EXISTING_OVERBOOK":"QUALIFIED_INTERVAL";
  return {status,groups,lo:[...lo,0],hi:[...hi,0],unknown,conflicts,overbook};
 }
 // Direct enumeration of qualified primitive record constraints, independent of intersection arithmetic.
 function enumerate(world){
  const per=[];
  for(const p of world.pools){
   const ids=[{id:p.cap,kind:"capacity"},...p.res.map(id=>({id,kind:"reservation"}))];
   const vals=ids.map(g=>Array.from({length:10},(_,i)=>i).filter(i=>world.rows.some(x=>eligible(x)&&x.id===g.id&&x.pool===p.id&&x.kind===g.kind)&&world.rows.filter(x=>eligible(x)&&x.id===g.id&&x.pool===p.id&&x.kind===g.kind).every(x=>x.lo<=i&&i<=x.hi)));
   const rem=new Set();
   function dfs(j,x){if(j===vals.length){rem.add(x[0]-sum(x.slice(1)));return}for(const k of vals[j])dfs(j+1,[...x,k])}
   dfs(0,[]);per.push([...rem].sort((a,b)=>a-b));
  }
  return per[0].flatMap(i=>per[1].map(j=>({c:[i,j,0],e:world.e})));
 }
 function mk(){
  const pools=[{id:"p0",cap:"cap0",res:["r00","r01"]},{id:"p1",cap:"cap1",res:["r10","r11"]}];
  let rows=[];
  for(const p of pools){
   let c=4+rnd(3);
   // Two reports of the same total; intersection nonempty.
   rows.push(row(p.cap,p.id,"capacity",p.cap+"a",Math.max(4,c-rnd(2)),Math.min(6,c+rnd(2))));
   rows.push(row(p.cap,p.id,"capacity",p.cap+"b",Math.max(4,c-rnd(2)),Math.min(6,c+rnd(2))));
   for(const r of p.res){
    const v=rnd(3);
    rows.push(row(r,p.id,"reservation",r+"a",Math.max(0,v-rnd(2)),Math.min(2,v+rnd(2))));
    if(rnd(2))rows.push(row(r,p.id,"reservation",r+"b",Math.max(0,v-rnd(2)),Math.min(2,v+rnd(2))));
   }
   // Incompatible source may have an identical root ID, but is outside grant or period.
   rows.push(row(p.cap,p.id,"capacity",p.cap+"bad",0,0,{grant:0}));
  }
  return {pools,rows,e:[rnd(4),rnd(4),0]};
 }
 const out={graphs:0,worlds:0,concreteCompletions:0,intervalEndpointChecks:0,commonChecks:0,commonBruteChecks:0,allWorldsAdaptiveOnly:0,duplicateWrongFail:0,duplicateWrongPass:0,firstSourceMissDefinite:0,firstSourceWrongDefinite:0,versionOnlyChanges:0,unaffectedWorldChecks:0,controls:0,states:{}};
 const check=(d,w)=>{
  const z=project(w);ck(z.status==="QUALIFIED_INTERVAL","qualified generated domain");
  const possible=enumerate(w);ck(possible.length>0&&possible.every(v=>v.c.every(x=>x>=0)),"nonempty");
  ck(eq(z.lo,[0,1,2].map(j=>Math.min(...possible.map(v=>v.c[j]))))&&eq(z.hi,[0,1,2].map(j=>Math.max(...possible.map(v=>v.c[j])))),"endpoint parity");
  const lows={c:z.lo,e:w.e},highs={c:z.hi,e:w.e};
  const l=flow(d,lows),h=flow(d,highs),L=verify(d,lows,l),H=verify(d,highs,h);
  const states=possible.map(v=>brute(d,[v]));
  ck(L===states.every(Boolean)&&H===states.some(Boolean),"monotone feasibility");
  out.concreteCompletions+=states.length;out.intervalEndpointChecks+=2;out.worlds++;
  const state=L?"EVERY_COMPLETION_HAS_PLAN":H?"MIXED":"NO_COMPLETION_HAS_PLAN";out.states[state]=(out.states[state]||0)+1;
  // Deliberately wrong: every report of a reservation is a separate obligation.
  const duplicate=w.pools.map(p=>{
   const cap=z.groups.find(x=>x.pool===p.id).records[0].L;
   return Math.max(0,cap-sum(w.rows.filter(v=>eligible(v)&&v.pool===p.id&&v.kind==="reservation").map(v=>v.hi)));
  });
  const dup=flow(d,{c:[...duplicate,0],e:w.e}).f===sum(d);
  out.duplicateWrongFail+=+(L&&!dup);out.duplicateWrongPass+=+(!L&&dup);
  // First-source baseline underapproximates knowledge, using same original interval contract.
  const seen=new Set(),first={...w,rows:w.rows.filter(v=>{if(!eligible(v))return true;const k=v.pool+"|"+v.id;if(seen.has(k))return false;seen.add(k);return true})};
  const f=project(first);ck(f.status==="QUALIFIED_INTERVAL","first input");
  const fL=flow(d,{c:f.lo,e:w.e}).f===sum(d),fH=flow(d,{c:f.hi,e:w.e}).f===sum(d);
  out.firstSourceMissDefinite+=+(L&&!fL||!H&&fH);
  out.firstSourceWrongDefinite+=+(fL&&!L||!fH&&H);
  return {z,possible,L,H,lows};
 };
 for(let t=0;t<1000;t++){
  const d=[1+rnd(3),1+rnd(3),0],W=2+rnd(3),ws=Array.from({length:W},mk),zs=ws.map(w=>check(d,w));
  const all=zs.flatMap(v=>v.possible),c=common(zs.map(v=>v.lows)),v=flow(d,c),ok=verify(d,c,v);
  ck(ok===brute(d,all),"common exact across completions");out.commonChecks++;out.commonBruteChecks++;
  if(zs.every(z=>z.L)&&!ok)out.allWorldsAdaptiveOnly++;
  // Same numeric interval with new source version changes lineage and only its world.
  const k=rnd(W),w=JSON.parse(JSON.stringify(ws[k])),old=project(w);
  w.rows[0].version++;const fresh=project(w);
  ck(eq(old.lo,fresh.lo)&&eq(old.hi,fresh.hi)&&!eq(old.groups,fresh.groups),"version-only change");out.versionOnlyChanges++;
  for(let i=0;i<W;i++)if(i!==k){ck(eq(zs[i].z,project(ws[i])),"unaffected");out.unaffectedWorldChecks++}
  out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 let w={pools:[{id:"p0",cap:"c0",res:["r"]},{id:"p1",cap:"c1",res:[]}],e:[1,2,0],rows:[row("c0","p0","capacity","c",4,4),row("r","p0","reservation","a",2,2),row("r","p0","reservation","b",2,2),row("c1","p1","capacity","c",2,2)]};
 ctl(eq(project(w).lo,[2,2,0]),"one obligation two sources");
 let x=JSON.parse(JSON.stringify(w));x.rows[2].lo=3;x.rows[2].hi=3;ctl(project(x).status==="SOURCE_CONFLICT","conflict");
 x=JSON.parse(JSON.stringify(w));x.rows=x.rows.filter(v=>v.id!=="r");ctl(project(x).status==="MISSING_EVIDENCE","missing not zero");
 x=JSON.parse(JSON.stringify(w));x.rows[1].grant=0;x.rows[2].grant=0;ctl(project(x).status==="MISSING_EVIDENCE","withdrawal");
 x=JSON.parse(JSON.stringify(w));x.rows[0].lo=1;x.rows[0].hi=4;ctl(project(x).status==="POSSIBLE_EXISTING_OVERBOOK","possible pre-existing deficit");
 x=JSON.parse(JSON.stringify(w));x.pools[0].res.push("r2");x.rows.push(row("r2","p0","reservation","a",1,1));ctl(eq(project(x).lo,[1,2,0]),"different same-source reservation");
 x=JSON.parse(JSON.stringify(w));x.rows.push({...x.rows[1]});let bad=false;try{project(x)}catch{bad=true}ctl(bad,"duplicate current report identity");
 return out;
}
console.log(JSON.stringify(experiment2(make),null,2));
```
