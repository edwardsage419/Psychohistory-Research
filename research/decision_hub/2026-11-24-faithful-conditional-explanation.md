# 第49轮：条件式决策建议的最简覆盖、受控白话表达与完整性核验
2026-11-24。固定 main 32aab8f9c28631a51aaa69cf7c74f835d8a9a36d；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一协调交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第7/34/46/48轮。PR #61 decision_conversation.py f505aeab2d9e5e0a9c8957ce6e039dea174918a7、decision_local_ai.py 726b7a2e0da64af7037d892ac8bf508412deb5d6、decision_language.py fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4 已有对话和语言提议机制；local_ai源码明确逐字复制待确认候选选项，本轮未运行实际模型或前端。关键词 explanation/claim coverage/faithful summary/output fidelity/rendering 查重，仅找到历史解释理论、历史R收据及产品显示审查题名，不声称全库无重复。区别于既有第5轮最少追问、第38/46轮竞争假设、第48轮结果发布证书，本轮新增已验证离散条件结果的精确短语覆盖、最小表达成本及受控白话回读。原创有限算法，无外部来源事实。
## 数学合同
给定非空、证据合格的有限联合世界域F，条件变量已具可辨认语义、主体、单位、时间及来源；每世界标签g(w)来自同一已核验决策合同（本实验四标签：无可行、A唯一最优、B唯一最优、A/B并列）。实际标签还须保留不确定、风险、不可比等结果；本实验不处理这些标签内含的详细义务。用户底线、授权与高风险信息始终独立且不可删。世界标签是条件结论，不宣称实际世界已识别、假设为事实或现实概率。三二元条件的一个合取式c可把每变量设0、1或省略，覆盖世界集合C。给定标签j的目标集合T_j={w∈F:g(w)=j}，仅允许非空(C∩F)⊆T_j的短语，确保其在合同内不会误导。所有同标签短语可重叠；不同标签不得覆盖同一允许世界。完整表达须覆盖F，保留无可行、并列和全部条件；可选择只发布局部分析，但明确未覆盖，不称完整。固定最少短语数再最少条件文字项数的示例目标，非真人理解负担或通用语言最佳。条件变量可能关联，合法域F不得被误当全空间；范围外明确未知，不能把省略域外条件的句子迁移到新合同。
在每个T_j上求最小成本集合覆盖：D(empty)=0；任取尚未覆盖点w，D(S)=min_{c:w∈C∩F且C∩F⊆T_j}[cost(c)+D(S\C)]。归纳：任一完整覆盖必含覆盖w的短语，去除其覆盖后余项仍覆盖其余；反向拼接合法。按标签分别最优化因无跨标签短语、成本相加。实验cost=100+文字项数（至多8短语、24项，故等价字典序）；更大规模不能沿用100常数。完整世界的单点合取式确保存在覆盖，最坏指数复杂度；预算不足可返回已有正确短语及明确未覆盖范围，不声称最简。本轮未实现截断和自由文本核验。
## 表达与核验
采用固定中文语法“若[条件合取]，[标签]。”，从可信条件注册表和标签生成。解析器仅接受该语法并对每个允许世界复核所有匹配标签，禁止空覆盖、错标签、未覆盖及不支持的额外句子。任一已列情景必须绑定有效F及快照，不能省略共同决策目标、评价口径、事实/假设身份和高风险提示。示例中文变量是占位符；未从真实白话提取，未测语言流畅度。生产自由生成可用受控短语作为事实骨架，但仍需真实语义提取核验；当前解析器无法识别自然语言同义、暗示、否定、复合条件或图表语义。不同解释不能由人工标签自行授权。输入修订或权限变化重新生成。
## 实验
8个全世界，每世界4标签，全部65536真值表。先计算所有256个目标集合在全域下的覆盖，与独立按已覆盖掩码的最短路枚举核对。所有表达逐句渲染和回读，比较8条逐世界句子、固定变量顺序0/1/2的完整决策树叶数（同标签子树压缩），以及错误的多数标签无条件输出（并列取低ID）。naiveUnsafe为多数标签未覆盖完整真实标签函数，非现实安全错误率；naiveLostTie和naiveLostNone为遗漏并列或无可行标签的表数。每257表执行逐句删除、错标签替换和附加非法语法句的控制；语义等价删除可通过，计入mutationEquivalent而非漏检。另256个确定模式（i*257的四进制标签）×15个非空域=3840组关联/限制域，逐标签核对最优成本及回读。重复域查询不代表独立样本。成本与条件名称均人工设置，两种算法同一研究者设计，非独立验收。无用户实验、真实Qwen或产品表现测量。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)}, W=Array.from({length:8},(_,i)=>i),K=[0,1,2],names=["条件甲","条件乙","条件丙"],labels=["无可行方案","A为唯一最优","B为唯一最优","A与B并列最优"];
 const pop=m=>W.filter(w=>m&(1<<w)).length;
 const cubes=[];
 for(let i=0;i<27;i++){let z=i;const p=K.map(()=>{let v=z%3-1;z=Math.floor(z/3);return v;});const mask=W.reduce((m,w)=>m|(p.every((v,k)=>v===-1||v===((w>>k)&1))?1<<w:0),0);cubes.push({p,mask,lit:p.filter(x=>x!==-1).length});}
 // Objective lexicographic number of clauses then literals, bounded 24 literals <100.
 const cost=c=>100+c.lit;
 const domainCache=new Map();
 function covers(domain,target){
  const key=domain*256+target;if(domainCache.has(key))return domainCache.get(key);
  const eligible=cubes.filter(c=>(c.mask&domain)!==0&&((c.mask&domain)&~target)===0);
  const memo=new Map([[0,{cost:0,ids:[]}]]);
  function dp(left){
   if(memo.has(left))return memo.get(left);
   const first=left&-left;let best={cost:Infinity,ids:[]};
   for(const c of eligible){if(!(c.mask&first))continue;const tail=dp(left&~c.mask),v=cost(c)+tail.cost;if(v<best.cost)best={cost:v,ids:[c,...tail.ids]};}
   memo.set(left,best);return best;
  }
  const v=dp(target);domainCache.set(key,v);return v;
 }
 // Independent shortest-path enumeration over covered masks, not recursion by first uncovered point.
 function oracle(domain,target){
  const dist=Array(256).fill(Infinity);dist[0]=0;
  for(let m=0;m<256;m++)if((m&~target)===0&&Number.isFinite(dist[m]))for(const c of cubes){
   const s=c.mask&domain;if(!s||(s&~target))continue;const n=m|s;if(n!==m)dist[n]=Math.min(dist[n],dist[m]+cost(c));
  }return dist[target];
 }
 function render(c,label){const cond=c.p.flatMap((v,k)=>v<0?[]:[names[k]+(v?"成立":"不成立")]);return "若"+(cond.length?cond.join("且"):"任一已列情景")+"，"+labels[label]+"。";}
 // Restricted grammar decoder (not a general natural-language evaluator).
 function parse(s){
  const match=/^若(.+)，(.+)。$/.exec(s);if(!match)return null;const l=labels.indexOf(match[2]);if(l<0)return null;
  const p=[-1,-1,-1];if(match[1]!=="任一已列情景")for(const t of match[1].split("且")){
   const k=names.findIndex(n=>t===n+"成立"||t===n+"不成立");if(k<0||p[k]!==-1)return null;p[k]=t.endsWith("不成立")?0:1;
  }return {mask:cubes.find(c=>c.p.join()===p.join()).mask,label:l};
 }
 function verify(lines,domain,truth){const parsed=lines.map(parse);if(parsed.some(x=>!x))return false;
  return W.filter(w=>domain&(1<<w)).every(w=>{const found=parsed.filter(x=>x.mask&(1<<w));return found.length>0&&found.every(x=>x.label===truth[w]);})&&parsed.every(x=>x.mask&domain);
 }
 function plan(domain,truth){const result=[];let score=0;for(let l=0;l<4;l++){const t=W.reduce((m,w)=>m|((domain&(1<<w))&&truth[w]===l?1<<w:0),0);const v=covers(domain,t);score+=v.cost;for(const c of v.ids)result.push(render(c,l));}return {result,score};}
 let cases=0,checks=0,clauses=0,literals=0,strict=0,treeGap=0,treeClauses=0,naiveUnsafe=0,naiveLostTie=0,naiveLostNone=0,mutationChecks=0,mutationRejected=0,mutationEquivalent=0,partialCases=0,oracleChecks=0,witness=null,partialWitness=null;
 for(let t=0;t<256;t++){check(covers(255,t).cost===oracle(255,t),"cover oracle");oracleChecks++;}
 function tree(truth,ws,k){if(ws.every(w=>truth[w]===truth[ws[0]]))return 1;return tree(truth,ws.filter(w=>!((w>>k)&1)),k+1)+tree(truth,ws.filter(w=>(w>>k)&1),k+1);}
 for(let i=0;i<65536;i++){
  let z=i;const truth=W.map(()=>{const v=z%4;z=Math.floor(z/4);return v;});
  const p=plan(255,truth);cases++;check(verify(p.result,255,truth),"roundtrip");checks++;
  clauses+=p.result.length;literals+=p.score-100*p.result.length;if(p.result.length<8)strict++;
  const tc=tree(truth,W,0);treeClauses+=tc;check(p.result.length<=tc,"tree bound");if(p.result.length<tc)treeGap++;
  const freq=labels.map((_,l)=>truth.filter(v=>v===l).length);const majority=freq.indexOf(Math.max(...freq));
  if(truth.some(v=>v!==majority))naiveUnsafe++;
  if(truth.includes(3)&&majority!==3)naiveLostTie++;
  if(truth.includes(0)&&majority!==0)naiveLostNone++;
  if(!witness&&p.result.length<tc&&truth.includes(0)&&truth.includes(3))witness={truth,lines:p.result,tree:tc};
  if(i%257===0){
   // Delete or replace each individual clause; redundant deletions can be semantically equivalent.
   for(let j=0;j<p.result.length;j++){
    const del=p.result.filter((_,k)=>j!==k);
    const d=parse(p.result[j]);const rep=p.result.map((s,k)=>j===k?s.replace(labels[d.label]+"。",labels[(d.label+1)%4]+"。"):s);
    const deleted=verify(del,255,truth);mutationChecks++;if(deleted)mutationEquivalent++;else mutationRejected++;
    mutationChecks++;check(!verify(rep,255,truth),"label mutation");mutationRejected++;
   }
   mutationChecks++;check(!verify([...p.result,"A肯定会成功。"],255,truth),"unsupported grammar");mutationRejected++;
  }
 }
 // Explicit constrained-domain tests: same truth table, 15 representative nonempty domains.
 for(let i=0;i<256;i++){
  let z=i*257;const truth=W.map(()=>{const v=z%4;z=Math.floor(z/4);return v;});
  for(const domain of [1,3,5,7,15,17,31,51,63,85,90,127,170,204,254]){
   const p=plan(domain,truth);partialCases++;check(verify(p.result,domain,truth),"restricted domain");
   for(let l=0;l<4;l++){const t=W.reduce((m,w)=>m|((domain&(1<<w))&&truth[w]===l?1<<w:0),0);check(covers(domain,t).cost===oracle(domain,t),"restricted oracle");oracleChecks++;}
   if(!partialWitness&&verify(p.result,domain,truth)&&!verify(p.result,255,truth))partialWitness={domain,truth,lines:p.result};
  }
 }
 check(mutationRejected+mutationEquivalent===mutationChecks,"mutation accounting");
 return {cases,checks,clauses,literals,strict,treeGap,treeClauses,naiveUnsafe,naiveLostTie,naiveLostNone,mutationChecks,mutationRejected,mutationEquivalent,partialCases,oracleChecks,witness,partialWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "cases": 65536,
  "checks": 65536,
  "clauses": 389308,
  "literals": 993672,
  "strict": 62884,
  "treeGap": 43344,
  "treeClauses": 456700,
  "naiveUnsafe": 65532,
  "naiveLostTie": 46686,
  "naiveLostNone": 37236,
  "mutationChecks": 1896,
  "mutationRejected": 1896,
  "mutationEquivalent": 0,
  "partialCases": 3840,
  "oracleChecks": 15616,
  "witness": {
    "truth": [
      3,
      1,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "lines": [
      "若条件乙成立，无可行方案。",
      "若条件丙成立，无可行方案。",
      "若条件甲成立且条件乙不成立且条件丙不成立，A为唯一最优。",
      "若条件甲不成立且条件乙不成立且条件丙不成立，A与B并列最优。"
    ],
    "tree": 6
  },
  "partialWitness": {
    "domain": 1,
    "truth": [
      1,
      0,
      0,
      0,
      1,
      0,
      0,
      0
    ],
    "lines": [
      "若任一已列情景，A为唯一最优。"
    ]
  }
}
```
## 接入
B02/B05/B06/B07/B08/B11候选增量。首答优先提供有效稳定结论、关键底线与足以改变建议的条件，再按需展开依据、图表和计算；同一可信快照生成全部视图，说明当前条件合同、未验证或未计算部分及无现实概率。用户无需填写技术字段；若不能确定条件真值，使用白话条件式比较，重要缺口只在必要时追问。最低短语成本仅用于结构化骨架，用户理解、阅读时长、误解、行动质量、自由生成及图文一致性须独立实测。独立轨冻结未见单位、时间、严格边界、条件极性、未知、多个并列、无可行、假设混为事实、过期结果、图文不一致与关键风险被省略；产品轨维护唯一交接和首答解释测试；模型轨核查连续阈值、多值条件、复杂逻辑及资源限制。无生产修改、CI、Codex、训练、合并、部署、冻结协议变更或新增费用。真实产品、设备、真人及独立验收均未运行。
