# 自主科学知识：共同上游证据根、最小支持集与来源损失证书
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与去重
起点main 9f0f24d6f6259dd657a49c07b454f39ab6b0083b，实际查询25近期提交、15开放PR，#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍draft。读取v3.2、同步规程及历史唯一交接固定blob 5e74f4f0b37141d631740e844ad8bbbfed232e07前段（未核对最新交接路径）。阅读固定前序research/decision_hub/2026-11-26-world-scoped-signed-inference-and-proof-retraction.md blob bb5596aa97731c536ff0b6aa66045bb4311ec7f1、版本差分57baff2229328ad2391c31dd6285c562b7349834、分域方法隔离ae545156e4ed8d39a96f940ab3aaac0b6cecad51、来源关系dff5ab32d4ea2698256f725f1ae3726578e4a015、知识资格df5a962a58ba0601b6014fad47c39cd3ebdb0e33相关合同。六关键词代码搜索无结果，非全库查重。前序已引用de Kleer ATMS及Green等来源半环摘要，本轮复用已有背景、不重审原论文，不宣称原创ATMS、最小击中集或半环理论。前序仅保存每槽一个见证，本轮新增固定共同上游根的全部最小有限证明支持和损失集合，实际调用原close/ref/status作逐根掩码参照。
## 数学合同
固定8符号槽（四个独立正负对），2..4联合世界、6个已确认的共同上游资格/失效根。源与规则各有世界范围及一组必要根；根可代表同一原数据、公共方法依赖或同一授权来源，需由可信宿主独立确认，不能按网站、作者或相似度推定统计独立。每个根可被共同撤回；本轮不研究新增未知来源、开放世界、概率可靠性、真实证据权重或因果推断。根掩码0仅表示不依赖此指定损失域，不代表现实无来源。所有资格、世界覆盖、规则正确性及根身份外部给定；输出研究只读authority NONE。
对每世界符号槽保留包含关系极小支持集族。初始源添加其全部必要根；规则对每个前件选择一个支持，与规则必要根取并，加入头的支持族，移除被真子集包含的支持。对任意可用根集A，支持族中存在S⊆A当且仅当在仅保留必要根均可用的源及规则的Horn闭包内可得。证明：每次添加有有限证明，删除超集保持任意A的存在性；从底迭代，任何有限推导的前件支持可替换为其子集，归纳得稳定时所有可推导槽可表示；有限根域的向上闭包单调扩大，必终止。循环不凭空产生支持。每个极小支持保留不可变证明对象，替代证明被剪枝时原对象仍可供已有证明验证；本原型未做实际撤权后的对象擦除，不可用于真实数据保留。最小损失集D与每个支持S相交，等价于撤回D后无支持；空支持族的最小损失为0，包含空支持的族在指定根域内无损失集。损失集大小是指定根撤回次数，不是统计独立性或概率。两条替代证明共享同一根时仍可被单点失效；只检查第一个证明也可能错误宣告丧失支持。各世界及正负槽独立；撤回只能移除支持，不通过冲突推出无关结论。预算不完全时已有支持/冲突见证可展示，缺失证明或完整损失界不得发布。覆盖未确认不声明全称。预算计规则世界扫描，不计笛卡尔组合、证明内存或墙时；根数较大时指数增长。
## 实际执行
700合成图，2..4世界、5..11源、6..18规则、6根、1..3前件，固定种子及共享根生成。完整 antichain 对全部64个可用根集合，实际调用上一轮close及逐世界ref，核验每个槽位、极小支持和极小损失集合。独立审查递归证明的根并集、世界、前件及有限性。4档扫描预算及两个损失情景对照完整结果，覆盖门检查。6专项控制含重复报告、共同规则根、无根循环、指定域外支持、世界分离、未知覆盖。实际标准JS两次一致；研究者选定规模、根、损失与基线，合成重复图非真实用户、真实论文来源关系、独立科学证据或性能。
```json
{
  "graphs": 700,
  "worlds": 2099,
  "completeProofs": 13816,
  "partialProofs": 42634,
  "closureChecks": 44800,
  "worldSlotChecks": 1074688,
  "minimalSupportChecks": 16792,
  "cutChecks": 16792,
  "partialChecks": 22400,
  "partialConflictWitnesses": 9105,
  "sharedRootFalseRedundancy": 462,
  "firstProofFalseLoss": 3868,
  "cutSizeHistogram": {
    "0": 7194,
    "1": 6770,
    "2": 2369,
    "3": 417,
    "4": 41,
    "5": 1
  },
  "scans": 65595,
  "maxAntichain": 7,
  "controls": 6,
  "example": {
    "w": 1,
    "p": 7,
    "supports": [
      12,
      40
    ],
    "cuts": [
      8,
      36
    ]
  }
}
```
## 接入
建议将知识索引的文献ID与真实数据/方法/授权依赖根分开，所有根资格由宿主提供并绑定当前版本。返回最小支持及最小损失见证，不以文献数当独立证据数。下一阶段应将证明集连接实际决策端口的联合依赖以及来源更新后的有限重算；未经独立科学资格及原生验证不可升级。未修改生产、唯一交接、冻结、证据等级、PR、训练、部署、主动CI或费用。原生、独立留出、真机、真实来源归因未运行。
## 复算
固定前序报告作为唯一输入，Node包装未执行，连接器实际运行核心。只执行已审阅项目自有源码。
```js
const code=require("node:fs").readFileSync(process.argv[2],"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0];
const make=Function(code.split(" const out={cases:")[0]+"\nreturn {close,verify,ref,status};\n}\nreturn experiment();");
function study(make){
 const R=make(),ck=(v,m)=>{if(!v)throw Error(m)},N=8,G=6,ALL=63,eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),sub=(a,b)=>(a&b)===a;
 let seed=20261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const pop=m=>{let n=0;while(m){m&=m-1;n++}return n};
 const min=xs=>[...new Set(xs)].filter(x=>!xs.some(y=>y!==x&&sub(y,x))).sort((a,b)=>a-b);
 function derive(W,S,Q,budget=Infinity){
  let f=Array.from({length:W},()=>Array.from({length:N},()=>[])),proof=Array.from({length:W},()=>Array.from({length:N},()=>new Map())),scans=0,inserted=0;
  function add(w,p,m,z){
   let a=f[w][p];if(a.some(x=>sub(x,m)))return false;
   f[w][p]=[...a.filter(x=>!sub(m,x)),m].sort((a,b)=>a-b);
   // Keep immutable proof objects, even if later pruned from the antichain.
   proof[w][p].set(m,z);inserted++;return true;
  }
  for(let w=0;w<W;w++)for(let i=0;i<S.length;i++){let s=S[i];if(s.w&(1<<w))add(w,s.p,s.g,{kind:"s",i,m:s.g});}
  for(let changed=true;changed;){
   changed=false;
   for(let w=0;w<W;w++)for(let i=0;i<Q.length;i++){
    if(scans===budget)return {f,proof,scans,inserted,done:false};
    scans++;
    const q=Q[i];if(!(q.w&(1<<w)))continue;
    // Snapshot live supports before deriving, including self-referential rules.
    const options=q.b.map(p=>f[w][p].map(m=>({m,z:proof[w][p].get(m)})));
    function walk(k,m,children){
     if(k===options.length){if(add(w,q.h,m,{kind:"r",i,m,children}))changed=true;return}
     for(let x of options[k])walk(k+1,m|x.m,[...children,x.z]);
    }
    walk(0,q.g,[]);
   }
  }
  return {f,proof,scans,inserted,done:true};
 }
 function audit(W,S,Q,z){
  let checked=0;
  function v(w,p,x,stack){
   ck(x&&!stack.has(x),"finite proof");stack.add(x);
   if(x.kind==="s"){let s=S[x.i];ck(s.p===p&&(s.w&(1<<w))&&s.g===x.m,"source witness")}
   else {let q=Q[x.i];ck(q.h===p&&(q.w&(1<<w))&&x.children.length===q.b.length,"rule witness");let m=q.g;for(let j=0;j<q.b.length;j++){v(w,q.b[j],x.children[j],stack);m|=x.children[j].m}ck(m===x.m,"union")}
   stack.delete(x);
  }
  for(let w=0;w<W;w++)for(let p=0;p<N;p++){ck(eq(z.f[w][p],min(z.f[w][p])),"antichain");for(let m of z.f[w][p]){let x=z.proof[w][p].get(m);ck(x.m===m,"mask");v(w,p,x,new Set());checked++}}
  return checked;
 }
 function oracle(W,S,Q,available){
  const s=S.filter(s=>sub(s.g,available)).map(s=>[s.p,s.w]),r=Q.filter(q=>sub(q.g,available)).map(q=>[q.h,q.b,q.w]);
  let z=R.close(W,s,r);ck(eq(z.a,R.ref(W,s,r)),"previous closure reference");
  return z.a;
 }
 function cuts(f){
  // Removing any set meeting every support destroys the proposition.
  return min(Array.from({length:64},(_,i)=>i).filter(m=>f.every(s=>s&m)));
 }
 function status(f,p,loss,done,covered){
  const pos=f.map(a=>a[p*2].some(m=>!(m&loss))),neg=f.map(a=>a[p*2+1].some(m=>!(m&loss)));
  if(pos.some((v,i)=>v&&neg[i]))return "CONFLICT_WITNESS";
  if(!done||!covered)return "UNRESOLVED";
  if(pos.every(Boolean)&&!neg.some(Boolean))return "ALL_POS";
  if(neg.every(Boolean)&&!pos.some(Boolean))return "ALL_NEG";
  if(pos.every((v,i)=>v||neg[i]))return "DIFFERENT_WORLDS";
  return "UNRESOLVED";
 }
 const out={graphs:0,worlds:0,completeProofs:0,partialProofs:0,closureChecks:0,worldSlotChecks:0,minimalSupportChecks:0,cutChecks:0,partialChecks:0,partialConflictWitnesses:0,sharedRootFalseRedundancy:0,firstProofFalseLoss:0,cutSizeHistogram:{},scans:0,maxAntichain:0,controls:0,example:null};
 for(let g=0;g<700;g++){
  let W=2+rnd(3),full=(1<<W)-1;
  let S=Array.from({length:5+rnd(7)},()=>({p:rnd(N),w:1+rnd(full),g:1<<rnd(G)}));
  // Some reports and rules depend on multiple shared upstream roots.
  for(let s of S)if(rnd(4)===0)s.g|=1<<rnd(G);
  let Q=Array.from({length:6+rnd(13)},()=>({h:rnd(N),b:[...new Set(Array.from({length:1+rnd(3)},()=>rnd(N)))],w:1+rnd(full),g:rnd(3)?0:1<<rnd(G)}));
  let z=derive(W,S,Q);out.completeProofs+=audit(W,S,Q,z);out.scans+=z.scans;
  let truth=[];
  for(let a=0;a<=ALL;a++){
   let v=oracle(W,S,Q,a);truth.push(v);out.closureChecks++;
   for(let w=0;w<W;w++)for(let p=0;p<N;p++){ck(z.f[w][p].some(m=>sub(m,a))===!!(v[p]&(1<<w)),"all availability");out.worldSlotChecks++}
  }
  for(let w=0;w<W;w++)for(let p=0;p<N;p++){
   let f=z.f[w][p],v=min(Array.from({length:64},(_,i)=>i).filter(a=>truth[a][p]&(1<<w)));
   ck(eq(f,v),"minimal support");out.minimalSupportChecks++;out.maxAntichain=Math.max(out.maxAntichain,f.length);
   let c=cuts(f),ref=min(Array.from({length:64},(_,i)=>i).filter(m=>!(truth[ALL^m][p]&(1<<w))));
   ck(eq(c,ref),"minimal loss");out.cutChecks++;
   const k=c.length?Math.min(...c.map(pop)):7;out.cutSizeHistogram[k]=(out.cutSizeHistogram[k]||0)+1;
   if(f.length>1&&k===1){out.sharedRootFalseRedundancy++;out.example??={w,p,supports:f,cuts:c}}
   if(f.length)for(let j=0;j<G;j++)if((f[0]&(1<<j))&&f.some(m=>!(m&(1<<j))))out.firstProofFalseLoss++;
  }
  for(let cap of [0,4,16,48]){
   let p=derive(W,S,Q,cap);out.partialProofs+=audit(W,S,Q,p);
   for(let loss of [0,1<<rnd(G)]){
    for(let i=0;i<4;i++){
     let got=status(p.f,i,loss,p.done,true),want=R.status(truth[ALL^loss],i,full,true,true);
     ck(got==="UNRESOLVED"||got===want,"partial port");if(got==="CONFLICT_WITNESS")out.partialConflictWitnesses++;
     ck(status(p.f,i,loss,p.done,false)==="UNRESOLVED"||status(p.f,i,loss,p.done,false)==="CONFLICT_WITNESS","coverage");
     out.partialChecks++;
    }
   }
  }
  out.graphs++;out.worlds+=W;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 let z=derive(1,[{p:0,w:1,g:1},{p:0,w:1,g:1}],[]);
 ctl(eq(z.f[0][0],[1])&&eq(cuts(z.f[0][0]),[1]),"duplicate source");
 z=derive(1,[{p:0,w:1,g:1},{p:1,w:1,g:2}],[{h:2,b:[0],w:1,g:4},{h:2,b:[1],w:1,g:4}]);
 ctl(eq(z.f[0][2],[5,6])&&eq(cuts(z.f[0][2]),[3,4]),"shared rule root");
 z=derive(1,[],[{h:0,b:[1],w:1,g:0},{h:1,b:[0],w:1,g:0}]);
 ctl(z.f[0].every(f=>!f.length),"cycle no support");
 z=derive(1,[{p:0,w:1,g:0}],[]);
 ctl(eq(z.f[0][0],[0])&&cuts(z.f[0][0]).length===0,"outside designated loss roots");
 z=derive(2,[{p:0,w:1,g:1},{p:1,w:2,g:2}],[]);
 ctl(status(z.f,0,0,true,true)==="DIFFERENT_WORLDS","world separation");
 ctl(status(z.f,0,0,true,false)==="UNRESOLVED","coverage");
 return out;
}
console.log(JSON.stringify(study(make),null,2));
```
