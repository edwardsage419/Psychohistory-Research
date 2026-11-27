# 自主认知：匿名群体基数、部分成员身份与重叠资源边界
2026-11-27。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / RAW_CUE_DIAGNOSTIC / CONNECTOR_JS_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线和去重
起点及写前main 0ecc78ed7043be4b1c0e55e328f30c0a3dffbfac。核对20近期提交、15开放PR、v3.2全文、同步规程全文、唯一产品交接前20行、decision_hub相关目录。#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。直接前序 implicit-group-antecedent-retrieval-and-member-coverage.md blob 5732471ee5a9ef63ebaf1886a09984adfe8eb470；相关 actor-scoped-resource-flow-and-common-plan.md bd75b981b35e3c63cbc5550b8ea690ddea2ed80f、cross-decision-obligation-union.md 19fa2b270056d448bd93b587049198d284c5eecf、reservation-identity-residual-capacity-bounds.md 33950948ea63a2f1d0874fff905043df9265973a 前22行。已有已知义务身份并集、容量流、来源区间及匿名对象检索；本轮只新增给定群体基数及部分交叠约束的成员不确定资源区间，以及上游数量提及候选诊断，不重复声明旧数学模型、完整语言解析或算法首创。非全库查重。

## A 有限群体表示与边界
研究合同：同一时间、同一计量单位、同一合法资源口径，2或3个已资格化群体；可信夹具提供成员总数上界N、各群体人数区间及两两交叠人数区间、最多N个不同的抽象位置。位置仅是组合数学槽，不生成真实成员身份；已知互异成员可限定其允许的群体归属掩码，匿名槽允许全部掩码；0表示该槽未被任何群体使用。没有独立确认上界、同一人是否可共享同份资源、同一时段或需求必然同时适用时，不可直接使用此合同或默认独立/重叠。允许掩码的覆盖必须由可信宿主确认；不推测用户授权、真实成员或源身份。模型不处理成员各自异质需求、部分共享、具体排班、资源时序、不可分割或跨资源约束。

若群体A,B人数a,b，总人数不超过N，交叠人数o有合格界[l0,h0]，精确可行范围 l=max(0,a+b-N,l0)，h=min(a,b,h0)。对任意整数o在[l,h]内，四类槽数o,a-o,b-o,N-a-b+o非负，均有构造；l>h则有限合同矛盾。每成员需求wA,wB非负且同一份资源可满足重叠需求时，成本 a*wA+b*wB-o*min(wA,wB)，极值在h,l；必须独立消耗时成本a*wA+b*wB，与身份重叠无关。若两群需求可能而不必同时出现，则需要显式联合情景；本模型计算的是已给定同时适用合同下的资源需求，不是需求发生概率、实际消费或全局计划可行性。

三群即使各人数2、每对交叠1，三重交叠仍可能0或1，总人数3或4（总上界4），不能仅按两两交叠得到唯一并集。一般算法按槽依次处理：状态v为k个群体计数及k(k-1)/2个成对交叠计数；允许掩码m对应增量f(m)，群体计数增量为成员位，交叠增量为两位同时为1。对每个v保存可达成本最小/最大及两个见证路径。因未来允许掩码及资源增量只依赖当前位置和v，具有相同v的前缀仅需保留各端点，归纳得到精确极值。超出上限或即使剩余全计入仍不足下限时剪枝，完整终态满足区间。非负整数，两个模式分别取成员所属群体需求最大值或和。求解空域CONFLICT_FINITE，覆盖未知UNKNOWN_COVERAGE，未资格化UNQUALIFIED，节点尝试超过cap返回UNKNOWN_BUDGET，不输出部分极值冒充确定边界。输入上限32槽、需求每群不超过1000000以限制整数；实际实验仅N<=5，默认100000尝试。最坏状态数(N+1)^(k+k(k-1)/2)，每步最多2^k转移，附带见证复制及计数处理；预算只计尝试转移，不是墙时、内存或安全资源保证。未实现真正匿名统计保护、鉴权、证据收据、成员版本与持久化。所有结果auth NONE。给定资源C，C>=上界可证明此限定资源合同的全部完成可满足，C<下界证明全部不足，其余保留条件性；不得把局部资源判断转为整体建议或动作授权。

## B 实测
标准JS连接器实际执行。双群：N=0..5，a,b=0..N，需求[1,1]/[1,3]/[3,1]，交叠约束无额外限制/明确不重叠/明确最大重叠，819配置（一些约束重复）；每例同时与闭式公式、独立逐槽枚举集合参照及端点见证核对。三群：每批240结构，每结构两种成本模式，共480配置。初批LCG取模存在低位相关及分布偏差，故补做相同seed高位缩放批次，未重复双群计数；不能称独立随机样本，仍有可能重复结构，非概率抽样。两批生成允许掩码、部分身份及交叠区间均为人工合成；部分身份结构数、成本模式差异和区间收紧按结构而非配置计数。所有主要配置与直接参照一致，可行每例两端点见证检查通过。参照和候选由同一研究者实现，非独立科研验收。对每配置cap=0/5/40测试，未完成不返回极值，完成与无额外截断一致。专项12种控制，两次运行重复，不算24种。

| 批次 | 模型配置 | 可行 | 矛盾 | 非点区间 |
| --- | ---: | ---: | ---: | ---: |
| 双群 | 819 | 714 | 105 | 90 |
| 三群取模 | 480 | 478 | 2 | 456 |
| 三群高位补充 | 480 | 476 | 4 | 388 |

双群4914个资源阈值检查中，机械按完全不重叠计算产生525项确定错误拒绝（真实上界仍可满足）；机械按最大重叠计算产生72项确定错误放行（真实下界已超过资源）。不计仅落入不确定区间的错误确定性，非产品真实错误率。三群两批每批240结构内共享与加和模式不同分别190、222；使用成对交叠比仅用群体人数区间收紧共享成本界分别26、92。全5337次预算控制中4325截断、1012完成。取模批次主要结果已先执行一次，第二次复算检查关键计数一致。完整计数见后文。worlds为带数学槽标签的可行赋值数，重复匿名排列且两模式重复，不等于独立世界样本或现实概率。

## C 原文数量候选与成员身份
固定公开合成资产（连接器实际完整读取，报告blob，不冒称独立Git字节重算）：
research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb
research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132
全部32情节64轮。仅扫描有限中文整数+量词提及，Unicode标量锚定，保留前后文及原文坐标。24个提及、15轮、16个数值大于1，均明确标记身份未决。人工审查16个复数提及：L04.1七个实际工作日为时间量；L06.0八次、L17.0三次任务/两个准时/三次做校准为事件与子集；S04.1两个为插座数量修订。这6项不应直接建造人员/决策对象组。其余10项含两家老人、两个地方、两项费用、两个目标、两个岗位、两套房、两个人、两个指标、两种方式等，仍需区分指代对象、候选集、度量集合、真正群体及历史来源。扫描不解析“十来天”、省略数量、非计数量词、一般多词数字、群体身份、指代和来源，也不证明数字量词一定正确。没有人工全集标注，不能报告召回率、精度或语言能力改善。人工分类是在看到数据后进行的，未用于拟合或提高已见分数。
L05“两个地方临时都可能需要七天”：如果两处同时需求且同一10天资源不能重叠使用，需求14天、缺4天；若不具同时发生证据，仅能展示条件结果，不构造概率或自动合并照顾任务。L12两个项目分别最低6万、共同上限10万，已资格同时适用时缺2万，无需进一步收集成员个人身份。S04两个人都得能用厨房，不等同两人同时使用厨房；仅人数不足以计算插座需求。上述是原有情节的人工条件性解释，未跑原生入口；不重复计为新模型复算证据。下一阶段优先保留群体提及的原文锚、基数候选、已知/匿名成员状态、交叠信息来源、同时性/共享资格，接真实候选发现而非扩大词表；仅在合法资格后进入数学端口。无明确成员时可以出无身份依赖的有限界，但不能以匿名数学槽修改个人长期记录。

## D 完整可执行复算
标准JS，输入两个固定JSON解析数组；数学函数无需外部数据。执行 experiment()、experiment(true,false)、diagnostic(docs)。下列为本轮第二次实际执行的函数。
```js
function experiment(high=false,runTwo=true){
 const ok=(v,m)=>{if(!v)throw Error(m)};
 const rng=(()=>{let s=20261127;return n=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return high?Math.floor(s*n/4294967296):s%n}})();
 const masks=k=>Array.from({length:1<<k},(_,i)=>i);
 const features=(k,m)=>{const x=Array.from({length:k},(_,j)=>Number(!!(m&(1<<j))));for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)x.push(x[i]*x[j]);return x};
 function cost(m,w,mode){let a=w.filter((_,i)=>m&(1<<i));return mode==="shared"?Math.max(0,...a):a.reduce((s,x)=>s+x,0)}
 function solve(k,slots,bounds,w,mode,{covered=true,qualified=true,cap=100000}={}){
  const auth="NONE",int=x=>Number.isSafeInteger(x)&&x>=0;
  if(![2,3].includes(k)||!Array.isArray(slots)||slots.length>32||!Array.isArray(bounds)||bounds.length!==k+k*(k-1)/2||!Array.isArray(w)||w.length!==k||!w.every(x=>int(x)&&x<=1000000)||!["shared","additive"].includes(mode)||!int(cap)||!slots.every(s=>Array.isArray(s)&&s.length>0&&s.every(m=>int(m)&&m<(1<<k))&&new Set(s).size===s.length)||!bounds.every(b=>Array.isArray(b)&&b.length===2&&b.every(int)&&b[0]<=b[1]&&b[1]<=slots.length))return {status:"INVALID",auth};
  if(!qualified)return {status:"UNQUALIFIED",auth};
  if(!covered)return {status:"UNKNOWN_COVERAGE",auth};
  let dp=new Map([["0,".repeat(bounds.length-1)+"0",{v:bounds.map(()=>0),lo:0,hi:0,wl:[],wh:[]}]]);
  let work=0;
  for(let t=0;t<slots.length;t++){
   const next=new Map();
   for(const s of dp.values())for(const m of slots[t]){
    if(work>=cap)return {status:"UNKNOWN_BUDGET",auth,work}; work++;
    const f=features(k,m),v=s.v.map((x,i)=>x+f[i]);
    if(v.some((x,i)=>x>bounds[i][1]||x+slots.length-t-1<bounds[i][0]))continue;
    const c=cost(m,w,mode),key=v.join(","),lo=s.lo+c,hi=s.hi+c,old=next.get(key);
    if(!old)next.set(key,{v,lo,hi,wl:[...s.wl,m],wh:[...s.wh,m]});
    else{if(lo<old.lo){old.lo=lo;old.wl=[...s.wl,m]}if(hi>old.hi){old.hi=hi;old.wh=[...s.wh,m]}}
   }
   dp=next;
  }
  const finals=[...dp.values()].filter(s=>s.v.every((x,i)=>x>=bounds[i][0]&&x<=bounds[i][1]));
  if(!finals.length)return {status:"CONFLICT_FINITE",auth,work};
  const l=finals.reduce((a,b)=>a.lo<=b.lo?a:b),h=finals.reduce((a,b)=>a.hi>=b.hi?a:b);
  return {status:"BOUNDED_FINITE",auth,lo:l.lo,hi:h.hi,wl:l.wl,wh:h.wh,work};
 }
 function oracle(k,slots,bounds,w,mode){
  let lo=Infinity,hi=-Infinity,n=0,assign=[];
  function rec(i){
   if(i<slots.length){for(const m of slots[i]){assign.push(m);rec(i+1);assign.pop()}return}
   const sets=Array.from({length:k},(_,j)=>new Set(assign.map((m,i)=>m&(1<<j)?i:-1).filter(i=>i>=0)));
   const counts=sets.map(s=>s.size);for(let a=0;a<k;a++)for(let b=a+1;b<k;b++)counts.push([...sets[a]].filter(i=>sets[b].has(i)).length);
   if(!counts.every((x,j)=>x>=bounds[j][0]&&x<=bounds[j][1]))return;
   let c=0;for(let i=0;i<slots.length;i++){const vals=sets.map((s,j)=>s.has(i)?w[j]:0);c+=mode==="shared"?Math.max(...vals):vals.reduce((s,x)=>s+x,0)}
   lo=Math.min(lo,c);hi=Math.max(hi,c);n++;
  }rec(0);return n?{lo,hi,n}:null;
 }
 function witness(k,slots,bounds,w,mode,row,target){
  if(row.length!==slots.length||row.some((m,i)=>!slots[i].includes(m)))return false;
  const f=bounds.map((_,i)=>row.reduce((s,m)=>s+features(k,m)[i],0));
  return f.every((x,i)=>x>=bounds[i][0]&&x<=bounds[i][1])&&row.reduce((s,m)=>s+cost(m,w,mode),0)===target;
 }
 const out={two:{cases:0,solved:0,conflicts:0,formulaChecks:0,worlds:0,work:0,nonpoint:0,naiveDisjointFalseFail:0,naiveFullOverlapFalsePass:0,naiveBoth:0,thresholds:0},three:{cases:0,solved:0,conflicts:0,worlds:0,work:0,nonpoint:0,sharedAdditiveDiffer:0,partialIdentityCases:0,overlapTightens:0},budget:{cases:0,cut:0,complete:0},controls:0,examples:{}};
 function test(k,s,b,w,mode,kind){
  const p=solve(k,s,b,w,mode),q=oracle(k,s,b,w,mode),o=out[kind];o.cases++;o.work+=p.work??0;
  ok(p.auth==="NONE","authority");if(q){o.solved++;o.worlds+=q.n;ok(p.status==="BOUNDED_FINITE"&&p.lo===q.lo&&p.hi===q.hi,"oracle");ok(witness(k,s,b,w,mode,p.wl,p.lo)&&witness(k,s,b,w,mode,p.wh,p.hi),"witness");o.nonpoint+=Number(p.lo!==p.hi)}else{o.conflicts++;ok(p.status==="CONFLICT_FINITE","conflict")}
  for(const cap of [0,5,40]){out.budget.cases++;const z=solve(k,s,b,w,mode,{cap});if(z.status==="UNKNOWN_BUDGET"){out.budget.cut++;ok(z.lo===undefined&&z.hi===undefined,"cut leak")}else{out.budget.complete++;ok(z.status===p.status&&z.lo===p.lo&&z.hi===p.hi,"budget exact")}}
  return p;
 }
 if(runTwo)for(let n=0;n<=5;n++)for(let a=0;a<=n;a++)for(let b=0;b<=n;b++)for(const w of [[1,1],[1,3],[3,1]])for(const overlap of [[0,n],[0,0],[Math.min(a,b),Math.min(a,b)]]){
  const s=Array.from({length:n},()=>masks(2)),bounds=[[a,a],[b,b],overlap],p=test(2,s,bounds,w,"shared","two");
  const l=Math.max(0,a+b-n,overlap[0]),h=Math.min(a,b,overlap[1]),base=a*w[0]+b*w[1],d=Math.min(...w);
  ok(l>h?p.status==="CONFLICT_FINITE":p.lo===base-h*d&&p.hi===base-l*d,"closed form");out.two.formulaChecks++;
  if(l<=h)for(let cap=0;cap<=base;cap++){
   out.two.thresholds++;
   const wrongFail=base>cap&&p.hi<=cap,wrongPass=base-Math.min(a,b)*d<=cap&&p.lo>cap;
   out.two.naiveDisjointFalseFail+=Number(wrongFail);out.two.naiveFullOverlapFalsePass+=Number(wrongPass);out.two.naiveBoth+=Number(wrongFail&&wrongPass);
  }
 }
 for(let t=0;t<240;t++){
  const k=3,n=2+rng(4),s=Array.from({length:n},(_,i)=>{
   if(i>=2||rng(3)===0)return masks(k);
   const j=rng(k),v=rng(2);return masks(k).filter(m=>Number(!!(m&(1<<j)))===v);
  });
  const sample=s.map(a=>a[rng(a.length)]),tot=features(k,0).map((_,i)=>sample.reduce((v,m)=>v+features(k,m)[i],0));
  const b=tot.map((x,i)=>{if(t%4===0&&i===0){const a=rng(n+1),z=rng(n+1);return [Math.min(a,z),Math.max(a,z)]}return [Math.max(0,x-rng(2)),Math.min(n,x+rng(2))]});
  const w=[1+rng(4),1+rng(4),1+rng(4)];
  const a=test(k,s,b,w,"shared","three"),d=test(k,s,b,w,"additive","three");
  if(s.some(x=>x.length<8))out.three.partialIdentityCases++;
  if(a.status==="BOUNDED_FINITE"){
   ok(d.status==="BOUNDED_FINITE"&&a.lo<=d.lo&&a.hi<=d.hi,"shared order");
   out.three.sharedAdditiveDiffer+=Number(a.lo!==d.lo||a.hi!==d.hi);
   const relaxed=b.map((x,i)=>i<3?x:[0,n]),z=solve(k,s,relaxed,w,"shared");
   ok(z.lo<=a.lo&&z.hi>=a.hi,"relax");
   out.three.overlapTightens+=Number(z.lo!==a.lo||z.hi!==a.hi);
  }else ok(d.status===a.status,"cost invariant feasibility");
 }
 const c=(v,m)=>{ok(v,m);out.controls++};
 let slots=Array.from({length:3},()=>masks(2)),b=[[2,2],[2,2],[0,3]];
 let p=solve(2,slots,b,[4,7],"shared"),a=solve(2,slots,b,[4,7],"additive");
 c(p.lo===14&&p.hi===18,"overlap ex");c(a.lo===22&&a.hi===22,"distinct obligation");
 c(solve(2,slots,b,[4,7],"shared",{covered:false}).status==="UNKNOWN_COVERAGE","coverage");
 c(solve(2,slots,b,[4,7],"shared",{qualified:false}).status==="UNQUALIFIED","qualification");
 c(solve(2,slots,b,[4,7],"shared",{cap:0}).status==="UNKNOWN_BUDGET","budget");
 c(solve(2,slots,[[2,2],[2,2],[0,0]],[4,7],"shared").status==="CONFLICT_FINITE","disjoint impossible");
 c(solve(2,[[4]],[[0,1],[0,1],[0,1]],[4,7],"shared").status==="INVALID","mask");
 c(solve(2,[[0,0]],[[0,1],[0,1],[0,1]],[4,7],"shared").status==="INVALID","duplicate mask");
 c(solve(2,slots,b,[4,7],"unknown").status==="INVALID","cost mode");
 c(solve(2,slots,b,[4,-1],"shared").status==="INVALID","negative");
 const trip=solve(3,Array.from({length:4},()=>masks(3)),Array.from({length:6},(_,i)=>i<3?[2,2]:[1,1]),[1,1,1],"shared");
 c(trip.lo===3&&trip.hi===4,"triple unresolved");
 const single=solve(2,[],[[0,0],[0,0],[0,0]],[1,1],"shared");
 c(single.lo===0&&single.hi===0,"empty population");
 out.examples={twoShared:[p.lo,p.hi],twoAdditive:[a.lo,a.hi],tripleUnion:[trip.lo,trip.hi]};return out;
}

function diagnostic(docs){
 const counts={"一":1,"二":2,"两":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10};
 const rows=[];let turns=0,hitTurns=0;
 for(const e of docs.flatMap(x=>x.cases))for(const [i,t] of e.turns.entries()){
  turns++;
  const hits=[...t.text.matchAll(/[一二两三四五六七八九十]+[个家项套种位名次]/gu)];
  hitTurns+=Number(hits.length>0);
  for(const m of hits){
   const q=Array.from(m[0]),n=q.slice(0,-1).join(""),start=Array.from(t.text.slice(0,m.index)).length,end=start+q.length;
   if(Array.from(t.text).slice(start,end).join("")!==m[0])throw Error("anchor");
   rows.push({id:e.id+"."+i,span:m[0],start,end,count:counts[n]??null,classifier:q[q.length-1],suffix:Array.from(t.text).slice(end,end+10).join(""),prefix:Array.from(t.text).slice(Math.max(0,start-5),start).join(""),identity:"UNRESOLVED",authority:"NONE"});
  }
 }
 return {turns,hitTurns,hits:rows.length,pluralHits:rows.filter(x=>x.count>1).length,rows};
}
```

```json
{
  "main": {
    "two": {
      "cases": 819,
      "solved": 714,
      "conflicts": 105,
      "formulaChecks": 819,
      "worlds": 7182,
      "work": 30888,
      "nonpoint": 90,
      "naiveDisjointFalseFail": 525,
      "naiveFullOverlapFalsePass": 72,
      "naiveBoth": 0,
      "thresholds": 4914
    },
    "three": {
      "cases": 480,
      "solved": 478,
      "conflicts": 2,
      "worlds": 55900,
      "work": 108144,
      "nonpoint": 456,
      "sharedAdditiveDiffer": 190,
      "partialIdentityCases": 208,
      "overlapTightens": 26
    },
    "budget": {
      "cases": 3897,
      "cut": 2997,
      "complete": 900
    },
    "controls": 12,
    "examples": {
      "twoShared": [
        14,
        18
      ],
      "twoAdditive": [
        22,
        22
      ],
      "tripleUnion": [
        3,
        4
      ]
    }
  },
  "extra": {
    "two": {
      "cases": 0,
      "solved": 0,
      "conflicts": 0,
      "formulaChecks": 0,
      "worlds": 0,
      "work": 0,
      "nonpoint": 0,
      "naiveDisjointFalseFail": 0,
      "naiveFullOverlapFalsePass": 0,
      "naiveBoth": 0,
      "thresholds": 0
    },
    "three": {
      "cases": 480,
      "solved": 476,
      "conflicts": 4,
      "worlds": 68514,
      "work": 162552,
      "nonpoint": 388,
      "sharedAdditiveDiffer": 222,
      "partialIdentityCases": 221,
      "overlapTightens": 92
    },
    "budget": {
      "cases": 1440,
      "cut": 1328,
      "complete": 112
    },
    "controls": 12,
    "examples": {
      "twoShared": [
        14,
        18
      ],
      "twoAdditive": [
        22,
        22
      ],
      "tripleUnion": [
        3,
        4
      ]
    }
  },
  "raw": {
    "turns": 64,
    "hitTurns": 15,
    "hits": 24,
    "pluralHits": 16,
    "rows": [
      {
        "id": "L02.1",
        "span": "一次",
        "start": 5,
        "end": 7,
        "count": 1,
        "classifier": "次",
        "suffix": "也不行，我说的是一次",
        "prefix": "A一年最多",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L02.1",
        "span": "一次",
        "start": 15,
        "end": 17,
        "count": 1,
        "classifier": "次",
        "suffix": "都不能有。",
        "prefix": "，我说的是",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L04.1",
        "span": "七个",
        "start": 2,
        "end": 4,
        "count": 7,
        "classifier": "个",
        "suffix": "实际工作日，延期会失",
        "prefix": "还剩",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L05.0",
        "span": "两家",
        "start": 0,
        "end": 2,
        "count": 2,
        "classifier": "家",
        "suffix": "老人要照顾，这个月我",
        "prefix": "",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L05.1",
        "span": "两个",
        "start": 12,
        "end": 14,
        "count": 2,
        "classifier": "个",
        "suffix": "地方临时都可能需要七",
        "prefix": "就不能调，",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L06.0",
        "span": "八次",
        "start": 8,
        "end": 10,
        "count": 8,
        "classifier": "次",
        "suffix": "都没坏，应该百分百没",
        "prefix": "手店我买过",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L12.0",
        "span": "两项",
        "start": 18,
        "end": 20,
        "count": 2,
        "classifier": "项",
        "suffix": "加起来只能十万，不能",
        "prefix": "得留六万。",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L12.1",
        "span": "两个",
        "start": 2,
        "end": 4,
        "count": 2,
        "classifier": "个",
        "suffix": "都必须至少六万，不能",
        "prefix": "对，",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L15.0",
        "span": "两个",
        "start": 2,
        "end": 4,
        "count": 2,
        "classifier": "个",
        "suffix": "目标，一个是拿证，一",
        "prefix": "我有",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L15.0",
        "span": "一个",
        "start": 7,
        "end": 9,
        "count": 1,
        "classifier": "个",
        "suffix": "是拿证，一个是学会实",
        "prefix": "两个目标，",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L15.0",
        "span": "一个",
        "start": 13,
        "end": 15,
        "count": 1,
        "classifier": "个",
        "suffix": "是学会实际操作。四周",
        "prefix": "个是拿证，",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L17.0",
        "span": "三次",
        "start": 3,
        "end": 5,
        "count": 3,
        "classifier": "次",
        "suffix": "任务两个准时，一个延",
        "prefix": "上个月",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L17.0",
        "span": "两个",
        "start": 7,
        "end": 9,
        "count": 2,
        "classifier": "个",
        "suffix": "准时，一个延期。我觉",
        "prefix": "月三次任务",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L17.0",
        "span": "一个",
        "start": 12,
        "end": 14,
        "count": 1,
        "classifier": "个",
        "suffix": "延期。我觉得我有八成",
        "prefix": "两个准时，",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "L17.0",
        "span": "三次",
        "start": 35,
        "end": 37,
        "count": 3,
        "classifier": "次",
        "suffix": "做校准吗？",
        "prefix": "，能直接拿",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S01.0",
        "span": "两个",
        "start": 2,
        "end": 4,
        "count": 2,
        "classifier": "个",
        "suffix": "岗位中选一个，留在维",
        "prefix": "想在",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S01.0",
        "span": "一个",
        "start": 8,
        "end": 10,
        "count": 1,
        "classifier": "个",
        "suffix": "，留在维修部或者转去",
        "prefix": "个岗位中选",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S02.0",
        "span": "两套",
        "start": 7,
        "end": 9,
        "count": 2,
        "classifier": "套",
        "suffix": "房。任何一套都必须离",
        "prefix": "东边和西边",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S02.0",
        "span": "一套",
        "start": 13,
        "end": 15,
        "count": 1,
        "classifier": "套",
        "suffix": "都必须离车站步行十五",
        "prefix": "套房。任何",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S04.0",
        "span": "两个",
        "start": 2,
        "end": 4,
        "count": 2,
        "classifier": "个",
        "suffix": "人都得能用厨房。想买",
        "prefix": "我们",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S04.0",
        "span": "一个",
        "start": 28,
        "end": 30,
        "count": 1,
        "classifier": "个",
        "suffix": "空插座。",
        "prefix": "，家里只有",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S04.1",
        "span": "两个",
        "start": 8,
        "end": 10,
        "count": 2,
        "classifier": "个",
        "suffix": "，之前那个数字不准。",
        "prefix": "量刚核实是",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S07.0",
        "span": "两个",
        "start": 13,
        "end": 15,
        "count": 2,
        "classifier": "个",
        "suffix": "指标，暂时没有选定贷",
        "prefix": "应急储蓄这",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      },
      {
        "id": "S14.1",
        "span": "两种",
        "start": 14,
        "end": 16,
        "count": 2,
        "classifier": "种",
        "suffix": "方式都先留着。",
        "prefix": "楚，所以这",
        "identity": "UNRESOLVED",
        "authority": "NONE"
      }
    ]
  }
}
```

## E 限制与治理
研究者自行选定2/3群、有限成员槽、成本模型、随机生成、基线、扫描词表；未授权为产品规范。数学覆盖不能代替真实语义覆盖。未执行完整v0.8入口、实际用户、独立留出、普通AI对照、Mac/iPhone性能、持续隐私控制、训练、生产代码修改、PR合并、部署或主动CI；无新增费用。冻结协议、历史证据等级、唯一交接保持原样。
