# MKT238 自我约束产品：采用率与行为效果的独立实验对照

track: market
subflow: commercial_product_research
run_date: 2026-11-03 UTC
target_key: (market,Beeminder-and-deposit-commitment,2015-NEJM-and-2024-PSE,uptake-versus-behavioral-effect)
observed_head_before_write: ad09a93dcabea2014fb4dcee874fd8274f733c3b
status: COMPLETE_BOUNDED_LITERATURE_AUDIT
evidence_grade: MARKET-E2_AUTHOR_REPORTED_RANDOMIZED_HUMAN_STUDIES
native_product_execution: NOT_RUN
participant_level_replication: NOT_RUN
ci_status: NOT_RUN
billing_checked: account balance NOT_VERIFIED; no paid API or Actions requested

## 研究问题与产品对应

Beeminder 官方 FAQ 描述：用户选择单位和目标速率，输入数据点，系统计算相对红线的安全缓冲；越线后核对并收取预先承诺的金额，通常自动提高下一次承诺金额且允许调整上限。目标归档有延迟，永久删除可请求人工处理。产品官方机制：https://lovelace.beeminder.com/faq 。此处仅确认官方公开机制，未验证线上支付、数据删除和生产实现。实际输入为目标、速率、数据点；状态为累积进度与安全天数；反馈为偏离提醒和承诺金损失。算法的完整生产代码与长期真人净福利效果均未独立确认。

## 独立研究一：2015 NEJM 五组随机试验

来源：Halpern et al., Randomized Trial of Four Financial-Incentive Programs for Smoking Cessation, NEJM 2015, DOI 10.1056/NEJMoa1414293, https://www.nejm.org/doi/abstract/10.1056/NEJMoa1414293 。公开结果：总计2538名参与者；2070人分配至四种激励方案，1060人接受所分配的方案（51.2%）。奖励方案接受率90.0%，押金方案13.7%，差76.3个百分点，比例约6.57倍。作者报告各激励方案均提高持续戒烟，但押金方案因接受率低，整体效果低于奖励方案；在愿意接受两类方案的人群的分析中，押金方案效果可能较强。后者依赖选择/模型假设，不能替代全体随机分配比较。押金为150美元，相关奖励总额与具体设计不同于Beeminder。没有将研究结果归因于Beeminder。

## 独立研究二：2024开放获取随机试验

来源：de Buisonjé et al., Less stick more carrot? Increasing the uptake of deposit contract financial incentives for physical activity: A randomized controlled trial, Psychology of Sport and Exercise 70 (2024) 102532, DOI 10.1016/j.psychsport.2023.102532, https://doi.org/10.1016/j.psychsport.2023.102532 。137名健康学生随机分入2×2设计，操纵押金是否匹配奖励与押金是否允许自定。20天步数目标；总体押金接受率83.2%，接受者113人平均完成14.9/20日目标。匹配奖励提高接受赔率 OR=4.08 (p=.010)；自定押金提高接受赔率 OR=3.53 (p=.022)。两种操纵对目标完成率的主要效应均未显著：匹配 p=.752，自定 p=.143。作者提醒四项组合干预不能单独归因于押金；样本为年轻学生，持续时间短，疫情限制可能影响活动。83.2%与NEJM 13.7%来自不同人群和合同条件，不能直接解释为某一种机制改善69.5个百分点。

## 研究判断与未来指标

在自我约束产品中必须将四项结果分开：提供功能后愿意采用的比例；采用者实际使用程度；全体被分配者的客观目标完成；扣除损失金额、压力、退出成本后的净福利。提高采用率未必提高目标完成，短期完成目标也不能自动推断长期人生改善。产品目标应允许用户撤回并检查退出成本，尤其不能默认罚金越高越好。

证据层级：厂商FAQ为MARKET-E0/E1机制披露；两项已发表随机实验的作者报告为MARKET-E2；未取得Beeminder产品专属随机效果、参与者级数据复算或MARKET-E3跨场景独立复现。本文不涉及R系列E等级。

## E与F只读关联

2026-11-03 已有 E168 正式治理审计及 F010 本周专题，故本轮不重复建立E/F编号。检查时 main HEAD=ad09a93dcabea2014fb4dcee874fd8274f733c3b；开放PR 12项均draft，main protected=false。R272生产完整性问题未有关闭证据，保持OPEN；未重算待核队列，净变化UNKNOWN。F专题可保留自愿性、撤回、罚金压力及数据删除为后续原则审查点；没有接触个人敏感数据。

## 限制与下一步

本轮基于公开官方FAQ、期刊页面摘要及开放研究正文搜索结果，未取得原始数据，也未验证所有附录统计。下一步优先调查Beeminder或其他目标偏离产品是否有产品专属、外部独立、预注册的随机效果研究。无此证据时转向其他产品，不连续堆叠同类编号。
