# A 公开数据侦察：Fudenberg 与 Pathak 2010 真人公共品惩罚实验

日期：2026-10-24。状态：**PUBLIC_SOURCE_BYTES_AND_STRUCTURE_VERIFIED; LICENSE_UNRESOLVED; R073_EXTERNAL_REPLICATION_INCOMPATIBLE**。

## 来源与第一手文献

Drew Fudenberg and Parag A. Pathak (2010), *Unobserved Punishment Supports Cooperation*, *Journal of Public Economics* 94(1–2):78–86，DOI 10.1016/j.jpubeco.2009.10.007。MIT 作者托管原论文：https://economics.mit.edu/sites/default/files/inline-files/Unobserved%20punishment%20supports%20cooperation.pdf 。

原作者相关公开复现仓库：https://github.com/MIT-Blueprint-Labs/unobserved_punishment ，固定提交 `f8d3760c954a8757ab16ac5c2f7a1c69d2517898`。复现说明 `Readme.txt` blob `58d10e9d34d49a808b84801ab2c08364c6698c73`。原始 SAS 清洗脚本 `code/clean.sas` blob `32058daccde6d2da013e79cb7c359409cdbb2d79`。已公开的清洗 CSV `clean_data/unobserved_dataset.csv` Git blob SHA1 **`f5767dd72928b16eaa30c8cc67af15b17ad25d4c`**，177144 字节。

此数据属于真人公共品贡献与惩罚的多期实验，**并非** R073 所需的双人重复囚徒困境。不得把它转换成 R073 的第二次独立预测检验。可在未来单独冻结制度激励与合作行为的 E2 协议。

## 实际原始 CSV 核验

已通过 GitHub 连接器读取完整 UTF-8 CSV，再由公开仓库标准 Ubuntu GitHub Actions 重新下载固定提交并执行独立 Python CSV 审计。验证结果：**2400 行，28 列，6 个 session，132 个 session+subject 键，600 个 session+period+group 单元，全部每组每期 4 人**。每个 `session,period,subject` 键唯一，2 个预设篡改负例均被拒绝。

| session | 行数 | 当场参与者数 | 期数 |
|:---|---:|---:|---:|
| C1 | 240 | 24 | 10 |
| C2 | 400 | 20 | 20 |
| T1 | 480 | 24 | 20 |
| T2 | 480 | 24 | 20 |
| T3 | 400 | 20 | 20 |
| T4 | 400 | 20 | 20 |

字段包括 `period,subject,group,session,contrib,profit,received,reduction,pun1,pun2,pun3,opp1,opp2,opp3,con1,con2,con3,base,punish,set,mod_period` 等。数值 subject 标签 1 至 24 在多个 session 重用，**跨 session 同号不构成同一个人的证据**。未来应以 `session+subject` 为最小个体标识，并以完整 session 为独立留出候选；同一 session 内的组与个体依赖必须保留。原始论文的实验分配和每一处理条件的 session 数量需要进一步核实，不能将 6 个 session 自动视为 6 个独立处理重复。

## 许可、风险和后续复现门槛

公开复现仓库的文件列表没有明确 LICENSE，复现 README 也没有给出原始数据再分发许可。MIT 论文手稿页面的 CC BY-NC-SA 3.0 只说明其手稿的使用条款，**不能直接推定 CSV 采用相同许可**。本项目没有把 2400 行数据复制到自己的仓库，暂不再分发。许可状态为 **UNRESOLVED**。

README 明确提示论文 Table 4 第五列的已发表估计与复现包输出不同，后续任何实证验收必须单独处理此差异。当前没有重新运行 SAS/Stata 全部作者估计，也没有新建模型或进行样本外预测。

可重放审计源码：`research/data_scout/audit_fudenberg_pathak_public_goods_csv.py`。公开 CI：`https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40071764071`，提交 `e3e7aa9899960ce50a9a211bccabb52b82842f5e`，作业 `120806532006` completed/success，已读取完整结构统计日志。CI 仅下载至临时目录，不上传数据或缓存。公共标准 runner 免费。

FRD2012 真人重复囚徒困境的优先侦察仍开放：RDA 二进制无法通过当前 GitHub 连接器解码；超博弈 `game` 不能当独立实验 session；其 `data.FRD2012` 衍生版本增加 `input` 字段，需区分原始 9 列与派生 10 列。不得对 R073 事后调参。

本项新增 E2 预测成绩 **0**，E3 **0**。完成的是**公开真人数据源的来源与结构核验**，不等于实证模型验收。
