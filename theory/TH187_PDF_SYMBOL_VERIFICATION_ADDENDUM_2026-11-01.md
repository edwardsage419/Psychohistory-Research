# TH187 原始PDF公式核验补记：严格上尾与离散检验水平

track: theory
subflow: main
run_date: 2026-11-01 (Asia/Singapore)
observed_baseline_head: 864bdf49a0c8df101a18970734557b6616516843
target_key: (theory,PuelzBasseFellerToulis1910.10862v3+Puelz2019authorDraft,theory-v1,original_pdf_strict_tail_and_level_claim)
status: COMPLETE_BOUNDED_SOURCE_VERIFICATION; PUBLISHED_VERSION_FORMULA_NOT_VERIFIED
evidence_scope: AUTHOR_PDF_DIRECT_PAGE_INSPECTION; NONBLIND; EXACT_ARTIFICIAL_ENUMERATION
ci_status: NOT_RUN
billing_checked: NOT_CHECKED
cost_action: NO_NEW_PAID_SERVICE_OR_CI

## 原始来源、实际阅读范围与版本差异

检索与直接核验日期：2026-11-01。仅使用非中文语言开放来源。

1. Puelz D, Basse G, Feller A, Toulis P. *A Graph-Theoretic Approach to Randomization Tests of Causal Effects Under General Interference*. arXiv:1910.10862v3，PDF首页标记 This Version: May 26, 2021，arXiv页脚v3 25 May 2021。开放PDF https://arxiv.org/pdf/1910.10862 。**实际查看PDF页面6、10、11、39（印刷页码）图像**，并核对附录B定理证明第31至32页可检索文本。第6页Theorem 1第三步为严格大于号 >；第10页Procedure 1 Equation (8)同样为 >；第11页Theorem 2写任意alpha属于(0,1)时拒绝概率 **等于** alpha；第39页Appendix E.2模拟步骤3使用 **大于等于** >=。这四处由PDF页面直接确认，原TH187的PDF_SYMBOL_CHECK_OPEN对该v3稿可关闭。
2. Puelz等，作者网站开放早期稿 *Working Draft (September 22, 2019)*，https://www.davidpuelz.com/causal_cliques_Draft.pdf 。实际阅读第4.1节Procedure 1 Equation (3)和Theorem 2以及附录A.1对应定理。该稿Equation (3)为严格 >，Theorem 2的拒绝概率结论写 **小于等于** alpha。该稿也存在离散分布严格尾部的有效性疑问。2019稿与2021 v3稿的定理比较符号不同，必须按版本引用。
3. 同一研究2022年发表于 *Journal of the Royal Statistical Society Series B* 84(1):174至204，DOI:10.1111/rssb.12478，出版商书目与摘要 https://rss.onlinelibrary.wiley.com/doi/10.1111/rssb.12478 。**正式刊印版公式未逐页核验**，不得宣称正式发表版存在相同符号。
4. ar5iv https://ar5iv.labs.arxiv.org/html/1910.10862 页面顶部显示2026-08-09，与上述可取得的PDF v3版本日期不一致。此次以实际可见PDF页眉和公式为准，不推断HTML日期代表新的经过核对的arXiv版本。

## 核心命题与可证伪的数学差异

设合法条件随机化支持集为六个等概率分配，锐零假设下统计量的六个值为3、5、6、9、10、12。用穷举而非统计近似得到：

| 规则 | 观测最大值12的p | alpha=1/20时零假设拒绝概率 | alpha=1/6时零假设拒绝概率 |
| --- | --- | --- | --- |
| p_strict=P(T'>Tobs) | 0 | 1/6 | 1/3 |
| p_inclusive=P(T'>=Tobs) | 1/6 | 0 | 1/6 |

当六个统计量完全相同，严格上尾p对每种观察分配均为0，在任意alpha>0下全部拒绝；包含平局的上尾p恒为1，均不拒绝。两个例子都满足正确随机化权重，说明单靠条件化无法修复尾部符号。

一般离散随机化下，保守的p_inclusive具有P(p<=alpha)<=alpha的超均匀性；不附加随机化时，通常不可能对任意实数alpha保证精确等号。若引入独立U~Uniform(0,1)并显式规定 p_random=P(T'>Tobs)+U P(T'=Tobs)，则在锐零假设与正确条件设计下可得到均匀p；这一规则没有出现在上述v3 PDF已读的Procedure 1 Equation (8)中。此处是数学建议，**不是作者实际实施方式的断言**。

本轮在Python标准库Fraction中重新穷举六个唯一值与全平局两种世界；上述分数和拒绝率计算均与精确枚举一致。未开展新真人实验、历史预测或作者代码复算。TH187已有的24项单元测试本轮未重跑；本轮仅进行了简短独立枚举，CI NOT_RUN。

## 竞争解释、四层关联与边界

竞争解释包括原稿笔误、缺少明示的随机平局机制、不同版本公式演进，以及正式发表版可能已更正。现有直接证据排除了“2021 v3 PDF图像实际为 >=，只是HTML转写成 >”这一特定解释。不能排除正式发表版修订、作者代码采用 >= 或论文其他位置补充约定。

个体层：潜在结果与统计量。群体层：干扰网络、条件焦点和离散支持。制度层：随机分配与可重复的检验实施规范。历史层：仅作为未来跨制度运输的识别边界，未验证历史外推。此项数学更正不构成R系列E1/E2/E3科学验收，不影响R073、PESEN v0.1冻结。

## 后续

1. 获取合法可公开阅读的2022正式刊印版相应页，核对Theorem 1、Equation (8)、Theorem 2和模拟附录是否更正。若不可得，保留PUBLISHED_VERSION_FORMULA_NOT_VERIFIED。
2. 检查作者开源实现的尾部比较与平局规则，必须固定源码版本及许可证；本轮NOT_RUN。
3. 继续推进广泛理论学习；本轮已闭合TH187的v3 PDF符号核验，未新增TH编号。
4. C009已满足2026-11-01，D002已满足2026-W44，两项保持只读。R轨及Codex未合并PR不受本补记改变。
