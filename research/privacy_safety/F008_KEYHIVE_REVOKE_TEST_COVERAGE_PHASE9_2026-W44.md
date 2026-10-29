# F008 第九阶段：Keyhive撤销入口与上游测试覆盖审计

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase9,upstream-revoke-entry-and-negative-test-coverage)。阶段状态：BOUNDED_SOURCE_COVERAGE_REVIEW_COMPLETE，F008整体仍IN_PROGRESS。零新增费用，未使用真实身份密钥或个人数据。

## 固定英文来源与读取范围

上游官方仓库 automerge/automerge-repo-keyhive 固定提交 390a1488826d26bd0f183d66ed260d69ca8b36af。
源码 https://github.com/automerge/automerge-repo-keyhive/blob/390a1488826d26bd0f183d66ed260d69ca8b36af/src/keyhive/automerge-repo-keyhive.ts ，Git blob 8edbe443571d95cf2139f0f1279180f48fc2a2fe。
授权前后历史访问测试 https://github.com/automerge/automerge-repo-keyhive/blob/390a1488826d26bd0f183d66ed260d69ca8b36af/test/new-member-access.test.ts ，Git blob 9acf53f2bda05ce8d0b63421958ae740f006af15。

通过GitHub连接器逐个读取该提交下test/目录8份测试文件和src/keyhive/目录5份源码，共13份、3778行。对revoke、revoked、removeMember、remove_member及access revocation等字面表达进行逐行扫描。8份测试文件中未命中；5份源码仅在automerge-repo-keyhive.ts的撤销方法注释处命中。此结论仅关于本次限定的文件和词形，不覆盖依赖包、其他目录、运行时动态调用或未命名的撤销测试。

## 实际源码机制

automerge-repo-keyhive.ts约192行暴露 revokeMemberFromDoc(docUrl, member)。若docUrl属于unprotected类型，直接抛UnprotectedDocError；否则将字符串成员ID转换为Identifier，使用文档上下文调用 keyhive.revokeMember(identifier, true, memberedDoc(docUrl))。这证明存在包装层的撤销入口和未保护文档防护检查。参数true的具体密码学含义、已缓存旧密文的可读性、历史密钥是否销毁、离线设备何时收到撤销均不能从此调用单独推断。

上游new-member-access.test.ts明确测试了新增成员对授权前后历史密文的可读性；本轮限定范围没有找到与之配对的撤销后历史密文不可读断言。当前证据仅说明测试覆盖缺口，不能据此声称实际权限绕过或漏洞。

## 候选零费用安全验收矩阵

未来若已具备可确认零费用的本地Node >=22.13与固定依赖环境，可用纯人工身份/文档执行如下候选场景，当前全部NOT_RUN：

1. 受保护文档撤销成员，检查新写入数据是否拒绝解密。
2. 撤销后重新读取撤销前已获取的明文缓存，明确无法追溯抹除。
3. 长期离线成员持旧密文和旧密钥，重联后检查权限版本与缓存状态。
4. 群组授予与群组撤销交叉，检查直接授权残留。
5. 撤销后重新授予，分别验证历史访问范围与新写入权限。
6. unprotected文档撤销入口必须拒绝，同时核验服务器是否另有绕过路径。
7. 历史备份、身份JWK和设备副本分开登记，GLOBAL_ERASED不得在未知时标记TRUE。

这些规则均为UNADOPTED候选。安全验收需记录上游固定版本、环境、测试输出、失败反例及清理结果。当前没有安装依赖、没有运行Vitest、没有真实设备测试、没有删除真实数据或生成私钥。

## 证据与下一步

证据等级为PINNED_UPSTREAM_SOURCE_AND_TEST_INVENTORY。既有F008第八阶段的追溯授权预期保留；本轮新增撤销入口与测试覆盖边界。没有独立安全认证或外部攻击实证。F008继续IN_PROGRESS。

下一阶段优先检查Keyhive核心依赖自身是否有撤销后旧密文/新密文测试，并确认其许可和本地运行前置条件。未确认免费条件时继续静态资料审查。