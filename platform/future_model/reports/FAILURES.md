# 真实失败、修复及未运行项目

- 初次环境阶段 `npm list -g` 失败：用户主目录无可写 npm 路径。工程使用明确的项目依赖、/tmp 或 /workspace 缓存，不依赖全局安装。
- 本次恢复：已发布自检脚本全部通过，保留 1 条 Starlette TestClient/httpx 弃用警告。请求功能实测通过，未把警告隐藏为无警告结果。
- TDD RED：核心 8 项、存储 4 项、调度/API 3 项在功能实现前因对应模块缺失失败；完整原始输出在 logs/*-red.log。实现后通过。
- 首次 Web 浏览器测试：静态 UI 未实现，访问令牌控件不存在，实际超时；随后导航按钮装饰编号进入 accessible name，导致精确定位超时，修复为 aria-hidden，不禁用测试。
- 首次 TypeScript 构建 TS2882：CSS 副作用导入缺少类型声明；添加 Vite/client declaration 后严格构建通过。
- 自查发现插件能力声明有缺失方法、适配器忽略额外 payload 字段；两个回归先失败后通过，日志 core-regressions-red.log。
- 独立审查发现 5 个 Important 缺陷：200 条历史上限隐藏活动任务、备份漏检引用对象、未强制执行源码锁、元数据形状/不确定性不一致被接受、未保存初始分支快照。15 个回归实际 RED→GREEN，完整报告 INDEPENDENT_REVIEW.md。最终套件也覆盖安全请求/清单路径/多版本/调度单实例。
- GitHub PR API：GraphQL、REST 和直接 HTTPS CONNECT 均曾被拒绝（Forbidden / proxy 403）；源草稿已包含 api.github.com，但当时当前运行实例仍 spec_revision=1、allowed_hosts=[]。用户确认保存后已重新核验；以最终 NETWORK_AND_PR.json 为准，不把源草稿持久化视为运行网络已生效。
- 注入的超时、取消、无效参数、缺失/篡改产物、非法路径、越权和旧版本执行都是真实拒绝测试；它们是预期失败路径，不计为正常实验成功。
- macOS 原生测试、破坏性全量故障注入、多用户、恶意第三方代码沙箱、真实社会预测、费用后台核验：NOT_RUN 或超出授权。未调用收费服务、未购买额度。
- 审查 Minor M1 后置：任意外部构造的状态仍需要插件级语义校验；当前 API 不接收外部快照上传/恢复执行。扩展此入口前必须补齐，不能把当前通用 JSON 恢复当作任意科学状态有效性证明。
