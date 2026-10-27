# A轨 Friedman与Oprea 2012 实验的外部文献复现线索及数据许可阻塞

日期：2026-10-27（Asia/Singapore）。本报告补充此前 [原始数据访问审计](FRIEDMAN_OPREA_2012_CONTINUOUS_DILEMMA_OPENICPSR_SOURCE_AND_ACCESS_GATE_2026-10-27.md)，不新增真人行为评分，不重复登记为新的独立数据集。

## 本轮实际核验的英文来源

1. 原始期刊 American Economic Review 2012，Friedman and Oprea, A Continuous Dilemma，DOI 10.1257/aer.102.1.337，官方 https://pubs.aeaweb.org/doi/10.1257/aer.102.1.337 。实验连续时间60秒，含八个离散子期等对照。
2. 原始数据正式存档 openICPSR E112495V1，2019-10-11，https://www.openicpsr.org/openicpsr/project/112495/version/V1/view 。公开目录可见 LICENSE.txt，14.6 KB，单文件页面 https://www.openicpsr.org/openicpsr/project/112495/version/V1/view?path=%2Fpcms%2Fprojects%2F1%2F1%2F2%2F4%2F112495%2FV1.0.1%2FLICENSE.txt&type=file 。本轮实际尝试从许可文件页点击下载，官方跳转ICPSR账户登录，无法读取许可正文；按零新增费用和不注册要求停止。
3. FORRT FLORA Replication Atlas 对该研究的记录 https://forrt.org/flora-replication-atlas/doi/10.1257/aer.102.1.337/ ，显示Camerer等2016 Science 研究曾复现原论文的某一预指定显著性结果，数据库将其标记successful。该判断依据Camerer等补充材料Table S1的二级登记，本轮未成功取得该表的原始PDF逐行核验。
4. Camerer等2016原始同行评议研究 DOI 10.1126/science.aaf0918，Caltech作者馆藏 https://authors.library.caltech.edu/records/gr9cr-qjb08 ，2016-03-25。其总体18项经济实验复现中11项满足原研究方向显著性标准；不能将总体成功率当作Friedman与Oprea的效应大小或全部结论复现。馆藏列有原始补充PDF，但本轮PDF下载重定向不可访问。原论文明确列出OSF原始研究资料索引 https://osf.io/bzm54 ，本轮未取得其中本实验原始逐行行为数据。

## 科学范围与复现准备结论

文献层面新增一个外部已发表复现线索，登记为 EXTERNAL_PAPER_RESULT_REPLICATION_SECONDARY_INDEX_ONLY。该复现测试的是原论文的一项显著性方向结论，与心理史学R073冻结的历史行为特征样本外概率评分属于不同研究命题。不能计为本项目外部独立复现，亦不能计为R073第二真人实验验证。

本轮实际核验许可文件在官方目录存在且单文件下载跳转登录。许可正文未取得，故 LICENSE_TEXT_BLOCKED_LOGIN，RAW_CSV_BYTES_BLOCKED_LOGIN，SESSION_DYAD_FIELDS_UNVERIFIED，R073_DIRECT_FROZEN_TRANSFER_BLOCKED。公开目录和第三方复现索引均无法替代原始逐行字段、独立实验场次、身份、时间语义及许可审查。下一次A轨优先寻找无需登录即可直接读取的原始二元重复博弈逐轮CSV，保持R073模型和评分冻结。新增E2预测0、E3预测0、费用0。
