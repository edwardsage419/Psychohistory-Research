# R226 选择与社会影响识别：八个有限网络来源世界与完整可观察等价对，计算前冻结

日期2026-10-22。原239目录 `09-017 Selection versus Influence Identification`，P0。研究编号R226。目标是以真正完整有限外生源检验网络同质性选择、共同潜在原因及个体模仿三种机制是否可从观察时序单独区分。结论限人工数学E1，不接入R073冻结模型，不使用真实人类或历史逐行为E2/E3。

一手方法背景：
* Shalizi & Thomas (2011), *Homophily and Contagion Are Generically Confounded in Observational Social Network Studies*, Sociological Methods & Research 40:211–239, DOI https://doi.org/10.1177/0049124111404820，讨论同质性、共同原因、社会影响的观察混淆。
* Aral, Muchnik & Sundararajan (2009), *Distinguishing influence-based contagion from homophily-driven diffusion in dynamic networks*, PNAS 106:21544–21549, DOI https://doi.org/10.1073/pnas.0908800106，方法背景为动态匹配、行为采用与同质性混淆；本R不重估其原样本或原量化效应。
* Eckles, Kizilcec & Bakshy (2016), *Estimating peer effects in networks with peer encouragement designs*, PNAS 113:7316–7322, DOI https://doi.org/10.1073/pnas.1511201113，作为随机鼓励设计的原则背景；本R仅自建外生信号的人工极小例子，不复原其实验和IV依从性机制。

## 固定外生源与可观察四元组

每世界潜在二元U、V、R、Q均互相独立Bernoulli(1/2)，四元组16种，每个原结构世界16条完整来源、每条概率1/16；8世界合计**128条结构原来源**。U是发送者A的潜在特征，V是接收者B的潜在特征，R是只有特定模型实际使用的随机外部A信号，Q是保留的独立背景源且不强制进入结果方程，目的是把完整原外生集合与因果机制明确归档。可观测数据仅包括 `edge_E`（两人是否形成关系）、`A_at_t0`（发送者先前公开行动）、`B_at_t0`（接收者自己的先前行动）、`B_at_t1`（接收者下一时点行动）；潜在U/V/R/Q只在人工oracle中读取。

边E在行动被实验干预之前由固定机制形成。干预 `do(A_at_t0=a)` 定义为在边E已经形成且U,V,R,Q保持不变时对实际发送者公开行动的替换，不允许重新形成网络边，不允许因do而改变U。将 `B_at_t1(do(A=1))−B_at_t1(do(A=0))` 在所有16原结构源上等权平均，得到**人工总体peer effect**；在E=1的来源上条件平均得到**已有关系的受控同伴效果**。研究不估计一般多主体或社会层传播。

## 冻结八世界（所有二元函数精确）

1. `PEER_COPY`：E=1, A0=U, B0=V, B1=A0，真peer effect=1。
2. `SHARED_LATENT_SHOCK`：E=1, A0=U, B0=V, B1=U，真peer effect=0。世界1和2**完整P(E,A0,B0,B1)逐格严格相同**，前者确有同伴影响，后者完全由未测共同U产生。
3. `HOMOPHILY_ONLY`：E=1{U=V}, A0=U, B0=V, B1=V，真peer effect=0。
4. `HOMOPHILY_WITH_COPY`：E=1{U=V}, A0=U, B0=V, B1=A0 if E else V，真总体peer effect=P(E=1)=1/2，条件E1真效应1。**世界3和4完整P(E,A0,B0,B1)逐格相同**；两者所有已成边来源均有A0=B0，因此无法从已有边观察到行动相异时的受控反事实。
5. `RANDOMIZED_PEER_COPY`：E=1, A0=R, B0=V, B1=A0，真peer effect1；外生R独立U,V提供真实随机信号。
6. `RANDOMIZED_NO_COPY`：E=1, A0=R, B0=V, B1=U，真peer effect0；R独立U,V。
7. `RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK`：E=1{U=V}, A0=R, B0=V, B1=A0 if E else V，总体peer effect1/2，条件E1真效应1；由于R独立U,V,E，已有边中A0与B0不同的事件具有正概率，提供前述世界3/4欠缺的行动变化支持。
8. `ANTI_PEER_COPY`：E=1, A0=U, B0=V, B1=1−A0，总体真peer effect−1，作为方向相反的辨别测试。

对每世界必须保存完整外生来源U,V,R,Q、实际E/A0/B0/B1，以及两个不读取真实资料的oracle B1(do(A=0))与B1(do(A=1))，完整概率、实际t1行动的结构一致性。

## 计算前冻结的检验

1. **只读观察**：完整联合P(E,A0,B0,B1)的所有原来源概率；在E=1的观察分组中报告D_peer=E[B1|A0=1,E=1]−E[B1|A0=0,E=1]；已成边中`P(A0≠B0|E=1)`的真实观察支持比率；观察边概率P(E=1)。
2. **独立oracle**：人工完整原来源 do(A=1)-do(A=0) 的总体与E=1条件平均，仅用于检查真假因果，不允许将其用于观察估计。对每世界给出与直接由固定结构函数/边概率计算出的理论真效果的独立精确校验。
3. **完整观察等价**：世界1/2完整四格联合分布相等而真peer=1和0；世界3/4完整四格联合分布相等而真peer=0和1/2。不能只比较相关系数或整体平均代替逐状态概率比对。
4. **极端观察限制**：HOMOPHILY_ONLY与HOMOPHILY_WITH_COPY两世界E1中A0≠B0的观察比例严格0，且D_peer=1；对照RANDOMIZED_SIGNAL_ON_HOMOPHILY_NETWORK在E1中A0≠B0的支持为1/2，且可观察对比D_peer=1与条件受控真因果1相等。样本是完全有限人工源，不能据此推断真实网络随机外生性。
5. 逐16来源枚举与独立消去未使用Q的8状态边际积分在所有联合观测格、概率和、分组差及真peer因果差上分别一致；全部Fraction精确值，禁止真实样本置信区间。
6. Python3.11与3.12两版本各运行至少40项真实单测，第三GitHub Actions job重新生成并核验128完整来源、结果JSON、SHA机读收据，永久入main。预先冻结文件独立先提交，再编制代码和数据；未通过CI与实际来源归档不得宣称正式结题。

全部仅人工E1；新增真人E2=0，历史E3=0；R073与PESEN v0.1继续冻结。完成本条后下一个原目录编号需再次查询原始239 JSON，避免擅猜。
