# 自主认知：隐含集体指代的历史对象检索与成员覆盖边界
2026-11-27。RESEARCH_CANDIDATE / KNOWN_SPAN_DIAGNOSTIC / RECOMBINED_PUBLIC_SYNTHETIC_DEVELOPMENT / CONNECTOR_JS_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线与范围
起点main 5afd61d0367feaad832b73a23852a610ab63b7ed。核对20次近期提交、15开放PR、v3.2与同步规程全文、唯一交接前20行；#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。直接前序原子组压缩与引号锚研究（blob 9dcaaccdeed4aace81f264b1d7a196a0073c987e），相邻跨轮指代 da54c5b88ed0f19f5c5d272230a1959b811f5b5e、子集消元 edb9b9356c6607f7c2d6614aec3ad3051cd17736、主体转述框架 4c85af379a2f47b393a6bd070eab9cd4170786f5 各读前段。新增：去掉显式当前引号锚，比较历史对象对的结构检索，检查跨主题干扰及成员表示缺失。并非完整原文到语义组的解析；非全库无重复证明。

固定输入（实际读取完整JSON，连接器返回blob，未独立复算原始Git字节）：
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
32情节64轮，首轮110条标注记录为模拟历史；原文记录跨度、角色、部分单位和主体由原标注提供，不是真实已确认账本。研究者事后选择17个有明显并列/比较关系的对象对，既包含方案和目标，也包含不同角色的资源记录、相似报道与隐私约束；人工标注只用于本轮目标组召回，不能当完整组标注或确定联合操作。无独立样本，未以未标注对作负例。

## 方法
每个历史情节内枚举两个不同不重叠记录的组合，不生成跨情节的对象对。原文按Unicode标量位置，使用首次匹配的标注跨度（未对任意重复跨度作完整身份消歧）。排序评分4×明确连接词+2×弱边界+2×同角色族+2×同显式单位+2×同点号后字段+1×未跨强标点+1×主体兼容。最后一项把主体未知视为不排斥，不能用于确认权限。连接词仅为有限词表，不是句法完整识别；角色族人工映射，分数不是概率。比较最近提及基线、结构评分、人工提供查询目标类型优先再结构评分。第三策略使用已知类型而非从当前原文自动提取。L12跨角色资源组类型未指定。首轮单情节142候选对，17组选定目标；再将每个目标情节与其他31情节分别按两种时间顺序组合，总1054配置，当前查询类型仍人工给定；组合仅模拟候选干扰，不是真实连贯对话。候选池预先按情节分隔，真实主题识别、跨主题组、组成员数量大于二、群体匿名指代、角色及来源自动提取均未实现。

## 实测
| 方法 | 单情节Top1/2/3 (17) | 双主题Top1/2/3 (1054) |
| --- | --- | --- |
| 最近提及 | 4/4/9 | 124/135/290 |
| 结构 | 16/17/17 | 746/1006/1044 |
| 已知类型+结构 | 17/17/17 | 947/1054/1054 |

重复实际运行计数一致。结构方法S12相机两方案中间夹估计金额，正确组首位未命中，第二位命中，人工类型提高排序。双主题类型+结构最高同分（不计时间和稳定排序）154；同分含目标 154，同分不含目标 0；非同分正确 856，非同分错误 44。非同分错误证明仅检查并列仍不够，必须保留未知域和确认门；稳定排序或时间不能把候选变为语义事实。目标保留于前二不是完整语义覆盖保证。所有结果authority NONE。

## 成员表示缺口及原始对话
L12第二轮“对，两个都必须至少六万，不能挪到以后。”前轮已有kitchen,bathroom记录，最近基线目标排6，结构排1。原文确认每个最低60000、合计最多100000、不能借钱，若资格及同时适用成立，则120000>100000，条件性缺额20000。该数学反例已在旧语料，不作为本轮新数学模型或原生验证。
S14第二轮“对方是否有空还不清楚，所以这两种方式都先留着。”两方案前轮记录已存在，最近排6，结构排1；人工查询类型为action。保留两个候选不表示两个行动必须同时执行，且原第二轮标注只有对方是否有空的unknown，未直接编码保留两个对象的集合操作。此为人工覆盖审计，不是自动语言解析效果。
L05前轮“两家老人要照顾”只标注总假期、分配计划及后续调整，未分别标注两家照顾对象，第二轮“两个地方临时都可能需要七天”也只标注群体需求。不能把两条其他历史记录强行当作两个成员。成员人数可以作为候选基数，但不等同稳定成员身份；可能分别需要七天不保证同时需要，不能直接将14天需求作为事实，须保留联合情景的资格。S04两个人能用厨房也仅群体约束，无两个成员身份。下一步单独表示群体提及、成员集合候选、基数范围、群体身份来源、分配/聚合/排他/保留等关系类型、成员未枚举状态；在成员不完整时只允许确有资格且不依赖具体身份的局部推理，禁止逐项修订。上述为接口建议，尚未实现或验证。

## 复算函数
下面为第二次实际执行的完整函数，输入上述两个JSON解析所得数组。第一轮已输出全部行；第二轮增加最高结构同分与非同分错误分解。
```js
function study(docs){
 const check=(x,m)=>{if(!x)throw Error(m)};
 const gold={L02:[2,3],L08:[0,1],L11:[1,2],L12:[0,1],L15:[0,1],L18:[0,1],S01:[0,1],S02:[0,1],S03:[1,2],S04:[1,2],S05:[0,1],S07:[0,1],S09:[0,1],S10:[2,3],S12:[0,2],S13:[0,1],S14:[0,1]};
 const family=c=>c.role??(c.kind.includes("ACTION")?"action":c.kind.includes("ESTIMATE")?"estimate":c.kind.startsWith("REPORTED")?"reported":c.kind==="PREFERENCE"?"preference":c.kind==="GOAL"?"goal":c.kind==="HARD"?"constraint":c.kind);
 const eps=docs.flatMap(x=>x.cases).map(e=>{const t=e.turns[0];const chars=Array.from(t.text);const records=(t.claims??t.proposal.claims).map((c,i)=>{const raw=c.span??c.quote;let start=Array.from(t.text.slice(0,t.text.indexOf(raw))).length;check(t.text.includes(raw),"span missing");return {id:e.id+":"+i,raw,start,end:start+Array.from(raw).length,family:family(c),unit:c.unit??null,actor:c.actor??null,field:c.field??null}});return {id:e.id,chars,records,text:t.text,next:e.turns[1].text}});
 const key=(x,y)=>[x.id,y.id].sort().join("|");
 function pairs(e){const a=[];for(let i=0;i<e.records.length;i++)for(let j=i+1;j<e.records.length;j++){let x=e.records[i],y=e.records[j];if(x.start>y.start)[x,y]=[y,x];if(x.end>y.start)continue;const gap=e.chars.slice(x.end,y.start).join("");const weak=/^[，、\s]*(?:和|与|及|或者|还是|或|以及|一个是)?[，、\s]*$/u.test(gap);const explicit=/^(?:[，、\s]*)(?:和|与|及|或者|还是|或|以及|一个是)(?:[，、\s]*)$/u.test(gap);const clause=!/[。！？；]/u.test(gap);const family=x.family===y.family;const unit=x.unit!==null&&x.unit===y.unit;const actor=x.actor===null||y.actor===null||x.actor===y.actor;const field=x.field&&y.field&&x.field.includes(".")&&y.field.includes(".")&&x.field.split(".").slice(1).join(".")===y.field.split(".").slice(1).join(".");
 const score=4*Number(explicit)+2*Number(weak)+2*Number(family)+2*Number(unit)+2*Number(!!field)+Number(clause)+Number(actor);
 a.push({key:key(x,y),episode:e.id,ids:[x.id,y.id],start:x.start,end:y.end,score,gap,explicit,weak,family,unit,actor,field:!!field,families:[x.family,y.family]});
 }return a;}
 const order=(a,b)=>b.score-a.score||a.start-b.start||a.key.localeCompare(b.key);
 const closest=(a,b)=>b.end-a.end||b.start-a.start||a.key.localeCompare(b.key);
 const queryKind={L02:"reported",L08:"preference",L11:"estimate",L12:null,L15:"goal",L18:"constraint",S01:"action",S02:"action",S03:"action",S04:"action",S05:"action",S07:"criterion",S09:"action",S10:"action",S12:"action",S13:"criterion",S14:"action"};
 const result={episodes:eps.length,records:eps.reduce((n,e)=>n+e.records.length,0),pairs:0,annotatedPairs:Object.keys(gold).length,rows:[],top:{nearest:[0,0,0],structural:[0,0,0],typed:[0,0,0]},recombined:{cases:0,nearest:[0,0,0],structural:[0,0,0],typed:[0,0,0],typedTieTop:0,uniqueWrong:0,uniqueCorrect:0,tieContainsGold:0,tieMissesGold:0},actual:[],unrepresented:["L05: two care locations lack individual records","S04: two people lack individual records"],authority:"NONE"};
 function hit(rows,k,target){return rows.slice(0,k).some(x=>x.key===target)}
 const pool=Object.fromEntries(eps.map(e=>[e.id,pairs(e)]));
 const typed=(arr,f)=>[...arr].sort((a,b)=>((b.families.every(v=>v===f)?1:0)-(a.families.every(v=>v===f)?1:0))||order(a,b));
 for(const e of eps){const p=pool[e.id];result.pairs+=p.length;if(!gold[e.id])continue;const target=key(...gold[e.id].map(i=>e.records[i]));check(p.some(x=>x.key===target),"missing gold "+e.id);
 const ranks=[ [...p].sort(closest),[...p].sort(order),typed(p,queryKind[e.id])];const row={id:e.id,pairs:p.length,target,kind:queryKind[e.id],ranks:ranks.map(x=>1+x.findIndex(y=>y.key===target)),targetPair:p.find(x=>x.key===target),top:ranks.map(x=>x[0].key)};
 result.rows.push(row);
 for(let i=0;i<3;i++)for(const [j,k] of [1,2,3].entries())result.top[["nearest","structural","typed"][i]][j]+=Number(hit(ranks[i],k,target));
 for(const d of eps.filter(x=>x.id!==e.id))for(const older of [true,false]){
   const list=older?[...p.map(x=>({...x,age:1})),...pool[d.id].map(x=>({...x,age:0}))]:[...p.map(x=>({...x,age:0})),...pool[d.id].map(x=>({...x,age:1}))];
   const recent=[...list].sort((a,b)=>a.age-b.age||closest(a,b));
   const structural=[...list].sort((a,b)=>b.score-a.score||a.age-b.age||order(a,b));
   const f=queryKind[e.id],bonus=x=>f&&x.families.every(v=>v===f)?1:0;
   const contextual=[...list].sort((a,b)=>bonus(b)-bonus(a)||b.score-a.score||a.age-b.age||order(a,b));
   result.recombined.cases++;for(let i=0;i<3;i++)for(const [j,k] of [1,2,3].entries())result.recombined[["nearest","structural","typed"][i]][j]+=Number(hit([recent,structural,contextual][i],k,target));
   const max=contextual[0], tied=contextual.filter(x=>bonus(x)===bonus(max)&&x.score===max.score);
   if(tied.length>1){result.recombined.typedTieTop++;result.recombined[tied.some(x=>x.key===target)?"tieContainsGold":"tieMissesGold"]++;}
   else result.recombined[max.key===target?"uniqueCorrect":"uniqueWrong"]++;
   check(contextual.some(x=>x.key===target),"pool lost target");
 }
 if(["L12","S14"].includes(e.id))result.actual.push({id:e.id,next:e.next,rank:row.ranks});
 }
 return result;
}
```
结果（含所有17行）：
```json
{
  "episodes": 32,
  "records": 110,
  "pairs": 142,
  "annotatedPairs": 17,
  "rows": [
    {
      "id": "L02",
      "pairs": 6,
      "target": "L02:2|L02:3",
      "kind": "reported",
      "ranks": [
        1,
        1,
        1
      ],
      "targetPair": {
        "key": "L02:2|L02:3",
        "episode": "L02",
        "ids": [
          "L02:2",
          "L02:3"
        ],
        "start": 18,
        "end": 34,
        "score": 8,
        "gap": "，",
        "explicit": false,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": true,
        "families": [
          "reported",
          "reported"
        ]
      },
      "top": [
        "L02:2|L02:3",
        "L02:2|L02:3",
        "L02:2|L02:3"
      ]
    },
    {
      "id": "L08",
      "pairs": 3,
      "target": "L08:0|L08:1",
      "kind": "preference",
      "ranks": [
        3,
        1,
        1
      ],
      "targetPair": {
        "key": "L08:0|L08:1",
        "episode": "L08",
        "ids": [
          "L08:0",
          "L08:1"
        ],
        "start": 7,
        "end": 23,
        "score": 6,
        "gap": "，",
        "explicit": false,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "preference",
          "preference"
        ]
      },
      "top": [
        "L08:1|L08:2",
        "L08:0|L08:1",
        "L08:0|L08:1"
      ]
    },
    {
      "id": "L11",
      "pairs": 6,
      "target": "L11:1|L11:2",
      "kind": "estimate",
      "ranks": [
        4,
        1,
        1
      ],
      "targetPair": {
        "key": "L11:1|L11:2",
        "episode": "L11",
        "ids": [
          "L11:1",
          "L11:2"
        ],
        "start": 19,
        "end": 34,
        "score": 8,
        "gap": "，",
        "explicit": false,
        "weak": true,
        "family": true,
        "unit": true,
        "actor": true,
        "field": false,
        "families": [
          "estimate",
          "estimate"
        ]
      },
      "top": [
        "L11:2|L11:3",
        "L11:1|L11:2",
        "L11:1|L11:2"
      ]
    },
    {
      "id": "L12",
      "pairs": 6,
      "target": "L12:0|L12:1",
      "kind": null,
      "ranks": [
        6,
        1,
        1
      ],
      "targetPair": {
        "key": "L12:0|L12:1",
        "episode": "L12",
        "ids": [
          "L12:0",
          "L12:1"
        ],
        "start": 2,
        "end": 17,
        "score": 6,
        "gap": "，",
        "explicit": false,
        "weak": true,
        "family": false,
        "unit": true,
        "actor": true,
        "field": false,
        "families": [
          "preference",
          "reported"
        ]
      },
      "top": [
        "L12:2|L12:3",
        "L12:0|L12:1",
        "L12:0|L12:1"
      ]
    },
    {
      "id": "L15",
      "pairs": 6,
      "target": "L15:0|L15:1",
      "kind": "goal",
      "ranks": [
        6,
        1,
        1
      ],
      "targetPair": {
        "key": "L15:0|L15:1",
        "episode": "L15",
        "ids": [
          "L15:0",
          "L15:1"
        ],
        "start": 10,
        "end": 22,
        "score": 10,
        "gap": "，一个是",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "goal",
          "goal"
        ]
      },
      "top": [
        "L15:2|L15:3",
        "L15:0|L15:1",
        "L15:0|L15:1"
      ]
    },
    {
      "id": "L18",
      "pairs": 1,
      "target": "L18:0|L18:1",
      "kind": "constraint",
      "ranks": [
        1,
        1,
        1
      ],
      "targetPair": {
        "key": "L18:0|L18:1",
        "episode": "L18",
        "ids": [
          "L18:0",
          "L18:1"
        ],
        "start": 11,
        "end": 23,
        "score": 6,
        "gap": "，",
        "explicit": false,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "constraint",
          "constraint"
        ]
      },
      "top": [
        "L18:0|L18:1",
        "L18:0|L18:1",
        "L18:0|L18:1"
      ]
    },
    {
      "id": "S01",
      "pairs": 6,
      "target": "S01:0|S01:1",
      "kind": "action",
      "ranks": [
        6,
        1,
        1
      ],
      "targetPair": {
        "key": "S01:0|S01:1",
        "episode": "S01",
        "ids": [
          "S01:0",
          "S01:1"
        ],
        "start": 11,
        "end": 23,
        "score": 10,
        "gap": "或者",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S01:2|S01:3",
        "S01:0|S01:1",
        "S01:0|S01:1"
      ]
    },
    {
      "id": "S02",
      "pairs": 3,
      "target": "S02:0|S02:1",
      "kind": "action",
      "ranks": [
        3,
        1,
        1
      ],
      "targetPair": {
        "key": "S02:0|S02:1",
        "episode": "S02",
        "ids": [
          "S02:0",
          "S02:1"
        ],
        "start": 2,
        "end": 7,
        "score": 10,
        "gap": "和",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S02:1|S02:2",
        "S02:0|S02:1",
        "S02:0|S02:1"
      ]
    },
    {
      "id": "S03",
      "pairs": 3,
      "target": "S03:1|S03:2",
      "kind": "action",
      "ranks": [
        1,
        1,
        1
      ],
      "targetPair": {
        "key": "S03:1|S03:2",
        "episode": "S03",
        "ids": [
          "S03:1",
          "S03:2"
        ],
        "start": 9,
        "end": 26,
        "score": 10,
        "gap": "，或者",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S03:1|S03:2",
        "S03:1|S03:2",
        "S03:1|S03:2"
      ]
    },
    {
      "id": "S04",
      "pairs": 6,
      "target": "S04:1|S04:2",
      "kind": "action",
      "ranks": [
        4,
        1,
        1
      ],
      "targetPair": {
        "key": "S04:1|S04:2",
        "episode": "S04",
        "ids": [
          "S04:1",
          "S04:2"
        ],
        "start": 13,
        "end": 23,
        "score": 10,
        "gap": "或者",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S04:2|S04:3",
        "S04:1|S04:2",
        "S04:1|S04:2"
      ]
    },
    {
      "id": "S05",
      "pairs": 3,
      "target": "S05:0|S05:1",
      "kind": "action",
      "ranks": [
        3,
        1,
        1
      ],
      "targetPair": {
        "key": "S05:0|S05:1",
        "episode": "S05",
        "ids": [
          "S05:0",
          "S05:1"
        ],
        "start": 11,
        "end": 24,
        "score": 10,
        "gap": "还是",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S05:1|S05:2",
        "S05:0|S05:1",
        "S05:0|S05:1"
      ]
    },
    {
      "id": "S07",
      "pairs": 3,
      "target": "S07:0|S07:1",
      "kind": "criterion",
      "ranks": [
        3,
        1,
        1
      ],
      "targetPair": {
        "key": "S07:0|S07:1",
        "episode": "S07",
        "ids": [
          "S07:0",
          "S07:1"
        ],
        "start": 2,
        "end": 12,
        "score": 10,
        "gap": "和",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "criterion",
          "criterion"
        ]
      },
      "top": [
        "S07:1|S07:2",
        "S07:0|S07:1",
        "S07:0|S07:1"
      ]
    },
    {
      "id": "S09",
      "pairs": 6,
      "target": "S09:0|S09:1",
      "kind": "action",
      "ranks": [
        6,
        1,
        1
      ],
      "targetPair": {
        "key": "S09:0|S09:1",
        "episode": "S09",
        "ids": [
          "S09:0",
          "S09:1"
        ],
        "start": 3,
        "end": 12,
        "score": 10,
        "gap": "和",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S09:2|S09:3",
        "S09:0|S09:1",
        "S09:0|S09:1"
      ]
    },
    {
      "id": "S10",
      "pairs": 6,
      "target": "S10:2|S10:3",
      "kind": "action",
      "ranks": [
        1,
        1,
        1
      ],
      "targetPair": {
        "key": "S10:2|S10:3",
        "episode": "S10",
        "ids": [
          "S10:2",
          "S10:3"
        ],
        "start": 23,
        "end": 33,
        "score": 10,
        "gap": "或者",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S10:2|S10:3",
        "S10:2|S10:3",
        "S10:2|S10:3"
      ]
    },
    {
      "id": "S12",
      "pairs": 10,
      "target": "S12:0|S12:2",
      "kind": "action",
      "ranks": [
        9,
        2,
        1
      ],
      "targetPair": {
        "key": "S12:0|S12:2",
        "episode": "S12",
        "ids": [
          "S12:0",
          "S12:2"
        ],
        "start": 0,
        "end": 14,
        "score": 4,
        "gap": "大约五百，",
        "explicit": false,
        "weak": false,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S12:3|S12:4",
        "S12:0|S12:1",
        "S12:0|S12:2"
      ]
    },
    {
      "id": "S13",
      "pairs": 3,
      "target": "S13:0|S13:1",
      "kind": "criterion",
      "ranks": [
        3,
        1,
        1
      ],
      "targetPair": {
        "key": "S13:0|S13:1",
        "episode": "S13",
        "ids": [
          "S13:0",
          "S13:1"
        ],
        "start": 5,
        "end": 15,
        "score": 10,
        "gap": "和",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "criterion",
          "criterion"
        ]
      },
      "top": [
        "S13:1|S13:2",
        "S13:0|S13:1",
        "S13:0|S13:1"
      ]
    },
    {
      "id": "S14",
      "pairs": 6,
      "target": "S14:0|S14:1",
      "kind": "action",
      "ranks": [
        6,
        1,
        1
      ],
      "targetPair": {
        "key": "S14:0|S14:1",
        "episode": "S14",
        "ids": [
          "S14:0",
          "S14:1"
        ],
        "start": 4,
        "end": 19,
        "score": 10,
        "gap": "还是",
        "explicit": true,
        "weak": true,
        "family": true,
        "unit": false,
        "actor": true,
        "field": false,
        "families": [
          "action",
          "action"
        ]
      },
      "top": [
        "S14:2|S14:3",
        "S14:0|S14:1",
        "S14:0|S14:1"
      ]
    }
  ],
  "top": {
    "nearest": [
      4,
      4,
      9
    ],
    "structural": [
      16,
      17,
      17
    ],
    "typed": [
      17,
      17,
      17
    ]
  },
  "recombined": {
    "cases": 1054,
    "nearest": [
      124,
      135,
      290
    ],
    "structural": [
      746,
      1006,
      1044
    ],
    "typed": [
      947,
      1054,
      1054
    ],
    "typedTieTop": 154,
    "uniqueWrong": 44,
    "uniqueCorrect": 856,
    "tieContainsGold": 154,
    "tieMissesGold": 0
  },
  "actual": [
    {
      "id": "L12",
      "next": "对，两个都必须至少六万，不能挪到以后。",
      "rank": [
        6,
        1,
        1
      ]
    },
    {
      "id": "S14",
      "next": "对方是否有空还不清楚，所以这两种方式都先留着。",
      "rank": [
        6,
        1,
        1
      ]
    }
  ],
  "unrepresented": [
    "L05: two care locations lack individual records",
    "S04: two people lack individual records"
  ],
  "authority": "NONE"
}
```

## 限制
本轮自主选择人工目标、角色映射、评分、基线和重组方式，均未授权为产品规范。未做自动查询类型识别、原始多主题连续文本、独立未知覆盖、真实授权、实际用户澄清或设备性能评测。未运行完整v0.8、训练、修改生产、合并PR、部署、主动CI或新增费用；冻结、历史证据等级及唯一交接保持原样。
