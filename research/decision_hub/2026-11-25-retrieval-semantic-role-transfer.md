# 自主认知专项累计第83轮候选：非参数语义角色检索与陌生表达迁移诊断

2026-11-25。RESEARCH_CANDIDATE / FIXED_RETRIEVAL_DIAGNOSTIC_EXECUTED / ORACLE_SPAN / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main 71fbbc4ffa7dd7ded02476cd1781c98294263ee0。核对最近20提交、13开放PR、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R72、R73、R82首35行。区别于R72字符词表覆盖、R73标注映射、R80跨轮引用边排序、R82固定组合词：本轮复用完整既有开发语料，实际比较不拟合权重的跨情节语义角色示例检索。无需第三方AI模型，无权重更新、语料仅开发诊断用途，不授权训练，不选择最终模型。

## 输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132。
两JSON全文实际取得并核对连接器blob。32个情节64轮167标注，ChatGPT研发辅助原创公开合成开发语料，非真人、独立留出或独立作者。沿用R73粗角色映射（保留L revision与S不同原标签逻辑，不主张真实等价），类别语义未经独立审定。测试查询已给定人工标注原文跨度，候选检索只用跨度文本及本轮前后最多8 UTF16字符，不使用目标角色、标签或后轮文本。未测试原始整句的跨度发现、完整语义义务、真实概念或关系、未知表达识别。

## 设计
三组检索库切分：排除整个目标情节；排除同一领域（研究者把study/learning、finance/financial_planning、health/wellness合并，其他原领域保留）；仅另一语料库。无法排除生成者、情节改写祖先等隐性同源，均为已见开发集诊断。频数基线；字符一元/二元集合Jaccard；两者等权；再加本轮局部上下文二元组等权。权重和窗口研究者预定用于本次实验，未拟合或校准；方法固定，但诊断后不得把最佳方法的同集结果当独立泛化。每个角色只取最高相似度，不把重复支持当独立；0相似不输出角色，同分第一保留全部不强行选取。前3角色含截止并列，可能多于3，单独报告平均集合大小。唯一首位仅为候选，不是确定分类，outside=true，authority=NONE。全部167查询为分母；已标角色不在检索库单独统计，不能把缺失角色预测当已知；唯一首位一致率按有唯一候选分母，整体一致率按167，零二元组重叠单列以评估词面陌生子集（不等于语义陌生）。粗标签与候选一致为代理指标，非真实语义真值。不同切分重叠，禁止把三个分母累加当独立样本。没有真人、负例、校准、开放义项检测、实际用户负担、设备性能或原生平台验收。十项专项控制，同一研究者执行。无新增外部资料、训练、生产修改、Codex、CI、PR合并、部署、费用或冻结协议变更。

## 可复算代码
按L/S顺序加载完整JSON。
```js
function experiment(docs){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 const L={HARD:"constraint",CONDITIONAL_HARD:"constraint",PREFERENCE:"preference",GOAL:"goal",USER_REPORTED:"report",UNKNOWN:"unknown",UNAVAILABLE_EVIDENCE:"unknown",REPORTED_UNCERTAIN:"report",REPORTED_PROMISE:"report",REPORTED_POSSIBILITY:"report",REPORTED_EXTERNAL:"report",REPORTED_UNVERIFIED:"report",REPORTED_ESTIMATE:"estimate",ESTIMATE:"estimate",PAST_COST:"cost",FUTURE_COST:"cost",PROPOSED_ACTION:"action",CONDITIONAL_ACTION:"action",ACTION:"action",CONFIRMED_CHOICE:"choice",OBSERVED_OUTCOME:"observation",COUNTERFACTUAL_CLAIM:"counterfactual",HYPOTHESIS:"hypothesis",POSTHOC:"retrospective",RETROSPECTIVE_ESTIMATE:"retrospective",RECORD_INTENT:"permission_intent",AUTHORIZATION_PROPOSAL:"permission_intent",EVENT_DEFINITION:"event_definition",TRIGGER:"trigger",EXCEPTION:"scope_modifier",EXCLUSION:"scope_modifier",HARD_CONSEQUENCE:"consequence",REVISION:"revision",CONFIRM:"confirmation"};
 const S={action:"action",criterion:"criterion",unknown:"unknown",constraint:"constraint",goal:"goal",fact:"report",observation:"observation",permission_intent:"permission_intent",estimate:"estimate"};
 const group=d=>({study:"learning",finance:"financial_planning",health:"wellness"})[d]||d;
 const norm=s=>s.normalize("NFKC").replace(/[\p{P}\p{Z}\s]/gu,"");
 const grams=(s,k)=>{let a=[...norm(s)];return new Set(a.slice(0,Math.max(0,a.length-k+1)).map((_,i)=>a.slice(i,i+k).join("")))};
 const jac=(a,b)=>{let n=0;for(let x of a)if(b.has(x))n++;return n/(a.size+b.size-n||1)};
 let rows=[];
 for(let d=0;d<docs.length;d++)for(let ep of docs[d].cases)for(let ti=0;ti<ep.turns.length;ti++){
  let t=ep.turns[ti],cs=d===0?t.claims:t.proposal.claims;
  for(let i=0;i<cs.length;i++){
   let c=cs[i],q=d===0?c.span:c.quote,role=d===0?L[c.kind]:S[c.role],at=t.text.indexOf(q);
   ck(role&&at>=0&&at===t.text.lastIndexOf(q),"anchor and role");
   // Oracle span; context only from the same observed turn, no future turn.
   let context=t.text.slice(Math.max(0,at-8),Math.min(t.text.length,at+q.length+8));
   rows.push({id:ep.id+"."+ti+"."+i,ep:ep.id,d,group:group(ep.domain),role,q,one:grams(q,1),two:grams(q,2),context:grams(context,2)})
  }
 }
 const modes=["episode","domain","corpus"],methods=["frequency","unigram","bigram","mixed","mixed_context"],blank=()=>({queries:0,absentLabel:0,zeroBigram:0,exactDuplicate:0,comparisons:0,methods:Object.fromEntries(methods.map(m=>[m,{covered:0,correctUnique:0,wrongUnique:0,ambiguous:0,noEvidence:0,top3InclusiveHit:0,top3SizeSum:0,zeroBigramCorrectUnique:0,zeroBigramCovered:0,unsupportedRoleCovered:0}]))});
 const out={rows:rows.length,episodes:new Set(rows.map(x=>x.ep)).size,roles:new Set(rows.map(x=>x.role)).size,modes:Object.fromEntries(modes.map(m=>[m,blank()])),controls:0};
 function run(q,pool,method){
  // One max similarity per role avoids counting repeated examples as independent support.
  let v=new Map();
  for(let p of pool){
   let a=jac(q.one,p.one),b=jac(q.two,p.two),c=jac(q.context,p.context);
   let score=method==="frequency"?1:method==="unigram"?a:method==="bigram"?b:method==="mixed"?(a+b)/2:(a+b+c)/3;
   if(method==="frequency")v.set(p.role,(v.get(p.role)||0)+1);
   else if(score>0)v.set(p.role,Math.max(v.get(p.role)||0,score));
  }
  let rank=[...v].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])),top=rank.length?rank.filter(x=>Math.abs(x[1]-rank[0][1])<=1e-12).map(x=>x[0]):[];
  let t3=rank.length?rank.filter(x=>x[1]>=rank[Math.min(2,rank.length-1)][1]-1e-12).map(x=>x[0]):[];
  return {top,t3,authority:"NONE",outside:true};
 }
 for(let mode of modes)for(let q of rows){
  let pool=rows.filter(p=>p.ep!==q.ep&&(mode==="episode"||mode==="domain"&&p.group!==q.group||mode==="corpus"&&p.d!==q.d));
  ck(pool.every(p=>p.ep!==q.ep),"episode leakage");
  if(mode==="domain")ck(pool.every(p=>p.group!==q.group),"domain leakage");
  if(mode==="corpus")ck(pool.every(p=>p.d!==q.d),"corpus leakage");
  let z=out.modes[mode],absent=!pool.some(p=>p.role===q.role),zero=!pool.some(p=>jac(q.two,p.two)>0);
  z.queries++;z.absentLabel+=+absent;z.zeroBigram+=+zero;z.exactDuplicate+=+pool.some(p=>norm(p.q)===norm(q.q));z.comparisons+=pool.length;
  for(let method of methods){
   let p=run(q,pool,method),m=z.methods[method];ck(p.authority==="NONE"&&p.outside,"authority");
   if(!p.top.length)m.noEvidence++;
   else if(p.top.length>1)m.ambiguous++;
   else{m.covered++;m.correctUnique+=+(p.top[0]===q.role);m.wrongUnique+=+(p.top[0]!==q.role);m.zeroBigramCovered+=+zero;m.zeroBigramCorrectUnique+=+(zero&&p.top[0]===q.role);m.unsupportedRoleCovered+=+absent}
   m.top3InclusiveHit+=+p.t3.includes(q.role);m.top3SizeSum+=p.t3.length;
  }
 }
 for(let z of Object.values(out.modes))for(let m of Object.values(z.methods)){
  ck(m.covered+m.ambiguous+m.noEvidence===z.queries&&m.correctUnique+m.wrongUnique===m.covered,"counts");
  ck(m.correctUnique<=z.queries-z.absentLabel&&m.top3InclusiveHit<=z.queries-z.absentLabel,"missing role");
  m.selectiveAgreement=m.covered?m.correctUnique/m.covered:null;m.allAgreement=m.correctUnique/z.queries;
 }
 for(let t of [()=>rows.length===167,()=>out.episodes===32,()=>Object.values(out.modes).every(z=>z.queries===167),()=>out.modes.domain.comparisons<=out.modes.episode.comparisons,()=>out.modes.corpus.comparisons<=out.modes.episode.comparisons,()=>run({one:new Set(),two:new Set(),context:new Set()},rows,"mixed").top.length===0,()=>run(rows[0],[],"frequency").top.length===0,()=>run(rows[0],[rows[0]],"mixed").top[0]===rows[0].role,()=>Object.values(out.modes).every(z=>z.methods.bigram.zeroBigramCovered===0),()=>Object.values(out.modes).every(z=>z.methods.bigram.noEvidence===z.zeroBigram)]){ck(t(),"control");out.controls++}
 return out;
}
```

## 实际结果
```json
{
  "rows": 167,
  "episodes": 32,
  "roles": 21,
  "modes": {
    "episode": {
      "queries": 167,
      "absentLabel": 8,
      "zeroBigram": 49,
      "exactDuplicate": 2,
      "comparisons": 27000,
      "methods": {
        "frequency": {
          "covered": 114,
          "correctUnique": 1,
          "wrongUnique": 113,
          "ambiguous": 53,
          "noEvidence": 0,
          "top3InclusiveHit": 85,
          "top3SizeSum": 501,
          "zeroBigramCorrectUnique": 1,
          "zeroBigramCovered": 37,
          "unsupportedRoleCovered": 6,
          "selectiveAgreement": 0.008771929824561403,
          "allAgreement": 0.005988023952095809
        },
        "unigram": {
          "covered": 140,
          "correctUnique": 31,
          "wrongUnique": 109,
          "ambiguous": 25,
          "noEvidence": 2,
          "top3InclusiveHit": 88,
          "top3SizeSum": 540,
          "zeroBigramCorrectUnique": 8,
          "zeroBigramCovered": 34,
          "unsupportedRoleCovered": 7,
          "selectiveAgreement": 0.22142857142857142,
          "allAgreement": 0.18562874251497005
        },
        "bigram": {
          "covered": 107,
          "correctUnique": 24,
          "wrongUnique": 83,
          "ambiguous": 11,
          "noEvidence": 49,
          "top3InclusiveHit": 48,
          "top3SizeSum": 241,
          "zeroBigramCorrectUnique": 0,
          "zeroBigramCovered": 0,
          "unsupportedRoleCovered": 5,
          "selectiveAgreement": 0.22429906542056074,
          "allAgreement": 0.1437125748502994
        },
        "mixed": {
          "covered": 147,
          "correctUnique": 34,
          "wrongUnique": 113,
          "ambiguous": 18,
          "noEvidence": 2,
          "top3InclusiveHit": 88,
          "top3SizeSum": 532,
          "zeroBigramCorrectUnique": 8,
          "zeroBigramCovered": 34,
          "unsupportedRoleCovered": 7,
          "selectiveAgreement": 0.23129251700680273,
          "allAgreement": 0.20359281437125748
        },
        "mixed_context": {
          "covered": 157,
          "correctUnique": 38,
          "wrongUnique": 119,
          "ambiguous": 8,
          "noEvidence": 2,
          "top3InclusiveHit": 91,
          "top3SizeSum": 529,
          "zeroBigramCorrectUnique": 11,
          "zeroBigramCovered": 40,
          "unsupportedRoleCovered": 7,
          "selectiveAgreement": 0.24203821656050956,
          "allAgreement": 0.2275449101796407
        }
      }
    },
    "domain": {
      "queries": 167,
      "absentLabel": 11,
      "zeroBigram": 52,
      "exactDuplicate": 0,
      "comparisons": 25900,
      "methods": {
        "frequency": {
          "covered": 129,
          "correctUnique": 14,
          "wrongUnique": 115,
          "ambiguous": 38,
          "noEvidence": 0,
          "top3InclusiveHit": 85,
          "top3SizeSum": 501,
          "zeroBigramCorrectUnique": 6,
          "zeroBigramCovered": 41,
          "unsupportedRoleCovered": 5,
          "selectiveAgreement": 0.10852713178294573,
          "allAgreement": 0.08383233532934131
        },
        "unigram": {
          "covered": 137,
          "correctUnique": 31,
          "wrongUnique": 106,
          "ambiguous": 27,
          "noEvidence": 3,
          "top3InclusiveHit": 86,
          "top3SizeSum": 531,
          "zeroBigramCorrectUnique": 7,
          "zeroBigramCovered": 35,
          "unsupportedRoleCovered": 10,
          "selectiveAgreement": 0.22627737226277372,
          "allAgreement": 0.18562874251497005
        },
        "bigram": {
          "covered": 105,
          "correctUnique": 25,
          "wrongUnique": 80,
          "ambiguous": 10,
          "noEvidence": 52,
          "top3InclusiveHit": 46,
          "top3SizeSum": 223,
          "zeroBigramCorrectUnique": 0,
          "zeroBigramCovered": 0,
          "unsupportedRoleCovered": 8,
          "selectiveAgreement": 0.23809523809523808,
          "allAgreement": 0.1497005988023952
        },
        "mixed": {
          "covered": 145,
          "correctUnique": 35,
          "wrongUnique": 110,
          "ambiguous": 19,
          "noEvidence": 3,
          "top3InclusiveHit": 86,
          "top3SizeSum": 524,
          "zeroBigramCorrectUnique": 7,
          "zeroBigramCovered": 35,
          "unsupportedRoleCovered": 10,
          "selectiveAgreement": 0.2413793103448276,
          "allAgreement": 0.20958083832335328
        },
        "mixed_context": {
          "covered": 156,
          "correctUnique": 40,
          "wrongUnique": 116,
          "ambiguous": 8,
          "noEvidence": 3,
          "top3InclusiveHit": 89,
          "top3SizeSum": 527,
          "zeroBigramCorrectUnique": 11,
          "zeroBigramCovered": 41,
          "unsupportedRoleCovered": 10,
          "selectiveAgreement": 0.2564102564102564,
          "allAgreement": 0.23952095808383234
        }
      }
    },
    "corpus": {
      "queries": 167,
      "absentLabel": 36,
      "zeroBigram": 79,
      "exactDuplicate": 2,
      "comparisons": 13524,
      "methods": {
        "frequency": {
          "covered": 167,
          "correctUnique": 8,
          "wrongUnique": 159,
          "ambiguous": 0,
          "noEvidence": 0,
          "top3InclusiveHit": 51,
          "top3SizeSum": 570,
          "zeroBigramCorrectUnique": 4,
          "zeroBigramCovered": 79,
          "unsupportedRoleCovered": 36,
          "selectiveAgreement": 0.04790419161676647,
          "allAgreement": 0.04790419161676647
        },
        "unigram": {
          "covered": 140,
          "correctUnique": 21,
          "wrongUnique": 119,
          "ambiguous": 24,
          "noEvidence": 3,
          "top3InclusiveHit": 61,
          "top3SizeSum": 514,
          "zeroBigramCorrectUnique": 8,
          "zeroBigramCovered": 62,
          "unsupportedRoleCovered": 30,
          "selectiveAgreement": 0.15,
          "allAgreement": 0.12574850299401197
        },
        "bigram": {
          "covered": 85,
          "correctUnique": 13,
          "wrongUnique": 72,
          "ambiguous": 3,
          "noEvidence": 79,
          "top3InclusiveHit": 27,
          "top3SizeSum": 143,
          "zeroBigramCorrectUnique": 0,
          "zeroBigramCovered": 0,
          "unsupportedRoleCovered": 16,
          "selectiveAgreement": 0.15294117647058825,
          "allAgreement": 0.07784431137724551
        },
        "mixed": {
          "covered": 147,
          "correctUnique": 22,
          "wrongUnique": 125,
          "ambiguous": 17,
          "noEvidence": 3,
          "top3InclusiveHit": 61,
          "top3SizeSum": 513,
          "zeroBigramCorrectUnique": 8,
          "zeroBigramCovered": 62,
          "unsupportedRoleCovered": 30,
          "selectiveAgreement": 0.14965986394557823,
          "allAgreement": 0.1317365269461078
        },
        "mixed_context": {
          "covered": 156,
          "correctUnique": 23,
          "wrongUnique": 133,
          "ambiguous": 9,
          "noEvidence": 2,
          "top3InclusiveHit": 67,
          "top3SizeSum": 522,
          "zeroBigramCorrectUnique": 9,
          "zeroBigramCovered": 69,
          "unsupportedRoleCovered": 31,
          "selectiveAgreement": 0.14743589743589744,
          "allAgreement": 0.1377245508982036
        }
      }
    }
  },
  "controls": 10
}
```

## 下一责任
该诊断用于量化单纯示例检索的局限，不能替代自主语义学习和组合语义。手动窗口继续研究联合角色/概念候选搜索和真实可学习接口；数据轨负责合法真实资料及情节祖先；独立轨保管独立留出；产品轨维护唯一交接。保留R50完整开发范围及正式验收门，训练和工程版本另获授权。
