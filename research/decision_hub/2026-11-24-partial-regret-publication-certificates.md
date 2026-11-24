# 第48轮：部分计算的发布前自检、后悔值上下界及停止证书
2026-11-24。固定 main a78b48c24819dfd729d55a3068fe4b481c116456；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一协调交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第6/27/46/47轮。原生 decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f 已有validate_gate、run_method的适用性及异常处理；decision_registry.py 8046de09674af850a456bbccc534e5f6c2511497 已有validate/execute契约；decision_planner.py f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b 已有条件性proof字段、分歧提示。查重 certificate/self-check/quality gate/proof carrying/metamorphic/interval arithmetic，发现C031 regret precision（9391033241305bc51e09f11f26160b933cee2247）、C034相关证书及独立留出提交，只有题名核对；不声称全库无相同研究或原生存在本轮模拟错误。区别于既有数值精度、局部分析、收据复算和预算规划，本轮新增有限完整情景清单中尚未计算的情景上界、全部最优集合发布证书及提前停止控制。原创有限证明，无新增外部文献事实。
## 数学合同
固定已获资格的非空有限情景W及所有已通过必要硬约束的固定可比行动A，共同效用单位及用户确认的最小最大后悔准则。比较范围不能任意缩小。情景w中所有行动的真实效用u_wa，已计算情景集合S中可信点值已独立取得；其余情景有来源明确的有限效用外界[l_wa,h_wa]，绝非默认范围或统计置信区间自动当硬界。情景身份、模型版本、证据、截止、行动资格及授权必须来自可信宿主；不能由待验证输出自报。若情景清单不完整、上界不可信、行动资格不明或模型不适用，不能提供本证书。无合法行动或风险门未通过时停止完整推荐。未知未计算与不可计算须区分。
R_a=max_w max_b(u_wb-u_wa)为最坏后悔。已计算情景中L_a=max(0,max_{w∈S,b∈A}(u_wb-u_wa))，尚未计算情景上界C_wa=max(0,max_{b≠a}(h_wb-l_wa))，U_a=max(L_a,max_{w∉S} C_wa)。逐项界得到L_a<=R_a<=U_a。b=a的差恒0，不能当独立变量相减。这里各情景共享约束也可使用有效外界，但不声称区间锐利。可排除行动若L_a>min_b U_b；剩余P为真实全局最优集合的外包，并不保证每个P成员可在联合效用域成为最优。保证最优集合G={a: 对所有b≠a有U_a<=L_b}；严格唯一集合Q用严格不等式。由逐项比较证明G包含于真实最优集合，且真实最优集合包含于P。G=P时能确定全部并列，不必计算剩余情景；G非空而不等于P时可报告保证最优行动及其他可能并列者；P非空但G空仅表示未决，不能将区间中点或已算情景领导冒充全局最优。G=P在此合同内必非空。全量计算时L=U=R，G=P为完整领导集合。证书成立仍不保证实际未来效用或唯一人生理性目标。
## 自检合同
生产器按情景最大值计算L/U；核验器从可信固定情景/行动清单、已算点值及未算合法外界重新逐对计算差分，检查完整身份、范围、资格与边界一致性，再复核全部输出字段，拒绝篡改范围、遗漏情景、伪造界限、错误领导、失效身份及未过硬门。本轮固定三情景三行动，identity/gate为人工布尔可信宿主标记，不是实际鉴权、哈希或持久化实现。核验器与生产器同研究者编写、共享可信输入、相同数学合同；同源数据错误、遗漏模型义务、错误效用或不当假设无法由此检测。不得因证书通过就跳过独立验收。分析预算耗尽仍可提供已证界和局部输出，明确未计算内容，不把停止变成最优。
## 实验
3^9=19683整数效用表（0/1/2），8个已算情景子集，两类合成外界：mode0所有[0,2]；mode1对真实0用[0,1]、1用[0,2]、2用[1,2]。后一外界由完整人工真值生成，仅模拟外部已获资格的粗界，不是现实可获取的预测证据。总314928例，按实际完整效用表计算真实最优，验证L/U、P/G/Q及全部并列。naiveWrong为仅取已算最大后悔的领导集合与完整真值不同（空扫描时全并列）；naiveUnjustified为该基线含至少一个未获保证的行动。strictExclusion为P严格小于全行动集。固定前缀顺序0,1,2的提前停止仅当G=P，不读取未来点值，mode1的可信粗界视作先验可用；earlyScans为省略的情景计算次数，不是实际耗时，两个mode是同一人工表的不同证据合同，不能合计称独立样本。每197个效用表对所有扫描域与两种界进行8类字段篡改及2类资格负控，均需拒绝；未覆盖任意程序漏洞。两算法非独立验收。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)}, A=[0,1,2],W=[0,1,2],full=7;
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const leaders=v=>A.filter(a=>v[a]===Math.min(...v));
 const cap=(box,a)=>Math.max(0,...A.filter(b=>b!==a).map(b=>box[b][1]-box[a][0]));
 function build(boxes,scanned,mask){
  const L=A.map(a=>Math.max(0,...W.filter(w=>mask&(1<<w)).map(w=>Math.max(...scanned[w])-scanned[w][a])));
  const U=A.map(a=>Math.max(L[a],...W.filter(w=>!(mask&(1<<w))).map(w=>cap(boxes[w],a))));
  const possible=A.filter(a=>L[a]<=Math.min(...U));
  const guaranteed=A.filter(a=>A.every(b=>b===a||U[a]<=L[b]));
  const unique=A.filter(a=>A.every(b=>b===a||U[a]<L[b]));
  return {L,U,possible,guaranteed,unique};
 }
 // Checker starts from trusted source contract, not claimed caps or caller-selected scope.
 function verify(c,boxes,actualScan,mask,identity,gate){
  if(!gate||!identity||c.mask!==mask||!eq(c.ids,W)||!eq(c.actions,A))return false;
  if(!Number.isInteger(mask)||mask<0||mask>7)return false;
  for(const w of W)for(const a of A){
   const b=boxes[w]?.[a];
   if(!b||b.length!==2||!b.every(Number.isFinite)||b[0]>b[1])return false;
   if(mask&(1<<w)){
    const x=actualScan[w]?.[a];
    if(!Number.isFinite(x)||x<b[0]||x>b[1])return false;
   }
  }
  // Separately compute pairwise regrets, checking the unscanned upper bound for each rival.
  const lower=[0,0,0],upper=[0,0,0];
  for(const w of W)for(const a of A)for(const b of A){
   if(a===b)continue;
   if(mask&(1<<w)){
    const d=actualScan[w][b]-actualScan[w][a];lower[a]=Math.max(lower[a],d);upper[a]=Math.max(upper[a],d);
   }else upper[a]=Math.max(upper[a],boxes[w][b][1]-boxes[w][a][0]);
  }
  const p=[],g=[],u=[];
  for(const a of A){
   if(!A.some(b=>upper[b]<lower[a]))p.push(a);
   if(!A.some(b=>b!==a&&lower[b]<upper[a]))g.push(a);
   if(!A.some(b=>b!==a&&lower[b]<=upper[a]))u.push(a);
  }
  return eq(c.L,lower)&&eq(c.U,upper)&&eq(c.possible,p)&&eq(c.guaranteed,g)&&eq(c.unique,u);
 }
 let cases=0,partial=0,checks=0,guaranteed=0,unique=0,exactSet=0,naiveWrong=0,naiveUnjustified=0,strictExclusion=0,fullChecks=0,mutations=0,mutationRejected=0,earlyCases=0,earlyScans=0;
 const byMode=[];
 let witness=null,earlyWitness=null;
 for(let mode=0;mode<2;mode++){
  let n=0,gu=0,un=0,ex=0,wrong=0,early=0,saved=0;
  for(let code=0;code<19683;code++){
   let z=code;const actual=W.map(()=>A.map(()=>{const x=z%3;z=Math.floor(z/3);return x;}));
   const box=actual.map(row=>row.map(x=>mode===0?[0,2]:x===0?[0,1]:x===1?[0,2]:[1,2]));
   const R=A.map(a=>Math.max(...actual.map(row=>Math.max(...row)-row[a])));
   const trueL=leaders(R);
   let first=3;
   for(let mask=0;mask<=full;mask++){
    cases++;const scan=actual.map((row,w)=>mask&(1<<w)?row:null);
    const c={...build(box,scan,mask),mask,ids:W,actions:A};
    check(verify(c,box,scan,mask,true,true),"independent certificate");checks++;
    for(const a of A)check(c.L[a]<=R[a]&&R[a]<=c.U[a],"actual bound");
    check(trueL.every(a=>c.possible.includes(a)),"possible superset");
    check(c.guaranteed.every(a=>trueL.includes(a)),"guaranteed subset");
    check(!c.unique.length||eq(c.unique,trueL)&&trueL.length===1,"unique sound");
    if(mask===7){check(eq(c.possible,trueL)&&eq(c.guaranteed,trueL),"complete ties");fullChecks++;}
    else{
     partial++;n++;
     if(c.guaranteed.length){guaranteed++;gu++;}
     if(c.unique.length){unique++;un++;}
     if(eq(c.guaranteed,c.possible)){exactSet++;ex++;}
     if(c.possible.length<3)strictExclusion++;
     const naive=leaders(c.L);
     if(!eq(naive,trueL)){naiveWrong++;wrong++;if(!witness)witness={mode,actual,mask,naive,truth:trueL,L:c.L,U:c.U,possible:c.possible,guaranteed:c.guaranteed};}
     if(naive.some(a=>!c.guaranteed.includes(a)))naiveUnjustified++;
     // Fixed prefix scan order: no selection based on hidden outcomes.
     if([0,1,3].includes(mask)&&eq(c.guaranteed,c.possible)){
      const count=mask===0?0:mask===1?1:2;first=Math.min(first,count);
      if(!earlyWitness)earlyWitness={mode,actual,mask,certificate:c};
     }
    }
    if(code%197===0){
     const ms=[{...c,L:c.L.map((v,a)=>a===0?v+1:v)},{...c,U:c.U.map((v,a)=>a===0?v-1:v)},{...c,mask:mask^1},{...c,ids:[0,1]},{...c,actions:[0,1]},{...c,possible:c.possible.includes(0)?c.possible.filter(a=>a!==0):[0,...c.possible]},{...c,guaranteed:c.guaranteed.includes(0)?c.guaranteed.filter(a=>a!==0):[0,...c.guaranteed]},{...c,unique:c.unique.includes(0)?c.unique.filter(a=>a!==0):[0,...c.unique]}];
     for(const m of ms){mutations++;if(!verify(m,box,scan,mask,true,true))mutationRejected++;else throw Error("mutant accepted");}
     for(const [identity,gate] of [[false,true],[true,false]]){mutations++;check(!verify(c,box,scan,mask,identity,gate),"authorization control");mutationRejected++;}
    }
   }
   if(first<3){earlyCases++;early++;earlyScans+=3-first;saved+=3-first;}
  }
  byMode.push({mode,partial:n,guaranteed:gu,unique:un,exactSet:ex,naiveWrong:wrong,earlyCases:early,savedScans:saved});
 }
 check(naiveWrong>0&&earlyCases>0&&mutationRejected===mutations,"coverage");
 return {cases,partial,checks,guaranteed,unique,exactSet,naiveWrong,naiveUnjustified,strictExclusion,fullChecks,mutations,mutationRejected,earlyCases,earlyScans,byMode,witness,earlyWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际结果
```json
{
  "cases": 314928,
  "partial": 275562,
  "checks": 314928,
  "guaranteed": 69537,
  "unique": 8046,
  "exactSet": 13302,
  "naiveWrong": 163992,
  "naiveUnjustified": 213480,
  "strictExclusion": 29970,
  "fullChecks": 39366,
  "mutations": 16000,
  "mutationRejected": 16000,
  "earlyCases": 4059,
  "earlyScans": 4434,
  "byMode": [
    {
      "mode": 0,
      "partial": 137781,
      "guaranteed": 23328,
      "unique": 0,
      "exactSet": 1944,
      "naiveWrong": 81996,
      "earlyCases": 648,
      "savedScans": 648
    },
    {
      "mode": 1,
      "partial": 137781,
      "guaranteed": 46209,
      "unique": 8046,
      "exactSet": 11358,
      "naiveWrong": 81996,
      "earlyCases": 3411,
      "savedScans": 3786
    }
  ],
  "witness": {
    "mode": 0,
    "actual": [
      [
        1,
        0,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        0
      ]
    ],
    "mask": 0,
    "naive": [
      0,
      1,
      2
    ],
    "truth": [
      0
    ],
    "L": [
      0,
      0,
      0
    ],
    "U": [
      2,
      2,
      2
    ],
    "possible": [
      0,
      1,
      2
    ],
    "guaranteed": []
  },
  "earlyWitness": {
    "mode": 0,
    "actual": [
      [
        0,
        2,
        0
      ],
      [
        2,
        0,
        0
      ],
      [
        0,
        0,
        0
      ]
    ],
    "mask": 3,
    "certificate": {
      "L": [
        2,
        2,
        2
      ],
      "U": [
        2,
        2,
        2
      ],
      "possible": [
        0,
        1,
        2
      ],
      "guaranteed": [
        0,
        1,
        2
      ],
      "unique": [],
      "mask": 3,
      "ids": [
        0,
        1,
        2
      ],
      "actions": [
        0,
        1,
        2
      ]
    }
  }
}
```
## 接入
B05/B06/B07/B08/B10/B11候选增量。在模型输出、图表和建议前引入固定方法合同与可信输入的可复算证书；区分保证最优、可能最优、已排除、未决及未计算，保留全并列。重要风险与授权独立门控；局部结果依赖不受影响时可以继续展示，完整建议需全部必要义务通过。任何输入、候选、效用、情景、授权、版本变化须重新核验，不能沿用旧停止证书。实际连续域、相关效用锐界、可适用的搜索上界、完整性绑定与并发发布、真实计算耗时、真实语言及用户解释均待研究。独立轨预留漏情景、失效来源、错误外界、共同错误、同值并列、空输入、权重更正、越界概率及图文错配；产品轨核查证书解释；模型轨研究不同方法的独立验证器。无生产修改、Codex、CI、Qwen训练、合并、部署、冻结协议变更或新增费用。真实产品与独立验收未执行。
