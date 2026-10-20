# R145｜隐藏努力、激励契约与监督信息价值

2026-10-20。原模型目录 **P2/06-003 Principal Agent Models**。

实际核阅 Holmström (1979) 原刊p74、76、81–84（Bell Journal of Economics 10:74–91；DOI 10.2307/3003320）：隐藏行动IC与参与IR、监督信息是否含条件增量的判断及其边界。Grossman–Hart (1983) *An Analysis of the Principal–Agent Problem*, Econometrica 51:7–45 DOI 10.2307/1912246 核对原作者Harvard书目及论文摘要、方法来源；未取得可逐页检验的作者全文PDF，不能冒充真正逐页复算。

严格数学：项目自设代理人$U(w)=\sqrt{w}$，不可观察高努力概率(成功3/4,失败1/4)、努力效用成本1/4，代理人保留效用1/2。弱IC及IR下的**最小期望工资成本**：
- 无监控：$39/64$；
- 条件冗余的四状态信号：$39/64$；
- 真正含额外努力信息的四状态信号：$5505/9104$；
- 严格可证节约$171/36416$，却小于冻定最低非零监督费1/64，故本例若需按给定收费购买监督则不值得购买。
- 努力成本0时，监督信息的效用恰为0；若产出分布对H/L完全相同且努力成本>0，隐蔽高努力合同不可实现。
- 最优工资是**弱IC**，代理人严格无差异时需另行假定选择H，不能声称无条件严格执行。

全部源、测试与审计：
- [预先冻结数学协议](../../protocols/R145_HOLMSTROM1979_GROSSMAN_HART1983_MORAL_HAZARD_FINITE_SIGNAL_EXACT_PRESCORE_FREEZE_2026-10-20.md)
- [一手文献核验及科学报告](R145_HOLMSTROM1979_GROSSMANHART1983_INFORMATIVENESS_CONVEX_CONTRACT_SCIENTIFIC_REPORT_2026-10-20.md)
- [完整程序、88项unittest及源机器JSON ZIP](R145_Holmstrom_GrossmanHart_88_Tests.zip)
- [正式科研状态](R145_FINAL_ACCEPTANCE_STATUS.json)
- [远端CI](../../.github/workflows/r145-holmstrom-grossman-hart-88-tests.yml)

ZIP解压同目录后：`python -m unittest -q test_r145_principal_agent_exact.py`；`python r145_principal_agent_exact.py > replay.json`。整数和Fraction精确KKT证书、24次状态置换求解，全部依赖Python标准库。本期为**自行构造E1数学检验**，不属于1983作者原模型完整重演，新增真人E2=0、历史E3=0。R073/PESEN v0.1冻结，按先全部R完成、再归纳分类、最后熔炼的顺序。

**已完成双环境真实CI**：[GitHub Actions run 39400383682](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39400383682)。初始源码commit `8381e2740df592523f26546b69f8475dd2ebb910`；Python3.11 job118553322996执行88 tests in 0.388s；Python3.12 job118553323410执行88 tests in 0.216s，实际合计176次，0失败。两环境分别完成ZIP与原程序、原测试、原结果4份SHA256校验，全部合同优化和KKT测试通过，并逐字节重算原始JSON。归档独立收据：[R145_PHASE_A_176_TESTS_4_KKT_CONTRACTS_GITHUB_CI_RECEIPT.json](R145_PHASE_A_176_TESTS_4_KKT_CONTRACTS_GITHUB_CI_RECEIPT.json)，正式科学状态已更新为CLOSED_BOUNDED。所有计算均为人工E1，没有实地合同因果证据。
