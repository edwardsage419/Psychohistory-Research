# 自主学习：未知退化起点的预算化序贯监测
2026-11-26。RESEARCH_CANDIDATE / EXACT_FINITE_ENUMERATION_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线及去重
固定main 66cda90a4eb83999714e7bdbeb02b5008898d6a9，核对20近期提交、15开放Draft PR、v3.2与同步规程前20行、唯一交接前20行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）、完整目录树退化/变化点/回退/序贯/跟踪题名。#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。既有 sequential-model-admission/README.md blob a2decfe7ff548aa98c94477c247bb50b6961a49f 已研究单次序贯、跨轮错误预算及已知反转点；feedback-replay-and-rollback/README.md f55a6fb6a801bb765b96530ce71b45e58d802852 已研究版本重放；delayed-feedback-anytime-evidence-envelope.md 4168eb54e9c3421cb0e8aecad7d92f5ccadbaecb 已研究固定起点缺失反馈包络。本轮新增未知退化起点的预分配资本混合及在线递推，并验证延迟包络，非重复模型权重跟踪或真正回退。目录查重非全库证明。仅使用既有研究记录及原创推导，未重审原论文。
## 数学合同
固定版本的现用模型与合格参照，对同一事件/行动/结局/信息边界冻结配对预测。z_i=现用Brier损失减参照Brier损失，正为现用退步。潜在完整过滤族F_i及可预测性沿用前轮；无退化零假设要求所有i E[z_i|F_(i-1)]<=delta。它是逐时条件均值约束，不是一般平稳性、边际平均或因果假设。若未知则不作统计认证。设 f_i(z)=1+lambda_i(z-delta)/(1+delta)，0<=delta<1，0<=lambda_i<1，z∈[-1,1]。每个预定起点s的过程 M^s_k 在k<=s时为1，之后为从i=s+1到k的因子乘积。各过程在H0下为非负超鞅。对事前固定非负权重w_s且总和1，M_k=Σw_s M^s_k，初值1，Ville界 P_H0(sup M_k>=1/alpha)<=alpha。可替代地给起点分别分配alpha*w_s并取并合界。后验挑最高起点并使用未分割阈值无同等保证。监测起点是可疑退化窗口，不证明真正环境变点或原因。
同一因子序列的混合可线性递推：A_0=0；A_k=(A_(k-1)+w_(k-1))*f_k；M_k=A_k+Σ_{s>=k}w_s。未启动资本始终为1倍权重，不能当已观测证据。无限期可用预设可求和的起点权重及剩余资本，但本轮仅有限期。单步常数复杂度需要O(1)提供当前权重及剩余权重；实际实验为短序列JS，数组查找未优化，未测性能。若不同起点使用不同自适应下注因子则该递推不适用。选择性反馈时沿前轮，用合格D_i(t)最小z替换全体已发布事件的因子，重算每个固定前缀混合下界；共享单调因子与非负权重保证逐前缀L<=M，任意报告时点及历史前缀越界仍属于同一Ville事件。无合法预测/授权或真值包含不足则暂停；更正曾错误排除真值不能修复历史保证。当前证据撤回后必须重算，不能复用已失效证书。此处没有新统计假设证明或真实反馈。
更新治理：统计退化提示仅触发审查，不自动回退。硬约束、隐私、来源资格、版本完整性失效不等待统计阈值。参照版本本身须当前合格，回退另经授权；否则安全降级或暂停。多领域/模型/方向/重复监测须预分配全局错误预算，不能把单次alpha当全系统风险。旧版本成绩不证明未来适用。
## 实际实验
标准JS实际执行。20次二元极端Brier差z=±1，delta=0，lambda=.75，单方向alpha=.05，阈值20。五种策略固定起点、5个等权起点(0/4/8/12/16)混合、20个等权起点混合、5起点各alpha/5并合门、无预算任意起点扫描。枚举2^20完整路径；四人工概率环境：公平IID零假设、早期变化(前4次正概率.25后.875)、后期变化(前12次.25后.875)、一直.25。正为退步；概率均为合成设定而非真实个人风险。每个环境计算有限期任意首次越界质量，变化前误报及变化后首次越界质量、条件平均延迟。双精度加总，核验质量，非符号有理数全程计算。短期14步额外2^14路径、4个等权起点，正反馈概率前4步.25后.75，检查即时/固定延迟3/仅正反馈三种计划；直接起点乘积对照递推（短序列dyadic精确），所有报告前缀保守包络和越界包含，完整反馈最终恢复。结果是有限人工场景计数与概率，非真实模型性能或一般变化点最优性。没有以同一结果事后调参或进行训练。
```json
{
  "N": 20,
  "alpha": 0.05,
  "lambda": 0.75,
  "starts": [
    0,
    4,
    8,
    12,
    16
  ],
  "paths": 1048576,
  "checks": 2097150,
  "weightSums": [
    1,
    1,
    1,
    1
  ],
  "stats": {
    "null": {
      "fixed": {
        "mass": 0.03589344024658203,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      },
      "sparse_mix": {
        "mass": 0.022735595703125,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      },
      "dense_mix": {
        "mass": 0.018503189086914062,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      },
      "sparse_union": {
        "mass": 0.011927604675292969,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      },
      "unbudgeted_scan": {
        "mass": 0.15044403076171875,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      }
    },
    "early_change": {
      "fixed": {
        "mass": 0.4042695486441003,
        "pre": 0,
        "post": 0.4042695486441003,
        "meanDelayGivenPost": 12.512051164684962
      },
      "sparse_mix": {
        "mass": 0.7948638732118124,
        "pre": 0,
        "post": 0.7948638732118124,
        "meanDelayGivenPost": 10.842219010304081
      },
      "dense_mix": {
        "mass": 0.7837758584714276,
        "pre": 0,
        "post": 0.7837758584714276,
        "meanDelayGivenPost": 11.209037723834888
      },
      "sparse_union": {
        "mass": 0.7430099130369383,
        "pre": 0,
        "post": 0.7430099130369383,
        "meanDelayGivenPost": 11.60921927218289
      },
      "unbudgeted_scan": {
        "mass": 0.9545190111594489,
        "pre": 0,
        "post": 0.9545190111594489,
        "meanDelayGivenPost": 7.79536760869746
      }
    },
    "late_change": {
      "fixed": {
        "mass": 0.0013456860216258804,
        "pre": 0.00031280517578125,
        "post": 0.0010328808458446304,
        "meanDelayGivenPost": 7.2243811302438905
      },
      "sparse_mix": {
        "mass": 0.13282192975191265,
        "pre": 0.00002849102020263672,
        "post": 0.13279343873171,
        "meanDelayGivenPost": 7.78306359622201
      },
      "dense_mix": {
        "mass": 0.09757353808191738,
        "pre": 0.000009715557098388672,
        "post": 0.09756382252481899,
        "meanDelayGivenPost": 7.57842201318851
      },
      "sparse_union": {
        "mass": 0.019474562446507804,
        "pre": 0.000005424022674560547,
        "post": 0.019469138423833243,
        "meanDelayGivenPost": 7.651987794254526
      },
      "unbudgeted_scan": {
        "mass": 0.6196574082797639,
        "pre": 0.001445770263671875,
        "post": 0.618211638016092,
        "meanDelayGivenPost": 6.040289801430668
      }
    },
    "stable_good": {
      "fixed": {
        "mass": 0.000318678246003401,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      },
      "sparse_mix": {
        "mass": 0.000054243631893768907,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      },
      "dense_mix": {
        "mass": 0.0000369269801012706,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      },
      "sparse_union": {
        "mass": 0.00001598558901605429,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      },
      "unbudgeted_scan": {
        "mass": 0.0030944459576858208,
        "pre": 0,
        "post": 0,
        "meanDelayGivenPost": null
      }
    }
  },
  "delayed": {
    "N": 14,
    "starts": [
      0,
      4,
      8,
      12
    ],
    "shortPaths": 16384,
    "envelopes": 8060928,
    "recurrenceChecks": 245760,
    "completeChecks": 32768,
    "subsetChecks": 49152,
    "results": {
      "immediate": {
        "nullCount": 206,
        "fullCrossMissed": 0,
        "nullProbability": 0.0125732421875,
        "altProbability": 0.109523244202137
      },
      "fixed_delay_3": {
        "nullCount": 206,
        "fullCrossMissed": 0,
        "nullProbability": 0.0125732421875,
        "altProbability": 0.109523244202137
      },
      "positive_only": {
        "nullCount": 206,
        "fullCrossMissed": 0,
        "nullProbability": 0.0125732421875,
        "altProbability": 0.109523244202137
      }
    }
  }
}
```
## 边界及下游
未实现真实时钟、证据资格、持久状态、晚反馈增量树、长期数值稳定性、跨设备、真实数据、原生产品、自动回退或独立验收；未验证实际条件均值假设。研究者选定起点/权重、概率、lambda、窗口、阈值，未授权为正式生产政策。后续需连接当前模型注册、分域适用性、真实反馈与不可变版本，独立审查退化、回退资格和多重检测。未修改正式代码、唯一交接、冻结协议或证据等级，未启动新Codex任务、训练、合并、部署、主动CI、费用。
## 完整复算
Node标准JS，无依赖；核心实际在连接器JS运行。
```js
function experiment(){
 const ck=(b,m)=>{if(!b)throw Error(m)},N=20,alpha=.05,threshold=20,lambda=.75,starts=[0,4,8,12,16],factor=z=>1+lambda*z;
 const names=["fixed","sparse_mix","dense_mix","sparse_union","unbudgeted_scan"],scenarios=[{name:"null",p:()=>.5,change:null},{name:"early_change",p:i=>i<4?.25:.875,change:4},{name:"late_change",p:i=>i<12?.25:.875,change:12},{name:"stable_good",p:()=>.25,change:null}];
 const stats=Object.fromEntries(scenarios.map(s=>[s.name,Object.fromEntries(names.map(n=>[n,{mass:0,pre:0,post:0,delayWeighted:0}]))]));
 let paths=0,checks=0,weightSums=Array(scenarios.length).fill(0);
 function visit(i,state,first,weights){
  if(i===N){paths++;for(let j=0;j<scenarios.length;j++){let s=scenarios[j],w=weights[j];weightSums[j]+=w;for(let k=0;k<names.length;k++)if(first[k]){let r=stats[s.name][names[k]];r.mass+=w;if(s.change!==null){if(first[k]<=s.change)r.pre+=w;else{r.post+=w;r.delayWeighted+=w*(first[k]-s.change)}}}}return}
  for(let z of [-1,1]){
   let f=factor(z),[fixed,sparse,dense,peakSparse,scan]=state,add=starts.includes(i)?1/starts.length:0;
   let a=[fixed*f,(sparse+add)*f,(dense+1/N)*f,Math.max(peakSparse,starts.includes(i)?1:0)*f,Math.max(1,scan)*f];
   let sparseRemaining=starts.filter(s=>s>i).length/starts.length,denseRemaining=(N-i-1)/N;
   let v=[a[0],a[1]+sparseRemaining,a[2]+denseRemaining,a[3]/starts.length,a[4]];
   ck(v[1]>=0&&v[2]>=0&&v[3]<=v[1]+1e-12,"mixture dominates union allocation");checks++;
   let hit=first.map((t,k)=>t||(v[k]>=threshold?i+1:0));
   let ws=weights.map((w,j)=>w*(z===1?scenarios[j].p(i):1-scenarios[j].p(i)));
   visit(i+1,a,hit,ws);
  }
 }
 visit(0,[1,0,0,0,0],Array(5).fill(0),Array(scenarios.length).fill(1));
 ck(weightSums.every(w=>Math.abs(w-1)<1e-9),"mass");
 for(const s of scenarios)for(const n of names){let r=stats[s.name][n];r.meanDelayGivenPost=r.post?r.delayWeighted/r.post:null;delete r.delayWeighted}
 for(const n of names.slice(0,4))ck(stats.null[n].mass<=alpha,"null control");
 // independent direct component product on shorter fixed sequences and delayed outcome support
 const smallN=14,ss=[0,4,8,12],modes=["immediate","fixed_delay_3","positive_only"],dout=Object.fromEntries(modes.map(m=>[m,{nullCount:0,altWeight:0,fullCrossMissed:0}]));
 let envelopes=0,recurrenceChecks=0,completeChecks=0,subsetChecks=0,shortPaths=0;
 function direct(ds,k,ss){let v=0;for(let s of ss){let m=1;for(let j=s;j<k;j++)m*=factor(ds[j]);v+=m/ss.length}return v}
 function series(ds,ss){let a=0,res=[1];for(let i=0;i<ds.length;i++){a=(a+(ss.includes(i)?1/ss.length:0))*factor(ds[i]);res.push(a+ss.filter(s=>s>i).length/ss.length)}return res}
 for(let mask=0;mask<2**smallN;mask++){
  const ds=Array.from({length:smallN},(_,i)=>mask&(1<<i)?1:-1);shortPaths++;
  let latent=series(ds,ss);for(let k=0;k<=smallN;k++){ck(latent[k]===direct(ds,k,ss),"recurrence direct");recurrenceChecks++}
  let crossed=Math.max(...latent)>=threshold,weight=ds.reduce((w,z,i)=>w*(i<4?(z===1?1:3):(z===1?3:1)),1);
  for(let m of modes){let hit=false;
   for(let t=1;t<=smallN+3;t++){let k=Math.min(t,smallN),d=ds.slice(0,k).map((z,i)=>i+1+(m==="immediate"?0:m==="fixed_delay_3"?3:z===1?0:smallN+4)<=t?z:-1),v=series(d,ss);
    for(let j=0;j<=k;j++){ck(v[j]<=latent[j]+1e-12,"delayed bound");envelopes++}
    if(Math.max(...v)>=threshold)hit=true;
    if(t===smallN+3&&m!=="positive_only"){ck(v.every((x,j)=>x===latent[j]),"final recovery");completeChecks++}
   }
   ck(!hit||crossed,"subset");subsetChecks++;if(hit){dout[m].nullCount++;dout[m].altWeight+=weight}if(crossed&&!hit)dout[m].fullCrossMissed++;
  }
 }
 for(let r of Object.values(dout)){r.nullProbability=r.nullCount/2**smallN;r.altProbability=r.altWeight/4**smallN;delete r.altWeight}
 return {N,alpha,lambda,starts,paths,checks,weightSums,stats,delayed:{N:smallN,starts:ss,shortPaths,envelopes,recurrenceChecks,completeChecks,subsetChecks,results:dout}}
}
console.log(JSON.stringify(experiment(),null,2));
```
