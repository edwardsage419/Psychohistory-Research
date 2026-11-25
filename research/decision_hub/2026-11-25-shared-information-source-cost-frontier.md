# 多来源信息获取的共享成本与双资源最小分离前沿
2026-11-25。RESEARCH_CANDIDATE / EXACT_FINITE_DEVELOPMENT_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 49247d54f32d2e71e5f2c040f12f357f8cdc555f；Draft #62固定候选 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期10提交、14开放PR、v3.2前15行、同步规程前22行、唯一产品交接前18行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。检索clarification/information value/question/information acquisition/cost/separation/acquisition/shared evidence/information source/prerequisite/bundle/Pareto；读取R5 eae10ff00db50587513bc72f628a7f0b8cd5ed8b、R40 1507376849edac68a46f352063a814b0434fd81a、R132 3a725062c742cc0116d29e0f28640bfacbecafbf、R123 15e1e1409464183290fa57b296ae453d8f13a741及序贯调查6d77d939b0cb3f5eebe9f7c58961d742cf80d778的合同与算法前段。已有多轮追问、拒答、延迟失败、相关支持下最小字段及现金时间约束；本轮只新增多个确定性来源共用一次获取成本、来源资格与独立现金/时间预算下的非自适应组合前沿。沿用R132分离定理，非新通用问询DP或信息价值理论；全库去重仍有限。

## 合同
可信宿主已确认完整非空有限关联世界W⊆{0,1}³及一个二元决策签名f(w)。四个来源各确定返回字段集合1、2、4、3（位掩码）；前两来源共享获取A，后两共享获取B；每来源有增量现金/时间成本，首次获取共享文档/授权通道的固定费用按身份只计一次。具体成本为代码中的整数夹具，时间假设顺序相加，无并行、延迟、拒答、失败、动态成本或真实授权；允许来源掩码由可信宿主给定，组A不可用则排除其两个来源，绝不把获取资格视为用户实际同意。签名完整性、证据权威、实际来源可用性和确定回答均人工给定。另设必需核实字段bit2，即使签名不变仍须单独取得；实际授权及重大风险核查独立于数学分离。用户拒绝、无来源或覆盖未知时保留UNKNOWN/UNRESOLVED；空支持CONFLICT。不能把信息获取费用当现实价值或预算授权，所有输出authority NONE。

## 推导
沿R132，对每对签名不同的世界生成差异字段掩码D。来源子集Q的字段并集F(Q)必须与所有D相交，并包含必需字段；必要性为答案相同却签名不同，充分性为不同签名不可能同一答案桶。每个来源增量费用及其所依赖的共享获取操作按规范身份并集计成本，分别计算现金及时间，不作默认加权。对合格分离子集保留成本不受其他子集严格支配的全部候选（同成本不同子集保留）；给定两个预算时，存在合格子集当且仅当前沿存在同时不超过预算的点。该性质由有限偏序中每个被支配点均存在不受支配点弱支配。无足够预算不说明用户目标本身不可行。共享费用须有明确相同操作身份、相同时点及适用资格；不同文档或重复付费不可误合并。枚举2^4来源集合，世界差异O(|W|²)，一般域指数增长，本轮未测真实资源。真实查询须先执行本地检索和最小权限判断，禁止自动上传个人决策数据；本轮不调用网络调查、不实际询问、不支付、不自动授权。

## 实验
255非空支持×256签名真值表×3模式（全来源/全来源加必需字段/组A不获准）=195840组合。独立按实际答案分桶和显式操作集合成本比较完整合格集合，前沿使用共同支配函数（不是独立前沿实现），每组5种现金/时间预算逐一核对前沿与全集合的可行性。对照按来源重复计算共享设置费用、忽略资格以及按每个来源独立单位现金成本贪心（实际预算检查用正确并集费用），均为人为对照，不是原生产品或普通AI错误率。重复世界标签及预算组合非独立用户样本，计数不可视为真实概率。第一次运行参照函数未定义y，未写仓库；修复后完整重跑。12控制。研究者选择成本、模式、必需字段、预算及非自适应合同，不代表正式产品政策。无新增外部资料、个人数据、真实训练、原生API、设备测量、CI请求、PR合并、部署、费用或冻结变更。Node标准JS。

```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),W=[0,1,2,3,4,5,6,7];
 const fields=[1,2,4,3],groups=[1,1,2,2],local=[[1,1],[1,1],[1,1],[3,1]],setup=[[2,1],[1,2]];
 const dominates=(a,b)=>a.cash<=b.cash&&a.time<=b.time&&(a.cash<b.cash||a.time<b.time);
 const front=xs=>xs.filter(b=>!xs.some(a=>dominates(a,b))).map(x=>x.q).sort((a,b)=>a-b);
 const fit=(xs,c,t)=>xs.some(x=>x.cash<=c&&x.time<=t);
 function options(support,labels,allowed,required,covered=true){
  if(!covered)return {status:"UNKNOWN",authority:"NONE"};
  if(!support)return {status:"CONFLICT",authority:"NONE"};
  const ws=W.filter(w=>support&(1<<w)),clauses=new Set();
  for(let i=0;i<ws.length;i++)for(let j=i+1;j<ws.length;j++)if(((labels>>ws[i])&1)!==((labels>>ws[j])&1))clauses.add(ws[i]^ws[j]);
  let xs=[];
  for(let q=0;q<16;q++){
   if((q&allowed)!==q)continue;
   let f=0,g=0,cash=0,time=0,naiveCash=0,naiveTime=0;
   for(let j=0;j<4;j++)if(q&(1<<j)){
    f|=fields[j];g|=groups[j];cash+=local[j][0];time+=local[j][1];
    naiveCash+=local[j][0]+setup[groups[j]-1][0];naiveTime+=local[j][1]+setup[groups[j]-1][1];
   }
   if((f&required)!==required||[...clauses].some(d=>!(f&d)))continue;
   for(let j=0;j<2;j++)if(g&(1<<j)){cash+=setup[j][0];time+=setup[j][1]}
   xs.push({q,cash,time,naiveCash,naiveTime});
  }
  return {status:xs.length?"CONDITIONAL":"UNRESOLVED",authority:"NONE",xs,front:front(xs)};
 }
 function oracle(support,labels,allowed,required){
  let valid=[];
  for(let q=0;q<16;q++){
   let ids=[0,1,2,3].filter(j=>q&(1<<j));if(ids.some(j=>!(allowed&(1<<j))))continue;
   let bins=new Map(),yes=true;
   for(let w of W)if(support&(1<<w)){
    let answer=ids.map(j=>w&fields[j]).join(","),y=(labels>>w)&1;
    if(bins.has(answer)&&bins.get(answer)!==y){yes=false;break}bins.set(answer,y);
   }
   if(!yes||((ids.reduce((f,j)=>f|fields[j],0)&required)!==required))continue;
   let ops=new Map();for(let j of ids){ops.set("read"+j,local[j]);ops.set("setup"+groups[j],setup[groups[j]-1])}
   let cash=0,time=0;for(let v of ops.values()){cash+=v[0];time+=v[1]}
   valid.push({q,cash,time});
  }return valid;
 }
 let o={cases:0,sourceSets:0,frontierChecks:0,budgetChecks:0,unresolved:0,noQuestion:0,tradeoffCases:0,doubleCountFalseUnresolved:0,permissionBlindFalseResolved:0,greedyFalseUnresolved:0,mandatoryIncreases:0,controls:0,witnesses:{}};
 function greedy(support,labels,allowed,required,bc,bt){
  let ws=W.filter(w=>support&(1<<w)),f=0,q=0;
  let pairs=[];for(let a of ws)for(let b of ws)if(a<b&&((labels>>a)&1)!==((labels>>b)&1))pairs.push(a^b);
  for(let step=0;step<4;step++){
   if((f&required)===required&&pairs.every(d=>d&f))return true;
   let opts=[];
   for(let j=0;j<4;j++)if((allowed&(1<<j))&&!(q&(1<<j))){
    let n=q|(1<<j),ids=[0,1,2,3].filter(k=>n&(1<<k)),g=ids.reduce((s,k)=>s|groups[k],0);
    let c=ids.reduce((s,k)=>s+local[k][0],0),t=ids.reduce((s,k)=>s+local[k][1],0);
    for(let k=0;k<2;k++)if(g&(1<<k)){c+=setup[k][0];t+=setup[k][1]}
    if(c>bc||t>bt)continue;
    let score=pairs.filter(d=>!(d&f)&&(d&fields[j])).length+((fields[j]&required&~f)?1:0);
    if(score)opts.push({j,score,c:local[j][0]+setup[groups[j]-1][0],t:local[j][1]+setup[groups[j]-1][1]});
   }
   if(!opts.length)return false;
   opts.sort((a,b)=>b.score*a.c-a.score*b.c||a.t-b.t||a.j-b.j);let j=opts[0].j;q|=1<<j;f|=fields[j];
  }return (f&required)===required&&pairs.every(d=>d&f);
 }
 for(let m=1;m<256;m++)for(let l=0;l<256;l++){
  let all=options(m,l,15,0);
  for(let [allowed,required] of [[15,0],[15,4],[12,0]]){
   let v=options(m,l,allowed,required),ref=oracle(m,l,allowed,required);
   ck(eq(v.xs.map(({q,cash,time})=>({q,cash,time})),ref),"oracle costs and separation");
   ck(eq(v.front,front(ref)),"frontier");
   o.cases++;o.frontierChecks++;o.sourceSets+=v.xs.length;o.unresolved+=+!v.xs.length;o.noQuestion+=+v.front.includes(0);
   let cf=v.xs.filter(x=>v.front.includes(x.q));if(new Set(cf.map(x=>x.cash+","+x.time)).size>1)o.tradeoffCases++;
   if(allowed===15&&required===4&&all.front.includes(0)&&!v.front.includes(0))o.mandatoryIncreases++;
   for(let [bc,bt] of [[3,3],[4,3],[4,5],[5,4],[6,5]]){
    let good=fit(v.xs,bc,bt),pf=fit(cf,bc,bt);
    ck(good===pf&&good===fit(ref,bc,bt),"budget");o.budgetChecks++;
    let naive=v.xs.some(x=>x.naiveCash<=bc&&x.naiveTime<=bt);
    if(good&&!naive){o.doubleCountFalseUnresolved++;o.witnesses.double??={m,l,allowed,required,bc,bt,front:cf}}
    if(allowed===12&&!good&&fit(all.xs,bc,bt)){o.permissionBlindFalseResolved++;o.witnesses.permission??={m,l,bc,bt}}
    if(good&&!greedy(m,l,allowed,required,bc,bt)){o.greedyFalseUnresolved++;o.witnesses.greedy??={m,l,allowed,required,bc,bt,front:cf}}
   }
  }
 }
 for(let t of [o.cases===195840,o.budgetChecks===979200,o.frontierChecks===o.cases,options(1,0,15,0).front.includes(0),!options(1,0,15,4).front.includes(0),options(255,170,0,0).status==="UNRESOLVED",options(0,0,15,0).status==="CONFLICT",options(1,0,15,0,false).status==="UNKNOWN",o.doubleCountFalseUnresolved>0,o.permissionBlindFalseResolved>0,o.greedyFalseUnresolved>0,o.tradeoffCases>0]){ck(t,"control "+o.controls);o.controls++}
 return o;
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实测
```json
{
  "cases": 195840,
  "sourceSets": 1230200,
  "frontierChecks": 195840,
  "budgetChecks": 979200,
  "unresolved": 0,
  "noQuestion": 25220,
  "tradeoffCases": 2688,
  "doubleCountFalseUnresolved": 135236,
  "permissionBlindFalseResolved": 12612,
  "greedyFalseUnresolved": 54404,
  "mandatoryIncreases": 12610,
  "controls": 12,
  "witnesses": {
    "double": {
      "m": 3,
      "l": 1,
      "allowed": 15,
      "required": 4,
      "bc": 5,
      "bt": 4,
      "front": [
        {
          "q": 12,
          "cash": 5,
          "time": 4,
          "naiveCash": 6,
          "naiveTime": 6
        }
      ]
    },
    "permission": {
      "m": 3,
      "l": 1,
      "bc": 3,
      "bt": 3
    },
    "greedy": {
      "m": 7,
      "l": 2,
      "allowed": 15,
      "required": 4,
      "bc": 5,
      "bt": 4,
      "front": [
        {
          "q": 12,
          "cash": 5,
          "time": 4,
          "naiveCash": 6,
          "naiveTime": 6
        }
      ]
    }
  }
}
```
后续：与R40的可停止问询策略及R123的延迟失败合同连接，真实来源资格、字段覆盖及费用由独立证据支持，产品轨维护唯一交接、独立轨检查未见真实入口和最小权限。无本轮正式版本开发授权。