# 长期个人决策：信息揭晓时间约束下的资金前沿与共同续策
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线与范围
同一手动轮第二阶段，起点main 76a3f2780b3c579fdad1089148bd9963e31e353f。沿用前阶段已核对v3.2、同步规程、25近期提交、15开放PR、固定交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf；未重跑原生。实际读取并执行 research/decision_hub/2026-11-26-time-varying-task-cost-liquidity-dp.md blob 56f16ddab494b41aa07852045653fbdf20f28341 的valid/actions/solve/verify。前阶段单世界最低资金，R121已有两阶段相关工时观察与共同预留、R101已有账本与开环规划、R42/R43已有动态反馈，故不重复宣称发明非预知规划、Pareto或DP。本轮新增同一时间变化任务支出及逐期现金底线下的二维最低开期资金前沿、共同早期动作、后续信息可用时点与精确共同阈值；全库去重有限。
## 合同与算法
两个联合可能世界，固定任务ID、需求及期限，三个有序期间，各世界的成本、工时容量、情景流入、必付支出和储备可能不同。无概率，已知世界集合、相关性和观察时序由可信宿主提供；信息揭晓前使用共同动作，揭晓期开始可完全区分两世界。此为限制性信息结构；若实际余额、收入、报价或工时在较早时点已经可观测并区分世界，应提前细分信息集，不能声称原限制下结果是所有真实可调策略的最优值。本轮不实现实际信号、部分观察、多次揭晓、调查费用、真实资产、真实资格或授权。未来收入仅情景条件。固定共同初始余额b，各世界后续余额可以不同。所有结果研究只读无授权能力。
对共同剩余需求r和期间t，保留可行策略在两个世界所需开期余额向量(n0,n1)的非支配前沿。各分量较小为好；若A各分量不大于B，则A支配B，后续任何共同前缀的逐分量单调变换不会反转该关系。未揭晓时必须枚举两个世界均合法的同一x，对后继前沿每个向量逐分量应用前阶段递推max(0,当期支出+max(储备,后继需要)-流入)，取非支配集。揭晓后两个世界可独立最小化各自的需要，得到一条二维向量及两条续策；此前相同动作确保剩余需求一致，但金额可以不同。终端仅需求全部完成才有(0,0)。归纳得到有限合同的精确前沿。共同初始余额的最低值为min_前沿 max(n0,n1)；先分别最优化再取最大值只在完整事前观察时正确，不能直接用于未知未来。保留策略见证，验证每世界独立的现金、期限、容量和共同前缀。若无前沿，表示给定信息结构下不存在可行时间方案，即使资金无限；不是现实世界全局不可行。无覆盖证据不得给全称；前沿规模可能指数增长，未做真实CPU/内存预算。
## 实际执行
1500个合成图，两个世界、三个期间、任务需求0..2、容量1..3、单位成本0..3、情景流入0..4、必付与储备0..2。每图分别在第0/1/2/3期揭晓（3等于全过程固定），6000次策略前沿。独立参照直接枚举各任务单位的所有日期分配，去重，直接计算前缀现金需求，再配对两个世界具有共同事前动作的计划，独立两两支配过滤。比较整个向量前沿、最小共同余额、每条策略见证、完整观察下单世界最小值和信息单调性。4专项控制含成本相反、双向前沿、共同时间窗口无解、相同世界。标准JS实际执行两次结果完全一致。计数为合成结构、重复策略与配对计算，非独立用户、现实成功概率或原生产品错误率。
```json
{
  "graphs": 1500,
  "policies": 6000,
  "schedulePairs": 126572,
  "frontierChecks": 6000,
  "states": 20112,
  "generated": 17831,
  "dominated": 4249,
  "branchCombos": 7186,
  "maxFront": 5,
  "perfectOnlyFeasible": 58,
  "delayedRaisesCash": 116,
  "earlyInformationLowersCash": 100,
  "scalarWorldMaxUnderstates": 196,
  "perfectWorldPlanWithoutCommon": 58,
  "clairvoyantFalsePass": 32,
  "controls": 4,
  "example": {
    "ps": [
      {
        "d": [
          2,
          1,
          0
        ],
        "jobs": [
          {
            "release": 0,
            "deadline": 1,
            "cost": [
              3,
              1,
              3
            ]
          },
          {
            "release": 0,
            "deadline": 2,
            "cost": [
              0,
              0,
              3
            ]
          },
          {
            "release": 0,
            "deadline": 2,
            "cost": [
              0,
              1,
              2
            ]
          }
        ],
        "cap": [
          1,
          2,
          3
        ],
        "income": [
          3,
          0,
          3
        ],
        "mandatory": [
          2,
          2,
          2
        ],
        "reserve": [
          0,
          0,
          2
        ]
      },
      {
        "d": [
          2,
          1,
          0
        ],
        "jobs": [
          {
            "release": 0,
            "deadline": 1,
            "cost": [
              1,
              3,
              1
            ]
          },
          {
            "release": 0,
            "deadline": 2,
            "cost": [
              3,
              3,
              1
            ]
          },
          {
            "release": 0,
            "deadline": 2,
            "cost": [
              0,
              3,
              0
            ]
          }
        ],
        "cap": [
          2,
          2,
          3
        ],
        "income": [
          4,
          1,
          4
        ],
        "mandatory": [
          1,
          0,
          0
        ],
        "reserve": [
          2,
          2,
          1
        ]
      }
    ],
    "cash": [
      4,
      6,
      6,
      6
    ]
  }
}
```
## 下游
将前沿及共同计划见证作为长期决策研究端口，和用户已确认的现金流、时段、义务、信息获知时间及可修改权限绑定。继续研究真实可见账本状态与信息集、版本变化下只重算未来部分，以及不能安全省略的状态。研究者选择有限两世界合同、三期、整数、揭晓时间与基线，未经授权为生产政策。未运行真实原生、独立留出、真机或真实数据；未修改生产、交接、冻结、证据等级、PR、训练、部署、主动CI或费用。
## 复算
固定前阶段报告为唯一参数，核心实际在连接器运行两次；Node包装未执行。
```js
const code=require("node:fs").readFileSync(process.argv[2],"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0];
const make=Function(code.split(" const out={graphs:")[0]+"\nreturn {valid,actions,solve,verify,oracle};\n}\nreturn study();");
function experiment(make){
 const {valid,actions,solve,verify}=make(),ck=(v,m)=>{if(!v)throw Error(m)},sum=a=>a.reduce((s,x)=>s+x,0),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),T=3,N=3;
 let seed=20261130;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function front(rows){
  let keep=[];
  for(let r of rows){if(keep.some(s=>s.need.every((n,i)=>n<=r.need[i])))continue;keep=keep.filter(s=>!r.need.every((n,i)=>n<=s.need[i]));keep.push(r)}
  return keep.sort((a,b)=>a.need[0]-b.need[0]||a.need[1]-b.need[1]);
 }
 function solvePair(ps,reveal){
  ps.forEach(valid);ck(eq(ps[0].d,ps[1].d),"fixed demands");ck(Number.isInteger(reveal)&&reveal>=0&&reveal<=T,"reveal");
  let memo=new Map(),states=0,generated=0,dominated=0,branchCombos=0;
  // For a fixed world continuation use the single-world backward threshold recursion
  // over the remaining periods, not a new initial state or future actual balance.
  function one(p,t,rem){
   if(t===T)return rem.every(n=>n===0)?{need:0,plan:[]}:null;
   let best=null;
   for(const a of actions(p,t,rem)){
    let v=one(p,t+1,a.nr);if(!v)continue;
    let b=Math.max(0,p.mandatory[t]+a.cost+Math.max(p.reserve[t],v.need)-p.income[t]);
    if(!best||b<best.need)best={need:b,plan:[a.x,...v.plan]};
   }return best;
  }
  function rec(t,rem){
   if(t===T)return rem.every(n=>n===0)?[{need:[0,0],plans:[[],[]]}]:[];
   const key=t+":"+rem.join(",");if(memo.has(key))return memo.get(key);states++;
   let rows=[];
   if(t===reveal){
    const a=one(ps[0],t,rem),b=one(ps[1],t,rem);branchCombos++;
    if(a&&b)rows=[{need:[a.need,b.need],plans:[a.plan,b.plan]}];
   }else{
    const aa=actions(ps[0],t,rem),bb=new Map(actions(ps[1],t,rem).map(a=>[a.x.join(","),a]));
    for(let a of aa){let b=bb.get(a.x.join(","));if(!b)continue;
     for(let v of rec(t+1,a.nr)){
      let need=[a,b].map((q,i)=>Math.max(0,ps[i].mandatory[t]+q.cost+Math.max(ps[i].reserve[t],v.need[i])-ps[i].income[t]));
      rows.push({need,plans:v.plans.map(p=>[a.x,...p])});
     }
    }
   }
   generated+=rows.length;const f=front(rows);dominated+=rows.length-f.length;memo.set(key,f);return f;
  }
  const f=rec(0,ps[0].d);let best=null;
  for(let v of f)if(!best||Math.max(...v.need)<Math.max(...best.need))best=v;
  return {front:f,best:best?{cash:Math.max(...best.need),...best}:null,states,generated,dominated,branchCombos};
 }
 // Independent schedule generation: enumerate dated placement of each task unit,
 // deduplicate repeated placements, evaluate prefix deficit directly.
 function schedules(p){
  let u=[];for(let i=0;i<N;i++)for(let k=0;k<p.d[i];k++)u.push(i);
  let a=Array.from({length:T},()=>Array(N).fill(0)),rows=new Map();
  function walk(k){
   if(k===u.length){
    let key=JSON.stringify(a);if(rows.has(key))return;
    let v=0,b=0;
    for(let t=0;t<T;t++){v+=p.mandatory[t]+sum(a[t].map((n,i)=>n*p.jobs[i].cost[t]))-p.income[t];b=Math.max(b,v+p.reserve[t]);}
    rows.set(key,{plan:a.map(x=>x.slice()),need:b});return;
   }
   let i=u[k],j=p.jobs[i];
   for(let t=j.release;t<=j.deadline;t++)if(sum(a[t])<p.cap[t]){a[t][i]++;walk(k+1);a[t][i]--}
  }
  walk(0);return [...rows.values()];
 }
 function ref(ss,reveal){
  let pairs=[],checks=0;
  for(let a of ss[0])for(let b of ss[1]){
   checks++;if(eq(a.plan.slice(0,reveal),b.plan.slice(0,reveal)))pairs.push([a.need,b.need]);
  }
  let unique=[...new Map(pairs.map(x=>[x.join(","),x])).values()];
  let f=unique.filter(a=>!unique.some(b=>b.every((n,i)=>n<=a[i])&&b.some((n,i)=>n<a[i]))).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  return {f,cash:f.length?Math.min(...f.map(x=>Math.max(...x))):null,checks};
 }
 const out={graphs:0,policies:0,schedulePairs:0,frontierChecks:0,states:0,generated:0,dominated:0,branchCombos:0,maxFront:0,perfectOnlyFeasible:0,delayedRaisesCash:0,earlyInformationLowersCash:0,scalarWorldMaxUnderstates:0,perfectWorldPlanWithoutCommon:0,clairvoyantFalsePass:0,controls:0,example:null};
 for(let g=0;g<1500;g++){
  const d=[1+rnd(2),1+rnd(2),rnd(2)],jobs=Array.from({length:N},()=>{let release=rnd(2),deadline=release+rnd(T-release);return {release,deadline}});
  const ps=Array.from({length:2},()=>({d,jobs:jobs.map(j=>({...j,cost:Array.from({length:T},()=>rnd(4))})),cap:Array.from({length:T},()=>1+rnd(3)),income:Array.from({length:T},()=>rnd(5)),mandatory:Array.from({length:T},()=>rnd(3)),reserve:Array.from({length:T},()=>rnd(3))}));
  const ss=ps.map(schedules),rs=[];
  for(let reveal=0;reveal<=T;reveal++){
   const p=solvePair(ps,reveal),o=ref(ss,reveal),f=p.front.map(v=>v.need);
   ck(eq(f,o.f)&&(p.best?.cash??null)===o.cash,"front and scalar parity");out.frontierChecks++;out.policies++;out.schedulePairs+=o.checks;out.states+=p.states;out.generated+=p.generated;out.dominated+=p.dominated;out.branchCombos+=p.branchCombos;out.maxFront=Math.max(out.maxFront,f.length);
   for(let row of p.front){ck(eq(row.plans[0].slice(0,reveal),row.plans[1].slice(0,reveal)),"nonanticipation");for(let i=0;i<2;i++)ck(verify(ps[i],row.plans[i],row.need[i])!==null,"world witness")}
   rs.push(p.best?.cash??null);
  }
  const ind=ps.map(p=>solve(p).best?.need??null);
  ck(rs[0]===(ind.includes(null)?null:Math.max(...ind)),"full observation equals scalar minima");
  for(let r=1;r<=T;r++)ck(rs[r]===null||rs[r-1]!==null&&rs[r-1]<=rs[r],"information monotonic");
  if(rs[0]!==null&&rs[T]===null){out.perfectOnlyFeasible++;out.perfectWorldPlanWithoutCommon++}
  if(rs[0]!==null&&rs[T]!==null&&rs[0]<rs[T]){out.scalarWorldMaxUnderstates++;out.example??={ps,cash:rs}}
  if(rs[1]!==null&&rs[0]<rs[1])out.delayedRaisesCash++;
  if(rs[1]!==null&&rs[T]!==null&&rs[1]<rs[T])out.earlyInformationLowersCash++;
  let b=rnd(12);
  if(rs[0]!==null&&b>=rs[0]&&(rs[1]===null||b<rs[1]))out.clairvoyantFalsePass++;
  out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const base={d:[1,0,0],jobs:[{release:0,deadline:1,cost:[0,4,0]},{release:0,deadline:2,cost:[0,0,0]},{release:0,deadline:2,cost:[0,0,0]}],cap:[1,1,0],income:[0,0,0],mandatory:[0,0,0],reserve:[0,0,0]};
 let ps=[base,{...base,jobs:[{...base.jobs[0],cost:[4,0,0]},...base.jobs.slice(1)]}];
 ctl(solvePair(ps,0).best.cash===0&&solvePair(ps,1).best.cash===4,"information cost");
 ctl(solvePair(ps,3).front.length===2,"tradeoff retained");
 ps=[{...base,cap:[1,0,0]},{...base,cap:[0,1,0]}];
 ctl(solvePair(ps,0).best!==null&&solvePair(ps,3).best===null,"no common schedule");
 ctl(solvePair([base,base],3).best.cash===solve(base).best.need,"same world");
 return out;
}
console.log(JSON.stringify(experiment(make),null,2));
```
