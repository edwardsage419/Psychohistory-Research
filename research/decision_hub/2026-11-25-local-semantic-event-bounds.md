# 自主认知专项累计第90轮候选：局部语义事件有证区间与密集候选结构偏差诊断

2026-11-25。RESEARCH_CANDIDATE / LOCAL_EVENT_BOUNDS_EXECUTED / RAW_BOTH_SIDES / STRUCTURAL_DIAGNOSTIC / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。main abb5fda5dfbb65b9c29a3efbe55d0826c1a1833d。核查近20提交、13开放PR（#61待审）、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R89首21行。新增范围：保留R89无监督全图、正权重与相邻因子，绕过全分区宽界直接求局部事件有证区间，诊断模型结构本身的质量偏置。非真实语言模型训练或科学方法准入。

## 固定输入
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
实际完整读取并核对blob。32情节64轮167标注，原创合成公开开发资料（ChatGPT研发辅助），非真人、独立留出或获授权训练。沿R89两侧全部不含标点/空白的1..24码点跨度、一元1+长度mod3、边1+共享字符二元组、相邻当前节点同时存在乘2、历史节点独立一元；当前节点最多一个引用，NO_LINK/OUTSIDE单位边权。小图使用给定标注跨度，不施加监督；扩展图不使用标签生成或计算，只在事后标记原文起止。所有正密边均保留；不是已资格的语义关系。未标注候选不能视作负例，标注也不等于真人语义真值。模型内概率不能解释为实际意图、真实引用概率或安全置信度。

## 推导
固定当前节点j为ABSENT，归一化其余历史存在X及当前存在Y的权重得到Q0；令L_j=2+Σe_ji X_i，C=2^{Y_{j-1}+Y_{j+1}}（不存在的邻居省略），T=E_Q0 C，M=E_Q0 CL_j，Lbar=M/T。当前节点存在相对缺失的赔率为b_j T Lbar；NO_LINK和OUTSIDE各为b_j T，任意域内LINK合计b_j T(Lbar-2)。将赔率除以1+b_j T Lbar得到存在、单个OUTSIDE和任意LINK边际，条件于存在的LINK为1-2/Lbar。此等式仅适用R89的固定有限结构。
在给定X及其他当前节点时，任一邻居k的存在赔率至少2b_k，故其存在概率至少2b_k/(1+2b_k)，用迭代条件期望得T≥∏_{邻居}(1+4b_k)/(1+2b_k)，且T≤2^{邻居数}。Lbar是以C加权的缺失图中L_j期望；积分其余当前节点后，历史独立先验被非负坐标单调多项式重新加权（所有边与系数非负），由R89单调关联E_prior[X_i W]≥E_prior[X_i]E_prior[W]，故Lbar≥2+Σe_ji a_i/(1+a_i)，且≤2+Σe_ji。对T、Lbar各自单调的事件公式取适当端点：存在与任意LINK随两者增加；OUTSIDE随T增加、Lbar减少；条件LINK随Lbar增加。全部区间采用BigInt有理交叉乘，只有展示宽度转为浮点。没有假设两个区间端点可同时达到，不声称最紧界。复杂度主要O(nm)，不构建完整赋值或分区；本实现仍生成密边矩阵、未做真实运行时间、内存、能耗或全请求预算控制，不是生产资源证明。所有返回authority NONE及outsideDomain true。有限图高分不提供任何真实执行权限。

## 实验与解释
512个3×3稀疏资格夹具（0边仅在该人工图允许）、32仓库oracle小图，独立直接枚举历史与当前存在掩码，每个存在节点的单OUTSIDE权重为该赋值质量除L_j，任意LINK为其余质量；核对四事件区间包含。同一研究者构造、非独立科学验收。扩展双侧原文图只能依据推导、小图核验及区间有效性，未穷举。0.9/0.99为研究者选定诊断阈值，使用精确有理比较；阈值通过仅指模型内下界达到该值，不是用户准入、模型准确率或证据等级。统计标注起止内/未标注候选分开；未标注候选高权重揭示结构倾向与候选泛滥风险，不能计为误报。历史候选越多，L_j会因每条边至少1而机械增加；这暴露任意示例权重、未归一候选多重性及正共现因素的结构偏置，不能把计算区间收窄解释为自主语义理解进步。没有新增外部资料，12项控制，未训练、未拟合、未选最终模型、未运行原生平台、真机或真人、无Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。保留R50完整范围及正式验收门。

## 可复算代码
按L/S顺序加载固定JSON并执行。
```js
function experiment(docs){
 const ck=(v,m)=>{if(!v)throw Error(m)},F=(n,d=1n)=>[n,d],mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),sub=(a,b)=>F(a[0]*b[1]-b[0]*a[1],a[1]*b[1]),div=(a,b)=>F(a[0]*b[1],a[1]*b[0]),le=(a,b)=>a[0]*b[1]<=b[0]*a[1],num=a=>Number(a[0])/Number(a[1]);
 const grams=q=>{let a=[...q];return new Set(a.slice(0,-1).map((c,i)=>c+a[i+1]))},u=q=>BigInt(1+[...q].length%3);
 function graph(a,b){let x=a.map(grams),y=b.map(grams);return {a:a.map(u),b:b.map(u),e:y.map(v=>x.map(w=>1n+BigInt([...v].filter(k=>w.has(k)).length)))}}
 function raw(t){let a=[...t],q=[];for(let i=0;i<a.length;i++)for(let j=i+1;j<=Math.min(i+24,a.length);j++){if(/[\p{P}\p{Z}\s]/u.test(a[j-1]))break;q.push({i,j,q:a.slice(i,j).join("")})}return q}
 const one=F(1n),two=F(2n),events=["present","outside","link","linkGivenPresent"];
 function local(g,j){
  let row=g.e[j],b=F(g.b[j]),mean=F(24n+row.reduce((s,e,i)=>s+e*g.a[i]*(12n/(1n+g.a[i])),0n),12n),max=F(2n+row.reduce((s,e)=>s+e,0n));
  let ns=[j-1,j+1].filter(k=>k>=0&&k<g.b.length),tlo=one,thi=F(2n**BigInt(ns.length));
  for(let k of ns)tlo=mul(tlo,F(1n+4n*g.b[k],1n+2n*g.b[k]));
  // T = E[C | node absent], Lbar = E[C L | absent]/T.
  const den=(t,l)=>add(one,mul(mul(b,t),l));
  const present=(t,l)=>div(mul(mul(b,t),l),den(t,l));
  const outside=(t,l)=>div(mul(b,t),den(t,l));
  const link=(t,l)=>div(mul(mul(b,t),sub(l,two)),den(t,l));
  const cond=l=>sub(one,div(two,l));
  return {present:[present(tlo,mean),present(thi,max)],outside:[outside(tlo,max),outside(thi,mean)],link:[link(tlo,mean),link(thi,max)],linkGivenPresent:[cond(mean),cond(max)],basePresent:[present(one,two),present(thi,max)],baseLinkGivenPresent:[F(0n),cond(max)],authority:"NONE",outsideDomain:true};
 }
 function exact(g){
  let n=g.a.length,m=g.b.length,z=0n,p=Array(m).fill(0n),o=Array(m).fill(0n);
  ck(n<=10&&m<=10,"oracle cap");
  for(let h=0;h<2**n;h++){
   let a=1n;for(let i=0;i<n;i++)if(h&(1<<i))a*=g.a[i];
   let L=g.e.map(row=>2n+row.reduce((s,e,i)=>s+((h&(1<<i))?e:0n),0n));
   for(let s=0;s<2**m;s++){let w=a;for(let j=0;j<m;j++)if(s&(1<<j)){w*=g.b[j]*L[j];if(j&&(s&(1<<(j-1))))w*=2n}z+=w;
    for(let j=0;j<m;j++)if(s&(1<<j)){p[j]+=w;ck(w%L[j]===0n,"integer");o[j]+=w/L[j]}
   }
  }return p.map((v,j)=>({present:F(v,z),outside:F(o[j],z),link:F(v-2n*o[j],z),linkGivenPresent:F(v-2n*o[j],v)}));
 }
 let out={syntheticGraphs:0,syntheticChecks:0,smallEpisodes:0,smallChecks:0,rawEpisodes:0,rawNodes:0,rawPairs:0,rawMarkedCovered:0,rawMarkedTotal:0,rawUnmarkedCandidates:0,thresholds:{"0.9":{}, "0.99":{}},intervals:{},controls:0,records:[]};
 let widths=Object.fromEntries(events.map(e=>[e,[]]));
 for(let t of Object.values(out.thresholds))for(let e of ["present","linkGivenPresent"])t[e]={all:0,marked:0,unmarked:0,unknown:0};
 function verify(g,k){let a=exact(g);for(let j=0;j<g.b.length;j++){let b=local(g,j);for(let e of events){ck(le(b[e][0],a[j][e])&&le(a[j][e],b[e][1]),"containment "+e);out[k+"Checks"]++}ck(le(b.basePresent[0],b.present[0])&&le(b.baseLinkGivenPresent[0],b.linkGivenPresent[0]),"improve")}}
 for(let mask=0;mask<512;mask++){let g={a:[1n,2n,3n],b:[2n,1n,3n],e:Array.from({length:3},(_,j)=>Array.from({length:3},(_,i)=>mask&(1<<(3*j+i))?BigInt(1+(i+j)%3):0n))};verify(g,"synthetic");out.syntheticGraphs++}
 for(let d=0;d<docs.length;d++)for(let ep of docs[d].cases){
  let [ta,tb]=ep.turns,aa=d===0?ta.claims:ta.proposal.claims,bb=d===0?tb.claims:tb.proposal.claims,quote=c=>d===0?c.span:c.quote;verify(graph(aa.map(quote),bb.map(quote)),"small");out.smallEpisodes++;
  let A=raw(ta.text),B=raw(tb.text),marked=new Set();for(let c of bb){let q=quote(c),at=tb.text.indexOf(q);ck(at>=0&&at===tb.text.lastIndexOf(q),"anchor");let i=[...tb.text.slice(0,at)].length,j=i+[...q].length,k=B.findIndex(x=>x.i===i&&x.j===j);out.rawMarkedTotal++;if(k>=0)marked.add(k)}
  let g=graph(A.map(x=>x.q),B.map(x=>x.q));out.rawEpisodes++;out.rawNodes+=B.length;out.rawPairs+=A.length*B.length;out.rawMarkedCovered+=marked.size;out.rawUnmarkedCandidates+=B.length-marked.size;
  let rec={id:ep.id,n:A.length,m:B.length,marked:marked.size,certifiedPresent99:0,certifiedLinkGivenPresent99:0};
  for(let j=0;j<B.length;j++){let b=local(g,j);ck(b.authority==="NONE"&&b.outsideDomain,"authority");for(let e of events){ck(le(F(0n),b[e][0])&&le(b[e][0],b[e][1])&&le(b[e][1],one),"valid interval");widths[e].push(num(b[e][1])-num(b[e][0]))}
   for(let [name,t] of [["0.9",F(9n,10n)],["0.99",F(99n,100n)]])for(let e of ["present","linkGivenPresent"]){
    let s=out.thresholds[name][e];if(le(t,b[e][0])){s.all++;s[marked.has(j)?"marked":"unmarked"]++;if(name==="0.99")rec[e==="present"?"certifiedPresent99":"certifiedLinkGivenPresent99"]++}
    else if(le(t,b[e][1]))s.unknown++;
   }
  }out.records.push(rec)
 }
 for(let e of events){let a=widths[e].sort((x,y)=>x-y);out.intervals[e]={min:a[0],median:(a[Math.floor((a.length-1)/2)]+a[Math.floor(a.length/2)])/2,max:a.at(-1)}}
 for(let t of [()=>out.syntheticGraphs===512,()=>out.syntheticChecks===6144,()=>out.smallEpisodes===32,()=>out.smallChecks===228,()=>out.rawEpisodes===32,()=>out.rawNodes===3074,()=>out.rawPairs===544737,()=>out.rawMarkedCovered===57&&out.rawMarkedTotal===57,()=>out.rawUnmarkedCandidates===3017,()=>Object.values(out.thresholds).every(t=>Object.values(t).every(x=>x.all===x.marked+x.unmarked&&x.all+x.unknown<=out.rawNodes)),()=>le(local({a:[],b:[1n],e:[[]]},0).present[0],F(2n,3n))&&le(F(2n,3n),local({a:[],b:[1n],e:[[]]},0).present[1]),()=>le(local({a:[],b:[1n],e:[[]]},0).link[1],F(0n))]){ck(t(),"control");out.controls++}
 return out;
}
```

## 实测
```json
{
  "syntheticGraphs": 512,
  "syntheticChecks": 6144,
  "smallEpisodes": 32,
  "smallChecks": 228,
  "rawEpisodes": 32,
  "rawNodes": 3074,
  "rawPairs": 544737,
  "rawMarkedCovered": 57,
  "rawMarkedTotal": 57,
  "rawUnmarkedCandidates": 3017,
  "thresholds": {
    "0.9": {
      "present": {
        "all": 3074,
        "marked": 57,
        "unmarked": 3017,
        "unknown": 0
      },
      "linkGivenPresent": {
        "all": 3074,
        "marked": 57,
        "unmarked": 3017,
        "unknown": 0
      }
    },
    "0.99": {
      "present": {
        "all": 3074,
        "marked": 57,
        "unmarked": 3017,
        "unknown": 0
      },
      "linkGivenPresent": {
        "all": 197,
        "marked": 3,
        "unmarked": 194,
        "unknown": 745
      }
    }
  },
  "intervals": {
    "present": {
      "min": 0.00013683844869782913,
      "median": 0.0006711827665147885,
      "max": 0.0026294816307103064
    },
    "outside": {
      "min": 0.000988562910706162,
      "median": 0.0030304852420292142,
      "max": 0.0066960246124147926
    },
    "link": {
      "min": 0.0021148537328196104,
      "median": 0.0070210438237579,
      "max": 0.015900311043712145
    },
    "linkGivenPresent": {
      "min": 0.0019790734852901393,
      "median": 0.006066701006483655,
      "max": 0.013419309864064144
    }
  },
  "controls": 12,
  "records": [
    {
      "id": "L01",
      "n": 133,
      "m": 55,
      "marked": 1,
      "certifiedPresent99": 55,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L02",
      "n": 137,
      "m": 110,
      "marked": 2,
      "certifiedPresent99": 110,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L03",
      "n": 128,
      "m": 91,
      "marked": 1,
      "certifiedPresent99": 91,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L04",
      "n": 156,
      "m": 90,
      "marked": 2,
      "certifiedPresent99": 90,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L05",
      "n": 152,
      "m": 157,
      "marked": 2,
      "certifiedPresent99": 157,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L06",
      "n": 178,
      "m": 70,
      "marked": 2,
      "certifiedPresent99": 70,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L07",
      "n": 366,
      "m": 196,
      "marked": 2,
      "certifiedPresent99": 196,
      "certifiedLinkGivenPresent99": 196
    },
    {
      "id": "L08",
      "n": 152,
      "m": 133,
      "marked": 2,
      "certifiedPresent99": 133,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L09",
      "n": 139,
      "m": 133,
      "marked": 3,
      "certifiedPresent99": 133,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L10",
      "n": 187,
      "m": 39,
      "marked": 1,
      "certifiedPresent99": 39,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L11",
      "n": 185,
      "m": 65,
      "marked": 2,
      "certifiedPresent99": 65,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L12",
      "n": 127,
      "m": 67,
      "marked": 2,
      "certifiedPresent99": 67,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L13",
      "n": 156,
      "m": 120,
      "marked": 2,
      "certifiedPresent99": 120,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L14",
      "n": 184,
      "m": 57,
      "marked": 2,
      "certifiedPresent99": 57,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L15",
      "n": 137,
      "m": 99,
      "marked": 2,
      "certifiedPresent99": 99,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L16",
      "n": 248,
      "m": 65,
      "marked": 2,
      "certifiedPresent99": 65,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L17",
      "n": 222,
      "m": 127,
      "marked": 3,
      "certifiedPresent99": 127,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "L18",
      "n": 85,
      "m": 79,
      "marked": 3,
      "certifiedPresent99": 79,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S01",
      "n": 205,
      "m": 83,
      "marked": 2,
      "certifiedPresent99": 83,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S02",
      "n": 226,
      "m": 76,
      "marked": 1,
      "certifiedPresent99": 76,
      "certifiedLinkGivenPresent99": 1
    },
    {
      "id": "S03",
      "n": 108,
      "m": 64,
      "marked": 1,
      "certifiedPresent99": 64,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S04",
      "n": 177,
      "m": 91,
      "marked": 1,
      "certifiedPresent99": 91,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S05",
      "n": 210,
      "m": 91,
      "marked": 1,
      "certifiedPresent99": 91,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S06",
      "n": 133,
      "m": 66,
      "marked": 2,
      "certifiedPresent99": 66,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S07",
      "n": 208,
      "m": 102,
      "marked": 2,
      "certifiedPresent99": 102,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S08",
      "n": 138,
      "m": 49,
      "marked": 1,
      "certifiedPresent99": 49,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S09",
      "n": 188,
      "m": 83,
      "marked": 1,
      "certifiedPresent99": 83,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S10",
      "n": 180,
      "m": 141,
      "marked": 2,
      "certifiedPresent99": 141,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S11",
      "n": 74,
      "m": 133,
      "marked": 2,
      "certifiedPresent99": 133,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S12",
      "n": 136,
      "m": 64,
      "marked": 2,
      "certifiedPresent99": 64,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S13",
      "n": 175,
      "m": 157,
      "marked": 2,
      "certifiedPresent99": 157,
      "certifiedLinkGivenPresent99": 0
    },
    {
      "id": "S14",
      "n": 233,
      "m": 121,
      "marked": 1,
      "certifiedPresent99": 121,
      "certifiedLinkGivenPresent99": 0
    }
  ]
}
```

## 后续
优先研究候选集合增广、重复或等价候选时的质量守恒及模型不变性，显式分离存在性、引用强度、域外未知与可信义务。未经证据不能通过任意删边、归一化或调权声称解决真实语义问题。数据轨、独立验收轨及产品轨责任不变；训练与工程另获授权。
