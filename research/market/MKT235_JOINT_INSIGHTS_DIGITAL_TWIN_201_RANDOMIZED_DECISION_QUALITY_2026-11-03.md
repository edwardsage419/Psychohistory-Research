# MKT235：Joint Insights 数字孪生辅助决策随机试验的结果与归因边界

track: market
run_date_utc: 2026-11-03
target_key: (market,Joint Insights,2025-eClinicalMedicine-103545,randomized-decision-quality+prediction-component-attribution)
baseline_main: 8ab5469de1f2fb07f82311830b16177e8eeeadee
status: COMPLETE_BOUNDED_PUBLISHED_ABSTRACT_AUDIT
evidence_grade: MARKET-E2_PUBLISHED_RANDOMIZED_HUMAN_STUDY; PRODUCT_ALGORITHM_NOT_REPRODUCED
participant_data_access: NOT_RUN
product_native_execution: NOT_RUN
CI_dispatch: NOT_RUN
paid_services: NONE

## 来源与产品机制
Jayakumar et al., *eClinicalMedicine*, published 2025-10-04, volume 89, 103545, DOI 10.1016/j.eclinm.2025.103545; PMID 41112505; PMCID PMC12528923; trial NCT04805554.
原始免费摘要：https://pubmed.ncbi.nlm.nih.gov/41112505/
研究中的 Joint Insights 是由研究团队与 OM1 关联的专门临床辅助决策工具。患者提供自报膝关节功能和症状指标及临床资料；系统提供患者教育、偏好评估、基于群体数据模型的个人化手术获益及风险预测，供患者和临床医生共同讨论。公开摘要未披露足以独立执行的完整模型权重、特征处理及校准实现。当前商业销售价格、一般公众可获得性、隐私删除与导出功能均未核实，不能将临床试验工具视为已验证的通用人生规划产品。

## 真实随机试验
美国单一大学附属骨科门诊在2021年2月至2022年11月开展开放标签随机试验。分析样本201人：完整AI辅助决策101人，对照教育内容100人。预设主要终点 K-DQI 决策质量，组均值84.4 (SD25.2) 对71.4 (SD29.8)，差13.0分，报告 P=0.0011。6至9个月决策后悔18.2对27.2，P=0.0051；膝关节健康KOOS JR 69.5对47.0，P<0.0001；治疗与偏好一致性91%对76%，P=0.0043。共同决策CollaboRATE、早期膝关节健康、满意度、就诊时长、手术率和三个月后悔评分无明确组间差异。

## 核心归因限制
随机分配的是包含教育、偏好评估和个体化预测的整体工具，相对仅教育的对照。不能将13分K-DQI差异单独归因于AI预测、数字孪生、模型校准或某个算法。研究为开放标签单中心，部分终点为自报评分，随访6至9个月，跨疾病、跨文化和长期人生福利外推未知。研究团队是Joint Insights共同开发者，大学与OM1存在版税协议，论文披露了这些关系。随机试验支持该整体工具在该临床场景改善若干结果，不构成独立第三方产品复现。

## 对未来研究方法的限定启示
评估决策辅助应区分：决策过程质量、选择与用户偏好一致性、决策后悔、客观结果、时间成本和风险分布。未来若检验个体化预测的增量价值，需要将教育、偏好询问和预测信息拆分随机条件，并预先冻结主要指标。不得将临床K-DQI当作普适人生决策量表。

## E/F协调
E只读检查发现R/B新增 R272 Python import shadow 反例，提交 cc7c77c426252677925346f0df9e157a4897c2f7 和 485388fb47b45ea2c4f01b557b220cc86719e2ec。候选入口未覆盖额外 json.py 的导入阴影风险；生产P0仍OPEN。E168当天已完成实质治理审计，未重做B轨错误注入。2026-11-03检查时main 8ab5469de1f2fb07f82311830b16177e8eeeadee，开放PR12项且全部draft、均未合并；原队列154项来自R/B报告，未在本轮逐行独立重算，净关闭没有新的证明。F010本周已有完成登记，未访问任何个人健康资料，未新增F编号。

## 证据与运行边界
仅审阅公开英文期刊/PubMed摘要、仓库短日志及R/B报告。未读取原始参与者数据、未运行Joint Insights、未复算原始回归、未开展人工合成实验、未触发GitHub Actions。MARKET-E2与R轨E2严格分开。GitHub账单与免费额度未确认，禁止触发可能收费CI。
