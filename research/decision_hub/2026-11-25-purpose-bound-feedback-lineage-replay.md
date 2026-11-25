# 自主认知专项累计第109轮候选：用途限定的反馈依赖与选择性重放
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_PLATFORM_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 2fdf92bb942f9b8bb1c054ac89056e5760c02ba4。核对近12提交、13开放PR（#61待审）、v3.2前15行及此前全文、唯一交接前25行、R108前20行、R54前14行、R18 README前25行、R101前20行及R18实际源码/配置。未重验全部历史隐私研究。R18已有全局撤回和重放，R54已有同用途参数依赖，R101已有长期规划账本，R108已有单条恢复资格。本轮新增多用途、逐记录及历史组合预测间接依赖核验；不重复执行全局撤回或长期规划DP。

## 固定资产
research/decision_hub/2026-11-24-feedback-replay-and-rollback/probe.js c07a499cfc0d3ab274fcb0a6e16abe71fab1f3f6
research/decision_hub/2026-11-24-feedback-replay-and-rollback/config.json fb4ec1cee38443c41d9f3fb7e90f616dafe78832
R108 75deb196da9b81a4d872ac29187101235194ac1c；R101 907f12081ddce7bb752ae498bcf21f4b4b218a60；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。

## 合同
R18真实研究apply生成三次预测和反馈交错序列（每次反馈后才发布下次预测）；复用原weights及brute路径枚举。每个专家概率向量p_i与实际反馈y_i各有独立合成根，共6根。固定专家概率向量人为给定，明确不依赖之前反馈或用户其他数据；真实自主模型若用过历史个人数据必须记录其实际训练/推理依赖，本轮不能假定独立。组合预测q_i由当前权重及p_i生成，保守依赖本次p_i及先前全部已用于更新的p_j/y_j；分数依赖q_i及当前y_i。固定共享可能使某些数值巧合不变，不能因此自动解除依赖。当前用途拆分为历史预测/复盘查看（archive）与本地反馈学习（learn），分别由可信宿主6位资格掩码提供，独立授权，不自动继承或放宽。掩码仅表示该用途每个确切原始记录当前获准使用，未实现真实用户确认、代次、删除、身份或恢复事务。全部是模拟开发数据，本轮执行固定既有算法数值重放，没有训练新的模型或权重文件，不能将模拟状态当成实际个人学习。

旧q冻结且不在新权重下重写，只有全部历史依赖获准才能显示；评分另需该事件实际标签获准。学习重放仅保留具有合格p_i和y_i的事件，保留原始反馈接收槽位顺序，使用R18固定共享规则从均匀初值重算；不会把未选择行动或缺失标签当作观察结果。新的权重可与旧历史不可见预测分离，后续真实发布须独立绑定重放使用的根集合、算法版本、当前授权及事务。实验临时replay对象内保留原q供R18结构兼容，weights不读q；原状态仍在内存供实验参照核对，不实现物理删除、最小数据驻留、真实授权阻断或保留审计的合法性。实际应用需要避免载入或保留已撤回内容，不能把过滤输出当数据擦除或机器遗忘保证。历史视图不生成任何替代预测；本轮不执行真实长期规划、原生入口、设备或跨端恢复。该事件过滤策略为研究者选定，未证明真实预测改善或对旧连续时间损失界的保持。

## 实验
两个既有版本×8标签组合×64历史资格掩码×64学习资格掩码。历史资格用直接逐项前序条件核对，学习资格用独立显式条件核对，权重以原R18隐专家路径枚举核对（两计算共享固定规则和同研究者夹具，非独立验收）。naiveHistoryExposure/naiveScoreExposure是只核本事件原始根、忽略先前反馈间接影响的构造基线错误显示资格次数；不是实际平台泄露或错误率。historyWithoutLearning/learningWithoutHistory为用途条件不同的事件数（按预测历史可见性），不能推断真实用户偏好。原始预测冻结检查不意味着撤权后可保留真实历史。全部合成材料为ChatGPT研发辅助原创开发夹具，非真人、训练或独立留出。无新增外部事实、费用、训练、Codex、CI、生产修改、合并、部署或冻结变更。

## 可复算代码
从上述固定版本取得两个自有源码文件，分别置为docs[0].content、docs[1].content。只加载已审查的项目自有源码，禁止执行任意网络内容。Node标准JS。
```js
const cfg=JSON.parse(docs[1].content);
function load(src){return Function(src.replace("const config=require('./config.json');","").split("console.log(JSON.stringify(run(config)")[0]+"\nreturn {initial,apply,weights,score,brute,canon};")()}
const R=load(docs[0].content);
function experiment(R,cfg){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),allows=(mask,need)=>(mask&need)===need;
 const ps=[[.8,.25],[.3,.75],[.65,.4]];
 const pbit=i=>1<<i,ybit=i=>1<<(3+i);
 function original(version,bits){
  let s=R.initial(),t=0;
  function send(e,owner=false){let z=R.apply(s,{...e,generation:s.generation},++t,cfg,owner);ck(["GRANTED","ACCEPTED"].includes(z.code),"apply "+z.code);s=z.s}
  send({id:"grant",type:"grant"},true);send({id:"activate",type:"activate",version},true);
  let lineage=[],learned=0;
  for(let i=0;i<3;i++){
   let event="e"+i,due=t+2;
   send({id:"i"+i,type:"issue",epoch:s.epoch,scope:cfg.scope,event,due,p:ps[i]});
   lineage.push({p:pbit(i),q:pbit(i)|learned,y:ybit(i)});
   send({id:"f"+i,type:"feedback",epoch:s.epoch,scope:cfg.scope,event,revision:1,priorRevision:0,observed:due,y:(bits>>i)&1});
   learned|=pbit(i)|ybit(i);
  }
  return {s,lineage}
 }
 function filtered(s,L,learn,archive){
  const obs=s.observations.filter((o,i)=>allows(learn,L[i].p|L[i].y));
  const ids=new Set(obs.map(o=>o.event));
  // transient internal replay state, never exported; q unused by weights().
  const replay={...s,observations:obs,receipts:s.receipts.filter(f=>ids.has(f.event))};
  const history=[],scores=[];
  for(let i=0;i<L.length;i++){
   if(allows(archive,L[i].q))history.push(s.receipts[i].event);
   if(allows(archive,L[i].q|L[i].y))scores.push(s.receipts[i].event);
  }
  const w=R.weights(replay,cfg);
  const replayRef=R.brute(replay,cfg);
  return {history,scores,learned:obs.map(o=>o.event),w,replayRef};
 }
 let o={originalSequences:0,cases:0,historyChecks:0,scoreChecks:0,learningChecks:0,weightChecks:0,maxError:0,historyRetained:0,scoresRetained:0,learnedEvents:0,naiveHistoryExposure:0,naiveScoreExposure:0,learningWithoutHistory:0,historyWithoutLearning:0,weightChanged:0,immutability:0,controls:0,example:null};
 for(const version of Object.keys(cfg.versions))for(let bits=0;bits<8;bits++){
  const {s,lineage:L}=original(version,bits),old=R.canon(s),w0=R.weights(s,cfg);o.originalSequences++;
  for(let archive=0;archive<64;archive++)for(let learn=0;learn<64;learn++){
   const z=filtered(s,L,learn,archive);o.cases++;
   const h=[],scores=[],l=[];
   for(let i=0;i<3;i++){
    const ownP=Boolean(archive&pbit(i)),ownY=Boolean(archive&ybit(i));
    let before=true;for(let j=0;j<i;j++)before=before&&Boolean(archive&pbit(j))&&Boolean(archive&ybit(j));
    if(ownP&&before)h.push("e"+i);
    if(ownP&&ownY&&before)scores.push("e"+i);
    if((learn&pbit(i))&&(learn&ybit(i)))l.push("e"+i);
    if(ownP&&!before)o.naiveHistoryExposure++;
    if(ownP&&ownY&&!before)o.naiveScoreExposure++;
   }
   ck(eq(z.history,h)&&eq(z.scores,scores)&&eq(z.learned,l),"purpose reference");
   o.historyChecks+=3;o.scoreChecks+=3;o.learningChecks+=3;
   const err=Math.max(...z.w.map((v,i)=>Math.abs(v-z.replayRef[i])));ck(err<1e-12,"path enumeration");o.maxError=Math.max(o.maxError,err);o.weightChecks++;
   o.historyRetained+=h.length;o.scoresRetained+=scores.length;o.learnedEvents+=l.length;
   o.learningWithoutHistory+=l.filter(x=>!h.includes(x)).length;o.historyWithoutLearning+=h.filter(x=>!l.includes(x)).length;
   if(z.w.some((v,i)=>Math.abs(v-w0[i])>1e-12))o.weightChanged++;
   ck(R.canon(s)===old,"frozen original");o.immutability++;
   if(!o.example&&version===Object.keys(cfg.versions)[0]&&bits===5&&archive===55&&learn===55)o.example={version,bits,archive,learn,originalWeights:w0,newWeights:z.w,history:h,scores,learned:l,frozenQ:s.receipts.map(f=>f.q)};
  }
  for(const [a,b,h,l] of [[63,63,3,3],[0,63,0,3],[63,0,3,0],[55,55,1,2],[0,0,0,0]]){
   let z=filtered(s,L,b,a);ck(z.history.length===h&&z.learned.length===l,"control");if(!b)ck(eq(z.w,[.5,.5]),"reset");o.controls++;
  }
 }
 return o
}
console.log(JSON.stringify(experiment(R,cfg),null,2));
```

## 实测
```json
{
  "originalSequences": 16,
  "cases": 65536,
  "historyChecks": 196608,
  "scoreChecks": 196608,
  "learningChecks": 196608,
  "weightChecks": 65536,
  "maxError": 2.220446049250313e-16,
  "historyRetained": 43008,
  "scoresRetained": 21504,
  "learnedEvents": 49152,
  "naiveHistoryExposure": 55296,
  "naiveScoreExposure": 27648,
  "learningWithoutHistory": 38400,
  "historyWithoutLearning": 32256,
  "weightChanged": 64512,
  "immutability": 65536,
  "controls": 80,
  "example": {
    "version": "v1",
    "bits": 5,
    "archive": 55,
    "learn": 55,
    "originalWeights": [
      0.8603785453312742,
      0.13962145466872578
    ],
    "newWeights": [
      0.7714334470989761,
      0.2285665529010239
    ],
    "history": [
      "e0"
    ],
    "scores": [],
    "learned": [
      "e1",
      "e2"
    ],
    "frozenQ": [
      0.525,
      0.4189285714285713,
      0.6119161032575291
    ]
  }
}
```
后续：将用途依赖记录连接到长期计划和R108恢复原型，区别真实权限、数学准备、数据保留、反馈学习和历史解释资格。独立验收轨保留未见案例，产品轨维护唯一交接。正式工程另获授权。
