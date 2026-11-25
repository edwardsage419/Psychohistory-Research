# 第53轮：原生方法输入义务映射与按概率支持补证
2026-11-25。固定main 3a076683fc846fd71ce067cc660fe8d085c7e0b0，PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一产品交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第24/29/30/52轮。第5/40轮是一般追问优化，第27轮是局部分析依赖，本轮专注真实原生字段与validator的要求差异，未重新验证原数学核心。
## 真实源码定位与输入映射
固定原生decision_state.py 0840855431fbc88fe212785584277aa01be74d93 lines38-141；decision_v05.py bc27cc42e4a8224c86c3113d044a328ae5eeba3e lines22-51；decision_scoring.py 7832116703246bafc98831a6039d14c0d691cdd1 _basic_errors/_weight_errors/_weight_sensitivity_errors/_c034_errors；decision_regret.py e56689a54897d95eaa126540c23fca51cc0eede7 lines42-90；decision_voi.py a69571fcf6df9a779ed317e76c5dcac6933d2728 _probability_row/_prepare/_validate/_declared_policy；decision_timing.py 4ed9fa430dcb993cc5005656c8b1744276fe7c33 _common_errors/_investigation_errors；decision_hub.py a97de30f5241063862dbc0ce797c214cbc4d405f lines149-161；decision_planner.py f2d3d21b853afe9dc757a33e83cd3d6160f8dd7b lines184-247及_bounded/_documented/plan。method_contracts.json blob 4ff1666907c362066dcef697d955bc6fb689b75c。实际源码阅读，未运行完整Python入口。
候选语义义务映射（字段为真实路径或有明确范围的容器；不是完整schema生成器，具体运行仍由原生validator及结果资格决定）：
|登记方法|共享及专用字段|关键边界|
|---|---|---|
|c028_interval_feasibility|constraints_confirmed, constraints[*].operator/threshold/unit/horizon, options[*].measurements[constraint_id], 候选行动|明确无底线须由用户确认；可信区间、来源、同口径；底线不可由语言模型默认确认|
|comparability, pareto|objectives[*].id/direction/unit, options[*].scores[objective_id], ctx.feasible|至少两通过筛查方案及目标；基本validator不要求每单元完整，缺失可在结果保留，不能用加权义务阻止描述性比较|
|weight_sensitivity|上述加weights_confirmed, weights[objective_id], score_basis|点得分、共同效用/时域、权重范围可行；不可擅自用收入代替生活质量或确定用户权重|
|c034_joint_robustness|上述共同加权字段，score_dependence/source, score_transform, shared_offsets[objective_id]|两个max效用目标，rectangle或shared_additive；共同偏移需名义点值；不可假定独立误差|
|C029,C030,C031|scenarios[*].utilities[option_id], scenario_basis, scenario.kind/source, utility.unit/horizon或deadline|C029点，C030区间及联合依赖/来源影响结果资格，C031点中心加precision_radius和至少2可行方案；无概率后悔使用全部已列情景，不受VOI零先验过滤影响|
|voi_point,voi_oracle_bounds,voi_fixed_policy,voi_maximin,voi_randomized_certificate|information.signals, prior[scenario_id], likelihoods[scenario_id][signal_id], cost, actions_by_signal或unrestricted_actions+action_source, timing_basis, scenarios/utility/feasible|完整先验，收紧概率行，零上界状态无需条件行/效用；可能信号必须有可行动作；点模式要求唯一概率，非点需rectangle及来源；fixed另需固定行动映射；规模上限和真实证据另检|
|timing_actions|timing.confirmed/time_unit/time_origin/horizon, timing.actions/status_quo_option_id/fallback_option_id, scenarios/scenario_basis/feasible|真实期限、机会窗口、成本与延迟损失；局部策略可UNKNOWN；来源复审状态不解除|
|timing_investigation|上述共同时间字段，timing.investigation.mode/kind/source/cost及联合或条件因式分解事件结构|正概率分支、联合或条件独立依据及行动机会；需原生具体模式验证，不自动套用无延迟VOI|
确认、来源和权限必须来自可信宿主；LLM只提出原文定位、角色及缺口线索，不能写入confirmed或概率。区分可直接复用的已确认字段、数学可推导值（仅有确认依据及完整合同才可推导，本轮不自动填补缺失概率）、需要补证及禁止推定。原生输入源非空不等于真实性。义务应绑定方法版本、目标、主体、时域、证据、当前修订、实际分支和输出；一个输入可供多个方法复用，只有所有相关义务均不依赖时才可省略。不得把结果字段出现视为执行资格。
## 具体差异
原生VOI _probability_row 先要求完整有来源区间、验证合计1的可行性并收紧；_prepare排除先验收紧后上界为0的状态，不要求其条件信号概率和效用；活跃状态的收紧条件行上界均0的信号无需动作。现有planner._information在未执行任何voi_方法、非timed路径且已存在信号和情景时，先检查所有先验、所有状态×信号的_bounded，再检查cost、全部信号的_documented action_sets及timing_basis；不会按上述支持过滤。若其它条件（如成本）确实缺失，可能先追问已证明无影响的条件概率；若仅缺时间假设，可能先追问不可达信号行动。源级差异，不声称完整产品已复现；若已有任一VOI executed则此函数提前返回，本轮不覆盖这个多模式问题。_scenario_evidence亦遍历所有情景效用，属于后悔等比较义务，不能全局删除。当前timing_actions来源REVIEW_REQUIRED继续隔离。
## 修正原型
只在当前请求确实需要无延迟VOI、无timed路径且同一可信快照已确认有限互斥完备状态/信号集合、全部先验与来源时，使用原生概率行语义收紧。对于n项区间，L=sum l,H=sum h；L<=1<=H时，第i项可达到的精确下/上界=max(l_i,1-(H-h_i)), min(h_i,1-(L-l_i))。在已知矩形行结构内，非负先验上界正的状态和至少一活跃状态条件概率上界正的信号是可能支持；若相关联合约束导致该外包过宽，仍可保守保留义务。缺失、不合法或未确认时不得当零；缺先验先补先验，活跃行缺失先补行，冲突提示复核；只跳过经证明零贡献的义务，先检查实际成本，再检查可能信号动作和时间依据。用户确认的其他风险及比较目标单独计算。不改原生数学方法、不跳过必要硬约束，不承诺全部缺口消除或最优追问。
## 实际实验
二状态二信号，概率为0/0.5/1的区间端点。36种二元概率行，分别以整数单纯形点枚举核对收紧及存在性；对所有合法先验和两条件行，枚举联合支持与收紧上界一致。8种条件字段缺失掩码、4种动作字段掩码、2种成本/时间是否齐全；原型与原生planner顺序的精确谓词投影比较，固定所有字段来源、口径及语义资格均有效，原生程序未运行。候选使用可见字段的缺失掩码，仅收紧完整活跃行；未读取缺失的活跃数据来推断零；全表供独立枚举参考。changed统计首项补证顺序不同，非真实用户问题数下降；advanceAdmission表示仍需查看实际原生适用性审计，绝不授权运行。另有冲突、可能正概率及跨方法作用域控制。同研究者设计合成对照，非独立验收。
```js
function experiment(){
 const ck=(x,m)=>{if(!x)throw Error(m)},I=[[0,0],[0,1],[0,2],[1,1],[1,2],[2,2]],rows=[];
 // Probabilities are numerators over 2. Independent enumeration of each binary simplex.
 function points(row){return [0,1,2].filter(x=>row[0][0]<=x&&x<=row[0][1]&&row[1][0]<=2-x&&2-x<=row[1][1]);}
 function tighten(row){const lo=row[0][0]+row[1][0],hi=row[0][1]+row[1][1];if(lo>2||hi<2)return null;return row.map(([l,h])=>[Math.max(l,2-hi+h),Math.min(h,2-lo+l)]);}
 let rowChecks=0;
 for(const a of I)for(const b of I){const row=[a,b],p=points(row),t=tighten(row);rowChecks++;ck(!!t===!!p.length,"row existence");if(t){ck(t[0][0]===Math.min(...p)&&t[0][1]===Math.max(...p)&&t[1][0]===2-Math.max(...p)&&t[1][1]===2-Math.min(...p),"tighten");rows.push({row,t,p});}}
 // All identity, provenance, partition, units and authorization are fixture assumptions.
 // Known prior and available signals; no timed investigation, no unrestricted-actions flag, no executed VOI.
 // Source-equivalent projection of original _information first missing part; not the whole Python function.
 function legacy(missing,cost,actions,timing){if(missing)return "likelihoods";if(!cost)return "cost";if(actions!==3)return "actions_by_signal";if(!timing)return "timing_basis";return "admission";}
 function candidate(prior,ls,missing,cost,actions,timing){
   const pt=tighten(prior);if(!pt)return "prior_conflict";
   const active=[0,1].filter(s=>pt[s][1]>0);
   if(active.some(s=>missing&(3<<(2*s))))return "likelihoods";
   const ts=active.map(s=>tighten(ls[s]));if(ts.some(t=>!t))return "likelihood_conflict";
   const reachable=[0,1].filter(y=>ts.some(t=>t[y][1]>0));
   if(!cost)return "cost";
   if(reachable.some(y=>!(actions&(1<<y))))return "actions_by_signal";
   if(!timing)return "timing_basis";
   return "admission";
 }
 let cases=0,changed=0,unnecessaryLikelihood=0,unnecessaryAction=0,advanceCost=0,advanceTiming=0,advanceAdmission=0,retainedLikelihood=0,retainedActions=0,oracleChecks=0,zeroPriorByTightening=0,zeroSignalByTightening=0;
 let witness=null,signalWitness=null;
 for(const pr of rows)for(const x of rows)for(const y of rows){
  const ls=[x.row,y.row],active=[0,1].filter(s=>pr.p.some(p=>s===0?p>0:p<2)),reach=[0,1].filter(j=>active.some(s=>[x,y][s].p.some(p=>j===0?p>0:p<2)));
  // Construct exact independent support by enumerating prior and row point completions.
  const joint=new Set();for(const p of pr.p)for(const q of x.p)for(const v of y.p)for(const [s,prior,first] of [[0,p,q],[1,2-p,v]])for(const [j,likelihood] of [[0,first],[1,2-first]])if(prior*likelihood>0)joint.add(j);
  ck(reach.join()===Array.from(joint).sort().join(),"reachable support");oracleChecks++;
  const tightenZero=[0,1].some(s=>pr.row[s][1]>0&&pr.t[s][1]===0);if(tightenZero)zeroPriorByTightening++;
  if([0,1].some(j=>!reach.includes(j)&&active.some(s=>ls[s][j][1]>0)))zeroSignalByTightening++;
  for(const missing of [0,1,2,3,4,8,12,15])for(let actions=0;actions<4;actions++)for(const cost of [false,true])for(const timing of [false,true]){
   cases++;
   const requiredLikelihood=active.some(s=>(missing&(3<<(2*s)))!==0);
   const requiredActions=reach.some(j=>!(actions&(1<<j)));
   const truth=requiredLikelihood?"likelihoods":!cost?"cost":requiredActions?"actions_by_signal":!timing?"timing_basis":"admission";
   const a=legacy(missing,cost,actions,timing),b=candidate(pr.row,ls,missing,cost,actions,timing);
   ck(b===truth,"gap ordering");if(a!==b){changed++;if(a==="likelihoods"){unnecessaryLikelihood++;if(!witness&&b==="cost")witness={prior:pr.row,active,likelihoods:ls,missing,cost,actions,timing,old:a,new:b};}if(a==="actions_by_signal"){unnecessaryAction++;if(!signalWitness&&b==="timing_basis")signalWitness={prior:pr.row,active,reachable:reach,likelihoods:ls,missing,cost,actions,timing,old:a,new:b};}if(b==="cost")advanceCost++;if(b==="timing_basis")advanceTiming++;if(b==="admission")advanceAdmission++;}
   if(b==="likelihoods")retainedLikelihood++;if(b==="actions_by_signal")retainedActions++;
  }
 }
 // Fail closed on inconsistent prior or active rows; no imputation and no proof of execution.
 ck(candidate([[0,0],[0,0]],[[[0,0],[2,2]],[[0,0],[2,2]]],0,true,3,true)==="prior_conflict","prior");
 ck(candidate([[2,2],[0,0]],[[[0,0],[0,0]],[[0,0],[2,2]]],0,true,3,true)==="likelihood_conflict","row");
 ck(candidate([[0,2],[0,2]],[[[0,0],[2,2]],[[0,0],[2,2]]],4,true,3,true)==="likelihoods","possibly positive");
 // Unknown/cross-method scope must never be removed merely on VOI support: separate obligation sets.
 const scoped=[{method:"voi_point@1.0.0",need:["prior","likelihoods:active","utilities:active","cost","actions:reachable","timing_basis"]},{method:"C029@1.0.0",need:["scenario_basis","utilities:all","scenario_sources:all"]}];
 ck(scoped[1].need.includes("utilities:all"),"regret scope");
 return {rowChecks,validRows:rows.length,oracleChecks,cases,changed,unnecessaryLikelihood,unnecessaryAction,advanceCost,advanceTiming,advanceAdmission,retainedLikelihood,retainedActions,zeroPriorByTightening,zeroSignalByTightening,controls:4,witness,signalWitness};
}
console.log(JSON.stringify(experiment(),null,2));
```
## 实际输出
```json
{
  "rowChecks": 36,
  "validRows": 26,
  "oracleChecks": 17576,
  "cases": 2249728,
  "changed": 331280,
  "unnecessaryLikelihood": 324480,
  "unnecessaryAction": 6800,
  "advanceCost": 162240,
  "advanceTiming": 31480,
  "advanceAdmission": 31480,
  "retainedLikelihood": 1644032,
  "retainedActions": 204736,
  "zeroPriorByTightening": 2704,
  "zeroSignalByTightening": 1552,
  "controls": 4,
  "witness": {
    "prior": [
      [
        0,
        0
      ],
      [
        0,
        2
      ]
    ],
    "active": [
      1
    ],
    "likelihoods": [
      [
        [
          0,
          0
        ],
        [
          0,
          2
        ]
      ],
      [
        [
          0,
          0
        ],
        [
          0,
          2
        ]
      ]
    ],
    "missing": 1,
    "cost": false,
    "actions": 0,
    "timing": false,
    "old": "likelihoods",
    "new": "cost"
  },
  "signalWitness": {
    "prior": [
      [
        0,
        0
      ],
      [
        0,
        2
      ]
    ],
    "active": [
      1
    ],
    "reachable": [
      1
    ],
    "likelihoods": [
      [
        [
          0,
          0
        ],
        [
          0,
          2
        ]
      ],
      [
        [
          0,
          0
        ],
        [
          0,
          2
        ]
      ]
    ],
    "missing": 0,
    "cost": true,
    "actions": 2,
    "timing": false,
    "old": "actions_by_signal",
    "new": "timing_basis"
  }
}
```
## 接入与后续
B02/B05/B06/B07/B08/B11候选增量。建议原生validator提供结构化缺口码与依赖作用域，规划器根据当前方法请求、已证明支持及可信来源生成白话追问；避免从错误字符串推断语义。现有源码保持不变；修正原型在合成域通过，真实接口、支持运行环境、完整15方法输入投影、用户测试、Qwen、独立验收未执行。后续必须真实复现上述差异及多方法同时请求时的义务合并，测试零上界、极小正概率、相关行、缺失来源、非概率情景、timed joint/factorized、修改先验和过期结果。未启动Codex、CI、训练、合并、部署、生产修改、冻结协议修改或新增费用。
