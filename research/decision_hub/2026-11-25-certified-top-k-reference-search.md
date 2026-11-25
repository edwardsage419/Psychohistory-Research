# v3.2 自主认知专项第19轮后续：精确有界引用候选 Top-K 搜索

2026-11-25。RESEARCH_CANDIDATE / FIXED_SCORE_SEARCH_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线 main 849a5bc3db4f95962c79055a6d8ddbf0631fec4c。核查 v3.2、AGENTS、同步规程、近期50提交、开放PR列表前10项、唯一交接首35行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07，非全文）、R76与R77方法和R78资源结论。R77完整原文边首位仅3/12、前100为10/12，bridge一例触及200000预算。本轮不重复训练或排序设计，检验保持固定评分和同分次序的精确截尾搜索。K=20/100为研究者选择，200000为访问预算沿用旧数量级但计数口径改变；不代表产品门槛。

输入：research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb；research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132。两文件全文实际获取并核对blob，32合成公开开发情节、12明确引用，ChatGPT研发辅助，非真人/独立留出，未训练。R77原跨度、词面相似度与修订词评分保持；原文候选生成后才使用标注评估。R77旧全边上限不适用于本轮离线穷举参照，单独报告本轮算法实际访问预算。无新增外部资料或事实。

## 证明与边界
分数 s=a.score+b.score+4J+2cue，J为集合Jaccard。令 b 按 b.score+2cue 降序遍历；J≤1，因此当行内 base+4 严格小于当前第K项分数时，当前及后续整行尾均不能进入前K。J≤min(|A|,|B|)/max(|A|,|B|)，使用额外安全余量1e-12的单边界。严格小于才能剪枝，分数相等仍需按位置比较；当前第K分数单调不降。只有所有未访问尾和跳过项均有界证明时返回 EXACT_TOP_K；访问超预算则 LIMIT，清空候选，不冒充完整。该证书仅针对已生成跨度、固定评分和K，不能保证语义真值、候选全集、概率校准或更正授权。候选权限始终NONE。最坏仍O(NM)，有序前K数组插入O(K)，空间O(N+M+K)（不含输入与穷举参照），未实测设备时间或峰值内存。访问数包含行尾界检查，评分数仅实际Jaccard。两种精确路径同一研究者执行，非独立科学验收。无训练、生产修改、Codex、CI、合并、部署、费用或冻结变更。

## 复算
将固定JSON按L/S顺序作为docs，运行以下标准JS函数。穷举仅研究参照，非产品路径。

```js
function experiment(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)},punct=/[，。！？；、：,.!?;:\s]/u,connect=["或者","还是","但是","如果","而且","以及","然后","并且","就","且","和","或","再"],revision=["改","撤","取消","替换","不再","重新","刚核实","实际是","暂时不","仅用于","不作为","纠正","更新"];
 function spans(s,bridge){
  if(typeof s!=="string"||s.length>128||!s.length)throw Error("invalid text");
  let out=[];
  for(let i=0;i<s.length;i++)if(!punct.test(s[i]))for(let j=i+1;j<=Math.min(s.length,i+24);j++){
   let x=s.slice(i,j),p=[...x].filter(v=>punct.test(v)).length;
   if(p>(bridge?1:0))break;
   if(punct.test(s[j-1]))continue;
   let left=i===0||punct.test(s[i-1])||connect.some(v=>s.slice(0,i).endsWith(v)),right=j===s.length||punct.test(s[j])||connect.some(v=>s.startsWith(v,j));
   out.push({start:i,end:j,score:3*(+left+ +right)-Math.abs(x.length-8)/4-2*p,cue:revision.some(v=>x.includes(v)),chars:new Set([...x].filter(v=>!punct.test(v)))});
  }return out.sort((a,b)=>b.score-a.score||a.start-b.start||a.end-b.end)
 }
 const jac=(a,b)=>{let n=0;for(const x of a.chars)if(b.chars.has(x))n++;return n/(a.chars.size+b.chars.size-n||1)};
 const score=(a,b)=>a.score+b.score+4*jac(a,b)+2*Number(b.cue);
 const cmp=(x,y)=>y.score-x.score||x.a.start-y.a.start||x.a.end-y.a.end||x.b.start-y.b.start||x.b.end-y.b.end;
 const key=e=>[e.a.start,e.a.end,e.b.start,e.b.end,e.score].join(":");
 function baseline(a,b,k){let all=[];for(const u of a)for(const v of b)all.push({a:u,b:v,score:score(u,v)});return all.sort(cmp).slice(0,k)}
 function optimized(a,b,k,cap=200000){
  let order=b.slice().sort((x,y)=>(y.score+2*Number(y.cue))-(x.score+2*Number(x.cue))||x.start-y.start||x.end-y.end),top=[],visits=0,scored=0,skippedTail=0,skippedSize=0;
  for(const u of a)for(let j=0;j<order.length;j++){
   let v=order[j],base=u.score+v.score+2*Number(v.cue),cut=top.length===k?top[k-1].score:-Infinity;
   if(++visits>cap)return {status:"LIMIT",top:[],visits:visits-1,scored,skippedTail,skippedSize};
   if(base+4<cut){skippedTail+=order.length-j;break}
   let ratio=Math.min(u.chars.size,v.chars.size)/Math.max(u.chars.size,v.chars.size,1);
   if(base+4*ratio+1e-12<cut){skippedSize++;continue}
   scored++;let e={a:u,b:v,score:score(u,v)};
   if(top.length===k&&cmp(e,top[k-1])>=0)continue;
   let l=0,h=top.length;while(l<h){let m=(l+h)>>1;if(cmp(e,top[m])<0)h=m;else l=m+1}
   top.splice(l,0,e);if(top.length>k)top.pop();
  }
  ck(scored+skippedTail+skippedSize===a.length*b.length,"pair conservation");
  return {status:"EXACT_TOP_K",top,visits,scored,skippedTail,skippedSize};
 }
 let result={episodes:0,positiveEdges:0,controls:0,modes:{},limits:[]};
 const same=(u,v)=>u.length===v.length&&u.every((x,i)=>key(x)===key(v[i]));
 for(const bridge of [false,true])for(const k of [20,100])result.modes[`${bridge?"bridge":"raw"}_${k}`]={pairs:0,visits:0,scored:0,skippedTail:0,skippedSize:0,exactEpisodes:0,limited:0,expectedGold:0,foundGold:0,worstVisits:0,worstScored:0,oracleGold:0};
 for(let d=0;d<docs.length;d++)for(const e of docs[d].cases){
  result.episodes++;
  let [t0,t1]=e.turns,aa=d===0?t0.claims:t0.proposal.claims,bb=d===0?t1.claims:t1.proposal.claims,gs=[];
  const pos=(s,q)=>{let i=s.indexOf(q);ck(i>=0&&i===s.lastIndexOf(q),"unique span");return [i,i+q.length]};
  for(const cur of bb){let ref=d===0?cur.supersedes:cur.ref;if(typeof ref!=="string")continue;let prev;if(d===0){let m=/^([^:]+):t0:(.+)$/.exec(ref);ck(m&&m[1]===e.id,"ref");let z=aa.filter(x=>x.field===m[2]);ck(z.length===1,"unique field");prev=z[0]}else{let m=/^([^.]+)\.1\.(\d+)$/.exec(ref);ck(m&&m[1]===e.id,"ref");prev=aa[+m[2]-1]}gs.push([...pos(t0.text,d===0?prev.span:prev.quote),...pos(t1.text,d===0?cur.span:cur.quote)].join(":"))}
  result.positiveEdges+=gs.length;
  for(const bridge of [false,true]){
   let a=spans(t0.text,bridge),b=spans(t1.text,bridge),oracle=baseline(a,b,100);
   for(const k of [20,100]){
    let z=optimized(a,b,k),m=result.modes[`${bridge?"bridge":"raw"}_${k}`];
    m.pairs+=a.length*b.length;m.visits+=z.visits;m.scored+=z.scored;m.skippedTail+=z.skippedTail;m.skippedSize+=z.skippedSize;m.worstVisits=Math.max(m.worstVisits,z.visits);m.worstScored=Math.max(m.worstScored,z.scored);m.expectedGold+=gs.length;
    let keys=oracle.slice(0,k).map(x=>key(x).split(":").slice(0,4).join(":"));m.oracleGold+=gs.filter(g=>keys.includes(g)).length;
    if(z.status==="LIMIT"){m.limited++;result.limits.push([e.id,bridge,k]);continue}
    ck(same(z.top,oracle.slice(0,k)),"exact ranking "+e.id);m.exactEpisodes++;
    let actual=z.top.map(x=>key(x).split(":").slice(0,4).join(":"));m.foundGold+=gs.filter(g=>actual.includes(g)).length;
   }
  }
 }
 const a=spans("甲甲甲",false),b=spans("甲甲",false);
 for(const test of [()=>same(optimized(a,b,1).top,baseline(a,b,1)),()=>same(optimized(a,b,100).top,baseline(a,b,100)),()=>optimized(a,b,1,0).status==="LIMIT",()=>optimized(a,b,1,0).top.length===0,()=>optimized([],b,1).top.length===0,()=>result.episodes===32,()=>result.positiveEdges===12,()=>Object.values(result.modes).every(m=>m.exactEpisodes+m.limited===32),()=>Object.values(result.modes).every(m=>m.foundGold<=m.oracleGold),()=>Object.values(result.modes).filter(m=>!m.limited).every(m=>m.foundGold===m.oracleGold)]){ck(test(),"control");result.controls++}
 return result;
}
```

## 实际结果
```json
{
  "episodes": 32,
  "positiveEdges": 12,
  "controls": 10,
  "modes": {
    "raw_20": {
      "pairs": 544737,
      "visits": 26602,
      "scored": 8406,
      "skippedTail": 523577,
      "skippedSize": 12754,
      "exactEpisodes": 32,
      "limited": 0,
      "expectedGold": 12,
      "foundGold": 6,
      "worstVisits": 1835,
      "worstScored": 543,
      "oracleGold": 6
    },
    "raw_100": {
      "pairs": 544737,
      "visits": 64220,
      "scored": 24576,
      "skippedTail": 485859,
      "skippedSize": 34302,
      "exactEpisodes": 32,
      "limited": 0,
      "expectedGold": 12,
      "foundGold": 10,
      "worstVisits": 4468,
      "worstScored": 1263,
      "oracleGold": 10
    },
    "bridge_20": {
      "pairs": 2017385,
      "visits": 36479,
      "scored": 9845,
      "skippedTail": 1992392,
      "skippedSize": 15148,
      "exactEpisodes": 32,
      "limited": 0,
      "expectedGold": 12,
      "foundGold": 6,
      "worstVisits": 2162,
      "worstScored": 581,
      "oracleGold": 6
    },
    "bridge_100": {
      "pairs": 2017385,
      "visits": 83608,
      "scored": 30416,
      "skippedTail": 1945217,
      "skippedSize": 41752,
      "exactEpisodes": 32,
      "limited": 0,
      "expectedGold": 12,
      "foundGold": 10,
      "worstVisits": 5016,
      "worstScored": 1386,
      "oracleGold": 10
    }
  },
  "limits": []
}
```

## 后续责任
手动研究可继续测试可学习语义特征及联合图推理的候选召回与预算证书；不因计算优化提升语义证据等级。数据轨合法语料与隔离，独立轨真实留出、支持环境及手机资源验收，产品轨维护唯一交接。训练与完整工程版本均待所有者另行授权。保留R50完整十二项范围及正式验收门。
