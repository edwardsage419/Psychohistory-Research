# 连续量预测的有界残差修正及后续评价门
2026-11-25。RESEARCH_CANDIDATE / EXACT_FINITE_DEVELOPMENT_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 45934aedcc37ad2bae1c56cee4dce4959befeccc；Draft #62固定候选 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期10提交、14开放PR、v3.2前12行、唯一产品交接前18行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07；检索calibration/feedback/bias/forecast error/correction/parameter/residual/prequential/censoring。审查R44 32e3e7a40e9e7d844ad3d67eb28eac5f0997bee0、R18 9bba8270025341979c8f1cc3daec4fb97da0c587、R20 7facdce9bd50b6e2487d307155e992b4d371d34e、C025 a4f6955164b94ecfa62e945625101176657827fd。已有二元概率反馈、反事实配对界、行动价值及逐次评价。本轮仅新增连续量加性残差修正、部分观测下的中位数保守选择、绝对误差及低估误差双门，非新通用统计理论。全库去重仍有局限。

## 合同与数学
同一已确认任务类型、同单位、同版本及同预测目标，成本或工时事前点预测p，实际结果y，残差r=y-p。实际完整结果对应单点区间；部分观察只在可信下界与上界已获得时形成闭区间[l,u]；右删失无可信上界、完全缺失且无可信界、范围变化、取消任务和未执行反事实不能擅自填界。本实验三条开发记录、两条后续评价记录，固定不重叠；八类整数残差区间为人工生成。假定各行可自由组合，若存在相关限制则区间结论仍为保守外界。没有真实记录时间、用途授权、鉴权、独立样本或置信区间；真实入口须复用R18/R109时间和权限规则，不得按结果选择评价记录。仅在对未来数据可使用的预测域内适用，不能将人群差异视为个人稳定偏差。

三条训练残差的中位数范围为[m_l,m_u]，分别取三个下界/上界的中位数，因中位数逐分量单调，端点可同时实现。在该区间内选择离0最近的修正delta（正区间取下端，负区间取上端，跨0取0）。对每个与训练记录相容的完整向量，delta都处于0与该向量某个绝对损失最优中位数之间；绝对损失为凸函数，因此训练总绝对损失不会增大。这是训练样本的代数性质，不代表真实未来改进，也不保证逐条误差下降。需要物理非负约束时独立验证p+delta>=0；本实验不做截断，适用前提为原预测足够大。固定的delta作为候选在评价记录结果揭晓前冻结。真实评价预测必须在相应结果获知前产生；合成夹具只模拟分区，不声称真实前瞻验证。

同一实际结果上定义绝对误差改善g(r)=|r|-|r-delta|及低估损失改善h(r)=max(0,r)-max(0,r-delta)。正值代表损失下降。两函数在0、delta及区间端点之间分段线性，故每条的极值在这些点获得；逐条区间求和给出矩形合同锐界。有限评价门要求总绝对误差改善下界>0且低估改善下界>=0。后者仅为示例成本/时间安全指标，不代替硬资金底线或独立的用户损失函数；负修正可能因低估门拒绝。门通过仅表示给定有限评价集合内两项条件成立；不等于科学验收、统计显著、未来风险下降或自动更新许可。阈值、单位、窗口、用途、用户偏好及回退门由未来产品另行确认。未执行真实模型训练或参数上线，所有结果authority NONE。若缺资格返回UNKNOWN，历史预测不重写、已撤回依赖应重新核验并失效。

## 实验
8^3=512训练区间组合，逐一枚举整数完整残差（连续区间的中位数端点及凸性证明见上）。每训练组合配8^2=64评价区间组合，32768组；两种损失上下界分别对照逐完整整数评价组合穷举，整数端点与折点使此参照覆盖连续极值。参照同研究者编写，非独立验收。只看完整单点评价记录的基线以观察到的绝对误差改善和为正判作改善；naiveGainNotCertified为该条件成立而完整评价集合下界<=0；不等于实际产品错误率或一定变差。研究者选定区间、3/2记录分区与双门，不代表有足够统计样本。无外部数据、个人数据、真实训练、原生API、独立验收、设备测量、CI请求、PR合并、部署、冻结改动或新增费用。Node标准JS。

```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const I=[[-2,-2],[-1,-1],[0,0],[1,1],[2,2],[-2,2],[0,2],[-2,0]];
 const sum=a=>a.reduce((s,v)=>s+v,0),med=a=>[...a].sort((x,y)=>x-y)[1];
 function correction(train,qualified=true){
  if(!qualified||train.length!==3||train.some(x=>!x||x[0]>x[1]))return {status:"UNKNOWN",authority:"NONE"};
  let lo=med(train.map(x=>x[0])),hi=med(train.map(x=>x[1]));
  return {status:"CANDIDATE",authority:"NONE",median:[lo,hi],delta:lo>0?lo:hi<0?hi:0};
 }
 const absGain=(r,d)=>Math.abs(r)-Math.abs(r-d),underGain=(r,d)=>Math.max(0,r)-Math.max(0,r-d);
 function rowBound(i,d,fn){
  let x=[...i,0,d].filter(v=>v>=i[0]&&v<=i[1]).map(v=>fn(v,d));
  return [Math.min(...x),Math.max(...x)];
 }
 function bounds(test,d,fn){
  let b=test.map(x=>rowBound(x,d,fn));return [sum(b.map(x=>x[0])),sum(b.map(x=>x[1]))];
 }
 const ints=x=>Array.from({length:x[1]-x[0]+1},(_,i)=>x[0]+i);
 function brute(test,d,fn){
  let v=[];for(let x of ints(test[0]))for(let y of ints(test[1]))v.push(fn(x,d)+fn(y,d));
  return [Math.min(...v),Math.max(...v)];
 }
 let o={training:0,nonzeroCandidate:0,trainCompletions:0,trainNonworse:0,testCases:0,boundChecks:0,finiteStrictGain:0,finiteStrictLoss:0,finiteGate:0,underestimateGateBlocked:0,ambiguousGain:0,naiveCompleteCaseGain:0,naiveGainNotCertified:0,naiveGainDefiniteLoss:0,controls:0,witnesses:{}};
 for(let a of I)for(let b of I)for(let c of I){
  let train=[a,b,c],v=correction(train),d=v.delta,ms=[];
  o.training++;o.nonzeroCandidate+=+(d!==0);
  for(let x of ints(a))for(let y of ints(b))for(let z of ints(c)){
   let rs=[x,y,z];ms.push(med(rs));o.trainCompletions++;
   ck(sum(rs.map(t=>absGain(t,d)))>=0,"training nonworse");o.trainNonworse++;
  }
  ck(eq(v.median,[Math.min(...ms),Math.max(...ms)]),"median extrema");
  for(let x of I)for(let y of I){
   let test=[x,y],g=bounds(test,d,absGain),u=bounds(test,d,underGain);
   ck(eq(g,brute(test,d,absGain))&&eq(u,brute(test,d,underGain)),"bounds");
   o.testCases++;o.boundChecks+=2;
   o.finiteStrictGain+=+(g[0]>0);o.finiteStrictLoss+=+(g[1]<0);
   o.ambiguousGain+=+(g[0]<=0&&g[1]>0);
   if(g[0]>0&&u[0]>=0)o.finiteGate++;
   else if(g[0]>0&&u[0]<0){o.underestimateGateBlocked++;o.witnesses.risk??={train,delta:d,test,g,u}}
   let seen=test.filter(x=>x[0]===x[1]);
   if(seen.length&&sum(seen.map(x=>absGain(x[0],d)))>0){
    o.naiveCompleteCaseGain++;
    if(g[0]<=0){o.naiveGainNotCertified++;o.witnesses.missing??={train,delta:d,test,g,u}}
    if(g[1]<0)o.naiveGainDefiniteLoss++;
   }
  }
 }
 for(let t of [o.training===512,o.testCases===32768,o.boundChecks===65536,o.trainNonworse===o.trainCompletions,correction([[1,2],[1,2],[-2,2]]).delta===1,correction([[-2,-1],[-2,-1],[-2,2]]).delta===-1,correction([[-2,2],[-2,2],[-2,2]]).delta===0,correction([null,[1,1],[2,2]]).status==="UNKNOWN",correction(I.slice(0,3),false).status==="UNKNOWN",o.finiteGate>0,o.underestimateGateBlocked>0,o.naiveGainNotCertified>0]){ck(t,"control "+o.controls);o.controls++}
 return o;
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实测
```json
{
  "training": 512,
  "nonzeroCandidate": 160,
  "trainCompletions": 4096,
  "trainNonworse": 4096,
  "testCases": 32768,
  "boundChecks": 65536,
  "finiteStrictGain": 596,
  "finiteStrictLoss": 2912,
  "finiteGate": 552,
  "underestimateGateBlocked": 44,
  "ambiguousGain": 1920,
  "naiveCompleteCaseGain": 2252,
  "naiveGainNotCertified": 1656,
  "naiveGainDefiniteLoss": 0,
  "controls": 12,
  "witnesses": {
    "risk": {
      "train": [
        [
          -2,
          -2
        ],
        [
          -2,
          -2
        ],
        [
          -2,
          -2
        ]
      ],
      "delta": -2,
      "test": [
        [
          -2,
          -2
        ],
        [
          -1,
          -1
        ]
      ],
      "g": [
        2,
        2
      ],
      "u": [
        -1,
        -1
      ]
    },
    "missing": {
      "train": [
        [
          -2,
          -2
        ],
        [
          -2,
          -2
        ],
        [
          -2,
          -2
        ]
      ],
      "delta": -2,
      "test": [
        [
          -2,
          -2
        ],
        [
          -2,
          2
        ]
      ],
      "g": [
        0,
        4
      ],
      "u": [
        -2,
        0
      ]
    }
  }
}
```
## 后续
将此候选与前轮持续收益阈值、联合目标期限及已确认现金义务连接；实际用户数据须明确授权、范围与单位一致，先分离训练开发与后续独立留出，并保留未完成、取消及失访状态。独立轨检验真实预测时序、跨场景退步、撤回与版本回退，产品轨维护唯一交接。无本轮正式版本开发授权。