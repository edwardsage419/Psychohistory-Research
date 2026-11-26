# 自主学习：选择反馈冲突的最小证据集合与偏好变化假说
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与范围
同一手动轮第二阶段，起点main bc4d4f6e9b4c3678c0b0d73f55475fdd442adc24，沿用本轮核对的v3.2、同步规程、25近期提交、15开放PR、固定历史交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。实际复用 research/decision_hub/2026-11-26-partial-lexicographic-goal-order-witnesses.md blob 56ccc94a47a135670b670e26e65c99503740e7e5 及 research/decision_hub/2026-11-26-choice-context-preference-identification-and-retraction.md blob 8f5190df8333d19b909ad1690774beb20b580317 的closure/winner/solve/allOrders。已有选择识别、序贯退化监测、反馈撤回及偏好版本管理，不重复宣称。本轮新增同一明确偏好合同中选择模型不相容时的最小冲突记录、最小暂隔离集合及单变化点解释集合。不是偏好变化检测的统计证据或全库查重证明。
## 合同与算法
五条已资格、菜单完整且理由已确认的时间有序合成选择记录，六二元目标、用户明确接受词典序且同一上下文；固定无环显式优先边始终保留，不作为可自动删除记录。每条记录限制可相容的优先顺序集合；联合相容 iff 交集非空。增加记录不能使空交集恢复，故枚举子集时若已含最小冲突核可安全跳过。按整数掩码递增，所有真子集先访问，发现不可相容即为最小冲突核；逆序保留不含核的极大相容集合，其补集为全部最小暂隔离集合。它们仅显示需要核查的记录组合，不是应删除、虚假或异常用户的结论。对每个相邻记录间切点分别核对两段在同一显式边下各自相容，允许两段不同的顺序；这只说明单次偏好变化假说在该模型下可能解释数据，无法证明真实变点，也可能源自语义误读、未建模理由、信息变化或不适用的偏好模型。若单变化点不相容，不自动增加变化次数或移除显式约束；返回冲突待核。不同上下文、未知菜单或资格不足不能直接使用本合同。所有输出authority NONE，不自动写偏好或删除反馈。
## 实验
900合成图，每图5次选择，随机生成两个人工排序、菜单、显式边及部分有意不一致选择；直接枚举全部允许排序，得到每个顺序满足的记录掩码并取全部子集作为参照，与前轮贪心求解驱动的冲突核、隔离集合、单切点候选全量核对。5专项控制包括相反选择、两个相容解释、交替、稳定及显式边不可删除。标准JS核心实际执行两次一致。有限五记录域、指数枚举，不作设备性能或真实变化概率声明。研究者选定合同、规模、生成分布与错误对照；前轮学习用途授权及撤回边界继续独立。未执行原生、独立留出、真人、训练、生产、交接、冻结、证据等级变更、PR、部署、主动CI或费用。
```json
{
  "graphs": 900,
  "conflicting": 546,
  "consistent": 354,
  "coreCount": 835,
  "repairCount": 1242,
  "multipleRepairs": 251,
  "oneChangeCompatible": 160,
  "noSingleChange": 386,
  "multipleChangePoints": 126,
  "checks": 28800,
  "greedyCalls": 22770,
  "oracleOrders": 251626,
  "arbitraryDropMayWrong": 439,
  "controls": 5,
  "example": {
    "edges": [],
    "rows": [
      {
        "known": [
          34,
          24,
          7
        ],
        "potential": [
          34,
          24,
          7
        ],
        "chosen": 24
      },
      {
        "known": [
          3,
          52
        ],
        "potential": [
          3,
          52
        ],
        "chosen": 52
      },
      {
        "known": [
          58,
          42,
          9
        ],
        "potential": [
          58,
          42,
          9
        ],
        "chosen": 58
      },
      {
        "known": [
          5,
          25,
          33
        ],
        "potential": [
          5,
          25,
          33
        ],
        "chosen": 25
      },
      {
        "known": [
          34,
          15,
          25
        ],
        "potential": [
          34,
          15,
          25
        ],
        "chosen": 34
      }
    ],
    "cores": [
      [
        0,
        4
      ],
      [
        1,
        3,
        4
      ]
    ],
    "repairs": [
      [
        0,
        1
      ],
      [
        0,
        3
      ],
      [
        4
      ]
    ],
    "cuts": [
      2,
      3,
      4
    ]
  }
}
```
## 复算
固定两份报告按上列顺序读取；只执行审阅的自有研究代码，Node包装未执行。
```js
const code=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0]);
const make=Function(code[0].split(" const out={graphs:")[0]+"\nreturn {closure,orderOK,winner};\n}\nreturn experiment();");
const make2=Function("make",code[1].slice(code[1].indexOf("function study(make){")).split(" const host={subject:")[0]+"\nreturn {solve,allOrders,clauses};\n}\nreturn study(make);");
function experiment(make,make2){
 const R=make(),S=make2(make),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),N=6,E=5,ALL=31;
 const ids=m=>Array.from({length:E},(_,i)=>i).filter(i=>m&(1<<i)),sub=(a,b)=>(a&b)===a;
 let seed=20261126;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function analyze(edges,rows){
  const cache=new Map();let calls=0;
  const test=m=>{if(!cache.has(m)){calls++;cache.set(m,S.solve(edges,ids(m).map(i=>rows[i]),"POSSIBLE").status==="COMPATIBLE")}return cache.get(m)};
  const cores=[],maxCons=[];
  for(let m=0;m<=ALL;m++){
   if(cores.some(c=>sub(c,m)))continue;
   if(!test(m))cores.push(m);
  }
  // Ascending integer order visits all strict subsets before supersets.
  for(let m=ALL;m>=0;m--){
   if(maxCons.some(c=>sub(m,c)))continue;
   if(cores.every(c=>!sub(c,m)))maxCons.push(m);
  }
  const repairs=maxCons.map(m=>ALL^m).sort((a,b)=>a-b);
  let cuts=[];
  for(let k=1;k<E;k++){let left=(1<<k)-1,right=ALL^left;if(test(left)&&test(right))cuts.push(k)}
  return {cores,repairs,cuts,calls,stationary:test(ALL)};
 }
 const out={graphs:0,conflicting:0,consistent:0,coreCount:0,repairCount:0,multipleRepairs:0,oneChangeCompatible:0,noSingleChange:0,multipleChangePoints:0,checks:0,greedyCalls:0,oracleOrders:0,arbitraryDropMayWrong:0,controls:0,example:null};
 for(let g=0;g<900;g++){
  let h=[0,1,2,3,4,5];for(let i=N-1;i>0;i--){let j=rnd(i+1);[h[i],h[j]]=[h[j],h[i]]}
  let h2=h.slice();for(let i=N-1;i>0;i--){let j=rnd(i+1);[h2[i],h2[j]]=[h2[j],h2[i]]}
  let edges=[];for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(rnd(8)===0)edges.push([h[i],h[j]]);
  const os=S.allOrders(R.closure(edges)),rows=[];
  for(let t=0;t<E;t++){
   let menu=[...new Set(Array.from({length:2+rnd(4)},()=>rnd(64)))];let c=R.winner(t<2?h:h2,menu);if(rnd(5)===0)c=menu[rnd(menu.length)];
   rows.push({known:menu,potential:menu,chosen:c});
  }
  const z=analyze(edges,rows),possible=Array(32).fill(false);
  // Enumerate orders once, then their satisfied episode masks, directly derive
  // feasible subsets by inclusion. Does not invoke greedy solver.
  for(let o of os){let m=0;for(let i=0;i<E;i++)if(R.winner(o,rows[i].known)===rows[i].chosen)m|=1<<i;
   for(let k=0;k<=ALL;k++)if(sub(k,m))possible[k]=true;
  }
  const cores=Array.from({length:32},(_,m)=>m).filter(m=>!possible[m]&&ids(m).every(i=>possible[m^(1<<i)]));
  const repairs=Array.from({length:32},(_,m)=>m).filter(m=>possible[ALL^m]&&ids(m).every(i=>!possible[ALL^(m^(1<<i))]));
  const cuts=Array.from({length:E-1},(_,i)=>i+1).filter(k=>possible[(1<<k)-1]&&possible[ALL^((1<<k)-1)]);
  ck(eq(z.cores,cores)&&eq(z.repairs,repairs)&&eq(z.cuts,cuts)&&z.stationary===possible[ALL],"oracle parity");
  for(let m=0;m<=ALL;m++){ck(possible[m]===z.cores.every(c=>!sub(c,m)),"core coverage");out.checks++}
  out.oracleOrders+=os.length;out.greedyCalls+=z.calls;out.coreCount+=cores.length;out.repairCount+=repairs.length;
  if(z.stationary)out.consistent++;else{
   out.conflicting++;out.multipleRepairs+=+(repairs.length>1);out.oneChangeCompatible+=+(cuts.length>0);out.noSingleChange+=+(cuts.length===0);out.multipleChangePoints+=+(cuts.length>1);
   if(!possible[ALL^1])out.arbitraryDropMayWrong++;
   if(repairs.length>1&&cuts.length>1)out.example??={edges,rows,cores:cores.map(ids),repairs:repairs.map(ids),cuts};
  }
  out.graphs++;
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const A={known:[1,2],potential:[1,2],chosen:1},B={...A,chosen:2};
 let z=analyze([],[A,A,B,B,B]);ctl(!z.stationary&&eq(z.cuts,[2]),"one split");
 ctl(eq(z.repairs,[3,28]),"retain both hypotheses");
 ctl(analyze([],[A,B,A,B,A]).cuts.length===0,"multiple changes or mismatch");
 ctl(analyze([],[A,A,A,A,A]).stationary,"stationary");
 ctl(analyze([[0,1]],[B,A,A,A,A]).cores.includes(1),"confirmed edge not removed");
 return out;
}
console.log(JSON.stringify(experiment(make,make2),null,2));
```
