# 第75轮增补：部分监督CRF极端评分及路径计数交叉核验

2026-11-25。RESEARCH_CANDIDATE / FIXED_SCORE_NUMERICAL_CROSSCHECK / TRAINING_NOT_AUTHORIZED。研究起点9e45ffc4fa935a4547d3b550b1bdcf27ed1a2d42；写前检测main变化停止，compare确认唯一新增提交bafadfad5d9f01b48050bd6f16d24a398840bf41，目标同主题主报告research/decision_hub/2026-11-25-partial-supervision-crf-objective.md blob 0fae5d3a25e09632b0ad3d49593393b74f0589e6，实际回读全文及结果，原主报告保留。其三角色192头、67标注、三特征6522梯度检查与本轮实验范围不同，禁止合并计数。此次仅保存数值压力测试和不同四特征参照路径的增量，非新的独立科学验收，不另计完整研究轮次。核查最新8提交、13开放Draft PR（#61未合并）、v3.2/AGENTS/同步规程（本轮摘录与历史阅读）、唯一交接相关标题（非全文）、R72/73/74。两份语料在新HEAD身份不变。未覆盖任何既有报告。

一手来源：Tsuboi等2008 COLING，https://aclanthology.org/C08-1113/ ，IBM Research作者机构摘要 https://research.ibm.com/publications/training-conditional-random-fields-using-incomplete-annotations ，实际阅读英文书目与机构摘要，未通读PDF或复现作者实验；本增补自身不继承主报告的PDF阅读为本轮新执行证据。CRF书目 Lafferty et al. 2001 https://mlanthology.org/icml/2001/lafferty2001icml-conditional/ 。无外部语料、代码或权重。

沿主报告L=log Z(Y)-log Z(A)，梯度为全集期望减相容集期望。单头O=0/B=1/I=2，合法转移I仅跟随B/I。未知允许全部合法标签，已知精确跨度首B内I，右邻不得I。固定四特征B计数、I计数、相邻同标签计数、偶数位置B计数；零、温和及极端固定参数(1000,-1000,500,-300)，不拟合。前向递推使用logsumexp和条件期望，额外精确BigInt合法路径计数；短序列直接枚举作参照。长度1..4、每位置7非空掩码，共2800掩码及三套固定参数8400比较（含不可行空集），合法掩码四维梯度有限差分8696次。极端参数测试扩展至全部掩码；不是完整机器学习性能证据。单独约束头25个跨度64轮实际计算，与主报告不同特征/参数、不得横比损失大小。无正例轮不提供本监督信号，强制O却会产生额外人为信号。无确证负例，不将其当事实错误率。其余未标注位置包含右邻限制位置，不能简单称全部可自由取三种标签。部分监督目标不解决选择偏差、错误标注及可辨识性；未测长序列数值、开放语义、性能或真实用户效果。代码使用相同数学合同及同研究者编写参照，不是独立验收。

固定数据（原创合成公开开发，训练许可未确认）：
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132

本轮首次运行实际得到8400比较、8696梯度检查、13控制，误差及单头统计与下列再次执行的核心检查一致（除新增最大相容路径数统计）。再次执行代码及实际输出：

```js
function crosscheck(docs){
 const ck=(b,m)=>{if(!b)throw Error(m)},zero=()=>[0,0,0,0],dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),add=(a,b)=>a.map((v,i)=>v+b[i]),sub=(a,b)=>a.map((v,i)=>v-b[i]),legal=(p,y)=>y!==2||p===1||p===2,feat=(i,p,y)=>[+(y===1),+(y===2),+(i>0&&p===y),+(i%2===0&&y===1)],empty=()=>({z:-Infinity,g:zero(),n:0n});
 function merge(a,b){if(!a.n)return b;if(!b.n)return a;let m=Math.max(a.z,b.z),x=Math.exp(a.z-m),y=Math.exp(b.z-m),s=x+y;return {z:m+Math.log(s),g:a.g.map((v,i)=>(x*v+y*b.g[i])/s),n:a.n+b.n}}
 function dp(m,w){
  if(!Array.isArray(m)||!m.length||m.length>128||m.some(x=>!Number.isInteger(x)||x<0||x>7)||w.length!==4||w.some(x=>!Number.isFinite(x)||Math.abs(x)>1000))return null;
  let a=[{p:-1,z:0,g:zero(),n:1n}];
  for(let i=0;i<m.length;i++){let b=[empty(),empty(),empty()];for(const v of a)if(v.n)for(let y=0;y<3;y++)if((m[i]&(1<<y))&&legal(v.p,y)){let f=feat(i,v.p,y);b[y]=merge(b[y],{z:v.z+dot(w,f),g:add(v.g,f),n:v.n})}a=b.map((v,p)=>({...v,p}))}
  return a.reduce((s,v)=>merge(s,v),empty());
 }
 function brute(m,w){let paths=[];function walk(y){let i=y.length;if(i===m.length){let f=[y.filter(x=>x===1).length,y.filter(x=>x===2).length,y.slice(1).filter((x,j)=>x===y[j]).length,y.filter((x,j)=>j%2===0&&x===1).length];paths.push({f,s:dot(w,f)});return}
 for(let k=0;k<3;k++)if((m[i]&(1<<k))&&(k!==2||(i>0&&y[i-1]!==0)))walk([...y,k]);}walk([]);
 if(!paths.length)return empty();let max=Math.max(...paths.map(x=>x.s)),weights=paths.map(x=>Math.exp(x.s-max)),z=weights.reduce((a,b)=>a+b,0);return {z:max+Math.log(z),g:zero().map((_,i)=>paths.reduce((a,x,j)=>a+x.f[i]*weights[j],0)/z),n:BigInt(paths.length)}}
 function loss(m,w){let a=dp(m.map(()=>7),w),b=dp(m,w);if(!b||!b.n)return null;return {v:a.z-b.z,g:sub(a.g,b.g),paths:b.n,all:a.n}}
 const w=[-.4,.2,.1,.3],ws=[[0,0,0,0],w,[1000,-1000,500,-300]],r={masks:0,valid:0,conflicts:0,comparisons:0,extremeComparisons:0,gradientChecks:0,maxLogError:0,maxMeanError:0,maxGradientError:0,corpus:{turns:0,spans:0,positivePositions:0,otherPositions:0,rightBoundaryOnly:0,noPositive:0,forcedOArtificialSignal:0,partialLoss:0,forcedLoss:0,maxCompatiblePaths:"0"}};
 for(let n=1;n<=4;n++){function walk(m){if(m.length<n){for(let i=1;i<=7;i++)walk([...m,i]);return}r.masks++;let a=dp(m,w);if(a.n)r.valid++;else r.conflicts++;
 for(let k=0;k<ws.length;k++){let x=dp(m,ws[k]),y=brute(m,ws[k]);ck(x.n===y.n,"count");if(x.n){let e=Math.abs(x.z-y.z),f=Math.max(...sub(x.g,y.g).map(Math.abs));ck(e<1e-8&&f<1e-8,"agreement");r.maxLogError=Math.max(r.maxLogError,e);r.maxMeanError=Math.max(r.maxMeanError,f)}r.comparisons++;if(k===2)r.extremeComparisons++}
 if(a.n){let q=loss(m,w);for(let i=0;i<4;i++){let u=[...w],v=[...w],h=1e-5;u[i]+=h;v[i]-=h;let e=Math.abs((loss(m,u).v-loss(m,v).v)/(2*h)-q.g[i]);ck(e<1e-7,"gradient");r.maxGradientError=Math.max(r.maxGradientError,e);r.gradientChecks++}}}walk([])}
 for(let d=0;d<2;d++)for(const e of docs[d].cases)for(const t of e.turns){let m=Array(t.text.length).fill(7),f=m.map(()=>1),positive=m.map(()=>false),spans=[];
 for(const a of (d===0?t.claims:t.proposal.claims).filter(a=>d===0?["HARD","CONDITIONAL_HARD"].includes(a.kind):a.role==="constraint")){let q=d===0?a.span:a.quote,s=t.text.indexOf(q),end=s+q.length;ck(s>=0&&s===t.text.lastIndexOf(q),"unique");for(let i=s;i<end;i++){ck(!positive[i],"overlap");positive[i]=true;m[i]=f[i]=i===s?2:4}spans.push([s,end])}
 for(const [s,end] of spans)if(end<m.length)m[end]&=3;let p=loss(m,w),b=loss(f,w),c=r.corpus;ck(p&&b&&b.paths===1n&&p.paths>=b.paths&&p.v<=b.v+1e-9,"nested");
 c.turns++;c.spans+=spans.length;c.positivePositions+=positive.filter(Boolean).length;c.otherPositions+=positive.filter(x=>!x).length;c.rightBoundaryOnly+=m.filter((x,i)=>!positive[i]&&x!==7).length;c.partialLoss+=p.v;c.forcedLoss+=b.v;if(p.paths>BigInt(c.maxCompatiblePaths))c.maxCompatiblePaths=String(p.paths);
 if(!spans.length){c.noPositive++;ck(Math.abs(p.v)<1e-12&&p.g.every(x=>Math.abs(x)<1e-12),"no supervision");c.forcedOArtificialSignal+=+(b.v>0&&b.g.some(x=>Math.abs(x)>1e-12))}}
 return r;
}
```

```json
{
  "masks": 2800,
  "valid": 2174,
  "conflicts": 626,
  "comparisons": 8400,
  "extremeComparisons": 2800,
  "gradientChecks": 8696,
  "maxLogError": 8.881784197001252e-16,
  "maxMeanError": 1.3322676295501878e-15,
  "maxGradientError": 6.950329201060867e-11,
  "corpus": {
    "turns": 64,
    "spans": 25,
    "positivePositions": 206,
    "otherPositions": 1560,
    "rightBoundaryOnly": 25,
    "noPositive": 41,
    "forcedOArtificialSignal": 41,
    "partialLoss": 161.28355324064992,
    "forcedLoss": 1483.4465943279354,
    "maxCompatiblePaths": "12200160415121876738"
  }
}
```

下一步以候选结构图和跨轮引用为主，研究局部链无法表述的约束及不完整标注的结构化排序，不重复此目标函数数值枚举；保持训练另授权、完整12项版本范围、独立留出及零新增费用。无生产修改、训练、Codex、CI、合并或部署。冻结协议不变。