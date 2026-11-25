# 自主认知专项累计第93轮候选：相关语义解释域的决策保持与最小固定澄清集合

2026-11-25。RESEARCH_CANDIDATE / CORRELATED_DOMAIN_EXACT_CERTIFICATE_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线main fafbe274b6c588fd9a40fc31f15ab5cde055d4d2。核查近20提交、13开放PR（#61待审）、v3.2首8行及历史全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07）、R65首20行（b16928724409abc5e701dd8716371430a212dcf6）、R92首18行。R65已经验证完整笛卡尔解释域下的单维相关性，明确非笛卡尔可能漏检；本轮专门验证这个缺口与非自适应固定澄清集合的证书，不重做原文修订解析或既有自适应询问策略。没有外部资料、真实用户或训练。

## 合同
人工给定3个二元语义维度：预算对象、替换/追加上限、仅B/全方案作用域。其允许解释集合为8个世界的任意非空子集，可能相关而非笛卡尔积。两个方案A/B各两项同口径费用，初始上限5/7，新上限6，追加取min；序位B优于A，均为人工夹具，非真实效用、偏好、货币或授权。4个端口：A可行、B可行、完整可行集、固定序位优选（无可行亦保留）。各解释不赋概率，计算结果仅在覆盖与事实资格已由可信宿主确认的有限域内成立；本轮coverage布尔为人工设定，实际覆盖证明未实现。未知域不得因当前枚举结果一致而放行，空闭域冲突，任何预算超限清空候选问题集合。全部authority NONE，不写入或执行。用户价值选择不由系统代替。

## 数学
对于端口f及允许域H，固定问题集合S充分当且仅当对任意h,h'∈H，若其S维度答案相同则f(h)=f(h')。等价于S命中每一对输出不同世界的差异维度集合D(h,h')。证明：若没有命中则两世界无法区分且输出不同；若全部命中，则任一答案等价类的输出恒定。最小固定集合在非负给定成本下枚举所有S、保留并列最优。对空差异对集合，空问题集合充分。不需要完整笛卡尔域。只在完整笛卡尔域，单维邻接检测在全部维度不变时可推出全域恒定；相关域可能没有单维变化边却存在输出不同的解释。不能将未出现的组合当作允许世界。问题成本1/2/3是研究者给定，并非实际认知时间、用户偏好或信息价值；本轮最优是预先固定问题集合，不是自适应追问策略最优，也不保证用户能回答、答复正确或愿意回答。复杂度朴素为O(|H|²d+2^d|H|²)，预算只计成对检查和集合枚举，不含构图、实际设备资源。精确覆盖布尔不得由统计置信度代替。候选语义细化或更新后要重新计算；根权重守恒不保证决策端口保持。

## 实验
枚举255个非空允许域×81组点值=20655场景、4端口；差异集合命中法与独立的答案投影分组法对照，同一研究者定义，非独立验收。对最优集合每个实际答案类检查端口恒定；1020个覆盖缺失及1020个预算少一控制。单维边漏检指端口不同但不存在只变一维且输出不同的允许世界对，不是产品误判率。首解释风险指存在另一个允许解释改变输出，不等于真实错误。所有问题总成本6，平均成本仅人工夹具。12项控制。无训练、Codex、CI、生产修改、PR合并、部署、费用或冻结协议变更。既有完整版本范围及正式验收门保留。下一步应研究解释域的可信来源与覆盖、真实语言输入、端口依赖和已有数学引擎连接；不能继续仅靠人工夹具宣称产品质量。产品轨维护唯一交接，独立轨负责独立样本，数据轨负责合法来源。

## 可复算源码
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)},W=Array.from({length:8},(_,i)=>[i&1,(i>>1)&1,(i>>2)&1]),cost=[1,2,3],key=(w,S)=>w.filter((_,i)=>S&(1<<i)).join(""),c=S=>cost.reduce((a,b,i)=>a+((S&(1<<i))?b:0),0);
 // x: budget target, y: replacement vs addition, z: conditional scope.
 // External finite interpretations, no automatic parsing. All money in same
 // qualified fixture unit; A/B fixed ordinal preference B>A.
 function calc(w,v){let [x,y,z]=w,lim=[[5,7],[5,7]];for(let i=0;i<2;i++)if(!z||i===1)lim[i][x]=y?Math.min(lim[i][x],6):6;
  let f=v.map((a,i)=>a.every((n,j)=>n<=lim[i][j]));return [f[0]?1:0,f[1]?1:0,f.map(Number).join(""),f[1]?"B":f[0]?"A":"NONE"]}
 function solve(rows,port,closed,cap=10000){
  if(!closed)return {status:"UNKNOWN_COVERAGE",authority:"NONE",sets:[]};
  if(!rows.length)return {status:"CONFLICT",authority:"NONE",sets:[]};
  let pairs=[],used=0;for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){if(used>=cap)return {status:"LIMIT",authority:"NONE",sets:[]};used++;if(rows[i].f[port]!==rows[j].f[port])pairs.push(rows[i].w.reduce((s,v,k)=>s|((v!==rows[j].w[k])?1<<k:0),0))}
  let best=Infinity,sets=[];for(let S=0;S<8;S++){if(used>=cap)return {status:"LIMIT",authority:"NONE",sets:[]};used++;if(pairs.every(D=>D&S)){let q=c(S);if(q<best){best=q;sets=[]}if(q===best)sets.push(S)}}
  return {status:best===0?"INVARIANT_CONDITIONAL":"VARIES",authority:"NONE",sets,best,used}
 }
 function oracle(rows,p){let a=[];for(let S=0;S<8;S++){let m=new Map(),ok=true;for(let row of rows){let k=key(row.w,S),v=row.f[p];if(m.has(k)&&m.get(k)!==v){ok=false;break}m.set(k,v)}if(ok)a.push(S)}let min=Math.min(...a.map(c));return {sets:a.filter(S=>c(S)===min),best:min}}
 let o={domains:0,scenarios:0,ports:0,invariant:0,varies:0,nonCartesian:0,singleEdgeMiss:0,singleEdgeMissNonCartesian:0,allQuestionsUnnecessary:0,lessThanAllCost:0,firstWorldRisk:0,meanCost:0,budgetChecks:0,coverageChecks:0,answerBranchChecks:0,answerBranchInvariant:0,controls:0,witness:null};
 for(let mask=1;mask<256;mask++){let domain=W.filter((_,i)=>mask&(1<<i));o.domains++;let prod=[0,1,2].reduce((p,k)=>p*new Set(domain.map(w=>w[k])).size,1),non=prod!==domain.length;if(non)o.nonCartesian++;
  for(let v0 of [4,6,8])for(let v1 of [4,6,8])for(let v2 of [4,6,8])for(let v3 of [4,6,8]){
   let v=[[v0,v1],[v2,v3]],rows=domain.map(w=>({w,f:calc(w,v)}));o.scenarios++;
   for(let p=0;p<4;p++){let x=solve(rows,p,true),y=oracle(rows,p);ck(x.best===y.best&&JSON.stringify(x.sets)===JSON.stringify(y.sets),"oracle");o.ports++;o.meanCost+=x.best;
    if(x.best===0){o.invariant++;o.allQuestionsUnnecessary++}else{o.varies++;o.firstWorldRisk++;let edgeChange=false;for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++)if(rows[i].w.filter((a,k)=>a!==rows[j].w[k]).length===1&&rows[i].f[p]!==rows[j].f[p])edgeChange=true;
     if(!edgeChange){o.singleEdgeMiss++;o.singleEdgeMissNonCartesian+=+non;if(!o.witness)o.witness={domain,v,port:p,outputs:rows.map(z=>z.f[p]),questions:x.sets}}
    }if(x.best<6)o.lessThanAllCost++;
    // Check every answer class of every optimal fixed question set.
    for(let S of x.sets){let keys=[...new Set(rows.map(row=>key(row.w,S)))];for(let k of keys){let branch=rows.filter(row=>key(row.w,S)===k);ck(new Set(branch.map(row=>row.f[p])).size===1,"branch");o.answerBranchChecks++;o.answerBranchInvariant++}}
    if(v0===4&&v1===4&&v2===4&&v3===4){let z=solve(rows,p,false);ck(z.status==="UNKNOWN_COVERAGE"&&!z.sets.length,"coverage");o.coverageChecks++;let t=solve(rows,p,true,x.used-1);ck(t.status==="LIMIT"&&!t.sets.length,"limit");o.budgetChecks++}
   }
  }
 }
 o.meanCost/=o.ports;
 for(let t of [()=>o.domains===255,()=>o.scenarios===20655,()=>o.ports===82620,()=>o.invariant+o.varies===o.ports,()=>o.singleEdgeMiss>0,()=>o.singleEdgeMiss===o.singleEdgeMissNonCartesian,()=>o.budgetChecks===1020,()=>o.coverageChecks===1020,()=>o.answerBranchInvariant===o.answerBranchChecks,()=>solve([],0,true).status==="CONFLICT",()=>solve([],0,false).status==="UNKNOWN_COVERAGE",()=>o.meanCost<6]){ck(t(),"control");o.controls++}return o
}
console.log(experiment())
```

## 实测
```json
{
  "domains": 255,
  "scenarios": 20655,
  "ports": 82620,
  "invariant": 67076,
  "varies": 15544,
  "nonCartesian": 228,
  "singleEdgeMiss": 2400,
  "singleEdgeMissNonCartesian": 2400,
  "allQuestionsUnnecessary": 67076,
  "lessThanAllCost": 81804,
  "firstWorldRisk": 15544,
  "meanCost": 0.5227305737109659,
  "budgetChecks": 1020,
  "coverageChecks": 1020,
  "answerBranchChecks": 117696,
  "answerBranchInvariant": 117696,
  "controls": 12,
  "witness": {
    "domain": [
      [
        0,
        0,
        0
      ],
      [
        1,
        1,
        0
      ]
    ],
    "v": [
      [
        4,
        4
      ],
      [
        6,
        4
      ]
    ],
    "port": 1,
    "outputs": [
      1,
      0
    ],
    "questions": [
      1
    ]
  }
}
```
