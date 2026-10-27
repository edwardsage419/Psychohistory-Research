# MKT074 Beeminder 第三方Python客户端批量写入表单序列化实测

日期：2026-10-27 Asia/Singapore。研究轨：market。状态：COMPLETE_BOUNDED_MARKET_E1。主动新增费用：0。没有注册、授权、调用Beeminder认证端点或发出网络写入。

## 去重与固定来源

读取已有MKT071、MKT072、MKT073及F002。本轮深挖MKT073未覆盖的实际HTTP请求体序列化。Beeminder官方英文API文档 https://api.beeminder.com/ 的 `POST /users/u/goals/g/datapoints/create_all.json` 示例把 `datapoints` 作为JSON数组字符串传入表单字段，响应成功时为点数组，部分失败时为 `successes` 与 `errors` 列表。官方文档来源仓库 https://github.com/beeminder/apidocs ，上轮固定master提交 `21e92e36bc15add4bcbe2944842215ab24e9aa0a`、文档blob `8af20e66b6663ef1deefabb9493e145c64b0f30d`。

第三方非官方Python客户端 https://github.com/ianm199/beeminder_api_client 固定提交 `ffff95afc12f32753d377d5bd072cf260166a962`。实际读取 `src/beeminder_client/beeminder.py` blob `efe161d656b2921af7832251df814f1d1258d3b2` 和 `tests/unit_tests.py` blob `ba9ae0b4a0581df2c32c26da6008c7c4258764ab`。客户端 `create_multiple_datapoints` 构造 `{"datapoints": datapoints}`，其中datapoints是Python字典列表；`_post` 使用 `requests.post(..., data=data)`。固定单测只mock `_post` 并断言传参，未准备真实HTTP表单字节。

## 新增实测：请求体结构与文档契约不匹配

在离线环境运行开源 `requests 2.32.5` 的真实 `requests.Request(...).prepare()`。输入两个点 `[{"value":1},{"value":2,"comment":"two"}]`，按该客户端实际代码路径构造表单，得到：

`datapoints=value&datapoints=value&datapoints=comment&auth_token=FAKE`

`requests` 将字典列表按可迭代项展开为三个字典键，数值1、2和注释值two没有进入 `datapoints` 表单值。若先对点列表执行 `json.dumps`，表单只含一个 `datapoints` 字段，URL解码后可以还原完整JSON数组。离线脚本 `research/market/mkt074_beeminder_batch_form_encoding_20261027.py` 共24项断言，0失败。测试使用虚构token和example.invalid，`prepare()` 没有发送HTTP请求。

此为**固定版本第三方客户端的可复现请求编码缺陷**，其风险是批量写入请求在进入服务端前已丢失业务数据。没有认证调用，服务端实际返回码、容错解析、是否拒绝请求及是否影响其他版本均未验证。单点写入传递标量字段，不能由该批量缺陷推断单点接口同样失效。该第三方客户端不是Beeminder官方服务器。

## 产品机制、适用性与风险

产品输入为目标内单点时间戳、daystamp、value、comment及可选requestid；状态是按目标分组的历史点、目标轨迹、缓冲和偏离状态；反馈为目标图、提醒及可能产生费用的偏离承诺。官方API按同目标requestid执行upsert，部分失败可返回分项结果；该接口没有在已核文档中承诺不可变修订日志或跨批次原子性。官方文档提供secret、datapublic隐私标志及OAuth授权撤销回调；这不能证明第三方缓存、衍生画像已同步删除。解释性来自原始点与图表，尚无独立真人研究证明长期决策质量提升。

费用来源：Beeminder英文帮助2026-03-06更新 https://help.beeminder.com/article/19-how-much-does-beeminder-cost ，说明有限免费目标、可能的偏离收费和付费会员。项目仅使用免费公开文档、开源代码与本地Python。没有购买、注册或启用扣费功能。账户整体账单未核验。

候选控制：第三方数据接入前先对实际HTTP请求字节做离线契约测试；批量请求序列化为单一合法JSON数组字段；对部分成功逐项核对ID及原始值；仅重试失败项并使用本地修订代数防止过期重试覆盖人工更正；保存发生时间、修订时间、来源版本和人工纠错状态；敏感数据默认最小采集及撤销后禁止旧任务写入。这些属于未来知识储备，不提前开发个人决策产品。

证据等级：官方接口文字 DOCUMENTED_VENDOR_CONTRACT；固定第三方代码 PINNED_SOURCE_INSPECTION；requests真实本地编码及24断言 INDEPENDENT_OFFLINE_WIRE_PREPARATION；真实服务器行为、收费风险发生率、长期行为效果 UNVERIFIED。内部 MARKET E1，不提升真人E2或历史E3。

下一轮MKT075：核对同类开源客户端的真实HTTP批量测试、官方部分成功响应解析和分页对账，优先寻找具备可执行契约测试的项目。
