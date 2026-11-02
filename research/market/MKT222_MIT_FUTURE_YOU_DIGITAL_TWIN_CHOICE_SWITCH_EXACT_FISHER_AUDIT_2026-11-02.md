# MKT222: MIT Future You 未来自我数字孪生与真实人生选择意向的随机试验证据审计

track: market
subflow: commercial_product_research + E_readonly_coordination + F_weekly_readonly
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,MIT-Future-You-multimodal-choice-avatar,2025-12-arxiv-2512.05397+2024-arxiv-2405.12514v4,choice-switch-versus-implemented-outcome+Fisher-tail+source-N-discrepancy)
observed_main_before_write: 4bf847a9617d6aa6473f7dec147955d096a98673
status: COMPLETE_BOUNDED_PRIMARY_PAPER_AND_EXACT_AGGREGATE_AUDIT
market_evidence_grade: MARKET-E2 for randomized short-term self-reported decision intention/psychological measures only
new_R_E2_E3: 0
real_long_term_decision_improvement: NOT_VERIFIED
participant_level_reanalysis: NOT_RUN
production_model_execution: NOT_RUN
actual_personal_sensitive_data: NOT_ACCESSED
ci_status: NOT_RUN
billing_account_and_free_quota: NOT_VERIFIED
paid_actions: NONE

## 1. 来源、去重与产品身份

直接阅读两项由 MIT Media Lab Future You 研究团队公开的英文原始论文全文及其研究项目官方说明，2026-11-02 访问：

1. Poonsiriwong 等，*Simulating Life Paths with Digital Twins: AI-Generated Future Selves Influence Decision-Making and Expand Human Choice*，2025-12-05 首次公开，arXiv:2512.05397，https://arxiv.org/abs/2512.05397 。本轮核心为 192 人五组随机试验。
2. Pataranutaporn 等，*Future You: A Conversation with an AI-Generated Future Self Reduces Anxiety, Negative Emotions, and Increases Future Self-Continuity*，arXiv:2405.12514v4（2024-10-01 修订），https://arxiv.org/abs/2405.12514v4 ；MIT 2025-02-26 出版记录 https://www.media.mit.edu/publications/future-you-a-conversation-with-an-ai-generated-future-self-reduces-anxiety-negative-emotions-and-increases-future-self-continuity/ 。原始 344 人短时心理试验。
3. 官方项目 https://www.media.mit.edu/projects/future-you/overview/ ，官方体验入口 https://futureyou.media.mit.edu/ 。
4. Albrecht 等，2025-12-05 arXiv:2512.06106，https://arxiv.org/abs/2512.06106 ，另一个 N=92 的文字、语音、头像模态比较试验，仅用于区分研究版本，不并入上述样本。

该 Future You 为真实可访问的研究型产品/实验系统。它与 futureyou.me、futureyou.cc 等同名商业产品无已确认同一性。本轮没有付费使用产品或上传头像、语音、私人决策数据。商业零售定价、长期商业运营和 2026 年生产模型版本均未独立核实；不得把研究原型视为已证实可销售的成熟决策产品。

此前 MKT210 为另一个 DecisionTwin 模拟候选，MKT219-221 为真实职业建议及就业行政结果；本轮研究对象、实验和缺口均不同。此前 MKT217 的决策知识/实际依从性区分继续适用。

## 2. 输入、状态、算法、反馈与可确认机制

2025 年 N=192 试验：参与者先输入一个未来一年内真实考虑的二选一问题、初始倾向、生活经历、职业/家庭/财务目标、个人价值与愿景，并上传本人照片及短语音。研究系统使用 Svelte Web 前端、Google Nano Banana 年龄进展、LivePortrait 动画、ElevenLabs 声音克隆、Claude Sonnet 4.5 生成每条路径的未来记忆和实时对话。参与者与约三十年后的虚构未来自我对话，时间约 7 至 10 分钟。

随机五组：仅引导想象对照 n=37，单独 A 未来自我 n=38，单独 B n=39，平衡 A+B n=38，额外生成新选项 C 的 A+B+C n=40。输出为多条虚构未来经历、价值与后果叙述及对话。试验后测量自报的当前选项倾向、决策冲突、自主感、执行意向、信心及未来自我连续性。不存在经验证的现实未来概率预测、实际目标优化、独立环境校准或长期结果反馈。2024 年 N=344 版本使用 GPT-3.5、StyleCLIP 和文字对话，研究版本不可混用。

2025 年试验中的 Option C 由 Claude 根据 A/B 的主题及自报价值生成，例如从医生和工程师的二选一扩展出兼顾教学的生物工程教授。作者明确说明这些是想象辅助，不能预测实际人生。完整提示词版本、训练数据、全部推理参数、生产服务日志及参与者级数据没有在本轮得到独立执行或复算。

隐私与商业限制：系统处理人脸、可识别语音、生活史及重大人生选择，使用第三方生成服务。官方 2024 项目 FAQ 称会匿名化收集问卷与对话用于研究；实际匿名化强度、供应商留存、删除和撤销结果没有实测。模型/云端调用涉及潜在费用，本轮不运行。项目页宣传覆盖 190 国、逾 60,000 用户，属于项目方披露的触达数字，不是效果试验样本，也没有独立验证。

## 3. 2025 年随机试验实际结果与测量边界

作者报告参与者为美国 18 至 28 岁的 192 人。方法章节另写排除 3 名技术/语言问题参与者，五组人数加总为 192；原始招募总数与排除前后分母关系尚未从公开文字明确复原。

按论文第 4 节公布的整数比例及五组样本量：

| 比较 | 试验组即时选择变化 | 对照组即时选择变化 | 论文报告 p | 直接证据 |
| --- | --- | --- | --- | --- |
| 双未来自我，改变 A/B 选择 | 13/38=34.21% | 4/37=10.81% | 0.015 | 立即改变问卷选项 |
| 三未来自我，选择额外 C | 8/40=20.00% | 1/37=2.70% | 0.019 | 立即选择新增选项 |
| 只展示 A，转向 A | 7/38=18.42% | 3/37=8.11% | 0.068 | 边缘结果 |
| 只展示 B，转向 B | 6/39=15.38% | 约2/37=5.41%（文中写5.3%） | 0.054 | 边缘结果，分母表述待核 |

关键区分：论文观察的是问卷前后选择/意向的改变。没有观察实际入学、就业、迁居、财务或关系选择的实施，也没有衡量一年或多年后是否更满意或更有利。选择变化本身没有外部正确答案。随机化只支持短时界面配置对这些近端指标的有限因果判断。

作者还报告：未来自我连续性在包括无 AI 对照的所有组均上升；决策冲突、自主感及未来自我连续性的**组间变化没有显著差异**。单组内部显著变化不能作为 AI 相对对照的额外效果。评价性逻辑及人生意义的主观评分高于情感/视觉维度；这是用户感知偏好，非客观决策收益。

## 4. 独立可复算的 Fisher 精确检验尾部审计

只使用原论文披露的组样本量和整数比例，采用 Python 标准库 math.comb 对固定边际的 2x2 超几何分布精确枚举，未使用原作者代码或参与者微观数据。对方向性假设使用 upper-tail，对 two-sided 使用“概率不大于观察表概率”的常见双侧定义。实算结果：

| 比较 | one-sided greater | two-sided exact | 原论文 p |
| --- | ---: | ---: | ---: |
| 双未来自我 vs 对照 | 0.014959996 | 0.025796905 | 0.015 |
| 新选项 C vs 对照 | 0.019333392 | 0.029677416 | 0.019 |
| 单独 A vs 对照 | 0.165433868 | 0.309076333 | 0.068 |
| 单独 B vs 对照 | 0.148681727 | 0.263383134 | 0.054 |

前两项论文 p 与**单侧**精确检验吻合，明显不同于常见双侧定义。论文正文只写 Fisher's exact test，未在所读段落明确尾部选择或事前方向假设。单独 A/B 两项从披露的二元比例不能复现论文 p，可能涉及其他分类/比较或分母，需原始列联表和分析代码确认。不能仅凭这一局部核对认定原作者计算错误，也不能把论文 p 自动称为双侧检验。多个条件和终点的全族多重比较调整未核实；两项双侧未经调整 p 均低于 0.05，但该事实不足以完成预注册确认。

可复算的最小标准库计算：
```python
from math import comb

def fisher(a, n1, b, n0, alternative="two-sided"):
    total, success = n1+n0, a+b
    lo, hi = max(0, success-n0), min(n1, success)
    def prob(x):
        return comb(n1,x)*comb(n0,success-x)/comb(total,success)
    observed = prob(a)
    if alternative == "greater":
        return sum(prob(x) for x in range(a, hi+1))
    return sum(prob(x) for x in range(lo, hi+1)
               if prob(x) <= observed + 1e-12)

for label,a,n1,b,n0 in [
    ("dual",13,38,4,37), ("third",8,40,1,37),
    ("single_A",7,38,3,37), ("single_B",6,39,2,37)
]:
    print(label, fisher(a,n1,b,n0,"greater"),
          fisher(a,n1,b,n0,"two-sided"))
```
本轮上述四组八个数值已在本地计算并用 SciPy fisher_exact 对照一致。属于发表聚合数值的独立小范围审计，未做原始实验复算、未触发 CI。

## 5. 2024 年论文及跨版本身份异常

2024 年 arXiv v4 论文明确记载最初 400 人，剔除注意力检查失败及技术问题后 344 人；四组为 Future You 73、问卷 76、普通聊天 103、无干预 92。其主要结果为立即自报负面情绪和未来自我连续性改善，长期执行行为没有检验。对照普通聊天的焦虑 post-hoc p=0.059，不能按常用 0.05 标准声称显著优于普通聊天。乐观、未来后果考虑、自尊、自我反思、洞察等多项组间检验未显著。

同一 MIT 官方项目概览仍称“188 participants”，MIT 正式出版页明确“N=344”，原文表中四组也合计 344。188 与 344 的关系未解释，不能推测为另一次试验或某个子样本。原论文正文部分单因素 ANOVA 使用 F(3,376)，若严格对应 344 人四组完整案例，经典组内自由度应为 340；数据子集/文稿版本或排版原因未证实，保留为报告一致性待核，避免擅自修订统计结果。

2024 年论文声明 AsPredicted #157535 预注册，直接访问该编号的可公开 PDF 未成功；无法独立确认初始登记时间、排除规则及终点冻结。2025 年 N=192 论文在已读正文未见可验证的预注册 URL；多终点选择和单/双侧检验事前规则仍 UNKNOWN。2025 年 N=92 模态实验为另外一个样本，且同属部分相同研究团队，不能视为外部独立团队复制 N=192 决策行为效果。

## 6. 科研治理 E 当天增量与开放 PR

已核 2026-11-02 的 E167 完整实质只读审计，故本轮不重复 E 编号。最新 R/B main 在本轮写入前为 4bf847a9617d6aa6473f7dec147955d096a98673。R180 08-004 最新报告完成 R177 上游来源与 30 人工世界 210 个精确矩的有限 E1 内部审计；正式 original239 逐项采纳仍 PARTIAL，真实 E2/历史 E3 新增 0。理论轨最新 TH212 Kermack/McKendrick 1927 印刷公式核查属于理论/原始历史文献审阅，未提升 R 科研等级。

队列与交叉索引重新读得 Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f 和 36f24235901172642c46853298aebb421f1a3552，较前轮无变化；最近 R/B 原始记录为待核154（P0=27，P1=82，P2=45），本轮文件级净减少0，未把 R180 复核当成自动关闭。R272 生产归档前像/优化模式完整性 P0 保持开放；R333至R340 生产组合入口强制调用缺口继续开放，先前观察为0/8，本轮未重复原生执行。R073 与 PESEN v0.1 冻结保持。

本轮 GitHub PR collection 实查 12 个 open，全部 Draft，未合并；PR #3 仍为 R257 S53 严格数学收据候选，和 main 的 compare diverged，main 独有1172提交、PR独有1提交。PR #8 R170 全状态复核存在历史 witness 排序歧义，PR #9 历史身份门依赖 #8 的证据，均未达到自动合并授权/科学验收条件。本轮没有改 PR、共享队列或冻结协议。

## 7. F 本周安全状态、费用与下一步

F010（2026-W45）已实质完成，Git blob b703777cd33fc72197e0368cc2f209e51e5dc420，本轮只读。新发现的高风险机制是**单侧未来自我叙事可能诱导即时选择改变**，而改变是否有益完全未知。研究候选要求：同时展示不同路径、明确标注虚构情景、可质疑/编辑模型叙事、保留用户延后和拒绝决定权，并独立测试“选项 C 是真实可行的新机会还是模型幻觉”。这属于方法问题，不等于已经部署的安全保证。

F 额外关注可识别照片、语音克隆、家庭与财务愿景等敏感数据及跨服务传输。没有访问用户个人资料、没有运行产品、没有新建 F 编号。MIT 项目 FAQ 的匿名化声明未经独立验证，实际删除/导出/第三方撤销为 NOT_RUN。

使用公开免费英文原始资料、GitHub 连接器只读和本地 Python 标准库。没有购买产品/论文、调用收费 API、运行云/GPU或主动触发 GitHub Actions。账户账单与免费 CI 额度 NOT_VERIFIED，故不启动 CI。当前 main 在写入前查询 check-runs=0、workflow runs=0、combined statuses=0；只表示指定 HEAD 的查询结果。

next_action: 优先获取 2025 N=192 论文真实列联表、原始代码或预注册记录，解释 Fisher 检验单/双侧及单独 A/B p 值差异；寻找由独立团队执行、测量真实决策实施及长期福利的比较试验。若无新证据，转向非同团队的真实产品；E 继续只读追踪 R272 P0 和 R333至R340 强制接入，F 保持本周 COMPLETE，不启动个人产品开发。
