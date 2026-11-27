# 自主认知：独立来源分组约束与数量语义消歧的有限鲁棒支持域
2026-11-27。RESEARCH_CANDIDATE / FINITE_SYNTHETIC_EXHAUSTIVE_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。

## 基线与去重
起点及写前main 59b42af04500c0f648deea911a8a7254f9af6cdf。实际核对25近期提交、10开放PR、v3.2及同步规程全文（同步规程输出范围8500字符内）、#63元数据：Draft未合并，head 734686980b19da9291bdd08b67d4e2519c011acf；当前唯一产品交接路径 research/coordination/DECISION_WORKBENCH_PRODUCT_PRIVACY_HANDOFF_2026-11-19.md，blob 5e74f4f0b37141d631740e844ad8bbbfed232e07，读取全文响应的首45行及末8500字符，其最新可见增量为11月22日，未逐行审阅全部。读取main树、最新数量联合词法一致性报告、原生开放数量与谓词报告 blob 80feb5e4264b555c6f7e5352178ccb5ba8117551、效果等价与账本报告18ae7920f9ca317da66d1d50ba7f0fc3d8951c26及相关语义证书1e17a6a47458c19e46f52151a59a0b6bf863a6f0。局部查重，未声称全库无重复。前序数量候选四链一致297个中257个错误，本轮未重新执行该真实语料实验，引用历史记录。新增原始来源组错误预算及复制引用对数学角色消歧的影响；不重复候选树生成、相关域澄清集合、账本写入和有限域决策一致性的既有结论。

## 合同及证明
人工给定数量0、1、2在三个不同对象/角色之间的一一分配，六个全排列为有限世界。三个角色同单位、同时间、同条件，数字只是合成夹具。各角色观察及总和记录是结构化谓词，来源根root和qualified由外部夹具指定，未实现真实来源鉴别、独立性识别或语言解析。总和3对全部排列不变，不能用来分配角色。若一个记录由候选自身计算而得，禁止把它作为额外观测去确认该候选；复制、转述及同源派生共享实际来源根。复杂多源派生依赖需要额外证据图建模，本轮不实现；无法确定其来源根时不得进入此筛选。假设最多e个不同来源组存在至少一条不符的记录，e由研究者预设（0、1），不是经验错误率、概率、可由一致性自动学习的参数。来源组不假定统计独立。若候选h与某来源任一条合格谓词不符，则该来源进入B(h)；保留H_e={h∈H:|B(h)|≤e}。若真解释h*∈H且|B(h*)|≤e，则由定义必在H_e。相同来源同一谓词重复不会改变B。若某只读硬门f在非空H_e上恒定，则在前述假设内其值等于f(h*)，即使解释不唯一。空域为冲突；覆盖未知、来源资格未知均不发放任何条件性证书，保持UNKNOWN。即使单候选也不能推出真实语义，更不能写入账本、发放权威或执行。全部authority NONE。真正不可违反的硬门不进入可污染来源容忍；本实验容忍的是解释所依据的可疑观察，不能放宽用户已确认的硬底线。每次有限筛选朴素时间O(|H|*R)、额外空间O(|H|+R)，R记录数；未测设备资源或开放域复杂度。

## 设计及结果
63个非空候选域×27个三角色观察组合×2种来源拓扑×6个指定真解释=20412配置。两个拓扑分别为前两角色不同根/同根；第三角色与总和另有根。给第一条观察追加8个完全相同引用，比较逐记录最少不符的简单基线、逐记录不符≤1、来源组不符≤1。所有域重复不变性、来源逐组枚举参照、严格零错误子域、总和不变性均实际核对；参照共享谓词及人工定义，不是独立科学复现。首次同代码两次执行输出相同，归档前再次执行并核对关键数值。全部计数为有限合成配置，非独立样本、现实频率或产品误判率。人为选定硬门第一角色值≤1，不能推断用户价值。满足真值在域且错误来源数≤1的3456配置中，真值保留3456，唯一解释1536，硬门恒定2320，错误硬门0。逐记录不符≤1排除真值1536；逐记录最少不符错误唯一1080，错误确定硬门784；追加重复引用使最少不符支持改变1248，其中792新增错误唯一。此两基线属于不同判定规则，不比较相同覆盖的真实效果。10044组真值不在域，其中4656仍有唯一候选，证明覆盖布尔不能来自筛选本身。6912组真值在域但违背错误预算，不计入安全声明。严格0错误的384个合格配置均唯一，因为夹具包含全部三角色真值，不能推广到不完整记录。六世界中57个多元素候选域的总和证据无法消歧。来源别名控制将同一错误观察错误拆成两个根，预算1时仅保留2个世界；正确同根则保留6个，说明真实来源身份是外部必要条件。未通过训练或参数拟合获得结果；没有使用真实或私人记录。研究者自行选择域、来源拓扑、重复数、预算、硬门及简单基线。下一责任：数据轨验证独立可追溯来源资格，模型轨研究多源派生及区间观测，独立验收轨保管未见语言案例；本报告不改变原生接口、版本范围、唯一交接、冻结证据等级。未执行原生入口、外部语料新实验、独立留出、真人、竞品、训练、生产集成、主动CI、合并或部署。零新增费用。

## 可执行复算
标准JS，无外部依赖。运行下列代码输出JSON。
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)};
 const W=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
 const keys=w=>w.join(","),port=w=>w[0]<=1?"PASS":"FAIL";
 function filter(domain,rows,e,closed=true){
  if(!closed)return {status:"UNKNOWN_COVERAGE",worlds:[],authority:"NONE"};
  if(rows.some(r=>!r.qualified||!r.root))return {status:"UNKNOWN_EVIDENCE",worlds:[],authority:"NONE"};
  const keep=domain.filter(w=>new Set(rows.filter(r=>r.field===3?w.reduce((a,b)=>a+b,0)!==r.value:w[r.field]!==r.value).map(r=>r.root)).size<=e);
  return {status:keep.length===0?"CONFLICT":keep.length===1?"CONDITIONAL_UNIQUE":"AMBIGUOUS",worlds:keep,authority:"NONE"};
 }
 const mism=(w,r)=>r.field===3?w.reduce((a,b)=>a+b,0)!==r.value:w[r.field]!==r.value;
 const score=(w,rows)=>rows.filter(r=>mism(w,r)).length;
 const best=(domain,rows)=>{let n=Math.min(...domain.map(w=>score(w,rows)));return domain.filter(w=>score(w,rows)===n)};
 const inv=ws=>ws.length&&new Set(ws.map(port)).size===1?port(ws[0]):"UNKNOWN";
 const stat={cases:0,eligible:0,truthMissing:0,assumptionViolated:0,robustUnique:0,robustPortKnown:0,robustWrong:0,robustFalsePort:0,rowExcludesTruth:0,naiveUniqueWrong:0,naiveFalsePort:0,duplicateChangesBest:0,duplicateCreatesWrongUnique:0,unsupportedUniqueWhenMissing:0,qualifiedStrictUnique:0,strictEligible:0,strictSumOnlyAmbiguous:0,aliasControls:0,unknownControls:0,witness:null};
 for(let m=1;m<64;m++){
  const domain=W.filter((_,i)=>m&(1<<i));
  const sum=[{field:3,value:3,root:"total",qualified:true}];
  ck(filter(domain,sum,0).worlds.length===domain.length,"permutation-invariant sum");
  if(domain.length>1)stat.strictSumOnlyAmbiguous++;
  for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++)for(let layout=0;layout<2;layout++){
   const raw=[{field:0,value:a,root:"A",qualified:true},{field:1,value:b,root:layout?"A":"B",qualified:true},{field:2,value:c,root:"C",qualified:true},...sum];
   const rows=[...raw,...Array.from({length:8},()=>({...raw[0]}))];
   const rr=filter(domain,rows,1),dedup=filter(domain,raw,1);
   ck(JSON.stringify(rr)===JSON.stringify(dedup),"duplicate invariance");
   const ref=domain.filter(w=>[...new Set(raw.map(r=>r.root))].reduce((n,root)=>n+Number(raw.some(r=>r.root===root&&mism(w,r))),0)<=1);
   ck(JSON.stringify(rr.worlds)===JSON.stringify(ref),"oracle");
   const naive=best(domain,rows),plain=best(domain,raw);
   for(const truth of W){
    stat.cases++;
    if(!domain.includes(truth)){stat.truthMissing++;if(rr.worlds.length===1)stat.unsupportedUniqueWhenMissing++;continue}
    const bad=new Set(raw.filter(r=>mism(truth,r)).map(r=>r.root)).size;
    if(bad===0){stat.strictEligible++;const strict=filter(domain,rows,0);ck(strict.worlds.includes(truth),"strict");if(strict.worlds.length===1)stat.qualifiedStrictUnique++}
    if(bad>1){stat.assumptionViolated++;continue}
    stat.eligible++;
    if(rr.worlds.length===1)stat.robustUnique++;
    if(inv(rr.worlds)!=="UNKNOWN")stat.robustPortKnown++;
    if(!rr.worlds.includes(truth))stat.robustWrong++;
    if(inv(rr.worlds)!=="UNKNOWN"&&inv(rr.worlds)!==port(truth))stat.robustFalsePort++;
    if(score(truth,rows)>1)stat.rowExcludesTruth++;
    if(naive.length===1&&naive[0]!==truth)stat.naiveUniqueWrong++;
    if(inv(naive)!=="UNKNOWN"&&inv(naive)!==port(truth))stat.naiveFalsePort++;
    if(JSON.stringify(naive)!==JSON.stringify(plain))stat.duplicateChangesBest++;
    if(naive.length===1&&naive[0]!==truth&&!(plain.length===1&&plain[0]!==truth)){
     stat.duplicateCreatesWrongUnique++;
     if(!stat.witness)stat.witness={truth:keys(truth),domain:domain.map(keys),rows:raw,naive:naive.map(keys),plain:plain.map(keys),robust:rr.worlds.map(keys)};
    }
   }
  }
 }
 const control=[{field:0,value:2,root:"X",qualified:true},{field:0,value:2,root:"Y",qualified:true}];
 ck(filter(W,control,1).worlds.length===2,"split aliases unsafe");
 ck(filter(W,control.map(r=>({...r,root:"X"})),1).worlds.length===6,"same source");
 stat.aliasControls=2;
 ck(filter(W,control,1,false).status==="UNKNOWN_COVERAGE","unknown coverage");
 ck(filter(W,[{...control[0],qualified:false}],1).status==="UNKNOWN_EVIDENCE","unknown source");
 ck(filter(W,control.map(r=>({...r,root:null})),1).status==="UNKNOWN_EVIDENCE","missing root");
 ck(filter([],[],1).status==="CONFLICT","closed empty");
 stat.unknownControls=4;
 ck(stat.cases===63*27*2*6&&stat.cases===stat.eligible+stat.truthMissing+stat.assumptionViolated,"partition");
 ck(stat.robustWrong===0&&stat.robustFalsePort===0&&stat.duplicateCreatesWrongUnique>0,"expected");
 return stat;
}
console.log(JSON.stringify(experiment(),null,2));
```

## 实测输出
```json
{
  "cases": 20412,
  "eligible": 3456,
  "truthMissing": 10044,
  "assumptionViolated": 6912,
  "robustUnique": 1536,
  "robustPortKnown": 2320,
  "robustWrong": 0,
  "robustFalsePort": 0,
  "rowExcludesTruth": 1536,
  "naiveUniqueWrong": 1080,
  "naiveFalsePort": 784,
  "duplicateChangesBest": 1248,
  "duplicateCreatesWrongUnique": 792,
  "unsupportedUniqueWhenMissing": 4656,
  "qualifiedStrictUnique": 384,
  "strictEligible": 384,
  "strictSumOnlyAmbiguous": 57,
  "aliasControls": 2,
  "unknownControls": 4,
  "witness": {
    "truth": "1,0,2",
    "domain": [
      "0,1,2",
      "1,0,2"
    ],
    "rows": [
      {
        "field": 0,
        "value": 0,
        "root": "A",
        "qualified": true
      },
      {
        "field": 1,
        "value": 0,
        "root": "B",
        "qualified": true
      },
      {
        "field": 2,
        "value": 2,
        "root": "C",
        "qualified": true
      },
      {
        "field": 3,
        "value": 3,
        "root": "total",
        "qualified": true
      }
    ],
    "naive": [
      "0,1,2"
    ],
    "plain": [
      "0,1,2",
      "1,0,2"
    ],
    "robust": [
      "0,1,2",
      "1,0,2"
    ]
  }
}
```
