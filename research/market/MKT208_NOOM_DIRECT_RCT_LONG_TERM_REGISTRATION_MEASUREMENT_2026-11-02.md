# MKT208：Noom两项直接随机试验，长期结果、测量与注册时序审计

track: market
subflow: 真实产品机制与真人决策行为证据
run_date_utc: 2026-11-01T21:20:00Z
local_date: 2026-11-02 Asia/Singapore
target_key: (market,Noom-Weight+Noom-Coach-DPP,2020-RCT+2026-RCT,measurement-quality-and-registration-prospectivity)
baseline_main: 60188e7151727ec941d2cdf6df95a412e5c89f6c
status: COMPLETE_BOUNDED_LITERATURE_REVIEW
market_evidence: MARKET-E1_OFFICIAL_PRODUCT; MARKET-E2_DIRECT_PRODUCT_RCT_SPONSOR_LINKED
external_independent_reproduction: NOT_VERIFIED
product_runtime: NOT_RUN
algorithm_source_replay: NOT_RUN
new_R_E2_E3: 0
ci: NOT_RUN
billing: NOT_VERIFIED
personal_sensitive_data: NOT_ACCESSED

## 研究问题与产品机制

前轮MKT200至MKT207已研究债务、退休规划、价值评分、承诺、反馈、情景模拟和Exist。此轮转向直接归属在售产品的随机试验。Noom Weight以用户输入的体重、食物和活动日志为状态数据，提供食物数据库、目标追踪、行为心理课程、反馈、群体支持与不同版本的教练支持。2026年试验版本提供16周自我监测、课程、个人教练和群体支持，对照组收到16封健康教育邮件。2020年Noom Coach DPP版本还提供每日挑战、自动反馈、教练互动及DPP课程。两版机制、目标人群与测量不同。完整生产推荐算法、个性化参数和源代码本轮未取得。

2026年Noom官方定价列出美国4个月169美元、6个月179美元、12个月209美元，预付并自动续费，渠道和促销可能影响价格。官方数据帮助说明用户可申请导出，通常30天内提供；账户删除通常30天内处理，活跃订阅、导出请求和法律保留可能构成例外。以上属于官方政策声明，实际清除效果未测试。未注册、购买或输入私人资料。

## 2026年Noom Weight直接RCT，68周随访

McCallum et al. (2026), Obesity Science & Practice, DOI 10.1002/osp4.70122，2026年3月13日首次发表。2022年6月至8月招募，2023年12月结束。随机分配427人，干预217、教育控制210。排除15名缺失或不可靠基线记录后，分析412人，干预211、控制201。文章称ITT并采用潜变量增长曲线FIML处理缺失；严格随机总体与排除后的分析集应分开记录。16周留存197/211与188/201，68周183/211与174/201。

16周体重相对基线模型变化为干预负1.2%、控制正0.6%，组间约1.8个百分点，p=0.001。68周为干预负4.1%、控制正1.5%，组间约5.5个百分点，95% CI 3.0至8.0，p<0.001。68周达到至少5%减重比例41%对19.5%。这是16周干预结束后52周的随访，未证明每名参与者都停止所有其他支持。

重要限制：体重由参与者使用各自体重秤自报，运动量使用IPAQ自报，未由统一设备独立测量。68周高强度活动组间差24.04分钟，95% CI 1.30至46.77，p=0.038；久坐、步行、中等活动差异未显著。饮食失调风险和身体欣赏量表两组均改善，组间差异分别p=0.119和p=0.582，无法归因于Noom特有机制。论文承认外部支持未测量、样本偏向高学历白人女性、未拆分教练和追踪等组件的独立因果作用。

利益冲突：研究由Noom Inc.资助，全部作者曾为或当时为Noom员工或承包商，部分有股票期权。去标识数据仅按申请提供，未取得独立复算。

**注册时序风险**：论文引用NCT06666842。两个ClinicalTrials.gov公开记录镜像显示研究2022年6月开始、2023年12月完成，首次提交注册2024年10月29日、首次公开2024年10月31日，晚于研究结束约10个月。原始ClinicalTrials.gov动态页面本轮未能直接核对历史版本，以上日期为两个二次镜像一致结果。注册时间晚于完成时间意味着公开登记不能直接充当随机前预注册证据；不能据此断言作者更改过终点。原始伦理协议、统计分析计划及注册历史仍待独立审阅。

## 2020年Noom Coach DPP直接RCT，临床测量对照

Toro-Ramos et al. (2020), JMIR mHealth and uHealth 8(7):e17842, DOI 10.2196/17842, PMCID PMC7381044。论文报告202名糖尿病前期成人随机招募，列出的干预101和对照99合计200，两人的口径差异待进一步查CONSORT。对照为通常医疗护理和纸质DPP教材。

体重在门诊随访记录于电子病历，HbA1c由临床实验室或少量诊所即时检测取得，测量来源强于2026年全自报体重。ITT 6个月组间体重差负2.64 kg，SE 0.71，p<0.001；12个月负1.80 kg，SE 0.81，p=0.01。HbA1c组间6个月差0.004%，p=0.94，12个月差0.006%，p=0.93，均未显示显著改善。课程完成者12个月平均减重4.7%，属于依从者分析，不可替代随机总体估计。食物日志与称重频率的关联不能证明组件因果效果。

作者含Noom雇员，原文披露工资、股票期权及专利利益。NCT03865342公开镜像亦显示2019年3月首次公开，晚于2018年6月研究结束，原始注册版本仍待核对。2020与2026是不同人群和版本的两项直接产品RCT，不能合并为同一因果估计，也不能将2026自报减重等同2020临床测量。

## 科学边界与未来研究价值

产品级随机化支持评价组合干预，尚不能区分课程、日志、教练、群体支持各自贡献。应分别保存干预期、停用后的随访、实际使用强度、客观行为、临床结局、主观满意度及长期福利。体重改善不能自动推断HbA1c、整体健康或跨人生领域多目标决策改善。两项研究均为MARKET-E2直接真人随机证据，商业利益、登记时序和测量局限需独立评分；与R系列E2/E3无关。

## E每日治理只读增量

本轮起始main 60188e7151727ec941d2cdf6df95a412e5c89f6c。最新R179 08-003独立V8内部人工E1审计报告核对90世界、810人工计数、540世界汇总及13项变异拒绝；历史CI run 39555471118三作业成功是既有报告所述，本轮未重做B数学验证。原239该项正式逐项验收PARTIAL，完整本地Node CLI NOT_RUN。理论轨最新TH204 1945 Bengal月度流量研究已交接，C010当日及D003本周据交接为COMPLETE。

原239待核队列blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f，crosswalk v7.8 blob 36f24235901172642c46853298aebb421f1a3552，均与前轮一致。最近直接核验154项，P0 27、P1 82、P2 45；本轮文件级净减少0，未重新进行逐项科学验收。

实时GitHub返回12个开放PR，全部Draft，均未合并。PR #1与#3的R257 S53错误接受及来源身份问题继续开放，PR #10仍为未合并候选。PR #3 head 97d5f74df5d84916917db943156120f08144f445 与本轮main比较diverged，main独有1109提交，PR独有1提交；版本差异不能直接证明合并冲突。R333至R340组合验收完整真实仓库原生执行NOT_RUN，八工作流强制接入PARTIAL，P0仍开放。无跨轨写入、合并、强推、协议改动。

F010已完成2026-W45人类实质控制和数据生命周期专题，本轮仅将Noom官方导出删除说明作为产品对照。实际安全测试NOT_RUN，没有新增F编号。

GitHub Actions本轮未启动。历史workflow runs总数846来自仓库查询，不能解释为本轮CI。账户账单和免费额度NOT_VERIFIED，未购买产品、数据或API。R073及PESEN v0.1保持冻结。

## 实际阅读的免费英文来源，访问2026-11-02

1. https://onlinelibrary.wiley.com/doi/full/10.1002/osp4.70122
2. https://mhealth.jmir.org/2020/7/e17842/
3. https://pubmed.ncbi.nlm.nih.gov/32459631/
4. https://ichgcp.net/clinical-trials-registry/NCT06666842
5. https://www.syfrah.com/trial/NCT06666842
6. https://ichgcp.net/clinical-trials-registry/NCT03865342
7. https://www.noom.com/blog/weight-management/noom-cost-2/
8. https://www.noom.com/support/faqs/privacy-and-data/2025/10/how-to-export-and-delete-your-noom-data/
9. research/validation/R179_08_003_ORIGINAL239_INDEPENDENT_90WORLD_EXACT_AUDIT_2026-11-02.md
10. research/coordination/r/20261101T144238Z-r333-r340-composite-candidate-handoff.md
11. research/coordination/theory/20261101T211205Z-th204-1945-monthly-flows-handoff.md
12. research/privacy_safety/F010_VALUES_AI_HUMAN_OVERRIDE_DATA_LIFECYCLE_2026-W45.md

next_action: 获取两项试验官方注册历史与事前SAP，核查主要终点、排除规则、缺失处理先后；寻找独立团队客观测量的长期产品复现。E继续R333至R340强制验收追踪，F本周只读。