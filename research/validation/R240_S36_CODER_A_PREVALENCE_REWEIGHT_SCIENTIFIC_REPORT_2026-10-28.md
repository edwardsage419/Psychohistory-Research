# R240 S36：观察编码者A标签边际重加权对Cohen κ的有限人工敏感性

日期：2026-10-28。原目录10-014 Inter Coder Reliability Models，九个人工世界原R240已正式有界验收。本轮只增加独立E1机制研究，不变更原验收状态。

## 事前协议、固定来源与程序
先冻结 [S36协议](../../protocols/R240_S36_OBSERVED_CODER_A_PREVALENCE_REWEIGHT_PRESCORE_FREEZE_2026-10-28.md)，冻结commit `6c3ec37fd867cf223ccb2709ea49d99ca6a8159d`。原R240 CSV Git blob `ef6b1382c80d9fe2e3a13054e31a7195786c4c7a`，原结果JSON blob `ea2dca9b93045e8c9765179e6b4e46dc82c0f267`。原2304条来源（九世界各256）不修改。

R主线源码 [r240_s36_coder_A_reweight_source_first_20261028.js](r240_s36_coder_A_reweight_source_first_20261028.js) 从完整CSV逐行读取S、可见A/B和来源质量，对S=1且A=0的记录赋权1，S=1且A=1的记录赋权w∈{1,2,4,8}，S=0不读取隐藏A/B。逐世界形成加权2×2表，精确有理数输出Po、Pe和Cohen κ。九世界×四权重共36个条件，完整收据 [R240 S36 exact JSON](R240_S36_CODER_A_REWEIGHT_EXACT_RECEIPT_2026-10-28.json)。

该权重是有限观察概率质量重加权，不是实际新参与者、独立重复采样或有效样本量。原R240有限名义α使用无放回编码符号计数，本轮不将加权质量伪装成独立样本以计算α。所有R073/PESEN v0.1原评分与状态冻结。

## 主要精确结果

| 人工世界 | 原Po | A=1权重8时Po | 原κ | A=1权重8时κ |
| --- | ---: | ---: | ---: | ---: |
| PERFECT_TRUTHFUL | 1 | 1 | 1 | 1 |
| PERFECT_SYSTEMATICALLY_WRONG | 1 | 1 | 1 | 1 |
| SHARED_SYSTEMATIC_ERROR | 1 | 1 | 1 | 1 |
| INDEPENDENT_QUARTER_ERRORS | 5/8 | 5/8 | 1/4 | 32/275 |
| BALANCED_INDEPENDENT_RANDOM | 1/2 | 1/2 | 0 | 0 |
| RARE_POSITIVE_INDEPENDENT_RANDOM | 25/32 | 19/40 | 0 | 0 |
| ASYMMETRIC_FALSE_POSITIVE | 7/8 | 35/36 | 3/4 | 16/19 |
| SELECTIVE_MISSING_DISAGREEMENTS | 1 | 1 | 1 | 1 |
| OPPOSING_CODERS | 0 | 0 | −1 | −16/65 |

观察一致率Po和校正偶然一致后的κ对边际组成反应不同。独立四分之一错误世界Po恒5/8，但κ由1/4降为32/275；完全对立编码世界Po恒0，但κ由−1变为−16/65。稀少正类的独立随机世界Po从25/32降为19/40，κ始终为0。ASymmetric世界κ由3/4升至16/19，不能把该变化解释成编码员实际质量改善，因为原编码函数及隐藏真值均未改变。

三个完整观察等价世界的所有权重条件结果保持完全一致，隐藏准确率仍分别1、0、3/4，不能用κ的权重稳定性识别内容真实。选择性缺失世界始终只有192/256=3/4原来源具有完整可见双编码；入选κ=1仍无法证明全源一致。

## B轨内部独立审计
B轨源码 [b_r240_s36_baseline_bigint_audit_20261028.js](../evidence_audit/b_r240_s36_baseline_bigint_audit_20261028.js) 仅读取原R240正式归档的2×2表，不读取2304行CSV或隐藏oracle；使用BigInt整数交叉乘法计算概率和κ，与R轨36条件逐格比对。实际完成372项程序性精确检查，失败0项。注入一个错误的加权单元计数后被拒绝。 [B机器审计收据](../evidence_audit/B_R240_S36_INDEPENDENT_AUDIT_RECEIPT_2026-10-28.json)。

上传后重新读取远端R/B源码、原CSV、原正式JSON和新增机器收据，在隔离V8环境实际调用两套上传代码的导出函数。R重新生成完整36条件结果与归档JSON逐字结构一致，B重新完成372项检查，失败0项，负对照成功。尚未运行GitHub Actions或完整Node.js命令行，不能声称CI成功或Node命令行验收。该B验证属于同项目内部不同算法的程序性复核，外部独立研究团队复现0项。

## 科学证据边界
本轮严格是E1有限人工观察分布敏感性，不能推断真实文本标签、真实编码者能力、真实历史材料效度、统计显著性或样本外预测。没有真实E2预测或历史E3预测。没有对R073或PESEN v0.1重新拟合。原R240的正式CI和结题文件保持原状态。下一主线可检查R241原始正式验收与R240后续是否存在未覆盖的多编码者缺失机制，先核对现有目录再决定下一项，避免重复。
