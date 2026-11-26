# 自主科学知识：联合方法义务、候选证据补充及冲突包络
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线
同一手动轮第二阶段，起点main e2616e2a4062a515d37f603e2e5abaed153ca77f；沿用本轮已查询25近期提交、15开放PR、v3.2、同步规程、固定历史交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。实际读取执行固定自有研究代码：
research/decision_hub/2026-11-26-world-scoped-signed-inference-and-proof-retraction.md bb5596aa97731c536ff0b6aa66045bb4311ec7f1
research/decision_hub/2026-11-26-shared-evidence-root-minimal-support-and-loss-certificates.md 9d8285175299c57f1f0193a99b1805ba1d42de75
既有世界签名闭包、共同根最小证明、分域方法传递资格、共同参数及信息价值研究不重计；本轮新增全世界多义务的必要根集、反证阻断族与多根获取动作的条件成本枚举。查重有限，非新集合逻辑或实际科学准入。
## 合同及证明
固定6根、2..4世界、8符号槽、一或两个明确必须具有正支持且无负支持的研究义务。可信宿主独立给定当前资格根A、规则、世界覆盖及完整的未来条件根域。根集合代表已确定来源依赖，不是概率或实际事实。对每个世界每个义务的正支持族做并集笛卡尔组合、去除超集，得到最小联合正支持族Y；对全部反符号支持取并集并极小化得到阻断族N。任一根集B下，全部正义务各有证明当且仅当存在y∈Y包含于B；任一反符号可证当且仅当存在n∈N包含于B。因此条件端口正支持且无反证等价于前者真且后者假。跨世界只合并根需求，不将不同世界前件拼接。源和规则当前资格、真实科学充分性、时效、方法边界由独立可信宿主核验；仅符号条件成立不足以升级现实模型。预算未完成的支持族不能用于否定反证，本轮要求完整推理。
五项人工候选补充动作，每项若成功且经独立核对后可使一个或多个根合格，成本为同单位的非负虚构调查成本，固定初始状态，仅枚举动作子集；不保证获取成功、不会虚构事实、不执行网络请求或真实开支。对于每个动作集计算当前根与其结果根并集，再核对Y与N。保留所有可行的包含极小动作集及最低成本集合。新增来源可能同时产生反证，因此不能用单调可行性剪枝；已确认反证不能通过只增加来源自动抹去。仅假设性展示子集并不授权选择性隐瞒反证；现实已发现的任何有资格反证均须进入当前A，不能为获得通过结果而排除。调查需预设完整披露、可能失败及反面结果，本模型只计算指定成功条件下的数学方案，不能当真实信息价值或推荐购买。逐世界分别可补足不等于同一获取动作集可补足；共享获取动作不应重复计费。当前有资格的条件支持与未来假设性补充分别输出；覆盖不明返回UNKNOWN_COVERAGE。全部authority NONE。
## 实际实验
900合成图，每图2..4世界、6根、随机有符号源与规则、1或2义务、5个候选获取动作。实际执行前序derive，全部64个根集合使用原闭包及逐世界参照核对正与反证合同；32个获取动作集合核对极小及最低成本，比较仅看正支持、所有获取动作都执行、逐世界单独规划。6控制含新增反证、既有反证、当前与假设、共享动作与未知覆盖。标准JS两次实际执行结果一致。数值是合成结构及重复子集，非真实来源、独立科学验证、实际信息价值、真实用户或性能。研究者选定资格假设、成本、动作、义务及规模；未运行原生、独立留出、真机、真实网络或个人数据；未修改生产、交接、冻结、证据等级、PR、训练、部署、主动CI或费用。
```json
{
  "graphs": 900,
  "worlds": 2683,
  "rootAssignmentChecks": 57600,
  "acquisitionChecks": 28800,
  "minimalSetChecks": 57,
  "currentlySupported": 21,
  "hypotheticalAcquisition": 21,
  "noAcquisition": 858,
  "positiveOnlyFalsePass": 3898,
  "acquisitionIntroducesConflict": 3481,
  "fullAcquisitionLosesQualifiedSubset": 16,
  "perWorldFalseCommon": 4,
  "sharedAcquisitionSaving": 10,
  "controls": 6,
  "example": {
    "req": [
      0,
      1
    ],
    "current": 60,
    "acts": [
      {
        "roots": 32,
        "cost": 2
      },
      {
        "roots": 32,
        "cost": 5
      },
      {
        "roots": 6,
        "cost": 1
      },
      {
        "roots": 32,
        "cost": 3
      },
      {
        "roots": 32,
        "cost": 4
      }
    ],
    "positive": [
      10,
      12
    ],
    "negative": [
      2
    ],
    "min": [
      0
    ],
    "best": 0
  }
}
```
## 复算
固定两份报告按顺序传入；仅执行已审阅自有代码。Node包装未执行，连接器实际运行核心。
```js
const c=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0]);
const make=Function(c[0].split(" const out={cases:")[0]+"\nreturn {close,verify,ref,status};\n}\nreturn experiment();");
const make2=Function("make",c[1].slice(c[1].indexOf("function study(make){")).split(" const out={graphs:")[0]+"\nreturn {derive,audit,oracle,cuts,status};\n}\nreturn study(make);");
function experiment(make,make2){
 const P=make2(make),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),sub=(a,b)=>(a&b)===a,ALL=63,K=5;
 let seed=20261127;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const masks=n=>Array.from({length:1<<n},(_,i)=>i);
 const minimal=xs=>[...new Set(xs)].filter(x=>!xs.some(y=>x!==y&&sub(y,x))).sort((a,b)=>a-b);
 function compile(f,required){
  // Required positive slots all hold in every world; any opposite slot blocks.
  let yes=[0],no=[];
  for(let w=0;w<f.length;w++)for(let p of required){
   yes=minimal(yes.flatMap(a=>f[w][2*p].map(b=>a|b)));
   no=minimal([...no,...f[w][2*p+1]]);
  }
  return {yes,no};
 }
 function qualifies(z,a){return z.yes.some(s=>sub(s,a))&&!z.no.some(s=>sub(s,a))}
 function plan(z,current,actions,covered=true){
  if(!covered)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  const possible=masks(K).map(m=>{
   let available=current,cost=0;
   for(let j=0;j<K;j++)if(m&(1<<j)){available|=actions[j].roots;cost+=actions[j].cost}
   return {m,available,cost,ok:qualifies(z,available)};
  });
  const good=possible.filter(x=>x.ok),min=minimal(good.map(x=>x.m)),best=good.length?Math.min(...good.map(x=>x.cost)):null;
  return {status:qualifies(z,current)?"CURRENT_CONDITIONAL_SUPPORT":good.length?"HYPOTHETICAL_ACQUISITION":"NO_ENUMERATED_ACQUISITION",minimal:min,best,bestSets:good.filter(x=>x.cost===best).map(x=>x.m),authority:"NONE"};
 }
 const out={graphs:0,worlds:0,rootAssignmentChecks:0,acquisitionChecks:0,minimalSetChecks:0,currentlySupported:0,hypotheticalAcquisition:0,noAcquisition:0,positiveOnlyFalsePass:0,acquisitionIntroducesConflict:0,fullAcquisitionLosesQualifiedSubset:0,perWorldFalseCommon:0,sharedAcquisitionSaving:0,controls:0,example:null};
 for(let g=0;g<900;g++){
  let W=2+rnd(3),full=(1<<W)-1;
  let S=Array.from({length:6+rnd(9)},()=>({p:rnd(8),w:1+rnd(full),g:1<<rnd(6)}));
  let Q=Array.from({length:5+rnd(10)},()=>({h:rnd(8),b:[...new Set(Array.from({length:1+rnd(2)},()=>rnd(8)))],w:1+rnd(full),g:rnd(3)?0:1<<rnd(6)}));
  let req=rnd(2)?[0,1]:[0],current=rnd(64),acts=Array.from({length:K},()=>({roots:(1<<rnd(6))|(rnd(3)?0:1<<rnd(6)),cost:1+rnd(5)}));
  let z=P.derive(W,S,Q),f=compile(z.f,req),truth=[];
  for(let m=0;m<=ALL;m++){
   const a=P.oracle(W,S,Q,m),pos=req.every(p=>a[2*p]===full),neg=req.some(p=>a[2*p+1]!==0),ok=pos&&!neg;
   ck(qualifies(f,m)===ok,"joint root support");
   truth[m]={pos,neg,ok};out.rootAssignmentChecks++;
  }
  let p=plan(f,current,acts),raw=[];
  for(let m of masks(K)){
   let a=current,cost=0;
   for(let j=0;j<K;j++)if(m&(1<<j)){a|=acts[j].roots;cost+=acts[j].cost}
   if(truth[a].ok)raw.push({m,cost});
   if(truth[a].pos&&truth[a].neg)out.positiveOnlyFalsePass++;
   if(!truth[current].neg&&truth[a].neg)out.acquisitionIntroducesConflict++;
   out.acquisitionChecks++;
  }
  let min=minimal(raw.map(x=>x.m)),best=raw.length?Math.min(...raw.map(x=>x.cost)):null;
  ck(eq(p.minimal,min)&&p.best===best&&eq(p.bestSets,raw.filter(x=>x.cost===best).map(x=>x.m)),"acquisition parity");
  out.minimalSetChecks+=min.length;
  if(p.status==="CURRENT_CONDITIONAL_SUPPORT")out.currentlySupported++;else if(p.status==="HYPOTHETICAL_ACQUISITION")out.hypotheticalAcquisition++;else out.noAcquisition++;
  let total=acts.reduce((a,v)=>a|v.roots,current);
  if(raw.length&&!truth[total].ok){out.fullAcquisitionLosesQualifiedSubset++;out.example??={req,current,acts,positive:f.yes,negative:f.no,min,best}}
  let per=z.f.map(w=>plan(compile([w],req),current,acts));
  if(per.every(x=>x.best!==null)&&best===null)out.perWorldFalseCommon++;
  if(best!==null&&per.every(x=>x.best!==null)&&per.reduce((a,x)=>a+x.best,0)>best)out.sharedAcquisitionSaving++;
  ck(plan(f,current,acts,false).status==="UNKNOWN_COVERAGE","coverage");
  out.graphs++;out.worlds+=W;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 let acts=[{roots:1,cost:1},{roots:2,cost:1},{roots:4,cost:2},{roots:8,cost:2},{roots:16,cost:2}];
 let f={yes:[1],no:[2]};
 ctl(plan(f,0,acts).best===1&&qualifies(f,1)&&!qualifies(f,3),"more information can block");
 ctl(plan(f,2,acts).status==="NO_ENUMERATED_ACQUISITION","existing contrary support");
 ctl(plan(f,1,acts).status==="CURRENT_CONDITIONAL_SUPPORT","current vs hypothetical");
 ctl(plan({yes:[3],no:[]},0,acts).best===2,"joint evidence");
 ctl(plan({yes:[3],no:[]},0,[{roots:3,cost:1},...acts.slice(1)]).best===1,"shared action");
 ctl(plan(f,0,acts,false).status==="UNKNOWN_COVERAGE","unknown domain");
 return out;
}
console.log(JSON.stringify(experiment(make,make2),null,2));
```
