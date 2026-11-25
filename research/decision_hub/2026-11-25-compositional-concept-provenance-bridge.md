# 自主认知专项累计第82轮候选：原文组合概念、来源凭据与开放域推理接口

2026-11-25。RESEARCH_CANDIDATE / FINITE_RAW_TEMPLATE_BRIDGE_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main d0cd24a3e7174647abcd0eaa89939215959735ad。核对最新20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R81、R80、R66、R73前20行。与R66通用知识支持、R73标注转换、R80排序、R81给定域联合一致性不同，本轮实际从有限原文模板生成组合概念、双路径来源及两个节点的候选关系，适配R81的有限关系语义，未直接运行其三节点源码。无新增外部文献或事实。

## 方法与证据边界
研究者构造六个概念类型、三个多义词头、六个修饰成分、三个全词直接别名、五个抽象来源位及12个短语。它们不是经词典或真实语言学证据认证的完整义项。五个来源位仅是夹具：基本词头、修饰成分、组合规则、直接别名、替代词头。组合必须消耗完整短语且满足类型相容，保留每个推导的原文UTF16位置、组成位置和来源掩码。一个概念允许多条证据路径，撤回来源后按原文重算；没有来源则不生成该义项。直接词面和组合路径不能当作独立科学证据或概率。输入仅支持甲提到「短语」，乙提到「短语」。这一固定模板，关系由可信夹具提供；不能识别自由白话、真实主体、关系语用、否定或实体身份。这里same/different只针对概念类型，不推断真实实体相同。全词覆盖不等于开放世界穷尽；常态outside=true。仅在人工有限覆盖证书、全部五来源有效、短语列入人工封闭目录且关系获资格时允许在该小域给出FINITE_CANDIDATES或CONFLICT。否则保留UNKNOWN，若关系无资格不输出关系候选；所有输出authority NONE。真实知识资格、许可、版本、时效、覆盖证书、实体映射及宿主权限仍未实现。人工coverage布尔非真实鉴权。任何唯一候选均不能自动执行更正或科学计算。

## 复算与对照
12短语×32来源组合=384；每次逐位撤回核验候选集合单调缩减与替代支持。12^2×32来源×2关系×2覆盖请求×2资格=36864模板情景；独立显式短语表和六义项两两枚举作为参照，同一研究者制定，非独立验收。错误强行闭域对照：在有资格关系但无完整覆盖时，若将部分候选直接判冲突或唯一，会产生未经授权的结论；另外只在两个全域已知、关系合格且请求封闭的子集中，计算部分来源相对完整夹具的确切错误冲突和错误唯一。所有数字是合成组合计数，非真实语言错误率、用户效用或实际产品表现。所有材料为ChatGPT研发辅助原创合成开发样例，非真人、训练或独立留出。未运行原生平台、真实设备、外部语料或统计学习。没有训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。

## 可执行程序
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),sort=a=>[...a].sort((x,y)=>x-y);
 // 6 concept types: money/time budget, loan/deposit rate, credit/spending limit.
 // This is a stipulated miniature ontology, not a claim about exhaustive Chinese meanings.
 const heads=[["预算",0,1],["利率",2,3],["额度",4,5]],mods=[["资金",0],["时间",1],["贷款",2],["存款",3],["信用",4],["支出",5]];
 const direct=[["时间预算",1],["贷款利率",2],["信用额度",4]];
 const phrases=["预算","资金预算","时间预算","利率","贷款利率","存款利率","额度","信用额度","支出额度","利息","决策预算","预算时间"];
 // Sources 1=head base meanings; 2=modifier; 4=composition rule;
 // 8=direct aliases; 16=alternative head meanings. Stipulated, no external authority.
 function candidates(s,mask,offset=0){
  let records=[];
  function add(c,parts,needs){if((mask&needs)!==needs)return;records.push({concept:c,span:[offset,offset+s.length],raw:s,parts:parts.map(([a,b])=>[a+offset,b+offset]),needs,authority:"NONE"})}
  for(const [h,a,b] of heads){
   if(s===h){add(a,[[0,s.length]],1);add(b,[[0,s.length]],16)}
   for(const [m,c] of mods)if(s===m+h&&(c===a||c===b))add(c,[[0,m.length],[m.length,s.length]],2|4|(c===a?1:16));
  }
  for(const [p,c] of direct)if(s===p)add(c,[[0,s.length]],8);
  return {raw:s,records,domain:sort(new Set(records.map(x=>x.concept))),outside:true,authority:"NONE"};
 }
 // Independent expected mapping, written explicitly for each full phrase.
 const expected={
  "预算":[[0,1],[1,16]],"资金预算":[[0,7]],"时间预算":[[1,22],[1,8]],
  "利率":[[2,1],[3,16]],"贷款利率":[[2,7],[2,8]],"存款利率":[[3,22]],
  "额度":[[4,1],[5,16]],"信用额度":[[4,7],[4,8]],"支出额度":[[5,22]],
  "利息":[],"决策预算":[],"预算时间":[]
 };
 const oracle=(s,mask)=>sort(new Set(expected[s].filter(([c,n])=>(mask&n)===n).map(([c])=>c)));
 function parse(text,mask){
  let m=/^甲提到「([^」]+)」，乙提到「([^」]+)」。$/u.exec(text);
  if(!m)return null;
  let first=4,second=first+m[1].length+7;
  // Locate exact capture start from the known delimiters rather than guessing from repeated text.
  second=text.indexOf("乙提到「",first+m[1].length)+4;
  let a=candidates(m[1],mask,first),b=candidates(m[2],mask,second);
  for(const x of [...a.records,...b.records])ck(text.slice(...x.span)===x.raw,"source span");
  return [a,b];
 }
 // Adapt R81's finite relation semantics to two nodes. This comparison is concept-type
 // equality, not identity of real objects. Relationship qualification is external.
 const relation=(a,b,t)=>t==="same"?a===b:a!==b;
 function pairs(a,b,t){return a.flatMap(x=>b.filter(y=>relation(x,y,t)).map(y=>[x,y]))}
 function resolve(text,mask,t,seal,qualified){
  let x=parse(text,mask);if(!x)return {status:"UNKNOWN",authority:"NONE",pairs:[]};
  let p=pairs(x[0].domain,x[1].domain,t);
  // An artificial coverage certificate is available only for declared full-catalog phrases.
  let complete=seal&&mask===31&&x.every(z=>Object.hasOwn(expected,z.raw)&&expected[z.raw].length>0)&&qualified;
  return {status:complete?(p.length?"FINITE_CANDIDATES":"CONFLICT"):"UNKNOWN",authority:"NONE",pairs:qualified?p:[],outside:!complete,complete,domains:x.map(z=>z.domain)};
 }
 let r={phraseMaskCases:0,exactDomains:0,receiptChecks:0,emptyDomains:0,alternateProofCases:0,withdrawals:0,retainedAfterWithdrawal:0,lostConcepts:0,graphCases:0,qualifiedClosed:0,closedConflict:0,closedUnique:0,unknown:0,forcedConflictWithoutCoverage:0,forcedUniqueWithoutCoverage:0,partialFalseConflictAgainstFullFixture:0,partialFalseUniqueAgainstFullFixture:0,controls:0};
 for(let s of phrases)for(let mask=0;mask<32;mask++){
  let c=candidates(s,mask);r.phraseMaskCases++;ck(eq(c.domain,oracle(s,mask)),"domain");r.exactDomains++;
  r.emptyDomains+=+(!c.domain.length);r.alternateProofCases+=+(c.records.length>c.domain.length);
  for(let x of c.records){ck((mask&x.needs)===x.needs&&s.slice(...x.span)===s&&x.authority==="NONE","receipt");r.receiptChecks++}
  for(let b=1;b<=16;b*=2)if(mask&b){let n=candidates(s,mask^b);r.withdrawals++;ck(eq(n.domain,oracle(s,mask^b))&&n.domain.every(v=>c.domain.includes(v)),"withdrawal");r.lostConcepts+=c.domain.filter(v=>!n.domain.includes(v)).length;r.retainedAfterWithdrawal+=+(c.records.some(x=>x.needs&b)&&n.domain.some(v=>c.records.some(x=>x.concept===v&&(x.needs&b))));}
 }
 for(let a of phrases)for(let b of phrases)for(let mask=0;mask<32;mask++)for(let t of ["same","different"])for(let seal of [false,true])for(let q of [false,true]){
  let text="甲提到「"+a+"」，乙提到「"+b+"」。",z=resolve(text,mask,t,seal,q),ad=oracle(a,mask),bd=oracle(b,mask);
  // Separate explicit pair enumeration with direct equality truth table.
  let o=[];for(let i=0;i<6;i++)for(let j=0;j<6;j++)if(ad.includes(i)&&bd.includes(j)&&((i===j)===(t==="same")))o.push([i,j]);
  ck(eq(z.pairs,q?o:[])&&eq(z.domains,[ad,bd]),"joint oracle");
  r.graphCases++;
  let complete=seal&&q&&mask===31&&expected[a].length>0&&expected[b].length>0;
  ck(z.complete===complete&&z.authority==="NONE"&&z.outside===!complete,"gate");
  if(complete){r.qualifiedClosed++;r.closedConflict+=+(!o.length);r.closedUnique+=+(o.length===1);ck(z.status===(o.length?"FINITE_CANDIDATES":"CONFLICT"),"closed")}
  else{r.unknown++;ck(z.status==="UNKNOWN","open");if(q){r.forcedConflictWithoutCoverage+=+(!o.length);r.forcedUniqueWithoutCoverage+=+(o.length===1)}}
  // Compare only when relation is qualified, caller asks for seal and both full fixture domains exist.
  if(q&&seal&&mask!==31&&expected[a].length&&expected[b].length){let full=pairs(oracle(a,31),oracle(b,31),t);r.partialFalseConflictAgainstFullFixture+=+(!o.length&&full.length>0);r.partialFalseUniqueAgainstFullFixture+=+(o.length===1&&full.length>1)}
 }
 for(const test of [()=>r.phraseMaskCases===384,()=>r.graphCases===36864,()=>r.exactDomains===384,()=>r.qualifiedClosed+r.unknown===r.graphCases,()=>eq(candidates("时间预算",31).domain,[1]),()=>candidates("时间预算",31).records.length===2,()=>eq(candidates("时间预算",8).domain,[1]),()=>eq(candidates("时间预算",22).domain,[1]),()=>candidates("决策预算",31).domain.length===0,()=>candidates("预算时间",31).domain.length===0,()=>resolve("甲提到「预算」，乙提到「时间预算」。",31,"same",true,true).pairs.length===1,()=>resolve("甲提到「预算」，乙提到「时间预算」。",31,"same",false,true).status==="UNKNOWN",()=>resolve("甲提到「预算」，乙提到「利率」。",31,"same",true,true).status==="CONFLICT",()=>resolve("甲提到「预算」，乙提到「利率」。",31,"same",false,true).status==="UNKNOWN",()=>resolve("甲提到「预算」，乙提到「预算」。",31,"same",true,false).pairs.length===0,()=>resolve("其他原文",31,"same",true,true).status==="UNKNOWN",()=>parse("甲提到「预算」，乙提到「预算」。",31)[1].records[0].span[0]===12]){ck(test(),"control");r.controls++}
 return r;
}
```

## 实际结果
```json
{
  "phraseMaskCases": 384,
  "exactDomains": 384,
  "receiptChecks": 168,
  "emptyDomains": 246,
  "alternateProofCases": 6,
  "withdrawals": 960,
  "retainedAfterWithdrawal": 24,
  "lostConcepts": 192,
  "graphCases": 36864,
  "qualifiedClosed": 162,
  "closedConflict": 66,
  "closedUnique": 60,
  "unknown": 36702,
  "forcedConflictWithoutCoverage": 16658,
  "forcedUniqueWithoutCoverage": 1288,
  "partialFalseConflictAgainstFullFixture": 2218,
  "partialFalseUniqueAgainstFullFixture": 276,
  "controls": 17
}
```

## 后续责任
候选桥需连接真实合法词义资源、可追溯词义证据和自主可学习的组合语义识别；不继续无界增加规则或词典，人工封闭证书不能推广为开放语言覆盖。数据轨负责资源资格与隔离，独立轨负责未见样本，产品轨维护唯一交接；手动研究继续解决原文到自主概念/关系的覆盖与学习接口。保留R50完整版本范围，训练和工程版本另行授权。
