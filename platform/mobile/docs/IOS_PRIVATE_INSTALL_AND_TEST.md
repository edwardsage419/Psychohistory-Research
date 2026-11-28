# iPhone 私人 HTTPS 安装与真实设备验收

关联 Issue #58 和 Draft PR #59。**真实 iPhone 验收：BLOCKED / NOT_RUN。** 本文只建立安装和记录流程，尚未有任何实际 iPhone 的操作结果。

## 最简安装方案

免费个人 Tailscale 网络仅在 Mac 与本人的 iPhone 之间提供第一次 HTTPS 静态文件安装入口。Tailscale Serve 限于 tailnet，不能使用公开 Funnel，也不访问或同步个人数据。官方文档：https://tailscale.com/docs/features/tailscale-serve 以及 https://tailscale.com/docs/reference/tailscale-cli/serve 。iPhone 主屏幕安装方法见 https://support.apple.com/guide/iphone/turn-a-website-into-an-app-iphea86e5236/ios 。

1. 在 Mac 和 iPhone 安装官方 Tailscale，使用同一私人网络身份登录。确认两端连接，检查同网络内其他成员和设备的访问控制。首次使用 Serve 可能请求启用 HTTPS，须由用户确认，切勿启用 Funnel。HTTPS 证书的公开透明日志可能显示机器的 ts.net 名称。
2. 在 Mac 单独检出当前 Draft 分支：

   ~~~sh
   git clone --single-branch --branch feat/psychohistory-mobile-v0.1 https://github.com/edwardsage419/Psychohistory-Research.git Psychohistory-Mobile
   cd Psychohistory-Mobile/platform/mobile
   git rev-parse HEAD
   ~~~

   已有该分支的受控工作树可直接使用。检查提交与 PR #59 的最新 head 一致。运行环境需要免费的 Node.js 22 或更新、curl 和 Mac 上已安装并登录的 Tailscale 应用。macOS 脚本优先直接调用 `/Applications/Tailscale.app/Contents/MacOS/Tailscale`，避免通过手工创建的 `/usr/local/bin/tailscale` 符号链接触发 Bundle Identifier 崩溃。如果之前根据旧指令创建了符号链接，脚本本身可以避开它；之后可通过 Tailscale 官方设置中的 CLI integration 安装正确的启动器。
3. 执行：

   ~~~sh
   bash scripts/iphone-private-install.sh
   ~~~

   脚本本地构建安装文件，并在 127.0.0.1:8766 启动临时服务，经 Tailscale Serve 的 HTTPS 8443 端口提供给私有网络。若端口冲突，可设置 MOBILE_PREVIEW_PORT=8767 或 MOBILE_TAILNET_HTTPS_PORT=9443；不得自动覆盖已有的 Serve 设置。脚本不会公开部署，也不会自行启用 Funnel。
4. 在 iPhone Safari 打开终端显示的 HTTPS 地址。确保 HTTPS 证书可信，遇到证书错误请停止。确认 Safari 页面出现“本机离线资源已准备”，在 Safari 分享菜单选择“添加到主屏幕”。
5. **从主屏幕图标重新打开该 App，并再次确认离线资源就绪。** Safari 标签页与主屏幕应用的存储可能隔离，不得以 Safari 的提示替代主屏幕确认。保持 Mac 在线直到主屏幕应用准备好，之后可按 Ctrl+C 停止本次 Serve。必要时用 tailscale serve status 检查残留配置，仅针对本次专用端口停止。

## 实体 iPhone 离线验收

仅用虚构数据。先确认安装成功，关闭 Mac、在 iPhone 开启飞行模式并确认 Wi-Fi 与蜂窝数据均已关闭；彻底结束主屏幕 App 后从图标冷启动。冷启动若失败，立即记录 FAIL，不宣称独立可用。

1. 职业选择：输入多方案，修改硬约束从排除到恢复，观察所有方案、图表与结果重算。
2. 学习及资金投入：填写标为 SYNTHETIC 的信号与概率，调整调查成本使净价值从正变负；撤去来源时保留条件性或 UNKNOWN。
3. 生活规划：设置时间窗口、严格截止与等待损失，修改截止时点并核对可行集合。
4. 离线授权保存一条虚构记录，设置至少 12 字符的测试口令；退出重开、解锁、记录实际行动与复盘。未选方案保持 NOT_OBSERVED。
5. 测试错误口令、篡改后的加密备份、撤回授权后旧备份拒绝，以及应用返回/切后台后的敏感内容清理。
6. 检查竖横屏、动态字体、触控目标和 VoiceOver 的可用性。如无法完成某项，记录 NOT_RUN。

## 无隐私验收记录格式

~~~text
固定 Git 提交：
静态包 manifest SHA-256：
iPhone 机型及 iOS 版本：
Safari 与主屏幕安装：PASS / FAIL / NOT_RUN
主屏幕内离线就绪：PASS / FAIL / NOT_RUN
Mac 关机 + 飞行模式冷启动：PASS / FAIL / NOT_RUN
职业选择：PASS / FAIL / NOT_RUN
学习投资：PASS / FAIL / NOT_RUN
生活规划：PASS / FAIL / NOT_RUN
本机加密记录和复盘：PASS / FAIL / NOT_RUN
撤回后旧备份拒绝：PASS / FAIL / NOT_RUN
无障碍和横竖屏：PASS / FAIL / NOT_RUN
去隐私化失败说明：
~~~

不可将私人 tailnet 地址、口令、密钥和真实决策数据写入公开 GitHub。当前备份仅支持**同一安装、同一来源、当前授权账本仍有效**时恢复；网站数据被清除、设备迁移、存储被逐出后，不保证恢复。四种区间信息价值方法仍标为 UNSUPPORTED。真实个人效果与独立科学验收尚未完成；只有取得实际 iPhone 证据后，方可修改 NOT_RUN 状态。
