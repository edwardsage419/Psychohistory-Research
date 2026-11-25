# 跨计划持续收益的最低可行阈值与兑现时序
2026-11-25。RESEARCH_CANDIDATE / EXACT_FINITE_DEVELOPMENT_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 82f44d69ababea611a0d9bb31f2b8f68cbb7602a；Draft #62固定候选 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期10提交、14开放PR、v3.2前12行、唯一产品交接前18行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。检索complement/investment/skill/feedback/income/longitudinal/threshold，审查R42、R98、R101、R110合同及R99全文（research/decision_hub/2026-11-25-complementarity-realization-timing.md，blob a1ea992561b43252c99e882494640b290a8fa5a4）。R99已有一次收益及减免、固定情景联合路径和提前入账错误；R101已有到账语义账本连接；本轮仅新增连续收益的逆向阈值、兑现延迟单调性与前轮联合目标期限的连接。非新通用优化方法；不能保证全库无重叠。

## 合同与推导
四期，每期单一工作槽，两个旧目标A/B各需一个槽和非负一次支出ca/cb，具有硬截止da/db。新计划固定busy期占槽并支付fee；其假设新增持续净收入x为非负整数，自busy+lag起每期到账，lag>=1。初始资金cash、储备reserve、每期基础净收入income>=0。初始先检查储备，每期收入到账后、训练及旧目标支出后均保持储备。因当期支出均非负且互不占同一槽，期末检查蕴含同期期中检查；不推广到任意日内事件顺序。旧目标必须在期限内完成。无随机、贷款、通胀、贴现、学习成功概率、收入因果识别、税务及其他真实成本；所有输入和覆盖来自研究者构造的合成夹具。未来收入仅条件情景，不入当前实际账本。

固定联合完成日期(a,b)，设C_t^0为不计新增收入时累计现金，k_t=max(0,t-busy-lag+1)为截至t累计新增收入次数。现金底线要求C_t^0+k_t*x>=reserve。若初始已违底线，或存在k_t=0且C_t^0<reserve，该日期对无有限收益阈值；否则其最低非负整数收益为max(0,max_{t:k_t>0} ceil((reserve-C_t^0)/k_t))。在所有符合期限及占槽条件的日期对上取最小值，并保留达到最小值的见证日期对。若无有限值，表示此固定时序、合同和时域中即使任意增大后续收益也无法满足全部约束；并非永久不可行。收益延迟增大时k_t逐期不增，因此最低阈值不降。这是特定静态输入下的必要充分条件，非现实投资回报预测、NPV或效用最优。用户可指定收益下界及最晚兑现期，在此单调模型中以最不利参数核对可行性；如果收入支持包含0且最低阈值为正，则不能宣称对所有收益情景保证可行。真实支持、联合相关性、因果关系须有独立证据。覆盖缺失UNKNOWN。authority NONE。枚举至多H²个日期对，每对扫描H期，O(H³)；未测设备资源。

## 实验
3初始现金×2储备×3基础收入×2 A成本×2 B成本×3新计划成本×2占用日期×2 A期限×2 B期限×3到账延迟=5184组。每组在额外收益整数0..10上以另一个3^4行动序列直接枚举实现核对阈值。该域总支出加储备至多10，故任何有限阈值不超过10。另查延迟增大单调性。对照提前在新计划当期记入收益及仅检查期末余额（两者在测试收益2时），属于故意错误的计算基线，非实际产品错误或风险概率。343组无新增计划时无法按期完成旧目标、加入计划且足够收益时可行；不意味着真实项目必有收益，也不称福利改善。uncertainZeroDisallows只计测试收益2可行但0不可行的组。参数及期限自行选择，重复夹具不当作独立样本。独立验收未执行，原生未接入，未实测真实用户和资源。无个人数据、新外部数据、第三方推理、训练、CI请求、PR合并、部署、冻结改动或新增费用。复算Node标准JS。
```js
function experiment(){
 const H=4,ck=(v,m)=>{if(!v)throw Error(m)},INF=Infinity;
 function threshold(p,covered=true){
  if(!covered)return {status:"UNKNOWN",authority:"NONE"};
  let best=INF,witness=[],paths=0;
  if(p.cash<p.reserve)return {status:"NO_FINITE_THRESHOLD",authority:"NONE",paths};
  for(let a=1;a<=p.da;a++)for(let b=1;b<=p.db;b++){
   if(a===b||a===p.busy||b===p.busy)continue;paths++;
   let c=p.cash,need=0;
   for(let d=1;d<=H;d++){
    c+=p.income-(d===p.busy?p.fee:0)-(d===a?p.ca:0)-(d===b?p.cb:0);
    let k=Math.max(0,d-p.busy-p.lag+1),gap=p.reserve-c;
    if(gap>0&&!k){need=INF;break}
    if(k)need=Math.max(need,Math.ceil(gap/k));
   }
   if(need<best){best=need;witness=[[a,b]]}else if(need===best&&Number.isFinite(need))witness.push([a,b]);
  }
  return Number.isFinite(best)?{status:"CONDITIONAL",authority:"NONE",minimum:best,witness,paths}:{status:"NO_FINITE_THRESHOLD",authority:"NONE",paths};
 }
 function feasible(p,x,early=false,terminalOnly=false,add=true){
  if(p.cash<p.reserve&&!terminalOnly)return false;
  for(let n=0;n<3**H;n++){
   let q=n,c=p.cash,dates=[0,0],ok=true;
   for(let d=1;d<=H&&ok;d++){
    let a=q%3;q=Math.floor(q/3);
    c+=p.income+(add&&d>=p.busy+(early?0:p.lag)?x:0);
    if(add&&d===p.busy){c-=p.fee;if(a)ok=false}
    if(!terminalOnly&&c<p.reserve)ok=false;
    if(a){if(dates[a-1]||d>(a===1?p.da:p.db))ok=false;dates[a-1]=d;c-=a===1?p.ca:p.cb}
    if(!terminalOnly&&c<p.reserve)ok=false;
   }
   if(ok&&dates.every(Boolean)&&c>=p.reserve)return true;
  }return false;
 }
 let o={cases:0,finite:0,zero:0,positive:0,noFinite:0,thresholdChecks:0,activationMonotonic:0,baseFeasible:0,baseUnavailableRescued:0,earlyFalseAtTest:0,terminalFalseAtTest:0,uncertainZeroDisallows:0,controls:0,hist:{},witnesses:{}};
 for(let cash of [0,2,4])for(let reserve of [0,1])for(let income of [0,1,2])for(let ca of [1,3])for(let cb of [1,3])for(let fee of [0,2,3])for(let busy of [1,2])for(let da of [2,4])for(let db of [3,4])for(let lag of [1,2,3]){
  let p={cash,reserve,income,ca,cb,fee,busy,da,db,lag},r=threshold(p),f=r.status==="CONDITIONAL",m=f?r.minimum:INF;
  o.cases++;o.finite+=+f;o.noFinite+=+!f;o.zero+=+(m===0);o.positive+=+(f&&m>0);
  if(f)o.hist[m]=(o.hist[m]||0)+1;
  for(let x=0;x<=10;x++){ck(feasible(p,x)===(x>=m),"threshold");o.thresholdChecks++}
  let later=threshold({...p,lag:lag+1}),lm=later.status==="CONDITIONAL"?later.minimum:INF;
  ck(lm>=m,"later");o.activationMonotonic++;
  let base=feasible(p,0,false,false,false);o.baseFeasible+=+base;
  if(!base&&f){o.baseUnavailableRescued++;o.witnesses.rescue??={p,result:r}}
  if(!feasible(p,2)&&feasible(p,2,true)){o.earlyFalseAtTest++;o.witnesses.early??={p,minimum:f?m:null}}
  if(!feasible(p,2)&&feasible(p,2,false,true)){o.terminalFalseAtTest++;o.witnesses.terminal??={p,minimum:f?m:null}}
  if(f&&m>0&&m<=2){o.uncertainZeroDisallows++;o.witnesses.conditional??={p,result:r}}
 }
 let p={cash:2,reserve:1,income:0,ca:1,cb:1,fee:1,busy:1,da:2,db:3,lag:1};
 let r=threshold(p);
 for(let t of [o.cases===5184,o.thresholdChecks===57024,o.finite+o.noFinite===o.cases,o.zero+o.positive===o.finite,r.minimum===1,threshold({...p,cash:1}).status==="NO_FINITE_THRESHOLD",threshold({...p,lag:2}).status==="NO_FINITE_THRESHOLD",threshold(p,false).status==="UNKNOWN",o.baseUnavailableRescued>0,o.earlyFalseAtTest>0]){ck(t,"control "+o.controls);o.controls++}
 return o;
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实测
```json
{
  "cases": 5184,
  "finite": 2866,
  "zero": 2247,
  "positive": 619,
  "noFinite": 2318,
  "thresholdChecks": 57024,
  "activationMonotonic": 5184,
  "baseFeasible": 3024,
  "baseUnavailableRescued": 343,
  "earlyFalseAtTest": 1117,
  "terminalFalseAtTest": 1113,
  "uncertainZeroDisallows": 536,
  "controls": 10,
  "hist": {
    "0": 2247,
    "1": 343,
    "2": 193,
    "3": 83
  },
  "witnesses": {
    "rescue": {
      "p": {
        "cash": 0,
        "reserve": 0,
        "income": 0,
        "ca": 1,
        "cb": 1,
        "fee": 0,
        "busy": 1,
        "da": 2,
        "db": 3,
        "lag": 1
      },
      "result": {
        "status": "CONDITIONAL",
        "authority": "NONE",
        "minimum": 1,
        "witness": [
          [
            2,
            3
          ]
        ],
        "paths": 1
      }
    },
    "conditional": {
      "p": {
        "cash": 0,
        "reserve": 0,
        "income": 0,
        "ca": 1,
        "cb": 1,
        "fee": 0,
        "busy": 1,
        "da": 2,
        "db": 3,
        "lag": 1
      },
      "result": {
        "status": "CONDITIONAL",
        "authority": "NONE",
        "minimum": 1,
        "witness": [
          [
            2,
            3
          ]
        ],
        "paths": 1
      }
    },
    "early": {
      "p": {
        "cash": 0,
        "reserve": 0,
        "income": 0,
        "ca": 1,
        "cb": 1,
        "fee": 0,
        "busy": 1,
        "da": 2,
        "db": 3,
        "lag": 2
      },
      "minimum": null
    },
    "terminal": {
      "p": {
        "cash": 0,
        "reserve": 0,
        "income": 0,
        "ca": 1,
        "cb": 1,
        "fee": 0,
        "busy": 1,
        "da": 2,
        "db": 3,
        "lag": 2
      },
      "minimum": null
    }
  }
}
```
## 后续
与前轮联合期限前沿及R101/R110已获资格账本接口连接；进一步研究收益来源依赖、条件下界变化、现金与时间收益不同量纲及撤回重算。真实收益证据不足时仅展示达到可行所需门槛，不能编造概率或把预测入账。产品轨维护唯一近期交接，独立轨负责未见及原生验收。无本轮正式版本开发授权。