# 第38轮：跨准则一致性、精确条件优选区间与重复模型投票反例
2026-11-24。起点 main 27260f3363dffe6cd233232f318d13af7e032681；PR #61 固定 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。核对 v3.1、AGENTS、同步规程、近期提交/开放PR、唯一产品交接 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第4/32/37轮及第34轮完整版本范围（本会话前轮已读取），另查 consensus/disagreement/criterion/Hurwicz 提交关键词，未发现同一专项（搜索不保证全库去重）。实际审阅 decision_planner.py blob f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b 的 _comparison、_model_disagreements：已有不同领导集合、不同规则、信息规则分歧提示；第四轮已有两准则比较和合同门控；第32轮已有权重极值和共享误差；第37轮研究条件策略。此轮新增三准则共同最优集合、连续概率区间内每行动的精确最优区域、重复投票与两两相交反例。不重复登记既有模型，不声称现有planner实际错误投票。只使用仓库固定源码作为设计上下文，以下为原创有限数学推导与虚构开发集。
## 数学合同
三个通过已确认硬约束的固定行动，共同基数效用，两个互斥穷尽且可比的未来状态，效用表固定。p为状态0的概率参数，若实际有可信区间[L,H]可使用；否则仅以显式假设的参数区间做敏感性分析，不能声称真实概率，也不能用区间中点作为默认概率。三准则为最大最小效用、最小最大后悔、期望效用。前两者不要求概率；期望准则只在概率和效用有适当资格时可支持现实建议。对照实验假设三准则均可比较，实际系统不得未经用户确认将它们设成同等重要或完整偏好集。
对行动a，E_a(p)=u(a,1)+p*(u(a,0)-u(a,1))。每个竞争行动b给出 c+s*p>=0 的半空间，其中c=u(a,1)-u(b,1)，s=u(a,0)-u(a,1)-u(b,0)+u(b,1)。s正时下界为-c/s，s负时上界为-c/s，s=0时c<0意味着无解；与[L,H]求交得到闭区间I_a或空集。端点并列保留，单点最优也保留。由于线性，一行动全区间领先等价同时在两个端点领先；但可能领先集合不能仅取端点的并集。
定义M为最大最小领导集合，R为最小最大后悔领导集合，E_all为I_a覆盖[L,H]的行动集，E_any为I_a非空的行动集。共同稳定集合=M∩R∩E_all；可有条件共同领先=M∩R∩E_any。若前者非空则这些行动对列出的全部准则及区间内所有概率均最优，可为并列；若前者空且后者非空，则只能展示其各自成立的p区间；若后者空则在该区间没有三准则共同领先。没有共同领先不代表没有可行行动。仅为已纳入的合同范围内证书，未知/失效/不可比的必需准则不得被静默删去后宣布完整一致。不同目标、时域、效用尺度或结构性行动集先隔离，不能直接求交；同合同算法数值矛盾先复算而非投票。即使共同最优也可能含弱支配行动（例如并列最差状态），需展示完整Pareto关系并经用户确认次级规则，不能擅自打破平局。
多数票不是独立证据；复制相同准则或同来源模型可改变投票结果。本轮对照给每准则每个并列领先行动一票，期望准则用区间中点（故意的简化基线）；重复期望准则3次与1次比较。此票制不推荐上线。三个集合两两相交也不能代替全体相交。
## 执行
本轮实际在JS工具执行下列原函数。所有5^6整数效用表，15个四分位闭区间；用半空间相交计算精确分数区间，再以所有竞争直线交点及相邻开区间中点独立算法核查每一查询点领导集合、可能领导和全域领导。整数交叉乘法，当前小数值不超JS安全整数范围；不是任意规模高精度实现。相同研究者设计两路径，不属独立验收。coarseMiss为四分位采样漏掉可能领先行动的案例，endpointMiss为仅端点漏掉行动的案例；clones为复制同准则改变票选领先集合，cloneUniqueFlip为两侧唯一且不同；dominatedLeader为共同稳定集合含至少一弱支配行动。所有频数只代表枚举设计，非现实概率或用户表现。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 const A=[0,1,2],eq=(a,b)=>a.join(",")===b.join(","),inter=(...sets)=>A.filter(a=>sets.every(s=>s.includes(a)));
 const leaders=values=>A.filter(a=>values[a]===Math.max(...values));
 const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
 const frac=(n,d=1)=>d<0?[-n,-d]:[n,d];
 const score=(u,p)=>u.map(([x,y])=>x*p[0]+y*(p[1]-p[0]));
 function regions(u,lo,hi){
  return A.map(a=>{
   let l=lo,h=hi;
   for(const b of A){
    const c=u[a][1]-u[b][1],s=u[a][0]-u[a][1]-u[b][0]+u[b][1];
    if(s===0){if(c<0)return null;continue;}
    const t=frac(-c,s);
    if(s>0&&cmp(t,l)>0)l=t;
    if(s<0&&cmp(t,h)<0)h=t;
    if(cmp(l,h)>0)return null;
   }
   return [l,h];
  });
 }
 let tables=0,cases=0,common=0,conditional=0,none=0,coarseMiss=0,endpointMiss=0,clones=0,cloneUniqueFlip=0,dominatedLeader=0,oracleChecks=0;
 let example=null,miss=null,cloneExample=null;
 for(let n=0;n<15625;n++){
  let z=n;const u=A.map(()=>{const x=z%5;z=Math.floor(z/5);const y=z%5;z=Math.floor(z/5);return [x,y]});tables++;
  const mm=leaders(u.map(v=>Math.min(...v)));
  const best=[0,1].map(w=>Math.max(...u.map(v=>v[w])));
  const mr=leaders(u.map(v=>-Math.max(best[0]-v[0],best[1]-v[1])));
  const weakDom=A.filter(a=>A.some(b=>b!==a&&u[b][0]>=u[a][0]&&u[b][1]>=u[a][1]&&u[b].some((x,w)=>x>u[a][w])));
  for(let l=0;l<=4;l++)for(let h=l;h<=4;h++){
   const lo=[l,4],hi=[h,4],r=regions(u,lo,hi);cases++;
   const possible=A.filter(a=>r[a]!==null),always=A.filter(a=>r[a]&&cmp(r[a][0],lo)===0&&cmp(r[a][1],hi)===0);
   // Independent arrangement oracle: all in-range pairwise ties and midpoints, evaluate exact integer numerators.
   let pts=[lo,hi];
   for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){
    const d0=u[a][0]-u[b][0],d1=u[a][1]-u[b][1];
    if(d0!==d1){const t=frac(d1,d1-d0);if(cmp(t,lo)>=0&&cmp(t,hi)<=0)pts.push(t);}
   }
   pts.sort(cmp);pts=pts.filter((v,i)=>i===0||cmp(v,pts[i-1])!==0);
   const queries=[...pts];for(let i=1;i<pts.length;i++){const [a,b]=pts[i-1],[c,d]=pts[i];queries.push([a*d+c*b,2*b*d]);}
   const oracle=queries.map(p=>leaders(score(u,p)));oracleChecks+=queries.length;
   check(eq(possible,A.filter(a=>oracle.some(s=>s.includes(a))))&&eq(always,inter(...oracle)),"region oracle");
   for(let i=0;i<queries.length;i++)check(eq(oracle[i],A.filter(a=>r[a]&&cmp(queries[i],r[a][0])>=0&&cmp(queries[i],r[a][1])<=0)),"point membership");
   const stable=inter(mm,mr,always),compatible=inter(mm,mr,possible);
   if(stable.length)common++;else if(compatible.length){conditional++;if(!example)example={u,lo,hi,mm,mr,possible,always,compatible,regions:r};}else none++;
   const coarse=A.filter(a=>Array.from({length:h-l+1},(_,j)=>leaders(score(u,[j+l,4]))).some(s=>s.includes(a)));
   if(!eq(coarse,possible)){coarseMiss++;if(!miss)miss={u,lo,hi,coarse,possible,regions:r};}
   const endpoints=A.filter(a=>[lo,hi].some(p=>leaders(score(u,p)).includes(a)));
   if(!eq(endpoints,possible))endpointMiss++;
   const ep=leaders(score(u,[l+h,8]));
   const votes=k=>leaders(A.map(a=>Number(mm.includes(a))+Number(mr.includes(a))+k*Number(ep.includes(a))));
   const v1=votes(1),v3=votes(3);
   if(!eq(v1,v3))clones++;
   if(v1.length===1&&v3.length===1&&!eq(v1,v3)){cloneUniqueFlip++;if(!cloneExample)cloneExample={u,lo,hi,mm,mr,ep,v1,v3};}
   if(stable.some(a=>weakDom.includes(a)))dominatedLeader++;
  }
 }
 let pairwiseOnly=0,pairExample=null;const sets=Array.from({length:7},(_,i)=>A.filter(a=>(i+1)&(1<<a)));
 for(const x of sets)for(const y of sets)for(const z of sets)if(inter(x,y).length&&inter(x,z).length&&inter(y,z).length&&!inter(x,y,z).length){pairwiseOnly++;if(!pairExample)pairExample=[x,y,z];}
 check(common+conditional+none===cases,"partition");
 check(cloneUniqueFlip>0&&coarseMiss>0&&pairwiseOnly>0,"counterexamples");
 return {tables,cases,oracleChecks,common,conditional,none,coarseMiss,endpointMiss,clones,cloneUniqueFlip,dominatedLeader,pairwiseOnly,pairCases:343,example,miss,cloneExample,pairExample};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "tables": 15625,
  "cases": 234375,
  "oracleChecks": 681179,
  "common": 174219,
  "conditional": 35586,
  "none": 24570,
  "coarseMiss": 216,
  "endpointMiss": 1446,
  "clones": 29082,
  "cloneUniqueFlip": 13956,
  "dominatedLeader": 0,
  "pairwiseOnly": 6,
  "pairCases": 343,
  "example": {
    "u": [
      [
        0,
        1
      ],
      [
        1,
        0
      ],
      [
        0,
        0
      ]
    ],
    "lo": [
      0,
      4
    ],
    "hi": [
      3,
      4
    ],
    "mm": [
      0,
      1,
      2
    ],
    "mr": [
      0,
      1,
      2
    ],
    "possible": [
      0,
      1
    ],
    "always": [],
    "compatible": [
      0,
      1
    ],
    "regions": [
      [
        [
          0,
          4
        ],
        [
          1,
          2
        ]
      ],
      [
        [
          1,
          2
        ],
        [
          3,
          4
        ]
      ],
      null
    ]
  },
  "miss": {
    "u": [
      [
        0,
        4
      ],
      [
        1,
        2
      ],
      [
        2,
        0
      ]
    ],
    "lo": [
      0,
      4
    ],
    "hi": [
      3,
      4
    ],
    "coarse": [
      0,
      2
    ],
    "possible": [
      0,
      1,
      2
    ],
    "regions": [
      [
        [
          0,
          4
        ],
        [
          2,
          3
        ]
      ],
      [
        [
          2,
          3
        ],
        [
          2,
          3
        ]
      ],
      [
        [
          4,
          6
        ],
        [
          3,
          4
        ]
      ]
    ]
  },
  "cloneExample": {
    "u": [
      [
        1,
        2
      ],
      [
        2,
        0
      ],
      [
        0,
        0
      ]
    ],
    "lo": [
      2,
      4
    ],
    "hi": [
      4,
      4
    ],
    "mm": [
      0
    ],
    "mr": [
      0
    ],
    "ep": [
      1
    ],
    "v1": [
      0
    ],
    "v3": [
      1
    ]
  },
  "pairExample": [
    [
      0,
      1
    ],
    [
      0,
      2
    ],
    [
      1,
      2
    ]
  ]
}
```
## 接入与验收
B06/B07/B08增量：可信中枢先校验统一决策快照、底线、行动范围、目标、效用、概率来源、准则身份及依赖；以语义准则身份去重而非模型版本投票。对确认的准则分别计算完整领先集，按上述合同给出稳定/条件/无共同/UNKNOWN；不把模型数、权重空间比例、p区间长度或重复票数称作现实概率。首答可以显示“在所列规则下有共同选择”或“要在保护最低结果与减少错过收益之间取舍”，只在分歧改变行动且用户未确定偏好时提出关键问题。允许查看精确边界、并列和各自依据。真实概率缺失时，仅条件展示期望曲线，并单独报告无概率准则结果。未知必需准则与不适用准则分开。若采用Pareto作为显式次级原则须获得用户同意并记录。连续多状态、共同效用不确定、联合参数域、不同策略/时限、证据分级和真实产品接入均待审。独立轨应使用未见非四分位边界、仅单点领先、并列、弱支配、重复方法、未知必需准则和同合同错误案例；模型轨复核更高维适用条件，产品轨验证白话解释及用户负担。本轮不增加生产方法、不运行原生planner、Qwen、真实设备或独立验收，不启动Codex、CI、训练、合并、部署、修改冻结协议或产生新增费用。
