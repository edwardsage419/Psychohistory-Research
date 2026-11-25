# 自主认知专项累计第121轮候选：相关工时不确定性与观察后调度
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / BOUNDED_TWO_STAGE_POLICY / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main 68ef01baa1a7d4a6469904094e99d1028dca7912。核对近12提交、13开放PR（#61待审）、v3.2前15行及历史全文、唯一交接前18行、R120前19行及实际源码、R42/R43前段、C036前20行。C036研究两阶段可调可行量词；R42/R43研究动态反馈及部分观察；本轮连接实际R120连续/可拆调度和R119/R118日期资格，在共享时段具体合同中检验相关工时、共同事前动作及不同观察支持，不重复通用递推或训练。
## 固定资产
research/decision_hub/2026-11-25-contiguous-task-window-feasibility.md 089e7d446004f5303a26a6de25ff328fc857295e
research/decision_hub/2026-11-25-anchored-deadline-shared-time-feasibility.md e5a2b2921d9c810b82a1e449200b17caf987cf7d
research/decision_hub/2026-11-25-civil-temporal-anchor-version-replay.md cc9f6c6103e4ac863d2cdaa6961721149fd4189a
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
R42 1d69fe923238f56fb8fb1f822c366335182f89ed；R43 0eb4141f42b9e1607c8f4fe4122f6cc6cb699320；C036 d2438afcc93f8568cb3a0ef00285fa2f66b34f23；唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07。无新外部资料、真实用户或日历。
## 合同
四日、每天3抽象小时位置，沿R120容量布局、A连续确定1/2小时及已锚定期限/释放日，B连续、C可拆，二者均第2日才释放且固定第4日截止。B/C需求联合支持为四个(1,1),(1,2),(2,1),(2,2)的任意非空子集；没有概率、相关系数或真实工时估计。事前第1日只允许完成A的整个连续块或空闲；其余时段在第2日观察后一次性共同预留，各信号可选不同计划。无进一步观察、重规划、任务取消、现金、资源波动、违约或信息成本。观察支持：无信号区分；完全辨别；混合信号0仅在低低及两个混合世界可能，1在高高及两个混合世界可能。信号无概率；真实发生域外信号未知。独立确认支持、观察时序、可调权限、任务和日期资格由研究者夹具提供，布尔qualified非真实授权。R119 project核验锚定日期；工时支持外部设定，未实现真实来源资格、真实持久化或权限。只运行固定日容量位图，evaluate未作为生产完整输入schema或资源防护。
## 数学
对给定早期占用m，某信号的共同预留可行，当且仅当该组各任务的最大工时向量可排程。必要性：若每个任务拥有同一固定预留集合，须容纳该任务在信号相容世界中的最大需求；充分性：按最大值排程，较短连续任务取其连续块前缀，可拆任务取子集，剩余不再分配。这里是共同预约合同而非所有世界实际同时达到各自最大值；最大向量可能不属于真实联合支持，不能称其为真实环境。不同信号分别求最大值，所有可能信号均有续策且共享同一事前动作才有给定域保证。R120 solve实际给出分支预约及validate；独立参照使用原R120逐实际时段分配oracle，独立枚举早期块与信号组。两计算路径同研究者，均依赖相同已说明最大值定理，非独立证明或验收。完整已知世界可行性是信息尚未揭晓的上界；不以逐世界存在解代替共同政策。完全观察至少不弱于混合，混合至少不弱于无观察。给定有限支持保证不等于真实成功，支持缺失、观察未确认或输入不合格为UNKNOWN，所有authority NONE。此合同因A确定且早做无额外成本，可能无逐世界与共同首动作差异；保留实测零结果，不推广一般性。盒形外包对照是无依据补充联合世界，保守损失不能当现实风险。
## 实验
12容量×2布局×2 A工时×2释放日×2 A期限×15非空支持=2880个合成情景，每情景3种信息结构共8640个政策参照检查。记录逐世界检查次数、可行分支预约核验、信息改善、联合外包保守损失；计数非独立用户、概率或效果估计。12专项控制。R120固定小域递归预算未覆盖所有分支/候选/真实时间内存，未验证生产设备性能。研究者选择任务、支持、观察合同和容量。无训练、Codex、CI、原生、PR合并、部署、新费用或冻结变化。产品轨维护唯一交接。
## 复算
按上述五文件顺序置入docs[i].content。Node标准JS，仅执行已审查项目自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const P=Function(c.split("function experiment(P)")[0]+"\nreturn load;")()(docs.slice(1));
 return {P,S:Function("P",c.slice(c.indexOf("function experiment(P)")).split(" let out={pairs:")[0]+"\nreturn {calendar,solve,oracle,validate,placements};\n}\nreturn experiment(P);")(P)}
}
function experiment(P,S){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const worlds=[[1,1],[1,2],[2,1],[2,2]];
 // Observation is externally specified: before any uncertain job starts.
 // Signal maps may overlap; each possible signal must work.
 const signals={none:()=>[0],full:i=>[i],noisy:i=>i===0?[0]:i===3?[1]:[0,1]};
 function evaluate(req,available,support,mode,qualified=true){
  if(!qualified||!Array.isArray(support)||!support.length||support.some(i=>!Number.isInteger(i)||i<0||i>=4)||new Set(support).size!==support.length||!Object.hasOwn(signals,mode))return {status:"UNKNOWN",authority:"NONE"};
  const plain=P.project(req,P.sources,P.anchors);if(!plain)return {status:"UNKNOWN",authority:"NONE"};
  const jobs=plain.map((j,i)=>({...j,block:i!==2}));
  if(jobs.length!==3||jobs[1].r<1||jobs[2].r<1)return {status:"UNKNOWN",authority:"NONE"};
  const make=(a,b,c)=>[{...jobs[0],h:a},{...jobs[1],h:b},{...jobs[2],h:c}];
  let possible=support.map(i=>({i,ok:S.solve(make(jobs[0].h,...worlds[i]),available).status==="FEASIBLE"}));
  const groups=[...new Set(support.flatMap(signals[mode]))].map(signal=>({signal,worlds:support.filter(i=>signals[mode](i).includes(signal))}));
  const early=S.placements(jobs[0],available).filter(m=>(m&7)===m); // A continuous, all or nothing on day 0
  const choices=[...new Set([0,...early])],safe=[],remaining=available&~7;
  for(let m of choices){
   const a=m?0:jobs[0].h,branches=[];
   for(let g of groups){
    const b=Math.max(...g.worlds.map(i=>worlds[i][0])),c=Math.max(...g.worlds.map(i=>worlds[i][1]));
    const j=make(a,b,c).map(x=>({...x,r:Math.max(1,x.r)}));
    let z=S.solve(j,remaining);
    if(z.status!=="FEASIBLE")break;
    ck(S.validate(z,j,remaining),"branch certificate");branches.push({signal:g.signal,worlds:g.worlds,requirements:[a,b,c],schedule:z.schedule})
   }
   if(branches.length===groups.length)safe.push({day0:m,branches})
  }
  return {status:safe.length?"GUARANTEED_IN_DOMAIN":possible.some(x=>x.ok)?"POSSIBLE_NOT_GUARANTEED":"NO_FEASIBLE_WORLD",possible,safe,authority:"NONE"}
 }
 // Independent policy oracle: enumerate early choices and assign future slots
 // using the prior round's direct enumeration. For each observation group
 // test a common reservation by enumerating all actual assignments at maxima.
 function reference(req,available,support,mode){
  let j=P.project(req,P.sources,P.anchors).map((x,i)=>({...x,block:i!==2}));
  let possible=support.map(i=>S.oracle(j.map((x,k)=>({...x,h:k===0?x.h:worlds[i][k-1]})),available));
  let early=[0];
  for(let start=0;start+j[0].h<=3;start++){let m=((1<<j[0].h)-1)<<start;if(j[0].r===0&&(m&available)===m&&j[0].h>0)early.push(m)}
  let result=[];
  for(let m of early){
   let ok=true;
   for(let sig=0;sig<4;sig++){
    let ws=support.filter(i=>signals[mode](i).includes(sig));if(!ws.length)continue;
    let demand=[m?0:j[0].h,0,0];
    for(let i of ws){demand[1]=Math.max(demand[1],worlds[i][0]);demand[2]=Math.max(demand[2],worlds[i][1])}
    let jobs=j.map((x,k)=>({...x,r:Math.max(1,x.r),h:demand[k]}));
    if(!S.oracle(jobs,available&~7)){ok=false;break}
   }
   if(ok)result.push(m)
  }
  return {possible,safe:result.sort((a,b)=>a-b)}
 }
 let out={cases:0,policyChecks:0,worldChecks:0,branchCertificates:0,noneGuaranteed:0,noisyGuaranteed:0,fullGuaranteed:0,fullInformationUpper:0,noPossible:0,possibleNotGuaranteed:0,informationRescue:0,noisyRescue:0,boxConservativeLoss:0,oraclePrematureGuarantee:0,controls:0,witness:null,boxWitness:null};
 // All 15 nonempty supports, 12 calendars, 2 layouts, 2 A workloads,
 // 2 A releases, 2 A deadlines; B and C both released on day 1.
 for(let cap of P.caps)for(let frag of [false,true])for(let ha of [1,2])for(let ar of [0,1])for(let a of [P.ra,P.ra2]){
  const req={covered:true,capacity:cap,records:[P.record(a,ha,ar),P.record(P.rb2,1,1),P.record(P.rc,1,1)]};
  const available=S.calendar(cap,frag);
  for(let mask=1;mask<16;mask++){
   let support=[0,1,2,3].filter(i=>mask&(1<<i)),z={};
   for(let mode of ["none","noisy","full"]){
    const r=evaluate(req,available,support,mode),o=reference(req,available,support,mode);
    ck(eq(r.possible.map(x=>x.ok),o.possible)&&eq(r.safe.map(x=>x.day0).sort((a,b)=>a-b),o.safe),"policy oracle");
    out.policyChecks++;out.worldChecks+=support.length;out.branchCertificates+=r.safe.reduce((s,x)=>s+x.branches.length,0);z[mode]=r;
    out[mode+"Guaranteed"]+=+(r.status==="GUARANTEED_IN_DOMAIN")
   }
   out.cases++;
   const n=z.none.safe.length>0,f=z.full.safe.length>0,v=z.noisy.safe.length>0,upper=z.full.possible.every(x=>x.ok);
   ck((!n||v)&&(!v||f)&&(!f||upper),"information monotonicity");out.fullInformationUpper+=+upper;
   out.noPossible+=+(z.full.status==="NO_FEASIBLE_WORLD");out.possibleNotGuaranteed+=+(z.full.status==="POSSIBLE_NOT_GUARANTEED");
   out.oraclePrematureGuarantee+=+(upper&&!f);
   if(!n&&f){out.informationRescue++;out.witness??={capacity:cap,fragmented:frag,aHours:ha,aRelease:ar,aDeadline:a.receipt.value.date,support:support.map(i=>worlds[i]),none:z.none.status,full:z.full.safe}}
   out.noisyRescue+=+(!n&&v);
   let bs=[...new Set(support.map(i=>worlds[i][0]))],cs=[...new Set(support.map(i=>worlds[i][1]))],box=worlds.map((w,i)=>bs.includes(w[0])&&cs.includes(w[1])?i:-1).filter(i=>i>=0);
   if(box.length>support.length&&f){let b=evaluate(req,available,box,"full");if(!b.safe.length){out.boxConservativeLoss++;out.boxWitness??={capacity:cap,fragmented:frag,aHours:ha,aRelease:ar,aDeadline:a.receipt.value.date,support:support.map(i=>worlds[i]),box:box.map(i=>worlds[i])}}}
  }
 }
 let req={covered:true,capacity:[2,2,2,2],records:[P.record(P.ra,1,0),P.record(P.rb2,1,1),P.record(P.rc,1,1)]},avail=S.calendar(req.capacity,false);
 for(let t of [()=>out.cases===2880,()=>out.policyChecks===8640,()=>out.noneGuaranteed<=out.noisyGuaranteed&&out.noisyGuaranteed<=out.fullGuaranteed&&out.fullGuaranteed<=out.fullInformationUpper,()=>out.informationRescue>0,()=>out.boxConservativeLoss>0,()=>evaluate(req,avail,[],"full").status==="UNKNOWN",()=>evaluate(req,avail,[0],"full",false).status==="UNKNOWN",()=>evaluate(req,avail,[0,0],"full").status==="UNKNOWN",()=>evaluate(req,avail,[4],"full").status==="UNKNOWN",()=>evaluate(req,avail,[0],"unknown").status==="UNKNOWN",()=>evaluate({...req,covered:false},avail,[0],"full").status==="UNKNOWN",()=>evaluate(req,avail,[0],"full").authority==="NONE"]){ck(t(),"control "+out.controls);out.controls++}
 return out
}
const {P,S}=load(docs);console.log(JSON.stringify(experiment(P,S),null,2));
```
## 实测
```json
{
  "cases": 2880,
  "policyChecks": 8640,
  "worldChecks": 18432,
  "branchCertificates": 1446,
  "noneGuaranteed": 249,
  "noisyGuaranteed": 249,
  "fullGuaranteed": 281,
  "fullInformationUpper": 281,
  "noPossible": 1988,
  "possibleNotGuaranteed": 611,
  "informationRescue": 32,
  "noisyRescue": 0,
  "boxConservativeLoss": 32,
  "oraclePrematureGuarantee": 0,
  "controls": 12,
  "witness": {
    "capacity": [
      0,
      2,
      0,
      2
    ],
    "fragmented": false,
    "aHours": 1,
    "aRelease": 0,
    "aDeadline": "2026-11-25",
    "support": [
      [
        1,
        2
      ],
      [
        2,
        1
      ]
    ],
    "none": "POSSIBLE_NOT_GUARANTEED",
    "full": [
      {
        "day0": 0,
        "branches": [
          {
            "signal": 1,
            "worlds": [
              1
            ],
            "requirements": [
              1,
              1,
              2
            ],
            "schedule": {
              "C": 1536,
              "B": 16,
              "A": 8
            }
          },
          {
            "signal": 2,
            "worlds": [
              2
            ],
            "requirements": [
              1,
              2,
              1
            ],
            "schedule": {
              "C": 16,
              "B": 1536,
              "A": 8
            }
          }
        ]
      }
    ]
  },
  "boxWitness": {
    "capacity": [
      0,
      2,
      0,
      2
    ],
    "fragmented": false,
    "aHours": 1,
    "aRelease": 0,
    "aDeadline": "2026-11-25",
    "support": [
      [
        1,
        2
      ],
      [
        2,
        1
      ]
    ],
    "box": [
      [
        1,
        1
      ],
      [
        1,
        2
      ],
      [
        2,
        1
      ],
      [
        2,
        2
      ]
    ]
  }
}
```
下一步：研究有真实成本的早期决策、可证伪的观测资格及跨现金时间资源联合约束；优先使用独立真实数据。正式开发与训练另获授权。
