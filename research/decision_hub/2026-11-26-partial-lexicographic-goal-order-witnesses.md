# 长期个人决策：不完整词典序目标优先级、可胜见证及最小关键比较
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线
同一手动轮第二阶段，起点main 437d31d760df532688e5646d617e83eeeea9b78d，沿用本轮已核对v3.2、同步规程、25近期提交、15开放PR、固定交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。前阶段目标组合反链与内生信息反例blob a2d68ed924489acbc4fc4ff72184a70118a588d3。R97已做Pareto、R98机会损失、既有偏好敏感性及澄清分离研究不重计。代码搜索preference/Pareto/regret等无结果，查重有限。本轮新增有限二元目标组合下，已明确采用词典序偏好的部分优先关系及免穷举所有优先排列的可胜证书，单次比较的最坏剩余候选数。
## 适用合同
输入6个身份固定的二元软目标及已资格的完整可行组合集合（可能存在非单调关系，不假设向下封闭）；硬义务已经由宿主独立筛除，不进入偏好取舍。只有用户明确接受词典序规则时，才可应用：先比最优先目标是否实现，若相同再比下一个。一个高优先目标胜过任意数量低优先目标，此强非补偿性假设不适合一般偏好、连续收益、目标实现程度或概率风险；不能由“更重要”擅自推断。用户没有确认该偏好模型时保持UNKNOWN_QUALIFICATION。世界覆盖、目标身份、真实用户确认、适用性、来源与权限由可信宿主提供，本原型不自动获得，不训练、不引入统一人生评分。每个目标组合唯一，不区分实现该组合的多条计划，后者仍需资源、风险等独立比较。优先边i→j为明确的i优先于j，取传递闭包，循环为PREFERENCE_CONFLICT，不能任意删除用户边。
## 算法与证明
目标组合t可胜 iff 存在优先偏序的线性扩展，使词典序选择t。依序选任一当前入度为0且不使t输掉的目标i：若t含i，移除不含i的剩余竞争组合；若t不含i，仅当剩余全部组合也不含i才可选。若存在一条成功后续优先排列，则任何如此允许且当前无前置的i可以移到其首位；t含i时只提前排除输给t的竞争组合，不含i时不区分任何现存竞争组合，因此不破坏成功的排列。移到首位不违反偏序，因为当前无前置。归纳：贪心不会错失成功线性扩展；无允许节点时不存在可胜顺序，完整时输出可直接复算的优先排列见证。每个目标测试至多N轮，每轮扫描N目标和剩余组合，避免直接N!遍历；没有生产规模或墙时测试。测试全部组合得到可能最优集合；集合唯一才是所有线性扩展共同最优，非用户真实唯一选择。保留同值不同计划的身份需宿主另作；此处只有二元组合。
对尚不可比较的两个目标，分别添加两个相反优先关系，重新计算可能最优集合；两分支并集应为原集合，最坏剩余候选数取两分支大小最大。最小者为仅限单次、用户确实愿意提供严格次序答案的候选问题。若两分支仍保留全部，不能宣称有决策价值；拒绝回答、无差别、偏好非词典序、问题认知成本和多步最优询问不在合同内。撤回关系按原始边重建闭包，不删除由其他边仍可推出的约束；可能最优集合只能扩张。所有结果authority NONE，不写用户偏好或自动执行。
## 实际实验
1600个合成偏序及可行组合集合（随机生成，不声称来自真实用户或上阶段具体账本）。6目标，每组2..16个抽取的二元组合去重；随机隐藏排列产生无环关系。与独立全部拓扑排列参照逐组核对可能集合，逐个不可比关系对照两个答案后的候选及并集，随机删除一条边验证重建与扩张；7专项控制。标准JS连接器两次实际运行一致。计数是有限合成结构、重复候选与偏好排列，不是真实认知负担、用户准确率或独立验收。研究者选定词典序合同、随机分布及最坏候选数比较，非正式产品默认。
```json
{
  "graphs": 1600,
  "distinctBundles": 13430,
  "ordersEnumerated": 179275,
  "possibleTests": 13430,
  "greedySteps": 50486,
  "necessaryWinners": 535,
  "ambiguous": 1065,
  "comparisonChecks": 16369,
  "usefulQuestions": 802,
  "oneQuestionGuaranteedResolve": 311,
  "arbitraryPriorityDisagrees": 1065,
  "revisionChecks": 1573,
  "removedEdgeExpands": 324,
  "controls": 7,
  "examples": {
    "question": {
      "bundles": [
        2,
        3,
        4,
        7,
        22,
        27,
        29,
        33,
        34,
        37,
        44,
        45,
        51,
        60
      ],
      "edges": [
        [
          4,
          3
        ],
        [
          5,
          3
        ]
      ],
      "possible": [
        7,
        22,
        29,
        45,
        51,
        60
      ],
      "best": {
        "i": 0,
        "j": 4,
        "l": [
          7,
          29,
          45,
          51
        ],
        "r": [
          22,
          29,
          51,
          60
        ],
        "worst": 4
      }
    }
  }
}
```
## 接入
GoalBundlePort首先产生经资格核验的完整可行组合；PreferenceOrderPort须由用户明确确认其规则、目标版本和当前关系，返回共同最优/可能最优与具体优先顺序见证，若偏好冲突或未确认维持未知。无需用户确认无影响的次序，但不以候选集合缩小替代真实认知负担和决策效果。未来需要与前轮实际组合求解连接、独立未见对话及真实偏好模型选择验证。未修改生产、唯一交接、冻结、证据等级、PR、训练、部署、主动CI或费用，未执行原生/独立留出/真机/真人。
## 复算
标准JS核心实际执行两次，Node包装未运行。
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),N=6,ALL=(1<<N)-1;
 const bits=m=>Array.from({length:N},(_,i)=>i).filter(i=>m&(1<<i));
 let seed=20261203;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function closure(edges){
  let p=Array(N).fill(0);
  for(let [i,j] of edges){ck(i!==j&&i>=0&&i<N&&j>=0&&j<N,"edge");p[j]|=1<<i;}
  for(let k=0;k<N;k++)for(let j=0;j<N;j++)if(p[j]&(1<<k))p[j]|=p[k];
  return p.some((v,i)=>v&(1<<i))?null:p;
 }
 function orderOK(order,p){
  let used=0;
  for(let i of order){if(used&(1<<i)||p[i]&~used)return false;used|=1<<i}
  return used===ALL;
 }
 function winner(order,bundles){
  let s=bundles.slice();
  for(let i of order){if(s.some(m=>m&(1<<i)))s=s.filter(m=>m&(1<<i))}
  ck(s.length===1,"unique distinct bundle");return s[0];
 }
 // Existence of a compatible lexicographic priority order making a target best.
 function possible(target,bundles,p){
  let remaining=bundles.slice(),used=0,order=[],steps=0;
  while(used!==ALL){
   let chosen=-1;
   for(let i=0;i<N;i++){
    if(used&(1<<i)||p[i]&~used)continue;
    if(!(target&(1<<i))&&remaining.some(m=>m&(1<<i)))continue;
    chosen=i;break;
   }
   steps++;
   if(chosen<0)return {ok:false,order,remaining,used,steps};
   if(target&(1<<chosen))remaining=remaining.filter(m=>m&(1<<chosen));
   used|=1<<chosen;order.push(chosen);
  }
  ck(orderOK(order,p)&&winner(order,bundles)===target,"positive witness");
  return {ok:true,order,steps};
 }
 function greedy(b,p){
  const witnesses={},blocked={},possibleSet=[];let steps=0;
  for(let t of b){let z=possible(t,b,p);steps+=z.steps;if(z.ok){possibleSet.push(t);witnesses[t]=z.order}else blocked[t]=z}
  return {possible:possibleSet.sort((a,b)=>a-b),necessary:possibleSet.length===1?possibleSet[0]:null,witnesses,blocked,steps};
 }
 function enumerate(b,p){
  let order=[],out=new Set(),orders=0;
  function walk(used){
   if(used===ALL){orders++;out.add(winner(order,b));return}
   for(let i=0;i<N;i++)if(!(used&(1<<i))&&!(p[i]&~used)){order.push(i);walk(used|(1<<i));order.pop()}
  }
  walk(0);return {possible:[...out].sort((a,b)=>a-b),orders};
 }
 function qualify(b,edges,coverage,semantics){
  if(!coverage||semantics!=="EXPLICIT_LEXICOGRAPHIC")return {status:"UNKNOWN_QUALIFICATION",authority:"NONE"};
  const p=closure(edges);
  if(!p)return {status:"PREFERENCE_CONFLICT",authority:"NONE"};
  if(!b.length)return {status:"NO_FEASIBLE_BUNDLE",authority:"NONE"};
  return {status:"CONDITIONAL",...greedy(b,p),authority:"NONE"};
 }
 function queries(b,edges,p){
  let out=[];
  for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){
   if(p[i]&(1<<j)||p[j]&(1<<i))continue;
   let l=greedy(b,closure([...edges,[i,j]])).possible,r=greedy(b,closure([...edges,[j,i]])).possible;
   out.push({i,j,l,r,worst:Math.max(l.length,r.length)});
  }
  return out.sort((a,b)=>a.worst-b.worst||a.i-b.i||a.j-b.j);
 }
 const out={graphs:0,distinctBundles:0,ordersEnumerated:0,possibleTests:0,greedySteps:0,necessaryWinners:0,ambiguous:0,comparisonChecks:0,usefulQuestions:0,oneQuestionGuaranteedResolve:0,arbitraryPriorityDisagrees:0,revisionChecks:0,removedEdgeExpands:0,controls:0,examples:{}};
 for(let g=0;g<1600;g++){
  let hidden=[0,1,2,3,4,5];for(let i=N-1;i>0;i--){let j=rnd(i+1);[hidden[i],hidden[j]]=[hidden[j],hidden[i]]}
  let edges=[];for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(rnd(4)===0)edges.push([hidden[i],hidden[j]]);
  let p=closure(edges),raw=Array.from({length:2+rnd(15)},()=>rnd(64)),b=[...new Set(raw)].sort((a,b)=>a-b);
  ck(p!==null,"acyclic generated");
  let z=greedy(b,p),o=enumerate(b,p);
  ck(eq(z.possible,o.possible)&&z.possible.length>0,"possible parity");
  out.graphs++;out.distinctBundles+=b.length;out.possibleTests+=b.length;out.greedySteps+=z.steps;out.ordersEnumerated+=o.orders;
  if(z.necessary!==null)out.necessaryWinners++;else out.ambiguous++;
  const qs=queries(b,edges,p);
  for(let q of qs){
   let l=enumerate(b,closure([...edges,[q.i,q.j]])),r=enumerate(b,closure([...edges,[q.j,q.i]]));
   ck(eq(l.possible,q.l)&&eq(r.possible,q.r),"question branch");
   ck(eq([...new Set([...q.l,...q.r])].sort((a,b)=>a-b),z.possible),"branch covers all orders");
   out.comparisonChecks++;
  }
  if(qs.length&&qs[0].worst<z.possible.length){out.usefulQuestions++;out.examples.question??={bundles:b,edges,possible:z.possible,best:qs[0]}}
  if(z.possible.length>1&&qs.length&&qs[0].worst===1)out.oneQuestionGuaranteedResolve++;
  // A fixed topological priority selects one result although another consistent order can win.
  if(z.possible.length>1)out.arbitraryPriorityDisagrees++;
  if(edges.length){
   let k=rnd(edges.length),e=edges.filter((_,i)=>i!==k),r=greedy(b,closure(e)),q=enumerate(b,closure(e));
   ck(eq(r.possible,q.possible)&&z.possible.every(v=>r.possible.includes(v)),"withdraw comparison");
   out.revisionChecks++;out.removedEdgeExpands+=+(r.possible.length>z.possible.length);
  }
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 ctl(eq(greedy([1,2],closure([])).possible,[1,2]),"unknown tradeoff");
 ctl(greedy([1,2],closure([[0,1]])).necessary===1,"explicit preference");
 ctl(greedy([1,2,3],closure([])).necessary===3,"superset dominates");
 ctl(qualify([1,2],[[0,1],[1,0]],true,"EXPLICIT_LEXICOGRAPHIC").status==="PREFERENCE_CONFLICT","cycle");
 ctl(qualify([1,2],[],true,"UNCONFIRMED").status==="UNKNOWN_QUALIFICATION","no model assumption");
 ctl(qualify([1,2],[],false,"EXPLICIT_LEXICOGRAPHIC").status==="UNKNOWN_QUALIFICATION","coverage");
 ctl(qualify([],[],true,"EXPLICIT_LEXICOGRAPHIC").status==="NO_FEASIBLE_BUNDLE","no feasible");
 return out;
}
console.log(JSON.stringify(experiment(),null,2));
```
