# Psychohistory 原生客户端 v0.8

`Psychohistory.xcodeproj` 提供同一套 SwiftUI 界面的 macOS 和 iOS 应用目标。原生界面接收自然语言，展示当前结论、未知、优先追问和局部分析，支持核对、修订或略过证据候选、调用共享引擎比较方案、确认选择和记录条件计划。服务器仍负责解析、方法选择、计算和权限判断。选择与计划只记录使用者当次确认的内容。

## 启动与连接

1. 在 Mac 启动 [v0.8 本地工作台](../future_model/README.md)，使用独立数据目录和环回地址。
2. 用 Xcode 16 或更新版本打开 `Psychohistory.xcodeproj`，选择 `Psychohistory` 及 `My Mac`。客户端默认使用 `http://127.0.0.1:8765`，输入该工作台的数据目录里的令牌后主动连接。决策引擎可在互联网断开时继续在同一台 Mac 运行。
3. iOS 目标支持 iOS 17 或更新版本。手机端默认地址为空，连接需要使用者已配置可访问的专用 HTTPS 服务。客户端接受专用 IPv4 地址和系统信任的 TLS 证书。签名团队、证书、网络接入和设备安装须在使用者控制的 Apple 环境验证。工作台目前只监听主机环回，应用工程没有配置局域网代理、交付或分发。

客户端使用 `/api/v8/decisions`。开始请求携带一次性取消标识，随后只使用服务端分配的会话标识、实例标识和当前修订。显示局部结果前核对回执的授权代次和依赖摘要。局部结果只显示可复算的限定事实或量差，无选择、计划及保存权限。标题与文本均来自计算结果和明确的显示规则。会话结束和应用切到后台清除端内临时输入，客户端尽力结束服务端会话。已经收到但无需显示的开始回复会请求结束。如果回复未送达，临时服务器状态按会话有效期清理。

令牌和当次对话只保留在客户端进程内存中，传输层禁用 Cookie、持久缓存及重定向。用户主动连接前没有网络请求。客户端校验指定地址，系统继续验证 HTTPS。历史记录、参数编辑、导出、删除、恢复及撤回使用本地 Web 工作台。本机完整 iPhone 计算、跨设备同步与生产签名仍待验证。现有移动 PWA 保留自己的离线方法与历史数据。

## 可复验范围

可移植的 `DecisionProtocol` 包仅用 Swift Foundation，可在 Linux 或 macOS 运行 `swift test --package-path platform/apple`。其中 Swift 到真实 API 的测试读取 `PH_APPLE_LOOPBACK_TEST_URL` 和 `PH_APPLE_LOOPBACK_TEST_TOKEN`。复验时使用新的临时数据目录，从其中读取测试令牌，执行结束后清理该目录。默认未配置时只跳过实际 HTTP 用例。Linux x86_64 的 Swift 6.2.1 实际执行 5 项 XCTest，用临时数据目录验证了真实 API 的连接、开始、核对、局部结果、陈旧修订拒绝和会话清理。

Apple 环境可使用 `xcodebuild -project platform/apple/Psychohistory.xcodeproj -scheme Psychohistory -destination 'platform=macOS' build` 和 `xcodebuild -project platform/apple/Psychohistory.xcodeproj -scheme Psychohistory -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build`。应进一步在实体设备检查启动、网络请求目标、掉线、前后台切换、中文证据确认、可访问性和撤回流程。Linux 没有 Apple SDK 或 Xcode。当前工程的 SwiftUI 目标编译、模拟器与实体设备验收均未执行。
