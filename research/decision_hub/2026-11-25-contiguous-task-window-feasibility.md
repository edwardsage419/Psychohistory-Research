# 自主认知专项累计第120轮候选：连续任务与分散时段的精确可行性
2026-11-25。RESEARCH_CANDIDATE / REUSED_RESEARCH_CODE_EXECUTED / EXACT_BOUNDED_MIXED_SCHEDULING / SYNTHETIC_FIXTURE / NATIVE_NOT_RUN / INDEPENDENT_ACCEPTANCE_NOT_RUN。固定main c58fb6fb43989c611e17a36caeaaf80b6c7fd51e。核对近期12提交、13开放PR（#61待审）、v3.2前15行及历史全文、同步规程前20行、唯一交接前18行、R119前20行及实际代码、学习调度README前18行、R96前16行。R119完整可拆分工时、R96二维连续线性域、R12固定考试间隔不同；本轮新增实际小时位置与不可拆分任务，直接复用R119日期资格、任务投影和EDF对照。不修改其正确适用范围或历史结果。
## 固定资产
research/decision_hub/2026-11-25-anchored-deadline-shared-time-feasibility.md e5a2b2921d9c810b82a1e449200b17caf987cf7d
research/decision_hub/2026-11-25-civil-temporal-anchor-version-replay.md cc9f6c6103e4ac863d2cdaa6961721149fd4189a
research/decision_hub/2026-11-25-temporal-quantity-candidate-separation.md 8a6b42f83b80283db6e215fe48f4fb2efbf8368c
research/decision_hub/2026-11-25-raw-field-candidate-coverage-and-numerals.md 07dcbda9532dbc3b330abfd79a399cb52aa91aeb
R96 5d130171355088ee7a86fd646f4e095db97a785d；学习调度README 72d7ae55999a34e1dabbfeab116dfcf199254ce1；唯一交接 5e74f4f0b37141d631740e844ad8bbbfed232e07。无新外部数据或真实用户信息。
## 合同与数学
沿R119四个合成民用日期、每日0..2整数小时，A/B必需工作各1..3小时，C可拆工作0或2小时。本轮每日本地抽象3个有顺序的单位时段，不是实际钟表或时区；容量为2时比较相邻(0,1)和分散(0,2)，容量1固定(0)，0空。A/B必须同日相邻连续完成，C可拆成单位工时；不允许跨日连续、并发、切换费用、行程、技能/现金、依赖、任务取消或期限代价。不可拆分标记、工时、可用时段与覆盖由可信合成宿主给定，非自动语义或真实授权。R119 project实际核验R118日期收据、根、版本、来源、范围；新增布尔块类型及容量位图一致性门，未知返回UNKNOWN_INPUT。没有实际持久化、授权、日历、原生C028或CAS。所有authority NONE。
每项任务的合法占用集合：可拆任务枚举其窗口内可用位的所有固定基数子集；连续任务枚举同一日所有相邻块并检查包含于可用位。零工时为空集合。按候选数排序，递归选择各任务一个与已占位不交叠的合法集合；以(任务索引,已占位)记忆已完全证伪状态，不改变可行性，因为未来只依赖该状态。归纳得到完整有限域判定，返回可行排程或无解；无解由穷尽搜索和独立参照核验，本轮未构造一般简短不可行证书。独立参照枚举每个实际可用时段为空闲或分配某任务，检查窗口、工时及终端连续性，不调用placement或memo。对每个成功解直接验占用、连续、容量和时间窗。预算10000只计递归调用，超限返回LIMIT且无排程；候选生成、循环、校验和真实时间内存未纳入同一预算，固定域最多12位，不能视为生产资源保护。真实多任务扩展可能指数增长。未知不可拆分状态不得擅自采用宽松结果。
R119 EDF作为完全可拆的放宽模型，可拆不可行必然严格不可行（删连续限制得到超集）；若EDF可行而严格不可行，不能当真实计划可行。计数为本合成域中的错误使用风险，不称R119自身缺陷。分散时段与相邻时段同容量，但本特定布局下分散严格可行可映射为相邻可行（连续块任务只能用1时段或其他日，C可拆）；不推广到具有额外绝对时刻条件的计划。A延长期限仅扩展其窗口，不增加资源或计算延期成本，旧解仍可行。
## 实验
12容量模式×3 A工时×3 B工时×2 B期限×2 A释放日×2 C工时×2 A版本×2布局=3456有限计算；同研究者双路径，非独立验收或真实决策。每个A新版本检查旧收据及撤回来源；15专项控制。记录实际递归计数而非设备性能；证书、比较、失败及具体见证保留。研究者选择全部时间网格、任务类型、比较和预算，非产品最终政策。未执行训练、Codex、CI、原生系统、真机、PR合并、部署、费用或冻结变更。
## 复算
按上述四文件顺序置入docs[i].content，Node标准JS。仅加载已审查的项目自有源码。
```js
function load(docs){
 const c=docs[0].content.split("```js\n")[1].split("\n```")[0];
 const T=Function(c.split("function experiment(T)")[0]+"\nreturn load;")()(docs.slice(1));
 return Function("T",c.slice(c.indexOf("function experiment(T)")).split(" let out={pairedScenarios:")[0]+"\nreturn {dates,sources,anchors,ra,ra2,rb,rb2,rc,record,project,edf,caps};\n}\nreturn experiment(T);")(T);
}
function experiment(P){
 const ck=(v,m)=>{if(!v)throw Error(m)},sum=a=>a.reduce((s,x)=>s+x,0),pop=m=>{let n=0;for(;m;m&=m-1)n++;return n};
 // 4 days, 3 ordered hour positions per day. A two-hour daily capacity
 // is either contiguous (0,1) or fragmented (0,2).
 function calendar(cap,fragmented){
  let mask=0;for(let d=0;d<4;d++)for(let h of (cap[d]===2?(fragmented?[0,2]:[0,1]):cap[d]===1?[0]:[]))mask|=1<<(3*d+h);
  return mask
 }
 function eligible(j,available){let m=0;for(let d=j.r;d<=j.d;d++)m|=7<<(3*d);return m&available}
 function placements(j,available){
  if(j.h===0)return [0];
  let domain=eligible(j,available),out=[];
  if(j.block){
   for(let d=j.r;d<=j.d;d++)for(let h=0;h+j.h<=3;h++){
    let m=((1<<j.h)-1)<<(3*d+h);if((domain&m)===m)out.push(m);
   }
  }else for(let m=domain;m;m=(m-1)&domain)if(pop(m)===j.h)out.push(m);
  return out
 }
 function solve(jobs,available,cap=10000){
  if(!Number.isInteger(cap)||cap<0)return {status:"UNKNOWN_INPUT",authority:"NONE"};
  let domains=jobs.map(j=>({id:j.id,masks:placements(j,available)})).sort((a,b)=>a.masks.length-b.masks.length||a.id.localeCompare(b.id));
  let memo=new Set(),steps=0,limited=false;
  function go(i,used){
   if(steps>=cap){limited=true;return null}steps++;
   if(i===domains.length)return {};
   let key=i+":"+used;if(memo.has(key))return null;
   for(let m of domains[i].masks)if(!(m&used)){
    let r=go(i+1,used|m);if(limited)return null;if(r!==null)return {...r,[domains[i].id]:m}
   }memo.add(key);return null
  }
  const found=go(0,0);
  return {status:limited?"LIMIT":found?"FEASIBLE":"INFEASIBLE",...(found&&!limited?{schedule:found}:{}),steps,authority:"NONE"}
 }
 // Independently enumerate assignments of actual slots to tasks or idle.
 // Check contiguity only at terminal; never use placement domains.
 function oracle(jobs,available){
  let slots=[];for(let i=0;i<12;i++)if(available&(1<<i))slots.push(i);
  let assigned=jobs.map(()=>[]);
  function terminal(){
   return jobs.every((j,i)=>{
    let x=assigned[i];if(x.length!==j.h)return false;
    return !j.block||!x.length||Math.floor(x[0]/3)===Math.floor(x.at(-1)/3)&&x.at(-1)-x[0]+1===x.length
   })
  }
  function go(k){
   if(jobs.every((j,i)=>assigned[i].length===j.h))return terminal();
   if(k===slots.length||jobs.reduce((n,j,i)=>n+j.h-assigned[i].length,0)>slots.length-k)return false;
   let s=slots[k],day=Math.floor(s/3);
   if(go(k+1))return true;
   for(let i=0;i<jobs.length;i++)if(assigned[i].length<jobs[i].h&&jobs[i].r<=day&&day<=jobs[i].d){
    assigned[i].push(s);let yes=go(k+1);assigned[i].pop();if(yes)return true
   }return false
  }return go(0)
 }
 function validate(z,jobs,available){
  if(z.status!=="FEASIBLE")return false;
  let used=0;for(let j of jobs){let m=z.schedule[j.id];if(!Number.isInteger(m)||m<0||(m&~available)||(m&used)||pop(m)!==j.h||(m&~eligible(j,available)))return false;
   if(j.block&&m){let xs=[];for(let i=0;i<12;i++)if(m&(1<<i))xs.push(i);if(Math.floor(xs[0]/3)!==Math.floor(xs.at(-1)/3)||xs.at(-1)-xs[0]+1!==xs.length)return false}used|=m
  }return true
 }
 function run(req,available,cap=10000,ss=P.sources,aa=P.anchors){
  let j=P.project(req,ss,aa);
  if(!j||!req.blockModes||req.blockModes.length!==j.length||req.blockModes.some(x=>typeof x!=="boolean")||!Number.isInteger(available)||available<0||available>=4096||req.capacity.some((n,d)=>n!==pop((available>>(3*d))&7)))return {status:"UNKNOWN_INPUT",authority:"NONE"};
  return solve(j.map((x,i)=>({...x,block:req.blockModes[i]})),available,cap)
 }
 let out={pairs:0,checks:0,feasible:0,infeasible:0,certificates:0,edfFeasible:0,edfFalseFeasible:0,edfFalseInfeasible:0,layoutLosses:0,layoutGains:0,extensionRescued:0,extensionLost:0,staleRejected:0,revokedUnknown:0,searchSteps:0,maxSteps:0,controls:0,witness:null,deadlineWitness:null};
 for(let cap of P.caps)for(let ha of [1,2,3])for(let hb of [1,2,3])for(let b of [P.rb,P.rb2])for(let ar of [0,1])for(let hc of [0,2]){
  let status=[];
  for(let a of [P.ra,P.ra2]){
   let req={covered:true,capacity:cap,records:[P.record(a,ha,ar),P.record(b,hb,1),P.record(P.rc,hc,2)],blockModes:[true,true,false]};
   let plain=P.project(req,P.sources,P.anchors);ck(plain,"qualified");let jobs=plain.map((x,i)=>({...x,block:req.blockModes[i]})),relaxed=P.edf(plain,cap).status==="FEASIBLE",pair=[];
   for(let frag of [false,true]){
    let avail=calendar(cap,frag),z=run(req,avail);let expected=oracle(jobs,avail);
    ck(z.status!=="LIMIT"&&z.status!=="UNKNOWN_INPUT"&&(z.status==="FEASIBLE")===expected,"oracle");
    out.checks++;out.searchSteps+=z.steps;out.maxSteps=Math.max(out.maxSteps,z.steps);
    out.edfFeasible+=+relaxed;out.edfFalseFeasible+=+(relaxed&&!expected);out.edfFalseInfeasible+=+(!relaxed&&expected);
    out.feasible+=+expected;out.infeasible+=+!expected;
    if(expected){ck(validate(z,jobs,avail),"schedule");out.certificates++}
    pair.push(expected);
   }
   out.pairs++;
   if(pair[0]&&!pair[1]){out.layoutLosses++;out.witness??={capacity:cap,jobs,contiguousMask:calendar(cap,false),fragmentedMask:calendar(cap,true),contiguousSchedule:run(req,calendar(cap,false)).schedule}}
   out.layoutGains+=+(!pair[0]&&pair[1]);status.push(pair);
   if(a===P.ra2){let stale={...req,records:[{...req.records[0],receipt:P.ra.receipt},...req.records.slice(1)]};ck(run(stale,calendar(cap,false)).status==="UNKNOWN_INPUT","stale");out.staleRejected++;
    ck(run(req,calendar(cap,false),10000,{...P.sources,a2:{...P.sources.a2,allowed:false}}).status==="UNKNOWN_INPUT","withdraw");out.revokedUnknown++}
  }
  for(let i=0;i<2;i++){if(!status[0][i]&&status[1][i]){out.extensionRescued++;out.deadlineWitness??={cap,ha,hb,hc,ar,layout:i===0?"contiguous":"fragmented",bDeadline:b.receipt.value.date}}out.extensionLost+=+(status[0][i]&&!status[1][i])}
 }
 const baseReq={covered:true,capacity:[2,2,2,2],records:[P.record(P.ra,2,0),P.record(P.rb,1,1)],blockModes:[true,true]};
 const avail=calendar(baseReq.capacity,false);
 for(let t of [()=>out.checks===3456,()=>out.feasible+out.infeasible===out.checks,()=>out.certificates===out.feasible,()=>out.edfFalseInfeasible===0,()=>out.extensionLost===0,()=>out.layoutGains===0,()=>out.layoutLosses>0,()=>run(baseReq,avail,0).status==="LIMIT",()=>!Object.hasOwn(run(baseReq,avail,0),"schedule"),()=>run({...baseReq,blockModes:[true,null]},avail).status==="UNKNOWN_INPUT",()=>run({...baseReq,covered:false},avail).status==="UNKNOWN_INPUT",()=>run(baseReq,0).status==="UNKNOWN_INPUT",()=>run(baseReq,avail,10000,P.sources,{a:{...P.anchors.a,allowed:false}}).status==="UNKNOWN_INPUT",()=>solve([{id:"X",r:0,d:0,h:2,block:true}],5).status==="INFEASIBLE",()=>solve([{id:"X",r:0,d:0,h:2,block:false}],5).status==="FEASIBLE"]){ck(t(),"control "+out.controls);out.controls++}
 return out
}
console.log(JSON.stringify(experiment(load(docs)),null,2));
```
## 实测
```json
{
  "pairs": 1728,
  "checks": 3456,
  "feasible": 294,
  "infeasible": 3162,
  "certificates": 294,
  "edfFeasible": 570,
  "edfFalseFeasible": 276,
  "edfFalseInfeasible": 0,
  "layoutLosses": 94,
  "layoutGains": 0,
  "extensionRescued": 20,
  "extensionLost": 0,
  "staleRejected": 864,
  "revokedUnknown": 864,
  "searchSteps": 4649,
  "maxSteps": 10,
  "controls": 15,
  "witness": {
    "capacity": [
      2,
      0,
      2,
      0
    ],
    "jobs": [
      {
        "id": "A",
        "r": 0,
        "d": 2,
        "h": 1,
        "block": true
      },
      {
        "id": "B",
        "r": 1,
        "d": 3,
        "h": 2,
        "block": true
      },
      {
        "id": "C",
        "r": 2,
        "d": 3,
        "h": 0,
        "block": false
      }
    ],
    "contiguousMask": 195,
    "fragmentedMask": 325,
    "contiguousSchedule": {
      "A": 1,
      "C": 0,
      "B": 192
    }
  },
  "deadlineWitness": {
    "cap": [
      0,
      2,
      0,
      2
    ],
    "ha": 1,
    "hb": 2,
    "hc": 0,
    "ar": 0,
    "layout": "contiguous",
    "bDeadline": "2026-11-24"
  }
}
```
下一责任：研究真实工作量不确定性、多资源约束及可解释的计划修改成本；自主识别事件、连续性和期限仍需要真实数据和独立验收。产品轨维护唯一交接，正式版本另获授权。
