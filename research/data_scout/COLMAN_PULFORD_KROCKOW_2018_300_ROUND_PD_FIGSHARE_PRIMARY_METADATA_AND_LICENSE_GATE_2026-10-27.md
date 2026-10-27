# A轨：Colman、Pulford与Krockow 2018年300轮真人囚徒困境数据候选资格核验

日期：2026-10-27。状态：PRIMARY_PUBLIC_METADATA_VERIFIED_BINARY_AND_LICENSE_GATE_OPEN。仅公开英文来源。主动新增费用0。

## 来源及独立性
正式论文：Colman, A. M., Pulford, B. D., and Krockow, E. M. (2018), *Persistent cooperation and gender differences in repeated Prisoner's Dilemma games: Some things never change*, Acta Psychologica 187, 1–8，DOI https://doi.org/10.1016/j.actpsy.2018.04.014 。PubMed https://pubmed.ncbi.nlm.nih.gov/29727770/ 记录2018年5月2日线上发表。作者报告真人两人囚徒困境连续300轮、已知终点的有限期实验；论文比较常规和较温和的两种收益条件，讨论期末行为。该实验作者、年代与R073的Montero-Porras 2022实验不同，值得作为独立实验候选；尚未通过数据层面确认参与者或场次是否完全无重叠。

原作者关联的英国莱斯特大学Figshare公开记录： https://figshare.le.ac.uk/articles/dataset/Repeated_Prisoner_s_Dilemma_Dataset/10194938 。页面标注2017年9月14日发布、作者三人同名、关联同题论文，公开下载包标示185.25 KB。已实际打开记录及下载链接；尝试访问 `https://figshare.le.ac.uk/ndownloader/articles/10194938/versions/1`，当前网络工具未取得二进制文件，无法读取任何原始数据行或文件名。

## 时间、行为、身份与许可
论文明确是两人重复博弈、300轮且参与者每轮获得双方行动及收益反馈；这些信息来自论文描述，尚未从数据文件核验。公开元数据没有暴露数据表头、被试匿名ID、固定配对ID、实验场次ID、轮次编码、缺失值及行动C/D字段。样本量、每个收益条件的独立场次数和原始行为总行数仍未从可核验数据取得。不得将300轮直接乘以未经核实的人数宣称实际记录量。

Figshare页面许可明确为 **All Rights Reserved**，并未提供CC BY或CC0等开放再分发授权。论文PubMed页版权同样注明Elsevier All Rights Reserved。当前只保存研究引用和资格审计，不下载非公开私人数据、不将原始记录复制到GitHub、不假定有再分发权。网页可访问和数据可合法再分发是两个不同检查门。

## R073冻结协议适配
已重新读取 `protocols/R073_HUMAN_IPD_LAGGED_SOCIAL_MEMORY_LOSO_2026-10-17.md`（Git blob `2f910c92436927f1488510af4ca98b665fa0d123`）。原协议针对Montero 2022的FP6/SP6共12个实验场次、每人100轮、t=3..100共同目标、同处理其余5场训练、场次等权，平滑alpha=20及7个固定模型。Colman的300轮、不同收益处理和未知场次结构不能直接替换原R073数据或照搬12折权重。若未来取得可用原始行，只允许先完成原始场次身份、双人配对镜像、时间戳、收益条件、许可证及数据独立性核验；任何跨实验冻结迁移评价需另行在评分前公开独立协议，不能在看到测试标签后选择截取100轮或重调模型。

## 实际阻塞及下一步
二进制下载未成功；文件名、字段、样本与场次未知；All Rights Reserved许可需要明确可用范围；独立来源去重尚未完成。当前候选优先级为高，资格为 `CANDIDATE_UNVERIFIED`，R073第二独立真人冻结评价资格仍为NO。新增E2=0、E3=0、外部独立复现=0。

核验英文来源：
1. https://figshare.le.ac.uk/articles/dataset/Repeated_Prisoner_s_Dilemma_Dataset/10194938
2. https://pubmed.ncbi.nlm.nih.gov/29727770/
3. https://doi.org/10.1016/j.actpsy.2018.04.014
