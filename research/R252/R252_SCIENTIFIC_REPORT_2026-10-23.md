# R252 熵与信息论：九人工六位世界、576完整来源、精确素数对数熵与条件依赖/干预非识别

日期2026-10-23（Asia/Taipei）。原239目录 `11-012 Entropy and Information Theory`（P1）；有界科学资格 `CLOSED_BOUNDED_E1_EXACT_SYMBOLIC_SHANNON_MUTUAL_INFORMATION`。全部概率来自人工六个独立公平位，不涉及真实人类沟通行为、历史信息传播或因果识别资料。新增真人E2=0、真实历史E3=0，R073/PESEN v0.1保持冻结。

## 一手来源、熵定义与精确性条件

C. E. Shannon (1948), [*A Mathematical Theory of Communication*, Part I](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x), *Bell System Technical Journal* 27(3):379–423，以及 [Part II](https://doi.org/10.1002/j.1538-7305.1948.tb00917.x), 27(4):623–656。定义`H(X)=−∑p(x)log₂p(x)`，`I(X;Y)=H(X)+H(Y)−H(X,Y)`，`I(X;Y|Z)=H(X,Z)+H(Y,Z)−H(Z)−H(X,Y,Z)`，所有信息量单位为bit。**信息论互信息仅针对概率联合分布的统计依赖，不告诉研究人员变量的社会意义或因果箭头方向；条件互信息与无条件互信息没有单调大小关系，数据处理不等式也不应被误套到任意条件选择上。**

[九人工模型、全部六位source与两条独立概率积分路线](../../protocols/R252_ENTROPY_9_SIXBIT_WORLDS_576_ORIGINAL_SOURCES_PRESCORE_FREEZE_2026-10-23.md)事前独立冻结提交[30815e30](https://github.com/edwardsage419/Psychohistory-Research/commit/30815e3018c099ee362780f1b2292dc33644e27d)，先于源码、测试和最终结果。九world各有公平独立bit`(U,A,B,C,D,E)∈{0,1}^6`，每world2⁶=64个原外生结构型、每源权重1/64，九world合计**576个完整人工原来源**。CSV逐行保存原六bit，实际可见(X,Y,Z)，oracle人工反事实Y(do(X←1−X))，及来源权重。U/D/E在部分模型里不改变观测，但必须保留原外生全集，不将其解释为新增独立受试者。

## 一手来源穷举与独立完整联合概率闭式

第一路线按每个人工世界的冻结布尔结构方程生成观察(X,Y,Z)，对全部六bit精确Fraction边缘化，得到完整三元观察PMF；第二路线**不读取原CSV或生成函数**，独立按模型枚举完整联合概率：INDEPENDENT_BITS的8种三元位组合各1/8；DIRECT_COPY和HIDDEN_COMMON_CAUSE_ALIAS的4种(x,x,z)各1/4；XOR_SYNERGY和XOR_MASK_REPARAM的4种满足x XOR y=z的三元组合各1/4；ERASURE_HALF的4个三元组合各1/4；BINARY_SYMMETRIC_QUARTER中z=0且y=x各1/4，z=1且y=x、y≠x分别各1/8；COLLIDER_AND四个(x,y,z=x AND y)各1/4；CONSTANT_REPORTER四个(x,0,z)各1/4。九个完整三元概率分布的两条数学路线全部**逐格、严格Fraction一致**，所有世界概率质量恰为1。

**非有理熵的精确保存，不用浮点冒称数学证明。** 对任意有正质量的支持点概率p=n/64，本R将`H=6−Σ(n/64)log₂n`中的整数n完全素数分解，得到形如`a + b·log₂3 + c·log₂5+...`的**精确有理系数向量**（log₂2完全并入有理项）。所有H/I/conditional I先对这些系数逐项严格代数核验，报告近似值才另外调用`math.log2`用于阅读。这避免了将正好是`(3/4)log₂3−1`的非有理bit误写成有理小数0.18872的逻辑错误。

## 九冻结机制的核心信息统计

| 人工机制 | H(Y) bit | I(X;Y) bit | I(X;Y｜Z) bit | 主要证据 |
|---|---:|---:|---:|---|
| INDEPENDENT_BITS | 1 | 0 | 0 | 三位独立、H(X,Y,Z)=3 |
| DIRECT_COPY | 1 | 1 | 1 | 直接Y=X，信息完全重复 |
| HIDDEN_COMMON_CAUSE_ALIAS | 1 | 1 | 1 | 观察与直接复制同源等价，但干预不同 |
| XOR_SYNERGY | 1 | 0 | 1 | 条件于XOR后，原本独立的X/Y完全依赖 |
| ERASURE_HALF | 3/2 | 1/2 | 1/2 | Y=2明示擦除符号，保留一半X信息 |
| BINARY_SYMMETRIC_QUARTER | 1 | `(3/4)log₂3−1` | 1/2 | 翻转概率1/4，非有理精确MI |
| COLLIDER_AND | 1 | 0 | `(3/4)log₂3−1` | 条件于共同结果可产生选择依赖 |
| XOR_MASK_REPARAM | 1 | 0 | 1 | 与XOR_SYNERGY全三元分布一样，生成方向不同 |
| CONSTANT_REPORTER | 0 | 0 | 0 | 常量Y没有X的信息，X仍有H(X)=1 |

非有理信息数`(3/4)log₂3−1`约为0.188721875541 bit，严格大于0，因为`3³=27>16=2⁴`，故`(3/4)log₂3>1`。数值小数仅作为辅助解释，源JSON同时保存`exact_rational=-1`与`exact_log2_prime_coefficients={"3":"3/4"}`，不丢失精确信息。

**相同无条件独立，条件信息可为整1bit。** XOR_SYNERGY的X=A、Y=B原本相互独立且均公平，故I(X;Y)=0；但Z=A XOR B一旦给定，知道X就完全确定Y，条件互信息I(X;Y|Z)=1。这并不意味着一个心理信息流凭空创造1bit外部数据，而是观测第三变量Z本身对两者提供联合约束。XOR_MASK_REPARAM产生完全相同(X,Y,Z)联合概率分布（每种偶校验约束的状态1/4），却以Y=A XOR B、Z=B为结构方程；即使完整三元观察联合分布已知，**也不唯一确定生成方向或社会传播机制**。

**碰撞变量选择会产生条件依赖。** COLLIDER_AND结构X=A、Y=B独立，但Z=A AND B。无条件I(X;Y)=0；给定Z=0，观察会排除(X,Y)=(1,1)，从而在剩余三态上产生依赖，精确I(X;Y|Z)=`(3/4)log₂3−1>0`。仅观察某个公共结果Z下的相关性，不可据此判断X和Y之间存在直接信息传输或社会因果效应。它与无条件二元对称信道的相同数字信息量不是相同因果机制。

**最强因果观察别名。** DIRECT_COPY让X=A，Y=X，Z=C，理论人工do(X←1−A)使Y与干预一起翻转；HIDDEN_COMMON_CAUSE_ALIAS让一个隐藏外生A分别决定X和Y，Z仍C，人工干预翻转报告X后，Y保留原A。对每条完全相同的六bit原来源，两世界的**所有实际观察(X,Y,Z)逐source完全一样**，完整联合、所有边际熵、互信息及条件互信息都相同；但人工结构oracle反事实`Y(do(X翻转))`逐source不同。因此**信息依赖甚至完美复制的观测，不足以独立证明干预因果效应**。该结论是明确人工结构非识别反例，不声称真实人类中发生何种因果箭头。

**擦除符号和无信息报告器边界：** ERASURE_HALF中第三个观测符号Y=2表示“本次无法观察X”而非正常二元0/1，H(Y)=3/2，但由于随机擦除一半，I(X;Y)=1/2，不能将报告变量熵当作完整保留X信息的数量。CONSTANT_REPORTER虽然H(Y)=0、I(X;Y)=0，X原本边际H(X)=1照旧不变，说明输入不确定性与观察通道可传递的信息不同。

## 实际两次CI、推送并发更正与完整SHA归档

[原生Fraction+符号素数对数信息计算程序](r252_exact_shannon_information.py) · [576完整六bit原source CSV](R252_ALL_576_ORIGINAL_SIXBIT_INFORMATION_SOURCES.csv) · [九人工完整三元PMF/所有熵与干预oracle JSON](R252_EXACT_RESULTS.json) · [SHA256来源验收机读收据](R252_FINAL_MACHINE_ACCEPTANCE.json)。

首次[GitHub Actions run39895196152](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39895196152)两个Python模型测试job成功、第三独立归档数学核验亦成功，日志`R252_ALL_576_SYMBOLIC_SHANNON_ENTROPY_SOURCE_ALIASES_AND_LOG3_VERIFIED`；**但永久推送main因恰有R251科研报告提交发生非快进并发冲突而失败**。故首轮**不计作成功验收**，尽管其临时artifacts上传成功。仅改归档workflow增加有界6次`git fetch origin main; git rebase origin/main; git push`重试，不强推、不删科学源、未修改九世界数学及全部原概率，修复提交[c4d86f78](https://github.com/edwardsage419/Psychohistory-Research/commit/c4d86f781b726bf0aa1f2971317aa92aa1d40ca4)并保留失败run历史。

最终[GitHub Actions run39895279784](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39895279784)总体completed/success，全部三job completed/success，Python3.11与3.12实际日志各`Ran 85 tests`、`OK`，合计**170次真实双版本测试通过**。第三独立作业再次严格验算各世界64个唯一六bit来源、每源1/64、九world全部三元概率完整分布、全部H/I/conditional I的精确有理及素数对数系数、XOR相同分布而条件依赖、选择碰撞精确log₂3量、擦除Y=2、DIRECT/COMMON两结构逐source观察同值但人工干预反事实不同，以及CSV/结果SHA256。成功日志`R252_ALL_576_SYMBOLIC_SHANNON_ENTROPY_SOURCE_ALIASES_AND_LOG3_VERIFIED`、`R252_ALL_ORIGINAL_576_SOURCES_PERMANENTLY_ARCHIVED`。完整CSV、结果JSON和SHA机器凭证机器人永久提交main [a63c75a0](https://github.com/edwardsage419/Psychohistory-Research/commit/a63c75a047dee455382f5983c70a4c9935e6182a)。

完整原CSV SHA256 `febd739ed17cbdac2dff13e32429e8250bfc13f067b31bf641c9679c241d3061`，完整结果JSON SHA256 `9537ad9ba2000043dce1f92c171eaae607c7a1b35f2a3059dcfcefcd7b1fe042`。

研究仅按`CLOSED_BOUNDED_E1_EXACT_SYMBOLIC_SHANNON_MUTUAL_INFORMATION`有界人工数学结题，无真人通信数据、文化扩散外部验证或真实历史因果估计。新真人E2/真实历史E3=0，R073和PESEN v0.1保持冻结。下一原目录`11-013 Information Cascade`（R253，P1），保留既定“全部原R→归纳分类→模型熔炼”顺序。
