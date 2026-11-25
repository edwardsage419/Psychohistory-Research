# v3.2 自主认知专项第2轮（累计第61轮）：有限组合语义与歧义保留

2026-11-25。RESEARCH_CANDIDATE。固定main 094279e0e8cedb255c4f321d6c2ccbf694e36b90；PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，13开放Draft PR。核对最近8提交、v3.2 blob 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前部及上轮全文）、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（末段，非全82KB逐段审计）、decision_hub目录语言与语义相关文件名、第2/58/60轮相关协议。第2轮已做给定布尔树的有限补全，本轮新增从原始有限中文字符串构造多个解析树，明确括号与否定范围，比较强制单一解释。不重复第59轮原生interpret评价，也不宣称新候选胜过实际PR。

## 研究问题与来源
固定词典和语法能否在无第三方模型条件下保留混合逻辑结构的多种候选，并避免在歧义足以改变结果时强行选择？Earley (1970), An Efficient Context-Free Parsing Algorithm, DOI 10.1145/362007.362035；Pratt (1973), Top Down Operator Precedence, DOI 10.1145/512927.512931。实际核对公开检索摘要、书目信息与Pratt原文重刊摘录 https://tdop.github.io/ ，未通读或复现原论文，不复制外部语料。候选为自写的区间记忆化递归解析，非Earley或Pratt算法实现。

## 算法及证据边界
词典仅三条固定含数值、单位、周期的原子谓词，各两个词面；只接受且、或者、并非、全角括号。按最长词匹配保留UTF16起止位置；所有字符必须被识别，未知字符返回UNKNOWN_TOKEN和首个偏移，不丢弃。没有通用数值解析、主体、角色、条件蕴涵、语用、指代或自由中文识别；逗号句号与空白目前也未支持。语法 E := atom | (E) | not atom | not (E) | E and E | E or E；并非只作用于一个原子或完整匹配括号组。对每个区间枚举合法拆分，保留全部树；25 token、每区间128树上限，超限整句LIMIT，禁止用截断树集合给确定结果。初版发现端点括号检查不保证完整匹配组，修正为深度扫描并加入并非（A）且（B）控制。初版1152文本核心计数相同；未把初版未覆盖的缺陷算作现行产品漏洞。重复同一原子共享同一赋值；不证明现实原子的独立性。对全部候选树及与三值输入相容的有限布尔世界求真值集合，只有全集真/假才给PASS/FAIL，其余UNKNOWN；空集合CONFLICT。PASS仅指这个布尔表达式在夹具中的判定，不表示真实约束已核实或推荐合格。明确语义等价的不同解析树可共享决策结果但保留原文。真实联合约束、真实事实以及独立覆盖义务仍须可信宿主提供；没有这些资格不得输出完整建议。

## 实际实验设计
8个词面组合×6个原子排列×4个操作符组合×3种括号模式×2个整体否定状态=1152个构造输入，每个27个真假未知状态，共31104个判断。比较基线：在同一合法树集合内用AND高于OR的简单优先级惩罚选择一棵树，显式括号已经由共同解析器遵守；不是现有PR、真实ChatGPT或正则全文基线。参照路径不调用解析器，直接按生成模板计算左右两种布尔结合顺序及所有相容世界；同一研究者定义语法和夹具，并非独立留出。baselineFalsePass/Fail为在参照UNKNOWN时强行确定，不代表实际世界必错或实际损害已发生。192个语义不同多树文本、192个等价多树文本。12项专项控制覆盖未知、标点、空、残缺、两个资源上限、共享原子、否定括号及空真值集合。没有测真实设备性能、开放语义、真实用户、原生平台或独立验收。代码和样例为项目原创合成研究（ChatGPT研发辅助生成，非真人语料、非训练数据，无外部权重和运行服务；没有另行训练授权）。

## 复算
以下函数与本轮实际执行代码一致，可在Node直接运行，无第三方包或网络请求：

```js
const probe = function(){
 const ck=(v,m)=>{if(!v)throw Error(m)};
 const words=[["收入不少于5000元","收入至少5000元"],["通勤不超过30分钟","通勤至多30分钟"],["每周工时最多40小时","每周工作不超过40小时"]];
 const lexicon=[...words.flatMap((g,i)=>g.map(s=>[s,String(i)])),["并非","!"],["且","&"],["或者","|"],["（","("],["）",")"]].sort((a,b)=>b[0].length-a[0].length);
 function parse(s){
  const t=[];let p=0;while(p<s.length){const w=lexicon.find(([k])=>s.startsWith(k,p));if(!w)return {status:"UNKNOWN_TOKEN",offset:p};t.push({k:w[1],start:p,end:p+w[0].length});p+=w[0].length;if(t.length>25)return {status:"LIMIT"};}
  const memo=new Map();function grouped(l,r){if(r-l<3||t[l].k!=="("||t[r-1].k!==")")return false;let d=0;for(let i=l;i<r;i++){if(t[i].k==="(")d++;if(t[i].k===")")d--;if(d<=0&&i!==r-1)return false;}return d===0;}
  function span(l,r){
   const key=l+":"+r;if(memo.has(key))return memo.get(key);let out=[];
   const add=x=>{out.push(x);if(out.length>128)throw Error("LIMIT")};
   if(r-l===1&&["0","1","2"].includes(t[l].k))add(["atom",+t[l].k,t[l].start,t[l].end]);
   if(grouped(l,r))for(const x of span(l+1,r-1))add(x);
   if(r-l>=2&&t[l].k==="!"&&((r-l===2&&["0","1","2"].includes(t[l+1].k))||grouped(l+1,r)))for(const x of span(l+1,r))add(["!",x]);
   for(let k=l+1;k<r-1;k++)if(["&","|"].includes(t[k].k))for(const a of span(l,k))for(const b of span(k+1,r))add([t[k].k,a,b]);
   memo.set(key,out);return out;
  }
  try{const trees=t.length?span(0,t.length):[];return trees.length?{status:"CANDIDATE",trees}:{status:"UNSUPPORTED_SYNTAX"}}catch(e){if(e.message==="LIMIT")return {status:"LIMIT"};throw e}
 }
 function evalTree(t,w){if(t[0]==="atom")return w[t[1]];if(t[0]==="!")return !evalTree(t[1],w);return t[0]==="&"?evalTree(t[1],w)&&evalTree(t[2],w):evalTree(t[1],w)||evalTree(t[2],w)}
 const worlds=Array.from({length:8},(_,m)=>[0,1,2].map(i=>!!(m&(1<<i))));
 const states=[false,true,null].flatMap(a=>[false,true,null].flatMap(b=>[false,true,null].map(c=>[a,b,c])));
 function verdict(vals){if(!vals.length)return "CONFLICT";return vals.every(Boolean)?"PASS":vals.every(x=>!x)?"FAIL":"UNKNOWN"}
 function penalty(t){if(t[0]==="atom")return 0;if(t[0]==="!")return penalty(t[1]);return penalty(t[1])+penalty(t[2])+(t[0]==="&"?Number(t[1][0]==="|")+Number(t[2][0]==="|"):0)}
 const permutations=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
 const op=(o,a,b)=>o==="&"?a&&b:a||b, sym=o=>o==="&"?"且":"或者";
 const counts={texts:0,checks:0,oracleMatches:0,baselineMatches:0,baselineFalsePass:0,baselineFalseFail:0,ambiguousTexts:0,multiTreeEquivalent:0,unknown:0,pass:0,fail:0,controls:0,maxTrees:0};
 let witness=null;
 for(let alias=0;alias<8;alias++)for(const ids of permutations)for(const o of ["&","|"])for(const p of ["&","|"])for(const mode of ["bare","left","right"])for(const neg of [false,true]){
  const [a,b,c]=ids.map(i=>words[i][(alias>>i)&1]);let s=mode==="left"?`（${a}${sym(o)}${b}）${sym(p)}${c}`:mode==="right"?`${a}${sym(o)}（${b}${sym(p)}${c}）`:`${a}${sym(o)}${b}${sym(p)}${c}`;if(neg)s=`并非（${s}）`;
  const r=parse(s);ck(r.status==="CANDIDATE","parse "+s);counts.texts++;counts.maxTrees=Math.max(counts.maxTrees,r.trees.length);
  const sig=new Set(r.trees.map(t=>worlds.map(w=>Number(evalTree(t,w))).join("")));if(sig.size>1)counts.ambiguousTexts++;else if(r.trees.length>1)counts.multiTreeEquivalent++;
  const baseline=r.trees.reduce((best,t)=>penalty(t)<penalty(best)?t:best);
  for(const state of states){
   const ws=worlds.filter(w=>state.every((v,i)=>v===null||v===w[i]));let reference=[];
   for(const w of ws){const [x,y,z]=ids.map(i=>w[i]);const left=op(p,op(o,x,y),z),right=op(o,x,op(p,y,z));for(const v of mode==="left"?[left]:mode==="right"?[right]:[left,right])reference.push(neg?!v:v)}
   const gold=verdict(reference),candidate=verdict(r.trees.flatMap(t=>ws.map(w=>evalTree(t,w)))),base=verdict(ws.map(w=>evalTree(baseline,w)));
   counts.checks++;ck(candidate===gold,"oracle "+s);counts.oracleMatches++;counts[candidate.toLowerCase()]++;
   if(base===gold)counts.baselineMatches++;if(base==="PASS"&&gold!=="PASS"){counts.baselineFalsePass++;if(!witness)witness={text:s,state,base,candidate,trees:r.trees};}if(base==="FAIL"&&gold!=="FAIL")counts.baselineFalseFail++;
  }
 }
 const a=words[0][0],b=words[1][0];
 for(const [s,expected] of [["", "UNSUPPORTED_SYNTAX"],[a+"且", "UNSUPPORTED_SYNTAX"],["（"+a,"UNSUPPORTED_SYNTAX"],[a+"但是要照顾家人","UNKNOWN_TOKEN"],["大概"+a,"UNKNOWN_TOKEN"],[a+"且"+b+"。","UNKNOWN_TOKEN"],[Array(14).fill(a).join("且"),"LIMIT"],[Array(10).fill(a).join("且"),"LIMIT"]]){ck(parse(s).status===expected,s);counts.controls++}
 const taut=parse(`${a}或者并非${a}`);ck(taut.status==="CANDIDATE"&&verdict(taut.trees.flatMap(t=>worlds.map(w=>evalTree(t,w))))==="PASS","shared atom");counts.controls++;
 const contradiction=parse(`${a}且并非${a}`);ck(contradiction.status==="CANDIDATE"&&verdict(contradiction.trees.flatMap(t=>worlds.map(w=>evalTree(t,w))))==="FAIL","shared atom");counts.controls++;
 const scope=parse(`并非（${a}）且（${b}）`);ck(scope.status==="CANDIDATE"&&scope.trees.length===1&&worlds.every(w=>evalTree(scope.trees[0],w)===(!w[0]&&w[1])),"negation scope");counts.controls++;
 ck(verdict([])==="CONFLICT","empty worlds");counts.controls++;
 return {counts,witness};
};
console.log(JSON.stringify(probe(),null,2));
```

实际输出：

```json
{
  "counts": {
    "texts": 1152,
    "checks": 31104,
    "oracleMatches": 31104,
    "baselineMatches": 29952,
    "baselineFalsePass": 576,
    "baselineFalseFail": 576,
    "ambiguousTexts": 192,
    "multiTreeEquivalent": 192,
    "unknown": 11520,
    "pass": 9792,
    "fail": 9792,
    "controls": 12,
    "maxTrees": 2
  },
  "witness": {
    "text": "收入不少于5000元且通勤不超过30分钟或者每周工时最多40小时",
    "state": [
      false,
      false,
      true
    ],
    "base": "PASS",
    "candidate": "UNKNOWN",
    "trees": [
      [
        "&",
        [
          "atom",
          0,
          0,
          10
        ],
        [
          "|",
          [
            "atom",
            1,
            11,
            20
          ],
          [
            "atom",
            2,
            22,
            32
          ]
        ]
      ],
      [
        "|",
        [
          "&",
          [
            "atom",
            0,
            0,
            10
          ],
          [
            "atom",
            1,
            11,
            20
          ]
        ],
        [
          "atom",
          2,
          22,
          32
        ]
      ]
    ]
  }
}
```

## 下一接口与验收
接第58轮义务核验与第60轮自主运行时接口：保留候选树、原文跨度、词典和语法版本、未知覆盖与限制状态；仅当解释差异影响当前可行性或排序时才要求用户消歧，未来应区分当前与未来情景影响，未实现问题生成及下游计算。下一轮优先研究可组合的类型化数量、单位、比较关系与候选原子产生，避免固定三条原子扩展成无限句式正则。独立验收轨负责冻结未知自由文本与真实设备实验，产品轨负责简洁追问，模型轨负责类型与复算。没有训练、Qwen/Ollama调用、产品改动、CI、合并、部署、个人数据或新增费用。冻结协议不变。没有发布Codex任务。