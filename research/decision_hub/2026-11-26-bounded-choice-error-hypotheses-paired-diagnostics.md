# 自主学习：有限选择误差容错假说与配对覆盖诊断
2026-11-26。RESEARCH_CANDIDATE / PREDECESSOR_CODE_EXECUTED / SYNTHETIC_PREQUENTIAL_EXECUTED / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。
## 基线与范围
同一手动轮第四阶段，起点main 977d89533bb9a921fc9af12c013ac4adb9894e4d；沿用本轮核对v3.2、同步规程、25近期提交、15开放PR、固定交接及#63固定head 734686980b19da9291bdd08b67d4e2519c011acf。实际读取并执行：
research/decision_hub/2026-11-26-partial-lexicographic-goal-order-witnesses.md 56ccc94a47a135670b670e26e65c99503740e7e5
research/decision_hub/2026-11-26-choice-context-preference-identification-and-retraction.md 8f5190df8333d19b909ad1690774beb20b580317
research/decision_hub/2026-11-26-frozen-prequential-choice-set-diagnostics.md 4381f3448d010dd30af332ddabf9f7c862dfa036
上一阶段事前诊断已发现全部历史和最近两条规则在含更正/变化的合成样本中产生覆盖退步，本轮是后见开发扩展，不能当独立留出。新增固定误差容许数的联合假说、严格包含关系及配对缺失反馈诊断；不重做R18权重或冻结Brier证据，局部查重有限。
## 数学合同
明确词典序、六个二元目标、同上下文及已确认显式边。当前epoch合格记录由前序真实recordsAsOf筛选，选择记录只为诊断假说，不改动显式偏好、硬约束或用户长期价值。允许至多k条既往选择与排序不相容：保留所有满足显式边且历史违反数不超过k的顺序。等价于从历史中假设隔离至多k条后，所有相容顺序的并集；证明每个满足违反数界的顺序可删其违反记录，反之任一隔离子集的相容顺序最多违反被隔离数。这里只是模型解释容差，不表示某条记录错误，不删除事实，不自动推断偏好变化。k固定为0、1、2，未拟合或训练；真实误差预算不明时不得默认该值，可能所有假说仍失效。输出下一菜单各保留顺序的可能胜者集合，空集弃答。随k增加集合嵌套于不使用选择历史的显式边基线，因此在相同标签上绝不能比该基线拥有更高的覆盖率。缩小集合可能减少认知负担，但必须同时检验实际覆盖退步、弃答和用户体验；不能仅以更窄宣称改善。
配对未覆盖改善为同一标签Y的基线未覆盖减候选未覆盖。缺失标签取同一完整菜单所有可能值的差最小/最大，跨记录在独立标签补全下求和为尖锐界，相关时仅外界。相同集合即使标签未知差仍0；严格子集必定每标签差<=0。保持集合大小与覆盖独立，未赋任何用户效用权重，未构造人生总分或实际升级门。固定预测先于观察记录，反馈严格获知截点及epoch，撤回不回退。真实授权、来源、签名、删除、持久化、观测真值及实际偏好模型适用性均未实现。全部authority NONE。
## 实际执行
四类合成环境各220组、每组7期：干净静态、选择噪声、隐性变化、显式epoch；干净组即时记录（严格下一期才获知）且无缺失，其他组随机反馈延迟/缺失/撤回。生成分布和新种子为研究者选定，开发诊断非独立测试；没有根据结果优化k。预先固定每组前40个情节对所有三种k实际枚举删除子集并核对顺序集合大小及预测集合，全部情节核对嵌套、严格规则及配对差上界，另6专项控制。标准JS核心实际两次运行一致。比较同一组同标签的未覆盖、集合大小、弃答、容错对严格规则覆盖及增加候选数、相对基线缺失配对界。数值是有限合成重复结构，非真实用户效果、未来风险、显著性或模型升降级证据。
```json
{
  "graphs": 880,
  "events": 6160,
  "referenceChecks": 3360,
  "pairedBoundChecks": 24640,
  "groups": {
    "clean": {
      "baseline": {
        "size": 3633,
        "abstain": 0,
        "observed": 1540,
        "misses": 0,
        "pairedLow": 0,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 788
      },
      "strict": {
        "size": 2845,
        "abstain": 0,
        "observed": 1540,
        "misses": 0,
        "pairedLow": 0,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 0
      },
      "tolerate1": {
        "size": 3382,
        "abstain": 0,
        "observed": 1540,
        "misses": 0,
        "pairedLow": 0,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 537
      },
      "tolerate2": {
        "size": 3565,
        "abstain": 0,
        "observed": 1540,
        "misses": 0,
        "pairedLow": 0,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 720
      }
    },
    "noisy": {
      "baseline": {
        "size": 3564,
        "abstain": 0,
        "observed": 1051,
        "misses": 116,
        "pairedLow": 0,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 177,
        "extraSizeVsStrict": 971
      },
      "strict": {
        "size": 2593,
        "abstain": 280,
        "observed": 1051,
        "misses": 293,
        "pairedLow": -353,
        "pairedHigh": -189,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 0
      },
      "tolerate1": {
        "size": 3351,
        "abstain": 25,
        "observed": 1051,
        "misses": 146,
        "pairedLow": -84,
        "pairedHigh": -34,
        "extraCoverageVsStrict": 147,
        "extraSizeVsStrict": 758
      },
      "tolerate2": {
        "size": 3525,
        "abstain": 3,
        "observed": 1051,
        "misses": 117,
        "pairedLow": -15,
        "pairedHigh": -2,
        "extraCoverageVsStrict": 176,
        "extraSizeVsStrict": 932
      }
    },
    "hiddenChange": {
      "baseline": {
        "size": 3599,
        "abstain": 0,
        "observed": 1083,
        "misses": 0,
        "pairedLow": 0,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 87,
        "extraSizeVsStrict": 554
      },
      "strict": {
        "size": 3045,
        "abstain": 52,
        "observed": 1083,
        "misses": 87,
        "pairedLow": -204,
        "pairedHigh": -87,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 0
      },
      "tolerate1": {
        "size": 3488,
        "abstain": 3,
        "observed": 1083,
        "misses": 11,
        "pairedLow": -38,
        "pairedHigh": -11,
        "extraCoverageVsStrict": 76,
        "extraSizeVsStrict": 443
      },
      "tolerate2": {
        "size": 3586,
        "abstain": 0,
        "observed": 1083,
        "misses": 0,
        "pairedLow": -6,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 87,
        "extraSizeVsStrict": 541
      }
    },
    "explicitEpoch": {
      "baseline": {
        "size": 3625,
        "abstain": 0,
        "observed": 1091,
        "misses": 0,
        "pairedLow": 0,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 160
      },
      "strict": {
        "size": 3465,
        "abstain": 0,
        "observed": 1091,
        "misses": 0,
        "pairedLow": -34,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 0
      },
      "tolerate1": {
        "size": 3608,
        "abstain": 0,
        "observed": 1091,
        "misses": 0,
        "pairedLow": -6,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 143
      },
      "tolerate2": {
        "size": 3624,
        "abstain": 0,
        "observed": 1091,
        "misses": 0,
        "pairedLow": -1,
        "pairedHigh": 0,
        "extraCoverageVsStrict": 0,
        "extraSizeVsStrict": 159
      }
    }
  },
  "controls": 6
}
```
## 接入结论
在没有明确偏好模型及误差容许资格之前，不应用历史过滤替代明确偏好。即使假说获准用于只读提示，也应保留未过滤基线与预测覆盖/候选规模的分别验证，并隔离强制硬约束、选择解释与真实结果质量；不以合成测试自动选k或上线。未修改生产、唯一交接、冻结、证据等级、PR、训练、部署、主动CI或费用，原生、独立留出、真机和真实用户验证未运行。
## 复算
固定三份报告按顺序输入；只执行审查过的项目自有源码，Node包装未执行，连接器核心实际运行。
```js
const code=process.argv.slice(2).map(p=>require("node:fs").readFileSync(p,"utf8").split("\`\`\`js\n")[1].split("\n\`\`\`")[0]);
const make=Function(code[0].split(" const out={graphs:")[0]+"\nreturn {closure,orderOK,winner};\n}\nreturn experiment();");
const make2=Function("make",code[1].slice(code[1].indexOf("function study(make){")).split(" const host={subject:")[0]+"\nreturn {solve,allOrders,clauses};\n}\nreturn study(make);");
const make3=Function("make","make2",code[2].slice(code[2].indexOf("function experiment(make,make2){")).split(" const groups=[")[0]+"\nreturn {recordsAsOf,predict,reference};\n}\nreturn experiment(make,make2);");
function experiment(make,make2,make3){
 const R=make(),S=make2(make),P=make3(make,make2),ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 let seed=20261207;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const sorted=a=>[...a].sort((x,y)=>x-y),N=6,T=7;
 function tolerated(os,menu,prior,k){
  const keep=os.filter(o=>prior.reduce((n,r)=>n+ +(R.winner(o,r.menu)!==r.choice),0)<=k);
  return {set:sorted([...new Set(keep.map(o=>R.winner(o,menu)))]),count:keep.length,dependencies:prior.map(r=>[r.id,r.version]),authority:"NONE"};
 }
 // Independent deletion-subset oracle: union all orders consistent after at most k
 // omitted records; no omission is actually written or attributed to a particular user error.
 function oracle(os,menu,prior,k){
  const union=new Set();
  for(let m=0;m<1<<prior.length;m++){
   let removed=prior.filter((_,i)=>m&(1<<i)).length;if(removed>k)continue;
   for(let o of os)if(prior.every((r,i)=>m&(1<<i)||R.winner(o,r.menu)===r.choice))union.add(o);
  }
  return {set:sorted([...new Set([...union].map(o=>R.winner(o,menu)))]),count:union.size};
 }
 function paired(a,b,menu,y){
  // Improvement in miss count: baseline miss minus candidate miss. Positive is better.
  const vals=(y===null?menu:[y]).map(c=> +( !a.includes(c))- +( !b.includes(c)));
  return [Math.min(...vals),Math.max(...vals)];
 }
 const names=["clean","noisy","hiddenChange","explicitEpoch"],ks=[0,1,2],out={graphs:0,events:0,referenceChecks:0,pairedBoundChecks:0,groups:{},controls:0};
 const stats=()=>({size:0,abstain:0,observed:0,misses:0,pairedLow:0,pairedHigh:0,extraCoverageVsStrict:0,extraSizeVsStrict:0});
 for(let group of names){
  let o=out.groups[group]={baseline:stats(),strict:stats(),tolerate1:stats(),tolerate2:stats()};
  for(let g=0;g<220;g++){
   let hidden=[0,1,2,3,4,5];for(let i=N-1;i>0;i--){let j=rnd(i+1);[hidden[i],hidden[j]]=[hidden[j],hidden[i]]}
   let edges=[];for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)if(rnd(9)===0)edges.push([hidden[i],hidden[j]]);
   const os=S.allOrders(R.closure(edges)),h2=os[rnd(os.length)],log=[],events=[];
   for(let t=0;t<T;t++){
    const epoch=group==="explicitEpoch"&&t>=3?2:1,menu=sorted([...new Set(Array.from({length:3+rnd(4)},()=>rnd(64)))]);
    const prior=P.recordsAsOf(log,t,epoch),base=P.predict(os,menu,prior,"baseline").set;
    const preds=ks.map(k=>tolerated(os,menu,prior,k));
    ck(eq(preds[0].set,P.predict(os,menu,prior,"allHistory").set),"strict parity");
    for(let k of ks){
     // Cross-check all cases except larger deletion enumeration: deterministic
     // predeclared g<40 cohort, all times and k, both candidate and oracle.
     if(g<40){let z=oracle(os,menu,prior,k);ck(z.count===preds[k].count&&eq(z.set,preds[k].set),"deletion union oracle");out.referenceChecks++}
     ck(preds[k].set.every(c=>base.includes(c))&&(!k||preds[k-1].set.every(c=>preds[k].set.includes(c))),"nested");
    }
    const h=(group==="hiddenChange"||group==="explicitEpoch")&&t>=3?h2:hidden;
    let choice=R.winner(h,menu);if(group==="noisy"&&rnd(4)===0)choice=menu[rnd(menu.length)];
    events.push({t,menu,choice,sets:[base,...preds.map(x=>x.set)]});
    // A clean control has no missing/correction; other regimes have delayed and
    // sometimes withdrawn observations; the noisy regime has choice violations.
    if(group==="clean"||rnd(5)!==0){
     const r={id:t,version:1,received:t+(group==="clean"?0:rnd(3)),epoch,menu,choice,allowed:true,qualified:true};log.push(r);
     if(group!=="clean"&&rnd(9)===0)log.push({...r,version:2,received:r.received+1,allowed:false});
    }
   }
   for(let e of events){
    const latest=log.filter(r=>r.id===e.t&&r.received<10).sort((a,b)=>b.version-a.version)[0];
    const y=latest?.allowed?latest.choice:null;
    for(let [i,name] of ["baseline","strict","tolerate1","tolerate2"].entries()){
     let s=o[name],set=e.sets[i],b=e.sets[0],strict=e.sets[1];
     s.size+=set.length;s.abstain+=+(set.length===0);s.extraSizeVsStrict+=set.length-strict.length;
     if(y!==null){s.observed++;s.misses+=+!set.includes(y);s.extraCoverageVsStrict+=+(set.includes(y)&&!strict.includes(y));}
     let [lo,hi]=paired(b,set,e.menu,y);s.pairedLow+=lo;s.pairedHigh+=hi;
     ck(lo<=hi&&hi<=0,"subset cannot improve coverage vs baseline");out.pairedBoundChecks++;
    }
    out.events++;
   }
   out.graphs++;
  }
 }
 const ctl=(v,m)=>{ck(v,m);out.controls++};
 const os=S.allOrders(R.closure([])),r={id:0,version:1,menu:[1,2],choice:1};
 ctl(eq(tolerated(os,[1,2],[r],0).set,[1]),"strict");
 ctl(eq(tolerated(os,[1,2],[r],1).set,[1,2]),"one omitted constraint");
 ctl(tolerated(os,[1,2],[r,{...r,id:1,choice:2}],0).count===0,"conflict");
 ctl(tolerated(os,[1,2],[r,{...r,id:1,choice:2}],1).count===720,"tolerance recovers both");
 ctl(eq(paired([1,2],[1],[1,2],null),[-1,0]),"paired missing bound");
 ctl(eq(paired([1],[1],[1,2],null),[0,0]),"same prediction cancels");
 return out;
}
console.log(JSON.stringify(experiment(make,make2,make3),null,2));
```
