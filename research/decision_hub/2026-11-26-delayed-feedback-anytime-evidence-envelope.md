# 自主学习：延迟及选择性反馈下的序贯证据保守包络
2026-11-26。RESEARCH_CANDIDATE / EXACT_FINITE_ENUMERATION_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线及去重
固定main ecb04fcdfd7aaa1c0cf7a0fbd25dd5944ed46136，核对20近期提交、15开放Draft PR、v3.2与同步规程前20行、唯一交接前20行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）、完整目录树相关题名。#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。读取既有 sequential-model-admission/README.md blob a2decfe7ff548aa98c94477c247bb50b6961a49f（R19 非负超鞅与重复审查，明确延迟缺失未解决）、feedback-replay-and-rollback/README.md f55a6fb6a801bb765b96530ce71b45e58d802852（反馈修订重放）、frozen-paired-forecast-cohort-feedback-bounds.md 799e4e0761a5544b1b6527ff69e594b51cbd369f（有限队列配对损失锐界）。本轮连接R19统计过程与固定发布序列的真值包含包络，不重做完整队列界、训练或真实反馈账本。引用仅既有项目研究记录，未重审原论文或新文献；去重非全库证明。
## 数学及严格成立条件
冻结共同事件/行动/结局定义及信息边界的配对预测，按事前固定发布顺序i排序，真实配对Brier改善d_i=(p_i-Y_i)^2-(q_i-Y_i)^2∈[-1,1]。潜在完整过滤族F_i必须使d_i可测、下注参数lambda_i及预测合同相对F_(i-1)可预测，零假设对每个i要求E[d_i|F_(i-1)]<=delta（0<=delta<1）；特别要求包含之前潜在未披露结果的完整历史条件下该性质仍成立。仅在观察到的反馈过滤族下的条件均值、边际均值或独立假设不足以替代此合同。重叠事件与提前信号可能破坏合同，未知时不作统计认证。沿R19因子 f_i(d)=1+lambda_i*(d-delta)/(1+delta)，0<=lambda_i<1。因子非负单调，M_k=prod_i<=k f_i(d_i) 是初值1非负超鞅；预设非负等权或固定归一化权重的多个此类过程之和亦然。Ville界 P_H0(sup_k M_k>=1/alpha)<=alpha。对每个报告时点t，只考察已事前发布的前缀k<=N(t)；每事件保留有资格的可能真实损失差集合D_i(t)，要求同时所有i,t的真实d_i∈D_i(t)（未证实/撤回/其他行动反馈为全二元结局，若配对预测本身仍合法可用；无合法预测或授权需暂停）。f单调，L_k(t)=prod f_i(min D_i(t))<=M_k，U同理用max。对具有非负lambda的固定混合过程，各分量同一最低d_i使其同时最小，最高亦同；在矩形支持下界锐利，相关约束下仍保守。未知项不丢弃、不乘1、不假定真实标签，仅计算证据下界。
令L*(t)=max_{k<=N(t)} L_k(t)（含k=0）。即使反馈到达/查询时点由结果决定，若上述路径包含及潜在过程假设均成立，任何t的越界事件都包含于潜在过程sup_k M_k越界事件，故错误概率不超过alpha。不需要L*(t)在观察过滤族中本身为超鞅，也不宣称它是e值或后验改善概率。可用最新合格反馈重评旧的固定前缀，不许事后选择预测版本、发布顺序、起点、方向、阈值、下注规则或样本资格。前缀本来就由同一Ville事件覆盖，多个不同起点/模型/方向必须另分配预设错误预算。若每次不确定集嵌套缩小且保持真值包含，固定前缀下界不下降；撤回导致集合扩大时当前证明可失效，不保留旧数值为当前证书。若已用错误单点而破坏真值包含，历史概率保证也不再成立；更正不能修复过去的错误拒绝。未核实暂定标签始终保留全支持。若有可靠的同时真值包含失败概率上界epsilon（本轮没有），可由并合界给alpha+epsilon上界，不可用未经核实的单次置信度代替。事实删除、授权撤回、版本隔离及真正科学资格仍独立门。反向退步可用事前冻结的-d和单独alpha，但本轮未运行反向检测或真实回退。所有输出authority NONE。
## 实际实验及限制
标准JS实际运行以下完整源码。压力案例旧概率0、新概率1，d=±1；IID公平标签为零假设，IID正标签概率0.75为人工备择，不是个人真实改善概率。delta=0、lambda=.5、单方向alpha=.05（阈值20），固定14次预测，报告至第18步；逐一枚举2^14全部路径，公平权重1/2^14，备择精确整数权重3^正数/4^14。四种反馈计划：立即、全部延迟4步、正反馈立即负反馈延迟4步、正反馈立即负反馈在观察窗内永不出现。故意错误基线只乘已知因子、缺失因子取1，对所有已发布前缀同样取最大；不声称为现有原生产品行为。记录截止14步及18步任意时点越界，核对每个报告时点保守包络不超过对应潜在前缀最大值，以及每条路径的越界包含；前三种完整反馈最终恢复精确潜在前缀最大。另5组不同预测对、3^5反馈支持、三个固定lambda混合，以所有可能标签穷举核对上下界；4专项控制含撤回和错误单点。当前短序列二进制浮点精确因子，混合平均共享三分母；长序列需对数域、可靠数值界、独立测试。
```json
{
  "n": 14,
  "T": 18,
  "threshold": 20,
  "paths": 16384,
  "lambda": 0.5,
  "pointwiseChecks": 1179648,
  "crossingSubsetChecks": 65536,
  "sharpMixtureChecks": 243,
  "completionChecks": 49152,
  "controls": 4,
  "rows": {
    "immediate": {
      "lower": {
        "nullCount": 232,
        "altWeight": 93953520,
        "byIssueEndNull": 232,
        "byIssueEndAlt": 93953520,
        "nullProbability": 0.01416015625,
        "altProbability": 0.3500041365623474,
        "byIssueEndNullProbability": 0.01416015625,
        "byIssueEndAltProbability": 0.3500041365623474
      },
      "skip": {
        "nullCount": 232,
        "altWeight": 93953520,
        "byIssueEndNull": 232,
        "byIssueEndAlt": 93953520,
        "nullProbability": 0.01416015625,
        "altProbability": 0.3500041365623474,
        "byIssueEndNullProbability": 0.01416015625,
        "byIssueEndAltProbability": 0.3500041365623474
      },
      "skipCrossWithoutLatent": 0
    },
    "fixed_delay_4": {
      "lower": {
        "nullCount": 232,
        "altWeight": 93953520,
        "byIssueEndNull": 64,
        "byIssueEndAlt": 26873856,
        "nullProbability": 0.01416015625,
        "altProbability": 0.3500041365623474,
        "byIssueEndNullProbability": 0.00390625,
        "byIssueEndAltProbability": 0.1001129150390625
      },
      "skip": {
        "nullCount": 232,
        "altWeight": 93953520,
        "byIssueEndNull": 64,
        "byIssueEndAlt": 26873856,
        "nullProbability": 0.01416015625,
        "altProbability": 0.3500041365623474,
        "byIssueEndNullProbability": 0.00390625,
        "byIssueEndAltProbability": 0.1001129150390625
      },
      "skipCrossWithoutLatent": 0
    },
    "outcome_delay_4": {
      "lower": {
        "nullCount": 232,
        "altWeight": 93953520,
        "byIssueEndNull": 232,
        "byIssueEndAlt": 93953520,
        "nullProbability": 0.01416015625,
        "altProbability": 0.3500041365623474,
        "byIssueEndNullProbability": 0.01416015625,
        "byIssueEndAltProbability": 0.3500041365623474
      },
      "skip": {
        "nullCount": 502,
        "altWeight": 125944956,
        "byIssueEndNull": 502,
        "byIssueEndAlt": 125944956,
        "nullProbability": 0.0306396484375,
        "altProbability": 0.46918152272701263,
        "byIssueEndNullProbability": 0.0306396484375,
        "byIssueEndAltProbability": 0.46918152272701263
      },
      "skipCrossWithoutLatent": 270
    },
    "positive_only": {
      "lower": {
        "nullCount": 232,
        "altWeight": 93953520,
        "byIssueEndNull": 232,
        "byIssueEndAlt": 93953520,
        "nullProbability": 0.01416015625,
        "altProbability": 0.3500041365623474,
        "byIssueEndNullProbability": 0.01416015625,
        "byIssueEndAltProbability": 0.3500041365623474
      },
      "skip": {
        "nullCount": 6476,
        "altWeight": 258162228,
        "byIssueEndNull": 6476,
        "byIssueEndAlt": 258162228,
        "nullProbability": 0.395263671875,
        "altProbability": 0.9617292433977127,
        "byIssueEndNullProbability": 0.395263671875,
        "byIssueEndAltProbability": 0.9617292433977127
      },
      "skipCrossWithoutLatent": 6244
    }
  },
  "latent": {
    "nullMass": 232,
    "altMass": 93953520,
    "nullProbability": 0.01416015625,
    "altProbability": 0.3500041365623474
  },
  "examples": [
    {
      "mode": "outcome_delay_4",
      "ds": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        -1,
        1,
        -1,
        -1,
        -1,
        -1,
        -1
      ],
      "skipCrossAt": 9,
      "latentMax": 17.0859375
    },
    {
      "mode": "positive_only",
      "ds": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        -1,
        1,
        -1,
        -1,
        -1,
        -1,
        -1
      ],
      "skipCrossAt": 9,
      "latentMax": 17.0859375
    }
  ]
}
```
## 下游与治理
该候选有意保守，反馈缺失可造成无法证明真实改善，不得将不触发解释为无改善。延迟或选择性披露不必然使潜在零假设成立，本轮IID仅有限示例，真实观察设计及条件均值仍未知；不能直接用于一般行动因果评价、非平稳个人环境或自动模型切换。未来需加入冻结发布收据、资格及授权、真实时间/事件、前缀版本与失效、跨版本及方向预算、独立真实反馈、变化检测和回退；独立轨保留未见评价样本。研究者自行选择阈值、下注参数、长度、延迟、概率和基线，非正式生产参数。没有执行训练、真实数据、原生入口、设备、生产修改、唯一交接修改、PR合并、部署、主动CI、费用或历史冻结/证据等级变化，未发新Codex任务。
## 可执行复算
Node标准JS，无依赖；实际执行为连接器JS，未另行运行Node命令行。
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)},n=14,T=n+4,threshold=20,range=n=>Array.from({length:n},(_,i)=>i);
 const modes=["immediate","fixed_delay_4","outcome_delay_4","positive_only"];
 const out={n,T,threshold,paths:2**n,lambda:0.5,pointwiseChecks:0,crossingSubsetChecks:0,sharpMixtureChecks:0,completionChecks:0,controls:0,rows:{},latent:{nullMass:0,altMass:0},examples:[]};
 for(const m of modes)out.rows[m]={lower:{nullCount:0,altWeight:0,byIssueEndNull:0,byIssueEndAlt:0},skip:{nullCount:0,altWeight:0,byIssueEndNull:0,byIssueEndAlt:0},skipCrossWithoutLatent:0};
 const factor=d=>1+d/2;
 function scan(ds,t,mode){
  let low=1,skip=1,lmax=1,smax=1;for(let i=0;i<Math.min(t,n);i++){
   const d=ds[i],delay=mode==="immediate"?0:mode==="fixed_delay_4"?4:mode==="outcome_delay_4"?(d===1?0:4):(d===1?0:T+1);
   const known=i+1+delay<=t;
   low*=known?factor(d):factor(-1);skip*=known?factor(d):1;
   lmax=Math.max(lmax,low);smax=Math.max(smax,skip);
  }return {lmax,smax,low};
 }
 for(let mask=0;mask<2**n;mask++){
  const ds=range(n).map(i=>mask&(1<<i)?1:-1),k=ds.filter(x=>x===1).length,w=3**k;let p=1,full=[1];for(let d of ds){p*=factor(d);full.push(Math.max(full.at(-1),p))}
  const crossed=full[n]>=threshold;out.latent.nullMass+=+crossed;out.latent.altMass+=crossed?w:0;
  for(const m of modes){let lc=0,sc=0;for(let t=1;t<=T;t++){const a=scan(ds,t,m);ck(a.lmax<=full[Math.min(t,n)],"pointwise envelope");out.pointwiseChecks++;if(a.lmax>=threshold&&!lc)lc=t;if(a.smax>=threshold&&!sc)sc=t;if(t===T&&m!=="positive_only"){ck(a.lmax===full[n],"complete max");out.completionChecks++}}
   ck(!lc||crossed,"crossing subset");out.crossingSubsetChecks++;const r=out.rows[m];for(const [key,c] of [["lower",lc],["skip",sc]])if(c){r[key].nullCount++;r[key].altWeight+=w;if(c<=n){r[key].byIssueEndNull++;r[key].byIssueEndAlt+=w}}
   if(sc&&!crossed){r.skipCrossWithoutLatent++;if(out.examples.length<2)out.examples.push({mode:m,ds,skipCrossAt:sc,latentMax:full[n]})}
  }
 }
 const den0=2**n,den1=4**n;out.latent.nullProbability=out.latent.nullMass/den0;out.latent.altProbability=out.latent.altMass/den1;
 for(const r of Object.values(out.rows))for(const key of ["lower","skip"]){let q=r[key];q.nullProbability=q.nullCount/den0;q.altProbability=q.altWeight/den1;q.byIssueEndNullProbability=q.byIssueEndNull/den0;q.byIssueEndAltProbability=q.byIssueEndAlt/den1}
 // Five different frozen paired predictions, lambda mixture. Values are exact dyadic.
 const preds=[[0,1],[1,0],[.25,.75],[.75,.25],[.5,.5]],L=[.25,.5,.75],supports=[[0],[1],[0,1]],diff=(a,b,y)=>(a-y)**2-(b-y)**2;
 const mixture=ds=>L.reduce((s,l)=>s+ds.reduce((p,d)=>p*(1+l*d),1),0)/L.length;
 for(let mask=0;mask<3**preds.length;mask++){
  let z=mask,sets=[];for(let i=0;i<preds.length;i++){let [a,b]=preds[i];sets.push(supports[z%3].map(y=>diff(a,b,y)));z=Math.floor(z/3)}
  const lb=mixture(sets.map(s=>Math.min(...s))),ub=mixture(sets.map(s=>Math.max(...s))),all=[];function visit(i,ds){if(i===sets.length){all.push(mixture(ds));return}for(const d of sets[i])visit(i+1,[...ds,d])}visit(0,[]);
  ck(lb===Math.min(...all)&&ub===Math.max(...all),"sharp mixture");out.sharpMixtureChecks++;
 }
 // Correction control: remove eligibility before narrowing support again; old certificate is not current.
 const exact=Array(8).fill(1),unknown=Array(8).fill(-1),certificate=ds=>ds.reduce((v,d)=>v*factor(d),1);
 ck(certificate(exact)>=threshold&&certificate(unknown)<threshold,"withdrawal removes live certificate");out.controls++;
 ck(certificate(exact.map((d,i)=>i===0?-1:d))<threshold,"counterexample mistaken singleton");out.controls++;
 ck(certificate(exact.map((d,i)=>i===0?-1:d))===certificate([ -1,...Array(7).fill(1)]),"pending lower");out.controls++;
 // An uncertified positive placeholder cannot be treated as a singleton.
 ck(certificate(unknown)<=certificate(Array(8).fill(-1))&&certificate(exact)>certificate(Array(8).fill(-1)),"provisional report");out.controls++;
 return out;
}
console.log(JSON.stringify(experiment(),null,2));
```
