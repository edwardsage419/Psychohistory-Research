# 第45轮：按问题情景的证据限定模型路由与分布变化鲁棒性
2026-11-24。固定 main 32e3e7a40e9e7d844ad3d67eb28eac5f0997bee0；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一协调交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第4/38/44轮及第16轮嵌套组合（ad1f8f373eb41a68e9493511fd3ba9fd539fd56f）、第17轮在线预测跟踪（56babe29da0daed80d6420c5bfad8d8397e8a558，历史勘误继续有效）、第19轮序贯审查（481d395603a89efd9bc3c014dddfcbda76f98d53）。原生decision_registry.py blob 8046de09674af850a456bbccc534e5f6c2511497、decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f、decision_planner.py f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b已有注册、适用性、依赖执行和分歧提示。区别于既有同目标组合、在线权重和依赖门，本轮新增相同评价合同内、根据决策前可观察任务类别切换已获资格模型、未来类别构成变化、固定验证资源及分组退步约束。仅核查相关记录，未证明全库无类似研究；不声称现有生产模型有本轮反例中的缺陷。纯原创有限模型，无新增外部文献事实。
## 数学合同
相同输出目标、时点、损失、范围、成本、用户价值、证据资格的任务先按决策前可辨认且冻结的类别c分组。每类有合格基线0及适用、已授权候选m。D_cm=[l_cm,u_cm]是有资格的同尺度相对基线净改善界，基线恒0。缺失评价不可当0，不进入可比较候选；基线不合格则UNKNOWN/独立局部分析。历史评价区间不自动成为未来保证；只有获资格的跨环境适用条件才支持未来改善范围，否则仅条件情景。第44轮有限样本识别界不等于总体置信区间。不同决策准则与因果目标按第4/38轮分开，预测表现不能替代用户偏好。
路由r(c)在观察结果前固定，满足每类资格及资源约束（实验限制使用专门模型的类别数量，非真实运行时间或费用）。两类构成p,1-p，p∈[L,H]。若类别改善与构成可独立组合，净改善下界min_{p∈{L,H}}[p*l_0,r(0)+(1-p)*l_1,r(1)]，上界相应取上端点及max。非负权重使端点可同时取得，剩下仿射函数在区间端点取极值；相关时仅为外界。要求重要类别不退步则每类下界>=0（示例规范需确认），在有限合格路由中最大化下界，保存并列。基线合格时值>=0。未知类别不假装已识别；无合格基线不强制使用。
## 初次实验失败与更正
第一版实际运行在最后断言nontrivial失败，未写仓库。错误假设是自由路由中分组门一定具有严格机会成本。经推导：若可行路由对逐类退回基线封闭，且相对基线的下界为0，任何负下界候选换成基线都不降低任一非负构成权重下的净改善下界，资源约束仍满足。逐一替换即可得到同样或更好的无退步路由；因此分组门不降低最大保证净改善值（可能减少并列集合）。这并非一般情况下的免费安全保证，仅适用上述条件。更正断言并增加绑定全局家族的门槛比较：同一模型必须在所有适用类使用，不能自由单类退回；此时替换封闭性不成立，分组门可能有机会成本。本轮第二次执行通过，保留失败原因及更正范围。
## 实验
两类，每类基线+两专门模型。四个改善区间各6种闭区间（端点-2/0/2）；16资格遮罩；3未来份额范围[0,1],[.25,.75],[.75,1]；资源上限1/2类。共124416组合。端点公式与独立逐上下端点及四分位份额枚举核对上下界及最优路由，连续份额精确性由仿射证明。数值乘4为整数，不是实际效用。全局家族基线为固定一个模型且不可用类退回0，资源不足排除，另允许全基线；历史中点选择按虚构75/25分布（乘8整数），平局先遇、基线优先。unsafeGlobal/unsafeLocal指选出路由至少一类改善下界负，未满足研究无退步保证，非实际损失。specializedGain为自由路由严格优于同资格资源分组门的固定家族策略；groupBlocks为自由路由取消分组门的最优值严格提高，按上文应为0；globalGroupBlocks为绑定家族取消分组门的最优值严格提高。allFallback仅全体最优路由为基线。ineligibleCases至少一项资格未通过，不推断原因。9项手工资格控制仅模拟可信宿主，不是真实鉴权。两计算路径同一研究者设计，非独立验收。没有训练、统计校准、实际模型识别或性能测量。 
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 const vals=[-2,0,2],ints=vals.flatMap(l=>vals.filter(h=>h>=l).map(h=>[l,h]));
 const routes=[0,1,2].flatMap(a=>[0,1,2].map(b=>[a,b]));
 const mixes=[[0,4],[1,3],[3,4]];
 let cases=0,oracleChecks=0,routeChecks=0,robustGain=0,specializedGain=0,unsafeLocal=0,unsafeGlobal=0,globalShortfall=0,localShortfall=0,groupBlocks=0,globalGroupBlocks=0,allFallback=0,ineligibleCases=0;
 let witness=null,globalWitness=null,groupWitness=null;
 for(const i of ints)for(const j of ints)for(const k of ints)for(const l of ints){
  const D=[[[0,0],i,j],[[0,0],k,l]];
  for(let mask=0;mask<16;mask++){
   const ok=(c,m)=>m===0||!!(mask&(1<<(2*c+m-1)));
   for(const [lo,hi] of mixes)for(const budget of [1,2]){
    const feasible=routes.filter(r=>r.every((m,c)=>ok(c,m))&&r.filter(m=>m!==0).length<=budget);
    const worst=r=>Math.min(...[lo,hi].map(p=>p*D[0][r[0]][0]+(4-p)*D[1][r[1]][0]));
    const best=r=>Math.max(...[lo,hi].map(p=>p*D[0][r[0]][1]+(4-p)*D[1][r[1]][1]));
    const safe=feasible.filter(r=>r.every((m,c)=>D[c][m][0]>=0));
    const value=Math.max(...safe.map(worst)),leaders=safe.filter(r=>worst(r)===value);
    cases++;
    const reference=[];
    for(const r of feasible){
     let low=Infinity,high=-Infinity,groupOK=true;
     for(const x of D[0][r[0]])for(const y of D[1][r[1]]){
      if(x<0||y<0)groupOK=false;
      for(let p=lo;p<=hi;p++){const v=p*x+(4-p)*y;low=Math.min(low,v);high=Math.max(high,v);oracleChecks++;}
     }
     check(low===worst(r)&&high===best(r),"range oracle");routeChecks++;
     if(groupOK)reference.push({r,low});
    }
    const v=Math.max(...reference.map(x=>x.low));
    check(v===value&&leaders.map(r=>r.join()).join(";")===reference.filter(x=>x.low===v).map(x=>x.r.join()).join(";"),"routing oracle");
    if(value>0)robustGain++;if(leaders.every(r=>r[0]===0&&r[1]===0))allFallback++;
    const global=feasible.filter(r=>r[0]===0&&r[1]===0||[1,2].some(m=>r.every((a,c)=>a===(ok(c,m)?m:0))));
    const score=r=>3*(D[0][r[0]][0]+D[0][r[0]][1])+(D[1][r[1]][0]+D[1][r[1]][1]);
    const pick=rs=>rs.reduce((a,b)=>score(b)>score(a)?b:a,rs[0]);
    const g=pick(global),q=pick(feasible);
    const gs=global.filter(r=>r.every((m,c)=>D[c][m][0]>=0));
    const gv=Math.max(...gs.map(worst));
    check(value>=gv,"global subset");if(value>gv){specializedGain++;if(!witness)witness={D,mask,mix:[lo,hi],budget,leaders,value,globalRobust:gv};}
    const gu=g.some((m,c)=>D[c][m][0]<0),qu=q.some((m,c)=>D[c][m][0]<0);
    if(gu){unsafeGlobal++;if(!globalWitness)globalWitness={D,mask,mix:[lo,hi],budget,global:g,globalRange:[worst(g),best(g)],leaders,value};}
    if(qu)unsafeLocal++;
    if(!gu&&worst(g)<value)globalShortfall++;
    if(!qu&&worst(q)<value)localShortfall++;
    if(Math.max(...feasible.map(worst))>value)groupBlocks++;
    const ungatedGlobal=Math.max(...global.map(worst));
    if(ungatedGlobal>gv){globalGroupBlocks++;if(!groupWitness)groupWitness={D,mask,mix:[lo,hi],budget,ungatedGlobal,gatedGlobal:gv,flexibleGated:value,globalLeaders:global.filter(r=>worst(r)===ungatedGlobal)};}
    if(mask!==15)ineligibleCases++;
   }
  }
 }
 const gate=x=>x.approved&&x.sameTarget&&x.sameVersion&&x.sameContext&&x.validEvidence&&x.resources&&x.scope&&!x.revoked;
 const good={approved:true,sameTarget:true,sameVersion:true,sameContext:true,validEvidence:true,resources:true,scope:true,revoked:false,score:999};
 let controls=0;check(gate(good),"positive");controls++;
 for(const k of ["approved","sameTarget","sameVersion","sameContext","validEvidence","resources","scope"]){check(!gate({...good,[k]:false}),"ineligible");controls++;}
 check(!gate({...good,revoked:true}),"revoked");controls++;
 check(specializedGain>0&&unsafeGlobal>0&&groupBlocks===0&&globalGroupBlocks>0,"nontrivial");
 return {cases,oracleChecks,routeChecks,robustGain,specializedGain,unsafeLocal,unsafeGlobal,globalShortfall,localShortfall,groupBlocks,globalGroupBlocks,allFallback,ineligibleCases,controls,witness,globalWitness,groupWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际输出
```json
{
  "cases": 124416,
  "oracleChecks": 5806080,
  "routeChecks": 435456,
  "robustGain": 19343,
  "specializedGain": 7334,
  "unsafeLocal": 0,
  "unsafeGlobal": 5808,
  "globalShortfall": 5614,
  "localShortfall": 483,
  "groupBlocks": 0,
  "globalGroupBlocks": 801,
  "allFallback": 39366,
  "ineligibleCases": 116640,
  "controls": 9,
  "witness": {
    "D": [
      [
        [
          0,
          0
        ],
        [
          -2,
          -2
        ],
        [
          -2,
          -2
        ]
      ],
      [
        [
          0,
          0
        ],
        [
          -2,
          -2
        ],
        [
          2,
          2
        ]
      ]
    ],
    "mask": 10,
    "mix": [
      1,
      3
    ],
    "budget": 1,
    "leaders": [
      [
        0,
        2
      ]
    ],
    "value": 2,
    "globalRobust": 0
  },
  "globalWitness": {
    "D": [
      [
        [
          0,
          0
        ],
        [
          -2,
          -2
        ],
        [
          -2,
          2
        ]
      ],
      [
        [
          0,
          0
        ],
        [
          -2,
          -2
        ],
        [
          0,
          2
        ]
      ]
    ],
    "mask": 10,
    "mix": [
      0,
      4
    ],
    "budget": 2,
    "global": [
      2,
      2
    ],
    "globalRange": [
      -8,
      8
    ],
    "leaders": [
      [
        0,
        0
      ],
      [
        0,
        2
      ]
    ],
    "value": 0
  },
  "groupWitness": {
    "D": [
      [
        [
          0,
          0
        ],
        [
          -2,
          -2
        ],
        [
          2,
          2
        ]
      ],
      [
        [
          0,
          0
        ],
        [
          -2,
          -2
        ],
        [
          -2,
          -2
        ]
      ]
    ],
    "mask": 10,
    "mix": [
      3,
      4
    ],
    "budget": 2,
    "ungatedGlobal": 4,
    "gatedGlobal": 0,
    "flexibleGated": 6,
    "globalLeaders": [
      [
        2,
        2
      ]
    ]
  }
}
```
## 接入
B04/B06/B08/B10/B11候选增量。先按目标及真实输入发现已准入模型，再匹配任务类别、评价合同、版本、证据适用期；不同科学解释并行，不由单一评分淘汰。性能权重与价值权重分离。对同目标替代模型报告条件净收益范围、适用类别、样本截止、回退理由；无可靠证据时基线/条件比较/UNKNOWN。必需风险检查不可因优化省略；资源不足标未完成。类别、版本、证据、权限变化后重算；禁止自动上线、训练、改变偏好或将合成表现当现实概率。独立轨预留未见类别、错误分类、选择性反馈、同名异目标、重复来源、漂移、权限失效、基线不适用、耦合资源与成本不明；数据轨核查分层留出和运输性；模型轨研究多类别联合分布及组合策略；产品轨审查解释及负担。未运行正式产品、原生方法、Qwen、Mac/iPhone、真人/历史数据或独立验收；无生产修改、Codex、CI、训练、合并、部署、冻结协议变更，零新增费用。
