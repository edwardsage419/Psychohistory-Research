# C017 Schmid 与 Yang（2022）开放 HTML 似然公式符号审计

track: theory
subflow: C
run_date: 2026-11-12 (Asia/Singapore)
observed_head: 8d082fa3918281d88a9f4d1ed7ac81bea817fcfc
target_key: (theory-C,SchmidYang2022,doi:10.1162/99608f92.3f1772ce,HTML_section_3_2_likelihood_sign_and_AR1_joint_density)
status: PARTIAL
source_links:
  - https://hdsr.mitpress.mit.edu/pub/b6efwlql/release/1
  - https://doi.org/10.1162/99608f92.3f1772ce
source_access: 正式开放 HTML 原文第2.3节及第3.2节，2026-11-12 直接核读；PDF 下载入口存在，未完成 PDF 版本对照。
work_performed: 对原文第3.2节未编号似然及式(3.3)作正态密度符号和相关性结构检查。
evidence_scope: 原文 HTML 的排版/数学表达与条件性代数审计；未核实出版 PDF、作者勘误或实现代码。

## 直接观察与独立推导

Schmid 与 Yang (2022), *Bayesian Models for N-of-1 Trials*, Harvard Data Science Review, DOI 10.1162/99608f92.3f1772ce。第2.3节式(2.5)设 e_j=rho_e e_(j-1)+epsilon_j，epsilon_j 独立 N(0,sigma²)，并给出平稳边际方差 v=sigma²/(1-rho_e²)。第3.2节 HTML 中的似然及随后式(3.3)显示 exp[+(y_j-M_j)²/(2v)]，指数前缺少负号，分母还省略正态密度常数。

在仅有独立 N(M_j,v) 观测的条件下，正确的密度乘积应正比于 v^(-J/2) exp[-sum_j (y_j-M_j)²/(2v)]。HTML 中正号若照字面使用，则在固定 v>0 时随残差绝对值增大而无界增大，积分无法归一化为概率密度。这是可独立证明的符号问题，不能据此断言作者实际分析代码采用了该错误。

另一个独立边界：若按第2.3节的 AR(1) 误差生成过程建模且 rho_e 非零，观测的联合密度通常不能直接写成平稳边际密度的乘积。正确的平稳 AR(1) 联合密度可分解为 p(e_1) 乘以 j>=2 的 p(e_j|e_(j-1))；后者的创新方差为 sigma²。若只用各期边际 N(M_j,v) 相乘，相当于丢弃了跨期协方差。原文第3.2节的乘积写法与第2.3节的误差相关过程需要作者代码或 PDF 核实。

## 竞争解释及证据边界

候选解释包括 HTML/公式转录排版错误、原刊公式错误、正文使用了简写的伪似然、实际程序采用了正确联合似然。现有证据无法判定哪一种成立。第4.1节式(4.8)后的 atanh 反变换亦有 HTML 表达疑点，待 PDF 对照，不在本记录升级为出版勘误。

可观测与可证伪检查：取得正式 PDF 后逐字符对照第3.2节；若作者公开代码，检查正态对数似然的平方残差系数及 AR(1) 协方差/条件密度实现。可在合成序列上比较联合 AR(1) 与边际独立似然，但合成检验不能证明真人效应估计有效。

与 C016 去重：C016 已覆盖第1至3.3节的原著阅读、设计秩亏与先验敏感性反例。本记录的独立增量限定于 HTML 似然表达的符号及相关结构审计，不重复 C016 的先验反例。

未读：PDF 正式排版、作者勘误、实际模型代码、完整第5至8节。未使用个人资料、未开展个人决策产品。

output_paths: research/decision_methods/C017_SCHMID_YANG_2022_HTML_LIKELIHOOD_SIGN_AUDIT_2026-11-12.md
ci_status: NOT_RUN
billing_checked: 未调用计费 API、未主动触发 CI；账户账单 NOT_VERIFIED
blockers: PDF 下载端点在本次网页读取中返回不支持的二进制内容类型；原文版本差异未闭合。
next_action: PDF/作者代码核实后再决定是否发布正式勘误；保持 D004 2026-W46 PARTIAL、R073 与 PESEN v0.1 冻结。
