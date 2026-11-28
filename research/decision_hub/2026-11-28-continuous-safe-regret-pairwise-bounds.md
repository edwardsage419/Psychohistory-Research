# 连续联合情景下的安全行动、精确后悔值及逐项停止界
2026-11-28。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。基线 7236967f9e2f7186baf663e9e233e440847201e5。本轮读取最近25项提交、开放PR、v3.2、AGENTS、同步规程、唯一产品交接（工具读取全文，输出末9000字符）、2026-11-27精确目标投影全文、预算消元和连续共享参数文档开头、2026-11-24条件后悔值文档数学及实验部分。#63 为 Draft，作者报告的语言数值单位7/23、条件0/5、账本修订0/10，不能宣称自主语言成熟。局部去重；本轮从既有离散情景安全后悔与连续精确目标投影推导组合，不宣称原创数学定理，未核对外部原论文。
## 数学合同
有限个已获资格且覆盖充分的非空连续联合世界域 P_w，每个是有界二维有理线性约束交集，可含严格边界。所有候选共享同一参数点、同一用户确认目标和单位。行动 a 的可行域 F_a；固定行动仅在所有 P_w 均包含于 F_a 时具备稳健可行资格。对于硬约束 g<=0，当 sup g<=0 可放行；对于 g<0，仅 sup g<0 或 sup g=0 且不可达可放行。空域不得产生虚假通过；无非空世界或无安全行动分别保留冲突/未知或无稳健可行行动。现实未知的候选覆盖不可通过任意删除情景解决。
已确认仿射效用 u_a(x)；全信息基准 b(x)=max_{j:x in F_j}u_j(x)。安全行动 i 的最坏后悔值 R_i=max_{w,j}sup_{x in P_w intersect F_j}(u_j(x)-u_i(x))，空交集跳过。证明：有限并集的上确界等于各上确界最大值，且同一参数点计算差值保留相关性。安全行动自身比较保证 R_i>=0。对于可能不可行的比较行动 j，只有其可行区域进入基准；不得将其效用扩展到不可行域。严格边界可能只存在上确界。目标是后悔值上确界最小化；并列须保留。没有用户确认效用时不排序，authority NONE。
预算：每项未求解差值用已认证全域外盒的仿射最大值 U_wj 作保守上界。已求项的非负最大值 L_i 为下界，H_i=max(L_i,剩余项U) 为上界。每次精确结算后 L_i 不减、H_i 不增；若 H_i 严格小于所有其他安全行动 L_j，可证 i 为唯一最优，不要求其精确值已知；等号不能作为唯一性证明。预算不足且区间重叠时不得强行推荐。安全资格完整计算在先，不将未检查安全性变成已通过。上界可通过更紧的已确认外域改进；快照变化后需失效重算。未实现外层真实故障根集合生成、证书签名、版本绑定、任意维、单次消元预算和设备内存限制。
## 实验
800组固定种子虚构配置；域[0,4]^2，两个连续世界候选，三个行动各一条线性硬门（部分严格），随机整数仿射效用。完整路径逐项精确投影与顶点枚举严格松弛参照比较；安全参照直接检查违反门的可行性。单独重放路径只按外盒上界排序，逐项调用投影函数，在唯一性证成时立即停止；参照结果仅用于断言，不参与排序/停止判定。统计多安全行动配置的后悔值投影调用节省，未包含安全门、参照运算、排序和内存开销，不代表端到端性能。边际差值上界过宽次数只反映该合成分布，不是产品错误或真实概率。非独立留出、研究者选定参数，未执行训练、原生入口、真机、独立验收、主动CI、合并、部署或新增费用。下一责任模型轨：将内层消元预算和外层故障枚举接入；独立轨：留出及负向安全门；产品轨：未知与严格边界解释。冻结与唯一交接不变。
复算（Node.js或支持BigInt的JS环境）：
```js
function experiment(){
 const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1],zero=[0n,1n],max=(a,b)=>cmp(a,b)>=0n?a:b,min=(a,b)=>cmp(a,b)<=0n?a:b;
 const R=(a,b,c,s=false)=>({v:[BigInt(a),BigInt(b)],c:BigInt(c),s});
 const box=[R(-1,0,0),R(1,0,4),R(0,-1,0),R(0,1,4)];
 function elim(z){const p=z.filter(r=>r.v[0]>0n),n=z.filter(r=>r.v[0]<0n),q=z.filter(r=>!r.v[0]).map(r=>({...r,v:r.v.slice(1)}));for(const a of p)for(const b of n){let u=-b.v[0],v=a.v[0];q.push({v:a.v.slice(1).map((x,i)=>u*x+v*b.v[i+1]),c:u*a.c+v*b.c,s:a.s||b.s})}return q}
 function proj(rs,g){const [a,b,k]=g;let z=rs.map(r=>({...r,v:[...r.v,0n]}));z.push({v:[a,b,-1n],c:-k,s:false},{v:[-a,-b,1n],c:k,s:false});let l=null,u=null,ls=false,us=false;for(const r of elim(elim(z))){let d=r.v[0];if(!d){if(r.c<0n||r.c===0n&&r.s)return null;continue}let t=d>0n?[r.c,d]:[-r.c,-d];if(d>0n){if(!u||cmp(t,u)<0n){u=t;us=r.s}else if(!cmp(t,u))us||=r.s}else{if(!l||cmp(t,l)>0n){l=t;ls=r.s}else if(!cmp(t,l))ls||=r.s}}if(cmp(l,u)>0n||!cmp(l,u)&&(ls||us))return null;return {v:u,attained:!us}}
 function oracle(rs,g){let V=[];for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){let p=rs[i],q=rs[j],d=p.v[0]*q.v[1]-q.v[0]*p.v[1];if(!d)continue;let x=p.c*q.v[1]-q.c*p.v[1],y=p.v[0]*q.c-q.v[0]*p.c;if(d<0n){d=-d;x=-x;y=-y}if(rs.every(r=>r.v[0]*x+r.v[1]*y<=r.c*d))V.push({x,y,d,t:[g[0]*x+g[1]*y+g[2]*d,d]})}const ok=W=>W.length&&rs.filter(r=>r.s).every(r=>W.some(v=>r.v[0]*v.x+r.v[1]*v.y<r.c*v.d));if(!ok(V))return null;let u=V.reduce((m,v)=>max(m,v.t),V[0].t);return {v:u,attained:!!ok(V.filter(v=>!cmp(v.t,u)))}}
 const diff=(a,b)=>a.map((x,i)=>x-b[i]),inv=r=>({v:r.v.map(x=>-x),c:-r.c,s:!r.s});
 const same=(a,b)=>!a&&!b||a&&b&&!cmp(a.v,b.v)&&a.attained===b.attained;
 const must=(x,m)=>{if(!x)throw Error(m)};
 let seed=20261128;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 const dirs=[[1,0],[0,1],[1,1],[1,-1],[-1,1],[-1,-1]];
 const randomRow=()=>{let [a,b]=dirs[rnd(dirs.length)];return R(a,b,rnd(9)-2,!!rnd(2))};
 const utility=()=>[BigInt(rnd(7)-3),BigInt(rnd(7)-3),BigInt(rnd(9)-4)];
 const out={generated:800,nonemptyCases:0,emptyWorlds:0,safetyChecks:0,safeActions:0,unsafeActions:0,objectiveChecks:0,emptyPairs:0,openSuprema:0,exactComparisons:0,partialBounds:0,earlyUnique:0,fullUnique:0,fullTies:0,marginalOverstates:0,noSafeCases:0,fullJobsMulti:0,earlyReplayJobsMulti:0,earlyReplaySavedMulti:0,replayCorrect:0};
 for(let trial=0;trial<out.generated;trial++){
  let worlds=[box.concat(randomRow()),box.concat(randomRow(),randomRow())],actions=[{r:R(0,0,0),u:utility()},{r:randomRow(),u:utility()},{r:randomRow(),u:utility()}];
  if(trial%7===0)actions[0].r=randomRow();
  worlds=worlds.filter(w=>{let p=proj(w,[0n,0n,0n]),o=oracle(w,[0n,0n,0n]);must(same(p,o),"world");if(!p)out.emptyWorlds++;return !!p});
  if(!worlds.length)continue;out.nonemptyCases++;
  const safe=actions.map(a=>worlds.every(w=>{let p=proj(w,[...a.r.v,-a.r.c]);let s=cmp(p.v,zero)<0n||!cmp(p.v,zero)&&(!a.r.s||!p.attained);let o=!oracle(w.concat(inv(a.r)),[0n,0n,0n]);out.safetyChecks++;must(s===o,"safety");return s}));
  out.safeActions+=safe.filter(Boolean).length;out.unsafeActions+=safe.filter(x=>!x).length;
  if(!safe.some(Boolean)){out.noSafeCases++;continue}
  let ids=actions.map((_,i)=>i).filter(i=>safe[i]),exact={},jobs=[];
  for(let i of ids){exact[i]=zero;for(let w=0;w<worlds.length;w++)for(let j=0;j<actions.length;j++){
    let rs=worlds[w].concat(actions[j].r),g=diff(actions[j].u,actions[i].u);
    let o=oracle(rs,g);
    if(o){exact[i]=max(exact[i],o.v);let mj=oracle(rs,actions[j].u).v,mi=oracle(rs,actions[i].u.map(x=>-x)).v;if(cmp([mj[0]*mi[1]+mi[0]*mj[1],mj[1]*mi[1]],o.v)>0n)out.marginalOverstates++}
    let bound=[g[2]+4n*(g[0]>0n?g[0]:0n)+4n*(g[1]>0n?g[1]:0n),1n];
    jobs.push({i,rs,g,bound,reference:o});
  }}
  let best=ids.map(i=>exact[i]).reduce(min),winners=ids.filter(i=>!cmp(exact[i],best));out[winners.length===1?"fullUnique":"fullTies"]++;
  jobs.sort((a,b)=>cmp(a.bound,b.bound)>0n?-1:cmp(a.bound,b.bound)<0n?1:0);
  function run(stopEarly){
   let lo=Object.fromEntries(ids.map(i=>[i,zero])),old={};
   for(let step=0;step<=jobs.length;step++){
    let intervals={};for(let i of ids){let hi=jobs.slice(step).filter(j=>j.i===i).reduce((m,j)=>max(m,j.bound),lo[i]);intervals[i]={lo:lo[i],hi};if(!stopEarly)out.partialBounds++;must(cmp(lo[i],exact[i])<=0n&&cmp(hi,exact[i])>=0n,"bound");if(old[i])must(cmp(lo[i],old[i].lo)>=0n&&cmp(hi,old[i].hi)<=0n,"monotone")}
    let certified=ids.filter(i=>ids.every(j=>i===j||cmp(intervals[i].hi,intervals[j].lo)<0n));
    if(certified.length){must(winners.length===1&&certified[0]===winners[0],"false winner");if(stopEarly)return {used:step,certified:certified[0]}}
    if(step===jobs.length){for(let i of ids){must(!cmp(intervals[i].lo,exact[i])&&!cmp(intervals[i].hi,exact[i]),"final");if(!stopEarly)out.exactComparisons++}return {used:step,certified:null}}
    old=intervals;let j=jobs[step],p=proj(j.rs,j.g);must(same(p,j.reference),"regret");
    if(!stopEarly){out.objectiveChecks++;if(!p)out.emptyPairs++;else if(!p.attained)out.openSuprema++}
    if(p)lo[j.i]=max(lo[j.i],p.v)
   }
  }
  run(false);let early=run(true);
  if(ids.length>1){out.fullJobsMulti+=jobs.length;out.earlyReplayJobsMulti+=early.used;out.earlyReplaySavedMulti+=jobs.length-early.used;if(early.used<jobs.length)out.earlyUnique++;if(early.certified!==null||early.used===jobs.length)out.replayCorrect++}
 }
 return out;
}
console.log(JSON.stringify(experiment(),null,2));
```
实际运行结果：
```json
{
  "generated": 800,
  "nonemptyCases": 776,
  "emptyWorlds": 311,
  "safetyChecks": 3192,
  "safeActions": 1262,
  "unsafeActions": 1066,
  "objectiveChecks": 6243,
  "emptyPairs": 540,
  "openSuprema": 883,
  "exactComparisons": 1262,
  "partialBounds": 13649,
  "earlyUnique": 403,
  "fullUnique": 721,
  "fullTies": 18,
  "marginalOverstates": 4010,
  "noSafeCases": 37,
  "fullJobsMulti": 4614,
  "earlyReplayJobsMulti": 1005,
  "earlyReplaySavedMulti": 3609,
  "replayCorrect": 421
}
```
