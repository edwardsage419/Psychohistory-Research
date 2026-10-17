# R079：第五套原作者真人互动资料的动态双人配对相关性和群体均值方差 E2 实证审计

**日期：** 2026-10-17。**正式范围：** 数据来源、真实双人网络身份互证与预先冻结的观察性组级二阶统计，`CLOSED_BOUNDED`。证据 `E2_REAL_AUTHOR_CLEANED_HUMAN_DESCRIPTIVE`，不等于新的个体预测 E3，也不识别个体感染、组间因果或社会历史演化。PESEN v0.1 全程冻结。

## A01：问题与与 R078 精确数学反例的界线

R078 以**人工**的两个因果结构例子证明，个体联合分布/预测Brier完全相同，却可能对应截然不同的`do(O)` 因果效应，且在额外组内独立/共因假设下的群体合作率方差不同。R079在新一项原作者真实实验中仅问：能否确定一轮内部谁与谁实际同组、二者已经实现的合作/贡献份额，并直接计算**在条件相同轮次的人群中实际配对合作相似性超过均匀随机重配对数学参考值多少**？

本次原实验**双人群组n=2**，不是R078的n=10人工群体模拟。不套用R078的 `q0=.3/q1=.7` 或理论方差0.025/0.061。即使实际配对正相关，也不允许由此推断“同伴行动因果影响本人”或“共同潜变量U被验证”。

## A02：作者身份、源数据、许可与复现层次

论文 Andreozzi, Ploner & Saral (2020), *The Stability of Conditional Cooperation: Beliefs Alone Cannot Explain the Decline of Cooperation in Social Dilemmas*, *Scientific Reports* 10,13610，[期刊及 DOI](https://doi.org/10.1038/s41598-020-70681-z)。作者GitHub [seyhunsaral/stabilitycondcoop](https://github.com/seyhunsaral/stabilitycondcoop) 固定 `master` commit `979abf87b5d3cfb7aa8be13b81ef233076c3bb75`，其亲自提供的清洗CSV `data/csv/subjects.csv` **425,701 bytes**、Git SHA1 blob `bd4c1550002621bee7dfb50e0d15d317764d1ea9`。原作者定义/清洗源程序 `code/process_raw_data.R` blob `522efd459f574ccaef3d9ce1dd2b086ffb70370e`，仓库README源blob `3292568ac99ec45c22ebcf009fa929028e07608a`；所有输出仅合法按原作者数据许可 CC BY 4.0 使用，原软件脚本MIT。

作者数据处理明确指出 z-Tree 首4轮**练习排除**，而后10轮的正式`period`编码为1..10；`action`为实际实现转移0/50/100，不是未执行的`uc`或者`ccL/ccM/ccH`条件选择计划，`opp`是真正对手编号、`opp_action`是该对手实际贡献，`group`为当轮配对。两个原始处理 `NoCondInfo` 与 `CondInfo` 的信息结构不同；参与者 `first_player` 为实际角色，可能是混淆来源。

**尚未完成：** 用作者6份原始z-Tree `.xls`重新跑原始R清洗程序并逐字节证明生成CSV完全相同。这是来源链的 OPEN 限制，当前`E2`的基线严格定为“作者本人发布、SHA锁定的清洗真人行为表”，不得把来源等价描述为已检查原始z-Tree全部列。原作者的论文研究结论已经被读过，本项是**回顾性真实数据描述分析**，不是人群招募前实验登记。

## A03：全部真人行与双人网络的实际安全核验

首先独立提交了 [R079 实数计算前冻结协议](../../protocols/R079_INDEPENDENT_HUMAN_DYAD_COVARIANCE_RANDOM_MATCHING_REFERENCE_FREEZE_2026-10-17.md)，Git commit `91faba1f2d956aec76550028f9ce1da681bd8c54`。随后在 [GitHub Actions 38996579448](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996579448) 通过34项**完全合成**身份互证、三档已执行值、强制单组两人和有限总体组合计数公式测试后，从原作者不可变Git blob 下载真正真人文件并运行严格 fail-closed gate。

核验结果：

| 作者真实数据宇宙 | 核验值 |
|---|---:|
| 真实个人×正式回合行动记录 | 1,340 |
| 原始 z-Tree 实验场次 | 6 |
| 原始场次内独立人物身份槽 | 134 |
| 每场正式轮次 | 10 |
| 场次×轮次群组 | 60 |
| 实际无向双人配对（每轮新网络边） | 670 |
| `CondInfo` 原始实验场次 | 3 |
| `NoCondInfo` 原始实验场次 | 3 |
| 同场同轮本人ID唯一且所有组恰两人 | PASS |
| 每条真实对手身份及双方动作 `opp`/`opp_action` 交叉互证 | 670/670 PASS |
| 两个处理的场次归属独一及练习回合剔除 | PASS |

数据是真人真实配对，不是策略模拟，也没有创建伪造场次。只是**当轮**完成后的已执行行为数据；若要检验某轮对手行为如何影响下一轮本人选择，必须另定时间上前置的 lagged feedback 研究，不能拿 `opp_action_t` 在同轮立刻估计因果影响。

## A03：冻结的组内/组间数学统计

把已实现三档 `action` 标准化为贡献份额 `y=action/100∈{0,1/2,1}`。对每个真实 `session×period` ，人数N为偶数，每个当前`group`恰两个参与者。设该轮平均贡献`μ`，人口方差 `v=Σ(y_i−μ)^2/N`；当前真实配对的去均值交叉矩
\[
c_{\mathrm{obs}}=\frac{1}{N/2}\sum_{(i,j)\in\mathrm{pairs}}(y_i-\mu)(y_j-\mu).
\]
在**固定当轮所有人的 y，假设配对在所有N人完美匹配中均匀随机**的数学参照下，严格可算的交叉矩
\[
c_{\mathrm{random}}=-\frac{v}{N-1},
\qquad
e=c_{\mathrm{obs}}-c_{\mathrm{random}}.
\]
同一轮真实双人组平均贡献 `m=(y_i+y_j)/2` 的总体方差满足代数恒等式
\[
\mathrm{Var}_{\mathrm{pairs}}(m)=\frac{v+c_{\mathrm{obs}}}{2},
\quad
\mathrm{Var}_{\mathrm{random}}(m)=\frac{v+c_{\mathrm{random}}}{2},
\quad
\Delta \mathrm{Var}=\frac{e}{2}.
\]
全部在Python `Fraction` 中以**精确有理数**对每轮检验，之后才转成浮点数发表。首要聚合不是把全部配对当独立个体，而是先对每个独立原始session的10轮等权平均，再六个原始session等权平均；处理内分别按各三场等权。

### 真正实跑原作者真人数据结果

| 已先验冻结的统计 | 六场总体等权 | CondInfo 3场 | NoCondInfo 3场 |
|---|---:|---:|---:|
| 人均实际贡献份额 `μ` | 0.328775 | 0.342588 | 0.314962 |
| 当轮真人个体总方差 `v` | 0.127521 | 0.140445 | 0.114596 |
| 实际双人交叉矩 `c_obs` | +0.033114 | +0.042004 | +0.024224 |
| 固定y后随机匹配参考 `c_random` | −0.006030 | −0.006732 | −0.005328 |
| 真实相对参考的超额 `e` | **+0.039144** | **+0.048736** | **+0.029552** |
| 真实双人组均值横截面方差 | 0.080317 | 0.091224 | 0.069410 |
| 重配对参考组均值方差 | 0.060745 | 0.066857 | 0.054634 |
| `e>0` 原始场次数量 | **6/6** | **3/3** | **3/3** |
| 正式1–5轮平均贡献 | 0.366692 | 0.383258 | 0.350126 |
| 正式6–10轮平均贡献 | 0.290859 | 0.301919 | 0.279798 |
| 后五轮−前五轮 | −0.075833 | −0.081338 | −0.070328 |

六场均表现为当轮真实配对的贡献相似性比固定当轮行为、均匀重配对的非因果参考值更强，且实际组均值方差比数学参考高 `+0.019572`。处理间超额交叉矩之差 `0.048736−0.029552=0.019184` **只是实验间观察差，不是条件策略信息的因果效应估计**；两个处理各仅3场，原作者实际干预和设计、实验参与者分配尚未在本项目建立可识别估计，严禁用“6/6同向”冒充统计显著性或人类心理学普适定律。

一部分 `c_obs>0` 也可能来自**同时**的角色和匹配互动、均衡选择、初始群体同质性、共同情境或策略菜单响应机制；反事实参照固定实际y并数学重配对，故**不**是真实随机分配干预，绝不推出 `do(peer)` 干预作用或R078合成 latent-U 真实存在。

## A04：保留失败记录和所有负面边界

- [首次 CI 38996553953](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996553953) 的34项合成断言中第26项误将无害的`dyad_count_per_session_period_distribution`键误判成泄漏的`per_session`，导致该CI **FAIL，未开始任何真人分析**。随后只修复纯合成测试，明确禁止实际“单场逐行分数”，保持已冻结的真实模型公式和共同样本未修改；[CI 38996579448](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996579448) 两job PASS，首次完成实际匿名宏统计。该失败应保留，不回填为通过。
- 人物身份槽134不是经独立身份追溯证明的134名完全不同真人；每场按独立实验参与者分组，**跨原始场次是否有人重复参加未经核实**。
- 组是当轮的**两人配对边**，不是持续十轮成员不变的固定团队；组号在别的轮次可能重用。不能把670组当670个独立群体，不能把该6场推导到R078的十人共因群体。
- 第一行动者/第二行动者的收益结构、控制组 vs 条件信息组可能改变已实现`action`的含义；我们只测已实现贡献，不断言因果角色效应。
- 仅有基于现成作者清洗表的原始z-Tree解析准确性，源真实观测E2成立但原始六个Excel重放未执行。
- 没有真实组历史长期转移、制度形成、多世代文化变化或宏观历史预测。

## A03/A06：跨环境真实执行与永久数字验收

[R079纯标准库真实数学/样本程序](r079_real_human_dyad_matching_moments.py)、[34项合成反例和隐私保护单测](test_r079_real_human_dyad_matching_moments.py)。在 [38996579448](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996579448) 原始Git SHA锁定运行中，实际独立核验六场、1340原始行、670对人类关系，每一轮精确恒等式 PASS；输出 `3771 bytes`，SHA256 `82efe8ad7bcc6c01ac10616676d84c5208ad9f6cc83670aa4c5b72f3860ff102`。之后由 [完全独立重下载原作者文件并原地两次运行 SHA 精确复核、永久归档 CI 38996643486](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38996643486) success，仅向仓库提交 [R079_REAL_AUTHOR_HUMAN_DYAD_NETWORK_MOMENTS_E2_RESULTS.json](R079_REAL_AUTHOR_HUMAN_DYAD_NETWORK_MOMENTS_E2_RESULTS.json)，Git blob `6c8f5f844f78d2cf288a26cd498e21572532ddc7`。

**隐私**：原始真人动作、全部具体参与者号码、逐组配对、具体session识别码及单场/单期指标一概没有写入Git，所有真实CSV仅CI runner临时文件中并在结束后删除。发表的只有处理级和全部独立场次**等权宏汇总**、每场超额符号计数和组数分布。

## A05：四层心理史学连接但不跨过因果门

- **个体**：当前选择是 0/50/100 实际贡献。与R073–R077的0/1合作并非直接同尺度；当前组内交叉矩不是个体条件概率预测性能，不构成第六个独立IPD七模型E3。
- **群体**：实际双人网络时变配对和交叉矩E2，首个真实数据可测R078微观到群体方差构造的部分观测对象；观察相似性与数学重配对参照可为后续结构识别准备材料。
- **制度**：两类条件策略信息，但只是现有处理分层描述，未使用真实随机设计证明制度因果。
- **历史**：十轮次短期行为下降只是实验时间变化，绝非代际演化或宏观历史预测证据。

与此前 E1 数学两机制的`n=10`群体方差对照不能直接比较，因群体规模、成员共享冲击机制和福利游戏均不同。若需要验证真实网络传播，后续可用R080去核验 Shirado & Christakis (2020) [公开Mendeley数据](https://data.mendeley.com/datasets/t963ktp6ft/1) 声称1024名人类、64真实互动网络、机器人干预；**在核验原文件、真人/机器实体身份与动态边之前，仅可记录为未纳入的候选资料**。

## A06 最终验收和后续

本次限定在“新真实作者资料上按预先确定的组内二阶矩指标复算、输出有界描述性证据”六项验收：
- A01 PASS 范围明确、未承诺完成真实社会因果识别；
- A02 PASS 作者原Git blob和 CC BY 源定位，未验证原始六个Excel重新加工的缺口明确 OPEN；
- A03 PASS 34合成、真实配对互证、精确有理数矩公式、双次独立Git SHA重放；
- A04 PASS 失败的首次CI与当前描述式反例/边界完整保留；
- A05 PASS E2描述与E1/真E3、预测/因果、双人/10人网络全部分离；
- A06 PASS 科学报告、全部匿名宏数字、验收状态、README、主仓核验。

`R079=CLOSED_BOUNDED` 只表示本限定实证研究档案完整；不等于 peer influence/制度/历史演化的完整因果科学目标闭合。

`R079_HUMAN_ORIGINAL_CLEANED_ROWS=1340`  
`R079_REALIZED_RECIPROCAL_DYADS=670`  
`R079_SESSIONS=6`  
`R079_PAIR_CROSS_EXCESS=0.03914395260219059`  
`R079_PAIR_GROUP_VAR=0.08031731137128864`  
`R079_RANDOM_MATCH_GROUP_VAR=0.06074533507019335`  
`R079_CAUSAL_SOCIAL_CONTAGION=NOT_IDENTIFIED`  
`R079_REAL_LONG_TERM_SOCIAL_EVOLUTION=NOT_ESTABLISHED`  
`PESEN_v0.1=FROZEN`
