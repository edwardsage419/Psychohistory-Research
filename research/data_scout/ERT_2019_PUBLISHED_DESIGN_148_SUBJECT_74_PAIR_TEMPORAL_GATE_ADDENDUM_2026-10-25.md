# A 数据侦察增量：Ert、Cohen-Amin、Dinar 2019 双边议题联结实验，发表论文设计核验

日期：2026-10-25。承接此前数据登记 `research/data_scout/ERT_DINAR_COHEN_AMIN_2019_BILATERAL_LINKAGE_REPEATED_GAMES_SOURCE_GATE_2026-10-25.md`。本轮额外直接读取英文公开的正式发表论文全文及其附录。来源为作者论文的大学公开副本 https://escholarship.org/content/qt51q0g17s/qt51q0g17s.pdf ，期刊 *Journal of Behavioral and Experimental Economics* 79 (2019) 134–142，DOI 10.1016/j.socec.2019.02.004；公开数据固定 V1 https://data.mendeley.com/datasets/6vsvptct74/1 ，DOI 10.17632/6vsvptct74.1，页面许可 CC BY-NC 3.0。

## 本轮实际新核实的实验设计

正式论文第4节说明 Experiment 1 共78名受试者，Isolated 36名、Linked 42名；第5节 Experiment 2 共70名受试者，Isolated 36名、Linked 34名。两实验合计148名受试者，按双人配对设计理论上74对；发表论文 Table 7 回归表也报告74个配对聚类、1905个回归观测。这里1905是特定回归表的观测数，**不可直接当作公开原始数据文件的行数或有效逐轮预测次数**。

论文第4节明确每次实验开始随机分配固定配对，同一对手连续互动30轮，每轮之后反馈本轮双方结果与支付。Experiment 1 单场6至10人，Experiment 2 单场6至12人；**实际场次数量尚未从原始文件验证**。Isolated 每轮先后玩两种不同的囚徒困境游戏；Linked 每轮同时选两个游戏的联合行动。论文附录 B 明确 Linked 四种联合动作 CC、CD、DC、DD，Isolated 单局二元动作 C/D。Experiment 2 修改了第一个游戏的收益非对称性，因此不可把两实验的支付矩阵视为完全相同。

## 预先列出的 R073 数据资格与泄漏门槛

1. 必须取得公开原始文件字节、固定版本 SHA256、许可与逐行字段；本轮仍未取得，状态 `BLOCKED_NOT_RETRIEVED`。
2. 场次、实验编号、处理、受试者、固定对手、期次、单局序号需要构成无冲突的观测键。论文总人数、配对聚类数不等于可用训练或留出单元数。
3. Isolated 的 game1 与 game2 有先后决策顺序，预测某个决策时必须屏蔽同一期之后才观察到的对手动作和结果。若 R073 冻结协议未授权把同一期 game1 当作 game2 的预测历史，不得自行增加该特征。
4. `partnerchoice` 是当期对手实际行动，预测同一时点自身行动时不得用作输入。每轮反馈可用于**下一轮**严格滞后特征。`FinalPay` 为最终抽取结果，`TimeDecision` 为决策后才确定的用时；两者均列为目标泄漏风险，不进入预测时点特征。
5. Linked 四级联合动作不得擅自重编码成 R073 二元标签；Isolated 虽为二元，但需核查两局序列是否满足冻结的观测和评分定义。不能在看到结果后选择较优的一个游戏、处理或配对。
6. 留出完整 session 进行独立预测评价，若 session 编号不足、场次过少或身份跨场次重叠，必须阻塞。检查 R073 及其他 R 研究已使用实验的重复来源，不能因新论文标题而直接判定独立。

## 本轮判定

论文设计层面：`PUBLISHED_DESIGN_CONFIRMED_148_SUBJECTS_74_PAIRS_30_ROUNDS`。逐行数据门槛：`BLOCKED_RAW_BYTES_AND_SESSION_IDENTITIES`。R073 冻结外部评分：`NOT_STARTED`。新增 E2/E3 预测均为0。仅使用英文论文和官方公开元数据，没有访问非公开私人数据、付费资源或注册账户。
