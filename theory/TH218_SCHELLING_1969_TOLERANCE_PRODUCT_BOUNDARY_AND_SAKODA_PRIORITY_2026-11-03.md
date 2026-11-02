# TH218 Schelling 1969 群体隔离模型的容忍阈值边界与模型史竞争

track: theory
subflow: primary
run_date: 2026-11-03 (Asia/Singapore)
target_key: (theory,Schelling1969+Sakoda1971+Hegselmann2017,1969-published+1971-publisher-abstract+2017-published,threshold-product-equality-vs-strict-and-micro-macro-attribution)
status: THEORY_NOTE_BOUNDED; PRIMARY_1969_FULLTEXT; SAKODA_ABSTRACT_ONLY; SYNTHETIC_PROOF; NO_R_UPGRADE
observed_head_before_work: 346f01484e6bd23faad1909383e3d08e5dd29301

## 原始来源、实际阅读范围及版本

1. Thomas C. Schelling (1969), “Models of Segregation”, *American Economic Review* 59(2):488–493, 原刊六页完整文字与p491、p492图文原版扫描直接核对。公开大学托管原刊扫描 https://www.uu.nl/sites/default/files/c4_schelling1969_models_segregation.pdf ，稳定JSTOR ID 1823701。该文件为个人研究阅读材料，原件及扫描图像不复制入仓库。
2. Thomas C. Schelling (1971), “Dynamic Models of Segregation”, *Journal of Mathematical Sociology* 1(2):143–186, DOI 10.1080/0022250X.1971.9989794。仅直接阅读出版者原始摘要，正式全文未读，不能将1969一维线性示例视为1971全部二维棋盘模型的逐式复现。
3. James M. Sakoda (1971), “The Checkerboard Model of Social Interaction”, *Journal of Mathematical Sociology* 1(1):119–132, DOI 10.1080/0022250X.1971.9989791。仅出版者原始摘要直接阅读，正式全文未取得。摘要涉及两群体、正中负态度、空间移动和多种配置，原文公式及实际运行未核。
4. Rainer Hegselmann (2017), “Thomas C. Schelling and James M. Sakoda: The Intellectual, Technical, and Social History of a Model”, *JASSS* 20(3):15, DOI 10.18564/jasss.3511，开放正式论文 https://jasss.soc.surrey.ac.uk/20/3/15/15.pdf ，直接审读引言及§2.1、§2.2、§2.3开头的指定文字（PDF页4至19的选段）。这是后世原创科学史研究，涉及Sakoda 1949博士论文的叙述仍属间接证据，1949原件未读。

## 新增数学限定：1969年p491的严格不等式边界

Schelling在p491定义某群体能接受的异群体人数与本群体人数之比上限，并明确采用“does not exceed”的含等号规则。令W、B为同一区域正的两群体人数，a为W群体容忍的B/W上限，b为B群体容忍的W/B上限。两群体同时满意当且仅当

B/W ≤ a，W/B ≤ b，亦即 1/b ≤ B/W ≤ a （a,b>0）。

因此正比例可行的必要充分条件为 **ab ≥ 1**；当 **ab > 1** 时才有非零宽度的可行比例区间。原刊p491文字称两群体最高容忍上限的乘积“must exceed one”，若其意图只是存在至少一个含边界的满意比例，则严格大于遗漏了等号边界。构造a=3/2、b=2/3、W=2、B=3，两个群体均恰好达到各自容忍上限，ab=1，存在满意混合配置。此为对原刊措辞的**条件性数学细化**，尚无正式勘误核验；若作者暗含稳健于微小扰动或要求一段正宽度比例，则严格大于成立。仅最大个体阈值存在不自动保证有足够数量的两群体成员共同进入，本文构造假设各组所有成员具有对应阈值。

限定检查脚本 `theory/th218_tolerance_boundary_audit.py` 使用Python标准库Fraction，边界、严格内部、严格不可行及20×20个整数人口组合共410项精确断言PASS。脚本仅验证所列阈值逻辑，未复算1969图形运动或任何真实人类行为。

## 竞争机制及识别边界

Schelling1969 pp488–490讨论制度组织、经济限制、沟通网络及个体偏好等不同隔离来源。p490一维线性邻域采用左右各4邻居，最低同类比例1/2，并通过按次序搬迁形成超出个体最低要求的聚集；p491–493的第二个模型改用两群体容忍比例分布及进出动态。p492明确存在可能满足的混合构成，却因进入退出动态无法稳定；p493指出一方人口规模增加、初始条件与迁移率会改变均衡，较高容忍度不保证更稳定的混合结果。

构造性识别反例：观察到A、B分别集中于两个社区，可以来自个体对本群体邻居的阈值要求，也可以来自外部强制进入限制。相同聚合分布并不能确定个体偏好或解除限制后的反事实结果。该反例是逻辑构造，不构成真实城市的因果证明。现实历史需独立观察制度、住房可得性、价格、歧视、迁移顺序与社区边界。1969论文的美国城市例子属于作者动机与概念分析，不能由此把棋盘模拟当作美国种族隔离的实证解释。

Sakoda1971原始摘要提出带正负态度和空间吸引的更广泛棋盘框架。Hegselmann2017 §2比较两者的距离权重、局部阈值与迁移规则，并讨论Sakoda1949先例和科学认可史。该科学史竞争提示不应将二维棋盘社会互动模型的全部起源简单归于Schelling；Sakoda原刊正文及1949学位论文尚待直接核验，不做原创优先权最终裁定。

## 层级、证据及未完成事项

个体层：偏好阈值、进入机会和迁移决策。群体层：局部比例、搬迁反馈与聚集。制度层：住房限制、价格和规则可能生成同样分布。历史层：长期隔离趋势需带日期、地理分母和制度档案的独立研究。1969模型属理论机制和手工演示，Sakoda摘要属原始出版者摘要，Hegselmann属现代科学史研究，410项测试属构造性数学证明。真实行为实验、历史因果识别、预测评价、R E1/E2/E3新增均NOT_RUN。

覆盖改善：数学社会学的微观互动到群体分布、动态均衡、模型优先权与历史归因。与既有TH020网络扩散及TH216语言因果争论仅作局部关联，未开展项目级分类或熔炼。

C011已于2026-11-03完成，本轮只读；D003已于2026-W45的2026-11-02完成，本轮只读。R073与PESEN v0.1冻结，R E1/E2/E3与MARKET等级不升级。无新增费用操作，实际账户费用NOT_VERIFIED，CI NOT_RUN。

下一步：取得Sakoda1971合法开放原刊正文或1949学位论文，逐式核查模型距离权重与先例；若来源不可得，转向其他弱覆盖学科。保持全部R系列完成后统一分类，再有条件熔炼。
