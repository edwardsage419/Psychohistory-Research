# 自主学习：冻结事前选择集合、历史假说过滤及反馈质量诊断
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_PREQUENTIAL_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线及去重
同一手动轮第三阶段，起点main 229a69a16874c564221e633ed80acda3a712d256，沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、固定交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。实际读取并执行固定自有研究源码：
research/decision_hub/2026-11-26-partial-lexicographic-goal-order-witnesses.md 56ccc94a47a135670b670e26e65c99503740e7e5
research/decision_hub/2026-11-26-choice-context-preference-identification-and-retraction.md 8f5190df8333d19b909ad1690774beb20b580317
前阶段冲突核与变化假说blob 3339c7325186ac97f242f469d617f9c8c76f1f5b；R18反馈重放、R109用途、冻结配对预测和延迟序贯评价已存在，不重复Brier、权重更新或概率显著性检验。此轮新增明确选择模型下的集合值事前预测诊断、不同历史过滤规则的覆盖和集合规模、显式偏好epoch与隐性变化对结果的区别。局部查重非全库证明。
## 合同
六二元目标、已明确接受词典序且完整菜单、同主体和用途，所有资格及选择理由由合成可信夹具假定；真实行为通常不满足，不能套用所有人生选择。冻结三种预设规则：仅显式优先边，不用历史；全部当前epoch合格已获知选择约束；最近两条合格选择约束（按原事件序而非获知序）。固定规则对兼容的全部优先顺序求下一菜单的可能胜者集合；空顺序集显式弃答，不回填已确认偏好，不自动切换规则。仅用于评价假说过滤，非训练模型权重、参数优化或真实个人学习。最新记录版本以received<t为严格信息截止；同根撤回不回退旧记录，当前epoch外数据排除。人工更正可能错误，故最终评分仅指给定夹具当前合格标签，不能声称真值包含或正式统计认证；不自动证明真实偏好变化。历史重放只限合成且授权夹具，未实现真实删除、身份验证、签名、持久化、跨端或用途权限。
每个预测集合先冻结，再产生该事件观察。覆盖(实际选择是否属于预测集合)、集合大小、单候选错误、弃答分别计量，不合成统一价值分；空集合计一次未覆盖而另标弃答。缺失或撤回标签不填补。固定队列的总未覆盖次数下界为已观察未覆盖加缺失事件空预测集合数量，上界再允许所有缺失事件中存在未包含菜单选项的事件未覆盖；端点在允许每个未知实际选择为菜单任意一项、各事件独立补全的合同下可取。无置信区间、未来改善概率或决策结果效用。若真实结局支持、授权或菜单范围未知，应暂停相应评价。只对合成选择标签，不将预测选择正确当决策正确或真实偏好已确认。
## 实际实验
四类环境各400组、每组9次选择：固定人工顺序、第四索引期隐性顺序变化、同样变化但显式epoch更新、固定顺序下随机选择噪声；所有顺序/菜单/噪声、延迟0..3、反馈缺失、撤回及更正由研究者预设合成生成机制。固定评分截止11；实际复用前序winner/allOrders，逐期以独立按事件筛选参照核对三规则，逐历史截点重放已冻结预测。比较三规则每组覆盖/大小/单候选错误/弃答及缺失标签未覆盖上下界，保留不利结果；六边界控制。标准JS核心实际执行两次一致。数据为同研究者公开合成开发样本，非独立留出、真实用户、训练或实际模型有效性；没有根据本轮结果再选优规则或宣布升级。
```json
{
  "groups": {
    "stationary": {
      "baseline": {
        "issued": 3600,
        "observed": 2460,
        "missing": 1140,
        "covered": 2314,
        "missed": 146,
        "abstained": 0,
        "observedAbstained": 0,
        "issuedSize": 8599,
        "observedSize": 5828,
        "singletons": 722,
        "observedSingletons": 500,
        "singletonWrong": 41,
        "missLower": 146,
        "missUpper": 1188
      },
      "allHistory": {
        "issued": 3600,
        "observed": 2460,
        "missing": 1140,
        "covered": 2085,
        "missed": 375,
        "abstained": 318,
        "observedAbstained": 213,
        "issuedSize": 6654,
        "observedSize": 4533,
        "singletons": 1140,
        "observedSingletons": 783,
        "singletonWrong": 75,
        "missLower": 480,
        "missUpper": 1457
      },
      "recent2": {
        "issued": 3600,
        "observed": 2460,
        "missing": 1140,
        "covered": 2207,
        "missed": 253,
        "abstained": 149,
        "observedAbstained": 92,
        "issuedSize": 7301,
        "observedSize": 4982,
        "singletons": 1033,
        "observedSingletons": 718,
        "singletonWrong": 68,
        "missLower": 310,
        "missUpper": 1328
      }
    },
    "hiddenChange": {
      "baseline": {
        "issued": 3600,
        "observed": 2514,
        "missing": 1086,
        "covered": 2388,
        "missed": 126,
        "abstained": 0,
        "observedAbstained": 0,
        "issuedSize": 8743,
        "observedSize": 6076,
        "singletons": 663,
        "observedSingletons": 483,
        "singletonWrong": 37,
        "missLower": 126,
        "missUpper": 1118
      },
      "allHistory": {
        "issued": 3600,
        "observed": 2514,
        "missing": 1086,
        "covered": 1899,
        "missed": 615,
        "abstained": 524,
        "observedAbstained": 350,
        "issuedSize": 6370,
        "observedSize": 4452,
        "singletons": 971,
        "observedSingletons": 699,
        "singletonWrong": 139,
        "missLower": 789,
        "missUpper": 1657
      },
      "recent2": {
        "issued": 3600,
        "observed": 2514,
        "missing": 1086,
        "covered": 2173,
        "missed": 341,
        "abstained": 155,
        "observedAbstained": 108,
        "issuedSize": 7356,
        "observedSize": 5086,
        "singletons": 957,
        "observedSingletons": 692,
        "singletonWrong": 105,
        "missLower": 388,
        "missUpper": 1371
      }
    },
    "explicitEpoch": {
      "baseline": {
        "issued": 3600,
        "observed": 2528,
        "missing": 1072,
        "covered": 2409,
        "missed": 119,
        "abstained": 0,
        "observedAbstained": 0,
        "issuedSize": 8707,
        "observedSize": 6139,
        "singletons": 670,
        "observedSingletons": 467,
        "singletonWrong": 33,
        "missLower": 119,
        "missUpper": 1111
      },
      "allHistory": {
        "issued": 3600,
        "observed": 2528,
        "missing": 1072,
        "covered": 2367,
        "missed": 161,
        "abstained": 43,
        "observedAbstained": 29,
        "issuedSize": 8089,
        "observedSize": 5708,
        "singletons": 833,
        "observedSingletons": 585,
        "singletonWrong": 47,
        "missLower": 175,
        "missUpper": 1167
      },
      "recent2": {
        "issued": 3600,
        "observed": 2528,
        "missing": 1072,
        "covered": 2371,
        "missed": 157,
        "abstained": 36,
        "observedAbstained": 26,
        "issuedSize": 8129,
        "observedSize": 5733,
        "singletons": 820,
        "observedSingletons": 574,
        "singletonWrong": 46,
        "missLower": 167,
        "missUpper": 1162
      }
    },
    "choiceNoise": {
      "baseline": {
        "issued": 3600,
        "observed": 2484,
        "missing": 1116,
        "covered": 2118,
        "missed": 366,
        "abstained": 0,
        "observedAbstained": 0,
        "issuedSize": 8582,
        "observedSize": 5902,
        "singletons": 707,
        "observedSingletons": 486,
        "singletonWrong": 110,
        "missLower": 366,
        "missUpper": 1414
      },
      "allHistory": {
        "issued": 3600,
        "observed": 2484,
        "missing": 1116,
        "covered": 1496,
        "missed": 988,
        "abstained": 984,
        "observedAbstained": 651,
        "issuedSize": 5441,
        "observedSize": 3823,
        "singletons": 829,
        "observedSingletons": 571,
        "singletonWrong": 151,
        "missLower": 1321,
        "missUpper": 2075
      },
      "recent2": {
        "issued": 3600,
        "observed": 2484,
        "missing": 1116,
        "covered": 1714,
        "missed": 770,
        "abstained": 621,
        "observedAbstained": 411,
        "issuedSize": 6294,
        "observedSize": 4378,
        "singletons": 885,
        "observedSingletons": 609,
        "singletonWrong": 146,
        "missLower": 980,
        "missUpper": 1848
      }
    }
  },
  "graphs": 1600,
  "predictions": 43200,
  "referenceChecks": 43200,
  "historicalChecks": 14400,
  "withdrawalChecks": 1381,
  "correctionChecks": 1283,
  "lateFeedbackExcluded": 19989,
  "epochExcluded": 6669,
  "controls": 6,
  "example": null
}
```
## 接入
正式系统应将用户主动确认的偏好、有限选择假说、冻结预测及真实观察分开存储，使用单独授权和当前来源版本；真实偏好学习须另经授权，评价应独立留出并审查适用性、实际认知负担和结果反馈，不能以选择命中率替代决策质量。此次不修改生产、唯一交接、冻结、历史证据等级、PR、训练、部署、主动CI或费用；原生、真实用户、真机、独立留出未运行。研究者选定词典序、规则、时序、样本分布及评分指标。
## 复算
固定两份报告按顺序传入；仅执行已审查自有源码。Node包装未执行，连接器核心已运行。
```js
const code=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0]);
const make=Function(code[0].split(" const out={graphs:")[0]+"\nreturn {closure,orderOK,winner};\n}\nreturn experiment();");
const make2=Function("make",code[1].slice(code[1].indexOf("function study(make){")).split(" const host={subject:")[0]+"\nreturn {solve,allOrders,clauses};\n}\nreturn study(make);");
function experiment(make,make2){
 const R=make(),S=make2(make),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),N=6,T=9;
 const copy=x=>JSON.parse(JSON.stringify(x)),sort=x=>[...x].sort((a,b)=>a-b);
 let seed=20261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function orders(p){return S.allOrders(p)}
 const winners=(os,menu)=>sort([...new Set(os.map(o=>R.winner(o,menu)))]);
 function recordsAsOf(log,t,epoch){
  const m=new Map();
  for(let r of log)if(r.received<t){const old=m.get(r.id);if(!old||old.version<r.version)m.set(r.id,r)}
  return [...m.values()].filter(r=>r.epoch===epoch&&r.allowed&&r.qualified&&r.choice!==null).sort((a,b)=>a.id-b.id);
 }
 // These are fixed hypothesis filters, not trained parameters or updated explicit preferences.
 function predict(os,menu,prior,mode){
  let used=mode==="baseline"?[]:mode==="recent2"?prior.slice(-2):prior;
  let keep=os.filter(o=>used.every(r=>R.winner(o,r.menu)===r.choice));
  return {set:winners(keep,menu),abstain:!keep.length,compatible:keep.length,dependencies:used.map(r=>[r.id,r.version]),authority:"NONE"};
 }
 function reference(os,menu,log,t,epoch,mode){
  let active=[];
  for(let i=0;i<t;i++){
   const r=log.filter(v=>v.id===i&&v.received<t).sort((a,b)=>b.version-a.version)[0];
   if(r&&r.epoch===epoch&&r.allowed&&r.qualified&&r.choice!==null)active.push(r);
  }
  if(mode==="baseline")active=[];if(mode==="recent2")active=active.slice(-2);
  let possible=new Set(),count=0;
  for(let o of os){if(active.some(r=>R.winner(o,r.menu)!==r.choice))continue;count++;possible.add(R.winner(o,menu))}
  return {set:sort(possible),abstain:!count,compatible:count,dependencies:active.map(r=>[r.id,r.version]),authority:"NONE"};
 }
 const groups=["stationary","hiddenChange","explicitEpoch","choiceNoise"],modes=["baseline","allHistory","recent2"],stat=()=>({issued:0,observed:0,missing:0,covered:0,missed:0,abstained:0,observedAbstained:0,issuedSize:0,observedSize:0,singletons:0,observedSingletons:0,singletonWrong:0,missLower:0,missUpper:0});
 const out={groups:{},graphs:0,predictions:0,referenceChecks:0,historicalChecks:0,withdrawalChecks:0,correctionChecks:0,lateFeedbackExcluded:0,epochExcluded:0,controls:0,example:null};
 for(let group of groups){
  out.groups[group]=Object.fromEntries(modes.map(m=>[m,stat()]));
  for(let g=0;g<400;g++){
   let h=[0,1,2,3,4,5];for(let i=N-1;i>0;i--){let j=rnd(i+1);[h[i],h[j]]=[h[j],h[i]]}
   let edges=[];for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(rnd(8)===0)edges.push([h[i],h[j]]);
   const os=orders(R.closure(edges)),h2=os[rnd(os.length)],log=[],events=[],frozen=[];
   for(let t=0;t<T;t++){
    const menu=sort([...new Set(Array.from({length:3+rnd(5)},()=>rnd(64)))]);
    const epoch=group==="explicitEpoch"&&t>=4?2:1;
    const p=group==="hiddenChange"||group==="explicitEpoch"?t>=4?h2:h:h;
    let choice=R.winner(p,menu);if(group==="choiceNoise"&&rnd(4)===0)choice=menu[rnd(menu.length)];
    const prior=recordsAsOf(log,t,epoch);
    const predictions={};
    for(let m of modes){
     let z=predict(os,menu,prior,m),ref=reference(os,menu,log,t,epoch,m);ck(eq(z,ref),"prequential reference");out.referenceChecks++;
     predictions[m]=z;out.predictions++;
     ck(z.dependencies.every(([id,v])=>log.some(r=>r.id===id&&r.version===v&&r.received<t&&r.epoch===epoch)),"no future or epoch leak");
    }
    out.lateFeedbackExcluded+=log.filter(r=>r.id<t&&r.received>=t).length;
    out.epochExcluded+=log.filter(r=>r.received<t&&r.epoch!==epoch).length;
    // Freeze prediction before creating observation; synthetic observation delay 0..3.
    frozen.push(JSON.stringify(predictions));events.push({t,epoch,menu,choice,predictions});
    let delay=rnd(4),willObserve=rnd(5)!==0,received=t+delay;
    if(willObserve){
     let r={id:t,version:1,received,epoch,menu,choice,allowed:true,qualified:true};log.push(r);
     if(rnd(8)===0){log.push({...r,version:2,received:received+1+rnd(2),allowed:false});out.withdrawalChecks++}
     else if(rnd(8)===0){log.push({...r,version:2,received:received+1+rnd(2),choice:menu[rnd(menu.length)]});out.correctionChecks++}
    }
   }
   // Score only current qualified feedback received by fixed cutoff 10; no latest
   // state recomputation of old forecasts. Missing label retains possible miss.
   const cutoff=11;
   for(let e of events){
    const r=log.filter(r=>r.id===e.t&&r.received<cutoff).sort((a,b)=>b.version-a.version)[0];
    let observed=r&&r.allowed&&r.qualified&&r.choice!==null;
    for(let m of modes){
     let z=e.predictions[m],s=out.groups[group][m];s.issued++;s.issuedSize+=z.set.length;s.abstained+=+z.abstain;s.singletons+=+(z.set.length===1);
     if(observed){
      s.observed++;s.observedSize+=z.set.length;s.observedAbstained+=+z.abstain;s.observedSingletons+=+(z.set.length===1);
      const miss=!z.set.includes(r.choice);s.covered+=+!miss;s.missed+=+miss;s.singletonWrong+=+(z.set.length===1&&miss);s.missLower+=+miss;s.missUpper+=+miss;
     }else{
      s.missing++;s.missLower+=+(z.set.length===0);s.missUpper+=+(e.menu.some(v=>!z.set.includes(v)));
     }
    }
    // Replay only records known at original cutoff, even after all later corrections.
    for(let m of modes)ck(eq(reference(os,e.menu,log,e.t,e.epoch,m),e.predictions[m]),"historical as-of");
    ck(JSON.stringify(e.predictions)===frozen[e.t],"frozen");out.historicalChecks++;
   }
   out.graphs++;
  }
 }
 for(let g of groups)for(let m of modes){
  let s=out.groups[g][m];ck(s.observed+s.missing===s.issued&&s.covered+s.missed===s.observed&&s.missLower<=s.missUpper&&s.missUpper<=s.issued,"counts");
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const os=orders(R.closure([])),r={id:0,version:1,received:0,epoch:1,menu:[1,2],choice:1,allowed:true,qualified:true};
 ctl(eq(predict(os,[1,2],[], "baseline").set,[1,2]),"baseline");
 ctl(eq(predict(os,[1,2],[r],"allHistory").set,[1]),"qualified prior");
 ctl(recordsAsOf([r],0,1).length===0,"strict cutoff");
 ctl(recordsAsOf([r],1,2).length===0,"new epoch");
 ctl(recordsAsOf([r,{...r,version:2,received:1,allowed:false}],2,1).length===0,"withdraw no fallback");
 ctl(predict(os,[1,2],[r,{...r,id:1,choice:2}],"allHistory").abstain,"conflict abstain");
 return out;
}
console.log(JSON.stringify(experiment(make,make2),null,2));
```
