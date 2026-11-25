# 自主认知专项累计第81轮候选：概念多义性、方向关系与联合一致性

2026-11-25。RESEARCH_CANDIDATE / FINITE_CONCEPT_CSP_EXECUTED / RAW_LANGUAGE_NOT_RUN / TRAINING_NOT_AUTHORIZED / INDEPENDENT_ACCEPTANCE_NOT_RUN。基线 main 5ceb9700775d9ae2da3e703147051f1caac1fbe9。已核查近20提交、13开放PR、v3.2首8行及此前全文、唯一交接首15行（5e74f4f0b37141d631740e844ad8bbbfed232e07），R63数量联合语义、R64引用身份、R65歧义决策相关性、R66有根知识推理各首28行；不重做其固定语法、决策端口、来源撤回或R76引用图加权分区。R80词面排序未解决同义、多义与隐含对象。本轮仅研究语言候选进入概念关系推理后的有限联合一致性，不声称从原文自动发现概念或真实关系。无新外部资料，数学为有限约束搜索，不主张原创定理。

## 合同及证明
每个节点具有若干候选义项，关系为已明确限定的允许义项对；同义身份、不同实体、无约束、方向关系分开。方向关系不传递为同一身份，实际关系必须由有资格知识或可信语义上下文提供；抽象义项0/1/2及关系a=b+1只是可复算有限夹具。候选生成、真实主体/时间/权限、词义全集均未完成。有限图上反复删去在相邻变量无支持的值，保留任何完整合法赋值（归纳：合法赋值各对始终互为支持）。局部一致性是必要条件；三节点两值两两不同是反例。再选最小非单例域逐个分支、传播，完整枚举叶，收集精确支持和完整赋值数量。若无叶且搜索完整，则对给定域与关系返回CONFLICT；任何域覆盖/关系资格缺失则UNKNOWN；超预算LIMIT且清空部分结果。仅在已核实穷尽的域中候选唯一，仍无确认或写入权限，authority始终NONE。实际概率、用户意图与真实语言理解不得由组合数推断。时间最坏指数，访问预算1000为研究者选定，未测设备性能。独立枚举参照使用显式真值表，与候选算法分离但同一研究者设定；非独立科学验收。

## 实验
三节点，每个节点7个非空候选子集，三条边各4种关系，共7^3*4^3=21952个合成图；比较局部传播、完整联合解与错误将方向关系等同身份。局部假可行计数表示局部未报冲突而联合无解，不是现实误判率；额外义项只统计实际有完整解的图；局部多义而完整唯一仅为夹具上的可能澄清收益，未测真人追问。错误关系对照不是原生平台或普通AI。14项专项控制。所有材料为ChatGPT研发辅助的项目原创合成夹具，非真人、训练、独立留出。真实原文候选覆盖、知识准入、上下文来源和独立质量仍未知。无训练、生产修改、Codex、CI、PR合并、部署、费用及冻结变更。

## 复算代码
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)};
 // Three abstract senses. A relation is an explicit set of allowed ordered pairs.
 // eq: identity; ne: distinct; any: no restriction; forward: typed directional relation, not identity.
 const rel=[(a,b)=>a===b,(a,b)=>a!==b,()=>true,(a,b)=>a===b+1];
 const arcs=[[0,1],[1,2],[0,2]],bits=m=>[0,1,2].filter(i=>m&(1<<i));
 function propagate(dom,edges){
  let d=dom.slice(),changed=true;
  while(changed){changed=false;for(const [i,j,t] of edges){
   let x=bits(d[i]).filter(a=>bits(d[j]).some(b=>rel[t](a,b))).reduce((m,a)=>m|(1<<a),0);
   let y=bits(d[j]).filter(b=>bits(d[i]).some(a=>rel[t](a,b))).reduce((m,b)=>m|(1<<b),0);
   if(x!==d[i]||y!==d[j])changed=true;d[i]=x;d[j]=y;
   if(!x||!y)return null;
  }}return d;
 }
 function solve(dom,edges,cap=1000){
  let visits=0,solutions=0,support=dom.map(()=>0),limited=false;
  function rec(d){
   if(limited)return;
   if(++visits>cap){limited=true;return}
   d=propagate(d,edges);if(!d||d.some(x=>!x))return;
   let i=d.reduce((best,m,j)=>bits(m).length>1&&(best<0||bits(m).length<bits(d[best]).length)?j:best,-1);
   if(i<0){solutions++;d.forEach((v,j)=>support[j]|=v);return}
   for(let x of bits(d[i])){let n=d.slice();n[i]=1<<x;rec(n)}
  }
  rec(dom);
  return limited?{status:"LIMIT",support:null,solutions:null,authority:"NONE"}:{status:solutions?"CANDIDATES":"CONFLICT",support,solutions,authority:"NONE",visits};
 }
 // Independent enumerator: explicit truth table, no call to rel or propagation.
 const tables=[0b100010001,0b011101110,0b111111111,0b010001000];
 function oracle(dom,types){
  let count=0,s=[0,0,0];
  for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++){
   let q=[a,b,c];if(q.some((v,i)=>!(dom[i]&(1<<v))))continue;
   if(!arcs.every(([i,j],k)=>tables[types[k]]&(1<<(3*q[i]+q[j]))))continue;
   count++;q.forEach((v,i)=>s[i]|=1<<v);
  }return {count,s};
 }
 let r={cases:0,feasible:0,conflict:0,exact:0,localFalseFeasible:0,localExtraSenseCases:0,localExtraSenseValues:0,localAmbiguousButExactUnique:0,exactUnique:0,orientationFalseFeasible:0,orientationFalseConflict:0,orientationChangedSupport:0,orientationChangedSolutionCount:0,maxVisits:0,controls:0,examples:{}};
 for(let a=1;a<=7;a++)for(let b=1;b<=7;b++)for(let c=1;c<=7;c++)for(let i=0;i<4;i++)for(let j=0;j<4;j++)for(let k=0;k<4;k++){
  let dom=[a,b,c],types=[i,j,k],edges=arcs.map(([u,v],n)=>[u,v,types[n]]),ac=propagate(dom,edges),z=solve(dom,edges),o=oracle(dom,types);
  ck(z.solutions===o.count&&z.support.every((x,n)=>x===o.s[n]),"oracle mismatch");
  r.cases++;r.exact++;r[z.solutions?"feasible":"conflict"]++;r.maxVisits=Math.max(r.maxVisits,z.visits);
  if(ac&&!o.count)r.localFalseFeasible++;
  if(o.count){ck(ac&&ac.every((x,n)=>(x&o.s[n])===o.s[n]),"propagation removed valid sense");
   let extra=ac.reduce((v,x,n)=>v+bits(x&~o.s[n]).length,0);if(extra){r.localExtraSenseCases++;r.localExtraSenseValues+=extra}
   if(o.count===1){r.exactUnique++;if(ac.some(x=>bits(x).length>1))r.localAmbiguousButExactUnique++}
  }
  // Incorrectly treating the directional relation as equality.
  let flat=solve(dom,edges.map(([u,v,t])=>[u,v,t===3?0:t]));
  if(flat.solutions&&!o.count)r.orientationFalseFeasible++;
  if(!flat.solutions&&o.count)r.orientationFalseConflict++;
  if(flat.solutions&&o.count&&flat.support.some((x,n)=>x!==o.s[n]))r.orientationChangedSupport++;
  if(flat.solutions!==o.count)r.orientationChangedSolutionCount++;
 }
 const odd=[[0,1,1],[1,2,1],[0,2,1]],direction=[[0,1,3],[1,2,2],[0,2,2]];
 r.examples.odd={local:propagate([3,3,3],odd),exact:solve([3,3,3],odd)};
 r.examples.direction={exact:solve([2,1,1],direction),flattened:solve([2,1,1],direction.map(([i,j,t])=>[i,j,t===3?0:t]))};
 // Model contract: exhaustive domain and qualified constraints are external obligations.
 function qualify(dom,edges,coverage,qualified,cap=1000){
  if(!coverage||!qualified)return {status:"UNKNOWN",authority:"NONE",support:null};
  return solve(dom,edges,cap);
 }
 for(const test of [()=>r.cases===21952,()=>r.exact===r.cases,()=>r.feasible+r.conflict===r.cases,()=>r.examples.odd.local.every(x=>x===3),()=>r.examples.odd.exact.status==="CONFLICT",()=>r.examples.direction.exact.solutions===1,()=>r.examples.direction.flattened.status==="CONFLICT",()=>solve([7,7,7],[],1).status==="LIMIT",()=>solve([7,7,7],[],1).support===null,()=>qualify([1,1,1],[],false,true).status==="UNKNOWN",()=>qualify([1,1,1],[],true,false).status==="UNKNOWN",()=>qualify([1,1,1],[],true,true).authority==="NONE",()=>solve([7,7,7],[]).solutions===27,()=>solve([7,7,7],[]).support.every(x=>x===7)]){ck(test(),"control");r.controls++}
 return r;
}
```

## 实测结果
```json
{
  "cases": 21952,
  "feasible": 10019,
  "conflict": 11933,
  "exact": 21952,
  "localFalseFeasible": 85,
  "localExtraSenseCases": 63,
  "localExtraSenseValues": 120,
  "localAmbiguousButExactUnique": 24,
  "exactUnique": 5688,
  "orientationFalseFeasible": 3240,
  "orientationFalseConflict": 1699,
  "orientationChangedSupport": 2329,
  "orientationChangedSolutionCount": 5819,
  "maxVisits": 40,
  "controls": 14,
  "examples": {
    "odd": {
      "local": [
        3,
        3,
        3
      ],
      "exact": {
        "status": "CONFLICT",
        "support": [
          0,
          0,
          0
        ],
        "solutions": 0,
        "authority": "NONE",
        "visits": 3
      }
    },
    "direction": {
      "exact": {
        "status": "CANDIDATES",
        "support": [
          2,
          1,
          1
        ],
        "solutions": 1,
        "authority": "NONE",
        "visits": 1
      },
      "flattened": {
        "status": "CONFLICT",
        "support": [
          0,
          0,
          0
        ],
        "solutions": 0,
        "authority": "NONE",
        "visits": 1
      }
    }
  }
}
```

## 下一责任
手动窗口将研究原始文本候选与概念义项及关系证据的接口；需要能够保留未知义项、来源与冲突，不能以扩充固定同义词表宣称开放语义。数据轨合法真实语料，独立轨保管未见评价，产品轨唯一交接；未获授权不启动训练或完整工程开发。保持R50完整范围和既有正式验收门。
