# A轨：DfE-DB公开仓库的行为数据可获得性审计

UTC日期：2026-10-30。目标键：(A,DfE-DB,github-main-2026-10-30,public-raw-trial-access-and-R073-gate)。与既有DF2011/R074、Montero/R073及NV_games来源不同，未开展数据合并或重复计分。

## 公开来源与实际读取

官方作者仓库 https://github.com/dwulff/DfE-DB ，公开预印本 https://doi.org/10.64898/2025.12.12.693971 。仓库README明确声称研究汇总约380万次真实人类选择、11921名参与者、168项研究、13类任务，以上为作者汇总声称，**本轮未获取逐试次数据，不能视作实际核验的原始记录**。

通过GitHub连接器实时读取官方仓库README Git blob 383f0480dc27e3d14c38a584621d4ca42741363a、LICENSE.txt（CC BY-SA 4.0文本）、data目录，以及两个示例研究子目录。README明确说明数据当前只向数据提供者开放，待文章接受后才公开。公开data/AK2011目录当前仅有README.md（blob 682edda2d409a14869c8665e57525f2915ae93e4）和AK2011_processing_code.R（blob d6c5f8e19f948bf58f5da252d503dc34c8de5f3b）。data/DBDF2016当前仅有README.md（blob 0452d7fa083e6361ed739b681a16a1cba7dcb90b）和DBDF2016_processing_code.R（blob db809f21f103e2ff76c347c333d72b4aa2ceb1b8）。两个公开示例目录都不存在raw或processed子目录，直接访问返回404。

README介绍未来标准化字段包括研究、受试者ID、问题ID、条件、试次序号、行动选择及反馈；本轮只核验字段说明，**没有核验任何数据行或真实可用字段**。AK2011 README还登记部分研究缺原始数据。该仓库的CC BY-SA文本不能自动证明尚未公开的原始受试者数据已经授权公开。

## 资格结论与下次触发条件

DATASET_DISCOVERY=CONFIRMED；PUBLIC_METADATA_AND_PROCESSING_CODE=CONFIRMED；PUBLIC_TRIAL_LEVEL_RAW_OR_PROCESSED_ACCESS=BLOCKED_BY_CURRENT_RELEASE_POLICY。由于无法合法获得公开试次数据，本轮不尝试访问非公开部分、联系申请受限数据、注册账户或下载付费资源。参与者级独立身份、实验场次、反馈时间单位、R073要求的固定百轮双人同伴连续行动记录及实际数据许可均NOT_VERIFIED。不能把作者所称的380万选择计作本项目E2数据验证。

R073_SECOND_DATASET=NOT_QUALIFIED，原因是公开试次不可得且百轮双人同伴结构未验证。未来只有作者正式公开可访问的原始/处理后逐行数据、明确许可及身份/场次结构时才重新开启来源验证。无新增真人E2预测、历史E3预测、收费操作。

英文第一手来源：
https://github.com/dwulff/DfE-DB/blob/main/README.md
https://github.com/dwulff/DfE-DB/tree/main/data/AK2011
https://github.com/dwulff/DfE-DB/tree/main/data/DBDF2016
https://github.com/dwulff/DfE-DB/blob/main/LICENSE.txt
