# MKT049 Fatebook 多选题结果标签、前端约束与服务器数据一致性审计

日期：2026-10-26（Asia/Singapore）。track: market。subflow: commercial。status: COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC。前序 MKT048。写前观察 main HEAD：`ff79c27e678a8cd9803cc728dc7a16f31886c5da`。CI：NOT_RUN。主动新增费用：0；账户整体账单和 GitHub 免费权益余量未独立核验。

## 1. 去重与固定英文来源

本轮先读取 main、MKT048、E017、F002、本轮 R179 新增协议与研究记录。MKT048 已覆盖非排他多选结算顺序、含糊评分、导出归属与撤回，本轮只审查此前未覆盖的**排他多选标签约束、创建时选项唯一性、前端与服务端验证差异**。固定开源提交：`Sage-Future/fatebook@ba7e89c790afd4532bc8e157d9c9c46fc0b4222f`。

原始英文源码：
1. `components/questions/MultiChoiceResolutionOptions.tsx`：前端从现有选项文本生成菜单，再追加 AMBIGUOUS 与 OTHER。https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/components/questions/MultiChoiceResolutionOptions.tsx
2. `components/questions/ResolveButton.tsx`：排他多选使用专用菜单，非排他选项使用二元结果菜单。https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/components/questions/ResolveButton.tsx
3. `lib/web/question_router.ts`：创建时选项文本仅为字符串，结算输入的 resolution 与 questionType 亦为字符串；服务端对题目作者做权限核验。重点第452至581、615至679行。https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/web/question_router.ts
4. `lib/interactive_handlers/resolve.ts`：排他多选逐项结果映射、父题结果、评分分支。重点第184至235、555至617行。https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/interactive_handlers/resolve.ts
5. `prisma/schema.prisma`：QuestionOption 文本没有显示唯一约束，Question 与选项有独立 ID 和父子关系。https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/prisma/schema.prisma
6. 官方产品页面仅用于功能存在性核对：https://fatebook.io/ 。

## 2. 真实新增机制 A：保留标签与用户自定义选项可能发生碰撞

排他多选前端直接将选项文本与 `AMBIGUOUS`、`OTHER` 合并为可选结算菜单。创建输入的 `options[].text` 仅要求字符串，所查服务器创建路径没有排除这两个保留标签。若自定义选项文本与保留标签相同，菜单产生同名条目；结果处理依据文本相等设置选项 YES/NO，同时依据结果枚举设置父题状态。

人工抽象示例：选项为 `AMBIGUOUS` 与 `Choice B`，选择 `AMBIGUOUS` 时，文本匹配会把同名选项映射为 YES，父题状态则为 AMBIGUOUS，评分分支跳过。**该不一致性来自固定源码控制流；未确认托管服务是否额外阻止该输入。**

## 3. 真实新增机制 B：重复选项文本会造成预测归属与结算歧义

创建路由没有显式检查同一题目选项文本唯一。初始预测创建使用 `question.options.find(o => o.text === option.text)` 按文本寻找第一个匹配选项 ID。若两项文本相同，其初始预测可能都关联第一个匹配选项。排他结算再使用 `option.text === resolution`，同名选项可能同时被标记为 YES。

这意味着预测记录与真实选项身份的映射可能出现多对一，结算时又出现一对多。实际数据库中选项顺序、前端重复文本是否允许、是否有其他保护仍未端到端测试。

## 4. 真实新增机制 C：前端可选值与服务器输入域不同

网页菜单通常只呈现题目选项及 AMBIGUOUS/OTHER，二元选项菜单只呈现 YES/NO/AMBIGUOUS。服务器结算输入采用宽泛字符串验证，并接受客户端提交的 questionType；所查服务端分支没有展示与已存题目类型、现有选项标签一致的完整白名单核验。按固定源码，未匹配任何选项的字符串可进入父题 YES 的分支，而所有选项均被标为 NO。

服务器已有题目作者权限核验，故不能声称整体接口无认证。**另外发现父题与选项对象关联的显式校验需要单独安全复核；本公开报告不提供可用于针对第三方对象操作的请求构造或复现步骤。** 建议维护者私下检查对象级归属及事务边界，未经授权不进行线上测试。

## 5. 独立人工检查

使用 JavaScript 在隔离人工数据上实现源码可见的排他多选结果映射，检查六类输入的父题状态、选项状态及是否进入评分分支，另检查重复标签、保留标签和未知标签三种反例。**21项断言，21 PASS，0 FAIL**。例子：
* `Choice A` 对两个不同选项得到 [YES,NO]，父题 YES。
* `OTHER` 得到 [NO,NO]，父题 NO，进入评分。
* `AMBIGUOUS` 得到 [NO,NO]，父题 AMBIGUOUS，跳过评分。
* 未匹配标签得到 [NO,NO]，父题 YES，进入评分。
* 两个同名 `Choice A` 得到 [YES,YES]。
* 自定义 `AMBIGUOUS` 选项得到该选项 YES、父题 AMBIGUOUS。

检查验证的是人工抽象与固定源码分支一致；没有运行原项目 TypeScript、Prisma、数据库、真实 API 或浏览器 E2E，也没有探测线上权限。不能据此声称线上已发生安全事件。

## 6. 产品方法映射与证据等级

输入：题目文本、选项文本与 ID、概率、时间、题型、结算结果。状态：父题结果与时间、逐选项结果、预测历史、评分。算法：排他多选通过选项文本匹配二元 YES/NO，再按结果状态决定评分。反馈：结算通知、Brier 分数及导出，受选项身份一致性影响。解释性：应保留冻结的选项 ID、显示文本版本、结果枚举及修订时间，避免文本标签重用改变历史语义。隐私权限：题目作者校验存在，对象级父子归属和参数类型一致性仍需专项验证。费用：开源源码可免费审查；托管产品费用与计费条款本轮未核实；未注册或购买。局限：缺少真实数据库和独立线上验证。

等级：固定代码 `SOURCE_CODE_E1`；21项人工断言 `SYNTHETIC_E1`；官网介绍 `VENDOR_CLAIM`；线上可达性、实际用户影响、长期决策改善 `NOT_VERIFIED`。营销描述不得替代科研效果。

## 7. 风险与候选控制

MKT049-R1 MEDIUM：保留结果标签与自定义选项同名，父题和选项状态语义不一致。
MKT049-R2 MEDIUM：重复选项文本造成初始预测归属歧义及多项同时 YES。
MKT049-R3 HIGH_CANDIDATE：服务端结果域、题型及对象关系约束不足，需要维护者授权的隔离复核，暂不宣称已利用。
MKT049-R4 MEDIUM：父题状态与逐选项状态不一致，可能影响历史评分及人工申诉。

候选控制：服务端对已存题型、合法结果枚举、选项 ID 与所属父题做一致性验证；选项以不可变 ID 结算，保留文本版本；保留标签使用独立类型而非用户文本；创建时拒绝同题重复标签或显式消歧；结果、评分、导出采用同一对象关联键；对历史更正保留最小可验证证据并尊重F轨删除生命周期。安全疑点优先私下向维护者核查，禁止未经授权的真实服务测试。

## 8. E/F 状态与下一轮

E轨当日全轨日检 E004 已完成；本轮独立增量审计 R179 的原始90世界PMF与新收据，另登记 E018。F轨 2026-W44 F002 已完成，本轮不重复立项。MKT049新增选项身份、结果更正、申诉的F003候选风险。所有发现均属候选知识储备；不改动R系列、R073、PESEN冻结协议或人生效用权重。

下一轮 MKT050：寻找新的开源预测日志或情景版本管理系统，优先评估结果版本化、对象身份绑定、导出与历史回放；若继续 Fatebook，先检查是否已有修复并采用新的固定版本。全程零新增费用。
