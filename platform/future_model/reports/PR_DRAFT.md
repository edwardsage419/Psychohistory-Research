实现 Psychohistory Platform v0.1 的完整合成科研闭环，全部新增文件限于 platform/future_model/。包含独立标准库机制核心、两个精确版本插件、实际跨模型适配、双时间尺度与事件、不可变快照及隔离分支、概率/UNKNOWN 契约、来源与科学准入、受限进程任务调度、SQLite/CAS 和验证备份恢复、共享 API/CLI、中文 React 科研控制台。

验证：Linux 完整 pytest 37 项通过；严格 TypeScript/Vite 构建、无第三方依赖核心运行、真实 Chromium 9 步页面流程通过。独立代码审查的 5 项重要问题已用 RED→GREEN 回归修复。从远端提交 eaafc58ece6a8f9a8d34f3fb5d1d632395fa21ec 全新克隆、新建 venv、npm ci、实验逐字段复算、SQLite/产物备份恢复全部通过；收据与原始日志随工程交付。

Gate 01 因 macOS 原生实测 NOT_RUN 为 PARTIAL；其他门槛详见 reports/ACCEPTANCE.md。审查 Minor M1（外部任意状态的完整语义校验）后置，当前 API 不开放此上传/执行入口。合成成功不代表真实预测/因果验证；R073、PESEN v0.1 与原科研协议保持不变。

不新增 CI，不合并、不公开部署、不使用收费 API/GPU/服务；只提交允许公开的代码、文档与合成产物，不含 token、SQLite 或受限数据。请按验收矩阵审阅，未经 owner 再次授权不合并。
