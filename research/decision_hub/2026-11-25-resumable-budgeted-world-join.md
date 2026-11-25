# 联合情景计算的预算分段、续算及提前停止证书
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / EXACT_FINITE_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 879ef117e9c6978482784eb81006bdc1468b5298；Draft #62固定候选 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期10提交、14开放PR、v3.2及同步规程前22行、唯一产品交接前22行blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。检索budget/anytime/truncation/bound/stopping/approximation；审阅R48 32aab8f9c28631a51aaa69cf7c74f835d8a9a36d、R87 cbf740574b8e07734a78d6fb5a8d178005e513ab、R47 a78b48c24819dfd729d55a3068fe4b481c116456、R43 912e740595ce7759d55829b5dead0093fd0b5399合同前段。已有后悔值界、预算闭包、有限搜索和观察支持；本轮只扩展上一轮实际联合情景接口，新增索引连接、可续算状态、未计算/无证据分离和混合结论提前停止。非新通用优化理论，全库去重有限。
## 固定资产
research/decision_hub/2026-11-25-world-bound-multistage-result-join.md @ 879ef117e9c6978482784eb81006bdc1468b5298 blob af4daae1aaeee5a36a140d8a0f272a48c064368b；
research/decision_hub/2026-11-25-recurring-benefit-feasibility-threshold.md @ 45934aedcc37ad2bae1c56cee4dce4959befeccc blob 9c27c104e3be8f18eebc18f5ad8a0e10e2940fcf。连接器身份核对，实际提取原group/join及threshold/feasible，未重写或声称原生接入。
## 合同与推导
同前轮完整有限联合情景H、可信当前输入端口、固定目标/约束/方法/来源/授权；两个端口为按相同值分组且情景内单值的必要收益阈值及假设收益。预处理验证每端口非重叠、合法支持及值，将世界索引至所属组，按组对聚合真正共同支持的任务；每个世界至多一个组对，故与全部组对求交等价，无需比较空交。缺失端口的世界保留为M，计算任务已知但尚未执行的世界为U。每次最多执行cap个非空组对谓词，按组覆盖基数降序及掩码排序，未读取其通过/失败结果选择顺序，不代表概率或实际重要性。每组恰执行一次，P/F为已确认条件通过/失败支持。P、F、U、M互斥且并集H；每次执行只将U的一组转入P或F，故下界单调收紧。在H及端口合同有效时，最终通过情景数介于|P|和|H|-|F|之间，失败数对称；这是枚举数量界，不是概率或真实风险。P和F均非空即可证明已知情景存在分歧，即使未算或缺证据仍有见证；全通过/全失败须P=H或F=H，不能用当前前缀替代。提前停止只针对存在分歧的询问，不保证完整数值、推荐或实际可行策略；完整输出请求继续计算。若整个域覆盖不可信则UNKNOWN_COVERAGE，空域CONFLICT。所有结果authority NONE。当前续算是可信内存可变对象，epoch模拟单调版本检查；外部状态、并发、授权撤回、持久化、完整性认证、内存释放及真正设备预算未实现。预处理、原模型、索引、排序、输出与参照不计入cap；cap只计组对谓词，不能称全请求资源上限或设备速度。非空组对数<=|H|，前处理O(|H|+组支持遍历)，当前八位实现固定，不直接推广无限域。停止/继续由分析目的及真实资源约束决定，硬约束与必要风险确认不能省略。
## 实验
复用上一轮48参数组合×8情景、255非空域×2端口覆盖=24480组，不是新增独立样本；逐个真实执行原阈值及直接行动枚举核验384点；每组0预算及随后每步1预算续算，逐前缀核对支持分区、通过/失败计数界、单调性、全域结论，终点对照原join。另以允许提前确认混合结论的方式执行，计省略的组对；priorCartesianComparisons为原join实际尝试，jobComparisons为新算法最终执行的非空组对数，仅比较谓词任务及原组对尝试计数，不是相同CPU成本或速度。naivePrefixFalseCertainty计仅依据已算单一方向、仍有未算或缺证据的前缀（未获全域保证，未必与真实终点相反）。14控制；同研究者、共享合同，非独立验收。自行选择排序、预算和停止目标。无真实预测、个人数据、训练、原生API、设备测量、CI请求、合并、部署、费用或冻结变化。
## 复算
按固定两份报告全文置于docs，Node标准JS，仅执行已审查自有代码。
```js
function load(docs){
 const s=docs[0].split("```js\n")[1].split("\n```")[0];
 const P=Function(s.split("function experiment(P)")[0]+"\nreturn load;")()(docs[1]);
 const J=Function("P",s.slice(s.indexOf("function experiment(P)")).split(" let o={settings:")[0]+"\nreturn {group,join};\n}\nreturn experiment(P);")(P);
 return {P,J}
}
function experiment({P,J}){
 const ck=(v,m)=>{if(!v)throw Error(m)},W=[0,1,2,3,4,5,6,7],INF="NO_FINITE_THRESHOLD";
 const pop=m=>W.filter(w=>m&(1<<w)).length;
 // Trusted in-memory planning. Index each world once; identical group pair is one task.
 function prepare(T,G,scope,epoch,covered=true){
  if(!covered)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  if(!scope)return {status:"CONFLICT",authority:"NONE"};
  function index(rows,threshold){
   let ix=Array(8).fill(-1),mask=0;
   for(let i=0;i<rows.length;i++){
    let {value,support}=rows[i];
    if(!Number.isInteger(support)||support<=0||support>255||(support&~scope)||(mask&support)||!(Number.isSafeInteger(value)&&value>=0||threshold&&value===INF))return null;
    mask|=support;for(let w of W)if(support&(1<<w))ix[w]=i;
   }return {ix,mask};
  }
  let t=index(T,true),g=index(G,false);if(!t||!g)return {status:"INVALID_PORT",authority:"NONE"};
  let known=t.mask&g.mask,jobs=new Map();
  for(let w of W)if(known&(1<<w)){
   let i=t.ix[w],j=g.ix[w],k=i+":"+j;
   if(!jobs.has(k))jobs.set(k,{threshold:T[i].value,gain:G[j].value,support:0});
   jobs.get(k).support|=1<<w;
  }
  // No result or feasibility predicate is evaluated when ordering jobs.
  let tasks=[...jobs.values()].sort((a,b)=>pop(b.support)-pop(a.support)||a.support-b.support);
  return {status:"PREPARED",epoch,scope,known,tasks,cursor:0,pass:0,fail:0,authority:"NONE"};
 }
 function advance(s,cap,epoch,stopMixed=false){
  if(s.status!=="PREPARED"||s.epoch!==epoch)return {status:"STALE_OR_INVALID",authority:"NONE"};
  if(!Number.isSafeInteger(cap)||cap<0)return {status:"INVALID_BUDGET",authority:"NONE"};
  let used=0;
  while(s.cursor<s.tasks.length&&used<cap&&!(stopMixed&&s.pass&&s.fail)){
   let a=s.tasks[s.cursor++];used++;
   if(a.threshold!==INF&&a.gain>=a.threshold)s.pass|=a.support;else s.fail|=a.support;
  }
  let pending=s.known&~(s.pass|s.fail),missing=s.scope&~s.known;
  let conclusion=s.pass&&s.fail?"CONDITIONAL_MIXED":pending||missing?"UNKNOWN_GLOBAL":s.pass?"CONDITIONAL_ALL_PASS":"CONDITIONAL_ALL_FAIL";
  return {status:"CONDITIONAL_PROGRESS",authority:"NONE",pass:s.pass,fail:s.fail,pending,missing,conclusion,used,cursor:s.cursor,
   passCountBounds:[pop(s.pass),pop(s.scope&~s.fail)],failCountBounds:[pop(s.fail),pop(s.scope&~s.pass)]};
 }
 let o={settings:0,worldChecks:0,cases:0,prefixChecks:0,resumeChecks:0,fullJoinChecks:0,earlyMixed:0,earlyMixedSaved:0,partialEvidence:0,zeroBudgetKnown:0,naivePrefixFalseCertainty:0,jobComparisons:0,priorCartesianComparisons:0,controls:0,witness:null};
 for(let fee of [0,1,2])for(let ca of [1,2])for(let cb of [1,3])for(let income of [0,1])for(let da of [2,3]){
  let ps=W.map(w=>({cash:(w&1)?3:1,reserve:1,income,ca,cb,fee,busy:1,da,db:4,lag:(w&2)?2:1})),G=W.map(w=>(w&4)?2:0),T=ps.map(p=>{let v=P.threshold(p);return v.status==="CONDITIONAL"?v.minimum:INF});
  let truth=ps.map((p,w)=>P.feasible(p,G[w]));o.settings++;
  for(let w of W){ck(truth[w]===(T[w]!==INF&&G[w]>=T[w]),"threshold");o.worldChecks++}
  for(let scope=1;scope<256;scope++)for(let live of [255,85]){
   let t=J.group(T,scope),g=J.group(G,scope&live),ref=J.join(t,g,scope),s=prepare(t,g,scope,1),k=s.tasks.length;
   let p=0,f=0;for(let w of W)if(scope&(1<<w)){if(truth[w])p|=1<<w;else f|=1<<w}
   let last=null;o.cases++;o.priorCartesianComparisons+=ref.used;o.jobComparisons+=k;o.partialEvidence+=+(ref.missing!==0);
   for(let n=0;n<=k;n++){
    let z=advance(s,n===0?0:1,1);
    ck((z.pass&p)===z.pass&&(z.fail&f)===z.fail&&!(z.pass&z.fail)&&!(z.pending&z.missing)&&(z.pass|z.fail|z.pending|z.missing)===scope,"partition");
    ck(z.passCountBounds[0]<=pop(p)&&pop(p)<=z.passCountBounds[1]&&z.failCountBounds[0]<=pop(f)&&pop(f)<=z.failCountBounds[1],"bounds");
    if(last){ck(z.used===1&&(z.pass&last.pass)===last.pass&&(z.fail&last.fail)===last.fail&&z.passCountBounds[1]<=last.passCountBounds[1],"monotone");o.resumeChecks++}
    if(z.conclusion==="CONDITIONAL_MIXED")ck(p&&f,"mixed");
    if(z.conclusion==="CONDITIONAL_ALL_PASS")ck(p===scope,"all pass");
    if(z.conclusion==="CONDITIONAL_ALL_FAIL")ck(f===scope,"all fail");
    if((z.pass||z.fail)&&(!z.pass||!z.fail)&&(z.pending||z.missing))o.naivePrefixFalseCertainty++;
    if(n===0&&z.conclusion!=="UNKNOWN_GLOBAL")o.zeroBudgetKnown++;
    o.prefixChecks++;last=z;
   }
   ck(last.pass===ref.pass&&last.fail===ref.fail&&last.missing===ref.missing&&last.pending===0,"prior join");o.fullJoinChecks++;
   let q=prepare(t,g,scope,1),z=advance(q,k,1,true);
   if(z.conclusion==="CONDITIONAL_MIXED"&&z.pending){o.earlyMixed++;o.earlyMixedSaved+=k-z.used;o.witness??={fee,ca,cb,income,da,scope,live,k,z};}
   ck(z.conclusion==="CONDITIONAL_MIXED"?p&&f:true,"early");
  }
 }
 let t=[{value:1,support:1},{value:0,support:2}],g=[{value:0,support:1},{value:2,support:2}],s=prepare(t,g,3,7);
 for(let v of [o.settings===48,o.cases===24480,o.fullJoinChecks===o.cases,o.zeroBudgetKnown===0,o.earlyMixed>0,o.naivePrefixFalseCertainty>0,advance(s,0,7).pending===3,advance(s,1,8).status==="STALE_OR_INVALID",s.cursor===0,advance(s,-1,7).status==="INVALID_BUDGET",prepare([...t,t[0]],g,3,7).status==="INVALID_PORT",prepare(t,[{value:INF,support:3}],3,7).status==="INVALID_PORT",prepare(t,g,3,7,false).status==="UNKNOWN_COVERAGE",prepare([],[],0,7).status==="CONFLICT"]){ck(v,"control "+o.controls);o.controls++}
 return o;
}
console.log(JSON.stringify(experiment(load(docs)),null,2));
```
## 实测
```json
{
  "settings": 48,
  "worldChecks": 384,
  "cases": 24480,
  "prefixChecks": 79168,
  "resumeChecks": 54688,
  "fullJoinChecks": 24480,
  "earlyMixed": 4609,
  "earlyMixedSaved": 6447,
  "partialEvidence": 11520,
  "zeroBudgetKnown": 0,
  "naivePrefixFalseCertainty": 33466,
  "jobComparisons": 54688,
  "priorCartesianComparisons": 77096,
  "controls": 14,
  "witness": {
    "fee": 0,
    "ca": 1,
    "cb": 1,
    "income": 0,
    "da": 2,
    "scope": 7,
    "live": 255,
    "k": 3,
    "z": {
      "status": "CONDITIONAL_PROGRESS",
      "authority": "NONE",
      "pass": 2,
      "fail": 1,
      "pending": 4,
      "missing": 0,
      "conclusion": "CONDITIONAL_MIXED",
      "used": 2,
      "cursor": 2,
      "passCountBounds": [
        1,
        2
      ],
      "failCountBounds": [
        1,
        2
      ]
    }
  }
}
```
后续：与已有R107事务和R125失效机制连接；独立轨验证真实原生端口、取消、续算、外部状态篡改及设备资源；产品轨维护唯一交接。本轮不授权正式版本开发。