# 自适应澄清的具名输出保证前沿与组合语义接口
2026-11-25。RESEARCH_CANDIDATE / REUSED_R63_CODE_EXECUTED / EXACT_FINITE_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 68e05550a14779855649dc287364e99fc199430e，Draft #62固定head e61bbad10932edabc9a87483e5407fdae6c751cc，未合并。核对近期12提交、14开放PR、v3.2/同步规程/唯一产品交接前22行（交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。检索clarification/question/ambiguity/joint/semantic conflict/partial/adaptive/Pareto clarification/question budget/certificate/decision signature。审阅R5 eae10ff00db50587513bc72f628a7f0b8cd5ed8b、R40 1507376849edac68a46f352063a814b0434fd81a、R53 9702d42453b022a10100d2db9935a8a2a869ab85、R132 3a725062c742cc0116d29e0f28640bfacbecafbf、共享来源成本3e599183f3e598f2a7a789f333956bec2df72551相关合同/算法前段、上一轮共享解释68e05550a14779855649dc287364e99fc199430e前25行。R5解决固定完整签名最坏深度，R40处理带代价的最坏后悔值、模糊回答与拒绝，R132处理固定字段最小分离，R27处理局部计算接口，共享成本研究处理非自适应双资源前沿。本轮只增量处理有限问题数内的具名输出保证族、可选择的部分结果和必要确认的结合，并实际使用旧组合解析结果；不重复前述最优化。查重非全库证明。
## 资产及工程源码
research/decision_hub/2026-11-25-joint-quantity-semantic-inference.md @ 68e05550a14779855649dc287364e99fc199430e blob 296465980e23a1d8082f81a8181343668965328b。获取全文核对连接器blob，实际执行原parse/evalTree/cmp/q/relation，未改变函数。未运行连续域solve、真实自然语言入口或完整App。decision_planner.py固定v0.7 blob f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b，实际读1–160行及函数目录；_clarification按缺失字段提示，_feasibility已支持基于当前确定失败见证暂缓其余同方案筛查，_comparison和_model_disagreements提供专项问题。现有逻辑已有价值，本轮不是已确认原生缺陷或实测用户问题数优化。
实际compare最新main与固定#62：diverged，候选独有1提交、落后main 25提交，merge base 6e44ecf50e9e8de0d8a3eb76766cd0d3bf44ab9c，候选方向126文件；17个platform/future_model/src/psychohistory文件变动，含language/semantics/evidence/conversation/math/resources/knowledge/candidates/scenarios及API/CLI。只核对差异清单，未逐文件合并、未运行CI或确认冲突。上述计数为写本报告之前的快照，不表示当前最新main永远相同。后续完整版本应先核对最新基线和#62所有未验收能力。
## 合同
有限8个联合解释世界w=(x,y,j)，x/y为人工绑定的两个二值工时测量，j为固定共享条件G的两种解析树编号。R63实际解析有限中文数量组合，使用其有理数比较和树求值，构造G及两个分支B,C；P=G_j?B:C。j在同一世界内固定；不依据文字相同自动共享变量。0/1秒只作有限夹具。4个具名结果端口bit1政策合格P、bit2守卫真值G、bit4独立测量y、bit8人工决策签名P且x=1。最后一个为纯测试标签，不是实际推荐；确定端口可为真假或具体0/1值，不能把“已解决”当“通过”。初始支持为8世界的非空子集H，允许相关、无概率；域及来源覆盖由人工给定，不从原文自动获得。端口分别检查所有当前世界是否同一值；第二种模式另要求bit1/bit8有明确语义确认，即使数值不变也不能省略。真正用户权限、重大风险、全部原文义务及独立证据资格另行检查；本实验的c标志仅人为资格。全部研究输出authority NONE。
4个问题：q0确定返回共享解释编号且模拟明确确认，q1/q2确定返回各测量，q3模拟有重叠回答支持（除x=y=1允许两个回答，其余返回异或），未生成真实问题文字，未估计人类答复或获取外部事实；有限拒答模式0/1，明确假设最多拒绝一次，不能把它作为真实用户行为保证。拒答不收缩域，不新增确认，移除该问题；无限拒答控制。用户退出或拒绝数据授权应立即停止相应询问，真实系统不应强制继续；本轮不模拟真实许可、时间变化、代价、多轮语义重解释、未知域、答复相互依赖或答复有误。全部4问可用由夹具给定，问题数预算1/2，不等同真实认知负担。
## 数学
终端可解决具名集合T(S,c)={i:端口i在S所有世界同值且资格满足}。设F(S,Q,d,r,c)为可保证解决集合的包含极大前沿，允许不继续问。d=0时仅T。若问q，所有可能回答y（含拒答）产生状态s_y，不允许跨答复假定相同世界。每个回答分支可自适应选子策略，对每个分支选择一个F_y成员A_y；该树保证的具体端口是交集_y A_y。递推F=MaxIncl({T}∪并_q {交集_y A_y:A_y∈F_y})。子集偏序剪枝正确，因为与任意集合取交集对包含关系单调；任一策略首步为停止或问某q，子树归纳给出必要充分性。不同分支解决相同端口的值可以不同，保证是将来获答后能确定哪个值，非当前已确定。只保留最大集合可按指定目标判断是否有成员覆盖目标。不同策略的前沿成员并集通常不可同时实现；最坏分支解决数量最大值也不意味着能保证同样数量的具名端口。此递推未保留实际策略树和所有并列首问，未实现问题许可、总预算截断和生产资源保护；一般端口数/问题数/分支数的组合开销可能指数增长。无限拒答时存在所有问均拒答的路径，无新增资格和事实，故F只有初始T；不说明自愿答复毫无价值。
## 实际实验
4守卫比较×3阈值×2真分支比较×2假分支比较=48配置，384实际解析树逐世界核对（对照生成模板直接布尔和整数比较）；255非空域×2资格模式×2预算×2拒答模式×48=97920主案例。逐目标16掩码进行直接按端口值分桶及递归存在性检查，1,566,720次核验全一致。两算法共享人工世界、答复规则及问题集合，非独立验收。再对所有固定问题序列、允许提前停止的自适应前沿、最坏分支解决数量最优值比较。固定序列允许按预算内任一长度，重复问禁止；终端集合随有效答复单调不减，所以无需在固定序列内模拟分支提前终止即可验证保证集合。固定序列基线是研究用，不是v0.7实测。24,480无限拒答控制、9专项断言。实际运行两次，核心计数一致。
2,850组自适应前沿严格扩大（至少一个具名目标固定策略无法保证）；全部4端口可保证解决数25,240 vs 24,184，增加1,056组。45,792组初始已有部分端口（每域四个预算/拒答配置重复计数）。15,046组最坏分支解决数量最优值大于具名保证最大数量；19,086组不同策略前沿并集不可一次保证；8,472组强制确认模式初始阻止本可由数学决定的端口（仅required=9，分母12240，未计预算/拒答重复），1,222组虽共享解释在域中已经固定，仍有需要独立确认的确定端口。这些数值是有限人工组合，非实际用户占比、产品错误率或减少真实问数。不可用这些结果宣称超过通用AI。
示例witness union：m=7时前沿[11,12]，即一次询问可以保证端口{1,2,8}或{4,8}，不能保证全部4。scalar：同m在d=2且最多一次拒答时具名前沿[8]，虽能保证每条路径至少解决2项，不能承诺除bit8外的任何特定项。adaptive：required=9、m=58、无拒答、两问，具名前沿[15]，固定序列仅[6,12]，说明按实际答复调整下一问的价值。真实产品须保留完整可复算策略见证与必要授权，不能将上述测试标签转为现实选择。
## 原生接口及v0.8准备增量
保留现有明确失败暂缓规则和C028硬门。语言候选由R63/102/103/116/131及Unicode桥提供，语义义务/来源/参数资格由可信宿主建立，缺覆盖不可用本闭域前沿声明最优或停止。方法目标明确区分硬约束、条件结果、独立测量、比较与建议；沿R27局部端口和f3708addeea0344826d49ea41dfd7e1ff2a5c44f权威隔离，先提供有证据的局部分析，再提出真正相关的一个问题。用户拒绝后保留未知与已核实结果；不要默认固定拒答次数。必须确认的硬底线、授权、风险不可用数量评分抵销。后续将前沿策略绑定问题ID、解释ID、作用域、原文、来源、会话实例、修订及代次；跨轮变化废弃旧策略，保留未受影响端口；预算或域不足则显示局限，不能把未求解写作最优。完整原生测试需从start/turn/confirm/compute到选择/保存，覆盖答复模糊、反问、拒答、语义更正、旧计算、条件局部输出及真正用户摩擦，独立轨保管未见情节。产品轨维护唯一交接。本轮仅梳理接口与差异清单，未完成完整v0.8任务规格，未启动Codex。自行选择四端口、回答模型、预算与人工确认模式。无真实个人数据、训练、第三方AI运行时、正式源码修改、CI、PR合并、部署、费用或冻结变更。
## 实际复算
固定资产全文为字符串doc，标准JS运行，只加载已审查自有代码。
```js
function load(doc){
 const src=doc.split("```js\n")[1].split("\n```")[0].split(" const ops=")[0];
 return Function(src+"\nreturn {parse,evalTree,cmp,q,relation};\n};\nreturn probe();")()
}
function experiment(P){
 const ck=(v,m)=>{if(!v)throw Error(m)},W=Array.from({length:8},(_,i)=>i),Q=[0,1,2,3],bits=[1,2,4,8],pop=x=>x.toString(2).replace(/0/g,"").length;
 const xyz=w=>[w&1,(w>>1)&1,(w>>2)&1];
 const rel=(x,n,o)=>o==="<="?x<=n:o==="<"?x<n:o===">="?x>=n:x>n;
 const ops=[["最多","<="],["少于","<"],["至少",">="],["超过",">"]],word=(o,n)=>"每周工时"+o+n+"秒";
 const replies=Q.map(q=>W.map(w=>{let [x,y,j]=xyz(w);return q===0?1<<j:q===1?1<<x:q===2?1<<y:x&&y?3:1<<(x^y)}));
 function maximal(xs){let a=[...new Set(xs)];return a.filter(x=>!a.some(y=>x!==y&&(x&y)===x)).sort((a,b)=>a-b)}
 function branches(m,q,r,confirm){
  let a=[];for(let v=0;v<2;v++){let n=0;for(let w of W)if((m&(1<<w))&&(replies[q][w]&(1<<v)))n|=1<<w;if(n)a.push([n,r,confirm||q===0])}
  if(r!==0)a.push([m,r===-1?-1:r-1,confirm]);
  return a
 }
 function engine(labels,required){
  function terminal(m,confirmed){
   let v=15;let first=W.find(w=>m&(1<<w));for(let w of W)if(m&(1<<w))v&=~(labels[first]^labels[w]);
   return v&(confirmed?15:15^required)
  }
  const memo=new Map(),oracleMemo=new Map(),scalarMemo=new Map(),fixedMemo=new Map();
  function dp(m,qs,d,r,c){
   let k=[m,qs,d,r,+c].join(":");if(memo.has(k))return memo.get(k);
   let all=[terminal(m,c)];
   if(d)for(let q of Q)if(qs&(1<<q)){
    let v=[15];for(let [n,s,t] of branches(m,q,r,c))v=maximal(v.flatMap(a=>dp(n,qs^(1<<q),d-1,s,t).map(b=>a&b)));
    all.push(...v)
   }
   let a=maximal(all);memo.set(k,a);return a
  }
  function oracle(m,qs,d,r,c,target){
   let k=[m,qs,d,r,+c,target].join(":");if(oracleMemo.has(k))return oracleMemo.get(k);
   let ok=(!(target&required)||c)&&bits.filter(b=>target&b).every(b=>new Set(W.filter(w=>m&(1<<w)).map(w=>!!(labels[w]&b))).size===1);
   if(!ok&&d)for(let q of Q)if(qs&(1<<q)){
    let rs=[0,1].map(v=>W.filter(w=>(m&(1<<w))&&(replies[q][w]&(1<<v))).reduce((a,w)=>a|(1<<w),0)).filter(Boolean);
    ok=rs.every(n=>oracle(n,qs^(1<<q),d-1,r,c||q===0,target))&&(r===0||oracle(m,qs^(1<<q),d-1,r===-1?-1:r-1,c,target));if(ok)break
   }
   oracleMemo.set(k,ok);return ok
  }
  function scalar(m,qs,d,r,c){
   let k=[m,qs,d,r,+c].join(":");if(scalarMemo.has(k))return scalarMemo.get(k);
   let best=pop(terminal(m,c));
   if(d)for(let q of Q)if(qs&(1<<q))best=Math.max(best,Math.min(...branches(m,q,r,c).map(([n,s,t])=>scalar(n,qs^(1<<q),d-1,s,t))));
   scalarMemo.set(k,best);return best
  }
  function fixed(m,qs,d,r,c){
   let k=[m,qs,d,r,+c].join(":");if(fixedMemo.has(k))return fixedMemo.get(k);
   let out=[terminal(m,c)];
   function apply(states,remaining,h){
    if(!h)return;
    for(let q of Q)if(remaining&(1<<q)){
     let a=states.flatMap(([n,s,t])=>branches(n,q,s,t)),v=a.reduce((p,[n,s,t])=>p&terminal(n,t),15);
     out.push(v);apply(a,remaining^(1<<q),h-1)
    }
   }
   apply([[m,r,c]],qs,d);out=maximal(out);fixedMemo.set(k,out);return out
  }
  return {dp,oracle,scalar,fixed,terminal}
 }
 let o={configurations:0,worldChecks:0,cases:0,targetChecks:0,partialWithoutQuestion:0,adaptiveStrict:0,adaptiveAllPorts:0,fixedAllPorts:0,scalarCountGap:0,unionNotAchievable:0,mandatoryBlocks:0,mandatoryInvariantDirectQuestion:0,unlimitedRefusalControls:0,controls:0,witnesses:{}};
 for(let [g,go] of ops)for(let n of [0,1,2])for(let [b,bo] of ops.slice(0,2))for(let [c,co] of ops.slice(2)){
  let txt=word(g,n)+"且"+word("至少",1)+"或者"+word("少于",1);
  let G=P.parse(txt),B=P.parse(word(b,1)),C=P.parse(word(c,1));ck(G.trees.length===2,"guard");
  function ts(p,ids,w){let v=xyz(w);let a=p.atoms.map((x,i)=>P.relation(P.cmp(P.q(BigInt(v[ids[i]])),x.value),x.op));return p.trees.map(t=>P.evalTree(t,a))}
  let labels=W.map(w=>{let [x,y,j]=xyz(w),a=ts(G,[0,1,0],w)[j],p=a?ts(B,[0],w)[0]:ts(C,[1],w)[0];let d=rel(x,n,go),e=y>=1,f=x<1,h=j===0?d&&(e||f):(d&&e)||f,ok=h?rel(x,1,bo):rel(y,1,co);ck(a===h&&p===ok,"reference");o.worldChecks++;return (+p)|(+a<<1)|(y<<2)|((p&&x===1?1:0)<<3)});
  o.configurations++;
  for(let required of [0,9]){
   let E=engine(labels,required);
   for(let m=1;m<256;m++){
    let start=E.terminal(m,false);if(required&&start!==engine(labels,0).terminal(m,false))o.mandatoryBlocks++;
    if(required&&new Set(W.filter(w=>m&(1<<w)).map(w=>xyz(w)[2])).size===1&&(E.terminal(m,true)&required&~start))o.mandatoryInvariantDirectQuestion++;
    for(let d of [1,2])for(let r of [0,1]){
     let a=E.dp(m,15,d,r,false),b=E.fixed(m,15,d,r,false),all=a.reduce((s,x)=>s|x,0),best=Math.max(...a.map(pop)),scalar=E.scalar(m,15,d,r,false);
     for(let t=0;t<16;t++){ck(a.some(x=>(x&t)===t)===E.oracle(m,15,d,r,false,t),"oracle");o.targetChecks++}
     ck(b.every(t=>a.some(x=>(x&t)===t)),"fixed subset");ck(scalar>=best,"count bound");o.cases++;
     o.partialWithoutQuestion+=+(start!==0&&start!==15);
     if(a.some(t=>!b.some(x=>(x&t)===t))){o.adaptiveStrict++;o.witnesses.adaptive??={txt,required,m,d,r,labels,a,b}}
     o.adaptiveAllPorts+=+a.includes(15);o.fixedAllPorts+=+b.includes(15);
     if(scalar>best){o.scalarCountGap++;o.witnesses.scalar??={txt,required,m,d,r,labels,a,scalar}}
     if(!a.includes(all)){o.unionNotAchievable++;o.witnesses.union??={txt,required,m,d,r,labels,a,all}}
    }
    ck(E.dp(m,15,2,-1,false).join()===String(start),"unlimited refusal");o.unlimitedRefusalControls++
   }
  }
 }
 for(let v of [o.configurations===48,o.worldChecks===384,o.cases===97920,o.targetChecks===1566720,o.unlimitedRefusalControls===24480,o.mandatoryInvariantDirectQuestion>0,o.scalarCountGap>0,o.unionNotAchievable>0,o.adaptiveStrict>0]){ck(v,"control "+o.controls);o.controls++}
 return o
}
console.log(JSON.stringify(experiment(load(doc)),null,2));
```
## 实测
```json
{
  "configurations": 48,
  "worldChecks": 384,
  "cases": 97920,
  "targetChecks": 1566720,
  "partialWithoutQuestion": 45792,
  "adaptiveStrict": 2850,
  "adaptiveAllPorts": 25240,
  "fixedAllPorts": 24184,
  "scalarCountGap": 15046,
  "unionNotAchievable": 19086,
  "mandatoryBlocks": 8472,
  "mandatoryInvariantDirectQuestion": 1222,
  "unlimitedRefusalControls": 24480,
  "controls": 9,
  "witnesses": {
    "union": {
      "txt": "每周工时最多0秒且每周工时至少1秒或者每周工时少于1秒",
      "required": 0,
      "m": 7,
      "d": 1,
      "r": 0,
      "labels": [
        3,
        0,
        7,
        13,
        3,
        0,
        7,
        13
      ],
      "a": [
        11,
        12
      ],
      "all": 15
    },
    "scalar": {
      "txt": "每周工时最多0秒且每周工时至少1秒或者每周工时少于1秒",
      "required": 0,
      "m": 7,
      "d": 2,
      "r": 1,
      "labels": [
        3,
        0,
        7,
        13,
        3,
        0,
        7,
        13
      ],
      "a": [
        8
      ],
      "scalar": 2
    },
    "adaptive": {
      "txt": "每周工时最多0秒且每周工时至少1秒或者每周工时少于1秒",
      "required": 9,
      "m": 58,
      "d": 2,
      "r": 0,
      "labels": [
        3,
        0,
        7,
        13,
        3,
        0,
        7,
        13
      ],
      "a": [
        15
      ],
      "b": [
        6,
        12
      ]
    }
  }
}
```
