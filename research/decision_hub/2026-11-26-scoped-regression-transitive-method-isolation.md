# 自主引擎：分域退化隔离、传递方法依赖及当前结果资格
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NATIVE_SOURCE_READ / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线与去重
固定main 071d4c235ec9fda6475c8a18f9776eeb922a901e，读取20近期提交、15开放Draft PR、v3.2、同步规程、唯一产品交接前20行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）、完整目录树相关题名。#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft。实际静态读取其 decision_registry.py b833a6d45d944f2f1b885ab1a409df28c390c233、decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f、decision_composition.py aea376e8c94a4959bee1afd5e8a6b8c785060d42 前100行相关接口，已有不可变注册版本、固定依赖、适用性、联合域和研究权限，不重计。核对context-qualified-model-routing.md dcc14692b2c92d1f5d256e969e4d9fd135ac714e（分域净改善路由）、composition-dispatch/README.md 8953af15d57350d892c5dddd401c5c2bdd6f237d（依赖调度）、partial-analysis-dispatch/README.md 08051d3b029ebb3acca1380bdf5b92ad99d8a44d（局部输出）、v07-knowledge-qualification-shared-parameter-bridge.md df5a962a58ba0601b6014fad47c39cd3ebdb0e33、budgeted-change-start-regression-monitor.md c58ae4a613957a8ecb3ad3bfbae0b5f943d33f56（统计退化）、frozen-paired-forecast-cohort-feedback-bounds.md 799e4e0761a5544b1b6527ff69e594b51cbd369f相关段落。本轮只连接分域监测状态、精确版本及传递资格与局部结果，非原生漏洞证明、全库去重证明或重新发明注册表。
## 合同
有限研究图六个固定方法版本节点，三种可信上下文类别，三出口（硬门、预测、比较），每出口预设优先方法和部分后备。节点名称仅虚构，不代表产品实际算法、科学资格或真正版本映射。全局阻断表示跨上下文的独立完整性/授权等资格失效；局部REVIEW表示已由宿主认定统计退化提示需隔离该具体范围，UNKNOWN表示该域适用性/资格待核。三者均不进入相应当前计算；QUALIFIED必须由独立宿主提供，未检测退化不能直接当合格。全局优先于局部。图边表示确切版本的必要依赖，范围映射为同域（研究选择，不覆盖跨域或可选依赖）；依赖需独立类型/单位/参数匹配，实验未计算这些内容。节点可调用 iff 自身及全部传递依赖均QUALIFIED。证明：DAG按拓扑递推，必要依赖的闭包由当前节点及各子闭包并集构成，归纳得到判定式。故局部隔离沿依赖传播而不影响无依赖的出口；全局隔离也覆盖相应全部域。并非统计退化自动证明共享底层方法有错。回退版本须另行有资格，禁止以版本更旧或历史成绩推导适用。
上下文域由可信宿主给出非空可能集合与覆盖标志。每域按优先次序可提出合格方法，均为研究候选。需要共同方法时另对全部可能域求资格交集，从原有优先顺序挑共同候选；不得仅根据第一域通过即通用。没有共同候选可保留逐域条件计划或未知；即使共同方法存在也不意味着语义完整、参数相同、结果相同、硬门满足或最终推荐。代码plan中的un仅在覆盖且各域首选同一方法时返回；实验另算共同备选actual，后者可在首选不一致时仍存在；两种策略分列，不视为自动执行。覆盖未确认无通用首选输出。所有authority NONE，无真实用户确认、权限、计算或行动。
收据绑定根方法精确版本、域、每个传递依赖的全局资格版本和本域资格版本；假定固定图、固定输入及算法、同会话/授权/用途、可信进程。每次变更单调推进相应代次，恢复原状态也不得复用旧收据；无关域/无关依赖变化可复用资格计算。真实数学收据还必须包含完整输入、方法配置、来源、作用域、版本、授权和结果认证，不得以本资格键替代。当前代码无签名、持久化、真实回退、并发或用户数据。
## 实际实验
标准JS实际运行。64全局阻断掩码×8当前预测版本分域REVIEW掩码×8共享核分域UNKNOWN掩码=4096配置。每配置6节点×3域，对比传递闭包与直接重复传播失败的参照；再枚举7非空域组合×3出口，检查条件首选及共同候选资格，并核对覆盖未知禁止通用首选。三简化对照分别为仅看自身、任一域受限即全域隔离、只用第一可能域的首选；计数为有限节点/端口，不是产品错误率。额外24种全局/局部切换事件的全部两步序列（含恢复原状）×18节点域收据，检查应失效及无关复用；3专项控制。同一研究者的合成夹具及参照，非独立科学验证。未运行原生方法、API/CLI、真机、真实反馈、统计监测器或训练。
```json
{
  "configurations": 4096,
  "qualificationChecks": 73728,
  "portChecks": 86016,
  "fullyCommon": 24546,
  "conditionalOnly": 0,
  "unavailableDomainPorts": 61470,
  "unknownCoverageControls": 86016,
  "naiveDependencyMiss": 15936,
  "globalOverblocking": 4356,
  "primaryDomainLeak": 1884,
  "receiptChecks": 10368,
  "unaffectedReuse": 7272,
  "staleRejected": 3096,
  "controls": 3,
  "examples": [
    {
      "global": 0,
      "l": 0,
      "u": 2,
      "domains": [
        0,
        1
      ],
      "port": "prediction",
      "primary": "predict@2",
      "actual": null,
      "by": [
        {
          "d": 0,
          "choice": 3
        },
        {
          "d": 1,
          "choice": null
        }
      ]
    },
    {
      "global": 0,
      "l": 0,
      "u": 2,
      "domains": [
        0,
        1
      ],
      "port": "comparison",
      "primary": "compare@1",
      "actual": "fallback@1",
      "by": [
        {
          "d": 0,
          "choice": 4
        },
        {
          "d": 1,
          "choice": 5
        }
      ]
    }
  ]
}
```
## 下游
拟议接口 MethodScopeStatus（版本、范围、用途、来源、审核状态、代次）、ScopedDependencyPlan、EligibilityReceipt；复用现有不可变注册与联合世界作用域，后续接统计监测真实证据、关键安全门和有效替代方法审核。研究者自行选择图、域、优先顺序及隔离策略；未授权为生产规则。全局隔离、局部隔离和统计审查分别记录，不能将结果计数解释为实际性能提升或能力退化率。真实产品需补齐跨域依赖映射、参数、证据和作用域身份、授权、回退事务及独立验证。未改正式代码、唯一交接、冻结协议或证据等级，未启动新Codex任务、训练、PR合并、部署、主动CI或费用。
## 完整复算
Node标准JS，无依赖；实际在连接器JS执行。
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),range=n=>Array.from({length:n},(_,i)=>i);
 // A@1 and A@2 are distinct; shared kernel, separate hard gate, fallback.
 const nodes=["kernel@1","hard@1","predict@1","predict@2","compare@1","fallback@1"];
 const deps=[[],[],[0],[0],[1,3],[1]],ports=[{id:"hard",choices:[1]},{id:"prediction",choices:[3,2]},{id:"comparison",choices:[4,5]}],D=3;
 const masks=range(8),status=(s,n,d)=>s.global&(1<<n)?"BLOCKED":s.local[n]&(1<<d)?"REVIEW":s.unknown[n]&(1<<d)?"UNKNOWN":"QUALIFIED";
 function closure(n){return [...new Set([n,...deps[n].flatMap(closure)])].sort((a,b)=>a-b)}
 const cls=nodes.map((_,i)=>closure(i));
 function qualified(s,n,d){return cls[n].every(k=>status(s,k,d)==="QUALIFIED")}
 function ref(s,n,d){let failed=nodes.map((_,k)=>status(s,k,d)!=="QUALIFIED");for(let i=0;i<nodes.length;i++)for(let j=0;j<nodes.length;j++)if(deps[j].some(k=>failed[k]))failed[j]=true;return !failed[n]}
 function plan(s,domains,covered){
  return ports.map(p=>{const by=domains.map(d=>({d,choice:p.choices.find(n=>qualified(s,n,d))??null}));let un=covered&&domains.length>0&&by.every(x=>x.choice!==null&&x.choice===by[0].choice)?by[0].choice:null;return {id:p.id,by,un,authority:"NONE"}})
 }
 const out={configurations:0,qualificationChecks:0,portChecks:0,fullyCommon:0,conditionalOnly:0,unavailableDomainPorts:0,unknownCoverageControls:0,naiveDependencyMiss:0,globalOverblocking:0,primaryDomainLeak:0,receiptChecks:0,unaffectedReuse:0,staleRejected:0,controls:0,examples:[]};
 // 64 global block patterns, 8 local review masks for active predictor, 8 unknown masks for kernel.
 for(let global=0;global<64;global++)for(let l of masks)for(let u of masks){const s={global,local:[0,0,0,l,0,0],unknown:[u,0,0,0,0,0]};out.configurations++;
  for(let n=0;n<nodes.length;n++)for(let d=0;d<D;d++){let a=qualified(s,n,d),b=ref(s,n,d);ck(a===b,"closure");out.qualificationChecks++;if(status(s,n,d)==="QUALIFIED"&&!a)out.naiveDependencyMiss++;if(a&&cls[n].some(k=>range(D).some(x=>status(s,k,x)!=="QUALIFIED")))out.globalOverblocking++}
  for(let dm=1;dm<8;dm++){let domains=range(D).filter(d=>dm&(1<<d)),p=plan(s,domains,true),unknown=plan(s,domains,false);for(let i=0;i<ports.length;i++){let z=p[i],o=domains.map(d=>({d,choice:ports[i].choices.find(n=>ref(s,n,d))??null}));ck(eq(z.by,o),"plan");let common=ports[i].choices.find(n=>domains.every(d=>ref(s,n,d)))??null;
   // Per-context preferred plans are allowed; use shared alternative if a common plan exists.
   let actual=common; if(actual!==null)ck(domains.every(d=>qualified(s,actual,d)),"common");
   out.portChecks++;out.fullyCommon+=+(actual!==null);out.conditionalOnly+=+(actual===null&&o.every(x=>x.choice!==null));out.unavailableDomainPorts+=+o.some(x=>x.choice===null);
   let primary=o[0].choice;if(primary!==null&&domains.some(d=>!qualified(s,primary,d))){out.primaryDomainLeak++;if(out.examples.length<2)out.examples.push({global,l,u,domains,port:ports[i].id,primary:nodes[primary],actual:actual===null?null:nodes[actual],by:o})}
   ck(unknown[i].un===null&&unknown[i].authority==="NONE","unknown coverage");out.unknownCoverageControls++;
  }}
 }
 // Versioned evidence: current receipts bind every transitive dependency in exact context.
 const initial=()=>({global:0,local:Array(6).fill(0),unknown:Array(6).fill(0),gv:Array(6).fill(0),lv:Array.from({length:6},()=>Array(3).fill(0)),seq:0});
 function receipt(s,n,d){return qualified(s,n,d)?{method:nodes[n],domain:d,basis:cls[n].map(k=>[nodes[k],s.gv[k],s.lv[k][d]]),authority:"NONE"}:null}
 function revise(s,event){let r=JSON.parse(JSON.stringify(s)),{n,d,type}=event;r.seq++;if(type==="global"){r.global^=1<<n;r.gv[n]=r.seq}else{r.local[n]^=1<<d;r.lv[n][d]=r.seq}return r}
 const events=range(6).flatMap(n=>[{n,type:"global"},...range(3).map(d=>({n,d,type:"local"}))]);
 for(let a of events)for(let b of events){let s=initial(),s1=revise(s,a),s2=revise(s1,b);for(let n=0;n<6;n++)for(let d=0;d<3;d++){let old=receipt(s,n,d),now=receipt(s2,n,d),affected=[a,b].some(e=>cls[n].includes(e.n)&&(e.type==="global"||e.d===d));let reusable=!!now&&eq(old,now);ck(reusable===!affected,"version invalidation");out.receiptChecks++;out.unaffectedReuse+=+reusable;out.staleRejected+=+affected}}
 const s=initial();let a=revise(s,{n:3,d:0,type:"local"});ck(!qualified(a,4,0)&&qualified(a,4,1)&&qualified(a,5,0)&&qualified(a,1,0),"local isolation");out.controls++;let b=revise(a,{n:0,type:"global"});ck(!qualified(b,2,1)&&!qualified(b,3,1)&&qualified(b,5,1),"global transitive");out.controls++;let c=revise(a,{n:3,d:0,type:"local"});ck(qualified(c,4,0)&&!eq(receipt(s,4,0),receipt(c,4,0)),"ABA");out.controls++;
 return out
}
console.log(JSON.stringify(experiment(),null,2));
```
