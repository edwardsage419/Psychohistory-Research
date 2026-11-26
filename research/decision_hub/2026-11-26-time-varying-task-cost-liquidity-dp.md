# 长期个人决策：日期变动的任务支出、逐期流动性和最低初始资金动态规划
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线与查重
固定main 0b816f27ba2f647950a539323c9c295a99129ddb，核对25近期提交、15开放PR、v3.2及同步规程、历史唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前段，#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍draft。未重跑原生。实际读取R101 907f12081ddce7bb752ae498bcf21f4b4b218a60、R125 ffac85bbee74bcd78cb7e34ab91d65d260753a91、R119 e5a2b2921d9c810b82a1e449200b17caf987cf7d、R120 089e7d446004f5303a26a6de25ff328fc857295e、R121 227daac97ef9bc28b62d0c5f3087602a05e0cb8b、R122 e828e2cb88fcc9d1fc4825908f27b7684fdb31b1、R124 43edd309981f55ff110de8fb57be0248f9a075df、混合资源调度d290553f783861c17e15140ee54671a6023566ea前段及相关代码。已有日期窗口、现金硬门、双时间账本、再规划、信息成本与通用DP不重复计为发明。本轮专门研究每项任务各日不同单位支出、每期已知情景流入、必付支出及期末余额底线的联合最低资金和可选任务容量前沿。代码搜索8关键词无返回，非全库去重证明。唯一交接为已知固定blob，未核对其路径最新版本。
## 合同与证明
三个有序抽象期间、3项可拆分整数单位任务，其中两个必需、第三个可选额外量；各任务释放/截止日、每期单位成本、可用工时、外部现金流入、必付支出、期末储备均由可信宿主在同一固定情景中给出。现金先流入再支出，每期结束必须满足非负储备；不允许借款，开期资金非负；无期内时点、利息、税费、分期信用、连续任务、转移成本、未知金额、跨主体账户或概率。未来收入只是明确情景假设，不进入当前实际到账余额。未知来源不能默认0。当前可支用资金须从已授权账本另行核验；本轮不执行真实对账、预留、付款或自动写入。计算结果均authority NONE（研究函数只输出数值和见证，正式端口须另加权属及当前性）。
V(t,r)为剩余需求r在t期开始所需的最低非负资金，不能按期限完成则无解。终端仅r=0时V=0。每期合法分配x满足窗口、剩余量、容量及到期义务，c为当期固定必付款与任务支出之和，i为当期流入，s为期末储备。递推V(t,r)=min_x max(0,c+max(s,V(t+1,r-x))-i)，忽略无解续策。给定x，期末资金必须同时满足储备和续策最低资金；额外现金不损害本模型可行性。对每个可行后继取其最小充分且必要开期金额，再取合法x中最小；归纳得精确结果。返回一条达到最低资金的排程。独立参照直接将每个任务单位分配到其窗口内日期，对全部合法分配计算所有累计净支出加储备的最大值，再取最小。工时期限无解与资金不足分开。增加非负成本的额外工作不能降低最低资金；不含额外工作本身带来的未来收益，不能推广到投资/培训真实回报。可选前沿仅为固定条件可增加的单位工作量，非统一人生分数。
## 实际实验
1800组人工随机结构，每组可选0/1/2单位共5400次DP及直接枚举。两个必需任务各1..2，随机窗口，容量0..3，单位支出0..3，流入0..4，必付与储备0..2，开期资金0..7。核对最小资金、合法见证、同见证少一单位失败、额外需求单调、工时不可行与现金不足分离。三种故意错误基线：只核期末（允许期间负余额）；分别取任务最便宜日期并仅比较总现金（忽略共同日期容量及前缀）；所有未来流入提前。首次运行提前流入基线超过输入单期上限9导致中止，未归档；将收入上限单独调整为27，保留原生成分布，并将重复终端枚举并入直接参照，完整重跑。5控制。标准JS核心实际执行两次一致。计数为合成结构与重复单位排列，不是独立用户、真实错误率或设备性能。
```json
{
  "graphs": 1800,
  "frontierChecks": 5400,
  "states": 21427,
  "transitions": 22510,
  "oracleAssignments": 7292,
  "timeInfeasible": 3467,
  "liquidityFeasible": 1040,
  "terminalOnlyFalsePass": 171,
  "independentGateFalsePass": 275,
  "earlyIncomeFalsePass": 162,
  "optionalCapacityReduced": 114,
  "controls": 5,
  "witnesses": {
    "terminal": {
      "p": {
        "d": [
          1,
          2,
          0
        ],
        "jobs": [
          {
            "release": 2,
            "deadline": 2,
            "cost": [
              3,
              2,
              1
            ]
          },
          {
            "release": 0,
            "deadline": 0,
            "cost": [
              2,
              1,
              2
            ]
          },
          {
            "release": 2,
            "deadline": 2,
            "cost": [
              2,
              3,
              2
            ]
          }
        ],
        "cap": [
          2,
          2,
          3
        ],
        "income": [
          2,
          4,
          0
        ],
        "mandatory": [
          2,
          2,
          1
        ],
        "reserve": [
          1,
          0,
          0
        ]
      },
      "b": 4,
      "terminal": 4,
      "need": 5
    }
  }
}
```
## 后续与局限
最小开期金额只对当前已资格固定情景和上述合同成立，不构造真实未来事实。下一阶段需要跨世界保持同一事前方案、各世界最低资金向量与共同资金阈值，并通过信息可用时点区别可调整计划；继承现有长期账本与版本事务。未修改生产、唯一交接、冻结、证据等级、PR、训练、部署、主动CI或新增费用。研究者选定小规模整数网格、现金时序、无借款及固定成本模型、基线；未执行完整原生、独立留出、真机或真实用户。
## 复算
标准JS核心实际运行两次，Node包装未运行。
```js
function study(){
 const ck=(v,m)=>{if(!v)throw Error(m)},sum=a=>a.reduce((s,x)=>s+x,0),N=3,T=3;
 let seed=20261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function valid(p){
  ck(p.d.length===N&&p.d.every(n=>Number.isInteger(n)&&n>=0&&n<=3),"demand");
  ck(p.jobs.length===N&&p.jobs.every(j=>Number.isInteger(j.release)&&Number.isInteger(j.deadline)&&j.release>=0&&j.release<=j.deadline&&j.deadline<T&&j.cost.length===T&&j.cost.every(n=>Number.isInteger(n)&&n>=0&&n<=5)),"jobs");
  for(const k of ["cap","income","mandatory","reserve"])ck(p[k].length===T&&p[k].every(n=>Number.isInteger(n)&&n>=0&&n<=(k==="income"?27:9)),k);
 }
 function actions(p,t,rem){
  const out=[];
  for(let a=0;a<=rem[0];a++)for(let b=0;b<=rem[1];b++)for(let c=0;c<=rem[2];c++){
   const x=[a,b,c];if(sum(x)>p.cap[t])continue;
   if(x.some((n,i)=>n&&(t<p.jobs[i].release||t>p.jobs[i].deadline)))continue;
   const nr=rem.map((n,i)=>n-x[i]);
   if(nr.some((n,i)=>n&&p.jobs[i].deadline<=t))continue;
   out.push({x,nr,cost:sum(x.map((n,i)=>n*p.jobs[i].cost[t]))});
  }return out;
 }
 function solve(p){
  valid(p);let memo=new Map(),states=0,transitions=0;
  function rec(t,rem){
   if(t===T)return rem.every(n=>n===0)?{need:0,plan:[]}:null;
   const k=t+":"+rem.join(",");if(memo.has(k))return memo.get(k);
   states++;let best=null;
   for(const a of actions(p,t,rem)){
    transitions++;let tail=rec(t+1,a.nr);if(!tail)continue;
    let need=Math.max(0,p.mandatory[t]+a.cost+Math.max(p.reserve[t],tail.need)-p.income[t]);
    if(!best||need<best.need)best={need,plan:[a.x,...tail.plan]};
   }
   memo.set(k,best);return best;
  }
  return {best:rec(0,p.d),states,transitions};
 }
 function verify(p,plan,b){
  let bal=b,rem=p.d.slice(),rows=[];
  if(!Number.isInteger(b)||b<0||plan.length!==T)return null;
  for(let t=0;t<T;t++){
   const x=plan[t];if(x.length!==N||x.some((n,i)=>!Number.isInteger(n)||n<0||n>rem[i]||n>0&&(t<p.jobs[i].release||t>p.jobs[i].deadline))||sum(x)>p.cap[t])return null;
   rem=rem.map((n,i)=>n-x[i]);if(rem.some((n,i)=>n&&p.jobs[i].deadline<=t))return null;
   bal+=p.income[t]-p.mandatory[t]-sum(x.map((n,i)=>n*p.jobs[i].cost[t]));
   if(bal<p.reserve[t])return null;
   rows.push(bal);
  }
  return rem.every(n=>n===0)?rows:null;
 }
 function oracle(p){
  let units=[];for(let i=0;i<N;i++)for(let k=0;k<p.d[i];k++)units.push(i);
  let x=Array.from({length:T},()=>Array(N).fill(0)),best=null,terminal=null,count=0;
  function rec(k){
   if(k===units.length){
    let cum=0,need=0;
    for(let t=0;t<T;t++){cum+=p.mandatory[t]+sum(x[t].map((v,i)=>v*p.jobs[i].cost[t]))-p.income[t];need=Math.max(need,cum+p.reserve[t]);}
    const end=Math.max(0,cum+p.reserve[T-1]);
    count++;if(best===null||need<best)best=need;if(terminal===null||end<terminal)terminal=end;return;
   }
   let i=units[k],j=p.jobs[i];
   for(let t=j.release;t<=j.deadline;t++)if(sum(x[t])<p.cap[t]){x[t][i]++;rec(k+1);x[t][i]--;}
  }
  rec(0);return {need:best,terminal,count};
 }
 const out={graphs:0,frontierChecks:0,states:0,transitions:0,oracleAssignments:0,timeInfeasible:0,liquidityFeasible:0,terminalOnlyFalsePass:0,independentGateFalsePass:0,earlyIncomeFalsePass:0,optionalCapacityReduced:0,controls:0,witnesses:{}};
 function check(p,b){
  let z=solve(p),o=oracle(p);ck((z.best?.need??null)===o.need,"oracle");
  out.frontierChecks++;out.states+=z.states;out.transitions+=z.transitions;out.oracleAssignments+=o.count;
  if(!z.best){out.timeInfeasible++;return null}
  ck(verify(p,z.best.plan,z.best.need)!==null,"feasible witness");
  if(z.best.need>0)ck(verify(p,z.best.plan,z.best.need-1)===null,"witness threshold");
  out.liquidityFeasible+=+(b>=z.best.need);
  if(b>=o.terminal&&b<z.best.need){out.terminalOnlyFalsePass++;out.witnesses.terminal??={p,b,terminal:o.terminal,need:z.best.need}}
  let independentMin=sum(p.d.map((n,i)=>n*Math.min(...p.jobs[i].cost.slice(p.jobs[i].release,p.jobs[i].deadline+1))));
  if(sum(p.income)+b>=sum(p.mandatory)+independentMin+p.reserve[2]&&b<z.best.need)out.independentGateFalsePass++;
  const early={...p,income:[sum(p.income),0,0]},e=solve(early);
  if(e.best&&b>=e.best.need&&b<z.best.need)out.earlyIncomeFalsePass++;
  return z.best.need;
 }
 for(let g=0;g<1800;g++){
  const jobs=Array.from({length:N},()=>{let release=rnd(T),deadline=release+rnd(T-release);return {release,deadline,cost:Array.from({length:T},()=>rnd(4))}});
  const p={d:[1+rnd(2),1+rnd(2),0],jobs,cap:Array.from({length:T},()=>rnd(4)),income:Array.from({length:T},()=>rnd(5)),mandatory:Array.from({length:T},()=>rnd(3)),reserve:Array.from({length:T},()=>rnd(3))};
  let b=rnd(8),prev=0,temporal=0,liquid=0;
  for(let k=0;k<=2;k++){
   const q={...p,d:[p.d[0],p.d[1],k]},v=check(q,b);
   if(k&&prev===null)ck(v===null,"time monotonic");
   if(k&&prev!==null&&v!==null)ck(v>=prev,"cash monotonic");
   if(v!==null){temporal=k+1;if(b>=v)liquid=k+1}
   prev=v;
  }
  out.optionalCapacityReduced+=+(temporal>liquid&&liquid>0);out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const p={d:[1,0,0],jobs:[{release:0,deadline:0,cost:[3,0,0]},...Array.from({length:2},()=>({release:0,deadline:2,cost:[0,0,0]}))],cap:[1,1,1],income:[0,3,0],mandatory:[0,0,0],reserve:[0,0,0]};
 ctl(solve(p).best.need===3&&oracle(p).terminal===0,"future cash not spendable now");
 ctl(solve({...p,jobs:[{...p.jobs[0],deadline:1},...p.jobs.slice(1)]}).best.need===0,"delay to receipt");
 ctl(solve({...p,cap:[0,1,1]}).best===null,"deadline");
 ctl(solve({...p,d:[0,0,0],income:[0,0,0],mandatory:[1,1,1],reserve:[1,1,1]}).best.need===4,"non-task obligations");
 ctl(solve({...p,d:[0,0,0],income:[0,0,0],mandatory:[0,0,0],reserve:[2,1,0]}).best.need===2,"earlier reserve");
 return out;
}
console.log(JSON.stringify(study(),null,2));
```
