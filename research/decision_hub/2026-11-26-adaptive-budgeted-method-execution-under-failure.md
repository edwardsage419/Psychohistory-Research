# 自主引擎：计算失败后的有限预算自适应方法执行
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线及去重
固定main 64ca5b497b311dfef581e4d0917849652b2fa557，核对18近期提交、15开放Draft PR、v3.2、同步规程、唯一产品交接前20行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）及完整目录树相关题名。#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。读取既有 budgeted-analysis-planning.md d99676bf1241e852a7c035fe092f1eabbf124c7e（第47轮固定工作集合，未实现失败后动态重规划）、adaptive-resource-allocation/README.md 7485bf6a5e6d4ea037fedebed0b752655f047000（概率学习资源DP，非本轮无概率执行）、composition-dispatch/README.md 8953af15d57350d892c5dddd401c5c2bdd6f237d、scoped-regression-transitive-method-isolation.md ae545156e4ed8d39a96f940ab3aaac0b6cecad51、bounded-numeric-wire-shared-parameter-receipts.md 7821b0afe42fc77ead90693f40a79ff7b6af54c7、v08-durable-budgeted-join-transaction.md 1367026835d896b6c1cddd5734d38624822376ed、anytime-decision-port-certificates.md 7f37403fc178117f61107833289ad60a15dcc3d7相关段落。新增失败/观察分支下的有限鲁棒预算执行策略，不重复固定闭包、持久预约或语义搜索证明。全库去重有限。
## 研究合同
六个虚构工作：硬门、共享证据、主要方法、独立替代方法、独立描述、联合检查。每工作至多尝试一次，固定正整数成本上界，失败也扣全额；资格掩码由可信宿主预设；主方法要求共享证据成功，联合检查必须实际硬门PASS且至少一个比较方法成功。硬门三状态：未知0、通过1、确定违反2。违反不是执行失败，也不能用于联合检查。其他方法二元成功或失败。替代方法与主方法的计算出口身份假定经宿主确认可替代，仅计一次；不合并科学上不同的预测或复核。三个独立可交付出口（计算候选、描述、联合检查），联合检查成功仅表示完成研究夹具的检查，不是现实推荐资格。无真实概率、真实数据或自动行动。所有authority NONE。
给定有限完整的潜在执行结果表W，每个世界包含各任务的固定潜在状态，不允许已观察任务改变后续潜在状态；允许任意相关，未知真实世界，不用样本频率作概率。算法仅按已观察结果更新相容世界集合H。状态为H、已尝试任务集、成功任务集、硬门结果、剩余额度。硬门有资格且预算能覆盖时必须首先尝试，即使保证产出不提高；硬门缺资格或预算不够时允许独立局部输出，但禁止联合检查。无法保证硬门解决并不意味着所有分支不解决。目标是在每个分支不超预算及资格/依赖约束的前提下，最大化最坏世界的字典序(硬门是否有确定结论,唯一出口数量)，属于研究工程覆盖目标，不是用户人生效用、实际质量或对每个较好世界的优化。无额外成本权重，同值可停止，非所有策略并列或最小实际开销证明。
Bellman: 对合法停止取当前覆盖；对每个合法任务i，将H按实际可能观察y分割为H_y，扣成本并更新状态，取所有非空分支后继价值的字典序最小；在任务/停止选择中取最大。每步减少未尝试任务，有限归纳得全策略最优；策略不访问真实世界，只观察后更新H。若H覆盖或成本/资格合同未知则该最坏世界保证不成立。实际执行前另核当前资格与预算；版本变化、失败重试、并发、原生结果及认证事务需接前轮研究。不能把计划覆盖当实际完成。
## 首次实验与修订
初版仅按最坏字典序评价，未强制硬门首先尝试。实际运行324配置、1126世界，阈值参照2592检查一致，13配置优于固定顺序；但反例W=[[2,1,1,1,0,1],[0,1,1,1,1,0],[1,0,1,1,1,1]], cost=[1,2,3,2,2,1], B=4,Q=63 中，策略先运行描述，成功分支跳过本可尝试的硬门，违反本轮拟议优先规则。初版未写仓库；计数不纳入终版。终版将门优先作为硬执行合同，同时修正伪随机取样使用高位比例而非低位取模，增加正向全联合、门失败/无资格/预算不足等控制。终版全部重跑。此为研究设计缺陷修正，并非实际产品缺陷。
## 实际实验
六手工控制及480固定种子合成配置（2..5世界、成本1..3、预算0..13、资格掩码），标准JS实际执行。候选有记忆Bellman求值；参照为不使用值递推的阈值可达性递归（对八个目标，要求每个可能观察分支均存在合法后续），共享研究合同，非独立科研验收。逐世界重放检查执行权、实际观察、门优先、预算及联合检查资格。对照为所有固定任务排列（门可尝试时必须排首位），遇依赖不满足、无资格或超额即跳过，仍会根据已观察结果判断可运行，不能事后改变次序；不是完全无反馈基线。自适应可模拟其策略，故不弱于固定排列最优。对照不代表现有产品或真实竞争工具。覆盖统计计数仅合成世界与配置，不能作泛化或实际速度估计。
```json
{
  "seed": 20261126,
  "cases": 486,
  "controls": 6,
  "worlds": 1681,
  "states": 8321,
  "branchChecks": 12729,
  "thresholdChecks": 3888,
  "worldReplays": 1681,
  "adaptiveBetter": 1,
  "adaptiveEqual": 485,
  "gateResolvedWorst": 89,
  "mandatoryFirstReplays": 1281,
  "fullJointAllWorlds": 2,
  "partialWhenGateUnknown": 396,
  "unavailablePorts": 1571,
  "staticOrdersTested": 129720,
  "examples": [
    {
      "case": {
        "W": [
          [
            1,
            0,
            0,
            1,
            0,
            1
          ],
          [
            2,
            0,
            0,
            0,
            1,
            1
          ]
        ],
        "c": [
          1,
          1,
          1,
          1,
          1,
          1
        ],
        "B": 2,
        "Q": 63
      },
      "adaptive": [
        1,
        1
      ],
      "static": [
        1,
        0
      ],
      "traces": [
        {
          "v": [
            1,
            1
          ],
          "spent": 2,
          "trace": [
            [
              "hard_gate",
              1
            ],
            [
              "alternative",
              1
            ]
          ],
          "ok": 9,
          "gate": 1
        },
        {
          "v": [
            1,
            1
          ],
          "spent": 2,
          "trace": [
            [
              "hard_gate",
              2
            ],
            [
              "description",
              1
            ]
          ],
          "ok": 16,
          "gate": 2
        }
      ]
    }
  ],
  "controlResults": [
    {
      "j": 0,
      "adaptive": [
        1,
        1
      ],
      "static": [
        1,
        0
      ],
      "joint": [
        false,
        false
      ]
    },
    {
      "j": 1,
      "adaptive": [
        1,
        3
      ],
      "static": [
        1,
        3
      ],
      "joint": [
        true,
        true
      ]
    },
    {
      "j": 2,
      "adaptive": [
        0,
        2
      ],
      "static": [
        0,
        2
      ],
      "joint": [
        false
      ]
    },
    {
      "j": 3,
      "adaptive": [
        1,
        2
      ],
      "static": [
        1,
        2
      ],
      "joint": [
        false
      ]
    },
    {
      "j": 4,
      "adaptive": [
        0,
        2
      ],
      "static": [
        0,
        2
      ],
      "joint": [
        false
      ]
    },
    {
      "j": 5,
      "adaptive": [
        0,
        2
      ],
      "static": [
        0,
        2
      ],
      "joint": [
        false
      ]
    }
  ]
}
```
## 接入及限制
计划层输入明确的当前方法资格/版本、必要依赖、固定任务身份、保守成本上界、可接受的观察支持及最少必需检查；输出条件执行策略与最坏覆盖，不发布任何数学结果。运行层按真实观察及当前资格重算策略，调用持久预算与发布事务；每个结果单独核验，失败不能默认零或合法。真实自主语义、开放模型、任务动态效果/并发、未知域、运行成本测量、超预算截断、真实回退及独立留出未实现。算法仅有限小图，状态指数增长，未测设备性能。研究者自行选图、成本、工程覆盖权重、世界、硬门优先及基线；未授权为生产规则。未改生产、唯一交接、冻结协议或证据等级，未启动新Codex任务、训练、合并、部署、主动CI或新增费用。
## 完整复算
Node标准JS，无依赖，实际运行在连接器JS。
```js
function experiment(){
 const ck=(b,m)=>{if(!b)throw Error(m)},N=6,ALL=63,ids=["hard_gate","shared_evidence","primary","alternative","description","joint_check"],bits=m=>Array.from({length:N},(_,i)=>i).filter(i=>m&(1<<i));
 const ready=(i,a,o,g,Q)=>!(a&(1<<i))&&(Q&(1<<i))&&(i!==2||!!(o&2))&&(i!==5||(g===1&&!!(o&12)));
 const eligible=(i,a,o,g,Q,b,c)=>ready(i,a,o,g,Q)&&c[i]<=b&&(!(a===0&&(Q&1)&&c[0]<=b)||i===0);
 const score=(o,g)=>[+(g!==0),+(!!(o&12))+(!!(o&16))+(!!(o&32))];
 const cmp=(a,b)=>a[0]-b[0]||a[1]-b[1],worst=(a,b)=>cmp(a,b)<=0?a:b;
 const transition=(i,y,a,o,g)=>[a|(1<<i),o|(y===1?(1<<i):0),i===0?y:g];
 const permutations=[];function perm(a,r){if(!r.length){permutations.push(a);return}for(let i of r)perm([...a,i],r.filter(j=>j!==i))}perm([],bits(ALL));
 function exact(W,c,B,Q){
  let memo=new Map(),nodes=0,edges=0;
  function solve(mask,a,o,g,b){let key=[mask,a,o,g,b].join(":");if(memo.has(key))return memo.get(key);nodes++;
   let forced=a===0&&(Q&1)&&c[0]<=b,result=forced?null:{v:score(o,g),act:-1};
   for(let i=0;i<N;i++)if(eligible(i,a,o,g,Q,b,c)){let parts=new Map();for(let w=0;w<W.length;w++)if(mask&(1<<w)){let y=W[w][i];parts.set(y,(parts.get(y)||0)|(1<<w))}
    let v=null;for(let [y,m] of parts){edges++;let x=solve(m,...transition(i,y,a,o,g),b-c[i]).v;v=v===null?x:worst(v,x)}
    if(!result||cmp(v,result.v)>0)result={v,act:i};
   }ck(result,"forced gate exists");memo.set(key,result);return result
  }
  let full=(1<<W.length)-1,r=solve(full,0,0,0,B),traces=[];
  for(let w=0;w<W.length;w++){let a=0,o=0,g=0,b=B,mask=full,trace=[];while(true){let i=solve(mask,a,o,g,b).act;if(i===-1)break;ck(eligible(i,a,o,g,Q,b,c),"execution ready");let y=W[w][i];trace.push([ids[i],y]);for(let j=0;j<W.length;j++)if(W[j][i]!==y)mask&=~(1<<j);ck(mask&(1<<w),"nonanticipation");[a,o,g]=transition(i,y,a,o,g);b-=c[i];ck(b>=0&&(!(o&32)||g===1&&!!(o&12)),"budget gate")}
   if((Q&1)&&c[0]<=B)ck(trace[0]?.[0]==="hard_gate","mandatory gate first");
   traces.push({v:score(o,g),spent:B-b,trace,ok:o,gate:g})
  }
  ck(cmp(traces.map(t=>t.v).reduce(worst),r.v)===0,"policy replay");return {v:r.v,nodes,edges,traces}
 }
 function feasible(W,c,B,Q,target){function check(rows,remaining,success,gate,budget,first){let force=first&&(Q&1)&&c[0]<=budget;if(!force&&cmp(score(success,gate),target)>=0)return true;
   for(let i of remaining){if(force&&i!==0||c[i]>budget||!(Q&(1<<i))||i===2&&!(success&2)||i===5&&(gate!==1||!(success&12)))continue;let values=[...new Set(rows.map(w=>w[i]))];if(values.every(y=>check(rows.filter(w=>w[i]===y),remaining.filter(j=>j!==i),success|(y===1?1<<i:0),i===0?y:gate,budget-c[i],false)))return true}return false}
  return check(W,bits(ALL),0,0,B,true)
 }
 function staticBest(W,c,B,Q){let v=null,order=null;for(let p of permutations){if((Q&1)&&c[0]<=B&&p[0]!==0)continue;let vals=W.map(w=>{let a=0,o=0,g=0,b=B;for(let i of p)if(ready(i,a,o,g,Q)&&c[i]<=b){[a,o,g]=transition(i,w[i],a,o,g);b-=c[i]}return score(o,g)});let r=vals.reduce(worst);if(v===null||cmp(r,v)>0){v=r;order=p}}return {v,order}}
 const targets=[0,1].flatMap(a=>[0,1,2,3].map(b=>[a,b]));let seed=20261126;function rand(n){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}
 let cases=[{W:[[1,0,0,1,0,1],[2,0,0,0,1,1]],c:[1,1,1,1,1,1],B:2,Q:63},{W:[[1,1,1,1,1,1],[1,0,0,1,1,1]],c:[1,1,1,1,1,1],B:6,Q:63},{W:[[0,1,1,1,1,1]],c:[1,1,1,1,1,1],B:6,Q:63},{W:[[1,1,1,1,1,1]],c:[1,1,1,1,1,1],B:6,Q:31},{W:[[1,1,1,1,1,1]],c:[3,1,1,1,1,1],B:2,Q:63},{W:[[1,1,1,1,1,1]],c:[1,1,1,1,1,1],B:6,Q:62}];
 for(let k=0;k<480;k++){let W=Array.from({length:2+rand(4)},()=>Array.from({length:N},(_,i)=>i===0?rand(3):(rand(7)>1?1:0))),c=Array.from({length:N},()=>1+rand(3)),B=rand(14),Q=rand(4)?63:rand(64);cases.push({W,c,B,Q})}
 let out={seed:20261126,cases:cases.length,controls:6,worlds:0,states:0,branchChecks:0,thresholdChecks:0,worldReplays:0,adaptiveBetter:0,adaptiveEqual:0,gateResolvedWorst:0,mandatoryFirstReplays:0,fullJointAllWorlds:0,partialWhenGateUnknown:0,unavailablePorts:0,staticOrdersTested:0,examples:[],controlResults:[]};
 for(let j=0;j<cases.length;j++){let {W,c,B,Q}=cases[j],r=exact(W,c,B,Q),s=staticBest(W,c,B,Q);out.worlds+=W.length;out.states+=r.nodes;out.branchChecks+=r.edges;out.worldReplays+=r.traces.length;out.staticOrdersTested+=(Q&1)&&c[0]<=B?120:720;for(let t of targets){ck(feasible(W,c,B,Q,t)===(cmp(r.v,t)>=0),"threshold oracle");out.thresholdChecks++}ck(cmp(r.v,s.v)>=0,"adaptive >= static");if(cmp(r.v,s.v)>0){out.adaptiveBetter++;if(out.examples.length<3)out.examples.push({case:cases[j],adaptive:r.v,static:s.v,traces:r.traces})}else out.adaptiveEqual++;
  out.gateResolvedWorst+=+!!r.v[0];out.mandatoryFirstReplays+=((Q&1)&&c[0]<=B)?r.traces.length:0;out.fullJointAllWorlds+=+r.traces.every(t=>!!(t.ok&32));out.partialWhenGateUnknown+=r.traces.filter(t=>t.gate===0&&t.v[1]>0).length;out.unavailablePorts+=r.traces.filter(t=>!(t.ok&32)).length;if(j<6)out.controlResults.push({j,adaptive:r.v,static:s.v,joint:r.traces.map(t=>!!(t.ok&32))});
 }
 ck(out.controlResults[0].adaptive[1]===1&&out.controlResults[0].static[1]===0,"strict advantage");
 ck(out.controlResults[1].joint.every(Boolean),"positive joint control");ck(out.controlResults.slice(2).every(r=>r.joint.every(x=>!x)),"blocked controls");
 return out
}
console.log(JSON.stringify(experiment(),null,2));
```
