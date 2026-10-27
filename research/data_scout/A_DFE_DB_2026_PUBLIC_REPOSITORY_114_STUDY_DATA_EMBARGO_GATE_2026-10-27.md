# A轨 DfE-DB 公开元数据与原始行为数据访问资格审计

日期：2026-10-27。候选：Yang, Spektor, Thoma, Hertwig and Wulff, Decisions-from-Experience Database (DfE-DB), bioRxiv DOI 10.64898/2025.12.12.693971。作者公开仓库 https://github.com/dwulff/DfE-DB，读取main固定HEAD `a45c00224bf59a617f88574f4f7e3dc6bfd95b3b`。本次仅访问公开英文文档与仓库树，不登录、购买或获取私人数据。

## 真实访问检查

作者README声称数据库涵盖168项研究、11921名参与者、约380万条试次决策和13类任务，并明确写明“data is currently made available to data providers and will be shared openly upon article acceptance”。这些数字为作者描述，未从真实行记录复核。

实际调用GitHub递归Git树，结果truncated=false，包含361个树条目；在data目录下确认114个论文文件夹。对整个data子树检查得到raw/和processed/目录内公开文件0项、CSV文件0项。抽查`data/AK2011`和`data/BE1998`仅有README与处理R代码；AK2011 README还明确写出“no raw data”。所以当前公开仓库确实未发布可逐行验证的处理后或原始真人决策表，不能按作者汇总数声称本轮已经读取380万行。

README描述计划统一的字段包括paper、study、subject、problem、options、trial、choice、feedback，以及选项结果概率；这些只是代码本级定义。时间单位为试次trial，跨研究的任务设计与试次间隔可能不同。研究/参与者/任务ID可用于未来候选独立分组，但当前没有可核验的实际身份和试次表。README中含战略决策任务，并不意味着它可直接用于R073双人重复囚徒困境100轮冻结评分。

## 许可与结论

仓库LICENSE.txt Git blob `2d58298e6eda10e7204abb52722efbc840db2390` 为Creative Commons Attribution-ShareAlike 4.0 International。公开仓库代码与文档许可不能自动推定未来每项原始实验数据的再分发授权；作者README还说明只有获许可时才提供原始数据。

资格判定：PUBLIC_METADATA_VERIFIED / PUBLIC_ROW_DATA_BLOCKED / R073_FROZEN_SCORING_NOT_ELIGIBLE。实际逐行行为=0，实际独立参与者/场次=未核，原始许可=逐研究待核，新增真人E2评分=0。复现难度目前为阻塞，未来作者公开数据后需先按论文、研究和参与者去重、检查时间泄漏与样本外分组，再冻结具体研究协议。无新增费用。
