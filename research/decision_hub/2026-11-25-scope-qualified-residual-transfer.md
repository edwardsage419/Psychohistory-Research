# 跨场景残差修正的资格约束与最坏改善收缩
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / EXACT_FINITE_DEVELOPMENT / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main c29366397b6af8a2546e6562450b62f94b69424c；Draft #62候选 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近10提交、14开放PR、v3.2前12行、唯一产品交接前18行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。查重transfer/transport/reference class/domain/similarity/subgroup，读取0bd11329987d421cf7af6a05bd44e5482a473357、3f743dc4051227e24c2b2a9b320489783a33dbdf参照类报告、62e83471fa2b9ae05e0221461d2cfec437f2ccb9因果迁移反例及C036 4015e81548d044ca95770e6e0e2ba868ce94ad14（物理转移不同义）。既有参照类、因果迁移和跨群体R273不重做。本轮只研究上一轮连续量修正向有独立支持界的目标场景迁移。全库去重仍有局限。

## 固定复用
research/decision_hub/2026-11-25-bounded-residual-correction-gate.md，固定提交c29366397b6af8a2546e6562450b62f94b69424c，连接器blob 0b4a892b4daf7c1b887dc93ca672797068d3da63。实际从已审查研究代码提取correction/absGain/underGain，未重写这些函数，不执行任意外部文档，不声称原生接入。

## 合同
源场景三条残差区间提供候选修正delta_s。独立可信宿主给定参考残差支持区间[a,b]以及目标误差关系的正比例s∈{1,2}、偏移区间[c,d]，目标残差包络[L,U]=[s*a+c,s*b+d]。此支持是人工夹具中的独立假设，绝不能用源训练样本的最小最大值自动声称覆盖未来目标误差。偏移关系不是因果识别，缩放也不是实际单位转换；真实范围、机制、单位及版本必须另有证据。七项资格（用途授权、指标、单位、机制、支持、版本、当前状态）全由布尔模拟；任一缺失则UNKNOWN_TRANSFER并且不输出修正量，原目标基线本身仍未验证。无真实个人数据、授权、身份、时间或统计置信界。预测基线需满足p+delta非负等物理范围，本实验假定足够大。缺证据不以0误差替代。

## 推导
源建议换算为D=s*delta_s，允许目标修正x在0与D之间收缩，不允许方向反转。对每个目标残差r，绝对误差改善G=|r|-|r-x|，低估改善H=max(0,r)-max(0,r-x)。要求所有r∈[L,U]满足H>=0，在可选修正中最大化min G，平局取绝对变化最小者。若D>0且L>0，最优x=min(D,L)；若D<0且U<0，最优x=max(D,U)；否则x=0。证明：正修正下G随r单调不减，最坏在L，G(L)=L-|L-x|（L>0时），最大值由x距L最近取得；L<=0时任何正修正最坏为负。负修正对称，最坏在U；U<0且x>=U时所有r<=x<=0，低估损失均为0；U>=0时任何负修正最坏为负。故所选x的最坏绝对改善恰为|x|且低估不恶化。该结论仅对包络覆盖真实r且使用相同目标/尺度成立；非期望损失、统计覆盖率或实际用户效果。若目标支持与源修正方向相反，只保持基线并等待新领域证据，不从旧修正推断新反向偏差。真实跨域独立评价、硬约束、回退、撤回重算及所有者授权仍为独立条件。所有结果authority NONE。

## 实验
8^3源开发区间组合×8参考支持×5偏移区间×2比例=40960组。直接整数枚举所有允许收缩值及目标包络各整数残差，核对最坏值、低估门与平局规则；分段线性折点均整数，连续包络的极值也被覆盖。参照使用前轮损失函数，同一研究者编写，非独立验收。直接照搬D为故意弱基线，统计存在相容残差恶化的组，不是实际错误率。七项资格分别缺失的拒绝控制；本实验未真实建立任何目标支持界。研究者选取缩放、偏移、包络、收缩策略和七门，不构成正式产品政策。无新增外部资料、个人数据、真实训练、原生API、设备测量、CI请求、合并、部署、费用或冻结变更。复算Node标准JS，将固定报告全文读为doc，仅执行已审查项目自有代码。
```js
function load(doc){const code=doc.split(" ```js\n".trimStart())[1].split("\n```")[0].split(" let o={training:")[0];return Function(code+"\nreturn {correction,absGain,underGain};\n}\nreturn experiment();")()}
function experiment(P){
 const ck=(v,m)=>{if(!v)throw Error(m)},I=[[-2,-2],[-1,-1],[0,0],[1,1],[2,2],[-2,2],[0,2],[-2,0]],S=[[-2,-2],[-1,1],[0,0],[1,2],[2,2]];
 const checks=["purpose","metric","unit","mechanism","support","version","current"];
 const eligible=Object.fromEntries(checks.map(k=>[k,true]));
 // Support bounds are independently qualified host inputs, not sample extrema.
 // The affine relation is a conditional envelope for the target residual.
 function transfer(train,anchor,shift,scale,host){
  const unknown={status:"UNKNOWN_TRANSFER",authority:"NONE",fallback:"BASELINE_UNVALIDATED_IN_TARGET"};
  if(!checks.every(k=>host[k]===true)||!Array.isArray(anchor)||!Array.isArray(shift)||![1,2].includes(scale)||anchor[0]>anchor[1]||shift[0]>shift[1])return unknown;
  const s=P.correction(train);if(s.status!=="CANDIDATE")return unknown;
  const L=scale*anchor[0]+shift[0],U=scale*anchor[1]+shift[1],d=scale*s.delta;
  // Restrict the correction to a shrinkage of the source suggestion.
  // Maximise the worst-case absolute improvement; tie resolves to zero/smaller change.
  const x=d>0&&L>0?Math.min(d,L):d<0&&U<0?Math.max(d,U):0;
  return {status:"CONDITIONAL_CANDIDATE",authority:"NONE",support:[L,U],raw:d,delta:x,minGain:Math.abs(x)};
 }
 let o={sourceCombos:0,cases:0,rawNonzero:0,retained:0,shrunk:0,abstainedNonzero:0,zeroSource:0,rawWorstLoss:0,rawUnderestimateLoss:0,rawWorstLossPrevented:0,targetPoints:0,optimalityChecks:0,qualificationRejects:0,controls:0,witnesses:{}};
 for(let a of I)for(let b of I)for(let c of I){
  let train=[a,b,c];o.sourceCombos++;
  for(let anchor of I)for(let shift of S)for(let scale of [1,2]){
   let v=transfer(train,anchor,shift,scale,eligible),[L,U]=v.support,d=v.raw,x=v.delta,rs=Array.from({length:U-L+1},(_,i)=>i+L);
   let gain=k=>Math.min(...rs.map(r=>P.absGain(r,k))),under=k=>Math.min(...rs.map(r=>P.underGain(r,k)));
   let choices=Array.from({length:Math.abs(d)+1},(_,i)=>Math.sign(d)*i).filter(k=>under(k)>=0);
   let max=Math.max(...choices.map(gain)),best=choices.filter(k=>gain(k)===max).sort((a,b)=>Math.abs(a)-Math.abs(b))[0];
   ck(gain(x)===max&&x===best&&gain(x)===v.minGain&&under(x)>=0,"oracle");
   for(let r of rs){ck(P.absGain(r,x)>=0&&P.underGain(r,x)>=0,"point");o.targetPoints++}
   o.cases++;o.optimalityChecks++;o.rawNonzero+=+(d!==0);o.zeroSource+=+(d===0);
   if(d!==0){if(x===d)o.retained++;else if(x===0)o.abstainedNonzero++;else o.shrunk++}
   if(gain(d)<0){o.rawWorstLoss++;o.rawWorstLossPrevented++;o.witnesses.raw??={train,anchor,shift,scale,result:v,rawWorst:gain(d)}}
   if(under(d)<0)o.rawUnderestimateLoss++;
   if(x!==0&&x!==d)o.witnesses.shrink??={train,anchor,shift,scale,result:v,rawWorst:gain(d)};
  }
 }
 const t=[[2,2],[2,2],[2,2]];
 for(let k of checks){let v=transfer(t,[1,2],[0,0],1,{...eligible,[k]:false});ck(v.status==="UNKNOWN_TRANSFER"&&!Object.hasOwn(v,"delta"),"qualification");o.qualificationRejects++}
 for(let v of [o.cases===40960,o.sourceCombos===512,o.rawNonzero===o.retained+o.shrunk+o.abstainedNonzero,o.rawNonzero+o.zeroSource===o.cases,o.rawWorstLoss===o.rawWorstLossPrevented,transfer(t,[1,2],[0,0],1,eligible).delta===1,transfer(t,[1,2],[-2,-2],1,eligible).delta===0,transfer(t,[2,2],[0,0],2,eligible).delta===4,transfer([[-2,-2],[-2,-2],[-2,-2]],[-2,-1],[0,0],1,eligible).delta===-1,o.qualificationRejects===7]){ck(v,"control "+o.controls);o.controls++}
 return o;
}
console.log(JSON.stringify(experiment(load(doc)),null,2));
```
## 实测
```json
{
  "sourceCombos": 512,
  "cases": 40960,
  "rawNonzero": 12800,
  "retained": 2680,
  "shrunk": 760,
  "abstainedNonzero": 9360,
  "zeroSource": 28160,
  "rawWorstLoss": 9448,
  "rawUnderestimateLoss": 5238,
  "rawWorstLossPrevented": 9448,
  "targetPoints": 126976,
  "optimalityChecks": 40960,
  "qualificationRejects": 7,
  "controls": 10,
  "witnesses": {
    "shrink": {
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
      "anchor": [
        -2,
        -2
      ],
      "shift": [
        -1,
        1
      ],
      "scale": 1,
      "result": {
        "status": "CONDITIONAL_CANDIDATE",
        "authority": "NONE",
        "support": [
          -3,
          -1
        ],
        "raw": -2,
        "delta": -1,
        "minGain": 1
      },
      "rawWorst": 0
    },
    "raw": {
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
      "anchor": [
        -2,
        -2
      ],
      "shift": [
        1,
        2
      ],
      "scale": 1,
      "result": {
        "status": "CONDITIONAL_CANDIDATE",
        "authority": "NONE",
        "support": [
          -1,
          0
        ],
        "raw": -2,
        "delta": 0,
        "minGain": 0
      },
      "rawWorst": -2
    }
  }
}
```
后续：同一经授权的个人经验可以提出新场景候选，目标资格与支持界仍需独立证据；若无法验证，显示未知并复用前轮后续评价门，不自动上线。产品轨维护唯一交接，独立轨检验未见跨域样本、支持破坏、撤回与原生入口。没有本轮正式版本开发授权。