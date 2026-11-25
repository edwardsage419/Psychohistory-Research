# 自主认知专项累计第119轮候选：原始日期锚定与共享时间窗口可行性
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / EXACT_BOUNDED_SCHEDULING / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main b4165eec265a6855440b3e07ca64abc14dfa8259。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、同步规程前22行、唯一交接前18行、R118前20行及实际源码、R97/R98前22行、R42前16行、R67规划源码前段。R97/R98为总时间现金与承诺状态，R42为随机支持下鲁棒反馈，R118为公历锚定，本轮新增有限每日容量、开始/截止窗口、可抢占单位工作与相同义务下可选新计划的工时前沿。未重复上述DP或原生方法。
## 固定资产
research/decision_hub/2026-11-25-civil-temporal-anchor-version-replay.md cc9f6c6103e4ac863d2cdaa6961721149fd4189a
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
R97 fa8c878449a333ab9ebe787c015df43dbcd1ec9f；R98 db648df87860bcb00037c8dddb3a2bc85d8aee28；R42 1d69fe923238f56fb8fb1f822c366335182f89ed；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。无新外部资料、个人信息或真实日程。
## 合同及算法
四个合成民用日期、每日0..2可用整数小时；三个任务最多各3小时。已获资格开始日期、工时和截止日（含截止日）由宿主夹具给定，两个必需任务A/B及可选新任务C，不默认真实人生目标。每单位可在任意合格日分配，完全可拆分、单一共享同质资源，零切换成本、无依赖、无时刻、无现金、无并发、无随机、无真实生产容量或工作日规则。明确日期短语由实际R118 propose/verify解析，A从本周三修订为本周四，B两种固定截止版本情景，C本周四；所有锚点为2026-11-23研究夹具，不是实际用户日期。绑定根、版本、原文、来源及原始锚点；实际R118校验后才投影，历史解释不能以旧版本替代当前。释放日和工时等外部字段资格仅布尔模拟，未绑定实际加密收据；无真实权限、用户确认、版本CAS、持久化或日程接入。校验缺失返回UNKNOWN_INPUT，过界不主张不可行。当前代码的固定日期、容量与任务域是研究者选择。
逐日按最早截止时间EDF分配单位时间，期限相同按ID打破平局。证明思路：若存在可行排程，与EDF的最早差异处交换较晚截止任务与EDF所选任务之后的一单位（或把该单位提前至空闲），后者已释放且前者截止不早于后者，交换不违反窗口；归纳成立。因此此有限合同下有可行排程则EDF找到。独立参照对每个可用小时递归枚举空闲或任一可执行任务，直接判断全部工作完成。不可行时寻找闭区间内所有可行窗口被包含的任务需求超过该区间容量的证书，必要性由这些任务无其他窗口直接得到；每个实测失败均验证正短缺证书，本轮不对其他调度模型宣称充分。EDF排序每单位最多3任务，直接枚举指数级，固定域有限；未测真实设备时延/内存。输出仅authority NONE，有限可行性不代表真实方案完整覆盖或授权。
可选C的0..3小时逐一验证，必需任务不可行则前沿null；若可行，最大额外小时只代表本模型固定窗口中可容纳的工作量，非福利/概率/目标收益。A延期只放宽一个窗口，不新增总资源，旧排程仍可行，前沿不得下降；不含延期违约或其他成本。聚合对照只比较全部需求与总工时，故可错放行，非原生系统或普通AI。证书例为合成，不代表现实。
## 实验
12日容量模式×3 A工时×3 B工时×2 B期限×2 A释放日=432配对情景，每个旧新版本各4个C工时，3456次EDF/直接枚举和独立证书检查。每配对旧A收据用于当前版拒绝及当前来源撤回未知。11专项控制。所有参数与参考由研究者选择，非独立验收、真人、训练或生产。未调用原生C028/决策引擎、真实时间日程或真机。无训练、Codex、CI、生产修改、PR合并、部署、费用及冻结协议变化。
## 复算
按上述三份固定文件顺序读取docs[i].content。Node标准JS，仅加载已审查的项目自有源码。
```js
function load(docs){
 const code=i=>docs[i].content.split("```js\n")[1].split("\n```")[0];
 const L=Function(code(2).slice(code(2).indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {lexical,parseNum};\n}\nreturn experiment({});")();
 const T=Function("L",code(1).slice(code(1).indexOf("function experiment(L,R,I,G")).split(" // Reuse the actual R116 graph")[0]+"\nreturn {temporal};\n}\nreturn experiment(L);")(L);
 return Function("T",code(0).slice(code(0).indexOf("function experiment(T,corpora)")).split(" // Explicit independently written calendar table")[0]+"\nreturn {propose,verify};\n}\nreturn experiment(T);")(T);
}
function experiment(T){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),clone=x=>JSON.parse(JSON.stringify(x));
 const dates=["2026-11-23","2026-11-24","2026-11-25","2026-11-26"],anchor={id:"a",date:dates[0],qualified:true,allowed:true},anchors={a:anchor},policy="monday-week@1";
 const sources={a1:{text:"本周三",allowed:true},a2:{text:"本周四",allowed:true},b1:{text:"本周二",allowed:true},b2:{text:"本周四",allowed:true},c1:{text:"本周四",allowed:true}};
 const make=(root,version,source)=>({receipt:T.propose(sources[source].text,anchor,source,root,version,policy),expected:{root,version,source,anchorId:"a",policy}});
 const ra=make("A",1,"a1"),ra2=make("A",2,"a2"),rb=make("B",1,"b1"),rb2=make("B",2,"b2"),rc=make("C",1,"c1");
 function project(request,ss,aa){
  const {capacity,records,covered}=request;
  if(!covered||capacity.length!==4||capacity.some(x=>!Number.isInteger(x)||x<0||x>2)||records.length>3||new Set(records.map(x=>x.expected.root)).size!==records.length)return null;
  let jobs=[];
  for(let j of records){
   if(!j.qualified||!Number.isInteger(j.hours)||j.hours<0||j.hours>3||!T.verify(j.receipt,ss,aa,j.expected)||j.receipt.value.kind!=="DATE")return null;
   const r=dates.indexOf(j.release),d=dates.indexOf(j.receipt.value.date);
   if(r<0||d<r)return null;
   jobs.push({id:j.expected.root,r,d,h:j.hours});
  }return jobs
 }
 function bottleneck(jobs,cap){
  for(let l=0;l<4;l++)for(let r=l;r<4;r++){
   let xs=jobs.filter(j=>j.r>=l&&j.d<=r),demand=xs.reduce((s,j)=>s+j.h,0),supply=cap.slice(l,r+1).reduce((s,v)=>s+v,0);
   if(demand>supply)return {from:l,to:r,ids:xs.map(x=>x.id),demand,supply,shortfall:demand-supply};
  }return null
 }
 // Preemptible identical unit work; EDF schedules earliest deadline among released unfinished jobs.
 function edf(jobs,cap){
  let pending=jobs.map(j=>({...j,left:j.h})),schedule=cap.map(()=>[]);
  for(let day=0;day<4;day++){
   for(let n=0;n<cap[day];n++){
    let j=pending.filter(j=>j.r<=day&&day<=j.d&&j.left>0).sort((a,b)=>a.d-b.d||a.id.localeCompare(b.id))[0];
    if(j){j.left--;schedule[day].push(j.id)}
   }
   if(pending.some(j=>j.d===day&&j.left>0))return {status:"INFEASIBLE",witness:bottleneck(jobs,cap),authority:"NONE"};
  }
  return {status:"FEASIBLE",schedule,authority:"NONE"};
 }
 // Separate direct search over individual available slots, with idle option.
 function oracle(jobs,cap){
  let slots=cap.flatMap((n,d)=>Array(n).fill(d)),left=jobs.map(j=>j.h);
  function go(k){
   if(left.every(x=>x===0))return true;
   if(k===slots.length)return false;
   let day=slots[k];
   if(go(k+1))return true;
   for(let i=0;i<jobs.length;i++)if(left[i]>0&&jobs[i].r<=day&&day<=jobs[i].d){
    left[i]--;let yes=go(k+1);left[i]++;if(yes)return true
   }return false
  }
  return go(0)
 }
 function checkSchedule(z,jobs,cap){
  if(z.status==="INFEASIBLE"){const w=z.witness;return !!w&&w.shortfall>0&&w.demand>w.supply&&w.supply===cap.slice(w.from,w.to+1).reduce((s,x)=>s+x,0)&&w.demand===jobs.filter(j=>j.r>=w.from&&j.d<=w.to).reduce((s,j)=>s+j.h,0)}
  let counts=Object.fromEntries(jobs.map(j=>[j.id,0]));
  for(let [d,arr] of z.schedule.entries()){if(arr.length>cap[d])return false;for(let id of arr){let j=jobs.find(x=>x.id===id);if(!j||d<j.r||d>j.d)return false;counts[id]++}}
  return jobs.every(j=>counts[j.id]===j.h)
 }
 function run(req,ss=sources,aa=anchors){
  let jobs=project(req,ss,aa);return jobs?edf(jobs,req.capacity):{status:"UNKNOWN_INPUT",authority:"NONE"}
 }
 function record(r,h,release){return {...r,hours:h,release:dates[release],qualified:true}}
 const caps=[[1,1,1,1],[2,0,2,0],[0,2,0,2],[1,0,1,2],[0,0,2,2],[2,2,0,0],[0,1,1,0],[2,1,1,2],[0,0,0,0],[1,2,0,1],[2,0,0,2],[1,1,0,2]];
 let out={pairedScenarios:0,solverChecks:0,scheduleCertificates:0,conflictCertificates:0,aggregateFalseFeasible:0,oldMandatoryFeasible:0,newMandatoryFeasible:0,extensionRescuedMandatory:0,extensionReducedFrontier:0,extensionIncreasedFrontier:0,optionalChecks:0,staleReceiptRejected:0,sourceUnknown:0,controls:0,witness:null,opportunityExample:null};
 for(let cap of caps)for(let ha of [1,2,3])for(let hb of [1,2,3])for(let b of [rb,rb2])for(let ar of [0,1]){
  const req={covered:true,capacity:cap,records:[record(ra,ha,ar),record(b,hb,1)]},rev={...req,records:[record(ra2,ha,ar),req.records[1]]};
  const frontier=[];
  for(let q of [req,rev]){
   let best=null;
   for(let hc=0;hc<=3;hc++){
    let r={...q,records:[...q.records,record(rc,hc,2)]},jobs=project(r,sources,anchors),z=run(r);
    ck(jobs&&z.status!=="UNKNOWN_INPUT"&&((z.status==="FEASIBLE")===oracle(jobs,cap)),"oracle");
    ck(checkSchedule(z,jobs,cap),"certificate");out.solverChecks++;out.optionalChecks++;
    if(z.status==="FEASIBLE"){best=hc;out.scheduleCertificates++}
    else {out.conflictCertificates++;if(jobs.reduce((s,j)=>s+j.h,0)<=cap.reduce((s,x)=>s+x,0)){out.aggregateFalseFeasible++;out.witness??={capacity:cap,jobs,witness:z.witness}}}
   }
   frontier.push(best);
  }
  out.pairedScenarios++;
  const [old,next]=frontier;out.oldMandatoryFeasible+=+(old!==null);out.newMandatoryFeasible+=+(next!==null);
  out.extensionRescuedMandatory+=+(old===null&&next!==null);
  out.extensionReducedFrontier+=+(old!==null&&(next===null||next<old));
  if(old!==null&&next!==null&&next>old){out.extensionIncreasedFrontier++;out.opportunityExample??={capacity:cap,oldJobs:project(req,sources,anchors),revisedJobs:project(rev,sources,anchors),oldExtraHours:old,newExtraHours:next}}
  ck(old===null||next!==null&&next>=old,"relaxation monotonicity");
  let stale={...rev,records:[{...rev.records[0],receipt:ra.receipt},rev.records[1]]};
  ck(run(stale).status==="UNKNOWN_INPUT","stale");out.staleReceiptRejected++;
  ck(run(rev,{...sources,a2:{...sources.a2,allowed:false}}).status==="UNKNOWN_INPUT","source");out.sourceUnknown++;
 }
 let req={covered:true,capacity:[1,1,1,1],records:[record(ra,2,0),record(rb,1,1)]};
 for(let t of [()=>out.pairedScenarios===432,()=>out.solverChecks===3456,()=>out.extensionReducedFrontier===0,()=>out.scheduleCertificates+out.conflictCertificates===out.solverChecks,()=>out.aggregateFalseFeasible>0,()=>run({...req,covered:false}).status==="UNKNOWN_INPUT",()=>run({...req,records:[req.records[0],req.records[0]]}).status==="UNKNOWN_INPUT",()=>run(req,sources,{a:{...anchor,allowed:false}}).status==="UNKNOWN_INPUT",()=>run({...req,records:[{...req.records[0],qualified:false},req.records[1]]}).status==="UNKNOWN_INPUT",()=>run({...req,capacity:[1,1,-1,1]}).status==="UNKNOWN_INPUT",()=>run({...req,records:[{...req.records[0],release:dates[3]},req.records[1]]}).status==="UNKNOWN_INPUT"]){ck(t(),"control "+out.controls);out.controls++}
 return out
}
console.log(JSON.stringify(experiment(load(docs)),null,2));
```
## 实测
```json
{
  "pairedScenarios": 432,
  "solverChecks": 3456,
  "scheduleCertificates": 414,
  "conflictCertificates": 3042,
  "aggregateFalseFeasible": 522,
  "oldMandatoryFeasible": 106,
  "newMandatoryFeasible": 137,
  "extensionRescuedMandatory": 31,
  "extensionReducedFrontier": 0,
  "extensionIncreasedFrontier": 0,
  "optionalChecks": 3456,
  "staleReceiptRejected": 432,
  "sourceUnknown": 432,
  "controls": 11,
  "witness": {
    "capacity": [
      1,
      1,
      1,
      1
    ],
    "jobs": [
      {
        "id": "A",
        "r": 1,
        "d": 2,
        "h": 1
      },
      {
        "id": "B",
        "r": 1,
        "d": 1,
        "h": 1
      },
      {
        "id": "C",
        "r": 2,
        "d": 3,
        "h": 2
      }
    ],
    "witness": {
      "from": 1,
      "to": 3,
      "ids": [
        "A",
        "B",
        "C"
      ],
      "demand": 4,
      "supply": 3,
      "shortfall": 1
    }
  },
  "opportunityExample": null
}
```
后续：结合多资源与不可拆分任务、实际日历可用性和延期成本；开放语言的事件/期限/工作量识别及独立数据仍需验证。产品轨维护唯一交接，正式开发另获授权。
