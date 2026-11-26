# 自主认知：跨句话题、主体归属、所有者与转述来源的候选分离
2026-11-26。RESEARCH_CANDIDATE / KNOWN_SPAN_DIAGNOSTIC / PUBLIC_SYNTHETIC_DEVELOPMENT / POST_INSPECTION_DIAGNOSTIC / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线和查重
同一手动窗口连续研究第三阶段，起点main cbedaa2f16e441cbfd6a80bcebb76a666807c18f。沿用本轮前段已核对v3.2、同步规程和#63候选固定head 734686980b19da9291bdd08b67d4e2519c011acf，未重跑原生。实际读取R133关系支持 dff5ab32d4ea2698256f725f1ae3726578e4a015、R130隐含零值 aa30d5d4cd66d4bc2bc736372b9c0485b63f1362、钟点开放角色 ef103587b216ad07c1a47102ddb7cb8d2975283d、历史引用排序 6e17e892bc7bcc512efed8e28b8f29bee05c5877、开发集边界多样性 62ce014c62b4e8415ef92f31aec9a3236802bc83前段。已有主体资格、已给定字段身份、角色候选及跨轮引用，不重复声称这些算法；此轮专门在已知目标跨度下比较人称邻近、跨句话题及转述者/财产所有者/认知者分离。不是全库无重复证明。
固定资产：
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-26-conditional-construction-envelope-and-modal-scope.md 6f3bf015c3a82faaf863c8cc38a14230e75e7fc0
第二份报告仅查阅坐标与引语边界设计，本轮自行实现有限扫描，不声称复用其执行代码。第一份语料14情节28轮，为公开ChatGPT辅助原创合成开发数据，非真实用户、独立留出、授权训练。目标原文跨度由既有标注提供，属于oracle诊断，不能视为原生端到端、开放主体识别或真实准确率。已见S04/S05/S14例，后设计本算法；不宣称盲测。其他语料未重跑。
## 方法与范围
有限最长匹配人称/关系词扫描，Unicode标量坐标，有限引语栈，强句及逗号/冒号分段。输入目标在文本唯一出现且位于同分句、未落入引语内才计算，否则保留UNRESOLVED。直接邻近基线选择目标内首个人称或前置最近人称，否则默认本人；不代表v0.8原生。新候选区分目标内所有格、认知状态中的本人、外部转述来源、目标内/前置人称、显式本人话题切换、共同话题、替他人思考的显式话题，以及上轮话题弱证据。人称词面不确定具体身份，群体未绑定真实成员，归属主体不是语用所有者的完整定义；转述来源独立保留，不能把转述者当作指标主体，也不能据此验证事实。话题传递仅为候选软证据，跨轮仅有当前和前一轮，不建立长期身份记忆；默认本人也只有候选权限。规则人工赋分5/4/3/2/1.5/1/0，非概率。所有结果authority NONE/outside true，既有语义义务、独立未知、证据确认及硬门继续阻断。未授权新语言训练、不增加业务对象词表，但仍使用有限关系词，不能以此替代通用分词/句法/指代。无跨句完整引语分析、间接引述、精确主体ID、共指图、隐式省略、事件时间或来源认证；候选为空不证明无义务。
## 实验
首次运行因报告将source.evidence误读为source.mention而中止，未写入仓库。统一字段、明确半开区间交叠并拒绝空目标后重跑。实际执行固定公开开发集所有标注，对照给定目标跨度的actor（self/other/joint），分别记录基线top1、新top1/top2/完整候选覆盖以及未决和候选数。只比较标注覆盖，人工actor类别并非全部可能解析，不能从其推导精度或真实产品改善。15项事后设计控制含共同话题、所有者/认知者、报告源、跨轮本人重置、重复跨度、引语、主体切换和未知。保留全部失误，不修正权重追求已见小样本命中。两次实际执行结果一致。未测原生、独立验收、真实对话和设备资源。
```json
{
  "turns": 28,
  "targets": 69,
  "byActor": {
    "self": {
      "n": 60,
      "baseline": 58,
      "top1": 59,
      "top2": 60,
      "full": 60
    },
    "joint": {
      "n": 5,
      "baseline": 1,
      "top1": 5,
      "top2": 5,
      "full": 5
    },
    "other": {
      "n": 4,
      "baseline": 4,
      "top1": 4,
      "top2": 4,
      "full": 4
    }
  },
  "baselineTop1": 63,
  "top1": 68,
  "top2": 69,
  "full": 69,
  "candidateCounts": 79,
  "unresolved": 0,
  "sourceBound": 1,
  "holderBound": 1,
  "knowerBound": 2,
  "rows": [
    {
      "id": "S04.1",
      "quote": "我们两个人都得能用厨房",
      "expected": "joint",
      "baseline": "joint",
      "actors": [
        "joint",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    },
    {
      "id": "S04.1",
      "quote": "买电饭煲",
      "expected": "joint",
      "baseline": "self",
      "actors": [
        "joint",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    },
    {
      "id": "S04.1",
      "quote": "买小烤箱",
      "expected": "joint",
      "baseline": "self",
      "actors": [
        "joint",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    },
    {
      "id": "S04.1",
      "quote": "家里只有一个空插座",
      "expected": "joint",
      "baseline": "self",
      "actors": [
        "joint",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    },
    {
      "id": "S04.2",
      "quote": "插座数量刚核实是两个",
      "expected": "joint",
      "baseline": "self",
      "actors": [
        "joint",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    },
    {
      "id": "S05.1",
      "quote": "报考执照",
      "expected": "other",
      "baseline": "other",
      "actors": [
        "other",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    },
    {
      "id": "S05.1",
      "quote": "继续做现有工作",
      "expected": "other",
      "baseline": "other",
      "actors": [
        "other",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    },
    {
      "id": "S05.1",
      "quote": "她的预算我不清楚",
      "expected": "other",
      "baseline": "other",
      "actors": [
        "other",
        "self"
      ],
      "source": [],
      "holder": [
        "她的"
      ],
      "knower": [
        "我"
      ]
    },
    {
      "id": "S06.2",
      "quote": "医生的意见还没拿到",
      "expected": "self",
      "baseline": "other",
      "actors": [
        "other",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    },
    {
      "id": "S12.2",
      "quote": "维修店说要七百",
      "expected": "self",
      "baseline": "other",
      "actors": [
        "self"
      ],
      "source": [
        "维修店"
      ],
      "holder": [],
      "knower": []
    },
    {
      "id": "S14.2",
      "quote": "对方是否有空还不清楚",
      "expected": "other",
      "baseline": "other",
      "actors": [
        "other",
        "self"
      ],
      "source": [],
      "holder": [],
      "knower": []
    }
  ],
  "controls": 15,
  "failures": []
}
```
## 接入建议
ActorFrameCandidate保留本轮原文坐标、上轮来源身份、候选actor类别和具体证据、归属通道（holder/source/knower/topic）、原文义务与未决状态；不得将actor=other直接视为本人可计算参数，不用候选类别自动合并不同第三方。持久历史根必须经宿主确认；来源、人物、所有者、实际行动者、政策制定者各自独立。优先在#63原生回放中验证给定角色/主体后是否仍被错误阻断，扩充合法独立开发诊断，独立轨保管未见案例；避免继续围绕本组4个other及5个joint标注调词。此次未修改生产、唯一交接、历史冻结、证据等级、PR、训练、部署、主动CI或费用。
## 复算
标准JS核心实际在连接器执行两次，Node包装未执行。
```js
function study(contents){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const doc=JSON.parse(contents[0]),cp=s=>[...s],strong=new Set([..."。！？；.!?;\n"]),weak=new Set([..."，,：:"]);
 const qopen={"“":"”","‘":"’","「":"」","『":"』","\"":"\""},qclose=new Set(Object.values(qopen));
 const lex=[
  ["我们两个人","joint","PERSON"],["我们","joint","PERSON"],["我和","joint","GROUP_CUE"],["我本人","self","RESET"],["本人","self","RESET"],["我的","self","POSSESSOR"],["我","self","PERSON"],
  ["她的","other","POSSESSOR"],["他的","other","POSSESSOR"],["对方的","other","POSSESSOR"],["她","other","PERSON"],["他","other","PERSON"],["对方","other","PERSON"],
  ["同事","other","PERSON"],["朋友","other","PERSON"],["医生","other","PERSON"],["房东","other","PERSON"],["维修店","other","PERSON"],["单位","other","PERSON"]
 ].sort((a,b)=>cp(b[0]).length-cp(a[0]).length);
 const reportWords=["说","称","告诉","表示","承诺","转述","保证"],epistemic=["不清楚","不知道","没问","不确定"],frameWords=["替","帮"];
 const matches=(a,i,w)=>cp(w).every((c,j)=>a[i+j]===c);
 function read(text){
  const a=cp(text);if(a.length>512)return {ok:false,a,clauses:[],mentions:[],reports:[],frame:null,quoteUnknown:true};
  let stack=[],mask=[],bad=false;
  for(let i=0;i<a.length;i++){let c=a[i];if(stack.length){mask[i]=false;if(c===stack[stack.length-1])stack.pop();else if(qopen[c])stack.push(qopen[c]);}else if(qopen[c]){stack.push(qopen[c]);mask[i]=false}else if(qclose.has(c)){bad=true;mask[i]=false}else mask[i]=true}
  if(stack.length||bad)return {ok:false,a,clauses:[],mentions:[],reports:[],frame:null,quoteUnknown:true};
  let clauses=[],l=0;
  for(let i=0;i<=a.length;i++)if(i===a.length||mask[i]&&(strong.has(a[i])||weak.has(a[i]))){if(i>l)clauses.push({start:l,end:i,strongEnd:i===a.length||strong.has(a[i])});l=i+1;}
  const span=(i,j)=>({start:i,end:j,text:a.slice(i,j).join("")});
  const words=(i,ws)=>ws.find(w=>matches(a,i,w)&&cp(w).every((_,j)=>mask[i+j]));
  const mentions=[];
  for(let i=0;i<a.length;i++){
   if(!mask[i])continue;
   let m=lex.find(v=>words(i,[v[0]]));if(!m)continue;
   let j=i+cp(m[0]).length;mentions.push({...span(i,j),actor:m[1],kind:m[2]});i=j-1;
  }
  const reports=[];
  for(const m of mentions.filter(x=>x.actor==="other")){let w=words(m.end,reportWords);if(w)reports.push({actor:m.actor,mention:m,marker:span(m.end,m.end+cp(w).length)});}
  let frame=null;
  for(const c of clauses){
   const m=mentions.filter(x=>x.start>=c.start&&x.end<=c.end);
   if(m.some(x=>x.kind==="RESET")){frame={actor:"self",evidence:m.find(x=>x.kind==="RESET"),kind:"EXPLICIT_RESET"};break}
   if(m.some(x=>x.actor==="joint")&&m[0]?.start===c.start){frame={actor:"joint",evidence:m.find(x=>x.actor==="joint"),kind:"JOINT_TOPIC"};break}
   let cue=frameWords.find(w=>matches(a,c.start,w));
   if(cue){let v=m.find(x=>x.actor==="other"&&x.start===c.start+cp(cue).length);if(v){frame={actor:"other",evidence:v,kind:"EXPLICIT_OTHER_TOPIC"};break}}
  }
  return {ok:true,a,clauses,mentions,reports,frame,quoteUnknown:mask.some(v=>!v),mask};
 }
 function locate(text,target){
  const a=cp(text),t=cp(target),hits=[];
  if(!t.length)return null;
  for(let i=0;i+t.length<=a.length;i++)if(t.every((v,j)=>a[i+j]===v))hits.push(i);
  return hits.length===1?{start:hits[0],end:hits[0]+t.length}:null;
 }
 function infer(text,target,previous=null){
  const z=read(text),p=previous===null?null:read(previous),anchor=locate(text,target);
  if(!z.ok||!anchor||!z.mask.slice(anchor.start,anchor.end).every(Boolean))return {status:"UNRESOLVED",authority:"NONE",outside:true,actors:[],source:[],holder:[],knower:[],baseline:"unknown",anchor};
  const clause=z.clauses.find(v=>v.start<=anchor.start&&anchor.end<=v.end);
  if(!clause)return {status:"UNRESOLVED",authority:"NONE",outside:true,actors:[],source:[],holder:[],knower:[],baseline:"unknown",anchor};
  const m=z.mentions.filter(x=>x.start>=clause.start&&x.end<=clause.end);
  const local=m.filter(x=>x.start<anchor.end&&x.end>anchor.start);
  const preceding=m.filter(x=>x.end<=anchor.start),nearest=local[0]??preceding.at(-1);
  const r=z.reports.filter(x=>x.mention.start>=clause.start&&x.marker.end<=anchor.end);
  const source=r.map(x=>({actor:x.actor,evidence:x.mention,reportMarker:x.marker,kind:"REPORTED_SOURCE"}));
  const poss=local.filter(x=>x.kind==="POSSESSOR"),holder=poss.map(x=>({actor:x.actor,evidence:x,kind:"POSSESSION"}));
  const tail=z.a.slice(clause.start,clause.end).join(""),knower=[];
  if(epistemic.some(w=>tail.includes(w)))for(let x of m.filter(v=>v.actor==="self"))knower.push({actor:"self",evidence:x,kind:"KNOWER_CANDIDATE"});
  let candidates=[];
  const add=(actor,score,evidence,reason)=>{candidates.push({actor,score,evidence,reason,authority:"NONE"})};
  for(const v of holder)add(v.actor,4,v.evidence,"POSSESSOR");
  for(const v of local){
   if(v.kind==="POSSESSOR")continue;
   if(r.some(x=>x.mention.start===v.start))continue;
   if(knower.some(x=>x.evidence.start===v.start)&&holder.length)continue;
   add(v.actor,v.kind==="RESET"?5:3,v,"LOCAL_MENTION");
  }
  for(const v of preceding){if(r.some(x=>x.mention.start===v.start))continue;add(v.actor,v.kind==="RESET"?5:2,v,"PRECEDING_MENTION")}
  let fr=z.frame&&z.frame.evidence.start<anchor.end?z.frame:null;
  const resets=z.mentions.filter(x=>x.kind==="RESET"&&x.start<anchor.end);
  if(resets.length)fr={actor:"self",kind:"EXPLICIT_RESET",evidence:resets.at(-1)};
  if(fr)add(fr.actor,fr.kind==="EXPLICIT_RESET"?5:1.5,fr.evidence,"TURN_TOPIC");
  else if(p?.ok&&p.frame&&!m.length)add(p.frame.actor,1,{...p.frame.evidence,turn:"previous"},"PREVIOUS_TOPIC");
  add("self",0,null,"DEFAULT_USER_PERSPECTIVE");
  candidates.sort((a,b)=>b.score-a.score);
  const actors=[...new Set(candidates.map(x=>x.actor))].map(k=>candidates.find(x=>x.actor===k));
  return {status:"CANDIDATES",authority:"NONE",outside:true,actors,source,holder,knower,baseline:nearest?.actor??"self",anchor,quoteUnknown:z.quoteUnknown};
 }
 const out={turns:0,targets:0,byActor:{},baselineTop1:0,top1:0,top2:0,full:0,candidateCounts:0,unresolved:0,sourceBound:0,holderBound:0,knowerBound:0,rows:[],controls:0,failures:[]};
 for(let e of doc.cases)for(let i=0;i<e.turns.length;i++){
  const t=e.turns[i];out.turns++;
  for(let c of t.proposal.claims){
   const v=infer(t.text,c.quote,i?e.turns[i-1].text:null);
   ck(v.authority==="NONE"&&v.outside,"authority");out.targets++;
   const actors=v.actors.map(x=>x.actor),b=v.baseline===c.actor,a=actors[0]===c.actor,full=actors.includes(c.actor);
   let q=out.byActor[c.actor]??={n:0,baseline:0,top1:0,top2:0,full:0};q.n++;q.baseline+=+b;q.top1+=+a;q.top2+=+actors.slice(0,2).includes(c.actor);q.full+=+full;
   out.baselineTop1+=+b;out.top1+=+a;out.top2+=+actors.slice(0,2).includes(c.actor);out.full+=+full;out.candidateCounts+=actors.length;out.unresolved+=+(v.status==="UNRESOLVED");out.sourceBound+=+(v.source.length>0);out.holderBound+=+(v.holder.length>0);out.knowerBound+=+(v.knower.length>0);
   if(c.actor!=="self"||!a||v.source.length||v.holder.length)out.rows.push({id:e.id+"."+(i+1),quote:c.quote,expected:c.actor,baseline:v.baseline,actors,source:v.source.map(x=>x.evidence.text),holder:v.holder.map(x=>x.evidence.text),knower:v.knower.map(x=>x.evidence.text)});
  }
 }
 ck(out.turns===28&&out.byActor.other.n===4&&out.byActor.joint.n===5,"fixed evaluation cohort");
 const tests=[
  ["替同事想一想：她在考虑报名。她的预算我不清楚。","报名",null,v=>v.actors[0]?.actor==="other"],
  ["她的预算我不清楚。","她的预算我不清楚",null,v=>v.holder[0]?.actor==="other"&&v.knower[0]?.actor==="self"&&v.actors[0]?.actor==="other"],
  ["维修店说要七百。","维修店说要七百",null,v=>v.source[0]?.actor==="other"&&v.actors[0]?.actor==="self"],
  ["我们两个人都得能用厨房。想买电饭煲。","买电饭煲",null,v=>v.actors[0]?.actor==="joint"],
  ["我本人暂时没有换工作。","没有换工作","替同事想一想：她在考虑报名。",v=>v.actors[0]?.actor==="self"],
  ["预算是七百。","预算是七百","我们两个人都得能用厨房。",v=>v.actors.some(a=>a.actor==="joint")],
  ["朋友说“我不要夜班”。","我不要夜班",null,v=>v.status==="UNRESOLVED"&&v.actors.length===0],
  ["她的预算和我的预算。","预算",null,v=>v.status==="UNRESOLVED"],
  ["我和她都要报名。","报名",null,v=>v.actors.some(a=>a.actor==="joint")],
  ["对方是否有空还不清楚。","对方是否有空还不清楚",null,v=>v.actors[0]?.actor==="other"],
  ["朋友说工资高。","工资高",null,v=>v.source[0]?.actor==="other"],
  ["这只是我转述的“她的预算是七百”。","她的预算是七百",null,v=>v.status==="UNRESOLVED"],
  ["我们两个人都去。后来我本人不去。","不去",null,v=>v.actors[0]?.actor==="self"],
  ["她的预算我不清楚。","她的预算我不清楚","我本人想买电脑。",v=>v.actors[0]?.actor==="other"],
  ["这笔钱的来源不明确。","这笔钱的来源不明确",null,v=>v.actors.every(a=>a.authority==="NONE")&&v.outside]
 ];
 for(let [s,t,p,f] of tests){const v=infer(s,t,p);out.controls++;if(!f(v))out.failures.push({s,t,actors:v.actors.map(a=>a.actor),source:v.source.map(a=>a.evidence.text),status:v.status});}
 return out;
}
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
console.log(JSON.stringify(study(contents),null,2));
```
