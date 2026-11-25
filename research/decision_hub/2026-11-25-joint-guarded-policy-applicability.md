# 多条件政策、共享语义解释及联合情景参数资格
2026-11-25。RESEARCH_CANDIDATE / REUSED_R63_CODE_EXECUTED / SYNTHETIC_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 3b2e5cdb7172c5644c76ba56cee3fdf6060762a4，Draft #62 固定head e61bbad10932edabc9a87483e5407fdae6c751cc待审。核对近期12提交、14开放PR、v3.2及同步规程前22行、唯一产品交接前22行blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。检索conditional/semantic inference/subject/composition/joint inference/parameter projection/guard/relocation/exception/move_if_onsite。审阅R61 e22acd18167c17df765996feea082ecc83703aaf、R62 bc4efb83819a198a981598c51ff33ceaf8a7e42c、R57 dd45037da2fe04dbb7687d110e75c2eda2eeb4ad、R35 c95c6e61137c9e45d8aa87298371ad1de831f22e、R130 5627ea49ee889773c8af1db373b3da0dfdf21f8d合同前段及R63完整代码。既有R63在已绑定变量上推理布尔树，R130隔离单条件政策/事实零值，R131研究条件连接候选，R93语义相关域，近期联合情景连接研究。本轮增量为多条件政策的触发状态、适用性和共享解释绑定；不是新开放语义识别算法，也非已发现的原生缺陷。查重非全库证明。
## 固定资产与原生接口审阅
research/decision_hub/2026-11-25-joint-quantity-semantic-inference.md @ 3b2e5cdb7172c5644c76ba56cee3fdf6060762a4 blob 296465980e23a1d8082f81a8181343668965328b。全文实际取得，连接器blob一致，直接执行已审查项目自有JS函数parse/evalTree/cmp/q/relation，不改原函数。没有调用R63连续矩形solve，新增9个离散情景而非连续域。生产禁止执行任意外部文本。
固定v0.7源：decision_language.py 4e6733499f74db505e2cedaff84cf8c5eae207d1，_conditional_start 518起、_SIMPLE_RELOCATION_EXCEPTION 541起、_clause_obligations 692起、interpret 795–895；decision_conversation.py ed1c5aa8407f53ef3dfc1484ba1a18ef1edabcad active_claims及blocking_constraints 132–172；decision_conversation_math.py de49b71a3c8bb63c81539dd9c69b3c02b3e94c23 lines1–260；decision_semantics.py c7158c996f82c208b4d142b2863ddc3e27efa267 lines109–176。当前仅明确支持搬家到岗例外的特定条件组合；其他条件义务有阻断路径，不能把v0.6的旧缺陷直接视为v0.7缺陷。本轮静态读取，不执行原生语言、会话、真实权限、C028或完整App。
## 合同及数学
用人工限定语法“如果G，就必须B”封装原R63完整输入解析；G/B为原支持的显式周期工时秒数比较，多树保留。没有自动理解普通白话主体、条件指代、说话人、现实义务或真实工时。0..2秒是为枚举严格比较而设的虚构数值。两变量X/Y由可信宿主明确绑定为不同或相同指标身份；同词面不是身份。现实证据、独立原文覆盖、主体/适用性/用途/版本由合成夹具提供。缺任何资格返回UNKNOWN_QUALIFICATION；REPORT不作为政策进入本接口，不能将用户政策反推实际事实或把报告直接变成政策。事实域为空CONFLICT，未知来源不能充当空域。
A：固定政策G=>B，在每个情景/解释内，G假为INACTIVE，G真且B真为ACTIVE_PASS，G真且B假为ACTIVE_FAIL。前两者对该政策不构成违反；不证明条件实际成立，也不证明全部决策义务已满足。不同政策的解释选择只有在可信宿主已确认为独立（或一个只有唯一读法，如本轮A）时才能各取组合；同一联合情景的量值保持关联。对各情景可行支持是存在一个解释使全部适用政策不违反，违反支持是存在一个解释使至少一政策违反；这两个支持可重叠。适用性确认NOT_APPLICABLE时保留明示不适用状态，UNRESOLVED时保留适用/不适用候选且最终UNKNOWN_APPLICABILITY，不擅自扩大或取消用户硬约束。此候选保守，即便已知某独立条件失败仍以资格状态为主，明细保留；不宣称最小追问。ALL_PASS/ALL_FAIL只在完整非空夹具域及已确认适用性下针对这些政策、所有读取解释和情景成立；不得升级为整体选择许可。全为INACTIVE只证明该政策未触发。所有authority NONE。
B：可信宿主确认两条政策引用同一个歧义条件G，第二条为其逻辑补集：G=>B且非G=>C。固定解释j与情景w组合的满足性等价于G_j(w)真时B(w)，否则C(w)。每个解释在全部世界固定，记录满足世界集合M_j；逐情景可能满足集合为并集M_j，所有解释均通过为交集M_j=H。存在统一可行解释须某个M_j=H；并集等于H不足以证明。错误地分别为两条政策选择相互独立的G解释，可在同一世界产生互相矛盾的假前提，虚构可行性；这属于语义身份错误，非概率相关。不同原文/不同含义不能默认共享解释；即使文字相同，也必须有可信共同义务/条件身份及作用域证据。B保留完整解释掩码族用于计数，代码为报告排序丢失解释ID，未实现真实可审计解释票据；生产必须保留ID、解析树、原文、变量、适用性、版本、权限和联合域，不允许任意序号对齐。也不把存在一个统一解释等同于用户已确认该解释。无真实因果推断、预测概率、自动执行、字典扩张或训练。
## 实验及结论
A：4守卫比较×4后果比较×3阈值×3括号模式×2绑定=288配置，53个非空支持域（49矩形组合+4额外相关掩码）×3适用性=45,792；2,592逐世界对照。直接算术/布尔模板及穷举适用性核对所有支持及状态。16控制。错误基线naiveSkipFalsePass是守卫未确定真即忽略整个政策，4,544组本应存在违反见证却被该捷径视为全过，含本应混合或全失败；naiveMarginalExtraUnknown是将守卫与后果边际独立组合，862组将本来全域通过误成未知。全部未触发第一政策7,584组，含第二政策可能失败或适用性未知，不能据此判全局。
B：4守卫比较×3阈值×4真分支比较×4假分支比较=192配置，枚举9世界的511非空支持域=98,112。1,728逐世界直接布尔参照；共享同一个聚合函数的两路径核对解释支持族（不是完全独立实现），7控制。27,392组独立解释基线在至少一个情景错误引入可能通过，包含1,324组实际所有情景/解释均失败却基线认为仍可通过。1,020组逐情景可找到解释却无任何统一通过的解释。12,428组至少一个统一通过解释，其中5,560组所有解释均通过。合计143,904主案例、4,320逐世界对照及23专项控制；数字是同一研究者的有限开发夹具组合，非独立用户、原生产品错误率或开放语义准确率。全部运行无异常；归档代码再次执行，核心计数核对一致。
例：B中mask32只含(X=1,Y=2)，真分支X<1、假分支Y<=1均失败；歧义G能真能假。独立读取可为第一条取G假且为第二条取G真，使两条表面都未触发，正确共同读取下无通过。uniformWitness的mask12含(0,2),(1,0)，两读取满足集合分别4与8；并集12却无单一解释覆盖12。
## 原生接入研究规格（非正式版本授权）
1. 组合语义候选接口复用R63、R102、R103、R116、R131及上一轮Unicode位置桥；保留每个原文义务、条件候选、角色、比较符、计量范围、歧义和outside。不可把解析器生成的候选当真实确认；宿主明确主体及个人约束/外部适用约束/报告，明确原文未覆盖时追问或局部输出。
2. 参数层统一事实身份、来源、时间、单位、修订、授权；条件G采用规范解释ID；同一守卫引用及补集共享该解释，而非每条规则重新取最有利读法。与最近knowledge-qualification、semantic-projection-boundary及scenario-score-basis研究配合。
3. 计算层保持联合支持和可行集合，区分条件未触发、适用性待核、触发后通过/失败、语义歧义、来源未知。将本轮有限结果作为隔离候选；现有原生C028完整硬门不应被研究函数替换。与world-bound-multistage-result-join及resumable-budgeted-world-join接口的结合尚未执行；中断也不能发布无条件全域结论。
4. 原生回归应从真实start/turn/confirm/project/compute触发，覆盖：同一守卫跨轮引用与明确修订、多个不同守卫、适用性改变、他人条件与本人采纳、缺事实、真实报告隔离、严格比较边界、跨端原文位置、显式否定、共享解释失效、旧收据、已有搬家到岗例外不退步；另测未知是否影响局部结果、原生模型调度、全部历史回归和独立未见情节。用户优先明确真正影响决策的条件，不要求先选模型。
5. v0.8完整规格仍需审#62与最新main差异、归并所有近期研究资产、确定执行环境、真实原生入口及独立验收；本轮不是完整研发规格、未交付Codex任务或修改正式产品源码。产品轨维护唯一交接。研究者选择有限语法、参数域、适用性模型及共享解释压力样例。无真实个人数据、第三方AI运行时、训练、CI、PR合并、部署、费用或冻结变化。
## 实际执行代码
从固定报告全文提供字符串doc，使用Node标准JS，无外部依赖。仅加载已审查项目自有代码。
```js
function load(doc){
 const src=doc.split("```js\n")[1].split("\n```")[0].split(" const ops=")[0];
 return Function(src+"\nreturn {parse,evalTree,cmp,q,relation};\n};\nreturn probe();")()
}
function experiment(P){
 const ck=(v,m)=>{if(!v)throw Error(m)},W=Array.from({length:9},(_,i)=>[Math.floor(i/3),i%3]);
 const ops=[["最多","<="],["少于","<"],["至少",">="],["超过",">"]];
 const word=(o,n)=>"每周工时"+o+n+"秒";
 const rel=(x,n,op)=>op==="<="?x<=n:op==="<"?x<n:op===">="?x>=n:x>n;
 const scope=a=>({covered:true,current:true,qualified:true,role:"POLICY",applicability:a});
 function parsePolicy(text,gb,rb){
  const m=/^如果(.+)，就必须(.+)$/u.exec(text);
  if(!m)return null;
  let g=P.parse(m[1]),b=P.parse(m[2]);
  if(g.status!=="CANDIDATE"||b.status!=="CANDIDATE"||g.atoms.length!==gb.length||b.atoms.length!==rb.length)return null;
  return {g,b,gb,rb,text}
 }
 function treeTruth(p,ids,w){
  let ts=p.atoms.map((a,i)=>P.relation(P.cmp(P.q(BigInt(w[ids[i]])),a.value),a.op));
  return p.trees.map(t=>P.evalTree(t,ts));
 }
 const truth=(p,ids,w)=>[...new Set(treeTruth(p,ids,w))];
 function states(p,w){
  let out=new Set();
  for(let g of truth(p.g,p.gb,w))for(let b of truth(p.b,p.rb,w))
   out.add(!g?"INACTIVE":b?"ACTIVE_PASS":"ACTIVE_FAIL");
  return out
 }
 function prepare(p,s){
  return !!(p&&s&&s.covered&&s.current&&s.qualified&&s.role==="POLICY"&&
   ["APPLIES","NOT_APPLICABLE","UNRESOLVED"].includes(s.applicability)&&
   [...p.g.atoms,...p.b.atoms].every(a=>a.metric==="工时"&&a.period==="week"&&a.unit==="s")&&
   [...p.gb,...p.rb].every(x=>x===0||x===1))
 }
 function evaluate(ps,scopes,mask){
  const no=status=>({status,authority:"NONE"});
  if(!Number.isInteger(mask)||mask<0||mask>511)return no("INVALID_DOMAIN");
  if(!mask)return no("CONFLICT");
  if(!ps.every((p,i)=>prepare(p,scopes[i])))return no("UNKNOWN_QUALIFICATION");
  let possiblePass=0,possibleFail=0,detail=ps.map(()=>({inactive:0,activePass:0,activeFail:0,notApplicable:0,unresolved:0}));
  for(let i=0;i<9;i++)if(mask&(1<<i)){
   let ok=true,bad=false;
   for(let j=0;j<ps.length;j++){
    let s=scopes[j],d=detail[j],a=states(ps[j],W[i]);
    if(s.applicability==="NOT_APPLICABLE"){d.notApplicable|=1<<i;continue}
    if(s.applicability==="UNRESOLVED")d.unresolved|=1<<i;
    if(a.has("INACTIVE"))d.inactive|=1<<i;
    if(a.has("ACTIVE_PASS"))d.activePass|=1<<i;
    if(a.has("ACTIVE_FAIL"))d.activeFail|=1<<i;
    ok=ok&&(s.applicability==="UNRESOLVED"||a.has("INACTIVE")||a.has("ACTIVE_PASS"));
    bad=bad||a.has("ACTIVE_FAIL");
   }
   if(ok)possiblePass|=1<<i;if(bad)possibleFail|=1<<i
  }
  return {status:scopes.some(s=>s.applicability==="UNRESOLVED")?"UNKNOWN_APPLICABILITY":possiblePass&&possibleFail?"CONDITIONAL_MIXED":possibleFail?"CONDITIONAL_ALL_FAIL":"CONDITIONAL_ALL_PASS",
    authority:"NONE",possiblePass,possibleFail,detail};
 }
 const masks=new Set([273,84,341,170]);
 for(let a=1;a<8;a++)for(let b=1;b<8;b++){let mask=0;for(let i=0;i<9;i++)if((a&(1<<W[i][0]))&&(b&(1<<W[i][1])))mask|=1<<i;masks.add(mask)}
 let o={textPairs:0,cases:0,worldChecks:0,allPass:0,allFail:0,mixed:0,unresolvedApplicability:0,naiveSkipFalsePass:0,naiveMarginalExtraUnknown:0,activeFailWitnesses:0,allInactiveFirstPolicy:0,controls:0,witness:null};
 for(let [g,go] of ops)for(let [b,bo] of ops)for(let n of [0,1,2])for(let mode of ["AMBIGUOUS","LEFT","RIGHT"])for(let shared of [false,true]){
  let x=word(g,n),y=word("至少",1),z=word("少于",2);
  let guard=mode==="LEFT"?`（${x}且${y}）或者${z}`:mode==="RIGHT"?`${x}且（${y}或者${z}）`:`${x}且${y}或者${z}`;
  let p=parsePolicy("如果"+guard+"，就必须"+word(b,1),[0,shared?0:1,0],[shared?0:1]);
  let q=parsePolicy("如果"+word("超过",0)+"，就必须"+word("最多",1),[1],[0]);
  ck(p&&q,"parse");o.textPairs++;
  let direct=W.map(([u,v])=>{
   let a=rel(u,n,go),c=(shared?u:v)>=1,d=u<2,r=rel(shared?u:v,1,bo);
   let gs=mode==="LEFT"?[(a&&c)||d]:mode==="RIGHT"?[a&&(c||d)]:[(a&&c)||d,a&&(c||d)];
   return {gs,body:r,second:v<=0?"INACTIVE":u<=1?"ACTIVE_PASS":"ACTIVE_FAIL",
     first:new Set(gs.map(t=>!t?"INACTIVE":r?"ACTIVE_PASS":"ACTIVE_FAIL"))}
  });
  for(let i=0;i<9;i++){
   let a=states(p,W[i]),b=states(q,W[i]);
   ck(a.size===direct[i].first.size&&[...a].every(s=>direct[i].first.has(s))&&b.has(direct[i].second),"world truth");
   o.worldChecks++
  }
  for(let mask of masks)for(let ap of ["APPLIES","NOT_APPLICABLE","UNRESOLVED"]){
   let res=evaluate([p,q],[scope("APPLIES"),scope(ap)],mask),pass=0,fail=0;
   let selected=direct.filter((_,i)=>mask&(1<<i)),guard=selected.flatMap(w=>w.gs),body=selected.map(w=>w.body);
   for(let i=0;i<9;i++)if(mask&(1<<i)){
    let w=direct[i];
    for(let g of w.gs)for(let active of ap==="UNRESOLVED"?[false,true]:[ap==="APPLIES"]){
     if((!g||w.body)&&(!active||w.second!=="ACTIVE_FAIL"))pass|=1<<i;else fail|=1<<i
    }
   }
   ck(res.possiblePass===pass&&res.possibleFail===fail,"joint");
   let expected=ap==="UNRESOLVED"?"UNKNOWN_APPLICABILITY":pass&&fail?"CONDITIONAL_MIXED":fail?"CONDITIONAL_ALL_FAIL":"CONDITIONAL_ALL_PASS";
   ck(res.status===expected,"status");o.cases++;
   o[ap==="UNRESOLVED"?"unresolvedApplicability":pass&&fail?"mixed":fail?"allFail":"allPass"]++;
   o.activeFailWitnesses+=+(res.detail[0].activeFail!==0);
   o.allInactiveFirstPolicy+=+(res.detail[0].inactive===mask&&!res.detail[0].activePass&&!res.detail[0].activeFail);
   if(ap==="NOT_APPLICABLE"&&!guard.every(Boolean)&&fail){o.naiveSkipFalsePass++;o.witness??={text:p.text,mask,pass,fail,detail:res.detail[0]}}
   if(ap==="NOT_APPLICABLE"&&pass===mask&&fail===0&&guard.some(Boolean)&&body.some(x=>!x))o.naiveMarginalExtraUnknown++;
  }
 }
 const p=parsePolicy("如果每周工时最多1秒，就必须每周工时少于2秒",[0],[0]),s=scope("APPLIES");
 for(let x of [o.textPairs===288,o.cases===45792,o.worldChecks===2592,o.naiveSkipFalsePass>0,o.naiveMarginalExtraUnknown>0,evaluate([p],[s],0).status==="CONFLICT",evaluate([p],[{...s,current:false}],1).status==="UNKNOWN_QUALIFICATION",evaluate([p],[{...s,covered:false}],1).status==="UNKNOWN_QUALIFICATION",evaluate([p],[{...s,qualified:false}],1).status==="UNKNOWN_QUALIFICATION",evaluate([p],[{...s,role:"REPORT"}],1).status==="UNKNOWN_QUALIFICATION",evaluate([p],[scope("UNRESOLVED")],1).status==="UNKNOWN_APPLICABILITY",evaluate([p],[scope("NOT_APPLICABLE")],511).detail[0].notApplicable===511,parsePolicy("如果每周工时最多1秒，就必须每周工时少于2元",[0],[0])===null,parsePolicy("如果每周工时最多1秒，就必须每周工时为2秒",[0],[0])===null,parsePolicy("如果每周工时最多1秒，就必须每周工时少于2秒",[0,1],[0])===null,evaluate([p],[s],512).status==="INVALID_DOMAIN"]){ck(x,"control "+o.controls);o.controls++}
 return o
}
function sharedGuard(P){
 const ck=(v,m)=>{if(!v)throw Error(m)},W=Array.from({length:9},(_,i)=>[Math.floor(i/3),i%3]);
 const ops=[["最多","<="],["少于","<"],["至少",">="],["超过",">"]];
 const word=(o,n)=>"每周工时"+o+n+"秒";
 const rel=(x,n,op)=>op==="<="?x<=n:op==="<"?x<n:op===">="?x>=n:x>n;
 function truths(p,ids,w){
  let a=p.atoms.map((x,i)=>P.relation(P.cmp(P.q(BigInt(w[ids[i]])),x.value),x.op));
  return p.trees.map(t=>P.evalTree(t,a))
 }
 let o={configurations:0,cases:0,worldChecks:0,independentFalsePossiblePass:0,independentFalseNotAllFail:0,pointwiseNotUniform:0,uniformReadingExists:0,allReadingsPass:0,controls:0,witness:null,uniformWitness:null};
 for(let [g,go] of ops)for(let n of [0,1,2])for(let [b,bo] of ops)for(let [c,co] of ops){
  let txt=word(g,n)+"且"+word("至少",1)+"或者"+word("少于",2);
  let G=P.parse(txt),B=P.parse(word(b,1)),C=P.parse(word(c,1));
  ck(G.status==="CANDIDATE"&&G.trees.length===2,"two trees");
  let direct=W.map(([u,v])=>{let a=rel(u,n,go),b=v>=1,c=u<2;return {gs:[(a&&b)||c,a&&(b||c)],b:rel(u,1,bo),c:rel(v,1,co)}});
  let rows=W.map(w=>({gs:truths(G,[0,1,0],w),b:truths(B,[0],w)[0],c:truths(C,[1],w)[0]}));
  function evalRows(rows,mask){
   let readingMasks=Array(rows[0].gs.length).fill(0),independent=0,possibleFail=0;
   for(let i=0;i<9;i++)if(mask&(1<<i)){
    let {gs,b,c}=rows[i];
    for(let j=0;j<gs.length;j++){if(gs[j]?b:c)readingMasks[j]|=1<<i;else possibleFail|=1<<i}
    if(gs.some(x=>!x||b)&&gs.some(x=>x||c))independent|=1<<i;
   }
   return {readingMasks:readingMasks.sort((a,b)=>a-b),pass:readingMasks.reduce((a,b)=>a|b,0),possibleFail,independent}
  }
  for(let i=0;i<9;i++){ck(rows[i].gs.slice().sort().join()===direct[i].gs.slice().sort().join()&&rows[i].b===direct[i].b&&rows[i].c===direct[i].c,"raw composition");o.worldChecks++}
  o.configurations++;
  for(let mask=1;mask<512;mask++){
   let x=evalRows(rows,mask),z=evalRows(direct,mask);
   ck(JSON.stringify(x)===JSON.stringify(z),"reading masks");
   o.cases++;
   o.independentFalsePossiblePass+=+(!!(x.independent&~x.pass));
   o.independentFalseNotAllFail+=+(!x.pass&&!!x.independent);
   o.uniformReadingExists+=+x.readingMasks.includes(mask);
   o.allReadingsPass+=+x.readingMasks.every(m=>m===mask);
   if(x.independent&~x.pass)o.witness??={guard:txt,bodyTrue:word(b,1),bodyFalse:word(c,1),mask,...x};
   if(x.pass===mask&&!x.readingMasks.includes(mask)){o.pointwiseNotUniform++;o.uniformWitness??={guard:txt,bodyTrue:word(b,1),bodyFalse:word(c,1),mask,...x}}
  }
 }
 for(let v of [o.configurations===192,o.cases===98112,o.worldChecks===1728,o.independentFalsePossiblePass>0,o.independentFalseNotAllFail>0,o.pointwiseNotUniform>0,o.allReadingsPass<=o.uniformReadingExists]){ck(v,"shared control "+o.controls);o.controls++}
 return o
}
const P=load(doc);
console.log(JSON.stringify({joint:experiment(P),shared:sharedGuard(P)},null,2));
```
## 实测
```json
{
  "joint": {
    "textPairs": 288,
    "cases": 45792,
    "worldChecks": 2592,
    "allPass": 10010,
    "allFail": 5134,
    "mixed": 15384,
    "unresolvedApplicability": 15264,
    "naiveSkipFalsePass": 4544,
    "naiveMarginalExtraUnknown": 862,
    "activeFailWitnesses": 26118,
    "allInactiveFirstPolicy": 7584,
    "controls": 16,
    "witness": {
      "text": "如果每周工时最多0秒且每周工时至少1秒或者每周工时少于2秒，就必须每周工时最多1秒",
      "mask": 84,
      "pass": 80,
      "fail": 4,
      "detail": {
        "inactive": 80,
        "activePass": 16,
        "activeFail": 4,
        "notApplicable": 0,
        "unresolved": 0
      }
    }
  },
  "shared": {
    "configurations": 192,
    "cases": 98112,
    "worldChecks": 1728,
    "independentFalsePossiblePass": 27392,
    "independentFalseNotAllFail": 1324,
    "pointwiseNotUniform": 1020,
    "uniformReadingExists": 12428,
    "allReadingsPass": 5560,
    "controls": 7,
    "witness": {
      "guard": "每周工时最多0秒且每周工时至少1秒或者每周工时少于2秒",
      "bodyTrue": "每周工时少于1秒",
      "bodyFalse": "每周工时最多1秒",
      "mask": 32,
      "readingMasks": [
        0,
        0
      ],
      "pass": 0,
      "possibleFail": 32,
      "independent": 32
    },
    "uniformWitness": {
      "guard": "每周工时少于0秒且每周工时至少1秒或者每周工时少于2秒",
      "bodyTrue": "每周工时少于1秒",
      "bodyFalse": "每周工时最多1秒",
      "mask": 12,
      "readingMasks": [
        4,
        8
      ],
      "pass": 12,
      "possibleFail": 12,
      "independent": 12
    }
  }
}
```
