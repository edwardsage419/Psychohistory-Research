# MKT073 Beeminder requestid 同键更新、过期重试与批量部分成功的客户端契约

日期：2026-10-27 Asia/Singapore。研究轨：market。状态：COMPLETE_BOUNDED_MARKET_E1。主动新增费用：0。未注册、购买、授权或调用Beeminder认证API。

## 去重、真实来源及固定版本

已读 MKT029（记录了 requestid 同键更新的基础语义）、MKT071（日平方根聚合）、MKT072（增量删除契约缺口）与本周 F002。本轮新增检验对象为**修正后到达的旧请求**及**批量部分成功后的错误重试**，并检查公开客户端的测试覆盖。

1. 官方英文API文档 https://api.beeminder.com/ ，源仓库 https://github.com/beeminder/apidocs ，本轮实际读取 `source/index.html.md`，Git blob `8af20e66b6663ef1deefabb9493e145c64b0f30d`，仓库master提交 `21e92e36bc15add4bcbe2944842215ab24e9aa0a`。
2. 独立开源客户端 https://github.com/ianm199/beeminder_api_client ，固定提交 `ffff95afc12f32753d377d5bd072cf260166a962`，实际读取 `src/beeminder_client/beeminder.py` blob `efe161d656b2921af7832251df814f1d1258d3b2` 和 `tests/unit_tests.py` blob `ba9ae0b4a0581df2c32c26da6008c7c4258764ab`。此客户端不是Beeminder官方服务器。
3. 2025-11-11 英文厂商论坛中用户指出真实遇到的 `Duplicate request` 文案与文档 `duplicate datapoint` 不一致，尚未看到厂商确认两者等价：https://forum.beeminder.com/t/document-duplicate-request-api-response/12573 。这是公开用户问题，不能视为经过验证的服务端错误语义。

## 输入、状态、算法与反馈

真实产品的输入为手动或授权集成写入的datapoint，包含goal、requestid、value、timestamp/daystamp、comment、updated_at等；目标状态含历史点、聚合规则、红线、缓冲、收费承诺与图形。公开API规定 `requestid` 在**同一目标内**识别一个点：同键同内容视为重复；同键不同内容更新已有点；无键时可新增点。该接口是upsert，不是不可变事件日志。按用户设定的目标轨迹反馈偏离、缓冲及可能的收费；没有证据支持它会自动求解个人终身多目标效用。API可返回目标和点用于解释图表，但未提供被核验的全量不可变修订历史。

`create_all` 官方文档说明部分出错时返回 `successes` 与 `errors` 列表；公开文档没有承诺批量写入整体原子性，也没有在这些端点说明基于历史版本的条件写入/CAS。没有在认证服务端执行并发实验，不能据此认定服务器必然发生竞态。

**新增具体风险一：过期重试覆盖较新更正。** 假设同一目标的 `requestid=r1` 最初值100，人工修正为25，延迟队列又发送旧值100。依照文档同键不同内容upsert语义，第三次请求可能把点改回100。仅用requestid去重不足以区分原始重试和有意更正。具体服务器对并发顺序、审计记录与自动同步优先级的行为仍未验证。

**新增具体风险二：批量部分成功后整批旧内容重试。** 人工批次a/b/c中a、c先成功，随后a被修正为7，若把原始整个批次重发，a可能回到10。仅重试失败的b，在这个模型里保留a=7。实际错误返回结构、重试政策及服务器执行顺序仍待认证测试。

**新增文档质量问题。** 官方 `create_all` 示例请求的两个requestid末尾分别为929和930，示例响应却两次写成923。这是源文档字面不一致，不代表生产服务器会返回重复requestid。

## 公开客户端源码与测试覆盖

第三方Python客户端 `create_datapoint` 原样转发可选 `requestid`，`create_multiple_datapoints` 原样转发列表，`update_datapoint` 直接按点ID提交PUT。固定版本单元测试验证参数传递、零值更新和响应解析；批量测试使用模拟响应 `{"created":2}`，没有测试官方文档所述 `successes/errors` 部分失败，也没有测试修正后旧重试。该结论只针对本次检查的公开文件及测试，不能断言整个生态没有其他防护。源文件中的示例凭据字符串未使用、未验证、未复制到本项目。

## 独立合成验证与候选控制

Node标准库脚本 `research/market/mkt073_beeminder_stale_retry_synthetic_20261027.js` 已执行 **73项断言，0失败**。覆盖同键同值去重、同键不同值更新、延迟旧值覆盖、跨目标键隔离、无键重复、客户端generation门、批量部分成功、选择性重试、16组循环对照和文档示例不一致。模拟器按官方公开契约构造，不是对真实Beeminder服务器的测试。

候选工程控制：保存来源ID、目标ID、原始观测、修订序号与更新目的；区分“网络重试”和“新修订”；过期generation请求在本地拒绝；批量按单点确认并只重试失败项；定期全量对账与历史评分失效标记；重要更正由人工复核；禁止在未明确授权的情况下自动触发扣费服务。这些是未来研究储备，不提前开发个人决策产品。

## 隐私、费用、解释性与证据等级

Beeminder公开目标图可透露派生行为趋势；API要求授权；文档提供OAuth撤销回调，撤销后外部缓存与衍生画像是否删除未获独立证明。F002已研究授权及派生生命周期，本轮只增加“撤销后队列旧写入”和“过期重试复活历史值”候选风险，F003留待下周。

公开API文档和开源源码可免费阅读；实际Beeminder存在订阅与偏离收费，本轮没有注册或启用服务，也没有计费API或付费CI。证据分类：官方接口文字为 DOCUMENTED_VENDOR_CONTRACT；第三方客户端为 PINNED_SOURCE_CODE_INSPECTION；73项为 INDEPENDENT_SYNTHETIC_CLIENT_TEST；真实并发结果、长期人生收益、生产异常为 UNVERIFIED。内部 MARKET E1 不等于真人E2或历史E3。

下一轮 MKT074：优先查找开源客户端对HTTP重试、部分失败、版本检查的可执行回归测试，比较独立修订日志与目标平台upsert之间的状态边界。
