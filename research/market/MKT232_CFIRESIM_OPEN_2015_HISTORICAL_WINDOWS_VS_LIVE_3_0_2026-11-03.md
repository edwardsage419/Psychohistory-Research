# MKT232: cFIREsim 历史开源引擎与现行3.0的版本分离、重叠历史窗口及成功率口径

track: market
subflow: commercial_product_mechanism_and_external_validity
run_date_utc: 2026-11-02T22:18Z
local_date: 2026-11-03 Asia/Singapore
target_key: (market,cFIREsim-open-vs-cFIREsim-3.0,master-c7c4ba4+2020-12-01-official-3.0-announcement,historical-window-denominator+stale-data+source-version-identity)
observed_main_before_write: 79d3b0cca2d814e73c35f82b7c0b49fd47a2bb05
status: COMPLETE_BOUNDED_PRIMARY_SOURCE_CODE_AND_OFFICIAL_PRODUCT_REVIEW
evidence_grade: MARKET-E1_PRIMARY_OPEN_CODE_AND_VENDOR_PRODUCT_DOCUMENTATION
current_production_runtime: NOT_RUN
historical_full_runtime: NOT_RUN
local_arithmetic_check: COMPLETE_SYNTHETIC_WINDOW_COUNT_ONLY
product_specific_human_RCT: NOT_VERIFIED
independent_long_term_decision_improvement: NOT_VERIFIED
participant_level_data: NOT_ACCESSED
new_R_E2_E3: 0
CI: NOT_RUN
account_billing_and_free_Actions_quota: NOT_VERIFIED
paid_operations: NONE

## 1. 选题去重与独立增量

先检查市场目录。MKT002、MKT027、MKT171至MKT174及MKT206已多次分析ProjectionLab的抽样、相关性和成功率；MKT200至MKT202已完整登记Goda等2023退休计算器随机试验及174美元的使用者效应、61.055美元且不显著的全部受邀者ITT效应。此次查到该RCT的LSE作者版本，但未将同一实验另计一次，也未重复建立统计研究编号。

本轮改为直接阅读另一真实退休规划产品cFIREsim的原作者公开源码和现行网站，识别旧开源参考实现与当前线上产品的实际版本断层，核对历史窗口分母及数据年份。cFIREsim的这一目标键此前市场目录无专门研究文件。

## 2. 来源身份与产品代际

原作者仓库： https://github.com/boknows/cFIREsim-open
仓库master最近提交 c7c4ba441830c1da457b663d2e602567306e8459，GitHub API提交时间2020-12-22T18:14:17Z。README Git blob b8356c937d1a4d81c03197aebf3a9ecd7c4c00ee，明确声明现行cfiresim.com已重写且闭源，旧项目仅作参考，许可证Apache-2.0。许可证文件确实包含Apache License Version 2.0。

现行官方网站： https://cfiresim.com/about/ 。2020-12-01作者公告明确3.0以Python/Django重写，历史数据改为自动更新，并把旧版本每步两位小数的计算精度改为显示前保留10位以上。2026-11-03读取到的现行网站 https://cfiresim.com/ 提供无需输入账户的模拟表单。该页面当前可访问不等于生产服务源码、数据更新任务、实时输出或账户隐私已被独立验证。

**版本边界**：本轮下述Git blob、历史数据质量问题和循环实现只属于旧公开参考仓库。不可据此指控现行3.0含同样代码或问题。现行生产源码、历史数据实际更新日期及精度未独立运行核验。

## 3. 实际输入、状态、目标、算法、反馈

旧源码js/cFIREsimOpen.js Git blob ac89710d7aaf32f325014011ed3812bf577cda1f。用户输入退休起止年份、起始资产、年度支出、股票债券黄金现金配比、再平衡、费用、额外收入和支出及不同提款规则。js/spendingModule.js Git blob 080ac7e82c328fd7fe4856fbbfa504eb513dbeee，直接实现通胀调整、组合资产百分比、可变支出及上下限等提款方法。

旧引擎按历史年份构造一组完整年度路径，逐年扣除支出、应用额外现金流、计算市场收益与期末资产。js/statsModule.js Git blob 2bbaaa38dab454be5a893fc798a9fc92462fa3a2，计算每条路径中是否出现通胀调整后资产小于零；successRate=(1-failed_cycles/total_cycles)*100。js/cFIREsimOpen.js 的calcFailures也按任一年期末资产小于零记整条路径失败。

现行网站仍提供退休时间、资产、提款策略、资产配比、历史区间及调整项目等输入，输出历史路径成功率和资产走势。其公开说明把失败定义为资产跌破零。未取得现行生产源码和原始用户行为研究。

## 4. 可独立核对的旧版本数据边界与数学增量

旧市场数据文件 js/marketData.js Git blob 46378eb867d9c589a6003ba3eaa26cadcbff9692，按年度提供1871至2015共145个键。末尾2014和2015的cpi、dividends、fixed_income、gold、growth及cape值逐项完全相同。该重复是源码可观察事实，具体原因及对真实回测输出的影响尚未复算。它提示旧数据版本需要来源与更新审查；不能当成现行3.0数据错误。

旧runSimulation按历史连续窗口产生路径。若以该旧数据集选30年窗口，算术上有145-30+1=116个起始年份窗口，首窗口1871至1900，末窗口1986至2015。相邻窗口共享29个年份，重叠率29/30=96.67%。本轮用本地Python标准库生成1871至2015整数年份并断言116个长度30的窗口、相邻交集29、末窗口边界，全部通过。该检查只验证组合算术，**没有执行原作者完整JS模拟器、没有复算任何真实退休成功率**。

因此历史窗口成功率的分母是选定数据和规则下的历史路径数。相邻路径高度重叠，不能按116次独立未来试验计算标准误，也不能把95%历史通过率直接表述为经前瞻校准的95%个人未来成功概率。历史样本外结构变化、制度、寿命、税费、支出行为和资产收益分布均可能改变实际结果。

现行官网 https://cfiresim.com/about/ 2020-12-01的3.0说明明确当前数据自动更新、旧版计算舍入方式已更改；这些信息强化了历史代码不能作为现行服务的生产审计证据。

## 5. 与ProjectionLab和真人外部证据的隔离

ProjectionLab官方 https://projectionlab.com/monte-carlo 披露历史回测与可自定义概率分布的Monte Carlo路径，并允许检查各条路径；2026-11-03官方定价 https://projectionlab.com/pricing 显示Basic每年0美元、Premium每年129美元、Pro每年549美元。官方 https://projectionlab.com/security 2026-08-12说明计划存储于Google Cloud Firestore，可导出与删除，且云基础设施认证不等于ProjectionLab本身已取得同一认证。该产品的详细方法与证据已归档MKT206，本轮仅作机制对照，不重做模拟测试。

cFIREsim的公开历史代码可以审计旧算法与数据，当前服务是否可逐项复现仍UNKNOWN。现行cFIREsim网站有公开可访问表单及链接式模拟回访说明；正式价格、生产部署代码、数据导出和实际删除结果未核验。ProjectionLab有付费商业规划功能、云端计划存储和官方导出声明。两者均无本轮直接验证的产品专属真人因果效果、未来概率校准或长期净福利证据。

既有MKT201/MKT202的OPM退休计算器随机试验仍为独立相邻机制研究，**并非cFIREsim或ProjectionLab产品效果**。同一实验不增加第二份RCT计数。

## 6. E当日治理与F本周状态，只读

本地2026-11-03已有E168实质治理报告，故本轮不新建E编号。R/B最新R127 05-003第二次490格原始论文表格视觉复查仍为同一代理非盲复核；未达到外部独立复现，正式队列保持PARTIAL。理论TH217在本轮并发增加原始回复文献校勘交接，与市场目标无交叉改写。

本轮只读核验R272生产YAML blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d，仍含contents:write及git push，且未调用单入口候选；P0保持OPEN。main分支查询protected=false。R333至R340组合强制验收尚无关闭证据。PR #1至#12查询仍全部open、Draft、未合并；最近更新的PR #12是R266非盲归档审计，PR #11是R270前缀DP审计，均未提升主线科研等级。PR #3相对本轮主线基线为main独有1224提交、PR独有1提交，处于diverged状态；PR #8/#9历史身份依赖继续待审。

original239待核CSV blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f及crosswalk blob 36f24235901172642c46853298aebb421f1a3552均未变化。最近完整核验队列154项，P0 27、P1 82、P2 45，本轮文件级净闭合0；本轮未再次逐行重算。R073与PESEN v0.1继续冻结。

F010为2026-W45已完成的价值权重、实质人工控制与数据生命周期专题。本轮只读：历史模拟器提供回访链接的做法需未来检查链接访问权限、分享时输入暴露、撤销和删除范围；本轮没有真实个人数据、登录、链接安全探测或删除实验，不新建F编号。

## 7. 证据等级、费用与下一步

MARKET-E1：原作者固定Git blob直接阅读、2020官方版本公告、当前网站公开机制与价格。旧源码结构与数据重复是可审计的静态事实。
LOCAL_SYNTHETIC_ARITHMETIC：145年数据、116个30年窗口、相邻29年重叠的标准库算术验证，不构成生产代码运行或概率校准。
MARKET-E2：cFIREsim或ProjectionLab自身真人决策改善证据NOT_VERIFIED；既有OPM实验在MKT201/MKT202归档，保持原等级。
MARKET-E3：跨环境长期个人福利与独立概率校准NOT_VERIFIED。
R E1/E2/E3：本轮新增0。

无注册、购买、付费API、云/GPU或Actions触发。实际GitHub账单和免费额度NOT_VERIFIED，因此CI保持NOT_RUN。未读取任何个人财务、健康或关系数据。

next_action: 优先寻找一个能够免费复算的现行开源人生/财务规划引擎及其公开版本化测试，核查不同历史数据截止年、重叠窗口和模型假设下的结果稳定性；随后寻找真实产品用户的独立行为或长期损失指标。E继续等待R272权限和强制完整性门由R主线及owner审查，F本周只读。R模型全部完成前不开展统一分类、熔炼或个人产品开发。
