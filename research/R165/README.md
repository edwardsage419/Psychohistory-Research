# R165 文化中性漂变｜48组两文化类别随机复制、创新及固定时间

日期：2026年10月21日。原模型目录 **P1 / 07-007 Neutral Cultural Drift**。正式研究证据 **CLOSED_BOUNDED_E1**。本研究采用完全人工的两种文化符号A/B与固定人数小群体，用随机复制建立中性基线。未输入真实人名、考古陶器、技术专利或人口分布资料。

**一手原文核查：** [Hahn与Bentley2003](https://doi.org/10.1098/rsbl.2003.0045)提出新生儿姓名文化变化的随机复制与新名字创新模型；[Bentley、Hahn和Shennan2004](https://doi.org/10.1098/rspb.2004.2746)分析姓名、考古陶器和技术专利的文化变体分布。两个研究原作者处理多种文化类别与复杂的数据序列；本项目采用的**仅两种符号模型**无法复制该作者的多种文化变体的长尾排名分布。我们核对原始论文记录和摘要，未重新拟合或读取原历史样本。

**冻结数学试验：** 人工群体规模N取4、6、8；每个规模有四种事前指定的初始A人数；对称创新概率取0、1/16、1/8、1/4，共48组，各观察5期。所有人独立从前一期群体按出现频率复制一个A/B符号，同时以设定概率改为等概率选择A/B。使用两个完全独立的精确Fraction算法：二项式概率矩阵传播与穷举最多256种下一代个人选择配置。12套转移矩阵与全部48组×5期人数概率分布严格完全相等。

**长期数学结论：**
* 无创新时，全A和全B都是吸收态；期望A比例始终保持最初的A频率，但每次随机抽样使期望文化多样性乘以\(1-1/N\)，逐期衰减。
* 相同初始A比例1/2时，N=4的下一期频率方差是1/16，N=8则是1/32；群体越小，人工抽样波动越大。
* 对上述两种各半初始状态，通过有理数线性方程求出**预期进入全A或全B吸收状态的时间**：4人群体为132/29≈4.551724代；8人群体为738222218968/74653224767≈9.888685代。全部转移与吸收方程残差严格为零。
* 有正的对称创新概率时，两个端点不再吸收；存在唯一有限群体稳定分布，其平均A频率严格为1/2。创新为0时存在多种稳定分布，不能强行报告唯一稳态。
* 这些均是有限状态人工模型内的精确数学性质，不证明某种现实文化物品的流行是纯随机造成的。

**真实CI验证及仓库归档：** [首次run39530110643](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39530110643)、[固定哈希run39530175910](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39530175910)及[最终归档run39530202133](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39530202133)均success。Python3.11与3.12两个环境三次运行82种真实单测，独立归档任务额外执行82项，共574次执行、82种不同测试方法、0失败。四项文件SHA256一致，完整原始JSON及程序测试ZIP已永久提交[9b3d1dd](https://github.com/edwardsage419/Psychohistory-Research/commit/9b3d1dd56a91affa30cebfa825fd2e9352bd5a9b)。

正式资料：[事前冻结协议](../../protocols/R165_NEUTRAL_CULTURAL_DRIFT_48_MARKOV_INNOVATION_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交5963e3a）｜[完整科学报告](R165_SCIENTIFIC_REPORT_2026-10-21.md)｜[原生程序](r165_neutral_drift_exact.py)｜[82项测试](test_r165_neutral_drift_exact.py)｜[全量结果JSON](R165_EXACT_RESULTS.json)｜[原始源码与数据ZIP](R165_Neutral_Drift_48_Worlds_82_Tests.zip)｜[最终机器验收](R165_FINAL_MACHINE_ACCEPTANCE.json)。

SHA256：
* 程序 `33e480abee890329bc93d59877697df97dac577e766452caea63c617cddeea09`
* 测试 `214e0583fc1fff08b69869c3d3883c90322518710c6bb66a5cfd0b4f52d3250b`
* 全量JSON `826576f87f5c586e64d3d70861e876e665da90beac5fbd49948a8839639018b8`
* ZIP `771d60b9a01ad39851bef77382f1d8d7d4b380779d24c5cbaecf74565565b724`

进入 `research/R165` 执行 `python r165_neutral_drift_exact.py > R165_EXACT_RESULTS.json` 和 `python -m unittest -q test_r165_neutral_drift_exact.py`，仅需Python标准库。

**本阶段E1限定结题，新增E2=0、E3=0。** R073/PESEN v0.1保持冻结。下一原目录为 **R166 P1/07-008 Cultural Selection Models（文化选择模型）**，原目录存在一份前期原始文献记录R19，下一阶段优先审查该记录以避免重复研究。继续先完成既定全部R系列，再归纳分类，最后开始模型熔炼。
