# R236 S32 调查回答偏差：观察答卷依赖的样本选择与随机模式ITT

日期：2026年10月28日。原始239目录10-010。证据类别E1，仅九个冻结的人工二元调查机制。原R236正式有界E1验收保持不变。

## 事前冻结与真实来源
事前协议先行提交 `e891710fb2013a3cfe566cb73bcde7acc5d7e239`，路径 `protocols/R236_S32_RESPONSE_DEPENDENT_RETENTION_PRESCORE_FREEZE_2026-10-28.md`。随后才创建评分脚本与机器结果。直接读取原R236完整576条六源人工CSV，Git blob `c612b226c3db493e1c8dd96f16eff68b98f8704c`，原九世界观察联合JSON Git blob `00e0d819816062964e629b1da49d4d5f065a5257`。没有修改原生成机制、真实私人状态或原正式验收。

六种预冻结保留规则为ALL、Y1_POS_HALF、Y1_NEG_HALF、R1_POS_HALF、R1_NEG_HALF、PROXY_P_MISSING_HALF。每个来源保留概率为1或1/2，选择后重新归一；九世界×六规则，共54个条件，576条原始人工来源重复用于不同反事实选择规则，不能视为3240个独立真人。

## 精确结果
| 人工世界 | 原报告ITT | Y1成功减半保留 | Y1失败减半保留 | R1成功减半保留 | R1失败减半保留 | 原真私人模式效应 |
|---|---:|---:|---:|---:|---:|---:|
| TRUTHFUL_STABLE | 0 | 0 | 0 | -1/6 | 1/6 | 0 |
| TRUE_MODE_CHANGE | 1/2 | 2/3 | 1/3 | 1/2 | 1/2 | 1/2 |
| REPORT_MODE_CHANGE_ALIAS | 1/2 | 2/3 | 1/3 | 1/2 | 1/2 | 0 |
| TRUE_MODE_COMPLIER_ONLY | 1/4 | 4/15 | 4/21 | 1/10 | 5/14 | 1/4 |
| SOCIAL_DESIRABILITY_U | 0 | 0 | 0 | -3/20 | 3/28 | 0 |
| MODE_SUPPRESS_REPORT | -1/2 | -1/3 | -2/3 | -1/2 | -1/2 | 0 |

表中四个选择列均为保留样本中 `E[Y1|R=1,S=1]-E[Y1|R=0,S=1]`，其中S表示人工保留。随机分配R在原总体中成立；依据R及观察报告Y1决定是否保留，保留样本可能产生新的选择关联。

最小反例：TRUTHFUL_STABLE中私人状态不受R影响，完整样本报告ITT=0。仅将R=1且Y1=1的保留概率减半，保留样本报告ITT变为-1/6；仅将R=1且Y1=0的保留概率减半则变为+1/6。原人工真实私人因果效应始终0。

第二反例：TRUE_MODE_CHANGE与REPORT_MODE_CHANGE_ALIAS在全部54条件的对应六组中完整五变量观察联合继续完全相同，然而真实私人效应分别为1/2和0。对Y1成功者保留减半，观察ITT共同变为2/3；对Y1失败者保留减半，共同变为1/3。观察相同仍无法区分真正态度变化与回答变化。

第三反例：TRUE_MODE_COMPLIER_ONLY的真实私人效应保持1/4，保留样本的报告ITT却可为1/10或5/14。报告差异不能直接当作真实私人效应。

## 两条计算路线与边界
R程序 `research/validation/r236_s32_response_retention_exact_20261028.js` 从576条原来源逐行加权。B路径从原R236冻结五维观察联合JSON独立加权积分，逐条件比较观察联合单元、保留总质量、组别质量及报告ITT。R脚本内部执行1917项精确断言，失败0。另有独立B脚本 `research/evidence_audit/b_r236_s32_observable_joint_independent_20261028.js`，从原冻结联合JSON与本轮收据独立比较1878项，失败0，篡改一项ITT为999的测试成功检出。

ALL完全恢复原R236观察结果。P缺失独立保留负对照在九世界中均不改变报告ITT。三组原R236完整观察等价世界在全部六规则下保持逐格相同。

完整54条件的归一化五维联合、保留概率、各R组质量、报告ITT和固定oracle私人效应见 `research/validation/R236_S32_RESPONSE_RETENTION_54_CONDITION_RECEIPT_2026-10-28.json`。B审计报告另存 `research/evidence_audit/B_R236_S32_OBSERVABLE_RETENTION_AUDIT_2026-10-28.md`。

## 结论范围
这是人工世界中的精确选择机制反例，未估计任何真人问卷流失率、真实心理态度、现实因果效应、真实样本外预测或校准。两算法由同一项目流程执行，属于程序性独立复核，不属于外部团队独立复现。新增真人E2、历史E3均0。R073模型和评分规则、PESEN v0.1保持冻结。完整Node.js命令行及本轮GitHub Actions尚未执行，不能写成CI通过。继续按原R系列逐项完成后归纳分类，最后模型熔炼。