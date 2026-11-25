# 跨决策目标完成日期与最小延期前沿
2026-11-25。RESEARCH_CANDIDATE / EXACT_FINITE_DEVELOPMENT_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 15a2f6f85b248b962e797014d31def7ed6748919；Draft #62固定 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期10提交、14开放PR、v3.2前12行及历史全文、唯一产品交接前18行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、前轮现金义务并集研究。查重搜索deadline/opportunity/completion/delay/schedule，读取R119（c58fb6fb43989c611e17a36caeaaf80b6c7fd51e）和R98（f8a16f272ec27d0d95fe90d7f323c8969b6c2978）合同与算法前段，以及完成时间研究acdd995760d49ff6e820612e4de8f5beba8afa70增量。R119已有EDF固定窗口与新增可选工时；R98已有配对承诺与资源前沿；本轮只新增给定现金及固定新计划时的联合完成日期集合、最小延期向量及边际最早日期不能同时实现的诊断，非新通用规划算法。无法保证全库无重叠。

## 合同及计算
四期每日单一工作槽，两个既有目标各需一个槽及非负一次性支付，均需完成。用户期望完成日dA/dB暂作为可协商的软目标；如为硬截止，不得自动延期。新计划固定第1或2日占用一个槽并付款；给定每日确定条件收入、初始现金和储备，每日先结算收入及新计划费用，再检查储备，再支付旧目标费用并再次检查。所有支付、同账户同币种及覆盖身份由可信宿主夹具给定，真实资格待验；不使用预测收入当现实现金，不假定新计划带来收益或互补，不处理连续任务、跨账户、随机、借贷、违约和实际日期。初始也检查储备。没有真实计划执行或授权。

对照原计划无新增占用，以相同初始账本枚举两个旧目标日期对(tA,tB)，校验所有期现金及槽位。新计划日期对集合是原集合的子集：移除非负费用和占用不会降低任一现金余额或增加冲突。只在此纯资源消耗假设成立，不能推广到有收益或互补项目。每可行日期对映射延期向量(max(0,tA-dA),max(0,tB-dB))。逐维不大且至少一维更小定义支配，保留非支配向量；给定允许延期向量e，当且仅当前沿有逐维不超过e的点可行（有限集合中任一点都被某非支配点弱支配）。最小共同延期为所有向量最大分量的最小值，仅为用户明确接受同一延期上限时的参考，不是生活总分或默认选择。单目标最早日期分别取完整联合集合的边际最小值，若其组合不在集合中不得显示为同一可达方案。没有日期对仅说明给定四期内无共同完成方案；进一步区分新增计划自身现金不可行与新增计划单独可行但两旧目标共同完成不可行；不得输出无限延期或永久不可达。缺覆盖UNKNOWN；所有结果authority NONE。枚举H²个日期对，各扫描H期，O(H³)，前沿直接比较最坏O(H⁴)，未测实际资源。一般模型需独立调度及更广义依赖。

## 实验
先执行短期限1/2日的1728组探索，新增计划必占前两天导致新增组全部无法同时按期完成，样本结构过于偏向冲突；故扩展两目标期限至2/3/4日，正式报告下列3888组公开开发夹具（并非预注册或独立留出）。同一研究者另以3^4行动字符串直接枚举核对完整日期对集合；每组对原/新两组各25种允许延期向量核对前沿与全集合，检验压缩不丢可行性。基线为无新计划的条件反事实，不是现实观测。各组合重复相同资源参数及不同截止日，不能当独立用户或风险概率。12控制。研究者选择时域、目标、资源、费用及允许延期口径，无用户真实数据、新外部资料、训练、原生、真机、CI请求、PR合并、部署、冻结修改或新增费用。复算Node标准JS。

```js
function experiment(){
 const H=4,ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),key=x=>x.join(","),pack=s=>[...s].sort();
 function pairs(p,add,covered=true){
  if(!covered)return {status:"UNKNOWN",authority:"NONE"};
  let rows=new Set(),work=0;
  for(let a=1;a<=H;a++)for(let b=1;b<=H;b++){
   work++;if(a===b||add&&(a===p.busy||b===p.busy))continue;
   let cash=p.cash,valid=cash>=p.reserve;
   for(let d=1;d<=H&&valid;d++){
    cash+=p.income;if(add&&d===p.busy)cash-=p.fee;
    if(cash<p.reserve){valid=false;break}
    if(a===d)cash-=p.ca;if(b===d)cash-=p.cb;
    if(cash<p.reserve)valid=false;
   }if(valid)rows.add(key([a,b]));
  }
  return {status:rows.size?"CONDITIONAL":"NO_JOINT_COMPLETION_WITHIN_HORIZON",authority:"NONE",rows,work};
 }
 function oracle(p,add){
  let rows=new Set();
  for(let n=0;n<3**H;n++){
   let q=n,c=p.cash,dates=[0,0],valid=c>=p.reserve;
   for(let d=1;d<=H&&valid;d++){
    let a=q%3;q=Math.floor(q/3);c+=p.income;
    if(add&&d===p.busy){c-=p.fee;if(a)valid=false}
    if(c<p.reserve)valid=false;
    if(a){if(dates[a-1])valid=false;dates[a-1]=d;c-=a===1?p.ca:p.cb}
    if(c<p.reserve)valid=false;
   }if(valid&&dates.every(Boolean))rows.add(key(dates));
  }return rows;
 }
 const vec=s=>[...s].map(k=>k.split(",").map(Number));
 const frontier=v=>v.filter(x=>!v.some(y=>y.every((a,i)=>a<=x[i])&&y.some((a,i)=>a<x[i]))).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 function impact(s,p){
  let v=vec(s);if(!v.length)return null;
  let ds=v.map(x=>[Math.max(0,x[0]-p.da),Math.max(0,x[1]-p.db)]);
  let f=frontier(vec(new Set(ds.map(key)))),minimum=[Math.min(...v.map(x=>x[0])),Math.min(...v.map(x=>x[1]))];
  return {earliest:minimum,earliestJoint:s.has(key(minimum)),onTime:ds.some(x=>x.every(a=>a===0)),extensions:f,common:Math.min(...ds.map(x=>Math.max(...x)))};
 }
 let out={cases:0,referenceChecks:0,datePairs:0,actionStrings:0,baseJoint:0,newJoint:0,baseOnTime:0,newOnTime:0,baseOnTimeLost:0,lostButRecoverable:0,lostNewPlanAloneInfeasible:0,lostJointWithinHorizon:0,earliestPairUnattainableAfter:0,minimumExtensionHistogram:[0,0,0,0,0],monotonicChecks:0,extensionChecks:0,controls:0,witnesses:{}};
 for(let cash of [0,2,4])for(let reserve of [0,1])for(let income of [0,1,2])for(let ca of [1,3])for(let cb of [1,3])for(let fee of [0,1,3])for(let busy of [1,2])for(let da of [2,3,4])for(let db of [2,3,4]){
  let p={cash,reserve,income,ca,cb,fee,busy,da,db},a=pairs(p,false),b=pairs(p,true),x=impact(a.rows,p),y=impact(b.rows,p);
  ck(eq(pack(a.rows),pack(oracle(p,false)))&&eq(pack(b.rows),pack(oracle(p,true))),"oracle");
  ck([...b.rows].every(k=>a.rows.has(k)),"subset");
  out.cases++;out.referenceChecks+=2;out.datePairs+=a.work+b.work;out.actionStrings+=2*3**H;out.monotonicChecks++;
  out.baseJoint+=+!!x;out.newJoint+=+!!y;out.baseOnTime+=+!!x?.onTime;out.newOnTime+=+!!y?.onTime;
  // For each possible extension, the Pareto set must give exactly the same
  // feasibility answer as the full set of completion-date pairs.
  for(let [s,i] of [[a.rows,x],[b.rows,y]])for(let u=0;u<=H;u++)for(let v=0;v<=H;v++){
   let ref=vec(s).some(d=>d[0]<=da+u&&d[1]<=db+v);
   let front=!!i&&i.extensions.some(d=>d[0]<=u&&d[1]<=v);
   ck(ref===front,"extension coverage");out.extensionChecks++;
  }
  if(x?.onTime&&!y?.onTime){
   out.baseOnTimeLost++;
   if(y){out.lostButRecoverable++;out.minimumExtensionHistogram[y.common]++;out.witnesses.delay??={p,base:x,new:y}}
   else if(cash<reserve||cash+busy*income-fee<reserve){out.lostNewPlanAloneInfeasible++;out.witnesses.newAlone??={p}}
   else{out.lostJointWithinHorizon++;out.witnesses.jointHorizon??={p}}
  }
  if(y&&!y.earliestJoint){out.earliestPairUnattainableAfter++;out.witnesses.joint??={p,new:y,attainable:pack(b.rows)}}
 }
 let p={cash:10,reserve:0,income:0,ca:1,cb:1,fee:0,busy:1,da:1,db:2};
 const a=impact(pairs(p,false).rows,p),b=impact(pairs(p,true).rows,p);
 const tests=[out.cases===3888,out.referenceChecks===7776,out.baseOnTimeLost===out.lostButRecoverable+out.lostNewPlanAloneInfeasible+out.lostJointWithinHorizon,out.baseOnTime>=out.newOnTime,out.baseJoint>=out.newJoint,a.onTime&&!b.onTime,b.common===1,b.earliest[0]===2&&b.earliest[1]===2&&!b.earliestJoint,eq(b.extensions,[[1,1],[2,0]]),pairs(p,true,false).status==="UNKNOWN",out.extensionChecks===194400,out.newOnTime>0];
 for(let t of tests){ck(t,"control "+out.controls);out.controls++}
 return out;
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实测
```json
{
  "cases": 3888,
  "referenceChecks": 7776,
  "datePairs": 124416,
  "actionStrings": 629856,
  "baseJoint": 2322,
  "newJoint": 1890,
  "baseOnTime": 2208,
  "newOnTime": 1558,
  "baseOnTimeLost": 650,
  "lostButRecoverable": 282,
  "lostNewPlanAloneInfeasible": 112,
  "lostJointWithinHorizon": 256,
  "earliestPairUnattainableAfter": 1800,
  "minimumExtensionHistogram": [
    0,
    273,
    9,
    0,
    0
  ],
  "monotonicChecks": 3888,
  "extensionChecks": 194400,
  "controls": 12,
  "witnesses": {
    "delay": {
      "p": {
        "cash": 0,
        "reserve": 0,
        "income": 1,
        "ca": 1,
        "cb": 1,
        "fee": 0,
        "busy": 1,
        "da": 2,
        "db": 2
      },
      "base": {
        "earliest": [
          1,
          1
        ],
        "earliestJoint": false,
        "onTime": true,
        "extensions": [
          [
            0,
            0
          ]
        ],
        "common": 0
      },
      "new": {
        "earliest": [
          2,
          2
        ],
        "earliestJoint": false,
        "onTime": false,
        "extensions": [
          [
            0,
            1
          ],
          [
            1,
            0
          ]
        ],
        "common": 1
      }
    },
    "joint": {
      "p": {
        "cash": 0,
        "reserve": 0,
        "income": 1,
        "ca": 1,
        "cb": 1,
        "fee": 0,
        "busy": 1,
        "da": 2,
        "db": 2
      },
      "new": {
        "earliest": [
          2,
          2
        ],
        "earliestJoint": false,
        "onTime": false,
        "extensions": [
          [
            0,
            1
          ],
          [
            1,
            0
          ]
        ],
        "common": 1
      },
      "attainable": [
        "2,3",
        "2,4",
        "3,2",
        "3,4",
        "4,2",
        "4,3"
      ]
    },
    "newAlone": {
      "p": {
        "cash": 0,
        "reserve": 0,
        "income": 1,
        "ca": 1,
        "cb": 1,
        "fee": 3,
        "busy": 1,
        "da": 2,
        "db": 2
      }
    },
    "jointHorizon": {
      "p": {
        "cash": 0,
        "reserve": 0,
        "income": 1,
        "ca": 1,
        "cb": 3,
        "fee": 1,
        "busy": 1,
        "da": 2,
        "db": 4
      }
    }
  }
}
```
下一步应将前轮现金义务身份与已确认目标期限接入真实资源快照，保留共同可行见证、旧目标冲突、硬期限制及授权，不自动改变目标。独立轨负责未见案例及真实入口，产品轨维护唯一交接。当前不授权完整版本开发。