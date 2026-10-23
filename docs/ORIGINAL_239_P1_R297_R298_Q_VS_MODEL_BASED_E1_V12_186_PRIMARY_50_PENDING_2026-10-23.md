# 心理史学：原239目录R297 Q-Learning 与R298模型式规划分别进行的E1有限研究，v1.2来源验收

日期2026-10-23 Asia/Taipei。本轮沿既定「完成全部R→统一归纳分类→模型熔炼」顺序处理原目录02-003、02-004两种不同机制。两者正式科研边界都仅是**有限人工精确数学 E1**，当前没有新增真人/动物E2，也没有历史E3，原始239整体科学结题**NOT_ESTABLISHED**。

## 两项研究、先行冻结及真实CI

| 项目与原目录编号 | 事前冻结提交 | 完整人工原source | 双Python主模型unit tests | 三job结果 |
|---|---|---:|---:|---|
| R297 Watkins–Dayan Q-learning，02-003 P1 | [fd66badd](https://github.com/edwardsage419/Psychohistory-Research/commit/fd66badd5a110b36cc97564f7e1a29daba4298ba) | 120 Q向量源行（24世界×5轮） | 611×2 | [39924889538](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39924889538) SUCCESS |
| R298 已知模型式规划与再估值，02-004 P1 | [24cdb311](https://github.com/edwardsage419/Psychohistory-Research/commit/24cdb3119991c7233ee02fdad271d74881ab8825) | 64行动源行（32世界×2动作） | 269×2 | [39925393352](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39925393352) SUCCESS |

R297 [科学报告](../research/R297/R297_SCIENTIFIC_REPORT_2026-10-23.md)和[机读验收](../research/R297/R297_FINAL_ACCEPTANCE_STATUS.json)：原著Watkins & Dayan 1992 *Q-learning*, DOI https://doi.org/10.1007/BF00992698。构造含S0安全与探索、S1高/低奖励及终止T的有限确定性人工MDP。折扣γ、步长α、高奖动作是否可观察，以及MAX自举/固定BAD行为自举组成24配置，120完整Q向量；4轮后γ=α=1/2且完整覆盖使用MAX得Q安全=15/16、Q探索=39/32、Q后继好动作=45/16，选择探索。和人工完整最优自由行动对照总24中12一致、12不一致。**固定BAD行为备份和自由行动最优控制目标不同**，不能把前者相对最优自由控制的偏差称为其自身政策回报差；4轮有限学习不能证明Watkins–Dayan原论文的随机渐近收敛定理。真正E2/E3均为0，原R063社会模仿学习机制、R073真实重复博弈冻结协议不改。

R298 [科学报告](../research/R298/R298_SCIENTIFIC_REPORT_2026-10-23.md)和[机读验收](../research/R298/R298_FINAL_ACCEPTANCE_STATUS.json)：Sutton1990 Dyna规划与模型更新第一手 DOI https://doi.org/10.1016/B978-1-55860-141-3.50030-4；Daw等模型式/无模型式对照 DOI https://doi.org/10.1038/nn1560 与 https://doi.org/10.1016/j.neuron.2011.02.027。人为构造两步双动作环境，测试奖励变更、转移变更、同时变更、未变更，以及折扣γ、准确外部信息是否通知、是否重规划/保持旧价值。32配置64原source，收到准确信息的已知模型规划器8/8最优；没收到信息的规划器、收到通知但不更新的缓存控制器、没通知缓存控制器均4/8；总32中20最优、12偏离。同时改变奖励与转移却保持原先动作最优，是对「一有环境变化就必须变选择」的精确负对照。**本研究没有从试次中学习转移模型、没有运行Sutton全Dyna-Q、没有拟合Daw人类fMRI数据**。真E2/E3仍0。

以上仅是研究者预先设置的人工模型参数网格，全部比例都不能解释为人类决策正确率或学习错误率。两研究共**184条不同人工来源行**、双Python主数学模型unittest总计(611+269)×2=**1760**通过。另各有完全独立、不导入主程序的源级逆向审计分别16、17项，且第三job重新核对原CSV、结果JSON和SHA256，所有原数据永久归档GitHub主分支：[R297 6d3b0496](https://github.com/edwardsage419/Psychohistory-Research/commit/6d3b0496111d58c03983941480398c1fd4bff85f)；[R298 bea6bf4f](https://github.com/edwardsage419/Psychohistory-Research/commit/bea6bf4f6b3b95db05b2ba1efe5f9d96fa4d2794)。

## 239原目录证据来源v1.0→v1.1→v1.2

| 目录来源分类 | v1.0 R296后 | v1.1 R297后 | v1.2 R298后 |
|---|---:|---:|---:|
| 已找到原候选主R来源关联 | 184 | 185 | **186** |
| 共享数学之前模型，不当作独立E2 | 3 | 3 | **3** |
| 旧资料只有范围有限关联 | 5 | 5 | **5** |
| 已检查资料里无逐条源链接 | 47 | 46 | **45** |
| 尚缺确认候选主R关联 | 52 | 51 | **50** |
| 原始模型唯一候选总数 | 239 | 239 | **239** |

[当前v1.2完整239行证据交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.2_2026-10-23.json)相对[v1.1](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.1_2026-10-23.json)仅02-004一行有新R298 E1来源关联；v1.1相对v1.0只增加02-003一行R297。**这些是有科研来源的R链接，不是186个原论文已经独立实证复现。**

[当前剩余50项P1/P2待核目录](ORIGINAL_239_PENDING_50_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)，其中P1=23、P2=27；下一个是**02-005 Model Free Reinforcement Learning**。它旧有R063对社会模仿强化学习作者源码的范围有限证据，跨到更一般的无模型RL必须重新核对真实研究对象和模型等价，不能偷换成R297已结题或再次计算同一实证实验。

GitHub原239目录独立元数据与来源哈希审计：[R297 v1.1代码](../research/catalogue_audit/verify_p1_r297_crosswalk_v1_1.py)，[run39925138650](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39925138650)三job成功；[R298 v1.2代码](../research/catalogue_audit/verify_p1_r298_crosswalk_v1_2.py)，[run39925750483](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39925750483)三job成功。两版均查原始239个ID、名称、优先级、变更仅一项、真实Git blob SHA、原source和结果SHA256、未向真人E2升格。资料完整性与理论的真实预测效果始终分别验收。

研究顺序不变，先补充R系列；R073/PESEN v0.1保持冻结；个人辅助决策工具继续暂缓。
