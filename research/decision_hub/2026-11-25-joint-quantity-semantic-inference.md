# v3.2 自主认知专项第4轮（累计第63轮）：数量原子与联合语义推理

2026-11-25。RESEARCH_CANDIDATE。main bc4efb83819a198a981598c51ff33ceaf8a7e42c；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，13开放Draft PR。核对最近8提交、v3.2 blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前部及此前全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（目录标题与此前相关末段，非全文逐段审查）、decision_hub相关目录名、第2轮801d48d62a05659d3afedf1f56a555afa12c5236、第61轮17b6035732e43c56edc44cb5db07b8d49aadfd5b、第62轮ada3d84a46e4d9a411ebf762884d13a5c5e87686。区别于第2轮给定布尔树补全、第61轮固定原子与第62轮单个量比较：本轮改编并实际连接前两轮原型，完整有限中文字符串产生带原文跨度的类型原子及多树，再由可信夹具按变量身份推理。没有运行生产PR，非完整语义解析或既有数学方法重新验收。

## 方法及证明
第62轮组件解析改为游标接口，供第61轮区间记忆化多树解析消费；保留完整输入检查、匹配括号、严格比较、精确有理数、未知拒绝及25 token/128树上限。仅接受显式周期、指标、比较词、非负ASCII数值、有限倍率单位、且/或者/并非/全角括号。不允许点值候选作为约束原子。宿主按每次原子出现位置提供量身份，字段一致只是必要条件，真实主体、版本、时间窗、权限、证据等另行核验。无合格矩形域或无法绑定返回UNKNOWN；空区间CONFLICT；不将不同来源量自动合并。原型qualified布尔是人工可信夹具，非实际鉴权或证据认证。已知跨变量相关限制时，不可用本轮矩形精确结论。

对变量x的合格闭有理区间[l,h]，将落在其中的全部阈值、l、h排序去重；取每一端点及相邻端点中点。每个一元比较谓词在相邻端点的开区间内真值恒定；端点单列保证严格与非严格关系。对n个变量，在已确认矩形域内取各自代表点笛卡尔积，所有候选树均在这些组合上计算。任意原域点与至少一个代表点组合具有相同的原子真值向量，因此表达式所有可能真值完整保持。所有为真PASS、所有为假FAIL、两者皆有UNKNOWN。有限域为空CONFLICT；不得把不可行证据真空通过。这里PASS/FAIL仅针对逻辑表达式及给定域，不代表用户事实已成立或整体推荐合格。无概率；代表点数量不是现实概率或频率。连续变量区间适用；整数格、开放/无界域、变量间线性关系、非线性及概率依赖未实现。最坏组合上限约为各轴(2m_i+3)之积乘树数；设4096次树求值限额，超限LIMIT，不截断后给确定结论。资源上限为设计候选，未测真机时间或内存。

## 实际实验
4种比较符的三元组合×3×3阈值组合×4括号/否定模式=2304构造文本；每条3种绑定方式（同一变量、前两个共享、第一第三共享）×6个X闭区间，Y固定[0,2]，41472次判断。阈值0/1/2秒，部分0分钟同义。参照用独立半秒网格与直接布尔表达式（对于这些整数阈值网格覆盖每个区间真值类），不调用候选树；仍同一研究者设计，不是独立留出。对照共享完全相同谓词但忽略同一变量不同阈值之间的依赖，对比额外UNKNOWN及错误确定。另20项专项控制，含单位等价、跨主体身份夹具、严格边界、空域、权限、未知语法、2^53附近精度、微小有理数和三个资源上限。样例是ChatGPT研发辅助生成的项目原创合成开发数据，非真人/训练/独立留出。没有本轮新增外部数据或论文复现；数学证明为基本阈值分区，不主张原创定理。

## 实际复算代码
以下JS在连接器计算环境实际执行，无网络及第三方运行依赖；可复制至Node复跑。

```js
const probe = function(){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const gcd=(a,b)=>{a=a<0n?-a:a;while(b){[a,b]=[b,a%b]}return a||1n};
 const q=(a,b=1n)=>{if(b<=0n)throw Error("denominator");let g=gcd(a,b);return [a/g,b/g]};
 const cmp=(a,b)=>a[0]*b[1]<b[0]*a[1]?-1:a[0]*b[1]>b[0]*a[1]?1:0;
 const mid=(a,b)=>q(a[0]*b[1]+b[0]*a[1],2n*a[1]*b[1]);
 const key=a=>a.join("/");
 const relation=(d,op)=>op==="<"?d<0:op==="<="?d<=0:op===">"?d>0:d>=0;
 const periods={"每月":"month","每周":"week","每天":"day","每年":"year","总":"total","单次":"event"};
 const metrics={"收入":"money","工资":"money","预算":"money","费用":"money","工时":"duration","通勤":"duration"};
 const operators={"不少于":">=","不能少于":">=","至少":">=","不超过":"<=","不得超过":"<=","最多":"<=","必须少于":"<","少于":"<","低于":"<","多于":">","高于":">","超过":">","为":"="};
 const units={"人民币":["money","CNY",1],"CNY":["money","CNY",1],"韩元":["money","KRW",1],"KRW":["money","KRW",1],"美元":["money","USD",1],"USD":["money","USD",1],"元":["money","AMBIGUOUS",1],"小时":["duration","s",3600],"分钟":["duration","s",60],"秒":["duration","s",1]};
 const mag={"千":1000,"万":10000,"":1};
 function read(s,p,map){for(const k of Object.keys(map).sort((a,b)=>b.length-a.length))if(s.startsWith(k,p))return [map[k],p+k.length,k];return null}
 // Adapted from round 62 typed-atom-0.2: parse one atom at the current cursor.
 function atom(s,p){
  let start=p,period=read(s,p,periods);if(!period)return null;p=period[1];
  let metric=read(s,p,metrics);if(!metric)return null;p=metric[1];
  let op=read(s,p,operators);if(!op||op[0]==="=")return null;p=op[1];
  let n=/^(?:0|[1-9][0-9]{0,17})(?:\.[0-9]{1,6})?/.exec(s.slice(p));if(!n)return null;p+=n[0].length;
  let scale=Object.hasOwn(mag,s[p])?s[p]:"";if(scale)p++;
  let u=read(s,p,units);if(!u||u[0][0]!==metric[0]||u[0][1]==="AMBIGUOUS")return null;p=u[1];
  let [a,b=""]=n[0].split(".");
  return {metric:metric[2],period:period[0],unit:u[0][1],op:op[0],value:q(BigInt(a+b)*BigInt(mag[scale])*BigInt(u[0][2]),10n**BigInt(b.length)),start,end:p,source:s.slice(start,p)};
 }
 // Adapted from round 61: full input, balanced groups, all parses, hard limits.
 function parse(s){
  if(typeof s!=="string"||s.length>1000)return {status:"LIMIT"};
  const tokens=[],atoms=[],lex={"并非":"!","且":"&","或者":"|","（":"(","）":")"};
  for(let p=0;p<s.length;){let l=read(s,p,lex);if(l){tokens.push({k:l[0]});p=l[1]}else{let a=atom(s,p);if(!a)return {status:"UNKNOWN_TOKEN",offset:p};tokens.push({k:"a",i:atoms.length});atoms.push(a);p=a.end}if(tokens.length>25)return {status:"LIMIT"}}
  const memo=new Map(),t=tokens;
  function grouped(l,r){if(r-l<3||t[l].k!=="("||t[r-1].k!==")")return false;let d=0;for(let i=l;i<r;i++){if(t[i].k==="(")d++;if(t[i].k===")")d--;if(d<=0&&i!==r-1)return false}return d===0}
  function span(l,r){let k=l+":"+r;if(memo.has(k))return memo.get(k);let out=[];const add=x=>{out.push(x);if(out.length>128)throw Error("LIMIT")};
   if(r-l===1&&t[l].k==="a")add(["a",t[l].i]);
   if(grouped(l,r))for(const x of span(l+1,r-1))add(x);
   if(r-l>=2&&t[l].k==="!"&&((r-l===2&&t[l+1].k==="a")||grouped(l+1,r)))for(const x of span(l+1,r))add(["!",x]);
   for(let i=l+1;i<r-1;i++)if(t[i].k==="&"||t[i].k==="|")for(const a of span(l,i))for(const b of span(i+1,r))add([t[i].k,a,b]);
   memo.set(k,out);return out;
  }
  try{let trees=t.length?span(0,t.length):[];return trees.length?{status:"CANDIDATE",atoms,trees}:{status:"SYNTAX"}}catch(e){if(e.message==="LIMIT")return {status:"LIMIT"};throw e}
 }
 function evalTree(t,truth){return t[0]==="a"?truth[t[1]]:t[0]==="!"?!evalTree(t[1],truth):t[0]==="&"?evalTree(t[1],truth)&&evalTree(t[2],truth):evalTree(t[1],truth)||evalTree(t[2],truth)}
 function verdict(vals){return !vals.length?"CONFLICT":vals.every(Boolean)?"PASS":vals.every(v=>!v)?"FAIL":"UNKNOWN"}
 function cells(lo,hi,thresholds){
  const cuts=[...new Map([lo,hi,...thresholds.filter(x=>cmp(x,lo)>=0&&cmp(x,hi)<=0)].map(x=>[key(x),x])).values()].sort(cmp);
  return cuts.flatMap((x,i)=>i+1<cuts.length?[x,mid(x,cuts[i+1])]:[x]);
 }
 // Host provides authenticated occurrence-level bindings and qualified rectangular domain.
 // Here these are synthetic fixtures; labels alone never authorize binding.
 function solve(p,bindings,domains,qualified,cap=4096){
  if(p.status!=="CANDIDATE"||!qualified||!Array.isArray(bindings)||bindings.length!==p.atoms.length)return {status:"UNKNOWN"};
  const ids=[...new Set(bindings)];
  if(ids.some(id=>typeof id!=="string"||!Object.hasOwn(domains,id)))return {status:"UNKNOWN"};
  for(let i=0;i<p.atoms.length;i++){let a=p.atoms[i],d=domains[bindings[i]];if(a.metric!==d.metric||a.period!==d.period||a.unit!==d.unit)return {status:"UNKNOWN"}}
  if(ids.some(id=>cmp(domains[id].lo,domains[id].hi)>0))return {status:"CONFLICT"};
  const axes=ids.map(id=>cells(domains[id].lo,domains[id].hi,p.atoms.filter((a,i)=>bindings[i]===id).map(a=>a.value)));
  const worlds=axes.reduce((n,a)=>n*a.length,1);
  if(worlds*p.trees.length>cap)return {status:"LIMIT"};
  const vals=[];function walk(i,w){if(i===ids.length){let truth=p.atoms.map((a,j)=>relation(cmp(w[ids.indexOf(bindings[j])],a.value),a.op));for(const t of p.trees)vals.push(evalTree(t,truth));return}for(const x of axes[i])walk(i+1,[...w,x])}walk(0,[]);
  return {status:verdict(vals),worlds,trees:p.trees.length};
 }
 // Conservative Boolean baseline shares exact identical bound predicates but drops cross-threshold dependence.
 function baseline(p,bindings,domains){
  const keys=[],sets=[];let indices=p.atoms.map((a,i)=>{const k=JSON.stringify([bindings[i],a.op,key(a.value)]);let j=keys.indexOf(k);if(j>=0)return j;j=keys.length;keys.push(k);let d=domains[bindings[i]];sets.push([...new Set(cells(d.lo,d.hi,[a.value]).map(x=>relation(cmp(x,a.value),a.op)))]);return j});
  let vals=[];function walk(i,w){if(i===sets.length){for(const t of p.trees)vals.push(evalTree(t,indices.map(j=>w[j])));return}for(const x of sets[i])walk(i+1,[...w,x])}walk(0,[]);return verdict(vals);
 }
 const ops=[["少于","<"],["最多","<="],["超过",">"],["至少",">="]],bool=(op,a,b)=>op==="&"?a&&b:a||b,sym=o=>o==="&"?"且":"或者";
 const ds=[[0,0],[0,1],[0,2],[1,1],[1,2],[2,2]];
 let out={texts:0,checks:0,exact:0,pass:0,fail:0,unknown:0,baselineMatches:0,baselineExtraUnknown:0,baselineWrongCertain:0,worlds:0,maxWorlds:0,controls:0},witnesses={};
 // Thresholds 0/1/2 seconds; alternate equivalent decimal minute representation for 0 only.
 const atomText=(i,op,k)=>"每周工时"+op+(i===0&&k===0?"0分钟":k+"秒");
 for(const [a,ao] of ops)for(const [b,bo] of ops)for(const [c,co] of ops)for(const k of [0,1,2])for(const j of [0,1,2])for(const mode of ["bare","left","right","neg"]){
  let x=atomText(0,a,k),y=atomText(1,b,j),z=atomText(2,c,1);
  let text=mode==="left"?`（${x}且${y}）或者${z}`:mode==="right"?`${x}且（${y}或者${z}）`:mode==="neg"?`并非（${x}且${y}或者${z}）`:`${x}且${y}或者${z}`;
  let p=parse(text);ck(p.status==="CANDIDATE",text);out.texts++;
  for(const binding of [["X","X","X"],["X","X","Y"],["X","Y","X"]])for(const [l,h] of ds){
   const domains={X:{metric:"工时",period:"week",unit:"s",lo:q(BigInt(l)),hi:q(BigInt(h))},Y:{metric:"工时",period:"week",unit:"s",lo:q(0n),hi:q(2n)}};
   // Independent reference: integer half-second grid on 0..2 with integer thresholds.
   // This grid intersects every possible cell in this particular fixture.
   const v=[];for(let x2=2*l;x2<=2*h;x2++)for(let y2=0;y2<=4;y2++){
    const n=binding.map(id=>id==="X"?x2:y2),u=n.map((t,i)=>relation(Math.sign(t-2*[k,j,1][i]),[ao,bo,co][i]));
    let L=(u[0]&&u[1])||u[2],R=u[0]&&(u[1]||u[2]);for(let f of mode==="left"?[L]:mode==="right"?[R]:[L,R])v.push(mode==="neg"?!f:f)
   }
   const gold=verdict(v),got=solve(p,binding,domains,true),base=baseline(p,binding,domains);
   ck(got.status===gold,"oracle "+text);out.checks++;out.exact++;out[gold.toLowerCase()]++;out.worlds+=got.worlds;out.maxWorlds=Math.max(out.maxWorlds,got.worlds);
   if(base===gold)out.baselineMatches++;else if(base==="UNKNOWN"){out.baselineExtraUnknown++;if(!witnesses[gold])witnesses[gold]={text,binding,range:[l,h],baseline:base,candidate:gold}}else out.baselineWrongCertain++;
  }
 }
 const dom=(lo,hi,unit="s")=>({metric:"工时",period:"week",unit,lo,hi});
 const cases=[
 ["每周工时至少40小时且每周工时少于30小时",["X","X"],{X:dom(q(0n),q(200000n))},true,"FAIL"],
 ["每周工时至少40小时且每周工时少于30小时",["X","Y"],{X:dom(q(0n),q(200000n)),Y:dom(q(0n),q(200000n))},true,"UNKNOWN"],
 ["每周工时至少40小时或者每周工时少于40小时",["X","X"],{X:dom(q(0n),q(200000n))},true,"PASS"],
 ["每周工时少于0.1小时且每周工时至少6分钟",["X","X"],{X:dom(q(0n),q(1000n))},true,"FAIL"],
 ["每周工时最多0.1小时且每周工时至少6分钟",["X","X"],{X:dom(q(360n),q(360n))},true,"PASS"],
 ["每周工时最多0.1小时且每周工时至少6分钟",["X","X"],{X:dom(q(0n),q(1000n))},true,"UNKNOWN"],
 ["并非（每周工时至少1秒）且（每周工时最多1秒）",["X","X"],{X:dom(q(2n),q(2n))},true,"FAIL"],
 ["每周工时最多1秒",["X"],{X:dom(q(2n),q(1n))},true,"CONFLICT"],
 ["每周工时最多1秒",["X"],{X:dom(q(0n),q(1n))},false,"UNKNOWN"],
 ["每周工时最多1秒",["X"],{X:dom(q(0n),q(1n),"KRW")},true,"UNKNOWN"],
 ["每周工时最多1秒",[],{},true,"UNKNOWN"],
 ["每周工时最多1秒且每天工时最多1秒",["X","X"],{X:dom(q(0n),q(1n))},true,"UNKNOWN"],
 ["总预算最多3万元",["X"],{},true,"UNKNOWN"],
 ["每周工时最多1秒但是照顾家人",["X"],{},true,"UNKNOWN"],
 ["每周工时为1秒",["X"],{},true,"UNKNOWN"],
 ["每周工时超过9007199254740992秒",["X"],{X:dom(q(9007199254740993n),q(9007199254740993n))},true,"PASS"],
 ["每周工时少于0.000001秒",["X"],{X:dom(q(1n,2000000n),q(1n,2000000n))},true,"PASS"]
 ];
 for(const [s,b,d,ok,e] of cases){ck(solve(parse(s),b,d,ok).status===e,s);out.controls++}
 let p=parse("每周工时少于1秒且每周工时最多2秒");ck(solve(p,["X","X"],{X:dom(q(0n),q(3n))},true,1).status==="LIMIT","cap");out.controls++;
 ck(parse(Array(14).fill("每周工时少于1秒").join("且")).status==="LIMIT","tokens");out.controls++;
 ck(parse(Array(10).fill("每周工时少于1秒").join("且")).status==="LIMIT","trees");out.controls++;
 return {out,witnesses};
};
console.log(JSON.stringify(probe(),null,2));
```

```json
{
  "out": {
    "texts": 2304,
    "checks": 41472,
    "exact": 41472,
    "pass": 9232,
    "fail": 9590,
    "unknown": 22650,
    "baselineMatches": 41018,
    "baselineExtraUnknown": 454,
    "baselineWrongCertain": 0,
    "worlds": 301568,
    "maxWorlds": 25,
    "controls": 20
  },
  "witnesses": {
    "FAIL": {
      "text": "每周工时少于1秒且（每周工时少于0秒或者每周工时超过1秒）",
      "binding": [
        "X",
        "X",
        "X"
      ],
      "range": [
        0,
        2
      ],
      "baseline": "UNKNOWN",
      "candidate": "FAIL"
    },
    "PASS": {
      "text": "（每周工时少于2秒且每周工时少于2秒）或者每周工时超过1秒",
      "binding": [
        "X",
        "X",
        "X"
      ],
      "range": [
        0,
        2
      ],
      "baseline": "UNKNOWN",
      "candidate": "PASS"
    }
  }
}
```

## 接入及后续
将原子出现span与第58轮独立义务、可信宿主确认、数量身份和版本绑定。结合第60轮迁移接口，禁止旧来源直接成为当前量身份。精确同一变量的冲突/恒真可减少无谓追问，但需区分硬要求冲突、测量区间不确定和多解释歧义，未实现冲突最小核/自然语言解释及真实交互。下一轮建议研究跨轮指代和数量身份绑定，尤其不同主体、时间窗口和修订，不以同标签自动合并。模型轨可复用联合判定；产品轨负责极简交互与唯一交接；独立轨负责未见文本及真实平台验收。未修改生产、训练、CI、Codex任务、合并、部署、个人数据、第三方AI调用或新增费用。冻结协议不变。