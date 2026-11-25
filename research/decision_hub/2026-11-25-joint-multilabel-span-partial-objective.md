# 自主认知专项累计第84轮候选：同轮多标签跨度联合因子与部分监督目标

2026-11-25。RESEARCH_CANDIDATE / FIXED_PARAMETER_FACTOR_ELIMINATION_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线 main 516068fb5cc8306b735df283fbfbf045b15adc6e。核对近期25提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R74/R75/R76/R83前16行。R75独立BIO头已验证部分监督，R76跨轮引用边已验证联合分区；本轮不重做这些实验，新增同轮多标签跨度存在性、允许重叠、显式互斥与软交互因子，以变量消元计算联合目标。没有实际原文角色发现或训练，没有新增外部资料；有限概率图求和不主张原创数学定理。

## 合同与公式
每个二元变量代表一个带原文锚点的跨度-角色命题是否存在，0/1为模型内部假设，并非客观真值。六个变量、六条环形边、固定正整数一元与软二元因子；已资格的互斥可对共存赋0。不同角色、同角色的重叠均不自动互斥，互斥必须由可信语义合同给出，真实允许条件未确定。四组固定因子：全软交互；仅一个夹具确认的互斥；再加入两个未经确认的互斥（故意错误对照）；独立变量基线。错误对照在新增禁用组合之外保持允许组合的因子相同的意图需核对：本实现0/1边soft的允许项相同，4/5边anti的00权重从2变1，因此总质量损失混合了互斥及软权重变化；冲突计数仍由新增零项造成，不能把质量损失全归因于互斥。无训练、无拟合、无优化器。部分监督每个命题允许集合为{0}已确认负例、{1}已确认正例、{0,1}未标注。0不等同于未知义项；开放域遗漏必须另保留OUTSIDE/UNKNOWN及覆盖义务，本轮未实现开放域概率或未知检测。固定候选集合的合法赋值权重为一元与边因子乘积；Z为全部权重和，受标注约束的Z_A为相容赋值和；损失log Z-log Z_A；对每个二元存在特征及一个共现特征的log权重导数为全域期望减相容域期望。若Z_A=0则不相容；未标注A=Y时损失与梯度为0。边际和组合数只是模型内归一结果，不能当真实概率、证据或权限。候选域外含义、真实义务和宿主确认仍需独立验证。

## 计算
按变量顺序将涉及变量的因子相乘并对其二元值求和，生成邻域因子；重复至标量分区。分配律保证等价于全部赋值求和。通过固定命题为1重算分区得到边际分子；共现同理。时间、空间随消元中间宽度指数增长，单次分区的预算256次表项求和为研究者选择，超限返回LIMIT；该固定小图的stats仅处理默认预算下完整子查询，真实生产应统一累计预算及LIMIT传播。本轮未实测真机内存时间。参照为独立枚举64赋值及中心有限差分，均同一研究者设计，非独立科学验收。

## 实验
6个命题每个三种非空标注掩码，共729掩码×4组因子=2916次联合分区场景，逐个比较精确BigInt权重和、6个存在边际与1个共现边际；合法场景7维梯度用h=1e-5中心差分核对，绝对误差容差1e-8。强制未标注为0的对照只说明额外监督损失，不代表准确率或真实误判。错误互斥相对已资格夹具的冲突只为有限人工图；质量损失指标还受到上述软因子改变影响。独立边际差异不代表联合预测优越。合成夹具为ChatGPT研发辅助原创开发材料，不是真人、真实语料、独立留出或训练。12项专项控制。未运行平台、设备、CRF原程序或真实语言。保留R50完整范围与正式验收门。无训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。

## 可复算代码
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},N=6,full=Array(N).fill(3);
 // six binary span-role propositions; 0=absent, 1=present.
 // 0/1 overlap with distinct roles; 2/3 overlap within one role;
 // 4/5 share an anchor but represent two separate metadata propositions.
 // This is an artificial factor graph, not real Chinese annotation.
 const unary=[[1n,2n],[1n,3n],[2n,1n],[1n,2n],[2n,3n],[3n,2n]];
 // Arbitrary positive integer pair factors; 0 allowed only in a stipulated contract.
 const soft=[1n,1n,1n,3n],anti=[2n,1n,1n,1n],hard=[1n,1n,1n,0n],free=[1n,1n,1n,1n];
 const edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[0,5]];
 const policy=[ [soft,anti,soft,soft,anti,soft], [soft,anti,hard,soft,anti,soft], [hard,anti,hard,soft,hard,soft], [free,free,free,free,free,free] ];
 // Generic exact variable elimination, factors use sorted variable list and bit-indexed table.
 function value(f,assignment){let j=0;f.v.forEach((x,i)=>{j|=assignment[x]<<i});return f.w[j]}
 function partition(masks,p,cap=256){
  let f=masks.map((m,i)=>({v:[i],w:unary[i].map((w,x)=>(m&(1<<x))?w:0n)}));
  for(let k=0;k<edges.length;k++){let [a,b]=edges[k];f.push({v:[a,b],w:p[k]})}
  let maxWidth=0,entries=0;
  for(let x=0;x<N;x++){
   let hit=f.filter(t=>t.v.includes(x)),rest=f.filter(t=>!t.v.includes(x));
   let vars=[...new Set(hit.flatMap(t=>t.v))].filter(v=>v!==x).sort((a,b)=>a-b);
   maxWidth=Math.max(maxWidth,vars.length);let size=2**vars.length;
   if(entries+2*size>cap)return {status:"LIMIT"};
   entries+=2*size;let w=[];
   for(let s=0;s<size;s++){let q=Array(N).fill(0);vars.forEach((v,i)=>{q[v]=(s>>i)&1});let z=0n;
    for(let b=0;b<2;b++){q[x]=b;z+=hit.reduce((a,t)=>a*value(t,q),1n)}
    w.push(z)
   }
   f=[...rest,{v:vars,w}]
  }
  return {status:"EXACT",z:f.reduce((a,t)=>a*t.w[0],1n),maxWidth,entries};
 }
 // Enumerative reference independently evaluates 64 complete assignments.
 function oracle(masks,p){
  let z=0n,ones=Array(N).fill(0n),co=0n;
  for(let s=0;s<64;s++){
   let q=Array.from({length:N},(_,i)=>(s>>i)&1);if(q.some((b,i)=>!(masks[i]&(1<<b))))continue;
   let w=1n;for(let i=0;i<N;i++)w*=unary[i][q[i]];
   for(let k=0;k<edges.length;k++){let [a,b]=edges[k];w*=p[k][q[a]+2*q[b]]}
   z+=w;for(let i=0;i<N;i++)if(q[i])ones[i]+=w;if(q[0]&&q[1])co+=w;
  }return {z,ones,co};
 }
 function stats(m,p){
  let base=partition(m,p);if(base.status!=="EXACT")return base;
  let ones=m.map((v,i)=>{let n=m.slice();n[i]&=2;return partition(n,p).z});
  let n=m.slice();n[0]&=2;n[1]&=2;
  return {...base,ones,co:partition(n,p).z};
 }
 const f=x=>Number(x),near=(a,b)=>Math.abs(a-b)<1e-8;
 function objective(m,p){
  let a=stats(full,p),b=stats(m,p);
  if(!b.z)return {status:"INCOMPATIBLE",authority:"NONE"};
  // Fixed log-linear feature gradient for each binary proposition and one pair cooccurrence.
  return {status:"EXACT",loss:Math.log(f(a.z))-Math.log(f(b.z)),gradient:[...a.ones,a.co].map((x,i)=>f(x)/f(a.z)-f([...b.ones,b.co][i])/f(b.z)),authority:"NONE"};
 }
 // Finite-difference oracle using real exp perturbation of the sufficient statistic;
 // no optimizer and no parameter update.
 function logpart(m,p,j,delta){
  let z=0;for(let s=0;s<64;s++){
   let q=Array.from({length:N},(_,i)=>(s>>i)&1);if(q.some((b,i)=>!(m[i]&(1<<b))))continue;
   let w=1;for(let i=0;i<N;i++)w*=f(unary[i][q[i]]);
   for(let k=0;k<edges.length;k++){let [a,b]=edges[k];w*=f(p[k][q[a]+2*q[b]])}
   z+=w*Math.exp(delta*(j===6?q[0]*q[1]:q[j]));
  }return Math.log(z);
 }
 let out={maskCases:0,exactPartitionCases:0,marginalChecks:0,gradientChecks:0,feasible:0,incompatible:0,unmarkedCases:0,forcedNegativeExtraLossCases:0,forcedNegativeConflictCases:0,unjustifiedExclusivityConflict:0,unjustifiedExclusivityMassLoss:0,independentDifferentMarginalCases:0,maxWidth:0,maxEntries:0,controls:0,perPolicy:policy.map(()=>({feasible:0,incompatible:0}))};
 function check(m){
  out.maskCases++;
  let exact=[];
  for(let k=0;k<policy.length;k++){
   let p=policy[k],z=stats(m,p),o=oracle(m,p);ck(z.status==="EXACT"&&z.z===o.z,"Z");
   ck(z.ones.every((v,i)=>v===o.ones[i])&&z.co===o.co,"marginals");out.exactPartitionCases++;out.marginalChecks+=7;
   out.maxWidth=Math.max(out.maxWidth,z.maxWidth);out.maxEntries=Math.max(out.maxEntries,z.entries);exact.push(z);
   let v=objective(m,p);ck(v.authority==="NONE","authority");
   if(!z.z){ck(v.status==="INCOMPATIBLE","empty");out.incompatible++;out.perPolicy[k].incompatible++;continue}
   out.feasible++;out.perPolicy[k].feasible++;ck(v.status==="EXACT"&&v.loss>=-1e-12,"loss");
   for(let j=0;j<7;j++){
    let h=1e-5,lp=logpart(full,p,j,h)-logpart(m,p,j,h),lm=logpart(full,p,j,-h)-logpart(m,p,j,-h);
    ck(near(v.gradient[j],(lp-lm)/(2*h)),"gradient");out.gradientChecks++
   }
   if(m.every(x=>x===3)){ck(v.loss===0&&v.gradient.every(x=>x===0),"no supervision");out.unmarkedCases++}
   if(m.includes(3)){let bad=m.map(x=>x===3?1:x),b=objective(bad,p);if(b.status==="INCOMPATIBLE")out.forcedNegativeConflictCases++;else if(b.loss>v.loss+1e-12)out.forcedNegativeExtraLossCases++}
  }
  // Policy 2 adds exclusivity to overlapping distinct-role propositions and metadata
  // compared with policy 1, while all nonzero potentials on allowed pairs remain unchanged.
  if(exact[1].z&& !exact[2].z)out.unjustifiedExclusivityConflict++;
  if(exact[1].z>exact[2].z)out.unjustifiedExclusivityMassLoss++;
  if(exact[0].z&&exact[3].z&&exact[0].ones.some((v,i)=>v*exact[3].z!==exact[3].ones[i]*exact[0].z))out.independentDifferentMarginalCases++;
 }
 function walk(m){if(m.length===N){check(m);return}for(let v=1;v<=3;v++)walk([...m,v])}walk([]);
 for(let t of [()=>out.maskCases===729,()=>out.exactPartitionCases===2916,()=>out.marginalChecks===20412,()=>out.feasible+out.incompatible===2916,()=>out.gradientChecks===7*out.feasible,()=>out.unmarkedCases===4,()=>partition(full,policy[0],0).status==="LIMIT",()=>objective([2,2,3,3,3,3],policy[1]).status==="EXACT",()=>objective([2,2,3,3,3,3],policy[2]).status==="INCOMPATIBLE",()=>objective([3,3,2,2,3,3],policy[1]).status==="INCOMPATIBLE",()=>out.unjustifiedExclusivityConflict>0,()=>out.independentDifferentMarginalCases>0]){ck(t(),"control");out.controls++}
 return out;
}
```

## 实际结果
```json
{
  "maskCases": 729,
  "exactPartitionCases": 2916,
  "marginalChecks": 20412,
  "gradientChecks": 18326,
  "feasible": 2618,
  "incompatible": 298,
  "unmarkedCases": 4,
  "forcedNegativeExtraLossCases": 2285,
  "forcedNegativeConflictCases": 0,
  "unjustifiedExclusivityConflict": 136,
  "unjustifiedExclusivityMassLoss": 568,
  "independentDifferentMarginalCases": 610,
  "maxWidth": 2,
  "maxEntries": 38,
  "controls": 12,
  "perPolicy": [
    {
      "feasible": 729,
      "incompatible": 0
    },
    {
      "feasible": 648,
      "incompatible": 81
    },
    {
      "feasible": 512,
      "incompatible": 217
    },
    {
      "feasible": 729,
      "incompatible": 0
    }
  ]
}
```

## 后续
下一步可研究原始文本候选与联合因子特征的统一表示及候选覆盖，学习需独立合法数据和所有者授权。数据轨负责资料资格，独立轨负责未见评价，产品轨维护唯一交接；不凭数值正确推断自然语言识别能力。
