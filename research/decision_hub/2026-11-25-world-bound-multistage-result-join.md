# 多阶段科学计算的情景绑定、压缩连接及局部覆盖
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / EXACT_FINITE_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 993ad729b8dc7dc13299092442e2d1a74b2d9d79；Draft #62固定候选 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期10提交、14开放PR、v3.2前15行、同步规程前22行、唯一产品交接前18行blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。检索dependency/composition/pipeline/intermediate/provenance/joint support/branch/correlated/join/conditional/support projection/envelope/factor/projection/elimination；审阅R4 c05bd6b76e1864a5b7649ae4ef93186817f5b88d、R27 984bf62a969ac0f368f21496fcacaecf903a6a38、R46 39354c9b7151ca3fb1aa17b76f81751e00ead6c2、R54 7ab23d84e837b9fdb05dee09335057a31f5f3709、R66 89da2969792d09fa4ba8e41325b0ff4e36251fe5、R93 c5fecc311d7b96a0d3e198a50272b9e041f45d00、R94 fdeb77f0dd0cdd9f98867bce1de73a3d0e2a7043、R107 2f0c17a303bde8ef3e9711a08fcbbbaa8d5e78ec、R111 7488da9ef7654f5f4ccbbe3fc720217d94bd0c92、R125 9d9cce085f07189809d1524cd189d94ca7e2ba51、R133 9931c93dd784ab2c39c9fec363bbefc62e62bbe9合同及算法前段。已有联合支持、证据失效和信封；R94已有跨方案联合状态，R133已有来源绑定联合投影。本轮不是新关联域理论，仅新增实际复用持续收益阈值方法的分组结果连接、保留逐情景见证、部分端口缺失与连接运算预算。全库去重有限。

## 固定资产
research/decision_hub/2026-11-25-recurring-benefit-feasibility-threshold.md，固定commit 45934aedcc37ad2bae1c56cee4dce4959befeccc，连接器blob 9c27c104e3be8f18eebc18f5ad8a0e10e2940fcf。实际加载已审查自有threshold和feasible函数，非重写计算。收益端口为人工假设情景，未调用真实预测模型；不执行任意外部文档。

## 合同及推导
可信宿主给定完整有限情景集合H、同一目标、现金储备、期限、时间槽、账户、币种、收支口径、方法及来源资格。每情景w有阈值T(w)及条件收益G(w)，T为前轮数学模型，G为另一独立结构化输入端口（非统计独立或真实预测）。T=NO_FINITE_THRESHOLD表示给定合同无有限持续收益可满足期限底线；不同于未知。每情景通过 iff T有限且G>=T。将每个端口按相同输出值分组，保留每组精确情景支持集合。连接两个组的支持交集非空才允许组合其值，交集保留为见证。两端口均为每情景确定单值的函数，组内覆盖无重复，故任一有两端口的情景恰落在一个连接组；逐组应用阈值比较等价于逐情景计算。覆盖缺失保留为H减去已连接情景，并且只能发布已覆盖情景的条件结果，不能将未计算情景判失败或移除。覆盖域本身未知不发布此类证书；空域冲突。分组身份必须绑定同一联合域、会话、修订、用途、来源及授权；本实验仅可信内存夹具，不验证真实元数据、密码学、跨轮或撤回。重复组覆盖拒绝仅测试实际相交重复，不提供完整外部端口收据验证。预算计尝试的组对（含空交集），超限不发布任何结果；不包含构建、前轮模型、存储等全请求资源，不测性能。位掩码仅8情景，通用实现须扩展。不能将组合计数当概率、现金门当总体最优或自动执行授权；authority NONE。用户目标与底线不可擅改。

## 实验
48组固定成本/基础收入/期限设置×8共同情景（现金1/3、兑现滞后1/2、收益0/2）先执行实际前轮阈值及直接行动枚举核对。各设置遍历255非空关联域×2收益端口覆盖模式（全部/掩码85），共24480域。第二种人为模拟收益缺失，不缩减H。对照逐情景直接结果及完整阈值收益值对支持集合；故意弱基线丢失支持标签后交叉全部边际组，统计虚增组合，以及完整域内所有真实情景失败却产生通过的组合、所有通过却产生失败的组合。partial下若已知分支单一而忽略未知则错误声称全域确定，计missingNaiveCertainty。rawPairs为逐行全笛卡尔比较次数的假设参照计数，joinPairs为实际分组尝试计数，不能直接推断整体速度；直接按世界键线性连接可能更高效。14控制。研究者自行选择情景、掩码、预算和分组接口，重复域非独立用户数据。复算路径共享历史数学合同，同研究者非独立验收。无新外部资料、个人数据、真实训练、原生API、设备测量、CI请求、PR合并、部署、费用或冻结变更。

```js
function load(doc){const s=doc.split("```js\n")[1].split("\n```")[0].split(" let o={cases:")[0];return Function(s+"\nreturn {threshold,feasible};\n}\nreturn experiment();")()}
function experiment(P){
 const ck=(v,m)=>{if(!v)throw Error(m)},W=[0,1,2,3,4,5,6,7],eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const list=m=>W.filter(w=>m&(1<<w)),sort=x=>[...x].sort();
 const INF="NO_FINITE_THRESHOLD";
 // Values are compacted into classes but the full support is retained.
 function group(values,mask){let m=new Map();for(let w of list(mask)){let v=values[w];m.set(v,(m.get(v)||0)|(1<<w))}return [...m].map(([value,support])=>({value,support}))}
 function join(T,G,scope,limit=100,covered=true){
  if(!covered)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  if(!scope)return {status:"CONFLICT",authority:"NONE"};
  let rows=[],seen=0,pass=0,fail=0,used=0;
  for(let a of T)for(let b of G){
   if(used>=limit)return {status:"LIMIT",authority:"NONE"};used++;
   let s=a.support&b.support&scope;if(!s)continue;
   if(seen&s)return {status:"INVALID_OVERLAP",authority:"NONE"};
   seen|=s;let ok=a.value!==INF&&b.value>=a.value;if(ok)pass|=s;else fail|=s;
   rows.push({threshold:a.value,gain:b.value,support:s,feasible:ok});
  }
  const missing=scope&~seen;
  return {status:missing?"PARTIAL_COVERAGE":pass&&fail?"CONDITIONAL_MIXED":pass?"CONDITIONAL_ALL_PASS":"CONDITIONAL_ALL_FAIL",authority:"NONE",rows,pass,fail,missing,used};
 }
 function key(t,g){return JSON.stringify([t,g])}
 let o={settings:0,worldCalculations:0,cases:0,complete:0,partial:0,fullPass:0,fullFail:0,mixed:0,localRetained:0,joinChecks:0,compressedGroups:0,rawPairs:0,joinPairs:0,cartesianExtraTuples:0,cartesianFalsePass:0,cartesianFalseFail:0,missingNaiveCertainty:0,controls:0,witnesses:{}};
 for(let fee of [0,1,2])for(let ca of [1,2])for(let cb of [1,3])for(let income of [0,1])for(let da of [2,3]){
  let params=W.map(w=>({cash:(w&1)?3:1,reserve:1,income,ca,cb,fee,busy:1,da,db:4,lag:(w&2)?2:1}));
  let gain=W.map(w=>(w&4)?2:0);
  let threshold=params.map(p=>{let q=P.threshold(p);return q.status==="CONDITIONAL"?q.minimum:INF});
  let result=params.map((p,w)=>P.feasible(p,gain[w]));
  for(let w of W){ck(result[w]===(threshold[w]!==INF&&gain[w]>=threshold[w]),"prior source replay");o.worldCalculations++}
  o.settings++;
  for(let scope=1;scope<256;scope++)for(let live of [255,85]){
   // Second port may be missing; its disappearance cannot shrink the world universe.
   let tm=scope,gm=scope&live,T=group(threshold,tm),G=group(gain,gm),v=join(T,G,scope),known=scope&live;
   let p=0,n=0,expected=new Map();
   for(let w of list(known)){if(result[w])p|=1<<w;else n|=1<<w;let k=key(threshold[w],gain[w]);expected.set(k,(expected.get(k)||0)|(1<<w))}
   let actual=new Map(v.rows.map(row=>[key(row.threshold,row.gain),row.support]));
   ck(actual.size===expected.size&&[...expected].every(([k,s])=>actual.get(k)===s)&&v.pass===p&&v.fail===n&&v.missing===(scope&~known),"joined support");
   o.cases++;o.joinChecks++;o.compressedGroups+=T.length+G.length;o.rawPairs+=list(tm).length*list(gm).length;o.joinPairs+=v.used;
   if(v.missing){o.partial++;if(known)o.localRetained++;if(known&&(!p||!n)){o.missingNaiveCertainty++;o.witnesses.missing??={fee,ca,cb,income,da,scope,live,v}}}
   else{o.complete++;if(p&&n)o.mixed++;else if(p)o.fullPass++;else o.fullFail++}
   // Deliberately weak baseline: discard support tags and cross all distinct values.
   let naive=new Set(),np=false,nf=false;
   for(let a of T)for(let b of G){naive.add(key(a.value,b.value));let ok=a.value!==INF&&b.value>=a.value;np||=ok;nf||=!ok}
   o.cartesianExtraTuples+=[...naive].filter(k=>!expected.has(k)).length;
   if(!v.missing&&np&&!p){o.cartesianFalsePass++;o.witnesses.falsePass??={fee,ca,cb,income,da,scope,v,T,G}}
   if(!v.missing&&nf&&!n){o.cartesianFalseFail++;o.witnesses.falseFail??={fee,ca,cb,income,da,scope,v,T,G}}
  }
 }
 const T=[{value:1,support:1},{value:0,support:2}],G=[{value:0,support:1},{value:2,support:2}];
 const v=join(T,G,3);
 for(let t of [o.settings===48,o.worldCalculations===384,o.cases===24480,o.complete+o.partial===o.cases,o.fullPass+o.fullFail+o.mixed===o.complete,o.cartesianFalsePass>0,o.cartesianFalseFail>0,o.missingNaiveCertainty>0,v.pass===2&&v.fail===1,join(T,G,3,3).status==="LIMIT",join(T,G,3,4).status==="CONDITIONAL_MIXED",join(T,G,3,100,false).status==="UNKNOWN_COVERAGE",join(T,G,0).status==="CONFLICT",join([...T,T[0]],G,3).status==="INVALID_OVERLAP"]){ck(t,"control "+o.controls);o.controls++}
 return o;
}
console.log(JSON.stringify(experiment(load(doc)),null,2));
```
## 实测
```json
{
  "settings": 48,
  "worldCalculations": 384,
  "cases": 24480,
  "complete": 12960,
  "partial": 11520,
  "fullPass": 3120,
  "fullFail": 2298,
  "mixed": 7542,
  "localRetained": 10800,
  "joinChecks": 24480,
  "compressedGroups": 86166,
  "rawPairs": 331776,
  "joinPairs": 77096,
  "cartesianExtraTuples": 22408,
  "cartesianFalsePass": 864,
  "cartesianFalseFail": 252,
  "missingNaiveCertainty": 8985,
  "controls": 14,
  "witnesses": {
    "missing": {
      "fee": 0,
      "ca": 1,
      "cb": 1,
      "income": 0,
      "da": 2,
      "scope": 3,
      "live": 85,
      "v": {
        "status": "PARTIAL_COVERAGE",
        "authority": "NONE",
        "rows": [
          {
            "threshold": 1,
            "gain": 0,
            "support": 1,
            "feasible": false
          }
        ],
        "pass": 0,
        "fail": 1,
        "missing": 2,
        "used": 2
      }
    },
    "falseFail": {
      "fee": 0,
      "ca": 1,
      "cb": 1,
      "income": 0,
      "da": 2,
      "scope": 18,
      "v": {
        "status": "CONDITIONAL_ALL_PASS",
        "authority": "NONE",
        "rows": [
          {
            "threshold": 0,
            "gain": 0,
            "support": 2,
            "feasible": true
          },
          {
            "threshold": 1,
            "gain": 2,
            "support": 16,
            "feasible": true
          }
        ],
        "pass": 18,
        "fail": 0,
        "missing": 0,
        "used": 4
      },
      "T": [
        {
          "value": 0,
          "support": 2
        },
        {
          "value": 1,
          "support": 16
        }
      ],
      "G": [
        {
          "value": 0,
          "support": 2
        },
        {
          "value": 2,
          "support": 16
        }
      ]
    },
    "falsePass": {
      "fee": 0,
      "ca": 1,
      "cb": 1,
      "income": 0,
      "da": 2,
      "scope": 65,
      "v": {
        "status": "CONDITIONAL_ALL_FAIL",
        "authority": "NONE",
        "rows": [
          {
            "threshold": 1,
            "gain": 0,
            "support": 1,
            "feasible": false
          },
          {
            "threshold": "NO_FINITE_THRESHOLD",
            "gain": 2,
            "support": 64,
            "feasible": false
          }
        ],
        "pass": 0,
        "fail": 65,
        "missing": 0,
        "used": 4
      },
      "T": [
        {
          "value": 1,
          "support": 1
        },
        {
          "value": "NO_FINITE_THRESHOLD",
          "support": 64
        }
      ],
      "G": [
        {
          "value": 0,
          "support": 1
        },
        {
          "value": 2,
          "support": 64
        }
      ]
    }
  }
}
```
后续：在原生方法端口引入当前联合情景身份与覆盖清单，优先以真实方法链对照逐世界复算；独立验收轨负责未见及篡改/失效测试，产品轨维护唯一交接。没有本轮正式版本开发授权。