# 自主学习：冻结预测对的缺失及更正反馈锐界
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线及去重
固定main aade53954c6f0804a13c82e7afaf29a18ee22d33，读取20近期提交、15开放Draft PR、v3.2、同步规程、唯一产品交接前20行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。#63 head 734686980b19da9291bdd08b67d4e2519c011acf，仍Draft，未重跑。固定既有资产：C025 Dawid逐次预测卡 2e78551a3098ec217e3062b3b3044af9e6aca9a6；feedback-replay-and-rollback/README.md f55a6fb6a801bb765b96530ce71b45e58d802852；purpose-bound-feedback-lineage-replay.md 5d2695da1f5a380369714adb5dd6fe0a5cdaa8db；paired-policy-feedback-bounds.md 93ba01e1fb71e32e0f7ed7e57c5acc76afb9b091；sequential-model-admission/README.md a2decfe7ff548aa98c94477c247bb50b6961a49f；conditional-event-knowledge-time-replay.md 52c64f77aae28680aac0e5d53dc692aae8b5dd6c。上述实际读取相关段落，未重审原论文。已有配对政策价值界限、反馈重放、用途授权、连续统计审查；本轮仅研究冻结配对预测的共用标签损失差、缺失及修订，不能替代政策价值或序贯显著性。未进行全库无重复证明。
## 数学合同
固定唯一事件/行动版本/结局定义/预测截止时间/相同信息边界及模型版本的两项真实已发布预测p,q，p,q∈[0,1]；比较二元结局Y的Brier损失差d=(p-Y)^2-(q-Y)^2，正为新模型损失较低。d=p²-q²+2(q-p)Y。已核实且当前用途合格的同一行动实际结局为单点，待观察、证据撤回或实际执行其他行动时，目标结局保持{0,1}；不将未选行动结局或模型预测当事实。若没有成对预测或配对口径不符，标记不合格并单列冻结队列覆盖缺口，不可默默移出分母后宣称整个队列改善。当前数值界只针对所有配对预测存在的指定队列。
对有限队列固定等权，单事件下上界取共同Y支持上的min/max d，队列取和除以N。证明：d对Y仿射，枚举两个端点即精确；在各事件剩余结局支持为笛卡尔积的合同内，每项端点同时可取得，因此界尖锐。如果存在跨事件依赖或约束，只是外界。先分别给两个模型损失定界再相减，可能使同一结局取不相容值；共同标签配对界更紧。相同预测差恒0，即便结局未知；这不意味着预测已校准或结果已知。上下界严格正/负仅说明该有限队列比较方向，在零点相接时不宣称严格改善。固定组内同理；整体正不能抵消关键组可能退步。无概率/置信区间/真实因果或未来提升。不能将缺失结果设为0，不能仅凭完整病例得分宣布整个队列改善。未经授权不得实际更新模型。
冻结预测不可随结果更正而改变；评价版本绑定当前结局证据与查询时间，旧版结果仅可作有权限审计，证据撤回恢复未知而不回退旧标签。实际权限删除及数据保留/重授权须另行实现，实验保留历史仅为合成对照。未来正式统计审查仍需独立数据、条件均值假设、固定时序、依赖和缺失处理、重复审查控制；本轮不证明e-process在迟到/修订反馈下有效。
## 实际执行
原创标准JS连接器执行以下完整程序；预测为0,.25,.5,.75,1（整数0..4），差分整数单位1/16以免浮点误差。两记录25预测对×5状态=125行类型，125²=15625队列；三记录5选定预测对×5状态=25行类型，25³=15625队列；固定组首记录及其余。每队列直接枚举所有共同标签，核验锐界与边际外界；对照故意只用完整病例及缺失当0。zeroImputedFalsePositive和completeCaseUncertified仅表示正向结论未获严格界证明，不意味着真实方向必错；completeCaseContradicted表示上界<=0。25预测对×5³结局状态序列=3125三版本合成重放，每前缀与枚举及历史版本重算核对。配对资格19项控制，输入口径由人工夹具定义，不是可信鉴权或真实发布证明。所有计数为合成有限配置/检查，非独立用户或语言、真实预测效果。
```json
{
  "cases": 31250,
  "checks": 62500,
  "sharpCases": 31250,
  "strictlyTighter": 5424,
  "missingCases": 27750,
  "completeCases": 3500,
  "completeCasePositive": 9084,
  "completeCaseUncertified": 4488,
  "completeCaseContradicted": 0,
  "zeroImputedFalsePositive": 9279,
  "allMissingCases": 9000,
  "equalPredictionCancellation": 750,
  "overallPositiveButGroupUncertified": 2048,
  "overallPositiveButGroupRegresses": 512,
  "classes": {
    "EQUAL": 1118,
    "REGRESSES": 4596,
    "IMPROVES": 4596,
    "UNRESOLVED": 20940
  },
  "revisionChecks": 18750,
  "revisionWithdrawControls": 1875,
  "eligibilityControls": 19,
  "examples": []
}
```
## 接入及限制
建议研究接口 FrozenForecastPair、OutcomeEvidenceVersion、CohortManifest、PairedLossBounds，分别记录预测原始身份、事件与行动、目标及预测时间/信息边界、分组、资格、实际观察来源、评价版本和未覆盖项。输出均为只读候选，authority NONE。未实现签名、持久化、真实权限、时钟、结果定义、原生入口、真实个人学习、模型训练或上线门。研究者选择预测网格、队列大小、状态和分组；未授权为生产标准。独立轨后续验证真实冻结预测、迟到和更正、弃权和缺失配对、资格撤回、历史隔离及真实反馈效果。未修改生产代码、唯一交接、冻结协议及证据等级，未启动Codex、训练、PR合并、部署、主动CI或新增费用。
## 完整复算
Node标准JS，无依赖；本轮实际执行为连接器JS，未另行运行Node命令行。
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),range=n=>Array.from({length:n},(_,i)=>i),D=16;
 const loss=(p,y)=>(p-4*y)**2,diff=(r,y)=>loss(r.old,y)-loss(r.fresh,y);
 const support=r=>r.status==="observed0"?[0]:r.status==="observed1"?[1]:[0,1];
 const statuses=["observed0","observed1","pending","withdrawn","other_action"];
 const row=(old,fresh,status)=>({old,fresh,status});
 function bounds(rs){let lo=0,hi=0,ol=0,oh=0,nl=0,nh=0,observed=0,observedSum=0;for(const r of rs){const y=support(r),ds=y.map(v=>diff(r,v)),o=y.map(v=>loss(r.old,v)),n=y.map(v=>loss(r.fresh,v));lo+=Math.min(...ds);hi+=Math.max(...ds);ol+=Math.min(...o);oh+=Math.max(...o);nl+=Math.min(...n);nh+=Math.max(...n);if(y.length===1){observed++;observedSum+=ds[0]}}return {lo,hi,marginal:[ol-nh,oh-nl],observed,observedSum,n:rs.length,denominator:D*rs.length}}
 function oracle(rs){let a=[];function visit(i,s){if(i===rs.length){a.push(s);return}const r=rs[i];for(let y=0;y<=1;y++){if(r.status==="observed0"&&y!==0||r.status==="observed1"&&y!==1)continue;visit(i+1,s+(r.old/4-y)**2*D-(r.fresh/4-y)**2*D)}}visit(0,0);return [Math.min(...a),Math.max(...a)]}
 const cls=(l,h)=>l>0?"IMPROVES":h<0?"REGRESSES":l===0&&h===0?"EQUAL":"UNRESOLVED";
 const out={cases:0,checks:0,sharpCases:0,strictlyTighter:0,missingCases:0,completeCases:0,completeCasePositive:0,completeCaseUncertified:0,completeCaseContradicted:0,zeroImputedFalsePositive:0,allMissingCases:0,equalPredictionCancellation:0,overallPositiveButGroupUncertified:0,overallPositiveButGroupRegresses:0,classes:{},revisionChecks:0,revisionWithdrawControls:0,eligibilityControls:0,examples:[]};
 function test(rs){out.cases++;const b=bounds(rs),o=oracle(rs),k=cls(b.lo,b.hi);ck(eq([b.lo,b.hi],o),"sharp");out.checks++;out.sharpCases++;out.classes[k]=(out.classes[k]??0)+1;ck(b.marginal[0]<=b.lo&&b.hi<=b.marginal[1],"marginal");out.checks++;out.strictlyTighter+=+(b.marginal[0]<b.lo||b.hi<b.marginal[1]);out.missingCases+=+(b.observed<rs.length);out.completeCases+=+(b.observed===rs.length);out.allMissingCases+=+(b.observed===0);if(b.observed>0&&b.observedSum>0){out.completeCasePositive++;out.completeCaseUncertified+=+(b.lo<=0);out.completeCaseContradicted+=+(b.hi<=0);if(b.hi<=0&&out.examples.length<2)out.examples.push({type:"complete_case",rs,b})}let zero=rs.reduce((s,r)=>s+diff(r,r.status==="observed1"?1:0),0);out.zeroImputedFalsePositive+=+(zero>0&&b.lo<=0);if(rs.every(r=>r.old===r.fresh)){ck(b.lo===0&&b.hi===0,"equal");out.equalPredictionCancellation++}if(b.lo>0){const gs=[bounds(rs.slice(0,1)),bounds(rs.slice(1))];out.overallPositiveButGroupUncertified+=+gs.some(g=>g.lo<0);out.overallPositiveButGroupRegresses+=+gs.some(g=>g.hi<0)}}
 const all=range(5).flatMap(a=>range(5).flatMap(b=>statuses.map(s=>row(a,b,s))));for(const a of all)for(const b of all)test([a,b]);
 const small=[[0,4],[4,0],[1,3],[2,2],[3,1]].flatMap(([a,b])=>statuses.map(s=>row(a,b,s)));for(const a of small)for(const b of small)for(const c of small)test([a,b,c]);
 // The same forecast is immutable while the actual outcome versions change.
 const transitions=["observed0","observed1","pending","withdrawn","other_action"];
 for(let a=0;a<=4;a++)for(let b=0;b<=4;b++)for(const s of transitions)for(const t of transitions)for(const u of transitions){const forecast=Object.freeze({old:a,fresh:b}),timeline=[s,t,u];let saved=[];for(let k=0;k<timeline.length;k++){const r={...forecast,status:timeline[k]},v=bounds([r]);ck(eq([v.lo,v.hi],oracle([r])),"version");saved.push(v);out.revisionChecks++;if(timeline[k]==="withdrawn"){const missing=bounds([{...forecast,status:"pending"}]);ck(eq(v,missing),"no fallback");out.revisionWithdrawControls++}}for(let k=0;k<3;k++){ck(eq(saved[k],bounds([{...forecast,status:timeline[k]}])),"historic");out.revisionChecks++}ck(forecast.old===a&&forecast.fresh===b,"immutable")}
 // Compare only precommitted forecasts for identical outcome, action, horizon and information boundary.
 const a={event:"E",action:"A",target:"binary-Y",horizon:10,issue:2,info:2,version:"old",p:2},b={...a,version:"new",p:3},manifest={event:"E",action:"A",target:"binary-Y",horizon:10,issue:2,info:2,versions:["old","new"],outcomeKnown:8};
 function qualify(x,y,m){const fields=["event","action","target","horizon","issue","info"];return !!x&&!!y&&fields.every(k=>x[k]===m[k]&&y[k]===m[k])&&x.issue<m.outcomeKnown&&x.info<=x.issue&&x.version===m.versions[0]&&y.version===m.versions[1]&&[x.p,y.p].every(p=>Number.isInteger(p)&&p>=0&&p<=4)}
 ck(qualify(a,b,manifest),"qualified");out.eligibilityControls++;for(const k of ["event","action","target","horizon","issue","info","version","p"]){for(const side of [0,1]){const bad=k==="p"?5:k==="horizon"||k==="issue"||k==="info"?9:"wrong";let x=side===0?{...a,[k]:bad}:a,y=side===1?{...b,[k]:bad}:b;ck(!qualify(x,y,manifest),"wrong pair");out.eligibilityControls++}}ck(!qualify(a,null,manifest),"missing prediction");out.eligibilityControls++;ck(!qualify(a,b,{...manifest,outcomeKnown:2}),"lookahead");out.eligibilityControls++;
 return out
}
console.log(JSON.stringify(experiment(),null,2));
```
