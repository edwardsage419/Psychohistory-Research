# v3.2 自主认知专项第5轮（累计第64轮）：跨轮指代与约束版本身份

2026-11-25。RESEARCH_CANDIDATE。main 449723c14b22a5d499f0ee3d546b22969b04d667；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，13开放Draft PR。核对最近8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前部及此前全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关章节标题及历史读取，非本轮全文审计）、decision_hub相关目录名、第2轮801d48d62a05659d3afedf1f56a555afa12c5236、第57轮e957deba40302b7f6d9ee61c34196d7ac28ce124、第58轮ad1f8ab7be83d28391ee62ce77a44d5f59804bef、第63轮296465980e23a1d8082f81a8181343668965328b。与第2轮给定语义修订、第57轮原生主体缺陷、第58轮单义务组合、第63轮人工变量绑定区分：本轮实际从有限多轮中文解析明确指代和修订候选，维护独立稳定身份及连续版本，再对条件作用域作单量计算。未运行原生PR或直接调用第63轮算法。

## 候选协议
有限语法：初始两轮为明确所有者+周期+生活费/房租+最多+非负整数+美元/韩元；后续为“把[引用]改为/另加上限/另加下限/增加到[金额]”，可附“如果选方案B，”。引用按显式主体、周期、类别、币种过滤当前有效基础记录；缺省字段只保留候选，预算在该夹具已定义为这两类支出的泛称，刚才那项保守保留所有活动候选，不按最近提及自动消歧。真实语用可能让其指代唯一，本轮可能过度澄清。新金额币种不能反向选择指代对象。朋友记录为夹具中的无修改权对象，真实代理权需独立授权。增加到的修订意图保持未知。未知表达、无目标、多目标、币种冲突、未获权限均保留原记录，当前相关完整判断UNKNOWN；本轮保守阻断全部当前判断，未实现独立局部端口。仅在宿主确认原文、当前修订、确切目标及权限后创建新事件。真实权限、身份及防篡改未实现，布尔和收据是人工夹具。条件B替换只覆盖基础上限，其他独立附加条件仍适用，A保持基础条件。普通基础修订保留独立附加条件；已有例外时新的基础或例外修订必须复核作用域，不猜测其延续/撤回。上述操作语义为研究选择，尚非最终产品规则。每个量使用稳定root，基础记录版本id与父版本分开；初版发现parent为空过滤会使第二次修订失去目标，最终版修正为kind和root，并加入连续修订与历史唯一性检查。未实现真实会话持久化、并发CAS、撤回、事件删除、跨会话授权、完整数量语法、任意主体/指代及条件逻辑。

## 实验
29个预定义引用场景（4类身份差异：类别、所有者、期间、币种）×2顺序×6操作×3数值×2币种=2088个三轮构造情节。参照由事先给定的目标索引、操作类别和独立公式生成，同一研究者设计，非独立留出。每个情节2个量×2个方案×5个测量值=20个旧或新已确认快照判断，41760次；未提交情节另核查当前出口UNKNOWN，已确认情节核查当前出口与快照一致。基线保留显式过滤、主体权限及币种检查，在歧义时取最近匹配记录，所有操作按无条件最新值覆盖。错误变更统计包含操作/作用域改变，即使某一测量值偶然相同；不是原生平台或普通AI实测。基线判断损害只统计336个有资格确认更新的情节，不在未决情节强造当前真值。基线是刻意简化的对照，不能推断真实产品错误率。夹具全部由ChatGPT研发辅助生成，项目原创合成开发样例，非真人、训练或独立留出。无新外部文献、真实设备性能、实际交互负担或科学验收；未复用个人数据。数值限定9位整数，非完整第62/63轮有理数推理；未来接稳定数量身份与原文义务时必须重新执行真实语义和数学门。

## 实际代码和结果
以下函数在连接器JS环境实际执行，可复制到Node复算，不需网络和第三方包。

```js
const probe = function(){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const owners={"我的":"self","朋友的":"friend"},periods={"每月":"month","每年":"year"},metrics={"生活费":"living","房租":"rent"},units={"美元":"USD","韩元":"KRW"};
 function read(s,p,map){for(const k of Object.keys(map))if(s.startsWith(k,p))return [map[k],p+k.length];return null}
 function describe(s,partial){
  if(partial&&s==="刚才那项")return {};
  let p=0,o=read(s,p,owners);if(o)p=o[1];let t=read(s,p,periods);if(t)p=t[1];let m=read(s,p,metrics);if(m)p=m[1];let u=read(s,p,units);if(u)p=u[1];if(partial&&!m&&s.slice(p)==="预算")p+=2;
  if(p!==s.length||(!partial&&(!o||!t||!m))||(partial&&!o&&!t&&!m&&!u&&s!=="预算"))return null;
  return {...(o?{owner:o[0]}:{}),...(t?{period:t[0]}:{}),...(m?{metric:m[0]}:{}),...(u?{unit:u[0]}:{})};
 }
 function amount(s){let m=/^(0|[1-9][0-9]{0,8})(美元|韩元)$/.exec(s);return m?{value:Number(m[1]),unit:units[m[2]]}:null}
 function initial(text,id){let p=text.indexOf("最多");if(p<0)return null;let ref=describe(text.slice(0,p),false),a=amount(text.slice(p+2));if(!ref||!a||(ref.unit&&ref.unit!==a.unit))return null;return {id:"base:"+id,root:id,...ref,...a,source:text,span:[0,text.length],revision:1,active:true,op:"<=",kind:"base",branch:null,parent:null}}
 function parse(text){
  let branch=null,s=text,prefix="如果选方案B，";if(s.startsWith(prefix)){branch="B";s=s.slice(prefix.length)}
  if(s.length>200||!s.startsWith("把"))return null;
  for(const [word,op] of [["改为","replace"],["另加上限","addMax"],["另加下限","addMin"],["增加到","ambiguous"]]){let p=s.indexOf(word,1);if(p<0)continue;let ref=describe(s.slice(1,p),true),a=amount(s.slice(p+word.length));if(!ref||!a)return null;let offset=branch?prefix.length:0;return {op,branch,ref,...a,source:text,span:[offset+1,offset+p]}}
  return null;
 }
 function propose(records,text,revision){
  let r=parse(text);if(!r)return {status:"UNKNOWN_SYNTAX"};
  if(r.op==="ambiguous")return {status:"UNKNOWN_OPERATION",r};
  let c=records.filter(x=>x.active&&x.kind==="base"&&Object.entries(r.ref).every(([k,v])=>x[k]===v));
  if(c.length!==1)return {status:c.length?"AMBIGUOUS":"UNRESOLVED",r,ids:c.map(x=>x.root)};
  let t=c[0];
  if(t.owner!=="self")return {status:"AUTHORITY_REQUIRED",r,ids:[t.root]};
  if(t.unit!==r.unit)return {status:"CURRENCY_CONFLICT",r,ids:[t.root]};
  if(r.branch&&r.op!=="replace")return {status:"UNSUPPORTED_BRANCH_OPERATION",r,ids:[t.root]};
  if(r.op==="replace"&&records.some(x=>x.active&&x.root===t.root&&x.kind==="exception"))return {status:"EXCEPTION_SCOPE_REVIEW",r,ids:[t.root]};
  return {status:"PENDING",r,ids:[t.root],target:t.id,revision,priorRevision:t.revision};
 }
 function commit(records,p,receipt,revision){
  if(p.status!=="PENDING"||!receipt||!receipt.authorized||receipt.revision!==revision||p.revision!==revision||receipt.target!==p.target||receipt.source!==p.r.source)return null;
  let t=records.find(x=>x.id===receipt.target&&x.active&&x.revision===p.priorRevision&&x.owner==="self"&&x.kind==="base");
  if(!t)return null;
  const r=p.r,id="event:"+String(revision+1);
  if(records.some(x=>x.id===id))return null;
  if(r.op==="replace"&&records.some(x=>x.active&&x.root===t.root&&x.kind==="exception"))return null;
  const kind=r.branch?"exception":r.op==="replace"?"base":"additional";
  const newRecord={...t,id,value:r.value,source:r.source,span:r.span,revision:revision+1,parent:t.id,op:r.op==="addMin"?">=":"<=",branch:r.branch,kind,active:true};
  return [...records.map(x=>x.id===t.id&&kind==="base"?{...x,active:false}:x),newRecord];
 }
 function decision(rs,root,branch,value){
  let relevant=rs.filter(x=>x.active&&x.root===root&&(x.branch===null||x.branch===branch));
  if(relevant.filter(x=>x.kind==="base").length!==1)return "UNKNOWN";
  if(relevant.some(x=>x.kind==="exception"))relevant=relevant.filter(x=>x.kind!=="base");
  return relevant.every(x=>x.op==="<="?value<=x.value:value>=x.value);
 }
 function current(rs,p,receipt,revision,root,branch,value){
  const changed=commit(rs,p,receipt,revision);return changed?decision(changed,root,branch,value):"UNKNOWN";
 }
 const defs=[
  {a:"我的每月生活费最多5000美元",b:"我的每月房租最多7000美元",refs:[["我的每月生活费",[0]],["我的每月房租",[1]],["我的预算",[0,1]],["刚才那项",[0,1]],["朋友的预算",[]],["每年生活费",[]],["生活费",[0]],["房租",[1]]]},
  {a:"我的每月生活费最多5000美元",b:"朋友的每月生活费最多7000美元",refs:[["我的生活费",[0]],["朋友的生活费",[1]],["每月生活费",[0,1]],["刚才那项",[0,1]],["房租",[]],["我的预算",[0]],["朋友的预算",[1]]]},
  {a:"我的每月生活费最多5000美元",b:"我的每年生活费最多7000美元",refs:[["每月生活费",[0]],["每年生活费",[1]],["我的生活费",[0,1]],["刚才那项",[0,1]],["房租",[]],["每月预算",[0]],["每年预算",[1]]]},
  {a:"我的每月生活费最多5000美元",b:"我的每月生活费最多7000韩元",refs:[["美元预算",[0]],["韩元预算",[1]],["我的生活费",[0,1]],["刚才那项",[0,1]],["每年预算",[]],["我的每月生活费美元",[0]],["我的每月生活费韩元",[1]]]}
 ];
 const modes=[["改为","replace",false],["另加上限","addMax",false],["另加下限","addMin",false],["改为","replace",true],["增加到","ambiguous",false],["另加上限","addMax",true]];
 let out={episodes:0,proposalMatches:0,commits:0,blocked:0,decisionChecks:0,decisionMatches:0,currentUnknown:0,baselineWrongMutations:0,baselineWrongPass:0,baselineWrongFail:0,controls:0,statuses:{}},witnesses={};
 for(const [fi,f] of defs.entries())for(const reverse of [false,true])for(const [ref,ids] of f.refs)for(const [word,op,conditional] of modes)for(const value of [4000,6000,8000])for(const u of ["美元","韩元"]){
  const original=[initial(f.a,"0"),initial(f.b,"1")];ck(original.every(Boolean),"initial");let rs=reverse?[original[1],original[0]]:original;
  const before=JSON.stringify(rs),text=(conditional?"如果选方案B，":"")+"把"+ref+word+value+u,p=propose(rs,text,2);
  let expected=op==="ambiguous"?"UNKNOWN_OPERATION":ids.length===0?"UNRESOLVED":ids.length>1?"AMBIGUOUS":fi===1&&ids[0]===1?"AUTHORITY_REQUIRED":u!==(fi===3&&ids[0]===1?"韩元":"美元")?"CURRENCY_CONFLICT":conditional&&op!=="replace"?"UNSUPPORTED_BRANCH_OPERATION":"PENDING";
  ck(p.status===expected,"proposal "+text);if(p.status==="PENDING")ck(p.ids[0]===String(ids[0]),"target");
  out.episodes++;out.proposalMatches++;out.statuses[expected]=(out.statuses[expected]||0)+1;
  let rec={authorized:true,revision:2,target:p.target,source:text},changed=commit(rs,p,rec,2);
  ck(JSON.stringify(rs)===before,"original mutation");ck(!!changed===(expected==="PENDING"),"commit");if(changed)out.commits++;else out.blocked++;
  let parsed=parse(text),last=parsed&&rs.filter(x=>Object.entries(parsed.ref).every(([k,v])=>x[k]===v)).at(-1);
  let naive=last&&last.owner==="self"&&last.unit===parsed.unit?{id:last.root,value}:null;
  const mutationCorrect=expected==="PENDING"&&!conditional&&op==="replace"?naive?.id===String(ids[0]):!naive;
  if(!mutationCorrect){out.baselineWrongMutations++;if(!witnesses.mutation)witnesses.mutation={text,expected,naive}}
  for(const id of ["0","1"])for(const branch of ["A","B"])for(const measurement of [3500,5000,6000,7000,8500]){
   const old=id==="0"?5000:7000;let gold=measurement<=old;
   if(expected==="PENDING"&&id===String(ids[0])){
    if(op==="replace"&&(!conditional||branch==="B"))gold=measurement<=value;
    else if(op==="addMax")gold=measurement<=old&&measurement<=value;
    else if(op==="addMin")gold=measurement<=old&&measurement>=value;
   }
   const got=decision(changed||rs,id,branch,measurement);ck(got===gold,"snapshot decision "+text);out.decisionChecks++;out.decisionMatches++;
   const published=current(rs,p,rec,2,id,branch,measurement);ck(published===(expected==="PENDING"?gold:"UNKNOWN"),"current");if(published==="UNKNOWN")out.currentUnknown++;
   if(expected==="PENDING"){
    const b=measurement<=(naive?.id===id?naive.value:old);
    if(b&&!gold){out.baselineWrongPass++;if(!witnesses.pass)witnesses.pass={text,id,branch,measurement}}
    if(!b&&gold){out.baselineWrongFail++;if(!witnesses.fail)witnesses.fail={text,id,branch,measurement}}
   }
  }
 }
 let rs=[initial(defs[0].a,"0"),initial(defs[0].b,"1")],p=propose(rs,"把生活费改为6000美元",2),ok={authorized:true,revision:2,target:p.target,source:p.r.source};
 for(const bad of [null,{...ok,authorized:false},{...ok,revision:1},{...ok,target:"base:1"},{...ok,source:"changed"}]){ck(commit(rs,p,bad,2)===null,"receipt");out.controls++}
 ck(commit(rs,p,ok,3)===null,"stale");out.controls++;
 ck(commit(rs.map(x=>x.root==="0"?{...x,revision:2}:x),p,ok,2)===null,"target stale");out.controls++;
 for(const s of ["把它改为6000美元","把生活费改为6000美元左右","把生活费改为6000","把生活费改为6000美元。","如果选方案C，把生活费改为6000美元","把生活费改为-1美元"]){ck(propose(rs,s,2).status==="UNKNOWN_SYNTAX",s);out.controls++}
 function step(text,rev){let p=propose(rs,text,rev),n=commit(rs,p,{authorized:true,revision:rev,target:p.target,source:text},rev);ck(n,"sequence "+text);rs=n}
 step("把生活费改为6000美元",2);step("把生活费改为5500美元",3);ck(decision(rs,"0","A",5600)===false&&decision(rs,"0","A",5500)===true,"second revision");out.controls++;
 step("把生活费另加上限5200美元",4);step("把生活费改为6000美元",5);ck(decision(rs,"0","B",5300)===false,"keep addition");out.controls++;
 step("如果选方案B，把生活费改为6500美元",6);ck(decision(rs,"0","A",5300)===false&&decision(rs,"0","B",5300)===false,"exception cannot discard additional");out.controls++;
 const later=propose(rs,"把生活费改为7000美元",7);ck(later.status==="EXCEPTION_SCOPE_REVIEW","review base scope");out.controls++;
 ck(propose(rs,"如果选方案B，把生活费改为8000美元",7).status==="EXCEPTION_SCOPE_REVIEW","duplicate scope");out.controls++;
 ck(new Set(rs.map(x=>x.id)).size===rs.length&&rs.filter(x=>x.root==="0"&&x.kind==="base"&&x.active).length===1&&rs.find(x=>x.id==="base:0").active===false,"identity");out.controls++;
 ck(current(rs,later,null,7,"0","A",0)==="UNKNOWN","pending gate");out.controls++;
 let fresh=[initial(defs[0].a,"0"),initial(defs[0].b,"1")];let b=propose(fresh,"如果选方案B，把生活费改为6000美元",2);let updated=commit(fresh,b,{authorized:true,revision:2,target:b.target,source:b.r.source},2);ck(decision(updated,"0","A",5500)===false&&decision(updated,"0","B",5500)===true,"branch isolation");out.controls++;
 return {out,witnesses};
};
console.log(JSON.stringify(probe(),null,2));
```

```json
{
  "out": {
    "episodes": 2088,
    "proposalMatches": 2088,
    "commits": 336,
    "blocked": 1752,
    "decisionChecks": 41760,
    "decisionMatches": 41760,
    "currentUnknown": 35040,
    "baselineWrongMutations": 672,
    "baselineWrongPass": 568,
    "baselineWrongFail": 192,
    "controls": 21,
    "statuses": {
      "PENDING": 336,
      "CURRENCY_CONFLICT": 420,
      "UNKNOWN_OPERATION": 348,
      "UNSUPPORTED_BRANCH_OPERATION": 84,
      "AMBIGUOUS": 480,
      "UNRESOLVED": 300,
      "AUTHORITY_REQUIRED": 120
    }
  },
  "witnesses": {
    "mutation": {
      "text": "把我的每月生活费另加上限4000美元",
      "expected": "PENDING",
      "naive": {
        "id": "0",
        "value": 4000
      }
    },
    "pass": {
      "text": "把我的每月生活费另加上限6000美元",
      "id": "0",
      "branch": "A",
      "measurement": 6000
    },
    "fail": {
      "text": "把我的每月生活费另加下限4000美元",
      "id": "0",
      "branch": "A",
      "measurement": 5000
    }
  }
}
```

## 下一步
下一轮优先研究多轮指代歧义下的决策相关性与最少追问，或可组合的指代/语用知识表示；先核查既有第24轮语料与澄清方法，避免重复。产品轨维护唯一交接，独立轨另冻自然情节并检查宿主确认与版本回退，模型轨研究稳定绑定及第63轮完整连接。未修改生产代码、训练、CI、Codex任务、合并、部署或使用第三方AI运行时，零新增费用，冻结协议不变。