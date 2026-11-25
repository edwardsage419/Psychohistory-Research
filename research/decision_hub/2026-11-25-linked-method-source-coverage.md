# 第52轮：登记方法来源覆盖、精确身份映射与关键数学边界复算
2026-11-25。固定 main ac8166ade98202694329a3ca9cf93f607c712d14，PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR及唯一交接 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第28/29/51轮。config blob 3a2d448caff63dedb9638aaef1eceaf6cd70bc5f，method_contracts blob 4ff1666907c362066dcef697d955bc6fb689b75c；第29轮基线baa5dc413b96ff3d0b742a193255fc2bbe727281至当前main的compare 50项变化、固定154份路径及7个模块无变化。实际读取七个原定模块并匹配身份，另读decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f；初次误把hub代替decision_v05导致清单匹配false，随后核对原清单、读取decision_v05（bc27cc42e4a8224c86c3113d044a328ae5eeba3e）完成7/7核对。没有源码动态执行。 
## 正文覆盖
新增8份此前第28/29/51轮未处理的真实方法档案，先读正文审查，再base64读取原始字节，按第51轮SHA1与UTF8往返方法实测，8/8与固定Git blob及大小一致，31440字节、6056词项（同原分词），12条已登记链接。历史累计40/154（26份登记关联文档全部已历轮处理；本轮8份原字节核验，其余沿用历史等级，非40份同时全文索引）。余114份主要非直接登记关联档案待处理。未重新审原始外部论文、许可、真实效应或全部历史正文。不重新计算已有第29轮源关系作为新发现。 
## 方法链接与边界
15个登记方法，26份关联文件，38条正反向映射完全一致，37条历史来源身份MATCH、1条CHANGED。timing_actions@1.0.0因Buehler原基线b611c66afbdeb862353dbad7330916afc57ac45e与当前e7e1002f00aab5bf782a5f2845fbfac2cb80969b不同，保留REVIEW_REQUIRED；即使检索其他匹配来源，也不能解除方法整体来源复审。历史37条匹配不等于科学准入。本轮路由研究只返回NO_LINK、REVIEW_REQUIRED或MATCHED_REFERENCE_ONLY，始终authority NONE；后续必须通过原生注册、可信输入、依赖、证据、用户授权和独立验收。全154×15组合核对与合同sources正向关系，另同量错误blob和短号控制；无相同短号跨文件绑定。静态合同中的共享VOI assumptions表达式保留原形参，不声称已完成动态解析。
新文档语义审查：C031补充仅在原三行动两情景六单元独立矩形与e∈[0,1]的尖锐阈值，不泛化任意表；Samuelson/Zeckhauser档案为现状标签与真实转换成本区分，Tversky/Shafir档案为延迟/搜索/默认与行动集范围，作者报告群体行为不能输入个人概率或直接替代效用。两篇行为研究只提供解释及提问线索，未重新核验原始论文。非对称VOI卡及先验切换卡要求合格概率和共同效用、无额外延迟；反向标签卡须同步交换概率与行动规则，标签无额外约束；联合稳健固定策略卡要求参数直积与预先承诺行动映射；先验区间卡是逐先验最优的参照而非固定可实施基线。不能仅凭同主题互换模型。
## 复算
独立于原卡代码，用整数比例计算原卡明确的合成算例：二状态、A恒6、B在S1为10否则0，三个概率十等分网格与四个确定策略枚举对照；反向标签、无信息与完全信息上界；固定质量先验690等分逐点与分段解析对照；联合质量八角点固定规则对A/B最小差及成本/质量边界；C031五个四分之一半径的构造见证，不是全域穷举或新定理。第33/48轮已有原生片段与一般证书研究，本轮仅补具体来源算例与接口可追溯边界；两算法同一研究者设计，非独立科学验收。没有运行15个完整原生方法或真实数据。
```json
{
  "docs": [
    {
      "path": "research/decision_methods/C031_ADDENDUM_SHARP_THRESHOLD_COUNTEREXAMPLE_2026-11-20.md",
      "blob": "04cb74c7ded99d16b3e96c0526872ec65fb50082",
      "size": 3323,
      "linkedMethods": [
        "C031@1.0.0"
      ],
      "length": 404,
      "uniqueTerms": 215,
      "hash": "04cb74c7ded99d16b3e96c0526872ec65fb50082"
    },
    {
      "path": "research/decision_methods/SAMUELSON_ZECKHAUSER_1988_STATUS_QUO_FRAMING_AUDIT_2026-11-20.md",
      "blob": "60ea84e4074a7f78644f3d70f0cbd2822d84374b",
      "size": 4409,
      "linkedMethods": [
        "timing_actions@1.0.0"
      ],
      "length": 569,
      "uniqueTerms": 337,
      "hash": "60ea84e4074a7f78644f3d70f0cbd2822d84374b"
    },
    {
      "path": "research/decision_methods/TVERSKY_SHAFIR_1992_CONFLICT_DEFERRAL_OPTION_SET_BOUNDARY_2026-11-21.md",
      "blob": "b03cdbe2165dd0543fff20cbeaefd6afacf718c4",
      "size": 5343,
      "linkedMethods": [
        "timing_actions@1.0.0"
      ],
      "length": 1251,
      "uniqueTerms": 901,
      "hash": "b03cdbe2165dd0543fff20cbeaefd6afacf718c4"
    },
    {
      "path": "research/decision_methods/VOI_ASYMMETRIC_BINARY_SIGNAL_EXTENSION_2026-11-20.md",
      "blob": "34cbe0e9268dbe249648ed30b94f57758e580ef4",
      "size": 3353,
      "linkedMethods": [
        "voi_point@1.0.0",
        "voi_oracle_bounds@1.0.0"
      ],
      "length": 713,
      "uniqueTerms": 491,
      "hash": "34cbe0e9268dbe249648ed30b94f57758e580ef4"
    },
    {
      "path": "research/decision_methods/VOI_ASYMMETRIC_SIGNAL_PRIOR_SWITCH_INTERVAL_2026-11-20.md",
      "blob": "40fa5a852337868670b39efff26a9b7b392cd762",
      "size": 4135,
      "linkedMethods": [
        "voi_point@1.0.0",
        "voi_oracle_bounds@1.0.0"
      ],
      "length": 855,
      "uniqueTerms": 565,
      "hash": "40fa5a852337868670b39efff26a9b7b392cd762"
    },
    {
      "path": "research/decision_methods/VOI_JOINT_SIGNAL_QUALITY_ROBUST_FIXED_POLICY_2026-11-21.md",
      "blob": "ae8091632eb376db97bce3caad6f4ede687a479b",
      "size": 3378,
      "linkedMethods": [
        "voi_fixed_policy@1.0.0",
        "voi_maximin@1.0.0"
      ],
      "length": 691,
      "uniqueTerms": 501,
      "hash": "ae8091632eb376db97bce3caad6f4ede687a479b"
    },
    {
      "path": "research/decision_methods/VOI_PRIOR_INTERVAL_ROBUST_COST_2026-11-21.md",
      "blob": "d3b68f67693e2f1f5f4e64fa63b44d39b9feb527",
      "size": 4530,
      "linkedMethods": [
        "voi_oracle_bounds@1.0.0"
      ],
      "length": 968,
      "uniqueTerms": 675,
      "hash": "d3b68f67693e2f1f5f4e64fa63b44d39b9feb527"
    },
    {
      "path": "research/decision_methods/VOI_REVERSED_BINARY_SIGNAL_LABEL_INVARIANCE_2026-11-20.md",
      "blob": "6f8b0271b1282a531ef29bbc5f4a6f9f36d2272c",
      "size": 2969,
      "linkedMethods": [
        "voi_point@1.0.0",
        "voi_oracle_bounds@1.0.0"
      ],
      "length": 605,
      "uniqueTerms": 433,
      "hash": "6f8b0271b1282a531ef29bbc5f4a6f9f36d2272c"
    }
  ],
  "routes": {
    "pairs": 2310,
    "links": 38,
    "review": 4,
    "matched": 34,
    "wrongHash": 2310,
    "shortIds": 2310
  },
  "result": {
    "voiGrid": 1331,
    "reverse": 1331,
    "uninformative": 121,
    "reversePositiveCases": 247,
    "priorChecks": 691,
    "cornerChecks": 8,
    "minA": 0.15,
    "minB": 0.25,
    "c031": [
      {
        "e": 0,
        "R": [
          6,
          2.5,
          5.5
        ]
      },
      {
        "e": 0.25,
        "R": [
          6.5,
          3,
          5
        ]
      },
      {
        "e": 0.5,
        "R": [
          7,
          3.5,
          4.5
        ]
      },
      {
        "e": 0.75,
        "R": [
          7.5,
          4,
          4
        ]
      },
      {
        "e": 1,
        "R": [
          8,
          4.5,
          3.5
        ]
      }
    ],
    "examples": {
      "asymmetric": 0.9,
      "reversed": 1.2
    }
  }
}
```
```js
function audit(cfg,cs){
 const check=(x,m)=>{if(!x)throw Error(m)};
 const map=new Map(cs.map(c=>[c.key,c])),byPath=new Map(cfg.assets.map(d=>[d.path,d]));
 function route(path,blob,key){
  const d=byPath.get(path),c=map.get(key);
  if(!d||d.blob!==blob||!c||!d.linkedMethods.includes(key))return {state:"NO_LINK",authority:"NONE"};
  if(c.sourceReview!=="MATCHED_IDENTITIES_ONLY"||c.sources.some(s=>s.status!=="MATCH"||s.baselineBlob!==s.currentBlob||byPath.get(s.path)?.blob!==s.currentBlob))return {state:"REVIEW_REQUIRED",authority:"NONE"};
  return {state:"MATCHED_REFERENCE_ONLY",authority:"NONE"};
 }
 let pairs=0,links=0,review=0,matched=0,wrongHash=0,shortIds=0;
 for(const d of cfg.assets)for(const c of cs){
  pairs++;const a=route(d.path,d.blob,c.key),oracle=c.sources.some(s=>s.path===d.path&&s.currentBlob===d.blob);
  check((a.state!=="NO_LINK")===oracle&&a.authority==="NONE","relation");
  if(oracle){links++;if(a.state==="REVIEW_REQUIRED")review++;else matched++;}
  check(route(d.path,"0".repeat(40),c.key).state==="NO_LINK","hash");wrongHash++;
  check(route(d.path,d.blob,c.key.split("@")[0]).state==="NO_LINK","short");shortIds++;
 }
 return {pairs,links,review,matched,wrongHash,shortIds};
}
function math(){
 const ck=(x,m)=>{if(!x)throw Error(m)};
 // Utility numerators, p,s,t in tenths. Four joint events sum to 100.
 function v(p,s,t){let a=p*s,b=(10-p)*(10-t),c=p*(10-s),d=(10-p)*t;return Math.max(6*(a+b),10*a)+Math.max(6*(c+d),10*c)-Math.max(600,100*p);}
 let n=0,reverse=0,uninformative=0,reverseLoss=0;
 for(let p=0;p<=10;p++)for(let s=0;s<=10;s++)for(let t=0;t<=10;t++){
  let x=v(p,s,t),j=[p*s,(10-p)*(10-t),p*(10-s),(10-p)*t],best=-Infinity;
  for(let a=0;a<2;a++)for(let b=0;b<2;b++){let total=(a?10*j[0]:6*(j[0]+j[1]))+(b?10*j[2]:6*(j[2]+j[3]));best=Math.max(best,total);}
  ck(x===best-Math.max(600,100*p)&&x>=0&&x<=600+40*p-Math.max(600,100*p),"VOI");
  ck(x===v(p,10-s,10-t),"reverse");reverse++;
  if(s+t===10){ck(x===0,"uninformative");uninformative++;}
  if(s+t<10&&x>0)reverseLoss++;n++;
 }
 // fixed quality 0.9/0.7, p=i/690, scaled 6900.
 let priorChecks=0;for(let i=0;i<=690;i++){const j=[9*i,3*(690-i),i,7*(690-i)],x=Math.max(6*(j[0]+j[1]),10*j[0])+Math.max(6*(j[2]+j[3]),10*j[2])-Math.max(41400,100*i);const expected=i<=230?0:i<=414?54*i-12420:i<=630?28980-46*i:0;ck(x===expected,"piecewise");priorChecks++;}
 // fixed strategy +B/-A, p tenths, s,t hundredths; scale1000.
 function fixed(p,s,t,c){return 10*p*s+6*(p*(100-s)+(10-p)*t)-c;}
 const corners=[];for(const p of [5,7])for(const s of [85,95])for(const t of [65,75]){let u=fixed(p,s,t,500);corners.push([p,s,t,u-6000,u-1000*p]);}
 const minA=Math.min(...corners.map(x=>x[3])),minB=Math.min(...corners.map(x=>x[4]));ck(minA===150&&minB===250,"joint");ck(fixed(5,85,65,650)===6000,"cost tie");ck(fixed(5,75,65,500)===5950,"failure");
 // C031 addendum: scale4, e in quarters. Witness strict margin or tie.
 const c031=[];for(let e=0;e<=4;e++){const U=[[32-e,8-e],[22-e,22-e],[10+e,32+e]],R=U.map(row=>Math.max(...row.map((x,w)=>Math.max(...U.map(v=>v[w]))-x)));ck(R[1]===10+2*e&&R[2]===22-2*e&&R[0]===24+2*e,"C031 witness");c031.push({e:e/4,R:R.map(x=>x/4)});}
 ck(v(5,9,7)===90&&v(5,1,2)===120,"card examples");
 return {voiGrid:n,reverse,uninformative,reversePositiveCases:reverseLoss,priorChecks,cornerChecks:corners.length,minA:minA/1000,minB:minB/1000,c031,examples:{asymmetric:v(5,9,7)/100,reversed:v(5,1,2)/100}};
}
// node >=18: 本报告数学函数可直接调用 math()；audit 使用固定 config.json 与 method_contracts.json。
// 原始字节可用 Node crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex') 重验。
// 词项使用第29轮 build_index.js 相同分词；本轮实际使用第51轮纯 JS SHA1 和 base64。
console.log(JSON.stringify(math(),null,2));
```
## 下一步
B04/B06/B08/B10/B11候选。优先用已有154份构建器在完整仓库环境构建单一索引，非直接登记的114份仍可能对理论与解释重要；不得让关联数等同于模型数量或有效性。需执行支持环境原生describe/validate/execute、真实Qwen多意图检索、独立语义与来源审核。既有来源版本隔离不解除；所有科研证据和冻结条件原样保留。不另建工作流，不修改生产、CI、Codex、训练、合并、部署，无新增费用。 
