# R161 符合偏向传承｜48组有限群体随机复制与吸收概率精确验证

日期：2026年10月21日。原目录 **P1 / 07-003 Conformist Transmission**。**CLOSED_BOUNDED_E1**，采用完全人工的5人和7人文化A/B复制概率模型。完全没有真实群体成员、文化行为记录、实验选择数据、群体适应度或历史社会事件的外部验证。

原刊核对：[Boyd与Richerson1985芝加哥大学出版社原书第7章目录](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html)、[Henrich与Boyd1998原出版方摘要](https://www.sciencedirect.com/science/article/pii/S109051389800018X)以及[Efferson等2008原期刊实证摘要](https://www.sciencedirect.com/science/article/pii/S1090513807000876)。后者区分一般跟随多数与加强多数频率的真正符合性，同时报告了学习策略的个体异质性。本阶段未获取或重新拟合原始真人实验记录，也未复制这些原作者的完整方程。

**设计：** 群体人数5或7；各6种冻结初始A人数；4种符合模仿强度h，合计48组，每组完整保存从t0至t4的A人数分布。下一代每名新成员以概率\(q(k;h)=(1-h)k/N+h[3(k/N)^2-2(k/N)^3]\)独立选择A，因此下一代人数按项目自建二项式条件过程取值。**两套独立完全有理数算法**（直接二项式系数和完整穷举2^N种下一代配置）在全部48组、所有时间点的每个概率单元均完全一致。

**长期吸收概率：** k=0与k=N在没有创新的人工模型中为吸收态。使用Fraction高斯消元求得所有未来最终固定为A的精确概率，并独立核验所有马尔可夫调和方程。随机无偏模仿h=0时，最终固定为A的概率等于初始A频率k/N。当N=5,h=1时，初始只有1名A最终全A的概率约0.04491958，初始有4名A最终全A的概率约0.95508042。所有结果属于模型生成的假想长期分布，不能解释为真实人群行为概率。

**有限与无限群体的区别：** N=5、初始2人A、h=1时第一期条件期望频率44/125=0.352。第二期经完整随机马尔可夫分布求得A的期望频率\(15605084/48828125=0.31959212032\)，连续使用两次确定性均值模型却得到\(555632/1953125=0.284483584\)，差值约0.03510853632。有限群体随机性与非线性模仿不可简单互换。无偏模仿虽然每代期望A频率不变，真实随机分布仍会逐渐分散到边界。

**正式远程验证：** [首次CI 39525830737](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39525830737)与[最终固定SHA256及永久归档CI 39525915174](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39525915174)均成功。Python3.11和3.12每轮各运行78项真正的测试方法，归档任务又运行78项，总共390次真实测试执行，78种不同方法，0失败。全量JSON及源码测试ZIP永久写入GitHub main：[归档提交e13324a](https://github.com/edwardsage419/Psychohistory-Research/commit/e13324aa0f82bbd39f8370b1b4a4e55f9cf8edcf)。

完整材料：[计算前冻结协议](../../protocols/R161_FINITE_CONFORMITY_48_MARKOV_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交e0d590f）｜[科学报告](R161_SCIENTIFIC_REPORT_2026-10-21.md)｜[源码](r161_finite_conformist_markov.py)｜[78项测试](test_r161_finite_conformist_markov.py)｜[完整JSON](R161_EXACT_RESULTS.json)｜[标准库源码与数据ZIP](R161_Conformity_48_Finite_Worlds_78_Tests.zip)｜[机器验收记录](R161_FINAL_MACHINE_ACCEPTANCE.json)。

固定四项SHA256：
* 源码 `744026427340efd9addba636d36fdefd65e94604f40678563e5b9995eccb2f21`
* 测试 `ee6b29e5bd404fde7cdd692ce2b348f0fe056cdaf839f24b9a0740c39971f699`
* JSON `8cba0edf39013a0bb8dd694e00b00f38cae20fd5473e46c7f0b0a6474232d5af`
* ZIP `dfd9483ca9f98f9fd07f671918b2074a846642d13e8dc17e4366fd35397ee766`

进入 `research/R161`，执行 `python r161_finite_conformist_markov.py > R161_EXACT_RESULTS.json`，以及 `python -m unittest -q test_r161_finite_conformist_markov.py`，仅需Python标准库。

**本阶段新增E2=0、E3=0**。R073/PESEN v0.1不变。下一原目录 **R162 P2/07-004 Prestige Biased Social Learning（声望偏向学习）**；全R系列完成后再统一分类，最后进行模型熔炼。
