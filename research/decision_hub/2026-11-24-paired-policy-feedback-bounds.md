# 第44轮：选择性反馈下新旧决策策略的配对界限和分组退步审查
2026-11-24。固定 main 912e740595ce7759d55829b5dead0093fd0b5399；PR #61 HEAD 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e，open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一协调交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第34/43轮；实际读取第18轮反馈重放（9bba8270025341979c8f1cc3daec4fb97da0c587）、第19轮序贯审查（481d395603a89efd9bc3c014dddfcbda76f98d53）、第20轮预测与行动价值（7facdce9bd50b6e2487d307155e992b4d371d34e）、第21轮NSW离线策略（76bc0b60db38ddf21949fda4e72290b91c498ace）及C028 Manski候选记录（58abceb54b961ec5afd932f4d7aed8d2644833a3）。既有C028研究群体平均干预边界，NSW研究有条件IPW/AIPW，既有顺序统计研究同事件预测；本轮新增有限同案例的旧新策略净值直接配对界、同动作抵消、缺失观察、成本与预设分组退步门。C028是历史候选同编号，不改变原生区间硬约束C028或任何历史记录。本轮只用仓库已有研究记录及原创有限证明，不重审外部文献、不开展R项或重新计既有成果。搜索发现MKT128/TH055/TH057及历史反事实相关提交，仅核对题名，不断言全库无重复。
## 数学合同
固定有限评价事件i及非负固定权重w_i（实际实验等权，报告整数总差；除以组内权重和得到均值）。两策略o_i,n_i在结果出现前冻结，基于同决策时点、同输入、同候选资格、相同目标及价值尺度；两者只决定当前行动。实际执行a_i，已观察Y_i(a_i)或结果缺失；潜在结果Y_i(a)仅在可信闭界[l_ia,u_ia]内，已核实观察固定其对应区间。需一致性、行动版本/时点明确、可比结果、无未建模跨事件干扰；没有随机分配/交换性/倾向概率要求。不同潜在结果在给定界内可自由组合（若有相关或总量限制，所得界为外界而非锐界）。未选结果保持未观察，不能利用模型预测补成事实。同一行动的同一潜在结果共享身份；若两策略对相同行动施加不同执行、支持、时机或成本且影响结果，须先定义不同完整干预，不能误抵消。
在o_i=n_i且完整执行及成本相同时，该行真实差恒为0，即便结果缺失；否则效果差区间为[l_i,n-u_i,o, u_i,n-l_i,o]，若行动已知确定成本差c_i以同尺度计入，则整体减c_i。各行加权求和给出配对差D的上下界，端点可由各行独立端点同时取得，因此在明示矩形合同中为锐界。若先分别计算两策略总收益的边际区间再相减，会对共享潜在结果允许互相矛盾取值，故可能严格更宽。全部已观察与未观察结果仅在[0,1]、每行最多一行动结果观察、无额外信息及相同成本时，每个行差区间均包含0（缺失值可与已观察值相等），故整体也包含0，不能仅凭此类反馈证实严格改善或退步。这是有限样本识别事实，不是统计置信区间或未来效果。只有更强合格界、已知成本或独立数据等才能收紧。
候选升级审查示例：总改善下界严格超过事前门槛且所有预设关键组差下界不低于允许退步容忍线，硬约束/隐私/资格独立通过，才得到有限评价集内相应证书。未确定门槛或成本尺度不能自动判定。某组上界为负可确定该组退步；跨零则未识别，不能以整体收益抵消。不得事后挑组、将重复个人记录当独立样本、把群体界套为个人因果效果，或自动晋级。新独立留出、抽样/依赖/漂移、序贯统计及所有者授权仍独立必要。缺失结果保持缺失；可核实的已选结果预测评分可依既有第18/19轮处理，不能声称候选决策效果已证明。
## 实际实验
3条人工评价记录，各24种（实际行动2、观察0/1/缺失、旧新推荐各2），13824组；对每条所有与观察一致的二元潜在结果配对，逐世界穷举核对总量与预设组{0}、{1,2}的锐界；再比较错误忽略共享身份的边际相减基线与分别计算日志匹配行均值的描述性基线（两策略匹配样本不同，不具因果资格）。naiveUnidentified表示匹配均值新高于旧却不能证明严格改善；naiveFalseGain为匹配均值新高于旧但真实差上界<=0，不能将其解释成实际产品错误率。第二实验使用同样记录、二元结果0/2、六组虚构且完全已知的成本差；相同行动成本差强制0，成本差允许为负；大额成本差只是压力案例，不代表真实价值。共82944组，独立逐潜在结果穷举同样三个范围；costAdmit仅为示例数值门总下界>0且两组下界>=0；costGroupFail为总量通过但某组上界<0，costGroupUncertain为总量通过但仍至少一组下界<0且无组确定负。未测试统计效应、真正分组公平、用户成本权重、真实数据或上线资格。两种算法同一研究者设计，非独立验收。
```js
function experiment(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 // Each row: observed action, observed outcome (null = missing), frozen old and new recommendations.
 const rows=[];
 for(const a of [0,1])for(const y of [0,1,null])for(const old of [0,1])for(const fresh of [0,1])rows.push({a,y,old,fresh});
 const groups=[[0,1,2],[0],[1,2]];
 const add=(x,y)=>[x[0]+y[0],x[1]+y[1]];
 const range=(r,a)=>r.a===a&&r.y!==null?[r.y,r.y]:[0,1];
 function pair(r){
  if(r.old===r.fresh)return [0,0];
  const n=range(r,r.fresh),o=range(r,r.old);return [n[0]-o[1],n[1]-o[0]];
 }
 function worlds(r){
  const all=[];for(let a=0;a<=1;a++)for(let b=0;b<=1;b++)if(r.y===null||[a,b][r.a]===r.y)all.push([a,b]);return all;
 }
 function marginal(rs,g){
  const o=g.reduce((v,i)=>add(v,range(rs[i],rs[i].old)),[0,0]);
  const n=g.reduce((v,i)=>add(v,range(rs[i],rs[i].fresh)),[0,0]);
  return [n[0]-o[1],n[1]-o[0]];
 }
 const equal=(a,b)=>a[0]===b[0]&&a[1]===b[1];
 let cases=0,completionChecks=0,groupChecks=0,tighter=0,strictGain=0,strictLoss=0,uncertain=0,tie=0,meanPassGroupFail=0,meanPassGroupUncertain=0,admit=0,missedByMarginal=0,naiveFalseGain=0,naiveEligible=0,naiveUnidentified=0;
 let witness=null,subgroupWitness=null,naiveWitness=null;
 for(const x of rows)for(const y of rows)for(const z of rows){
  const rs=[x,y,z],exact=groups.map(g=>g.reduce((v,i)=>add(v,pair(rs[i])),[0,0]));
  const brute=groups.map(()=>[Infinity,-Infinity]);cases++;
  for(const u of worlds(x))for(const v of worlds(y))for(const w of worlds(z)){
   const all=[u,v,w],d=rs.map((r,i)=>all[i][r.fresh]-all[i][r.old]);completionChecks++;
   groups.forEach((g,k)=>{const t=g.reduce((s,i)=>s+d[i],0);brute[k][0]=Math.min(brute[k][0],t);brute[k][1]=Math.max(brute[k][1],t);});
  }
  exact.forEach((v,i)=>{check(equal(v,brute[i]),"sharp paired bounds");groupChecks++;});
  const m=marginal(rs,groups[0]),p=exact[0];
  check(m[0]<=p[0]&&m[1]>=p[1],"marginal outer");
  if(!equal(m,p))tighter++;
  if(p[0]>0){strictGain++;if(m[0]<=0)missedByMarginal++;if(!witness&&m[0]<=0)witness={rs,paired:p,marginal:m,groups:exact};}
  else if(p[1]<0)strictLoss++;
  else if(equal(p,[0,0]))tie++;else uncertain++;
  if(p[0]>0){
   if(exact.slice(1).every(v=>v[0]>=0))admit++;
   else if(exact.slice(1).some(v=>v[1]<0)){meanPassGroupFail++;if(!subgroupWitness)subgroupWitness={rs,groups:exact};}
   else meanPassGroupUncertain++;
  }
  const old=rs.filter(r=>r.y!==null&&r.a===r.old).map(r=>r.y);
  const fresh=rs.filter(r=>r.y!==null&&r.a===r.fresh).map(r=>r.y);
  if(old.length&&fresh.length){
   naiveEligible++;
   if(fresh.reduce((a,b)=>a+b,0)*old.length>old.reduce((a,b)=>a+b,0)*fresh.length){
    if(p[0]<=0)naiveUnidentified++;
    if(p[1]<=0){naiveFalseGain++;if(!naiveWitness)naiveWitness={rs,old,fresh,paired:p};}
   }
  }
 }
 // Distinguish missing outcomes from identical recommendations. Independently check known cost differences.
 const costs=[{a:0,y:null,old:0,fresh:0},{a:1,y:1,old:0,fresh:1}];
 const bounds=costs.reduce((v,r)=>add(v,pair(r)),[0,0]);check(equal(bounds,[0,1]),"missing unchanged cancels");
 // Candidate can be worse in one subgroup even with a positive lower overall when n=4.
 const four=[{a:0,y:0,old:0,fresh:1},{a:0,y:0,old:0,fresh:1},{a:0,y:0,old:0,fresh:1},{a:0,y:1,old:0,fresh:1}];
 // Binary outcomes with only chosen observed: each discordant row has 0 in range, so strict guaranteed nonzero needs external bounds or known net costs.
 check(strictGain===0&&strictLoss===0,"no strict identification from binary one-arm records");
 // Known action-specific deterministic costs (same outcome scale). In units of half outcome:
 // y in {0,2}, incremental cost known -1,0,+1; pair reward range scaled then subtract cost.
 let costCases=0,costChecks=0,costGain=0,costLoss=0,costAdmit=0,costGroupFail=0,costGroupUncertain=0,costTighter=0,costMiss=0;
 let costWitness=null,costGroupWitness=null;
 for(const x of rows)for(const y of rows)for(const z of rows){
  const rs=[x,y,z];
  for(const costs of [[0,0,0],[1,1,1],[-1,-1,-1],[1,-1,0],[-2,-2,2],[-3,-3,3]]){
   // per row difference in costs of fresh vs old, zero if action identical
   const cs=rs.map((r,i)=>r.old===r.fresh?0:costs[i]);
   const e=groups.map(g=>g.reduce((v,i)=>{const p=pair(rs[i]);return add(v,[2*p[0]-cs[i],2*p[1]-cs[i]])},[0,0]));
   const b=groups.map(()=>[Infinity,-Infinity]);costCases++;
   for(const u of worlds(x))for(const v of worlds(y))for(const w of worlds(z)){
    const all=[u,v,w],d=rs.map((r,i)=>2*(all[i][r.fresh]-all[i][r.old])-cs[i]);
    groups.forEach((g,k)=>{const t=g.reduce((s,i)=>s+d[i],0);b[k][0]=Math.min(b[k][0],t);b[k][1]=Math.max(b[k][1],t);});
   }
   e.forEach((v,i)=>{check(equal(v,b[i]),"cost oracle");costChecks++;});
   const m=marginal(rs,groups[0]),c=cs.reduce((a,b)=>a+b,0),mm=[2*m[0]-c,2*m[1]-c];
   if(!equal(e[0],mm))costTighter++;
   if(e[0][1]<0)costLoss++;
   if(e[0][0]>0){
    costGain++;
    if(mm[0]<=0){costMiss++;if(!costWitness)costWitness={rs,cs,paired:e[0],marginal:mm};}
    if(e.slice(1).every(v=>v[0]>=0))costAdmit++;
    else if(e.slice(1).some(v=>v[1]<0)){costGroupFail++;if(!costGroupWitness)costGroupWitness={rs,cs,groups:e};}
    else costGroupUncertain++;
   }
  }
 }
 check(costGain===costAdmit+costGroupFail+costGroupUncertain,"partition");
 // Same unknown outcome cannot independently take two different values. Missing never becomes zero.
 return {cases,completionChecks,groupChecks,tighter,strictGain,strictLoss,uncertain,tie,naiveEligible,naiveUnidentified,naiveFalseGain,naiveWitness,costCases,costChecks,costGain,costLoss,costAdmit,costGroupFail,costGroupUncertain,costTighter,costMiss,costWitness,costGroupWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际输出
```json
{
  "cases": 13824,
  "completionChecks": 262144,
  "groupChecks": 41472,
  "tighter": 9728,
  "strictGain": 0,
  "strictLoss": 0,
  "uncertain": 12096,
  "tie": 1728,
  "naiveEligible": 7360,
  "naiveUnidentified": 1392,
  "naiveFalseGain": 0,
  "naiveWitness": null,
  "costCases": 82944,
  "costChecks": 248832,
  "costGain": 11328,
  "costLoss": 5824,
  "costAdmit": 10944,
  "costGroupFail": 0,
  "costGroupUncertain": 384,
  "costTighter": 58368,
  "costMiss": 7168,
  "costWitness": {
    "rs": [
      {
        "a": 0,
        "y": 0,
        "old": 0,
        "fresh": 0
      },
      {
        "a": 0,
        "y": 0,
        "old": 0,
        "fresh": 1
      },
      {
        "a": 0,
        "y": 0,
        "old": 1,
        "fresh": 1
      }
    ],
    "cs": [
      0,
      -1,
      0
    ],
    "paired": [
      1,
      3
    ],
    "marginal": [
      -1,
      5
    ]
  },
  "costGroupWitness": null
}
```
## 接入
B08/B09/B10/B11候选增量。决策记录冻结两策略版本、同一原始问题、决策时信息、完整行动身份、用户确认、真实执行、结果到期时间、合法成本与证据界；用户拒绝保存时不收集复盘资料。每次到期按真实可观察数据更新区间，保留未选和未到期结果；旧预测、权重、版本不覆盖。结果修订触发重新复算，不能继承原序贯检验保证。输出配对改善区间、样本覆盖及分组限制、结果是否识别、额外证据需求；对可确定关键退步启动隔离审查并按授权治理，不自动改变模型。所有组门槛、权重、价值尺度、更新策略必须独立确认。独立轨冻结未见同动作不同干预、未到期/撤回、已观察与未选混淆、成本不明、组别事后选择、真实分组身份、反事实预测填补、干扰、漂移及独立留出；数据轨核查真实识别条件；产品轨解释不确定性及用户同意；模型轨审查联合约束、序贯推断、可比策略评价。未运行生产、Qwen、真实设备、真人或独立验收，不启动Codex、CI、训练、合并、部署、冻结协议变更；零新增费用。
