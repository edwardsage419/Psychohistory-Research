# v3.2 自主认知专项第3轮（累计第62轮）：类型化数量原子与精确比较

2026-11-25。RESEARCH_CANDIDATE。固定main e22acd18167c17df765996feea082ecc83703aaf；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，13开放Draft PR。核对最近8提交、v3.2 blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（本轮前部及此前全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关末段，非全文逐段审查）、decision_hub目录相关名称、第55轮d7eedbca02da7f66f06911fffedc8f8b82be3f90、第56轮2c7810d1cad4986b9ecabdf727adab5600ed6fca、第54轮412a98c4bd335864a32f27aa796fc8a42414e7f4、第61轮17b6035732e43c56edc44cb5db07b8d49aadfd5b。区别：55/56轮复现原生误标，54轮假定已经合格事实并研究派生量，61轮固定原子逻辑解析；本轮实际实现独立可组合的量词法与类型核验、精确标量比较。没有再次运行原生PR。

## 来源及设计
NIST SP811 Chapter 5 https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-5-units-outside-si （公开检索摘录：minute=60s、hour=3600s）；ISO 4217 https://www.iso.org/iso-4217-currency-codes.html （公开检索摘要，代码标识与维护机构；未读取完整代码表或标准全文）。不声称符合完整SI/ISO标准。三币种是本轮人工限定的示范词典，不含实时汇率，不下载或重分发原始外部数据。
有限语法 Period Metric Operator Decimal Magnitude? Unit，最长词组件匹配、完整输入消耗。Period显式月/周/日/年/总/单次；Metric六词；Operator十二种比较词及为；Magnitude千/万；三币种、三种时长单位及含糊元。数字为非负ASCII十进制，整数至18位、小数至6位；拒绝不支持表达、类型错配和歧义。保存原文、UTF16原文跨度、比较符、单位、周期和算法版本。用BigInt有理数a/b精确表示，换算秒后交叉乘法比较；不做日月年转换或跨币种换算。真实税前税后、单程往返、特定年月/总量范围、主体、来源、情景、预算与费用等同义映射仍须独立验证；同周期标签不证明真实时间窗相同。原型compare中的trusted是由研究者提供的综合资格夹具，假定上述身份与义务已合格，不是实际鉴权。为只表示点值候选，不能证明观察事实。初版以另一约束文本作为合成标量夹具，最终版改为独立点值候选，拒绝把上下限当点值；无权限通过不得比较。与前轮解析树的接口是将各类型化候选与原文span作为atom，再用经确认的同一量标识共享世界；本轮未执行组合树连接，不得将同指标不同阈值当独立随机原子。相同值不同来源不自动等同。BIGINT输出将来用十进制字符串或版本化有理数字段序列化，未完成生产schema。

## 实验与边界
四组指标共15个单位词，6数字、3倍率、8比较词，2160个构造约束文本；每条与同组测量3周期、各单位及4点组合，共108864次比较（重复值可能重复，非独立样本）。参照由整数千分位和单独夹具映射实现，安全整数范围内；额外测试2^53附近精度。对照是故意忽略单位周期和尺度的裸数比较，非原生PR、普通AI或专业工具。单独统计不相容时不当确定与已相容时反向错误。初版主计数与终版一致但初版角色未分离；本报告只以终版为准。角色与权限控制共5项，非法/未知控制15项，专项精度与语义边界8项。测试为ChatGPT研发辅助生成的项目原创合成开发样例，非真人、训练或独立留出；没有训练、第三方权重、外部推理、真实设备资源测试或实际建议效果。每个语法维度的完整覆盖、自由文本、中文数字、标点、多复合单位、区间、条件句、负数和非显式周期不支持；不可用这些计数推断开放语言准确率。原型未覆盖所有词典交叉组合。总预算/工资等概念的具体聚合含义、合法性与现实量可比性仍待核对。

## 可复算代码
以下JS实际执行于连接器计算环境；Node无需依赖或网络即可重放。两个路径同一研究者设计，非独立验收。

```js
const probe = function(){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const periods={"每月":"month","每周":"week","每天":"day","每年":"year","总":"total","单次":"event"};
 const metrics={"收入":"money","工资":"money","预算":"money","费用":"money","工时":"duration","通勤":"duration"};
 const comparisons={"不少于":">=","不能少于":">=","至少":">=","不超过":"<=","不得超过":"<=","最多":"<=","必须少于":"<","少于":"<","低于":"<","多于":">","高于":">","超过":">"};
 const units={"人民币":["money","CNY",1],"CNY":["money","CNY",1],"韩元":["money","KRW",1],"KRW":["money","KRW",1],"美元":["money","USD",1],"USD":["money","USD",1],"元":["money","AMBIGUOUS",1],"小时":["duration","s",3600],"分钟":["duration","s",60],"秒":["duration","s",1]};
 const mag={"千":1000,"万":10000,"":1};
 function readMap(s,p,map){for(const k of Object.keys(map).sort((a,b)=>b.length-a.length))if(s.startsWith(k,p))return [k,map[k],p+k.length];return null}
 function decimal(s){const [a,b=""]=s.split(".");return [BigInt(a+b),10n**BigInt(b.length)]}
 function parse(s){
  if(typeof s!=="string"||s.length>200)return {status:"LIMIT"};
  let p=0,period=readMap(s,p,periods);if(!period)return {status:"UNKNOWN_PERIOD",offset:p};p=period[2];
  let metric=readMap(s,p,metrics);if(!metric)return {status:"UNKNOWN_METRIC",offset:p};p=metric[2];
  let op=readMap(s,p,{...comparisons,"为":"="});if(!op)return {status:"UNKNOWN_OPERATOR",offset:p};p=op[2];
  let n=/^(?:0|[1-9][0-9]{0,17})(?:\.[0-9]{1,6})?/.exec(s.slice(p));if(!n)return {status:"UNKNOWN_NUMBER",offset:p};const start=p;p+=n[0].length;
  let scale=Object.hasOwn(mag,s[p])?s[p]:"";if(scale)p++;
  let u=readMap(s,p,units);if(!u)return {status:"UNKNOWN_UNIT",offset:p};p=u[2];
  if(p!==s.length)return {status:"UNKNOWN_SUFFIX",offset:p};
  if(u[1][0]!==metric[1])return {status:"TYPE_MISMATCH",offset:start};
  if(u[1][1]==="AMBIGUOUS")return {status:"AMBIGUOUS_CURRENCY",offset:start};
  let [a,b]=decimal(n[0]);a*=BigInt(mag[scale])*BigInt(u[1][2]);
  return {status:"CANDIDATE",role:op[1]==="="?"POINT_PROPOSAL":"BOUND_PROPOSAL",metric:metric[0],period:period[1],unit:u[1][1],op:op[1],a,b,source:s,span:[0,p],quantitySpan:[start,p],version:"typed-atom-0.2"};
 }
 // trusted is a synthetic host fixture, NOT supplied by the parser or user text.
 function compare(c,m,trusted){
  if(!trusted||c.status!=="CANDIDATE"||m.status!=="CANDIDATE"||c.role!=="BOUND_PROPOSAL"||m.role!=="POINT_PROPOSAL"||c.metric!==m.metric||c.period!==m.period||c.unit!==m.unit)return "UNKNOWN";
  let d=m.a*c.b-c.a*m.b;
  return (c.op==="<"?d<0n:c.op==="<="?d<=0n:c.op===">"?d>0n:d>=0n)?"PASS":"FAIL";
 }
 const groups=[
  {p:"每月",m:"收入",us:[["人民币",1],["CNY",1],["韩元",1],["KRW",1],["美元",1],["USD",1]],ps:["每月","每年","每天"]},
  {p:"总",m:"预算",us:[["人民币",1],["韩元",1],["美元",1]],ps:["总","每月","单次"]},
  {p:"每周",m:"工时",us:[["小时",3600],["分钟",60],["秒",1]],ps:["每周","每天","每月"]},
  {p:"单次",m:"通勤",us:[["小时",3600],["分钟",60],["秒",1]],ps:["单次","每天","每周"]}
 ];
 const codes={人民币:"CNY",CNY:"CNY",韩元:"KRW",KRW:"KRW",美元:"USD",USD:"USD",小时:"s",分钟:"s",秒:"s"};
 const nums=[["0",0],["0.1",100],["1.5",1500],["3",3000],["3.125",3125],["900",900000]];
 const opCases=[["不能少于","ge"],["至少","ge"],["不得超过","le"],["最多","le"],["必须少于","lt"],["少于","lt"],["超过","gt"],["高于","gt"]];
 const truth=(op,d)=>op==="ge"?d>=0:op==="le"?d<=0:op==="lt"?d<0:d>0;
 let out={atoms:0,checks:0,matches:0,pass:0,fail:0,unknown:0,naiveForcedPass:0,naiveForcedFail:0,naiveWrongPass:0,naiveWrongFail:0,naiveMatches:0,controls:0,exactPrecision:0};let witnesses={};
 for(const g of groups)for(const [u,uf] of g.us)for(const [n,ni] of nums)for(const [k,kf] of [["",1],["千",1000],["万",10000]])for(const [op,rel] of opCases){
  const t=g.p+g.m+op+n+k+u,c=parse(t);ck(c.status==="CANDIDATE",t);ck(c.a*1000n===BigInt(ni*kf*uf)*c.b,"scale");ck(c.source.slice(...c.span)===t,"span");out.atoms++;
  for(const p of g.ps)for(const [v,vf] of g.us)for(const [q,qi] of [nums[1],nums[2],nums[3], [n,ni]]){
   let measurement=parse(p+g.m+"为"+q+k+v);let expected=(p!==g.p||codes[u]!==codes[v])?"UNKNOWN":truth(rel,qi*kf*vf-ni*kf*uf)?"PASS":"FAIL";
   const got=compare(c,measurement,true);ck(got===expected,"compare "+t);out.checks++;out.matches++;out[got.toLowerCase()]++;
   let naive=truth(rel,qi-ni)?"PASS":"FAIL";if(naive===expected)out.naiveMatches++;
   else {let type=expected==="UNKNOWN"?(naive==="PASS"?"naiveForcedPass":"naiveForcedFail"):(naive==="PASS"?"naiveWrongPass":"naiveWrongFail");out[type]++;if(!witnesses[type])witnesses[type]={constraint:t,measurement:measurement.source,expected,naive};}
  }
 }
 for(const [s,e] of [["预算最多3万元","UNKNOWN_PERIOD"],["总预算最多3万元","AMBIGUOUS_CURRENCY"],["总预算最多3小时","TYPE_MISMATCH"],["每周工时最多3美元","TYPE_MISMATCH"],["每周工时最多40小时左右","UNKNOWN_SUFFIX"],["总预算最多3万日元","UNKNOWN_UNIT"],["总预算大约3000美元","UNKNOWN_OPERATOR"],["总预算最多-1美元","UNKNOWN_NUMBER"],["总预算最多1e3美元","UNKNOWN_UNIT"],["总预算最多01美元","UNKNOWN_UNIT"],["总预算最多1.1234567美元","UNKNOWN_UNIT"],["总预算最多3美元。","UNKNOWN_SUFFIX"],["总预算最多3","UNKNOWN_UNIT"],["总预算最多3万万人民币","UNKNOWN_UNIT"],["总预算最多"+"1".repeat(210)+"人民币","LIMIT"]]){ck(parse(s).status===e,s+" "+parse(s).status);out.controls++}
 const exact=[["总预算少于9007199254740993人民币","总预算为9007199254740992人民币","PASS"],["总预算超过9007199254740992人民币","总预算为9007199254740993人民币","PASS"],["单次通勤少于0.1小时","单次通勤为6分钟","FAIL"],["单次通勤不得超过0.1小时","单次通勤为6分钟","PASS"],["每月收入至少3万韩元","每月收入为30000KRW","PASS"],["每月收入至少3万韩元","每年收入为360000KRW","UNKNOWN"],["总预算最多100USD","总预算为100CNY","UNKNOWN"],["每周工时最多40小时","每周通勤为40小时","UNKNOWN"]];
 for(const [a,b,e] of exact){ck(compare(parse(a),parse(b),true)===e,a);out.exactPrecision++}
 const c=parse("每月收入至少3万韩元"),m=parse("每月收入为3万韩元");
 for(const [a,b,ok,e] of [[c,c,true,"UNKNOWN"],[m,m,true,"UNKNOWN"],[m,c,true,"UNKNOWN"],[c,m,false,"UNKNOWN"],[c,m,true,"PASS"]]){ck(compare(a,b,ok)===e,"role");out.controls++}
 return {out,witnesses};
};
console.log(JSON.stringify(probe(),null,2));
```

实际终版输出：
```json
{
  "out": {
    "atoms": 2160,
    "checks": 108864,
    "matches": 108864,
    "pass": 9504,
    "fail": 9504,
    "unknown": 89856,
    "naiveForcedPass": 44928,
    "naiveForcedFail": 44928,
    "naiveWrongPass": 1272,
    "naiveWrongFail": 1272,
    "naiveMatches": 16464,
    "controls": 20,
    "exactPrecision": 8
  },
  "witnesses": {
    "naiveForcedPass": {
      "constraint": "每月收入不能少于0人民币",
      "measurement": "每月收入为0.1韩元",
      "expected": "UNKNOWN",
      "naive": "PASS"
    },
    "naiveForcedFail": {
      "constraint": "每月收入不得超过0人民币",
      "measurement": "每月收入为0.1韩元",
      "expected": "UNKNOWN",
      "naive": "FAIL"
    },
    "naiveWrongPass": {
      "constraint": "每周工时不能少于0.1小时",
      "measurement": "每周工时为0.1分钟",
      "expected": "FAIL",
      "naive": "PASS"
    },
    "naiveWrongFail": {
      "constraint": "每周工时不得超过0.1小时",
      "measurement": "每周工时为1.5分钟",
      "expected": "PASS",
      "naive": "FAIL"
    }
  }
}
```

## 后续
优先研究同一可信数量变量上的多比较谓词如何共享可行域（例如x>=40与x<30不可同时成立），连接第61轮多解析树并避免独立布尔世界引入不可行状态；既有第2轮有限补全已指出需要联合域，本项待实际数值语义实现与端到端验证。产品轨维护独立未知与最小追问交接；独立验收轨另冻自由文本并验证真实环境；模型轨继续科学算法与复算。无重大开发授权，不发布零碎Codex任务。未改产品代码、训练、CI、合并、部署或使用个人数据；零新增费用，冻结协议不变。
