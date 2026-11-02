# MKT219: Jobnet 职业建议的直接收益、拥挤外部性与论文版本漂移

track: market
subflow: 真实非医疗决策辅助产品与外部因果效果
run_date_utc: 2026-11-02
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Jobnet,2019-field-RCT+2022-IZA+2023-author-draft+2026-accepted-paper,direct-benefit-vs-congestion-spillover-and-version-specific-numerics)
baseline_main: a53c6904a5772919742ee48d1e7b69b6a3cd825d
status: COMPLETE_BOUNDED_PUBLIC_PRIMARY_PAPERS_AND_OFFICIAL_PRODUCT_DOCUMENTS
evidence_grade: MARKET-E2_DIRECT_RANDOMIZED_FIELD_EXPERIMENT_WITH_ADMINISTRATIVE_OUTCOMES
2026_published_full_text_checked: BLOCKED_PAYWALL
original_participant_data_reanalysis: NOT_RUN
original_recommendation_code_execution: NOT_RUN
current_2026_product_RCT_transport: NOT_VERIFIED
real_personal_data_accessed: NO
new_R_E2_E3: 0
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
paid_actions: NONE

## 一、选择原因及去重

此前 MKT211 至 MKT218 已覆盖行为追踪、数字疗法、医疗决策辅助、承诺合同及储蓄目标。此次转向职业选择的真实收入和就业结果，研究数字建议是否因竞争与规模扩大而失效。检索当前 research/market 文件名未见 Jobnet 或该论文专门审计。本次是不同产品、不同结果及不同证据缺口，不沿用旧 MKT 的人工实验编号。

## 二、实际产品及输入到结果的机制

研究对象是丹麦公共就业平台 Jobnet 的 2019 年实验性个人 dashboard。Jobnet 是公共就业服务，不应归类为商业收费 SaaS。实验版本与 2025 年官方界面改版后的现行版本须分开。

1. 用户输入：失业登记时提供感兴趣的职业清单，约 1,020 种职业分类，系统已掌握居住邮编。求职者还可修改职业偏好，登记求职活动。
2. 空缺信息卡：显示其已选职业在居住地周围 50 公里内的空缺数，按日更新，数据来自 Jobnet 招聘数据库。
3. 职业推荐卡：每次登录从个人已有职业中随机选一个，以 2013 至 2016 年丹麦成功失业转就业的职业转移记录建立各来源职业最常见的五种去向，排除已在个人清单中的职业，最多展示三个备选职业。研究描述另考虑当前岗位空缺和教育匹配限制。用户可点击查看相关空缺或更改职业清单。
4. 反馈：用户在平台继续记录实际申请，研究以行政记录链接 12 个月就业、工时和劳动收入。没有发现实验 dashboard 对个人长期目标的预测概率校准或可审计个体福利函数。
5. 机制公开程度：上述规则来自作者研究正文；原始线上推荐代码、全部排序细节、2026 当前算法及运行配置未取得，不能声称源码级复现。

官方现行 Jobnet 帮助页确认 CV、职业偏好、职位匹配和 Joblog 等功能。2025 年 10 月改版页面也有官方公告；不能把 2019 年研究中的实验卡片直接当作 2026 年生产功能。

## 三、真实随机试验设计与可观察结果

Altmann、Glenny、Mahlstedt、Sebald 的研究对 2019 年 3 月 17 日登记的 92,098 名丹麦失业保险领取者进行双层随机化。98 个市镇分为：10 个纯对照市镇 10,100 人；44 个 60% 处理分配市镇 45,232 人；44 个 90% 处理分配市镇 36,766 人。个体在对照、职业推荐、空缺信息、联合干预四组之间随机分配。12 个月的就业、工时、收入来自行政数据。2019 年实验到 2020 年 3 月的窗口大致在丹麦疫情首次封锁前结束，仍需留意其他宏观变化及外推限制。

核心发现：

* 职业推荐使用户申请更多推荐职业；空缺信息使用户更加集中于原有目标职业。联合提供两种信息没有形成简单相加的效果。
* 低处理密度地区的就业和收入存在正向效果。随着更多求职者收到类似建议，同一职业的申请竞争增加，直接收益下降，接近全面覆盖时部分估计归零。
* 这说明算法推荐的效果依赖其他用户收到的建议。个人建议的局部有效性与全市场推广后的净收益必须分别衡量。现有试验没有测量个人主观生活满意度、长期职业适配或整体人生福利。

## 四、重要的跨版本数值漂移

必须保存来源版本，严禁把不同稿本的数字合并为一个稳定估计：

| 来源版本 | 本轮直接可确认的表述 | 统计口径限制 |
| --- | --- | --- |
| 2022-12 IZA DP15830 免费全文 | 低于 50% 处理比例地区，工时和收入约增加 8.5% 至 9.5%；高于 75% 处理比例时效果大致抵消 | 2022 工作论文数值及其区域定义；不能标为 2026 正式数值 |
| 2023-09 作者网站公开修订稿 | 处理密度分布最低三分位的收入和工时增加约 4.0% 至 4.5%；最高三分位时效果大致抵消 | 修订稿使用通勤流量加权的处理强度及三分位口径；与 2022 的阈值口径不同 |
| 2026-10-12 Review of Economic Studies 接受稿公开摘要 | 限制覆盖率时就业与收入改善，覆盖率上升时效果衰减甚至消失；未给出百分比 | 同行评审接受稿全文在本轮显示收费；不能用旧数值替代最终数值 |

因此，研究的定性外部性方向跨版本一致；定量效果仍是版本特定证据。上述 8.5% 至 9.5% 与 4.0% 至 4.5% 的差异不能直接解释为同一估计的统计误差或论文造假，分析定义与稿本发生变化。正式稿具体表格及稳健性未经审阅。

## 五、证据分级、利益与商业局限

MARKET-E2：真实产品中的大规模随机现场实验，且有客观行政结果。研究者及丹麦公共就业机构合作，研究经费来自丹麦就业部；不能宣称完全脱离实施机构的外部团队独立复现。正式稿于 2026-08-03 接受、2026-10-12 在线发布。原始个体数据、算法源码及 2026 正式表格独立复算 NOT_RUN。长期福利、跨国家文化环境迁移、2025 改版后产品效果均 NOT_VERIFIED。

平台面向丹麦求职者，公共服务和行政数据条件与独立消费者应用差异较大。没有采购、注册或登录任何账户。官方帮助页面说明 Joblog 可以记录求职行为、上传 CV 和申请材料，因而隐私及访问权限属于高敏感治理问题；实际删除、第三方访问、保留时限均未实测。产品价格对照：官方公共服务页面未给出与独立付费产品可比的订阅价格，本轮不推断零成本部署或商业授权条件。

## 六、与 E/F 的交叉边界

E：2026-11-02 已有 E167 当日实质审查，维持其 COMPLETE。最新 R272 审计确认 wrapper 自检在三种身份守卫被单独删除时仍可假通过，属于合成错误注入证实的自检覆盖缺陷；原 wrapper 的未改动生产假接受未被证明。R272 生产 P0 仍开放。R333 至 R340 八份工作流中组合入口强制调用 0/8，原生完整仓库组合验收未完成。original239 队列 Git blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，交叉索引 Git blob 36f24235901172642c46853298aebb421f1a3552；当前读取 154 行，P0=27、P1=82、P2=45，文件级净变化 0。开放 PR 12 个均 Draft；PR #3 对本轮 main 比较为 main 独有 1158 提交，PR 独有 1 提交，来源身份及历史盲态验收未完成。不得自动合并。

F：F010 本周独立专题已完成，本轮只读。Jobnet 案例补充算法建议的群体外部性、公共行政数据访问与人工职业选择权三个未来方法问题。没有新增 F 编号，没有访问个人健康、财务或关系记录，没有开展安全部署或删除测试。

## 七、可执行下一步

1. 优先寻找 2026 接受稿的作者免费合法版本或公开补充材料，逐项核对表格和区域处理强度定义；付费访问 BLOCKED，直接跳过收费。
2. 比较另一独立求职推荐随机试验，重点考察是否也发现竞争拥挤及收入影响，避免把单项丹麦结果普遍化。
3. E 只读跟踪 R272 身份守卫自检覆盖、原归档先验证后生成，以及 R333 至 R340 的原生验收和强制调用。等待 R/B 主责修复及可信执行收据。
4. 维持 R073、PESEN v0.1 及全部 R 系列先完成、统一分类随后进行、有条件熔炼最后开展的冻结顺序。

## 实际直接读取的免费非中文来源

* 2022 IZA DP15830 原始全文：https://docs.iza.org/dp15830.pdf
* 2023 作者网站修订稿全文：https://www.robertmahlstedt.com/media/files/agms_search_advice.pdf
* 2026 Review of Economic Studies 接受稿摘要（全文收费，未购买）：https://academic.oup.com/restud/advance-article-abstract/doi/10.1093/restud/rdag112/8909591
* 2026 期刊官方发布记录：https://www.restud.com/the-direct-and-indirect-effects-of-online-job-search-advice/
* Jobnet 官方帮助与当前功能：https://jobnet.dk/hjaelp-og-support/hjaelp-og-support-til-jobnet
* Jobnet 官方职位匹配说明：https://support.jobnet.dk/ofte-stillede-spoergsmaal-fra-borgere/jobsoegning/hvor-kommer-jobforslagene-paa-min-forside-fra
* Jobnet 2025 年改版公告：https://support.jobnet.dk/information/nyt-jobnet-den-17-19-oktober-2025
* Cornell Job Search Lab 试验索引：https://jobsearchstudies.ilr.cornell.edu/papers/f80a5e0a-1914-43ae-b11a-02b1e2250b81/

本文件为公开资料的只读研究报告。没有运行商业应用、独立原始数据复算、真实用户实验、付费服务或 GitHub Actions。历史提交 [skip ci] 不代表已验证账户账单或免费额度。