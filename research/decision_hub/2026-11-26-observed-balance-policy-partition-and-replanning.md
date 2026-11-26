# 长期个人决策：已观察余额的信息分组、共同策略与实际进度后的再规划
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线与范围
同一手动轮第三阶段，起点main 1149a741e40f1026c074077e256e3dc5c597251e；沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、固定交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。实际读取并执行 research/decision_hub/2026-11-26-time-varying-task-cost-liquidity-dp.md blob 56f16ddab494b41aa07852045653fbdf20f28341 的valid/actions/verify等固定函数；前阶段资金前沿 aafd3481410faa89972494ddcc5791bbc1f7196a 的信息时点合同、R121部分观察、R124实际成本和R125依赖失效原则沿用，不重复声称发明反馈DP或再规划。新增可观察实际现金余额（由先前动作与世界决定）产生的动态信息分组、历史不重新合并，以及在同一策略的已执行分支上重算剩余工作。查重范围有限。
## 合同与数学
沿用三期、三个任务、固定整数需求、窗口和共同主体，2..3联合世界，成本、流入、容量、必付支出、储备可变。每期开始已知上期真实期末余额及当前外部信号（人工可信夹具），本期流入和支出发生在动作决定后；资源约束对当前同组每个世界均须成立。真实余额未到账、未核对或未获授权不得输入；本实验的余额观察为精确无噪声的合成合同，不代表真实账户已取得。若现金余额没有实际观察，只用信号且保留各世界余额向量；若其他事实已可观察，需将其加入可信信息状态。当前信号与余额相同不抹掉以前不同的观察历史。世界无概率；完整支持与观测真实性外部假设。给定固定开期余额、每个信息组的剩余需求、当前时期及各世界余额向量，未来合同只取决于这些状态。对每组枚举共同合法动作，逐世界更新余额，剔除违反期末底线的动作；以新观察值及新信号对当前组分区，各子组必须存在续策，组间独立选取。若所有共同动作穷尽失败才判该组无策；终端仅需求完成。状态缓存保留组成员及其余额向量；不跨历史合并信息组。证明由信息树归纳：当前不可区分世界必须共享动作，各可区分的观察分支允许不同策略，所有分支通过才保证给定域。独立参照直接枚举每世界合法完整排程，再要求任意两条世界排程在其全部既往观察历史仍相同的各时期动作一致；由此可形成统一非预知策略，反之亦然。所有输出只读authority NONE。未实现搜索预算、持久化、真实授权、对账、预测校准或自动行动。
## 实际实验
1400合成图，2..3世界，两个非零任务；随机容量、成本、流入、必付、储备和开期余额。每图对照无信号且不观测余额、观察实际余额、额外部分信号、完全事前信号四类；直接枚举合法排程及历史相容的策略，核对每个树见证的时间、余额、资格及共同动作。对存在观察余额策略的图，取世界0的已执行第一期动作、已观察余额与其相容世界作为明确夹具，冻结历史后重算第二期起剩余工作；在一个未来世界缩减未来容量再重算，与独立排程参照核对。未模拟真实世界的事后更正、未知任务完成度或收入撤回。4专项控制（实际余额区分、同余额不可区分、额外信号、历史不同不重合）。标准JS核心两次执行一致。计数为合成重复结构，不是独立人次、真实成功概率或真实产品错误率。
```json
{
  "graphs": 1400,
  "policyChecks": 6933,
  "oraclePlans": 28714,
  "states": 34146,
  "actions": 36880,
  "cacheHits": 196,
  "treeChecks": 3170,
  "balanceObservationImproves": 25,
  "partialSignalsImprove": 4,
  "fullSignalsImprove": 21,
  "unobservableFutureFalsePass": 25,
  "replanningChecks": 500,
  "actualHistoryChecks": 500,
  "controls": 4,
  "example": {
    "ps": [
      {
        "d": [
          1,
          2,
          0
        ],
        "jobs": [
          {
            "release": 0,
            "deadline": 1,
            "cost": [
              1,
              1,
              3
            ]
          },
          {
            "release": 1,
            "deadline": 2,
            "cost": [
              0,
              3,
              2
            ]
          },
          {
            "release": 1,
            "deadline": 2,
            "cost": [
              0,
              0,
              1
            ]
          }
        ],
        "cap": [
          2,
          2,
          1
        ],
        "income": [
          4,
          1,
          3
        ],
        "mandatory": [
          2,
          0,
          0
        ],
        "reserve": [
          2,
          2,
          1
        ]
      },
      {
        "d": [
          1,
          2,
          0
        ],
        "jobs": [
          {
            "release": 0,
            "deadline": 1,
            "cost": [
              3,
              2,
              0
            ]
          },
          {
            "release": 1,
            "deadline": 2,
            "cost": [
              2,
              2,
              2
            ]
          },
          {
            "release": 1,
            "deadline": 2,
            "cost": [
              1,
              1,
              3
            ]
          }
        ],
        "cap": [
          3,
          1,
          2
        ],
        "income": [
          0,
          2,
          3
        ],
        "mandatory": [
          1,
          0,
          0
        ],
        "reserve": [
          2,
          2,
          0
        ]
      }
    ],
    "b": 3
  }
}
```
## 下游
当前已执行动作必须由真实观察记录确认，不从旧策略推断已发生。本研究选择合成执行世界用于测试；生产需独立记录实际进度、时间、支出与来源版本，经当前授权核对后重建相容世界与剩余需求。旧条件策略只能作为历史研究记录，不恢复已消耗资源。建议和R125依赖失效、v0.8持久事务及本轮资金前沿接口连接。未修改生产、交接、历史冻结、证据等级、PR、训练、部署、主动CI或费用。研究者选择精确余额观察、有限世界、信号、预算域及合成编辑，未执行原生、独立留出、真机或真实数据验证。
## 复算
固定前序单世界报告为唯一参数，Node包装未执行，连接器实际运行核心。
```js
const code=require("node:fs").readFileSync(process.argv[2],"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0];
const make=Function(code.split(" const out={graphs:")[0]+"\nreturn {valid,actions,solve,verify,oracle};\n}\nreturn study();");
function experiment(make){
 const {valid,actions,verify}=make(),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),sum=a=>a.reduce((s,x)=>s+x,0),T=3,N=3;
 let seed=20261201;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 // At period start, previous end-of-period actual cash and the current qualified signal
 // are observed. Groups never merge, even if observations later coincide.
 function solve(ps,signals,b,observe=true,start=0,initialRem=ps[0].d){
  ps.forEach(valid);ck(ps.every(p=>eq(p.d,ps[0].d))&&signals.length===ps.length&&signals.every(s=>s.length===T)&&Number.isSafeInteger(b)&&b>=0,"scope");
  let states=0,actionsTested=0,cacheHits=0,memo=new Map();
  const split=(ids,t,balances)=>{
   const m=new Map();
   for(let id of ids){
    const k=JSON.stringify([signals[id][t],observe?balances[id]:null]);if(!m.has(k))m.set(k,[]);m.get(k).push(id);
   }return [...m.values()];
  };
  // With no cash observation, balances may differ inside a group; retain vector.
  function rec(ids,t,rem,bal){
   if(t===T)return rem.every(n=>n===0)?[]:null;
   const k=JSON.stringify([ids,t,rem,ids.map(i=>bal[i])]);if(memo.has(k)){cacheHits++;return memo.get(k)}
   states++;let result=null;
   const maps=ids.slice(1).map(i=>new Map(actions(ps[i],t,rem).map(a=>[a.x.join(","),a])));
   for(let a of actions(ps[ids[0]],t,rem)){
    actionsTested++;
    let aa=[a,...maps.map(m=>m.get(a.x.join(",")))];if(aa.some(x=>!x))continue;
    let next={};for(let [j,id] of ids.entries()){let p=ps[id];next[id]=bal[id]+p.income[t]-p.mandatory[t]-aa[j].cost}
    if(ids.some(id=>next[id]<ps[id].reserve[t]))continue;
    if(t===T-1){if(a.nr.every(n=>!n)){result={ids,t,action:a.x,after:next,children:[]};break}continue}
    const groups=split(ids,t+1,next),children=groups.map(g=>rec(g,t+1,a.nr,next));
    if(children.every(c=>c!==null)){result={ids,t,action:a.x,after:next,children};break}
   }
   memo.set(k,result);return result;
  }
  const ids=ps.map((_,i)=>i),bal=Object.fromEntries(ids.map(i=>[i,b]));
  const groups=split(ids,start,bal),children=groups.map(g=>rec(g,start,initialRem,bal));
  return {ok:children.every(c=>c!==null),trees:children.every(c=>c!==null)?children:null,states,actionsTested,cacheHits,authority:"NONE"};
 }
 // Independent whole-schedule enumeration. No DP, no candidate action routine.
 function schedules(p,b,start=0,rem=p.d){
  let units=[];for(let i=0;i<N;i++)for(let k=0;k<rem[i];k++)units.push(i);
  let a=Array.from({length:T},()=>Array(N).fill(0)),rows=new Map();
  function walk(k){
   if(k===units.length){
    let key=JSON.stringify(a);if(rows.has(key))return;let bal=b,history=[];
    for(let t=start;t<T;t++){
     bal+=p.income[t]-p.mandatory[t]-sum(a[t].map((n,i)=>n*p.jobs[i].cost[t]));if(bal<p.reserve[t])return;history.push(bal);
    }
    rows.set(key,{plan:a.map(x=>x.slice()),history});return;
   }
   let i=units[k],j=p.jobs[i];
   for(let t=Math.max(j.release,start);t<=j.deadline;t++)if(sum(a[t])<p.cap[t]){a[t][i]++;walk(k+1);a[t][i]--}
  }
  walk(0);return [...rows.values()];
 }
 function compatible(a,b,s1,s2,observe,start=0){
  let same=true;
  for(let t=start;t<T;t++){
   if(s1[t]!==s2[t])same=false;
   if(observe&&t>start&&a.history[t-start-1]!==b.history[t-start-1])same=false;
   if(same&&!eq(a.plan[t],b.plan[t]))return false;
  }return true;
 }
 function oracle(ps,signals,b,observe,start=0,rem=ps[0].d){
  const ss=ps.map(p=>schedules(p,b,start,rem));let count=0;
  function walk(chosen,i){
   if(i===ss.length){count++;return true}
   for(let a of ss[i])if(chosen.every((q,j)=>compatible(q,a,signals[j],signals[i],observe,start))&&walk([...chosen,a],i+1))return true;
   return false;
  }
  return {ok:walk([],0),count,plans:ss.reduce((n,a)=>n+a.length,0)};
 }
 function unpack(z,ps,signals,b,observe,start=0,rem=ps[0].d){
  if(!z.ok)return false;
  let plans=ps.map(()=>Array.from({length:T},()=>[0,0,0])),seen=ps.map(()=>new Set());
  function walk(n){for(let i of n.ids){ck(!seen[i].has(n.t),"duplicate tree coverage");seen[i].add(n.t);plans[i][n.t]=n.action}
   for(let c of n.children)walk(c);
  }
  for(let n of z.trees)walk(n);
  for(let i=0;i<ps.length;i++)ck(seen[i].size===T-start,"tree covers world");
  let rows=plans.map((plan,i)=>{
   let hist=[],bal=b,remaining=rem.slice();
   for(let t=start;t<T;t++){const a=plan[t],p=ps[i];ck(a.every((n,j)=>n>=0&&Number.isInteger(n)&&n<=remaining[j]&&(!n||t>=p.jobs[j].release&&t<=p.jobs[j].deadline))&&sum(a)<=p.cap[t],"witness action");
    remaining=remaining.map((n,j)=>n-a[j]);ck(remaining.every((n,j)=>!n||p.jobs[j].deadline>t),"witness deadline");bal+=p.income[t]-p.mandatory[t]-sum(a.map((n,j)=>n*p.jobs[j].cost[t]));ck(bal>=p.reserve[t],"cash");hist.push(bal);
   }ck(remaining.every(n=>!n),"done");return {plan,history:hist};
  });
  for(let i=0;i<ps.length;i++)for(let j=i+1;j<ps.length;j++)ck(compatible(rows[i],rows[j],signals[i],signals[j],observe,start),"observation history");
  return true;
 }
 const out={graphs:0,policyChecks:0,oraclePlans:0,states:0,actions:0,cacheHits:0,treeChecks:0,balanceObservationImproves:0,partialSignalsImprove:0,fullSignalsImprove:0,unobservableFutureFalsePass:0,replanningChecks:0,actualHistoryChecks:0,controls:0,example:null};
 function check(ps,s,b,obs,start=0,rem=ps[0].d){
  const z=solve(ps,s,b,obs,start,rem),o=oracle(ps,s,b,obs,start,rem);ck(z.ok===o.ok,"oracle");
  out.policyChecks++;out.oraclePlans+=o.plans;out.states+=z.states;out.actions+=z.actionsTested;out.cacheHits+=z.cacheHits;
  if(z.ok){ck(unpack(z,ps,s,b,obs,start,rem),"tree");out.treeChecks++}
  return z;
 }
 for(let g=0;g<1400;g++){
  const d=[1+rnd(2),1+rnd(2),0],jobs=Array.from({length:N},()=>{let release=rnd(2),deadline=release+rnd(T-release);return {release,deadline}});
  const W=2+rnd(2),ps=Array.from({length:W},()=>({d,jobs:jobs.map(j=>({...j,cost:Array.from({length:T},()=>rnd(4))})),cap:Array.from({length:T},()=>1+rnd(3)),income:Array.from({length:T},()=>rnd(5)),mandatory:Array.from({length:T},()=>rnd(3)),reserve:Array.from({length:T},()=>rnd(3))}));
  const b=rnd(10),none=ps.map(()=>[0,0,0]),partial=ps.map((_,i)=>[0,i%2,i%2]),full=ps.map((_,i)=>[i,i,i]);
  const a=check(ps,none,b,false),c=check(ps,none,b,true),p=check(ps,partial,b,true),f=check(ps,full,b,true);
  ck(!a.ok||c.ok,"balance information monotonic");ck(!c.ok||p.ok,"partial information monotonic");ck(!p.ok||f.ok,"full information monotonic");
  out.balanceObservationImproves+=+(!a.ok&&c.ok);out.partialSignalsImprove+=+(!c.ok&&p.ok);out.fullSignalsImprove+=+(!p.ok&&f.ok);out.unobservableFutureFalsePass+=+(f.ok&&!c.ok);
  if(!a.ok&&c.ok)out.example??={ps,b};
  // Only if a qualified policy and a concrete first observation exist, replan on the
  // actual branch using the frozen executed action, its observed balance and remaining demand.
  if(c.ok){
   const n=c.trees.find(t=>t.ids.includes(0)),history=JSON.stringify({t:0,action:n.action,balance:n.after[0]});
   const ids=n.children.find(x=>x.ids.includes(0))?.ids??[];
   if(ids.length){
    let next=ids.map(i=>ps[i]),sig=ids.map(i=>none[i]),rem=d.map((v,i)=>v-n.action[i]),actualBalance=n.after[0];
    ck(ids.every(i=>n.after[i]===actualBalance),"observed balance partition");
    ck(check(next,sig,actualBalance,true,1,rem).ok,"continuation feasible");
    out.replanningChecks++;
    // revise future only in one branch, retain frozen first period.
    const revised=next.map((p,i)=>i===0?{...p,cap:[p.cap[0],Math.max(0,p.cap[1]-1),p.cap[2]]}:p);
    const rr=check(revised,sig,actualBalance,true,1,rem);
    ck(!rr.ok||check(next,sig,actualBalance,true,1,rem).ok,"less capacity");
    ck(history===JSON.stringify({t:0,action:n.action,balance:n.after[0]}),"immutable history");out.actualHistoryChecks++;
   }
  }
  out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const p={d:[1,0,0],jobs:[{release:1,deadline:2,cost:[0,0,4]},{release:0,deadline:2,cost:[0,0,0]},{release:0,deadline:2,cost:[0,0,0]}],cap:[0,1,1],income:[1,0,0],mandatory:[0,0,0],reserve:[0,0,0]};
 const q={...p,jobs:[{...p.jobs[0],cost:[0,4,0]},...p.jobs.slice(1)],income:[0,0,0]};
 ctl(!solve([p,q],[[0,0,0],[0,0,0]],0,false).ok&&solve([p,q],[[0,0,0],[0,0,0]],0,true).ok,"balance reveals world");
 ctl(!solve([p,{...q,income:[1,0,0]}],[[0,0,0],[0,0,0]],0,true).ok,"equal balances not reveal");
 ctl(solve([p,q],[[0,0,0],[0,1,1]],0,true).ok,"qualified signal");
 ctl(compatible({plan:[[0],[0],[1]],history:[1,0,0]},{plan:[[0],[1],[0]],history:[0,0,0]},[0,0,0],[0,0,0],true),"distinct histories do not remerge");
 return out;
}
console.log(JSON.stringify(experiment(make),null,2));
```
