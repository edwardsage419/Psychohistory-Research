# A轨：Kuper-Smith与Korn真人实验的正式Zenodo版本身份与R073冻结迁移硬门槛

日期：2026-10-26。状态：OFFICIAL_TAG_ARCHIVE_IDENTITY_VERIFIED / DIRECT_R073_FROZEN_TRANSFER_BLOCKED / DATA_LICENSE_PENDING。独立于原有A轨逐行镜像报告的新增来源与资格核验；本轮未重新执行33702行CSV的逐行分析。

## 本轮新核实的一手来源
英文正式论文 Kuper-Smith & Korn, *Loss avoidance during social interactions*, Communications Psychology (2025), DOI 10.1038/s44271-025-00288-5，发表2025-07-24。出版社Data availability明确指出全部数据在作者GitHub仓库以及Zenodo归档 https://zenodo.org/records/15667770 。Zenodo官方记录为2025-06-15发布的v2.0，资源类型Software，归档ZIP名 dnhi-lab/losses_gains_2x2-v2.0.zip，页面大小3.9 MB，MD5 82fdf1d671727c9aaba18b3b21f8a236。Zenodo页面的License字段**空白**，不能据此推定真人CSV的独立授权。

本轮通过GitHub原生Git ref接口读取作者tag v2.0，实际指向commit **345348cdc0018e8e030b05fb47dc845fd3e0d29a**，与本项目此前冻结的清洗CSV来源提交完全相同。原始清洗CSV blob ffd6776f3e9fd1444c84e50e4c61e3ff418a2488。tag和Git提交身份已核验，Zenodo ZIP原始字节未取得，因此Git源码与Zenodo压缩包的字节内容一致性仍为OPEN。仓库根MIT许可明确写Software及documentation，真人行为CSV文件层面许可仍需确认；论文正文CC BY 4.0不可自动延伸为所有外部仓库数据文件许可。

## 与R073冻结协议逐项核对
R073原冻结协议 protocols/R073_HUMAN_IPD_LAGGED_SOCIAL_MEMORY_LOSO_2026-10-17.md，Git blob 2f910c92436927f1488510af4ca98b665fa0d123：FP与SP两处理，每处理6个独立场次，每名参与者100轮，t3..100共98个评分目标，M0至M6共七模型，alpha=20固定，同处理5场训练和完整留出第六场，12场等权Brier/log loss。

候选实验2与3由作者字段程序 analysis/format_data_Exp_1_2_3.m（blob 6965e66ac05ec67b519f0674a708fcdcef917785）明确每人300次、5个60次区块；原A轨已核清洗实验2/3有16个六人组、26601条有向决策记录、12292个完整双人镜像事件、2017条无完整镜像的有向记录。第25/26列是本轮自己与对手行为，30/31列是上一**全局试次**的自己与当时对手行为。前次可观察反馈已有33177项逐行核验，二阶滞后未由作者单独给出；不能直接用清洗后相邻行代替前两次合法试次。

候选资料未提供R073冻结FP/SP处理标签，300轮与冻结100轮目标宇宙不同，16个实验组与原12场、每处理6场的分层训练规则没有等价映射。把300轮截成100轮、任意重标FP/SP或改为跨处理训练，都会改变原R073冻结评分定义。**当前直接套用R073原冻结评分的资格为BLOCKED**。这不妨碍未来在独立新协议下进行另一个明确标注的真人E2探索性预测；任何新协议必须先于新评分冻结，不能冒充原R073的同口径零改动复验。

## 本轮数据登记与下一关口
结构来源仍采用此前已完成的33702行真实逐行审计，不将本轮来源身份核验记为重新执行真人评分。新登记JSON：research/data_scout/KUPER_SMITH_KORN_V2_TAG_ZENODO_R073_COMPATIBILITY_GATE_2026-10-26.json，包含11项逐项门槛及状态。

后续仅在无费用且许可允许的前提下，核实Zenodo压缩包的真实MD5与Git树对应文件、取得明确真人CSV使用授权，随后决定是否立项**新的**事前冻结跨实验协议。保持R073七模型、原alpha、原评分规则不变。新增真人预测E2=0、历史E3=0、外部团队独立复现=0。未主动启动Actions或购买资源；账户账单未核验。
