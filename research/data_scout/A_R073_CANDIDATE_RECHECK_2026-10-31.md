# A轨：R073独立真人百轮数据候选重新核查与阻塞记录

UTC 2026-10-30。只查英文公开来源，不访问非公开个人资料，不购买数据，不注册付费账户。本次仅做来源及可用性审计，E2新增0。

Leicester Figshare的Repeated Prisoner's Dilemma Dataset页面 https://figshare.le.ac.uk/articles/dataset/Repeated_Prisoner_s_Dilemma_Dataset/10194938 实际核实2017-09-14公开、185.25kB下载入口、All Rights Reserved许可。实际访问 https://figshare.le.ac.uk/ndownloader/articles/10194938/versions/1 ，网页工具报400 Unsupported content-type application/zip；本地网络下载失败。原始ZIP字节、字段、参与者身份、逐轮行动、场次及SHA尚未核验。状态 RAW_BLOCKED_RIGHTS_REVIEW_PENDING。

Mao等（2017）论文 https://pmc.ncbi.nlm.nih.gov/articles/PMC5241863/ 实读方法：94名完成者，20个工作日，最多400个独立10轮囚徒困境游戏；每轮结束可见对方行动，游戏之间重新随机配对。原始数据指向 https://osf.io/64z8u/ ，访问403。原作者实验代码仓库 https://github.com/TurkServer/long-run-cooperation 可读取，仓库树没有可替代OSF原始行为CSV。连续配对每场只有10轮，不能把400场拼成100轮固定双人互动。R097和此前A轨已研究此来源，本轮按原来源身份去重，不重复作为新E2。

公开100轮模拟仓库 https://github.com/jb-githubuser/prisonersDilemma_Simulation 明确是机器策略对战；Zenodo https://zenodo.org/records/10246247 的迭代囚徒困境锦标赛也是机器生成。两者不符合真人E2数据门。先前A轨已有机器模拟排除记录。

本轮重新核查后，未新增满足R073冻结条件的独立100轮真人连续双人互动数据。下一步仍需合法获取Figshare原始文件，逐项核对身份、对手历史、逐轮时间与使用许可。OSF访问恢复后核对每场游戏边界，不跨对手拼接长序列。R073模型和评分规则保持冻结。E2=0，E3=0。
