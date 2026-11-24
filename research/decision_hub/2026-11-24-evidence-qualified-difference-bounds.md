# 第39轮：证据限定的未知范围推导与差分约束闭包
2026-11-24。固定 main d49e8f17c885686523892bc95a1e00685c99beb1；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR及唯一产品交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第27/37/38轮。审阅原生decision_feasibility.py blob 6181d6c578c7ef251e9708d0ffcf65e95d35f88f、decision_state.py blob 0840855431fbc88fe212785584277aa01be74d93；C028已有闭区间单调门控、单位/时域检查及同指标不相交检查。本轮不重计已有区间判定、有限矩形世界或情景枚举，新增从可信关系推导未知上下界、路径依据、冲突核及证据角色隔离。提交关键词 difference constraints / temporal constraint / shortest path / constraint propagation 查询均未返回结果，不能证明全库不存在类似资料。
## 来源
Dechter, Meiri & Pearl (1991), Temporal constraint networks, Artificial Intelligence 49, 61–95, DOI https://doi.org/10.1016/0004-3702(91)90006-6 。本轮实际查看出版商公开摘要 https://www.sciencedirect.com/science/article/pii/0004370291900066 ，核对简单时间约束与连续变量框架。未阅读全文、未复算论文实验、未复制论文代码或原文；以下闭包证明及脚本为独立推导与原创应用夹具，不能宣称验证论文全部结论。未取得全文再分发许可，未归档原文。
## 数学合同
同一可比量、单位、币种、时域、对象及语义下，把已获资格的闭差分约束 x_j-x_i<=c 记为边 i->j 权重c；固定零点0，绝对区间[l,h]为0->j权重h及j->0权重-l。不可凭空指定有限区间。事实、已验证关系和条件性假设分别构建网络；用户认可估计仍为估计，条件假设不能成为事实；政策底线、目标及优化约束是待检验对象，不得当现实测量事实加入网络。未核验来源/单位/时域或条件不能进入无条件网络。用户确认不等于外部事实核验。真实来源资格由可信宿主提供，本轮角色标记为人工合成。
沿路径累加不等式可得 x_j-x_i<=路径权重；最短路径d(i,j)给出最紧上界，下界为-d(j,i)。负环意味着证据集合矛盾，不存在同时满足的赋值；不得利用空集把所有行动判为可行。无负环时，从i可达节点以d(i,v)赋值可达紧上界；不可达部分可取超级源可行势并整体平移至足够大的有限值，使通向可达部分的边满足（从可达至不可达无边）；最后减去零点势保持x0=0。若j不可达，则通过任意增大该平移量可使差分无有限上界。下界对称。闭约束整数常量的有限极值存在整数见证（上述最短路势及平移），故在已给整数盒内的逐整数穷举可以核对本例连续域差分极值。Floyd-Warshall求闭包O(n^3)；维护对应路径和来源ID。负环后不发布任何该冲突域数值，贪婪逐边删除给出包含意义下不可再删的冲突集合，不保证最小基数或唯一，也不判定哪个事实错误。无穷界显示未知/无有限界，不能替成0或默认区间。两个变量各自的区间重叠仍可能有确定差分；只能将有证据的共同域传给后续模型，不能把所有成对边当独立世界。
## 实际执行
所有3变量各10种整数闭区间(0..3)，3条有向边各4种状态(无/-1/0/1)，共64000组。用闭包与逐整数点穷举核查是否冲突、所有16个有序差分上下界、路径来源与权重；对矛盾网络核查删任一冲突核边即可恢复可满足性。独立计算路径由同一研究者编写，不是独立验收。对于6个非零不同变量有序对及7个阈值，比较只使用初始边际盒与联合闭包的门槛判断，boxFalseUnknown是旧盒未决而联合闭包可证明通过/失败的测试次数，strictGain为至少一项此类改善的网络数。旧盒未决为保守结论，不是错误事实。对矛盾网络不计算优选。额外测试无锚定差分、来源/时域/假设/政策/未知角色隔离、撤去假设和循环证明反例；这些是手工资格标记而非实际认证。路径检查仅一致网络。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 // Edge [from,to,c,id] represents x[to]-x[from]<=c; node 0 is fixed zero.
 function close(edges,n=4){
  const d=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?0:Infinity));
  const p=Array.from({length:n},()=>Array.from({length:n},()=>[]));
  for(const [i,j,c,id] of edges)if(c<d[i][j]){d[i][j]=c;p[i][j]=[id];}
  for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(d[i][k]+d[k][j]<d[i][j]){
   d[i][j]=d[i][k]+d[k][j];p[i][j]=[...p[i][k],...p[k][j]];
  }
  return {d,p,conflict:d.some((r,i)=>r[i]<0)};
 }
 function core(edges){let c=edges.slice();for(const e of edges){const t=c.filter(x=>x!==e);if(close(t).conflict)c=t;}return c;}
 const bounds=[];for(let l=0;l<=3;l++)for(let h=l;h<=3;h++)bounds.push([l,h]);
 const relations=[null,-1,0,1],pairs=[[1,2],[2,3],[3,1]];
 let cases=0,conflicts=0,consistent=0,tightened=0,worlds=0,checks=0,certs=0,coreChecks=0,strictGain=0,boxFalseUnknown=0,boxChecks=0;
 const status=(lo,hi,t)=>hi<=t?"PASS":lo>t?"FAIL":"UNRESOLVED";
 let witness=null;
 for(const a of bounds)for(const b of bounds)for(const c of bounds)for(const x of relations)for(const y of relations)for(const z of relations){
  const box=[a,b,c], rs=[x,y,z],e=[];
  box.forEach(([l,h],j)=>e.push([0,j+1,h,"U"+j],[j+1,0,-l,"L"+j]));
  rs.forEach((v,i)=>{if(v!==null)e.push([...pairs[i],v,"R"+i]);});
  const r=close(e);cases++;
  const pts=[];
  for(let i=a[0];i<=a[1];i++)for(let j=b[0];j<=b[1];j++)for(let k=c[0];k<=c[1];k++){
   const v=[0,i,j,k];if(e.every(([f,t,h])=>v[t]-v[f]<=h))pts.push(v);
  }
  check(r.conflict===(pts.length===0),"conflict oracle");
  if(r.conflict){conflicts++;const m=core(e);check(close(m).conflict&&m.every(q=>!close(m.filter(v=>v!==q)).conflict),"minimal conflict");coreChecks++;continue;}
  consistent++;worlds+=pts.length;
  let tight=false,better=false;
  for(let i=0;i<4;i++)for(let j=0;j<4;j++){
   const hi=Math.max(...pts.map(v=>v[j]-v[i])),lo=Math.min(...pts.map(v=>v[j]-v[i]));
   check(r.d[i][j]===hi&&-r.d[j][i]===lo,"exact bounds");checks++;
   // Verify actual provenance path weight and endpoints, including empty diagonal.
   let at=i,sum=0;
   for(const id of r.p[i][j]){const edge=e.find(q=>q[3]===id);check(edge&&edge[0]===at,"path");at=edge[1];sum+=edge[2];}
   check(at===j&&sum===hi,"path bound");certs++;
   if(i===0&&j>0&&(lo>box[j-1][0]||hi<box[j-1][1]))tight=true;
   if(i===j||i===0||j===0)continue;
   const blo=box[j-1][0]-box[i-1][1],bhi=box[j-1][1]-box[i-1][0];
   for(let t=-3;t<=3;t++){
    const s=status(lo,hi,t),old=status(blo,bhi,t);boxChecks++;
    check(old==="UNRESOLVED"||old===s,"sound box");
    if(old==="UNRESOLVED"&&s!=="UNRESOLVED"){boxFalseUnknown++;better=true;if(!witness)witness={box,relations:rs,from:i,to:j,threshold:t,boxRange:[blo,bhi],exactRange:[lo,hi],status:s};}
   }
  }
  if(tight)tightened++;if(better)strictGain++;
 }
 // One-sided or fully missing bounds stay unbounded.
 const unbounded=close([[1,2,5,"gap"]],3);
 check(!unbounded.conflict&&unbounded.d[0][1]===Infinity&&unbounded.d[1][2]===5&&unbounded.d[2][1]===Infinity,"unbounded");
 // Distinguish evidence, assumption, policy and unknown; source and scope are mock trusted-host metadata.
 function qualified(items,assume=false){return items.filter(x=>x.source&&x.scope==="same"&&(x.role==="fact"||(assume&&x.role==="assumption"))).map(x=>x.edge);}
 const items=[
  {role:"fact",source:"fixture contract",scope:"same",edge:[1,0,-8,"lower"]},
  {role:"policy",source:"user budget",scope:"same",edge:[0,1,10,"budget"]},
  {role:"assumption",source:"conditional estimate",scope:"same",edge:[0,1,9,"estimate"]},
  {role:"fact",source:"other period",scope:"other",edge:[0,1,7,"wrong"]},
  {role:"fact",source:"",scope:"same",edge:[0,1,6,"missing"]},
  {role:"unknown",source:"fixture",scope:"same",edge:[0,1,4,"unknown"]}
 ];
 const factual=close(qualified(items),2),conditional=close(qualified(items,true),2);
 check(factual.d[0][1]===Infinity&&-factual.d[1][0]===8,"no invented cap");
 check(conditional.d[0][1]===9&&status(8,9,10)==="PASS","conditional only");
 const circular=close([...qualified(items),items[1].edge],2);check(circular.d[0][1]===10,"circular counterexample");
 const revoked=close(qualified(items.filter(x=>x.role!=="assumption"),true),2);check(revoked.d[0][1]===Infinity,"revocation");
 const example=close([[0,1,14,"Amax"],[1,0,-10,"Amin"],[1,2,3,"BminusAmax"],[2,1,-2,"BminusAmin"]],3);
 check(example.d[0][2]===17&&-example.d[2][0]===12&&example.d[1][2]===3,"example");
 return {cases,conflicts,consistent,worlds,checks,certs,coreChecks,tightened,strictGain,boxFalseUnknown,boxChecks,witness,unbounded:{absolute:"UNKNOWN",upperDifference:5,lowerDifference:"UNBOUNDED"},sourceControls:{factual:[8,"UNBOUNDED"],conditional:[8,9],circular:[8,10],afterAssumptionRemoval:[8,"UNBOUNDED"]},example:{A:[10,14],B:[12,17],BminusA:[2,3],BUpperPath:example.p[0][2]}};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际输出
```json
{
  "cases": 64000,
  "conflicts": 30298,
  "consistent": 33702,
  "worlds": 144144,
  "checks": 539232,
  "certs": 539232,
  "coreChecks": 30298,
  "tightened": 22164,
  "strictGain": 26163,
  "boxFalseUnknown": 251760,
  "boxChecks": 1415484,
  "witness": {
    "box": [
      [
        0,
        0
      ],
      [
        0,
        0
      ],
      [
        0,
        1
      ]
    ],
    "relations": [
      null,
      null,
      -1
    ],
    "from": 1,
    "to": 3,
    "threshold": 0,
    "boxRange": [
      0,
      1
    ],
    "exactRange": [
      1,
      1
    ],
    "status": "FAIL"
  },
  "unbounded": {
    "absolute": "UNKNOWN",
    "upperDifference": 5,
    "lowerDifference": "UNBOUNDED"
  },
  "sourceControls": {
    "factual": [
      8,
      "UNBOUNDED"
    ],
    "conditional": [
      8,
      9
    ],
    "circular": [
      8,
      10
    ],
    "afterAssumptionRemoval": [
      8,
      "UNBOUNDED"
    ]
  },
  "example": {
    "A": [
      10,
      14
    ],
    "B": [
      12,
      17
    ],
    "BminusA": [
      2,
      3
    ],
    "BUpperPath": [
      "Amax",
      "BminusAmax"
    ]
  }
}
```
## 接入与边界
B02/B05/B06/B08/B10候选增量。自然语言层只提出事实/估计/关系/底线候选及原文位置；用户和可信证据确认语义、单位、范围、角色后才构造边；事实域与每个明确条件域分开闭包，禁止借助底线循环证明符合底线。每个推导记录输入版本、边ID、原始依据、最短路见证、条件身份、上下界与是否有限；证据更正或撤回后重建而非沿用旧收据。阈值单独检查；若事实域已足够则不必追问，若只有假设域通过则标条件性；若冲突先向用户展示一组相关矛盾事实；若无有限界，保留未知并仅询问影响当前判断的信息。所有用户偏好、重要假设和真实外部验证仍按v3.1确认。C028接口是否能表达关系、严格不等式、非线性、和式约束、单位换算、离散选择、跨世界因果关系及概率均未实现于本脚本；开放边界不能擅自闭合；候选不替代原生gate。不同对象/时期等不能因数值相近而连接。独立轨冻结未见非整数、无界、冲突、预算循环、单位混用、证据撤回、多条相等最短路、条件依赖案例；模型轨核查通用求解器及证据合同；产品轨验证是否减少实际追问。当前同源合成测试，不证明真实用户效果、自然语言理解或完整软件能力。未运行原生方法、Qwen、设备、CI，未改生产、启动Codex、训练、合并、部署或变更冻结协议；零新增费用。
