# 自主认知：原文条件、角色及历史引用的联合候选审计
2026-11-26。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线及查重
固定main a532226cf95443a7a1af544bf2deae575866c399，核对20近期提交、15开放Draft PR、v3.2、同步规程、唯一产品交接前20行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）、完整目录树相关题名。#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。实际阅读 condition-polarity-attachment-candidate-audit.md 81df7d2fc56f29084ecc623b98cdf0991d3260d4（独立条件边及极性）、open-span-quantity-composition-audit.md 175f8b48a4cc46cb3b41b7b65b13b06448bf461a、implicit-zero-role-condition-inference.md aa30d5d4cd66d4bc2bc736372b9c0485b63f1362、raw-revision-to-confirmed-history-joint-ranking.md 6e17e892bc7bcc512efed8e28b8f29bee05c5877以及以下实际复用资产。已有单边条件及单角色检索、历史引用匹配，不重复调词面；本轮连接三类候选，以原文精确共同目标作为联合键，测组合覆盖与候选预算，非全库无重复证明。
## 固定资产
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
research/decision_hub/2026-11-25-bounded-semantic-candidate-search.md bbdc12dfe65b24aa24e6b1d25a04955766cadab4
research/decision_hub/2026-11-25-raw-text-reference-search.md 16075b3ba567ee6dc3496300beab1417172a6c42
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-26-compositional-role-candidate-recovery.md b0bea7b4c101c170be2aaa2355973739b125e0b7
research/decision_hub/2026-11-26-clock-event-and-open-role-projection.md ef103587b216ad07c1a47102ddb7cb8d2975283d
research/decision_hub/2026-11-25-condition-polarity-attachment-candidate-audit.md 81df7d2fc56f29084ecc623b98cdf0991d3260d4
全部完整获取，核对连接器blob，未独立重算原始Git字节。只加载固定已审查项目自有代码，生产禁止执行外部文档。两个语料共32情节64轮，ChatGPT研发辅助原创合成公开开发材料，已见且非独立留出、真人或授权训练。S中只有4项字面条件标注可精确评估，其中2项引用旧记录。L条件编码不充当原文守卫标注。生成只读取当前原文、是否有前轮及人工给定的首轮已确认记录身份/原文夹具；当前标注仅评价。没有将首轮人工标签等同实际授权记录。
## 方法
直接复用R131 graph及最新clock-event-and-open-role-projection的propose完整池（其原文词法/跨度/角色生成不变）。条件边的目标跨度与角色候选按完全相同start:end连接，保留角色候选各自身份；评分为原条件边score+角色score，两者非同尺度概率，此处仅人为排序。若角色为revision且有历史，进一步枚举每个历史根，评分加4倍局部字符集合及相邻双字集合Jaccard和（沿用前轮局部相似度思想，无额外上下文项）。同文不同根保留，同分稳定字符串顺序，不作语义消歧。条件边跨强句限制由原R131继承；没有新逻辑方向、主体、事件、否定、修订类型、作用域及资格推断。原文精确共目标是必要的研究连接合同，真实句法可能存在嵌套或不同跨度，不能将未连接当作语义不成立。候选全部authority NONE/outside true；候选未出现不能证明无条件，候选出现不能执行。raw与joint预算为每轮总前K，triples只含revision角色且历史存在，三类不同任务空间，计数不可直接等同CPU或准确率。条件角色用原S标签constraint/action，修订引用另测revision联合三元组；不把原条件动作角色当修订操作，两个维度仍需可信语义确认。全部候选全量构造后截取，无生产资源上界。
## 实际输出
标准JS连接器实际执行。核对原文位置、历史根身份、完整64轮4条件/2引用标注、共同跨度及强句隔离、相同描述不同根保留。以下结果只为候选存在/排名，不能视为完整语义准确率或真实产品效果。
```json
{
  "turns": 64,
  "edges": 2842,
  "joint": 3386,
  "triples": 1680,
  "conditionTargets": 4,
  "rawExact": 4,
  "roleExact": 4,
  "jointExact": 4,
  "revisionTargets": 2,
  "tripleExact": 2,
  "rows": [
    {
      "episode": "S03",
      "role": "action",
      "guard": "如果周五需要加班",
      "target": "周五答疑就取消",
      "ref": "S03.1.3",
      "rawRank": 1,
      "roleRank": 1,
      "jointRank": 1,
      "tripleRank": 1,
      "rawEdges": 203,
      "jointCount": 336,
      "tripleCount": 504
    },
    {
      "episode": "S06",
      "role": "action",
      "guard": "如果医生允许",
      "target": "参加长跑活动",
      "ref": null,
      "rawRank": 31,
      "roleRank": 13,
      "jointRank": 28,
      "tripleRank": null,
      "rawEdges": 314,
      "jointCount": 304,
      "tripleCount": 0
    },
    {
      "episode": "S09",
      "role": "action",
      "guard": "如果集合改到周一早上",
      "target": "隔天出发也可以",
      "ref": null,
      "rawRank": 1,
      "roleRank": 1,
      "jointRank": 1,
      "tripleRank": null,
      "rawEdges": 308,
      "jointCount": 308,
      "tripleCount": 336
    },
    {
      "episode": "S13",
      "role": "constraint",
      "guard": "正式交付",
      "target": "准确率的要求仅用于正式交付",
      "ref": "S13.1.3",
      "rawRank": 1,
      "roleRank": 2,
      "jointRank": 1,
      "tripleRank": 1,
      "rawEdges": 544,
      "jointCount": 824,
      "tripleCount": 840
    }
  ],
  "budgets": {
    "5": {
      "rawHit": 3,
      "jointHit": 3,
      "tripleHit": 2,
      "rawCount": 40,
      "jointCount": 40,
      "tripleCount": 15
    },
    "10": {
      "rawHit": 3,
      "jointHit": 3,
      "tripleHit": 2,
      "rawCount": 80,
      "jointCount": 80,
      "tripleCount": 30
    },
    "20": {
      "rawHit": 3,
      "jointHit": 3,
      "tripleHit": 2,
      "rawCount": 160,
      "jointCount": 160,
      "tripleCount": 60
    },
    "50": {
      "rawHit": 4,
      "jointHit": 4,
      "tripleHit": 2,
      "rawCount": 400,
      "jointCount": 400,
      "tripleCount": 150
    },
    "100": {
      "rawHit": 4,
      "jointHit": 4,
      "tripleHit": 2,
      "rawCount": 800,
      "jointCount": 800,
      "tripleCount": 300
    }
  },
  "roleMiss": [],
  "conditionTurns": 8,
  "controls": 4,
  "authority": "NONE"
}
```
## 后续与限制
如果联合排序损失覆盖或排名无改善，保留负面结果，不围绕4例继续调权重。需要外部合法开发语料及独立留出、真实主体/条件方向/事件身份/修订效果连接；优先从真实原生入口核对语义义务及不能安全计算的出口。研究者选择精确共跨度、评分加和、预算、历史夹具，尚无完整负例精度或资源测量，不声称语言泛化。未修改正式生产、唯一交接、冻结及历史证据等级，未启动新Codex任务、训练、合并、部署、主动CI或新增费用。
## 可执行复算
Node标准JS，以下包装按固定顺序读九文件并核对Git blob（包装未单独运行），核心experiment实际在连接器JS执行。
```js
const fs=require("node:fs"),crypto=require("node:crypto"),expected=["be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb","05c239f3f3b1f46235fa2464d2945c21c6c08132","bbdc12dfe65b24aa24e6b1d25a04955766cadab4","16075b3ba567ee6dc3496300beab1417172a6c42","07dcbda9532dbc3b330abfd79a399cb52aa91aeb","8a6b42f83b80283db6e215fe48f4fb2efbf8368c","b0bea7b4c101c170be2aaa2355973739b125e0b7","ef103587b216ad07c1a47102ddb7cb8d2975283d","81df7d2fc56f29084ecc623b98cdf0991d3260d4"],buffers=process.argv.slice(2).map(p=>fs.readFileSync(p));
if(buffers.length!==expected.length||buffers.some((b,i)=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex")!==expected[i]))throw Error("asset identity");
function experiment(contents){
 const ck=(v,m)=>{if(!v)throw Error(m)},code=i=>contents[i].split("```js\n")[1].split("\n```")[0],docs=contents.slice(0,2).map(JSON.parse);
 const P=Function("input",code(7).split(" const out={episodes:")[0]+"\nreturn {propose};\n}\nreturn experiment(input);")(contents.slice(0,7));
 const S=Function(code(2).split(" const blank=()=>")[0]+"\nreturn {scan};\n}\nreturn experiment();")();
 const graph=Function("S",code(8).slice(code(8).indexOf("function experiment(I,S,corpora,assets)")).split(" const out={turns:")[0]+"\nreturn graph;\n}\nreturn experiment(null,S,null,null);")(S);
 const roles=["constraint","action","revision"],key=x=>x.start+":"+x.end,same=(a,b)=>key(a)===key(b),K=[5,10,20,50,100],rank=(a,b)=>b.score-a.score||a.id.localeCompare(b.id),ch=s=>new Set([...s].filter(c=>!/[\p{P}\s]/u.test(c))),grams=s=>{let a=[...s];return new Set(a.slice(1).map((v,i)=>a[i]+v).filter(v=>!/[\p{P}\s]/u.test(v)))},jac=(a,b)=>{let k=0;for(let x of a)if(b.has(x))k++;return k/(a.size+b.size-k||1)},sim=(a,b)=>jac(ch(a),ch(b))+jac(grams(a),grams(b));
 function candidates(text,prior,history){
  let g=graph(text),p=P.propose(text,prior);ck(g.status==="CANDIDATES_ONLY","graph limit");
  let maps=Object.fromEntries(roles.map(r=>[r,new Map(p.all[r].map(v=>[key(v),v]))])),joint=[],triples=[];
  for(let e of g.edges)for(let r of roles){let a=maps[r].get(key(e.target));if(!a)continue;let id=key(e.guard)+"/"+key(e.target)+"/"+r;
   joint.push({id,e,r,score:e.score+a.score,roleScore:a.score,authority:"NONE",outside:true});
   if(r==="revision")for(let h of history){let v=sim(e.target.text,h.quote);triples.push({id:id+"/"+h.id,e,r,ref:h.id,score:e.score+a.score+4*v,authority:"NONE",outside:true})}
  }
  joint.sort(rank);triples.sort(rank);return {g,p,joint,triples}
 }
 let out={turns:0,edges:0,joint:0,triples:0,conditionTargets:0,rawExact:0,roleExact:0,jointExact:0,revisionTargets:0,tripleExact:0,rows:[],budgets:Object.fromEntries(K.map(k=>[k,{rawHit:0,jointHit:0,tripleHit:0,rawCount:0,jointCount:0,tripleCount:0}])),roleMiss:[],conditionTurns:0,controls:0,authority:"NONE"};
 for(let d=0;d<2;d++)for(let ep of docs[d].cases)for(let ti=0;ti<ep.turns.length;ti++){let t=ep.turns[ti],hist=ti?(d?ep.turns[0].proposal.claims.map((x,i)=>({id:ep.id+".1."+(i+1),quote:x.quote})):ep.turns[0].claims.map(x=>({id:ep.id+":t0:"+x.field,quote:x.span}))):[],z=candidates(t.text,!!ti,hist);
  out.turns++;out.edges+=z.g.edges.length;out.joint+=z.joint.length;out.triples+=z.triples.length;out.conditionTurns+=+(z.g.edges.length>0);
  for(let k of K){let b=out.budgets[k];b.rawCount+=Math.min(k,z.g.edges.length);b.jointCount+=Math.min(k,z.joint.length);b.tripleCount+=Math.min(k,z.triples.length)}
  for(let a of d?t.proposal.claims:[]){if(!a.condition)continue;let st=t.text.indexOf(a.quote),gs=t.text.indexOf(a.condition);ck(st>=0&&gs>=0&&st===t.text.lastIndexOf(a.quote)&&gs===t.text.lastIndexOf(a.condition),"anchor");let target={start:st,end:st+a.quote.length},guard={start:gs,end:gs+a.condition.length},match=e=>same(e.target,target)&&same(e.guard,guard),role=a.role;
   ck(roles.includes(role),"role");out.conditionTargets++;let raw=z.g.edges.findIndex(match)+1,rr=z.p.all[role].findIndex(v=>same(v,target))+1,jr=z.joint.findIndex(v=>v.r===role&&match(v.e))+1,tr=a.ref?z.triples.findIndex(v=>v.ref===a.ref&&match(v.e))+1:null;
   out.rawExact+=+!!raw;out.roleExact+=+!!rr;out.jointExact+=+!!jr;if(a.ref){out.revisionTargets++;out.tripleExact+=+!!tr}
   for(let k of K){let b=out.budgets[k];b.rawHit+=+(raw>0&&raw<=k);b.jointHit+=+(jr>0&&jr<=k);b.tripleHit+=+(tr>0&&tr<=k)}
   let row={episode:ep.id,role,guard:a.condition,target:a.quote,ref:a.ref,rawRank:raw||null,roleRank:rr||null,jointRank:jr||null,tripleRank:tr||null,rawEdges:z.g.edges.length,jointCount:z.joint.length,tripleCount:z.triples.length};out.rows.push(row);if(!rr)out.roleMiss.push(row)
  }
  ck(z.joint.every(v=>v.authority==="NONE"&&v.outside&&t.text.slice(v.e.target.start,v.e.target.end)===v.e.target.text),"joint identity");ck(z.triples.every(v=>hist.some(h=>h.id===v.ref)),"history identity")
 }
 ck(out.turns===64&&out.conditionTargets===4&&out.revisionTargets===2,"fixed cohort");ck(out.jointExact<=Math.min(out.rawExact,out.roleExact),"join coverage");out.controls+=2;
 let a=candidates("如果下雨。明天取消",true,[{id:"A",quote:"明天取消"}]);ck(a.joint.every(v=>!v.e.target.text.includes("明天")),"strong boundary");out.controls++;
 let b=candidates("如果下雨，明天取消",true,[{id:"A",quote:"明天活动"},{id:"B",quote:"明天活动"}]);for(let x of b.triples.filter(v=>v.ref==="A"))ck(b.triples.some(v=>v.ref==="B"&&same(v.e.guard,x.e.guard)&&same(v.e.target,x.e.target)&&v.score===x.score),"distinct roots");ck(b.triples.length>0,"positive control");out.controls++;
 return out
}
console.log(JSON.stringify(experiment(buffers.map(b=>b.toString("utf8"))),null,2));
```
