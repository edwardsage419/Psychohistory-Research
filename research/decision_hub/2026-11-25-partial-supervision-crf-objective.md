# v3.2 自主认知专项第16轮（累计第75轮）：部分监督CRF目标及梯度复算

2026-11-25。RESEARCH_CANDIDATE / FIXED_PARAMETER_OBJECTIVE_EXECUTED / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线 9e45ffc4fa935a4547d3b550b1bdcf27ed1a2d42，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核查最新8提交、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、AGENTS 78cc1f8327ec50b5762103fedfaf1f06e85f7658、同步规程26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题非全文）、R72 82f53eb20bcb7b49e0e56088a7c2c586000627fa、R73 af648d16ee96b9af4a3efb61b413d113208bb0ca、R74 bbdc12dfe65b24aa24e6b1d25a04955766cadab4。新增研究：从已有精确跨度正例构造部分BIO监督，计算固定参数损失和梯度，验证未知标签不被擅自变成负例。非训练、非新生产模型。

## 一手来源
Tsuboi, Kashima, Mori, Oda & Matsumoto (2008), Training Conditional Random Fields Using Incomplete Annotations, COLING 2008, pp.897–904, https://aclanthology.org/C08-1113/ ，PDF https://aclanthology.org/C08-1113.pdf 。实际读取第3/4节及相关文本，并截图核对印刷页899/900（PDF零基2/3）公式1–5。作者对相容标签序列边际化，指出目标一般非凹，Markov条件下可用动态规划；本轮自行实现前向期望递推，不是复现作者日语分词/词性实验。未读全文、未下载作者数据或代码，不声称许可、语言效果或论文复现。

## 数学
固定输入x，合法BIO序列集合Y，符合部分标注的子集A。s(y)=theta·f(y)，Z(S)=Σ_{y∈S}exp(s(y))。负对数似然 L=log Z(Y)-log Z(A)；梯度 E_Y f-E_A f。未知位置允许O/B/I（仍需合法转移）；已标注精确跨度首字B、内部I，紧随跨度后不允许I（前提是原标注确实声明该角色的精确完整边界）。完全无标注A=Y时损失和梯度均0；A为空则不相容，阻断而非伪造标签。独立角色头允许不同角色跨度重叠，同一头重叠当前拒绝；这不支持一般嵌套、多标签结构或联合语义关系。目标本身不解决标注选择偏差、漏标机制、模型可辨识性、虚假正例或全量义务覆盖，不能把边际概率当真实决策概率。无监督样本可另研其他目标，不能自动推定为负例。真实训练许可、独立样本、验证及资源预算另行授权。

采用O=0/B=1/I=2，I不得跟随O或句首。固定theta=(.2,-.3,.4)，三个特征仅计B、I以及B/I到O转移，不使用实际字符或词语特征，非语言预测模型。前向每状态保留log权重和条件特征期望，logsumexp稳定合并；对长度T、K标签、d特征，朴素期望递推时间O(T K² d)，空间O(Kd)（不含输入和临时数组），不等于未来完整CRF资源。固定参数未拟合、没有执行更新、训练或选择超参数。梯度仅数学复算。对照将所有未标注位置强制O，模拟未经核实的负例填充；更高损失不是模型准确率差异；未有正例头被强制造成梯度，说明其额外监督来自假设。部分标注本身不提供完全准确的负例。

## 实际输入与实验
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
读取两个固定JSON全文并校验连接器返回blob。沿R74三角色正例映射，约束/行动/修订共67（角色重叠可双计），64轮×3头。全部为ChatGPT研发辅助原创合成公开开发样例，训练许可未确认；未标注位置及其他角色的标签均不当作本角色负例。未将R73粗角色转换当真人真值。原始文本与数据保留不变。BIO按UTF16位置，与前轮一致，真实Unicode边界与多语言需另审。固定数值实验：长度1..4，每位置7种非空标签集合，动态规划对直接枚举；合法情形每3维中心有限差分（h=1e-5），容差1e-7。另13控制含非法I、空集合、相邻跨度、重叠拒绝及大分数稳定性。代码同研究者设计，非独立科学验收；未执行原生语言、数学模型、真机或用户实验。当前范围无外部原始数据、无实际训练或运行时第三方AI依赖。

## 可复算代码及结果
将两个固定JSON按L/S顺序解析为docs，执行以下JS，无第三方包。不更新任何权重。

```js
function experiment(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)},theta=[.2,-.3,.4],near=(a,b,t=1e-9)=>Math.abs(a-b)<=t;
 // O=0 B=1 I=2; legal I follows B or I; implicit initial O.
 const legal=(p,k)=>k!==2||p!==0,feat=(p,k)=>[+(k===1),+(k===2),+(p!==0&&k===0)],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
 const combine=arr=>{if(!arr.length)return null;let max=Math.max(...arr.map(a=>a.z));let w=arr.map(a=>Math.exp(a.z-max)),sum=w.reduce((a,b)=>a+b,0);return {z:max+Math.log(sum),e:[0,1,2].map(j=>arr.reduce((s,a,i)=>s+w[i]*a.e[j],0)/sum)}};
 function dp(masks,t){let states=[{z:0,e:[0,0,0]},null,null];for(const mask of masks){states=[0,1,2].map(k=>{if(!(mask&(1<<k)))return null;let a=[];for(let p=0;p<3;p++)if(states[p]&&legal(p,k)){let f=feat(p,k);a.push({z:states[p].z+dot(t,f),e:states[p].e.map((x,j)=>x+f[j])})}return combine(a)})}return combine(states.filter(Boolean))}
 // Direct enumeration, independent scoring of complete path counts.
 function brute(m,t){let z=0,e=[0,0,0];function walk(y){if(y.length===m.length){let b=y.filter(k=>k===1).length,i=y.filter(k=>k===2).length,c=y.filter((k,j)=>j>0&&k===0&&y[j-1]!==0).length,f=[b,i,c],w=Math.exp(t[0]*b+t[1]*i+t[2]*c);z+=w;e=e.map((x,j)=>x+w*f[j]);return}for(let k=0;k<3;k++)if((m[y.length]&(1<<k))&&(k!==2||(y.length>0&&y[y.length-1]!==0)))walk([...y,k])}walk([]);return z?{z:Math.log(z),e:e.map(x=>x/z)}:null}
 function objective(m,t){let a=dp(m.map(()=>7),t),b=dp(m,t);return b?{loss:a.z-b.z,g:a.e.map((x,i)=>x-b.e[i])}:null}
 let out={mathematics:{maskCases:0,valid:0,infeasible:0,maxPartitionError:0,maxExpectationError:0,gradientChecks:0,maxGradientError:0},corpus:{turns:0,heads:0,annotatedSpans:0,positions:0,positivePositions:0,boundaryOnlyPositions:0,fullyUnknownPositions:0,headsWithoutPositive:0,zeroSignalHeads:0,forcedOArtificialSignalHeads:0,lossPartial:0,lossForcedO:0,forcedOLarger:0,gradientDiffHeads:0,byRole:{}},controls:0};
 for(let n=1;n<=4;n++){
  function run(m){if(m.length<n){for(let v=1;v<8;v++)run([...m,v]);return}let q=out.mathematics;q.maskCases++;let a=dp(m,theta),b=brute(m,theta);ck(Boolean(a)===Boolean(b),"feasibility");if(!a){q.infeasible++;return}q.valid++;q.maxPartitionError=Math.max(q.maxPartitionError,Math.abs(a.z-b.z));q.maxExpectationError=Math.max(q.maxExpectationError,...a.e.map((v,i)=>Math.abs(v-b.e[i])));ck(near(a.z,b.z)&&a.e.every((v,i)=>near(v,b.e[i])),"enumeration");let l=objective(m,theta);ck(l.loss>=-1e-9,"nonnegative loss");for(let j=0;j<3;j++){let p=theta.slice(),r=theta.slice(),h=1e-5;p[j]+=h;r[j]-=h;let g=(objective(m,p).loss-objective(m,r).loss)/(2*h);q.gradientChecks++;q.maxGradientError=Math.max(q.maxGradientError,Math.abs(g-l.g[j]));ck(near(g,l.g[j],1e-7),"gradient")}}
  run([]);
 }
 const roles=["constraint","action","revision"];
 function gold(d,a,r){if(d===0)return r==="constraint"?["HARD","CONDITIONAL_HARD"].includes(a.kind):r==="action"?["PROPOSED_ACTION","CONDITIONAL_ACTION","ACTION"].includes(a.kind):a.kind==="REVISION";return r==="revision"?["replace","retract"].includes(a.op):a.role===r}
 function masksFor(text,spans){let m=Array(text.length).fill(7),positive=Array(text.length).fill(false),boundary=Array(text.length).fill(false);for(const [s,e] of spans){ck(s>=0&&s<e&&e<=text.length,"span bounds");for(let j=s;j<e;j++){ck(!positive[j],"within-head overlap");positive[j]=true;m[j]=j===s?2:4}if(e<text.length)boundary[e]=true}for(let j=0;j<m.length;j++)if(boundary[j])m[j]&=3;ck(m.every(Boolean),"conflicting exact boundaries");return {m,forced:m.map((v,i)=>positive[i]?v:1),positive,boundary}}
 for(const r of roles)out.corpus.byRole[r]={heads:0,spans:0,noPositive:0,partialLoss:0,forcedLoss:0};
 for(let d=0;d<2;d++)for(const ep of docs[d].cases)for(const turn of ep.turns){out.corpus.turns++;const src=d===0?turn.claims:turn.proposal.claims;
  for(const role of roles){const c=out.corpus,h=c.byRole[role],spans=src.filter(a=>gold(d,a,role)).map(a=>{let s=d===0?a.span:a.quote,i=turn.text.indexOf(s);ck(i>=0&&i===turn.text.lastIndexOf(s),"unique");return [i,i+s.length]});const v=masksFor(turn.text,spans),p=objective(v.m,theta),f=objective(v.forced,theta);ck(p&&f&&p.loss<=f.loss+1e-9,"nested event");c.heads++;h.heads++;h.spans+=spans.length;c.annotatedSpans+=spans.length;c.positions+=v.m.length;c.positivePositions+=v.positive.filter(Boolean).length;c.boundaryOnlyPositions+=v.m.filter(x=>x===3).length;c.fullyUnknownPositions+=v.m.filter(x=>x===7).length;c.lossPartial+=p.loss;c.lossForcedO+=f.loss;h.partialLoss+=p.loss;h.forcedLoss+=f.loss;c.forcedOLarger+=+(f.loss>p.loss+1e-9);c.gradientDiffHeads+=+p.g.some((x,i)=>!near(x,f.g[i]));
   if(!spans.length){c.headsWithoutPositive++;h.noPositive++;ck(near(p.loss,0)&&p.g.every(x=>near(x,0)),"no positive no supervision");c.zeroSignalHeads++;if(f.loss>1e-9&&f.g.some(x=>!near(x,0)))c.forcedOArtificialSignalHeads++}
  }
 }
 let tests=[()=>objective([7,7],theta).loss===0,()=>objective([4],theta)===null,()=>objective([2,4],theta)!==null,()=>objective([1,4],theta)===null,()=>objective([0],theta)===null,()=>objective([7],theta).g.every(x=>x===0),()=>objective([1],theta).g.some(x=>Math.abs(x)>1e-9),()=>masksFor("甲乙丙",[[0,1],[1,2]]).m.join()==="2,2,3",()=>masksFor("甲乙丙",[[1,2]]).m.join()==="7,2,3",()=>{try{masksFor("甲乙",[[0,2],[1,2]]);return false}catch{return true}},()=>out.corpus.positions===out.corpus.positivePositions+out.corpus.boundaryOnlyPositions+out.corpus.fullyUnknownPositions,()=>out.corpus.annotatedSpans===67,()=>{let a=objective([7,2,3],[1000,-1000,500]);return a&&Number.isFinite(a.loss)&&a.g.every(Number.isFinite)}];
 for(const t of tests){ck(t(),"control");out.controls++}return out;
}
```

```json
{
  "mathematics": {
    "maskCases": 2800,
    "valid": 2174,
    "infeasible": 626,
    "maxPartitionError": 8.881784197001252e-16,
    "maxExpectationError": 1.1102230246251565e-15,
    "gradientChecks": 6522,
    "maxGradientError": 5.916583889487015e-11
  },
  "corpus": {
    "turns": 64,
    "heads": 192,
    "annotatedSpans": 67,
    "positions": 5298,
    "positivePositions": 478,
    "boundaryOnlyPositions": 67,
    "fullyUnknownPositions": 4753,
    "headsWithoutPositive": 138,
    "zeroSignalHeads": 138,
    "forcedOArtificialSignalHeads": 138,
    "lossPartial": 624.3583078310637,
    "lossForcedO": 5696.591992934521,
    "forcedOLarger": 192,
    "gradientDiffHeads": 192,
    "byRole": {
      "constraint": {
        "heads": 64,
        "spans": 25,
        "noPositive": 41,
        "partialLoss": 270.95270356952443,
        "forcedLoss": 1910.4639976448395
      },
      "action": {
        "heads": 64,
        "spans": 30,
        "noPositive": 45,
        "partialLoss": 221.49216133143779,
        "forcedLoss": 1895.4639976448393
      },
      "revision": {
        "heads": 64,
        "spans": 12,
        "noPositive": 52,
        "partialLoss": 131.9134429301013,
        "forcedLoss": 1890.6639976448391
      }
    }
  },
  "controls": 13
}
```

## 后续
应将此部分监督合同用于候选排序的可学习特征与结构化搜索设计，先对角色/跨度标签选择偏差、跨轮引用、独立义务覆盖和真实语料许可证进行审查；可在固定人工参数下测试跨轮特征的可辨识性与搜索覆盖，训练待另行授权。现阶段不宣布架构最终选定，不发布零碎Codex任务；R50完整版本12项范围保留，独立轨负责未见样本及真实运行验证。未改生产代码、训练、CI、合并、部署或增加费用，冻结协议不变。