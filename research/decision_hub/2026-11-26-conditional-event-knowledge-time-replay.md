# 自主认知：条件事实的发生时点、获知版本与历史决策重放
2026-11-26。RESEARCH_CANDIDATE / SYNTHETIC_EXECUTED / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。
## 基线与去重
固定main 504e60eb7629eaf9167911f8b9d08f5ac4878b37，核对22近期提交、15开放Draft PR、v3.2、同步规程、唯一产品交接前20行（blob 5e74f4f0b37141d631740e844ad8bbbfed232e07）。#63固定head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft，未重跑。读取前轮raw-revision-to-confirmed-history-joint-ranking.md 6e17e892bc7bcc512efed8e28b8f29bee05c5877、v08-conditional-permission-direction-and-revision.md 529750962f2686179703de19e37d5e037fd75d0d、joint-guarded-policy-applicability.md 5fed5e9108fbc97257fbf0546d521aa3cf725769、interpretation-effect-equivalence-and-ledger-boundary.md 18ae7920f9ca317da66d1d50ba7f0fc3d8951c26，以及civil-temporal-anchor-version-replay.md cc9f6c6103e4ac863d2cdaa6961721149fd4189a、selective-replanning-dependency-invalidation.md ffac85bbee74bcd78cb7e34ab91d65d260753a91、discourse-reference-revision-identity.md da54c5b88ed0f19f5c5d272230a1959b811f5b5e前段。已有条件方向、版本修订、时间锚、现金双时间及分层失效；本轮专门验证同一谓词的两个不同发生身份、按获知时间重放、事实撤回墓碑及条件出口依赖。未实现或重复真实SQLite、语言解析、权限系统、事件身份识别；局部查重非全库证明。
## 形式合同
两事件身份t=0/1为已由可信夹具确定的不同发生实例；获知时间k为离散追加序列，允许后来得知早先事件的真/假或撤回。对固定t及截至k的证据，取该t最后一条合格记录；若最新记录撤回(null)或缺失，则事实未知，不能回退旧证据。政策在获知序列中更新，当前条件真时上限为1或2，假时上限为3；数值仅合成同单位整数，非真实政策或人生分数。未知时用两个可能上限分别计算x<=cap，均通过为PASS，均失败为FAIL，其余UNKNOWN。权限夹具撤回时输出NO_PERMISSION，重新授予后仅在人工设定的原证据仍可用模型中继续；真实删除、授权范围、新许可不能自动恢复旧数据等不在此夹具内，生产必须另核。权限变更不意味着事实为假。当前政策变化只影响当前分析，历史按当时已知政策及证据重放；此处没有政策独立生效时点、复杂持续时间及真实交易，不能称完整双时态数据库。
对于每个只读端口，缓存键为事件身份、查询量、政策版本、权限代次、当前该事件证据版本(无记录用0)。假定版本单调、内部可信状态、固定算法和身份，键相同意味着全部依赖相同，复用安全；同值更正、撤回后再取得相同值均更新版本；另一事件变化不必使本端口失效。全局权限与政策变化保守失效。真实系统还需来源、适用性、模型版本、用途、有效期和可信签名/事务。无实际操作，authority NONE。实际已执行行动作为独立不可变观察夹具，不因条件分析更正而逆转；真实行动纠错/补偿仍需明确授权。历史重放仅为获授权审计，权限撤回不允许绕过访问限制读取历史。
## 实际实验
10种事件（两个发生身份各真/假/撤回、两政策值、权限撤回/恢复）全长4序列，共10000组，逐前缀比较2个事件×5查询量。直接参照按日志前缀筛选最新证据与政策并逐条件分支枚举，不使用候选缓存逻辑。再逐历史截点重放。三种故意错误对照：忽略撤回而回退非空旧事实、混用最近另一事件证据、用最终状态重构历史。差异计数为有限结构重复端口，非独立用户、真实语言错误率或现行产品缺陷。实验实际在连接器JS执行，无Node命令行、真实数据、训练或第三方AI运行时。
```json
{
  "sequences": 10000,
  "steps": 40000,
  "ports": 400000,
  "cacheHits": 120000,
  "invalidated": 280000,
  "staleValueChanges": 61832,
  "wrongFallback": 3028,
  "wrongLatestEvent": 21616,
  "wrongHistoricalReconstruction": 114898,
  "historicalChecks": 500000,
  "withdrawalChecks": 40000,
  "abaChecks": 14670,
  "controls": 4,
  "examples": [
    {
      "sequence": [
        {
          "t": 0,
          "v": true
        },
        {
          "t": 0,
          "v": false
        },
        {
          "t": 0,
          "v": null
        },
        {
          "t": 0,
          "v": true
        }
      ],
      "results": [
        "FAIL",
        "PASS",
        "UNKNOWN",
        "FAIL"
      ],
      "keys": [
        [
          0,
          3,
          0,
          0,
          1
        ],
        [
          0,
          3,
          0,
          0,
          2
        ],
        [
          0,
          3,
          0,
          0,
          3
        ],
        [
          0,
          3,
          0,
          0,
          4
        ]
      ]
    }
  ]
}
```
## 边界及下游
本轮历史及资格由夹具指定，未解析原语料中的条件引用，前轮S03/S13仍需自主语义识别和可信确认；无真实时间轴、来源资格、外部事实、持久化、签名、撤权删除、备份、跨端或真机性能证据。重复组合数量不表示统计泛化。研究者选定事件数、时间、阈值、缓存合同和比较基线；不作为生产标准。下一步连接真实语义候选的条件事件身份及政策/事实/实际行动三种效果，不以条件事实改变自动执行或撤销现实行为，独立轨验证真实入口。未修改生产或唯一交接，未开启Codex、训练、合并PR、部署、主动CI、费用或历史证据等级变化。
## 完整可执行复算
Node标准JS，无依赖；本轮实际在连接器JS运行。
```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),range=n=>Array.from({length:n},(_,i)=>i);
 // event t=0,1; learning sequence k; a null record withdraws the evidence, not the event.
 const actions=[{t:0,v:true},{t:0,v:false},{t:0,v:null},{t:1,v:true},{t:1,v:false},{t:1,v:null},{type:"policy",v:1},{type:"policy",v:2},{type:"grant",v:false},{type:"grant",v:true}];
 const initial=()=>({facts:[null,null],policy:{v:2,k:0},grant:{v:true,k:0},k:0});
 function advance(s,a){const r=JSON.parse(JSON.stringify(s));r.k++;if(a.type==="policy"||a.type==="grant")r[a.type]={v:a.v,k:r.k};else r.facts[a.t]={v:a.v,k:r.k};return r}
 function derive(s,t,x){const f=s.facts[t],known=s.grant.v&&f&&f.v!==null?f.v:null;const caps=known===null?[3,s.policy.v]:[known?s.policy.v:3];const values=[...new Set(caps.map(c=>x<=c))];const result=!s.grant.v?"NO_PERMISSION":values.length===2?"UNKNOWN":values[0]?"PASS":"FAIL";return {result,key:[t,x,s.policy.k,s.grant.k,f?.k??0],authority:"NONE"}}
 function oracle(log,t,x,asOf){const p=log.slice(0,asOf);let g=p.filter(a=>a.type==="grant").at(-1)?.v??true;if(!g)return "NO_PERMISSION";let cap=p.filter(a=>a.type==="policy").at(-1)?.v??2;const f=p.filter(a=>a.t===t).at(-1);let support=f&&f.v!==null?[f.v]:[false,true];let pass=0;for(let v of support)if(x<=(v?cap:3))pass++;return pass===support.length?"PASS":pass===0?"FAIL":"UNKNOWN"}
 const out={sequences:0,steps:0,ports:0,cacheHits:0,invalidated:0,staleValueChanges:0,wrongFallback:0,wrongLatestEvent:0,wrongHistoricalReconstruction:0,historicalChecks:0,withdrawalChecks:0,abaChecks:0,controls:0,examples:[]};
 function naive(log,t,x,kind){let p=log.filter(a=>a.type==="policy").at(-1)?.v??2,g=log.filter(a=>a.type==="grant").at(-1)?.v??true;if(!g)return "NO_PERMISSION";let f=kind==="fallback"?log.filter(a=>a.t===t&&a.v!==null).at(-1):log.filter(a=>a.t!==undefined).at(-1);let caps=f&&f.v!==null?[f.v?p:3]:[p,3],n=caps.filter(c=>x<=c).length;return n===caps.length?"PASS":n===0?"FAIL":"UNKNOWN"}
 function run(log){out.sequences++;let s=initial(),cache=range(2).flatMap(t=>range(5).map(x=>derive(s,t,x))),snap=[cache.map(z=>z.result)];const observedAction=Object.freeze({event:0,executed:true,knownAt:0});for(let k=0;k<log.length;k++){const before=s;s=advance(s,log[k]);out.steps++;let next=[];for(let t=0;t<2;t++)for(let x=0;x<5;x++){let i=t*5+x,r=derive(s,t,x),old=cache[i],fresh=oracle(log,t,x,k+1);out.ports++;ck(r.result===fresh,"oracle");const reuse=eq(r.key,old.key);if(reuse){out.cacheHits++;ck(r.result===old.result,"reuse");next.push(old)}else{out.invalidated++;out.staleValueChanges+=+(r.result!==old.result);next.push(r)}if(log[k].t===t&&log[k].v===null){out.withdrawalChecks++;ck(s.facts[t].v===null,"withdrawal tombstone")}if(naive(log.slice(0,k+1),t,x,"fallback")!==fresh)out.wrongFallback++;if(naive(log.slice(0,k+1),t,x,"latest")!==fresh)out.wrongLatestEvent++;if(before.facts[t]?.v===s.facts[t]?.v&&before.facts[t]?.k!==s.facts[t]?.k){out.abaChecks++;ck(!reuse,"same value new evidence")}ck(r.authority==="NONE","authority")}cache=next;snap.push(cache.map(z=>z.result));ck(observedAction.executed===true&&observedAction.knownAt===0,"observed immutable")}
 for(let k=0;k<snap.length;k++)for(let t=0;t<2;t++)for(let x=0;x<5;x++){out.historicalChecks++;const past=oracle(log,t,x,k);ck(snap[k][t*5+x]===past,"as of replay");if(k<log.length&&cache[t*5+x].result!==past)out.wrongHistoricalReconstruction++}}
 function enumerate(a){if(a.length===4){run(a);return}for(let e of actions)enumerate([...a,e])}enumerate([]);
 const seq=[actions[0],actions[1],actions[2],actions[0]];let s=initial(),rs=[];for(let a of seq){s=advance(s,a);rs.push(derive(s,0,3))}ck(eq(rs.map(r=>r.result),["FAIL","PASS","UNKNOWN","FAIL"]),"correction and withdraw");ck(!eq(rs[0].key,rs[3].key),"ABA");out.controls+=2;out.examples.push({sequence:seq,results:rs.map(r=>r.result),keys:rs.map(r=>r.key)});let a=advance(initial(),actions[0]),b=advance(a,actions[4]);ck(eq(derive(a,0,3),derive(b,0,3)),"other occurrence unchanged");out.controls++;let c=advance(b,actions[8]),d=advance(c,actions[9]);ck(derive(c,0,3).result==="NO_PERMISSION"&&!eq(derive(b,0,3).key,derive(d,0,3).key),"grant ABA");out.controls++;return out
}
console.log(JSON.stringify(experiment(),null,2));
```
