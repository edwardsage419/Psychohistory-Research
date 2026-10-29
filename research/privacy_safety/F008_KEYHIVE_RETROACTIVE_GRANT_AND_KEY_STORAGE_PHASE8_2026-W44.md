# F008 第八阶段：Keyhive追溯授权与身份密钥存储边界

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase8,retroactive-grant-history-and-key-persistence)。状态 PHASE8_BOUNDED_UPSTREAM_SOURCE_AUDIT_COMPLETE，F008整体IN_PROGRESS。

## 新增固定上游来源
官方仓库 automerge/automerge-repo-keyhive 固定提交 390a1488826d26bd0f183d66ed260d69ca8b36af。源码 test/new-member-access.test.ts Git blob 9acf53f2bda05ce8d0b63421958ae740f006af15；src/keyhive/active.ts Git blob cf85062c58603bfca6f0b6b5c0c5bbb3fb82fd4f；test/close.test.ts blob 089d1e26beb2932c95e7d3b0d8e5554103227f8d；package.json blob caf1a1bdacf751cec2557b2e0ee5501ba46eb4f4。

原始英文源码：
https://github.com/automerge/automerge-repo-keyhive/blob/390a1488826d26bd0f183d66ed260d69ca8b36af/test/new-member-access.test.ts
https://github.com/automerge/automerge-repo-keyhive/blob/390a1488826d26bd0f183d66ed260d69ca8b36af/src/keyhive/active.ts
https://github.com/automerge/automerge-repo-keyhive/blob/390a1488826d26bd0f183d66ed260d69ca8b36af/test/close.test.ts

## 源码级增量
new-member-access.test.ts 中两项上游测试明确期望新成员在被授予文档read权限后，可以读取授予之前及之后分别加密写入的内容。第一项直接授予文档权限，第二项通过已经有文档访问权的群组授予。测试预期 before 和 after 均为可读字符串。由此可见该固定版本的测试合同允许追溯读取历史内容，未来个人决策系统的分享授权应明确提示历史记录可见范围。测试是源码中的断言，当前没有在本轮实际运行Vitest，不能声称现实部署均遵循该行为。

active.ts 使用存储键 active-key-pair-2；初始化尝试从adapter读取已有JWK，缺失时用WebCrypto生成Ed25519密钥并存储。源码中生成和导入使用extractable=true，序列化导出public/private JWK并交由storage adapter保存。其具体静态/传输加密强度取决于adapter和部署环境；本轮未验证adapter加密。close.test.ts验证close时调用clearCachedKeyMaterial，但这不构成持久化JWK删除、其他副本清理或备份清除证明。

package.json固定版本0.7.0-alpha.1，要求Node >=22.13、pnpm 10.15.0，测试命令vitest run，依赖包括@keyhive/keyhive 0.4.0-alpha.1及@automerge/automerge-repo 2.6.0-subduction.49。源码及测试可免费阅读；完整依赖获取、许可逐项核验、真实运行时与WASM测试本轮均NOT_RUN。没有新增安装、服务、密钥或计费操作。

## 零费用候选控制及风险
R24 历史共享范围：未来每次授权前展示历史记录可见范围，支持仅共享新记录的独立设计候选；本轮未证明组件自带此限制。
R25 私钥持久化：本地优先的身份私钥应评估存储适配器保护、密钥备份、撤销和用户确认；不能把缓存清理当成私钥擦除。
R26 生命周期证据：分别记录授予、历史访问、密钥副本、离线缓存及备份删除状态；未知则显示UNVERIFIED。
R27 运行时复验：固定上游提交和依赖版本后，只有确认零费用环境才执行真实测试；若缺失依赖或额度，则维持源码审计。

控制均UNADOPTED。无真实敏感数据、无用户私钥读取、无设备同步和实际删除。证据为固定上游源码与测试预期，未取得独立安全认证或实测撤销证明。下一阶段研究仅限原生本地可复现条件和源码中的权限撤销负例覆盖。
