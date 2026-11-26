# 自主认知：条件构式的原文封套、考虑动作与适用范围分离
2026-11-26。RESEARCH_CANDIDATE / PUBLIC_SYNTHETIC_DEVELOPMENT / POST_INSPECTION_DIAGNOSTIC / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线及查重
固定main 6a11adb488cb74078129176d0df33d9c49365166；核对15近期提交、#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍open/draft、v3.2及同步规程。复用同一窗口上一轮唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前段，未重新读取最新交接身份，亦未重新枚举全部开放PR；局部查重非全库证明。实际读取前轮数值世界投影 e9290c4efda30628dfbd8d76691d3f1f7fee7669、条件方向 529750962f2686179703de19e37d5e037fd75d0d、联合语义 d827adc15f983c9c66c4f9fb989d2d911b92a9c6、账本效果 18ae7920f9ca317da66d1d50ba7f0fc3d8951c26、联合政策 5fed5e9108fbc97257fbf0546d521aa3cf725769、联合条件角色历史 94f6de457f60655cabb8f65dd90c6e4be81591cb 和R131条件极性 81df7d2fc56f29084ecc623b98cdf0991d3260d4 前段及相关代码。已有全部跨度候选及排名、政策方向、证据和条件硬门不重复。前轮四个显式条件标注均在完整池内，其中S06“如果医生允许，我再考虑参加长跑活动”联合候选排名28。此轮专门研究保留“考虑”模态封套、条件事件与范围限制的结构差异及引语边界；不以改善这4例宣称语言泛化。
固定输入顺序及连接器blob：
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-26-joint-guard-role-history-candidate-audit.md 94f6de457f60655cabb8f65dd90c6e4be81591cb
两套语料32情节64轮为既有ChatGPT辅助原创公开合成开发材料，非独立留出、真实用户、训练。第三份报告仅作为历史对照读取；本轮不重跑其大候选池，不声称与旧算法同CPU/预算。
## 方法
Unicode标量坐标、有限引号栈与强句分段。对显式条件功能词，优先保留有逗号的前件和完整后件；无逗号枚举就/才/再等后件提示，不直接决定必要/充分关系。后件为“考虑”构式时保留完整模态封套、另提出动作补语；不能把考虑参加变为已决定参加，也不推出医生意见或条件真值。显式仅用于/适用于构式提取目标范围及完整约束文本，候选类型与事件守卫分开；不直接判断该约束能否撤回或适用于哪些范围。引号内不作为候选，跨引语或不匹配引号保守不连接，未解析转述不等于本人政策。功能词及预算由研究者在见过公开数据后选择，属于有限构式诊断而非通用解析，不新增领域业务词表，不用训练。原文长度512、候选128上限，未测试真实设备或解析复杂度上界；候选全部authority NONE/outside true。嵌套条件、反问、隐含条件、多层语用、角色/主体、跨轮引用、逻辑极性、事件实例、资格仍需独立推理与宿主确认。输出候选未覆盖不意味着无条件或无义务。
## 实际执行
标准JS连接器实际执行两次，结果一致。四个S中明确字面条件与目标跨度按原标注核对；其余未标注不能作负例。原报告旧候选历史对照仅4/4完整、3/4前5；本轮不能据同开发数据的少量候选或命中声称理解能力提高。16专项控制事后设计，记录失败和保留歧义。结果：
```json
{
  "turns": 64,
  "candidateTurns": 9,
  "candidates": 13,
  "targets": 4,
  "hits": 4,
  "top5": 4,
  "rows": [
    {
      "turn": "S03.2",
      "condition": "如果周五需要加班",
      "target": "周五答疑就取消",
      "rank": 1,
      "kind": "EVENT_GUARD_CANDIDATE",
      "modal": null,
      "candidates": 1,
      "ref": "S03.1.3"
    },
    {
      "turn": "S06.1",
      "condition": "如果医生允许",
      "target": "参加长跑活动",
      "rank": 2,
      "kind": "DELIBERATION_GUARD_CANDIDATE",
      "modal": "我再考虑",
      "candidates": 2,
      "ref": null
    },
    {
      "turn": "S09.2",
      "condition": "如果集合改到周一早上",
      "target": "隔天出发也可以",
      "rank": 1,
      "kind": "EVENT_GUARD_CANDIDATE",
      "modal": null,
      "candidates": 1,
      "ref": null
    },
    {
      "turn": "S13.2",
      "condition": "正式交付",
      "target": "准确率的要求仅用于正式交付",
      "rank": 1,
      "kind": "SCOPE_RESTRICTION_CANDIDATE",
      "modal": null,
      "candidates": 1,
      "ref": "S13.1.3"
    }
  ],
  "controls": 16,
  "controlFailures": [],
  "historicalControl": [
    {
      "s": "如果下雨，如果下雪，改路线。",
      "kind": [
        "EVENT_GUARD_CANDIDATE"
      ],
      "count": 1,
      "unresolved": 1,
      "authority": "NONE"
    },
    {
      "s": "如果他转述“明天取消”，我就核对。",
      "kind": [],
      "count": 0,
      "unresolved": 0,
      "authority": "NONE"
    },
    {
      "s": "假如我说如果迟到就取消，大家会怎么想？",
      "kind": [
        "EVENT_GUARD_CANDIDATE"
      ],
      "count": 1,
      "unresolved": 1,
      "authority": "NONE"
    },
    {
      "s": "如果需要，我再考虑取消。",
      "kind": [
        "EVENT_GUARD_CANDIDATE",
        "DELIBERATION_GUARD_CANDIDATE"
      ],
      "count": 2,
      "unresolved": 0,
      "authority": "NONE"
    },
    {
      "s": "费用上限仅用于正式交付，试验阶段不套用。",
      "kind": [
        "SCOPE_RESTRICTION_CANDIDATE"
      ],
      "count": 1,
      "unresolved": 0,
      "authority": "NONE"
    }
  ],
  "kinds": {
    "COMPACT_GUARD_CANDIDATE": 6,
    "EVENT_GUARD_CANDIDATE": 5,
    "DELIBERATION_GUARD_CANDIDATE": 1,
    "SCOPE_RESTRICTION_CANDIDATE": 1
  },
  "authority": "NONE"
}
```
## 工程接入
ConditionConstructionCandidate应保留guard/target/outer三个原文坐标、cue、modal及类型；坐标接入v0.8原文摘要和Unicode标量合同。事件守卫、范围限制、条件下仅考虑的行动分别送入不同的语义候选类型，保留未决主体、方向、条件及对象。后续研究在可信宿主显式确认语义和历史根后，比较条件分支的只读计算、长期记录版本及执行状态；不把“如果某事件就取消”直接作为当前无条件撤回。未实际连接原生API、CLI、Swift或真实数据，未训练、修改生产、交接、冻结、证据等级、PR、部署、CI或费用。
## 完整复算
Node包装未执行；核心study实际在连接器运行，固定三个文件按上列顺序读取。
```js
function study(contents){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const docs=contents.slice(0,2).map(JSON.parse),strong=new Set([..."。！？；.!?;\n"]),weak=new Set([..."，,"]),starts=["如果","只要","只有","除非","一旦","假如","若"],scopes=["仅用于","只用于","仅适用于","只适用于"],quotes={"“":"”","‘":"’","「":"」","『":"』","《":"》","\"":"\""},closeSet=new Set(Object.values(quotes));
 const cp=s=>[...s],match=(a,i,w)=>cp(w).every((v,j)=>a[i+j]===v),span=(a,i,j)=>({start:i,end:j,text:a.slice(i,j).join("")});
 function scan(text){
  const a=cp(text);
  if(a.length>512)return {status:"LIMIT",candidates:[],outside:true,authority:"NONE"};
  let stack=[],visible=[],bad=false;
  for(let i=0;i<a.length;i++){
   let c=a[i];if(stack.length){visible[i]=false;if(c===stack[stack.length-1])stack.pop();else if(quotes[c])stack.push(quotes[c]);}
   else if(quotes[c]){stack.push(quotes[c]);visible[i]=false}
   else if(closeSet.has(c)){bad=true;visible[i]=false}
   else visible[i]=true;
  }
  if(stack.length||bad)return {status:"QUOTE_UNRESOLVED",candidates:[],outside:true,authority:"NONE"};
  const marks=(i,ws)=>ws.find(w=>match(a,i,w)&&cp(w).every((_,j)=>visible[i+j]));
  const clauses=[];let st=0;
  for(let i=0;i<=a.length;i++)if(i===a.length||(visible[i]&&strong.has(a[i]))){if(i>st)clauses.push([st,i]);st=i+1;}
  let result=[],unresolved=[];
  const add=(kind,g0,g1,t0,t1,outer0,outer1,cue,modal=null)=>{
   if(g1<=g0||t1<=t0||outer1<=outer0)return;
   if(!visible.slice(g0,g1).every(Boolean)||!visible.slice(t0,t1).every(Boolean))return;
   const g=span(a,g0,g1),t=span(a,t0,t1),outer=span(a,outer0,outer1);
   result.push({kind,guard:g,target:t,outer,cue,modal,authority:"NONE",outside:true});
  };
  for(let [l,r] of clauses){
   let anchors=[];
   for(let i=l;i<r;i++){const w=marks(i,[...scopes,...starts]);if(w){anchors.push([i,w]);i+=cp(w).length-1}}
   for(let n=0;n<anchors.length;n++){
    const [i,w]=anchors[n],end=i+cp(w).length,next=anchors[n+1]?.[0]??r;
    // Explicit scope restriction: subject before marker and scope phrase after it.
    if(scopes.includes(w)){
     let left=i;while(left>l&&!weak.has(a[left-1]))left--;
     let right=end;while(right<r&&!weak.has(a[right]))right++;
     if(left===i||right===end){unresolved.push(span(a,i,end));continue}
     add("SCOPE_RESTRICTION_CANDIDATE",end,right,left,right,left,right,w);
     continue;
    }
    let sep=end;while(sep<next&&!weak.has(a[sep]))sep++;
    if(sep<next){
     let t0=sep+1,t1=t0;
     while(t1<next&&!weak.has(a[t1]))t1++;
     if(t1>t0){
      add("EVENT_GUARD_CANDIDATE",i,sep,t0,t1,t0,t1,w);
      // Keep the modal envelope, and expose its action complement as a separate span.
      for(let modal of ["我再考虑","再考虑","我才考虑","才考虑","我就考虑","就考虑"])
       if(match(a,t0,modal)&&t0+cp(modal).length<t1)add("DELIBERATION_GUARD_CANDIDATE",i,sep,t0+cp(modal).length,t1,t0,t1,w,modal);
      continue;
     }
    }
    // Compact forms without a comma: enumerate explicit consequence markers, retain ambiguity.
    let found=false;
    for(let j=end+1;j<next;j++){
     let m=marks(j,["我就","我才","就","才","再"]);if(!m)continue;
     let stop=j+cp(m).length;if(stop>=next)continue;
     add("COMPACT_GUARD_CANDIDATE",i,j,j,next,j,next,w,m);found=true;
    }
    if(!found)unresolved.push(span(a,i,end));
   }
  }
  const key=v=>[v.kind,v.guard.start,v.guard.end,v.target.start,v.target.end,v.modal].join(":");
  result=[...new Map(result.map(v=>[key(v),v])).values()];
  if(result.length>128)return {status:"LIMIT",candidates:[],outside:true,authority:"NONE"};
  return {status:"CANDIDATES",candidates:result,unresolved,outside:true,authority:"NONE"};
 }
 const out={turns:0,candidateTurns:0,candidates:0,targets:0,hits:0,top5:0,rows:[],controls:0,controlFailures:[],historicalControl:[],kinds:{},authority:"NONE"};
 for(let d=0;d<2;d++)for(let e of docs[d].cases)for(let i=0;i<e.turns.length;i++){
  const t=e.turns[i],z=scan(t.text),a=cp(t.text);out.turns++;out.candidateTurns+=+(z.candidates.length>0);out.candidates+=z.candidates.length;
  for(let v of z.candidates){out.kinds[v.kind]=(out.kinds[v.kind]||0)+1;ck(v.guard.text===span(a,v.guard.start,v.guard.end).text&&v.target.text===span(a,v.target.start,v.target.end).text&&v.outer.text===span(a,v.outer.start,v.outer.end).text&&v.authority==="NONE"&&v.outside,"span and authority")}
  if(d)for(let c of t.proposal.claims.filter(x=>x.condition)){
   let idx=z.candidates.findIndex(v=>v.guard.text===c.condition&&v.target.text===c.quote);out.targets++;out.hits+=+(idx>=0);out.top5+=+(idx>=0&&idx<5);
   out.rows.push({turn:e.id+"."+(i+1),condition:c.condition,target:c.quote,rank:idx>=0?idx+1:null,kind:idx>=0?z.candidates[idx].kind:null,modal:idx>=0?z.candidates[idx].modal:null,candidates:z.candidates.length,ref:c.ref});
  }
 }
 ck(out.turns===64&&out.targets===4,"fixed cohort");
 // Designed controls after seeing public cases. No assertion that candidate presence equals policy.
 const trials=[
 ["如果下雨，明天取消。","EVENT_GUARD_CANDIDATE","如果下雨","明天取消"],
 ["如果下雨。明天取消。",null,null,null],
 ["朋友说“如果下雨，明天取消”。",null,null,null],
 ["“如果下雨，明天取消",null,null,null],
 ["如果下雨，我再考虑改路线。","DELIBERATION_GUARD_CANDIDATE","如果下雨","改路线"],
 ["只有拿到证书我才报名。","COMPACT_GUARD_CANDIDATE","只有拿到证书","我才报名。".slice(0,-1)],
 ["只要下雨我就取消。","COMPACT_GUARD_CANDIDATE","只要下雨","我就取消"],
 ["费用上限仅适用于本月。","SCOPE_RESTRICTION_CANDIDATE","本月","费用上限仅适用于本月"],
 ["如果他转述“明天取消”，我就核对。",null,null,null],
 ["😀如果下雨，改路线。","EVENT_GUARD_CANDIDATE","如果下雨","改路线"],
 ["如果下雨，如果下雪，改路线。","EVENT_GUARD_CANDIDATE","如果下雪","改路线"],
 ["只有十天假。",null,null,null],
 ["若没收到答复就等等。","COMPACT_GUARD_CANDIDATE","若没收到答复","就等等"],
 ["除非已付款，否则暂缓。","EVENT_GUARD_CANDIDATE","除非已付款","否则暂缓"],
 ["无条件保存。",null,null,null],
 ["如果"+"甲".repeat(513)+"，取消。",null,null,null]
 ];
 for(let [s,k,g,t] of trials){const z=scan(s);let good=k?z.candidates.some(v=>v.kind===k&&v.guard.text===g&&v.target.text===t):z.candidates.length===0;out.controls++;if(!good)out.controlFailures.push({s,expected:k,candidates:z.candidates});}
 // Two known difficult cases illustrate ambiguity rather than successful semantic classification.
 for(let s of ["如果下雨，如果下雪，改路线。","如果他转述“明天取消”，我就核对。","假如我说如果迟到就取消，大家会怎么想？","如果需要，我再考虑取消。","费用上限仅用于正式交付，试验阶段不套用。"]){
  let z=scan(s);out.historicalControl.push({s,kind:z.candidates.map(v=>v.kind),count:z.candidates.length,unresolved:z.unresolved?.length??null,authority:z.authority});
 }
 return out;
}
const contents=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8"));
console.log(JSON.stringify(study(contents),null,2));
```
