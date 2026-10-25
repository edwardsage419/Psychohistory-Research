# MKT030 Beeminder 公开图表、API 隐私字段与图像数值反推边界

date: 2026-10-25 (UTC+08)
track: commercial_market
subflow: market
status: COMPLETE_BOUNDED_OFFICIAL_DOCUMENT_CONTRADICTION_AND_SYNTHETIC_INFERENCE
initial_main_head: 76b2377c940041b60a8a0ee74b0753f233232176
prewrite_main_head: 76b2377c940041b60a8a0ee74b0753f233232176
prior: MKT001, MKT029
source_language: English only
real_product_executed: NO
authenticated_api_or_real_user_data: NONE
new_CI: NOT_RUN
new_spend: 0 (account billing and free quota not independently verified)
R_protocols_modified: NO

## 1. 相对 MKT029 的真实新增事实

MKT029 已确认新目标默认公开图表、原始点私有，以及撤销 YNAB 授权仍保留历史数据。本轮继续直接核对官方 API 字段及帮助页面，并识别一处**文档语义冲突**，将其作为需供应商澄清的证据缺口。

F1. 官方 API 的 Goal 对象定义 `secret` 为访问目标是否要求所有者登录，默认 `false`。API 将 `datapublic` 描述为“查看数据点是否需要以所有者身份登录”，默认 `false`。然而字段名 `datapublic` 暗示“是否公开数据点”，而帮助文档明确说新目标“public, with private data”，且仅勾选 “Make the datapoints public” 才会向他人显示最近原始点和评论。API 描述的逻辑方向与帮助文档存在明显歧义。**不能直接把 `datapublic=false` 解释为匿名用户可以查看原始数据。** 应以产品帮助页的用户界面说明为目前较清楚的默认隐私陈述，同时将 API 文档缺口登记为未验证。没有通过真实账户或未授权 HTTP 请求判定生产行为。

F2. 官方帮助明确区分四种表面：目标页面、图表图片、统计页、原始数据点与评论。默认公开目标允许任何知道链接的人看到图表和统计页。勾选原始点公开才显示 Data 页中的近期数据和评论。将目标设为私有后，访客会看到与不存在目标相似的错误页，降低目标名称枚举信息泄漏。公开展示不是匿名搜索可轻易发现的同义词，官方说明随机用户目标没有方便的全局列表，除非知道用户名或主动 featured。

F3. 官方 API 的 Goal 资源公开文档列出 `svg_url`、`graph_url`、`thumb_url`、`curval`、`curday`、`rate`、`roadall` 等字段，用户授权后的接口可提供更丰富的数值状态。官方 API 同时声明所有 API endpoints 需要认证。因此，不能由字段存在推断未认证访客可以通过 API 读取 `curval` 或 `roadall`；公开图表图片与认证 API 的权限是两条独立边界。图片 CDN 的缓存与变更私有后的旧链接失效尚未验证。

F4. API 文档允许创建和更新目标时设置 `secret`、`datapublic`，但没有给出所有组合的完整权限真值表，也未给出设置变化对已缓存图像、第三方嵌入或旧截图的撤回保证。对 `secret=true, datapublic=true` 等组合的实际有效权限不作推断。

## 2. 数学上可检验的图像反推风险

若一张公开图表有可辨认的数值纵轴、固定的像素高度 H 和可识别的点位置，则即使不公布原始数值，图像也携带数值信息。对纵轴范围 [0,100]、高度 H 的理想无噪声线性图，令像素坐标 p=round(H*x/100)，重建值 xhat=100*p/H。只要没有裁剪或额外变换，|xhat-x|<=50/H。这个界限是构造模型的数学性质，**不是 Beeminder 实际图像分辨率、抗锯齿、聚合、坐标缩放或泄漏程度的测量**。

本轮以 12 个纯人工数值 [5.3,12.4,19.8,27.1,34.4,39.6,40.4,47.7,55.3,62.8,75.1,92.3]、三种高度 H={20,100,200} 运行 Python 标准库 Fraction 检查，共 36 个误差界断言，全部 PASS。

| H | 最大绝对反推误差 | 平均绝对误差 | 理论误差上限 |
| ---: | ---: | ---: | ---: |
| 20 | 2.4 | 1.1333333333333333 | 2.5 |
| 100 | 0.4 | 0.2833333333333333 | 0.5 |
| 200 | 0.2 | 0.15 | 0.25 |

H=100 时，39.6 与 40.4 都映射为像素 40，说明图像反推有量化歧义；其他值可能被更精确地限制在小区间内。真实产品是否暴露坐标刻度、采用何种图形聚合和渲染，均未独立检查。

可复算的完整脚本：

```python
from fractions import Fraction

values = [Fraction(n, 10) for n in
          (53, 124, 198, 271, 344, 396, 404, 477, 553, 628, 751, 923)]
for height in (20, 100, 200):
    pixels = [round(value * height / 100) for value in values]
    reconstructions = [Fraction(100 * pixel, height) for pixel in pixels]
    errors = [abs(a - b) for a, b in zip(values, reconstructions)]
    assert len(errors) == 12
    assert all(error <= Fraction(50, height) for error in errors)
    print(height, "max", max(errors), "mean", float(sum(errors) / 12))
print("36/36 synthetic error-bound assertions PASS")
```

独立研究支撑的适用范围：Drevon, Fursa & Malcolm (2017) 在论文摘要中报告两位编码员从36张图的168条序列提取3596个点，并观察到较高一致性与效度；Poco & Heer (2017) 研究从图像恢复图表编码。它们支持“从图像反推数值在技术上可行”的一般命题，**没有测试 Beeminder 的隐私系统**。本轮只阅读公开摘要与研究组公开页面，没有购买论文、读取未开放全文或复算作者原始图像。

## 3. 输入、状态、目标、算法、反馈、解释、权限与费用

真实产品公开文档中的输入为目标类型、红线、日期、数值点、隐私开关、数据源及可选公开评论。状态包括 `secret`、`datapublic`、图表 URL、当前值、风险缓冲及目标是否归档。目标是用户设定的单项承诺阈值和可视化反馈。算法层面，MKT001 已审查目标曲线和缓冲字段，本轮仅检验隐私文档及抽象图像量化，不复现服务器授权判断。反馈包括图表、统计、提醒和用户可修改的隐私设置；未见官方文档证明会自动学习个人效用权重或优化跨领域人生目标。解释边界：用户能看到阈值及曲线，访客对公开曲线也可能进行近似数值推断。

隐私与权限：公开图像和统计、私有原始点、已认证 API、第三方截图/缓存必须分开审计。API 文档存在 `datapublic` 语义歧义。费用：Beeminder 具有可能触发扣费的承诺机制，项目不注册、不授权、不试用、不购买；本轮仅使用公开免费页面及本地标准库。

## 4. 候选风险与方法储备

MKT030-R1：公开图表与统计页可以在隐藏原始点的情况下泄露行为节奏、数值区间或生活模式。候选控制：敏感目标默认私有；公开统计、图片、元数据、分享链接分别做最小披露审计。

MKT030-R2：API `datapublic` 描述与用户帮助文档默认设置语义不一致。候选控制：将其登记为供应商文档澄清问题，未来如允许免费且无敏感数据的安全测试，可用合成目标检查四种布尔组合；当前不执行。

MKT030-R3：撤回图表公开后，第三方截图和外部缓存的生命周期不明。候选控制：公开副本与撤销权限分开建模，默认不承诺可回收所有副本。

MKT030-R4：模型输出的趋势图可能导致敏感健康、财务、关系行为被推断。候选控制：未来决策系统以本地优先、最小化共享、单独用户批准及导出副本登记为候选要求；不提前开发。

## 5. E 当日只读检查

已读取 E002、E003、F001 和当前 main 提交历史。E002/E003 已在 2026-10-25 完成实质治理检查，本轮不重复新建 E 文件。初始和写前 main HEAD 均为 `76b2377c940041b60a8a0ee74b0753f233232176`，已有 market 仅到 MKT029，MKT030 文件不存在，其他轨有独立新增提交。

新增检查：R158 先冻结第三方法协议 `12e2388771a1ab83a8aff14d3ad937b096469479`，再执行并归档60个人工 Poisson 世界的精确似然比与目标泄漏负对照。报告 `research/validation/R158_POISSON_EXACT_RATIO_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md` 明确 E1 内部、有界通过，不修改 R158 原验收，不含真实冲突事件预测。直接用 Actions REST `head_sha` 查询最新 R158 第三方法科学报告提交 `67758615e917facc499d73a4b0b94d4c2bada1f1`，返回 0 项；该新增方法不能宣称新的远端 CI 验收。R157 的 Georgescu 2023 数据侦察确认原论文支持文件为8张 TIF 和1张系数 XLSX，原始逐年数据仍未取得，历史 E3 阻塞；查询该数据侦察提交 `bae4ca71956c463fb7884ca9c4108b66a0eac6aa` 的 Actions 亦为 0 项。既有 original239 v7.8 的154条 provisional itemwise audit open、R136 冻结负对照 FAILED_NONDISCRIMINATING 和完整 CSV 缺失仍待解决。本轮未重跑 R158 全套算法、未做全仓冻结哈希扫描，也未修改 R、E、F、TH、C、D、A、B 或共享索引。仅核实本轮涉及路径和提交，不能宣称全仓无冲突。

## 6. F 本周专题

2026-W43 的 F001 已归档，涵盖人类否决权、解释、最小采集。MKT030 的图像泄漏和 API 隐私字段歧义列为下一次 F 研究候选风险；同周不重复立项。下一周 F002 仍优先授权撤销、缓存与衍生数据生命周期。无真实个人数据、无新产品开发。

## 7. 来源、证据等级与下一项

S1 Beeminder 官方隐私帮助：https://help.beeminder.com/article/102-privacy
S2 Beeminder 官方 API：https://api.beeminder.com/
S3 Drevon et al. (2017), DOI 10.1177/0145445516673998：https://pubmed.ncbi.nlm.nih.gov/27760807/
S4 Poco & Heer (2017), DOI 10.1111/cgf.13193：https://visualdslab.com/papers/ReverseEngineeringVis/
S5 MKT029：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT029_BEEMINDER_RETROACTIVE_DATA_CHARGES_EXIT_AND_PRIVACY_BOUNDARIES_2026-10-25.md
S6 E003：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E003_R136_FROZEN_NEGATIVE_CONTROL_INCIDENT_DELTA_2026-10-25.md
S7 F001：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md

证据等级：MARKET_E1_VENDOR_OFFICIAL_DOC_CONTRADICTION; INDEPENDENT_PUBLISHED_ABSTRACTS_GENERAL_CHART_DIGITIZATION_ONLY; SYNTHETIC_FRACTION_QUANTIZATION_36_PASS. No authenticated API, real product privacy penetration test, human E2, historical E3, or actual data exfiltration. No new CI, no new spending, no account-wide billing check.

下一项 MKT031：审查 Beeminder `secret` 变更与静态图片 URL 缓存的公开文档证据，若无法取得新的直接证据则转向 Dcider 的偏好与结果反馈；E 按日只读，F 下周推进 F002。R 系列全部完成后再系统分类，最后模型熔炼。
