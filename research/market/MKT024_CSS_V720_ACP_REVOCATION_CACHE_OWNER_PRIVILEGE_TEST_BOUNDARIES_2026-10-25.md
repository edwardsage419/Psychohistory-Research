# MKT024：CSS v7.2.0 ACP 撤权验证、对象身份缓存与 Pod 所有者权限的测试边界

date: 2026-10-25 (UTC+08)
track: commercial_market
status: COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC_PORT_AUDIT
preflight_main_head: b36d16b5add8a71cf2abe4f2fce2a35b6b1970a9
prior: MKT017–MKT023；本次重点推进 MKT023 遗留的撤权负对照。
scope: CommunitySolidServer/CommunitySolidServer v7.2.0 固定源码、上游单元/集成测试与本地无外部依赖的简化 JavaScript 复刻测试。未启动 CSS 服务器，未下载真实 Pod、个人数据或安装依赖。未调用 CI。

## 1. 本轮可核验的新发现

### MKT024-F1：同一对象身份复用时，缓存保留旧结果；源码还跳过底层 canHandle

[FIXED_SOURCE + UPSTREAM_UNIT_TEST + INDEPENDENT_REDUCED_PORT]

`src/util/handlers/CachedHandler.ts` 使用嵌套 WeakMap，并通过严格对象身份缓存输出。默认权限配置 `config/ldp/authorization/readers/default.json` 指定键为 `credentials` 和 `requestedModes`。在 `handle` 中，如果缓存值为 truthy，则直接返回，不调用底层 `source.handle`；`canHandle` 在存在相同键的缓存时也直接成功返回，不调用 `source.canHandle`。该实现没有显式按 ACR 版本或 PUT 事件失效的逻辑。上游 `CachedHandler.test.ts` 直接测试对象复用命中、浅复制输入仍命中、字段对象变化后重新调用底层、命中后 `canHandle` 跳过底层检查。

为隔离这一逻辑，本轮将上述 WeakMap 键和缓存分支忠实缩减移植到 Node.js 22 JavaScript，并以合成布尔 `read` 权限代替真实服务器 PermissionMap。使用 Node 内置 `assert`，本地执行得到：
`{"checks_passed":7,"source_calls":3,"canHandle_calls":1,"scope":"reduced JavaScript port, synthetic only"}`。

七项检查包括：初次 allow、后端变为 deny 后相同对象仍返回 allow、浅复制外层输入仍返回 allow、更换 requestedModes 对象后返回 deny、更换 credentials 对象后返回 deny、缓存命中跳过底层 canHandle、换键后底层 canHandle 的拒绝被观察到。合成脚本本地路径 `/mnt/data/mkt024_cached_handler_synthetic.js`，该脚本未单独提交 GitHub；以下最小复现可在现成 Node 上重建核心观察：

```js
const cache = new WeakMap();
const credentials = {}, modes = {};
let allowed = true;
const get = (c, m) => {
  let inner = cache.get(c);
  if (!inner) { inner = new WeakMap(); cache.set(c, inner); }
  let result = inner.get(m);
  if (result) return result;
  result = { read: allowed };
  inner.set(m, result);
  return result;
};
console.log(get(credentials, modes).read);  // true
allowed = false;
console.log(get(credentials, modes).read);  // true, same object keys
console.log(get(credentials, {}).read);     // false, new modes key
```

**边界：** 这是简化逻辑的合成测试，验证缓存合同的条件行为；不等于独立运行 CSS 编译版本。正常不同 HTTP 请求是否复用两个对象引用，尚无实际执行证据。不能据此宣称真实服务器存在已确认撤权漏洞。

### MKT024-F2：现有 HTTP 权限表逐用例重置授权，不能替代“先授权后撤销”的同一资源时序测试

[FIXED_UPSTREAM_TEST_DESIGN]

`test/integration/PermissionTable.test.ts` 的 beforeEach 通过 `authFunction(store,...)` 为测试资源设置权限，每个表格行检查预设权限下目标存在和不存在时的 HTTP 状态。配置同时覆盖 WAC、ACP 的内存和磁盘后端。这些测试验证静态权限矩阵及资源存在性。

`test/integration/AcpServer.test.ts` 的 `requires control permissions to access ACRs` 用例覆盖 Control 授予后通过 HTTP PUT 更新 ACR、后续 GET 返回 200 的正向授权变化；已检查的这两份集成文件未直接构造同一资源 `GET=200 → 撤销 Read → 新 GET=401/403` 的反向序列。范围仅限本轮已读文件，不能声称仓库中绝无其他撤权测试。

### MKT024-F3：Pod 所有者具有独立的授权资源 Control 兜底，撤权测试必须隔离所有者身份

[FIXED_SOURCE + UPSTREAM_UNIT_TEST]

`src/authorization/OwnerPermissionReader.ts` 只针对识别为授权辅助资源的目标进行 Pod 所有者检查。若请求凭据 WebID 属于该 Pod 的 owners 列表，则为对应授权资源返回包含 `control/read/write/append/create/delete` 的权限集合。`test/unit/authorization/OwnerPermissionReader.test.ts` 验证：非授权资源、无 WebID、非 owner 均返回空权限；owner 访问授权资源获得全部模式。默认配置将 OwnerPermissionReader 与其他权限读取器组合。

因此，若使用 Pod 所有者作为撤权负对照身份，仍可能因其独立的授权资源管理权限而通过 ACR 读写测试。应将「第三方读取普通数据资源的 Read 是否撤销」与「Pod 所有者仍能管理 ACR」分开验证。该兜底针对授权资源，不能扩大解释为 owner 可绕过所有普通资源 Read 检查。

## 2. 对未来个人决策模型的候选方法映射

| 维度 | 实际机制与候选知识 | 证据边界 |
| --- | --- | --- |
| 数据输入 | WebID、客户端凭据、请求权限模式、资源 URL、ACR 内容、Pod owner 登记 | 无真实用户生活数据 |
| 状态表达 | ACP 权限结果、两个对象身份键、授权文件版本、请求前后许可状态 | 服务器端授权版本键尚未证实 |
| 算法 | 嵌套 WeakMap、缓存命中分支、OwnerPermissionReader 的授权资源所有者检查 | 独立测试仅简化端口 |
| 目标 | 访问控制可撤销、权限最小化、可解释授权路径 | 不设唯一人生效用权重 |
| 反馈和修正 | 候选为撤权后重新读取、不同身份重试、比对实际结果与授权状态 | 没有证据表明 CSS 自动修复撤权 |
| 隐私权限 | 区分 owner 的 Control、第三方 Read、clientId、issuer 与缓存对象生命周期 | 历史副本/备份仍需单独治理 |
| 解释性 | 记录 ACR 版本、来源、缓存键是否复用、身份和最终 HTTP 结果 | 无完整最终用户解释性验证 |
| 费用模式 | 公开开源代码和 Node 内置测试；未购买/部署 | GitHub 额度与整体账单未核验 |
| 可验证性 | 固定 v7.2.0 源码与上游测试、7 项本地合成断言 | MARKET 独立完整服务器执行=0，真人决策 E2=0，历史 E3=0 |

## 3. 后续独立验证协议候选（尚未执行）

T01 以非 owner 的匿名/第三方身份，对同一资源执行授予 Read、GET 成功、撤销 Read、新 HTTP GET 被拒；记录状态码、请求对象身份和 ACR 版本。
T02 在同一进程分别使用相同及全新 credentials/requestedModes 对象调用 PermissionReader，先改变底层合成策略，检查两类缓存路径；这是单元测试，与真实 HTTP 测试分开报告。
T03 以 Pod owner 修改 ACR，但用非 owner 第三方验证普通资源的撤权；另核实 owner 的 ACR Control 是否保留，避免错误负对照。
T04 同时覆盖 ACP 内存与文件后端、客户端身份变化、父容器继承、显式 deny Read、正确/错误 ACR 目标。
T05 把“后续新请求无法读取”和“已经下载的第三方副本/衍生数据已删除”作为两个独立验收项；后者不能仅靠 HTTP 401/403 证明。
测试仅允许在现有设备与免费开源环境进行。不能确保零新增费用时只保留测试设计。

## 4. E 当日治理增量（只读，避免重复 E002/E003）

先读本日 E002、E003、F001、MKT023 与 main 新提交。E002/E003 已满足今日正式实质审计，本轮只核实新增 R148、A 数据侦察修正和 TH027 的归档证据，没有另写 E004 或更改其他轨索引。

R148 最新 B 独立报告提交 `84cfbe6be6087a80c1b2c5a593116f76c7862104`，报告称 Python 3 标准库独立计算与 Node 路径枚举在 24 个首次耗竭分布格、3 个存活和 3 个收益汇总等项一致，共 40 个本地检查通过，并含吸收态错误突变负对照。该报告明确是同项目内部合成 E1，且没有远端新 CI。通过 GitHub REST Actions head_sha 直接查询 R148 B 报告提交和科学报告提交 `0ca544b34ba195271f914b700bb83c24ae7b6216`，各返回 `total_count=0`。这只支持两个具体 SHA 没有关联运行，不代表仓库所有 R148 提交均无 CI。不得将 196608 个理论事件路径计为独立真实样本。

A 轨 `MONTERO_2022_R096_PRIOR_USE_2026_10_25_CORRECTION_2026-10-25.md` 在提交 `5213e3a43bb66853be8713232ed7c96d274a1cd9` 明确纠正候选去重：Montero-Porras 2022 12 场次真人实验已经被 R096 用于独立冻结 M0/M1/M2 的 18612 个下一行动目标。官方 Dryad 原始字节仍受 HTTP403 阻塞，且既有 R096 协议不同于 R073。不得登记为新独立实验、新 R073 冻结迁移或新增 E2。此次纠正保留旧记录供追溯。

最新理论提交 `b36d16b5add8a71cf2abe4f2fce2a35b6b1970a9` 更新 TH027 与理论索引，尚未独立核验其原始学术来源。E 未修改该文件。original239 v7.8 既有登记仍显示 154 项逐项审计待办，本轮未重新计算完整索引。R136 负对照历史失败及 R074/R075 旧 E3 标签冲突继续保留。未执行全仓冻结哈希审计；不宣称全面验收。

## 5. F 本周专题状态

2026-W43 F001 已归档且明确 COMPLETE_BOUNDED_POLICY_METHOD_REVIEW；本轮避免重复生成 F 文件。将 F002 的候选问题具体化为「撤销授权后访问检查、权限缓存失效、owner 与第三方身份分离、已下载副本与衍生数据的删除责任」。F002 仍计划下一研究周执行。当前无个人真实敏感数据、自动决策功能或产品开发。

## 6. 来源、证据与费用

证据类别：固定官方源码 FIXED_SOURCE、官方上游测试设计 UPSTREAM_TEST_DESIGN、独立简化端口合成执行 SYNTHETIC_REDUCED_PORT，以及仓库既有报告 PROJECT_RECORD。源码/测试设计不等于本轮真实服务器运行。个人长期决策改善效果的独立实证为零。

非中文原始资料：
S1 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/util/handlers/CachedHandler.ts
S2 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/util/handlers/CachedHandler.test.ts
S3 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/config/ldp/authorization/readers/default.json
S4 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/authorization/OwnerPermissionReader.ts
S5 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/unit/authorization/OwnerPermissionReader.test.ts
S6 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/AcpServer.test.ts
S7 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/test/integration/PermissionTable.test.ts
S8 https://github.com/CommunitySolidServer/CommunitySolidServer/blob/v7.2.0/src/server/AuthorizingHttpHandler.ts
S9 https://communitysolidserver.github.io/CommunitySolidServer/latest/docs/classes/AcpReader.html
S10 https://solid.github.io/authorization-panel/acp-specification/
S11 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R148_FIRST_RUIN_INDEPENDENT_PYTHON_MUTANT_SCIENTIFIC_AUDIT_2026-10-25.md
S12 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/MONTERO_2022_R096_PRIOR_USE_2026_10_25_CORRECTION_2026-10-25.md
S13 https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md

主动新增费用=0；没有购买、收费 API、注册收费账户、CI、服务器/GPU、真实敏感数据。GitHub 免费额度和账户账单没有独立核验。研究主线：先完成全部 R 系列，再统一归纳，最后模型熔炼；本轨只形成候选知识。

next_action: MKT025 转向 Exist 的 OAuth/API 授权撤回和数据生命周期，避免连续围绕 CSS 缓存重复。E 下次优先核查 R148 后续 CI、Montero/R096 去重传播与 original239 元数据；F002 下周按已冻结周任务研究撤权及衍生数据生命周期。
