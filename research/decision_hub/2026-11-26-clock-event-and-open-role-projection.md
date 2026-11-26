# 自主认知：钟点事件、开放角色候选与严格时间可行性
2026-11-26。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / POST_INSPECTION_DIAGNOSTIC / BOUNDED_MATH / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与查重
起始main b4faa9afbeaf7516c1d5d238e72d8a86abcc5cdb，核对12近期提交、15开放PR、v3.2/同步规程/唯一交接/前轮报告前12行，唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。Draft #63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍draft/unmerged。检索clock/temporal/time boundary/deadline/time expression/event time/travel time/door-to-door/departure/arrival/clock ambiguity/event binding。发现并审阅R117 866e86147409ee852b6bdfff2bb5939ee07568c8、R118 b4165eec265a6855440b3e07ca64abc14dfa8259、R119 c58fb6fb43989c611e17a36caeaaf80b6c7fd51e。R117已有钟点词法，R118已有民用日历锚定，R119已有逐日EDF共享资源，均不重复发明。本轮新增R117接入前轮角色候选、有限钟点方向与事件假设、局部开放对象候选、分钟级严格截止/分段缺失时长的判定。全库去重有限。未运行#63，不能宣称产品语义门改善。
## 固定资产
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-26-compositional-role-candidate-recovery.md b0bea7b4c101c170be2aaa2355973739b125e0b7
完整读取并核对连接器返回blob（非独立Git字节重算）；仅执行已审阅项目自有固定JS，生产禁止执行任意文档。实际复用R115 lexical/parseNum、R117 temporal、前轮propose及其R74/R77代码。两套公开原创ChatGPT研发辅助合成开发语料32情节64轮167标注；67个粗角色目标，前轮60/67。已经看到七个遗漏及其原文后设计候选，明确事后诊断，非盲测、训练、独立泛化、真人或真实使用。运行阶段仅输入原文与有无前轮；不输入标注、field、ref、领域或正确答案。候选全为authority NONE/outside true。
## 候选层
R117 CLOCK原文锚与同一分句最早/最晚、前到/后到/前出发/后出发组合为有限事件边界假设，前缀型event保持null，不能直接假定是出发；R117的无时段、分钟默认及宽松词法保留限制。要不要/是否后面的分句作为开放行动对象候选；大约/费用前的分句部分作为费用承担对象候选；仅保留文本，不拆出通用动词/实体/谓词。前轮存在且分句以是必须的结尾，产生角色改变候选；分句有说及R115数量，产生外部报告修订候选，单位及具体旧目标保持null。两类可能只是普通陈述，绝不能自动更新。新增分数固定10，旧候选原分数不改，相同跨度+角色去重。无新增业务对象字典，但规则仍是针对已知遗漏的有限模板，非通用分词或语义解析。完整池由8636增加为8647，新增11；所有七项遗漏出现，完整覆盖67/67。前5/10/20/50每类预算结果分别51/58/65/66，原44/51/58/59，实际候选数详表；非相同CPU预算。对照角色仅原文精确跨度及粗类别，不测完整语义或精度。5个新增对照均会生成不应直接采纳的候选：过去到达事实、到账疑问、物品估价、无修订目标的义务陈述、未绑定的他人报告。之前四个反例未解决，原候选仍保留；本轮没有自动消歧或独立义务确认。不得将67/67宣传成理解准确率。
## 钟点解释及时间计算
研究者选定civil-clock-ambiguous@1政策；无时段的1..11点保留两个分钟值，十二点保留0/720，0或13..23采用明确24小时假设；显式上午/下午等有限相容规则，未覆盖凌晨十二点、口语约略、隐含日期或所有合法表达。零分来自R117词法，精确分钟仍依赖宿主明确确认。时区/日期/主体/事件/比较符及时间精度不能从锚点推断，未实现时区数据库/DST。qualify为人工可信宿主夹具：仅检查给定期望与非空字段、允许及当前标志、所选分钟属于候选；非身份授权、来源认证、原文绑定、时区合法性或真实用户确认，所有authority NONE。19项控制含8钟点、1合格、10变异拒绝；另5负例仍有候选。不能作为生产资格门。
时间模型为已知同一线性分钟轴、可选最早出发、静态非负时长、无其他限制的隔离条件分析。最早出发是本模型所有更晚出发的弱优势，不能推广到班次时刻、动态路况或多目标。对截止<或<=，用已资格时长下界/上界判定全通过、全失败或混合；上界未知但已资格下界本身违反时，可确定失败；否则保留UNKNOWN_DURATION，不把缺少的分段时间默认0。初版对缺上界全部UNKNOWN，修正版允许上述单向失败证据，完整重跑。2268有限区间与逐整数直接枚举参照全部一致，55组严格/非严格结果不同。504个仅下界配置，逐公式与三个有限补全控制核对，统计见结果。124个车上50分钟加0..30分钟的有限构造点值，忽略额外时间对照有42个确定错误通过，不是现实频率或原生缺陷。连续实数区间单调关系同理，但本次只枚举整数分钟，未调用C028原生或科学模型注册。
L11原文为九点前到/最早八点、开车估计40..70分钟、火车说50分钟且只算车上。保留原文时间未确定，不能借标注08:00/09:00作真实锚；本轮只条件展示假设同日且同上午或同下午、允许最早出发、静态时长、所有时间估计在假设中有资格，则余量60分钟，开车混合（40..59可行、60..70违反），车上50分钟的所有额外路程必须严格小于10分钟；实际路程未知，不能确定火车通过。若两钟点时段各自未定，同日4个组合中两混合、一通过、一失败（仅针对该估计区间）。原文没有确认时段、日期、起点、时长证据或出发事件的充分资格，不得给现实推荐；当前仅可提出必要的时段和完整路程澄清。跨日需要独立共同时间轴。
## 结论及后续责任
本轮只补齐已知粗角色候选入口，不解决开放语义、原义务覆盖、主体、动作与实体、完整修订目标、时间锚及事实真实性。应停止继续针对这67项调词面以追求满分，转向独立未知/语义验证、跨轮角色与条件推理及外部合法语言开发诊断，保留独立轨未见留出；产品轨维护唯一交接，模型轨复算、准入和实际原生连接。预算/有限词面/时间政策/测试由研究者选定，未授权为生产标准。未修改生产、训练、合并PR、部署、主动CI或增加费用；R073/PESEN/冻结及历史证据等级不变。
## 复算
固定七份文件全文依次作为contents。Node标准JS，实际整合运行两次完整输出一致，候选结果及有限完整区间计数与初版一致。报告含代码与数据摘要，无单独ZIP。
```js
function experiment(contents){
 const ck=(x,m)=>{if(!x)throw Error(m)},docs=contents.slice(0,2).map(JSON.parse),code=i=>contents[i].split("```js\n")[1].split("\n```")[0];
 const L=Function(code(4).slice(code(4).indexOf("function experiment(A)")).split(" let out={corpusTurns:")[0]+"\nreturn {lexical,parseNum};\n}\nreturn experiment({});")();
 const T=Function("L",code(5).slice(code(5).indexOf("function experiment(L,R,I,G")).split(" // Reuse the actual R116 graph")[0]+"\nreturn {temporal};\n}\nreturn experiment(L);")(L);
 const B=Function("input",code(6).split(" function diversify(")[0]+"\nreturn {propose,R};\n}\nreturn experiment(input);")(contents.slice(0,5));
 const roles=["constraint","action","revision"],obj=(a,f)=>Object.fromEntries(a.map(k=>[k,f(k)])),key=v=>v.start+":"+v.end,rank=(a,b)=>b.score-a.score||a.start-b.start||a.end-b.end,ks=[1,5,10,20,50];
 function add(out,text,role,start,end,kind,detail){if(start<0||end>text.length||start>=end)return;out.push({role,start,end,text:text.slice(start,end),kind,detail,authority:"NONE",outside:true})}
 function propose(text,prior){
  let base=B.propose(text,prior).sets.repair,cl=B.R.scan(text).clauses,tem=T.temporal(text),newer=[];
  for(let c of tem.items.filter(v=>v.kind==="CLOCK")){
   let s=cl.find(v=>v.start<=c.start&&c.end<=v.end);if(!s)continue;
   for(let [prefix,op] of [["最早",">="],["最晚","<="]])if(c.start-prefix.length>=s.start&&text.slice(c.start-prefix.length,c.start)===prefix)add(newer,text,"constraint",c.start-prefix.length,c.end,"CLOCK_BOUND",{clock:c,op,event:null});
   for(let [suffix,op,event] of [["前到","<","arrival"],["后到",">","arrival"],["前出发","<","departure"],["后出发",">","departure"]])if(c.end+suffix.length<=s.end&&text.startsWith(suffix,c.end))add(newer,text,"constraint",c.start,c.end+suffix.length,"CLOCK_BOUND",{clock:c,op,event});
  }
  for(let s of cl){
   for(let w of ["要不要","是否"]){let i=s.text.indexOf(w);if(i>=0&&s.start+i+w.length<s.end)add(newer,text,"action",s.start+i+w.length,s.end,"QUESTION_COMPLEMENT",{cue:w,actor:null,modality:"UNKNOWN"})}
   for(let w of ["大约","费用"]){let i=s.text.indexOf(w);if(i>0)add(newer,text,"action",s.start,s.start+i,"COST_BEARER_CANDIDATE",{cue:w,actor:null,modality:"UNKNOWN"})}
   if(prior&&s.text.endsWith("是必须的"))add(newer,text,"revision",s.start,s.end,"ROLE_CHANGE_CANDIDATE",{target:null,operation:"promote_to_hard_candidate"});
   if(prior&&s.text.includes("说")&&L.lexical(s.text).items.length)add(newer,text,"revision",s.start,s.end,"REPORTED_VALUE_CHANGE_CANDIDATE",{target:null,source:"UNVERIFIED_REPORT",unit:null});
  }
  let all=obj(roles,r=>new Map(base[r].map(v=>[key(v),v])));
  for(let v of newer)if(!all[v.role].has(key(v)))all[v.role].set(key(v),{...v,score:10});
  return {base,all:obj(roles,r=>[...all[r].values()].sort(rank)),newer,temporal:tem.items.length,authority:"NONE",outside:true}
 }
 const out={episodes:0,turns:0,targets:0,baseFull:0,newFull:0,newCandidates:0,temporal:0,baseCount:0,newCount:0,byRole:obj(roles,r=>[0,0,0]),budget:obj(ks,k=>({base:0,new:0,baseCount:0,newCount:0,lost:0,gained:0})),recovered:[],missed:[],contrast:[],controls:0};
 for(let d=0;d<2;d++)for(let ep of docs[d].cases){out.episodes++;for(let ti=0;ti<ep.turns.length;ti++){
  let t=ep.turns[ti],p=propose(t.text,ti>0);out.turns++;out.temporal+=p.temporal;out.newCandidates+=p.newer.length;
  for(let r of roles){out.baseCount+=p.base[r].length;out.newCount+=p.all[r].length;for(let k of ks){out.budget[k].baseCount+=Math.min(k,p.base[r].length);out.budget[k].newCount+=Math.min(k,p.all[r].length)}}
  for(let a of d?t.proposal.claims:t.claims)for(let r of B.R.gold(d,a)){let q=d?a.quote:a.span,i=t.text.indexOf(q),j=i+q.length;ck(i>=0&&i===t.text.lastIndexOf(q),"unique");let match=v=>v.start===i&&v.end===j,old=p.base[r].some(match),now=p.all[r].some(match);out.targets++;out.baseFull+=+old;out.newFull+=+now;out.byRole[r][0]+=+old;out.byRole[r][1]+=+now;out.byRole[r][2]++;
   if(!old){let row={id:ep.id+"."+(ti+1),role:r,text:q,types:p.newer.filter(v=>v.role===r&&match(v)).map(v=>v.kind)};(now?out.recovered:out.missed).push(row)}
   for(let k of ks){let b=p.base[r].slice(0,k).some(match),n=p.all[r].slice(0,k).some(match),z=out.budget[k];z.base+=+b;z.new+=+n;z.lost+=+(b&&!n);z.gained+=+(!b&&n)}
  }
 }}
 ck(out.targets===67&&out.baseFull===60&&out.newFull===67&&out.temporal===48&&out.baseCount===8636&&out.newCount===8647,"baseline");
 for(let [s,prior,q,kind] of [["我昨天九点前到",false,"九点前到","CLOCK_BOUND"],["是否已经到账",false,"已经到账","QUESTION_COMPLEMENT"],["这台电脑大约五百",false,"这台电脑","COST_BEARER_CANDIDATE"],["证书是必须的",true,"证书是必须的","ROLE_CHANGE_CANDIDATE"],["同事说要七百",true,"同事说要七百","REPORTED_VALUE_CHANGE_CANDIDATE"]]){
  let z=propose(s,prior),v=z.newer.find(x=>x.text===q&&x.kind===kind);ck(!!v&&v.authority==="NONE","negative candidate");out.contrast.push({s,q,kind,authority:v.authority});
 }
 function clock(c,policy){if(!c||c.kind!=="CLOCK"||policy!=="civil-clock-ambiguous@1")return null;let {hour:h,minute:m,partOfDay:p}=c.detail;if(!Number.isInteger(h)||h<0||h>23||!Number.isInteger(m)||m<0||m>59)return null;
  if(p===null)return h===12?[m,720+m]:h>=1&&h<=11?[h*60+m,(h+12)*60+m]:[h*60+m];
  if(["凌晨","早上","上午"].includes(p)&&h>=1&&h<=11)return [h*60+m];
  if(["下午","晚上"].includes(p)&&h>=1&&h<=11)return [(h+12)*60+m];
  if(p==="中午"&&h===12)return [720+m];return null
 }
 const get=s=>T.temporal(s).items.find(v=>v.kind==="CLOCK"),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 for(let [s,e] of [["八点",[480,1200]],["九点",[540,1260]],["十二点",[0,720]],["下午五点半",[1050]],["上午八点",[480]],["晚上二十三点",null],["中午十二点",[720]],["十三点",[780]]]){ck(eq(clock(get(s),"civil-clock-ambiguous@1"),e),"clock "+s);out.controls++}
 function qualify(c,ctx){if(!ctx||!ctx.allowed||!ctx.current||!ctx.source||!ctx.event||!ctx.date||!ctx.zone||ctx.event!==ctx.expectedEvent||ctx.op!==ctx.expectedOp||ctx.root!==ctx.expectedRoot)return null;let t=clock(c,ctx.policy);if(!t||!t.includes(ctx.selectedMinute))return null;return {minute:ctx.selectedMinute,event:ctx.event,date:ctx.date,zone:ctx.zone,op:ctx.op,root:ctx.root,authority:"NONE"}}
 const c=get("八点"),ctx={allowed:true,current:true,source:"fixture-source",event:"departure",expectedEvent:"departure",date:"fixture-day",zone:"fixture-zone",op:">=",expectedOp:">=",root:"trip",expectedRoot:"trip",policy:"civil-clock-ambiguous@1",selectedMinute:480};
 ck(!!qualify(c,ctx),"qualify");out.controls++;
 for(let p of [{allowed:false},{current:false},{source:null},{event:"arrival"},{date:null},{zone:null},{op:"<"},{root:"other"},{policy:"unknown"},{selectedMinute:481}]){ck(!qualify(c,{...ctx,...p}),"qualification");out.controls++}
 // Unknown upper bound: a qualified lower bound alone may prove impossibility.
 function gate(dep,deadline,lo,hi,op){const test=t=>op==="<"?t<deadline:t<=deadline;if(!test(dep+lo))return "ALL_FAIL";if(hi===null)return "UNKNOWN_DURATION";return test(dep+hi)?"ALL_PASS":"MIXED"}
 function oracle(dep,deadline,lo,hi,op){let vals=[];for(let t=lo;t<=hi;t++)vals.push(op==="<"?dep+t<deadline:dep+t<=deadline);return vals.every(Boolean)?"ALL_PASS":vals.every(v=>!v)?"ALL_FAIL":"MIXED"}
 let math={cases:0,ALL_PASS:0,ALL_FAIL:0,MIXED:0,strictBoundaryDiff:0,partialCases:0,partialFail:0,partialUnknown:0,railFalsePass:0,railCases:0};
 for(let dep of [0,480,540,720,1200,1380])for(let end of [0,480,540,720,1260,1440,1500])for(let lo of [0,10,40,50,60,70])for(let hi of [0,10,40,50,60,70,120])if(lo<=hi)for(let op of ["<","<="]){let g=gate(dep,end,lo,hi,op);ck(g===oracle(dep,end,lo,hi,op),"math");math.cases++;math[g]++;if(op==="<"&&g!==gate(dep,end,lo,hi,"<="))math.strictBoundaryDiff++}
 for(let dep of [0,480,540,720,1200,1380])for(let end of [0,480,540,720,1260,1440,1500])for(let lo of [0,10,40,50,60,70])for(let op of ["<","<="]){
  let g=gate(dep,end,lo,null,op),ref=op==="<"?dep+lo>=end:dep+lo>end;
  ck(g===(ref?"ALL_FAIL":"UNKNOWN_DURATION"),"partial");math.partialCases++;math.partialFail+=+ref;math.partialUnknown+=+!ref;
  for(let hi of [lo,lo+1,lo+1441])if(ref)ck(oracle(dep,end,lo,hi,op)==="ALL_FAIL","partial safe");
 }
 for(let dep of [480,1200])for(let end of [540,1260])for(let extra=0;extra<=30;extra++){math.railCases++;if(gate(dep,end,50,50,"<")==="ALL_PASS"&&gate(dep,end,50+extra,50+extra,"<")==="ALL_FAIL")math.railFalsePass++}
 const l11=docs[0].cases.find(e=>e.id==="L11"),first=propose(l11.turns[0].text,false),second=propose(l11.turns[1].text,true);
 let arr=first.newer.find(x=>x.text==="九点前到"),dep=second.newer.find(x=>x.text==="最早八点");ck(arr&&dep&&dep.detail.event===null,"L11");out.travel={clockHypotheses:[],sameDaypartConditional:[],authority:"NONE"};
 for(let a of clock(dep.detail.clock,"civil-clock-ambiguous@1"))for(let b of clock(arr.detail.clock,"civil-clock-ambiguous@1")){let v={depart:a,deadline:b,drive:gate(a,b,40,70,"<"),rail:gate(a,b,50,null,"<"),extraUpperExclusive:b-a-50};out.travel.clockHypotheses.push(v);if(b-a===60)out.travel.sameDaypartConditional.push(v)}
 out.math=math;return out
}
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
console.log(JSON.stringify(experiment(contents),null,2));
```
## 实测输出
```json
{
  "episodes": 32,
  "turns": 64,
  "targets": 67,
  "baseFull": 60,
  "newFull": 67,
  "newCandidates": 11,
  "temporal": 48,
  "baseCount": 8636,
  "newCount": 8647,
  "byRole": {
    "constraint": [
      23,
      25,
      25
    ],
    "action": [
      27,
      30,
      30
    ],
    "revision": [
      10,
      12,
      12
    ]
  },
  "budget": {
    "1": {
      "base": 23,
      "new": 29,
      "baseCount": 88,
      "newCount": 94,
      "lost": 0,
      "gained": 6
    },
    "5": {
      "base": 44,
      "new": 51,
      "baseCount": 437,
      "newCount": 444,
      "lost": 0,
      "gained": 7
    },
    "10": {
      "base": 51,
      "new": 58,
      "baseCount": 851,
      "newCount": 858,
      "lost": 0,
      "gained": 7
    },
    "20": {
      "base": 58,
      "new": 65,
      "baseCount": 1584,
      "newCount": 1592,
      "lost": 0,
      "gained": 7
    },
    "50": {
      "base": 59,
      "new": 66,
      "baseCount": 3561,
      "newCount": 3569,
      "lost": 0,
      "gained": 7
    }
  },
  "recovered": [
    {
      "id": "L11.1",
      "role": "constraint",
      "text": "九点前到",
      "types": [
        "CLOCK_BOUND"
      ]
    },
    {
      "id": "L11.2",
      "role": "constraint",
      "text": "最早八点",
      "types": [
        "CLOCK_BOUND"
      ]
    },
    {
      "id": "L13.1",
      "role": "action",
      "text": "把他拉黑",
      "types": [
        "QUESTION_COMPLEMENT"
      ]
    },
    {
      "id": "L15.2",
      "role": "revision",
      "text": "证书是必须的",
      "types": [
        "ROLE_CHANGE_CANDIDATE"
      ]
    },
    {
      "id": "S12.1",
      "role": "action",
      "text": "修旧相机",
      "types": [
        "COST_BEARER_CANDIDATE"
      ]
    },
    {
      "id": "S12.1",
      "role": "action",
      "text": "买二手相机",
      "types": [
        "COST_BEARER_CANDIDATE"
      ]
    },
    {
      "id": "S12.2",
      "role": "revision",
      "text": "维修店说要七百",
      "types": [
        "REPORTED_VALUE_CHANGE_CANDIDATE"
      ]
    }
  ],
  "missed": [],
  "contrast": [
    {
      "s": "我昨天九点前到",
      "q": "九点前到",
      "kind": "CLOCK_BOUND",
      "authority": "NONE"
    },
    {
      "s": "是否已经到账",
      "q": "已经到账",
      "kind": "QUESTION_COMPLEMENT",
      "authority": "NONE"
    },
    {
      "s": "这台电脑大约五百",
      "q": "这台电脑",
      "kind": "COST_BEARER_CANDIDATE",
      "authority": "NONE"
    },
    {
      "s": "证书是必须的",
      "q": "证书是必须的",
      "kind": "ROLE_CHANGE_CANDIDATE",
      "authority": "NONE"
    },
    {
      "s": "同事说要七百",
      "q": "同事说要七百",
      "kind": "REPORTED_VALUE_CHANGE_CANDIDATE",
      "authority": "NONE"
    }
  ],
  "controls": 19,
  "travel": {
    "clockHypotheses": [
      {
        "depart": 480,
        "deadline": 540,
        "drive": "MIXED",
        "rail": "UNKNOWN_DURATION",
        "extraUpperExclusive": 10
      },
      {
        "depart": 480,
        "deadline": 1260,
        "drive": "ALL_PASS",
        "rail": "UNKNOWN_DURATION",
        "extraUpperExclusive": 730
      },
      {
        "depart": 1200,
        "deadline": 540,
        "drive": "ALL_FAIL",
        "rail": "ALL_FAIL",
        "extraUpperExclusive": -710
      },
      {
        "depart": 1200,
        "deadline": 1260,
        "drive": "MIXED",
        "rail": "UNKNOWN_DURATION",
        "extraUpperExclusive": 10
      }
    ],
    "sameDaypartConditional": [
      {
        "depart": 480,
        "deadline": 540,
        "drive": "MIXED",
        "rail": "UNKNOWN_DURATION",
        "extraUpperExclusive": 10
      },
      {
        "depart": 1200,
        "deadline": 1260,
        "drive": "MIXED",
        "rail": "UNKNOWN_DURATION",
        "extraUpperExclusive": 10
      }
    ],
    "authority": "NONE"
  },
  "math": {
    "cases": 2268,
    "ALL_PASS": 1153,
    "ALL_FAIL": 1019,
    "MIXED": 96,
    "strictBoundaryDiff": 55,
    "partialCases": 504,
    "partialFail": 233,
    "partialUnknown": 271,
    "railFalsePass": 42,
    "railCases": 124
  }
}
```
