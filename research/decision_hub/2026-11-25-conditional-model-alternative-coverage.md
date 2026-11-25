# 竞争模型的条件适用域、完整覆盖与共同最优集合
2026-11-25。RESEARCH_CANDIDATE / EXACT_FINITE_DEVELOPMENT_EXECUTED / NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。起始main 3e599183f3e598f2a7a789f333956bec2df72551；Draft #62候选 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期10提交、14开放PR、v3.2前15行、同步规程前22行、唯一产品交接前18行blob 5e74f4f0b37141d631740e844ad8bbbfed232e07；检索model selection/disagreement/dispatch/eligibility/combination/routing、competition、method、composition、agreement、portfolio；读取R45 f211f008f3a3caf7b2dbaa66271562d92f07467e、R54 7ab23d84e837b9fdb05dee09335057a31f5f3709、R11 e140dda93ebb6065312baa69b44f16c2c1050b2f、R38 d49e8f17c885686523892bc95a1e00685c99beb1、R16 ad1f8f373eb41a68e9493511fd3ba9fd539fd56f、R112 d916fd5acec2a59e9b267fdb6f7e17931f25eb2c合同及相关结果前段。实际读取v0.7 decision_registry.py blob 8046de09674af850a456bbccc534e5f6c2511497：已有版本、适用性、输入输出、验证执行及固定依赖顺序。R38已有跨准则共同最优，R45已有证据限定路由，R112已有方法发现连接。本轮仅新增竞争假设按外部情景的适用关系及撤回后的覆盖缺口，非新模型学习或通用组合理论；不声称现有原生缺陷，全库查重有限。

## 合同
三个情景w、三个候选行动、三个竞争模型假设。每个模型适用的情景集合scope_i由可信宿主给定；相同目标、期限、行动全集、用户准则、尺度及全部硬约束已确认。每个模型提供在其适用情景下的完整非空最优行动集合M_i（本实验固定于该模型，不随情景另变，实际可扩展为M_i(w)）；模型假设可能是替代解释，不能把它们当同时必真的约束。不同目标或不同用户准则必须分开。仅当来源可信、结果可复算、模型集合穷尽本合同的可能解释，才能发布条件共同最优；模型选择及穷尽性为外部假设。无模型概率，无真实效用、结果测量、推荐、执行权或科学准入。撤回live掩码是模拟资格变化；若来源撤回但假设仍可能为真且无法计算，须保留该未知假设并阻塞全局共同最优，本实验的live=3仅模拟宿主已确认第三模型退出合同且其余候选仍穷尽的条件性重评。不可将隐私撤回自动当作理论被证伪。若穷尽性不明covered=false返回UNKNOWN_COVERAGE。

## 推导
对每个w，I(w)为适用且当前有资格的模型索引；若为空，明确缺覆盖，不能静默删除该情景。若非空，则所有竞争解释均最优的行动集合G(w)=交集M_i；至少一个解释最优的行动集合P(w)=并集M_i。全域共同最优G=交集_w G(w)，可能最优P=并集_w P(w)；必要充分性直接来自全称和存在量词。G为空只表示无统一共同最优，不表示无安全可行行动；若各w的G(w)非空，可在情景于决策前确知时提供条件分支，不能事前知晓未知情景或擅自选定分支。P是至少一个合格假设的最优行动，不是实际推荐或所有情景可行。共同最优仍需核对支配与其他偏好。若任一w未覆盖，局部结果保留，G/P=null（并非空集）；合同本身覆盖未知时无局部结果。禁止机械平均、复制投票及用共同最优交集代替可能最优并集。模型竞争与同时成立的证据约束不同；后者需单独证明共同真及兼容后方可求交。本模型只处理已确认最优集合，不处理将不同约束模型求交。复杂度O(世界×模型×行动)，小域位掩码，未测真实设备。

## 实验
7^3非空适用域组合×7^3非空最优集合×2资格模式=235298组。直接按行动成员逐世界逐模型遍历参照核验；两算法同研究者设计、同一合成夹具，非独立验收。skipMissingFalseCommon计忽略缺覆盖仍产生非空共同最优；intersectFalseExclusion计完整覆盖时共同集合不等于可能集合，若混用会排除条件最优；conditionalBranchCases为全域无共同而每个情景有共同的组；withdrawalChecks为第二种条件资格掩码的核验数量，不是实际撤回安全测试。12控制。人工选取模型数、情景、最优集合及资格模式；重复组合非真实用户或风险概率。无外部资料、个人数据、真实训练、原生API、CI请求、设备测量、合并、部署、费用或冻结变化。Node标准JS。

```js
function experiment(){
 const ck=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),A=[0,1,2],W=[0,1,2];
 const bits=m=>A.filter(a=>m&(1<<a)),masks=[1,2,3,4,5,6,7];
 // Hypothesis i can apply only in declared worlds. For the same output
 // contract its possible winner set is M[i]. Models are alternative worlds,
 // not simultaneous restrictions. Qualified host supplies exhaustive relation.
 function combine(scope,M,live,covered=true){
  if(!covered)return {status:"UNKNOWN_COVERAGE",authority:"NONE"};
  let rows=[],global=7,possible=0,missing=[];
  for(let w of W){
   let active=[0,1,2].filter(i=>(scope[i]&(1<<w))&&(live&(1<<i)));
   if(!active.length){missing.push(w);continue}
   let all=active.reduce((s,i)=>s&M[i],7),any=active.reduce((s,i)=>s|M[i],0);
   rows.push({w,active,all,any});global&=all;possible|=any;
  }
  return {status:missing.length?"PARTIAL_COVERAGE":global?"CONDITIONAL_COMMON":"CONDITIONAL_NO_COMMON",authority:"NONE",rows,missing,common:missing.length?null:global,possible:missing.length?null:possible};
 }
 function oracle(scope,M,live){
  let rows=[],missing=[],sets=[];
  for(let w of W){
   let active=[0,1,2].filter(i=>Boolean(scope[i]&(1<<w))&&Boolean(live&(1<<i)));
   if(!active.length){missing.push(w);continue}
   let alternatives=active.map(i=>bits(M[i]));sets.push(...alternatives);
   rows.push({w,active,all:A.reduce((s,a)=>s|(alternatives.every(x=>x.includes(a))?1<<a:0),0),any:A.reduce((s,a)=>s|(alternatives.some(x=>x.includes(a))?1<<a:0),0)});
  }
  let common=missing.length?null:A.reduce((s,a)=>s|(sets.every(x=>x.includes(a))?1<<a:0),0);
  let possible=missing.length?null:A.reduce((s,a)=>s|(sets.some(x=>x.includes(a))?1<<a:0),0);
  return {rows,missing,common,possible};
 }
 let o={cases:0,complete:0,partial:0,stable:0,noCommon:0,conditionalBranchCases:0,skipMissingFalseCommon:0,intersectFalseExclusion:0,withdrawalChecks:0,controls:0,witnesses:{}};
 for(let a of masks)for(let b of masks)for(let c of masks)for(let x of masks)for(let y of masks)for(let z of masks){
  let scope=[a,b,c],M=[x,y,z];
  // Only one all-live pass plus one deterministic source-withdrawal case.
  for(let live of [7,3]){
   let v=combine(scope,M,live),q=oracle(scope,M,live);
   ck(eq(v.rows,q.rows)&&eq(v.missing,q.missing)&&v.common===q.common&&v.possible===q.possible,"oracle");o.cases++;
   if(live===3)o.withdrawalChecks++;
   if(v.missing.length){
    o.partial++;
    if(v.rows.length&&v.rows.reduce((s,r)=>s&r.all,7)){o.skipMissingFalseCommon++;o.witnesses.missing??={scope,M,live,result:v}}
   }else{
    o.complete++;if(v.common)o.stable++;else{o.noCommon++;if(v.rows.every(r=>r.all)){o.conditionalBranchCases++;o.witnesses.branch??={scope,M,live,result:v}}}
    // Wrongly using universal winner intersection as possible-winner set.
    if(v.common!==v.possible){o.intersectFalseExclusion++;o.witnesses.intersection??={scope,M,live,result:v}}
   }
  }
 }
 for(let t of [o.cases===235298,o.complete+o.partial===o.cases,o.stable+o.noCommon===o.complete,o.withdrawalChecks===117649,o.skipMissingFalseCommon>0,o.conditionalBranchCases>0,o.intersectFalseExclusion>0,combine([1,2,4],[1,2,4],7).common===0,combine([1,2,4],[1,2,4],3).common===null,combine([7,7,7],[1,2,4],7).possible===7,combine([7,7,7],[1,2,4],7).common===0,combine([7,7,7],[1,2,4],7,false).status==="UNKNOWN_COVERAGE"]){ck(t,"control "+o.controls);o.controls++}
 return o;
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实测
```json
{
  "cases": 235298,
  "complete": 150920,
  "partial": 84378,
  "stable": 90110,
  "noCommon": 60810,
  "conditionalBranchCases": 12060,
  "skipMissingFalseCommon": 56694,
  "intersectFalseExclusion": 140490,
  "withdrawalChecks": 117649,
  "controls": 12,
  "witnesses": {
    "missing": {
      "scope": [
        1,
        1,
        1
      ],
      "M": [
        1,
        1,
        1
      ],
      "live": 7,
      "result": {
        "status": "PARTIAL_COVERAGE",
        "authority": "NONE",
        "rows": [
          {
            "w": 0,
            "active": [
              0,
              1,
              2
            ],
            "all": 1,
            "any": 1
          }
        ],
        "missing": [
          1,
          2
        ],
        "common": null,
        "possible": null
      }
    },
    "branch": {
      "scope": [
        1,
        1,
        6
      ],
      "M": [
        1,
        1,
        2
      ],
      "live": 7,
      "result": {
        "status": "CONDITIONAL_NO_COMMON",
        "authority": "NONE",
        "rows": [
          {
            "w": 0,
            "active": [
              0,
              1
            ],
            "all": 1,
            "any": 1
          },
          {
            "w": 1,
            "active": [
              2
            ],
            "all": 2,
            "any": 2
          },
          {
            "w": 2,
            "active": [
              2
            ],
            "all": 2,
            "any": 2
          }
        ],
        "missing": [],
        "common": 0,
        "possible": 3
      }
    },
    "intersection": {
      "scope": [
        1,
        1,
        6
      ],
      "M": [
        1,
        1,
        2
      ],
      "live": 7,
      "result": {
        "status": "CONDITIONAL_NO_COMMON",
        "authority": "NONE",
        "rows": [
          {
            "w": 0,
            "active": [
              0,
              1
            ],
            "all": 1,
            "any": 1
          },
          {
            "w": 1,
            "active": [
              2
            ],
            "all": 2,
            "any": 2
          },
          {
            "w": 2,
            "active": [
              2
            ],
            "all": 2,
            "any": 2
          }
        ],
        "missing": [],
        "common": 0,
        "possible": 3
      }
    }
  }
}
```
后续：把原生方法适用性、证据缺口、待确认条件与上述集合输出连接；对仍可能成立却因证据失效无法计算的假设保持未知；独立轨验证未见输入、真实来源和跨模型比较合同，产品轨维护唯一交接。本轮不授权正式版本开发。