# 自主认知专项累计第107轮候选：计算发布事务、跨轮失效与重复完成
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 7a7aa9fdbf986d07e9492263ddb7ee2e7d9ccba6。读取近期12提交、13开放PR、v3.2前15行（前轮全文）、唯一交接前18行、R106前18行与结果、R70前45行、R71前35行、R36/R4/R34前14行及R66/R67全文代码。R36为v0.6会话关闭竞态；R4为有类型方法依赖；R70为数学收据核验；R106为静态失效。本轮新增有限事件交错的计算发布事务，非实际平台漏洞或生产修复。当前容器未保留原生隔离目录，raw.githubusercontent.com解析失败；未恢复原生Python、API、设备或完整数学执行。

## 资产
research/decision_hub/2026-11-25-grounded-knowledge-provenance-inference.md 1a7a8560ff3349635966857a07a4e71b1680f7f6
research/decision_hub/2026-11-25-native-method-backward-knowledge-planning.md ca51e90ab907c50524243231dc905f7ad1067ea8
R106 blob 33b87eae4f6500e3bab01854f97850ceb27a178e；R70 1a6572805eaeb9400ca5b8429a14e1f518493a91；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。

## 合同
可信宿主夹具提供完整已确认非空约束、两个虚构方案、当前授权及范围。固定R66两种知识状态，sm=4合格、20冲突；只人工映射为测量资格，非科学事实推导。复用R67原plan作C028计算准备门。计算本体仅两点阈值比较模拟，未调用真实C028；不得将P.plan的准备度视为正式执行准入。数字及授权均合成。相关变更（底线、测量、授权、知识、范围）增加单调代次并立即隐藏旧当前结果；目标变更在本合同独立于硬约束，保持原计算。授权恢复、数值恢复、来源恢复不能恢复旧任务代次（ABA）；任务启动后保存结果，完成按当前代次和资格复核，已消费任务重复完成拒绝。新任务同一有效代次完成可以替代旧同代次结果；过期任务完成不会覆盖已发布新结果。任务身份通过可信队列位置模拟，无真实鉴权、伪造防护、并行线程/数据库事务、签发、持久化、备份恢复、取消、真实撤回清理、授权范围核验、上限或跨端实现。实际实现须以原子比较交换或等效事务保证检查与发布不可被插入变更，且展示读取同一快照。研究选择为保守全相关代次失效，可能额外计算。独立目标前提改变则需更广依赖，不能通用化。无实际建议发布权限。

9种事件的全部长度5序列，逐前缀比较候选与独立事件日志参照；参照使用任务起点后的变更事件判定，不使用候选代次。统计为共享前缀树边数，非独立用户情节或实测竞态频率。简化基线无失效的旧缓存可显示过期结果；naiveInvalidDisplays计前缀边上的基线非空且与当前有效结果不同或无当前结果，不是实际产品错误率。12额外控制包括ABA、撤权、重复完成、两任务逆序、目标独立。合成开发材料为ChatGPT研发辅助项目原创，不是训练、真人、独立留出或独立验收。未增加费用、训练、CI、生产变更、PR合并、部署或冻结变更。

## 复算
从固定Git版本获取两个报告全文至docs[i].content，Node标准JS。
```js
function load(doc,marker,names){const s=doc.split("```js\n")[1].split("\n```")[0].split(marker)[0];return Function(s+"\nreturn {"+names+"};\n};\nreturn probe();")()}
const K=load(docs[0].content," let out={graphs:","report");
const P=load(docs[1].content," let out={snapshots:","plan,phrases");
function experiment(K,P){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const reports=[K.report(4,63),K.report(20,63)],valid=reports.map(r=>r.supports[6].length>0&&!r.methodReview);
 ck(eq(valid,[true,false]),"knowledge fixture");
 const ops=["start","finishFirst","finishLast","limit","measure","auth","source","objective","scope"];
 const relevant=new Set(["limit","measure","auth","source","scope"]);
 function initial(){return {epoch:0,limit:10,measure:0,auth:true,source:0,objective:0,scope:0,jobs:[],published:null,naive:null}}
 function plan(s){return P.plan({inventory:"nonempty",accepted:2,gateSourceOK:true,facts:s.auth&&valid[s.source]?["measurements"]:[]},P.phrases[0])}
 function can(s){return s.auth&&plan(s).status==="PREPARED_FOR_NATIVE_REVIEW"}
 function calc(s){return [8+s.measure,10+s.measure].map(x=>x<=s.limit?"PASS":"FAIL")}
 function step(s,e){
  s=JSON.parse(JSON.stringify(s));let decision="NONE";
  if(relevant.has(e)){
   s.epoch++;s.published=null;
   if(e==="limit")s.limit=20-s.limit+2;
   if(e==="measure")s.measure=2-s.measure;
   if(e==="auth")s.auth=!s.auth;
   if(e==="source")s.source=1-s.source;
   if(e==="scope")s.scope=1-s.scope;
  }else if(e==="objective")s.objective=1-s.objective;
  else if(e==="start"){
   if(can(s)){s.jobs.push({epoch:s.epoch,output:calc(s),used:false});decision="STARTED"}else decision="NOT_READY";
  }else{
   const j=e==="finishFirst"?s.jobs[0]:s.jobs.at(-1);
   if(!j)decision="NO_JOB";
   else{
    if(!j.used)s.naive=j.output;
    if(j.used)decision="REPLAY";
    else{j.used=true;if(j.epoch!==s.epoch||!can(s))decision="STALE";else{s.published=j.output;decision="PUBLISHED"}}
   }
  }
  return {s,decision}
 }
 // Independent event-log oracle. No epoch counter or candidate transition.
 function replay(trace){
  let limit=10,measure=0,auth=true,source=0,scope=0,objective=0,jobs=[],pub=null,decision="NONE";
  for(let i=0;i<trace.length;i++){
   let e=trace[i];decision="NONE";
   if(["limit","measure","auth","source","scope"].includes(e))pub=null;
   switch(e){
    case "limit":limit=limit===10?12:10;break;
    case "measure":measure=measure===0?2:0;break;
    case "auth":auth=!auth;break;
    case "source":source=1-source;break;
    case "scope":scope=1-scope;break;
    case "objective":objective=1-objective;break;
    case "start":
     if(auth&&source===0){jobs.push({start:i,output:[8+measure<=limit?"PASS":"FAIL",10+measure<=limit?"PASS":"FAIL"],done:false});decision="STARTED"}else decision="NOT_READY";break;
    default:{
     let j=e==="finishFirst"?jobs[0]:jobs[jobs.length-1];
     if(!j)decision="NO_JOB";
     else if(j.done)decision="REPLAY";
     else{j.done=true;let changed=trace.slice(j.start+1,i).some(x=>["limit","measure","auth","source","scope"].includes(x));
      if(changed||!auth||source!==0)decision="STALE";else{pub=j.output;decision="PUBLISHED"}}
    }
   }
  }
  return {decision,pub,auth,source,limit,measure,scope,objective}
 }
 let o={traces:0,transitionChecks:0,matched:0,started:0,published:0,staleRejected:0,replayRejected:0,notReady:0,noJob:0,displayInvalidated:0,objectivePreserved:0,naiveInvalidDisplays:0,controls:0,examples:{}};
 function visit(s,trace){
  if(trace.length===5){o.traces++;return}
  for(let e of ops){let t=[...trace,e],z=step(s,e),r=replay(t),a=z.s;
   ck(z.decision===r.decision&&eq(a.published,r.pub)&&["auth","source","limit","measure","scope","objective"].every(k=>a[k]===r[k]),"oracle "+t.join(","));
   o.transitionChecks++;o.matched++;
   const key={STARTED:"started",PUBLISHED:"published",STALE:"staleRejected",REPLAY:"replayRejected",NOT_READY:"notReady",NO_JOB:"noJob"}[z.decision];if(key)o[key]++;
   if(s.published&&relevant.has(e)&&!a.published)o.displayInvalidated++;
   if(s.published&&e==="objective"&&eq(s.published,a.published))o.objectivePreserved++;
   if(a.naive&&(!a.published||!eq(a.naive,a.published)))o.naiveInvalidDisplays++;
   visit(a,t);
  }
 }
 visit(initial(),[]);
 const controls=[
  [["start","limit","finishFirst"],"STALE",null],
  [["start","limit","limit","finishFirst"],"STALE",null],
  [["start","auth","auth","finishFirst"],"STALE",null],
  [["start","source","source","finishFirst"],"STALE",null],
  [["start","objective","finishFirst"],"PUBLISHED",["PASS","PASS"]],
  [["start","finishFirst","finishFirst"],"REPLAY",["PASS","PASS"]],
  [["start","measure","start","finishLast"],"PUBLISHED",["PASS","FAIL"]],
  [["start","measure","start","finishLast","finishFirst"],"STALE",["PASS","FAIL"]],
  [["start","finishLast","scope"],"NONE",null],
  [["auth","start"],"NOT_READY",null],
  [["source","start"],"NOT_READY",null],
  [["start","finishLast","objective"],"NONE",["PASS","PASS"]]
 ];
 for(let [t,d,p] of controls){let s=initial(),z;for(let e of t){z=step(s,e);s=z.s}ck(z.decision===d&&eq(s.published,p),"control "+t.join(","));o.controls++;o.examples[t.join("/")]=[d,p]}
 ck(o.traces===59049&&o.transitionChecks===66429,"coverage");return o
}
console.log(JSON.stringify(experiment(K,P),null,2));
```
## 实测
```json
{
  "traces": 59049,
  "transitionChecks": 66429,
  "matched": 66429,
  "started": 3441,
  "published": 967,
  "staleRejected": 1736,
  "replayRejected": 1297,
  "notReady": 3940,
  "noJob": 10762,
  "displayInvalidated": 1165,
  "objectivePreserved": 233,
  "naiveInvalidDisplays": 7057,
  "controls": 12,
  "examples": {
    "start/limit/finishFirst": [
      "STALE",
      null
    ],
    "start/limit/limit/finishFirst": [
      "STALE",
      null
    ],
    "start/auth/auth/finishFirst": [
      "STALE",
      null
    ],
    "start/source/source/finishFirst": [
      "STALE",
      null
    ],
    "start/objective/finishFirst": [
      "PUBLISHED",
      [
        "PASS",
        "PASS"
      ]
    ],
    "start/finishFirst/finishFirst": [
      "REPLAY",
      [
        "PASS",
        "PASS"
      ]
    ],
    "start/measure/start/finishLast": [
      "PUBLISHED",
      [
        "PASS",
        "FAIL"
      ]
    ],
    "start/measure/start/finishLast/finishFirst": [
      "STALE",
      [
        "PASS",
        "FAIL"
      ]
    ],
    "start/finishLast/scope": [
      "NONE",
      null
    ],
    "auth/start": [
      "NOT_READY",
      null
    ],
    "source/start": [
      "NOT_READY",
      null
    ],
    "start/finishLast/objective": [
      "NONE",
      [
        "PASS",
        "PASS"
      ]
    ]
  }
}
```
后续：真实原生执行与实际事务、持久化、授权代次恢复测试；独立验收轨保留未见案例，产品轨维护唯一交接。正式版本另获授权。
