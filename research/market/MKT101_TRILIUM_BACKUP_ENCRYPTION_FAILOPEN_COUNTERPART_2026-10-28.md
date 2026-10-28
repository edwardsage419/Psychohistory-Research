# MKT101 Trilium备份加密降级与同名备份替换机制
日期：2026-10-28。等级：MARKET E1，固定源码与官方英文文档；尚未运行真实Trilium应用。零新增费用。

## 上游固定来源
TriliumNext/Trilium main固定提交 5285da233c1182539b70e43caee8c957b0e499cd。
apps/server/src/backup_provider.ts Git blob 已读取，核心代码包含 resolveFormat、backupNow、writeBackup、writeContainer。
packages/trilium-core/src/services/backup.ts 固定源码包含定期备份调度。
官方英文文档 https://docs.triliumnotes.org/user-guide/setup/backup 。
仓库许可证 package.json 声明 AGPL-3.0-or-later。
源码 https://github.com/TriliumNext/Trilium/blob/5285da233c1182539b70e43caee8c957b0e499cd/apps/server/src/backup_provider.ts 。

## 本轮新增的条件性机制
当备份设置要求使用已保存的密码，而getPassphrase无法提供密码时，resolveFormat记录错误并发出15秒toast，返回 passphrase:null、keepLocal:true。backupNow随后跳过自定义备份目录，在默认本地目录写入不加密备份。若未启用压缩，生成.db明文数据库备份；若启用压缩，生成.tnbackup容器，但容器的encrypted标记为false。文件扩展名不能单独证明加密状态。
writeBackup成功后删除同一目录、同一备份名称、另一扩展名的counterpart。因此在默认目录已有backup-daily.tnbackup加密备份且下一次因密码不可用生成backup-daily.db时，成功写入后原加密备份会被删除。若压缩启用，则同名.tnbackup被新写入的未加密容器替换。上述结论限定于代码路径、备份名称相同、写入成功及目标文件位于相同目录的条件。未进行真实文件系统测试。
设计上，降级时强制使用默认本地目录，避免把明文数据库写入原先可能用于云同步的自定义目录；同时允许本地备份在密码不可用时继续完成。官方文档确认启用加密之前产生的备份不会自动加密，密码更换只影响后续备份。恢复旧数据库还可能与同步集群较新状态冲突。

## 机制记录
输入：SQLite个人笔记、关系和元数据，备份开关、压缩开关、系统密钥环可用性、备份目录、同步状态。
状态：数据库快照、daily/weekly/monthly备份名称、文件扩展名、加密标记、最近备份时间、存储位置。
算法：SQLite复制；可选GZIP、scrypt派生密钥与AES-256-GCM容器；密码不可用时降级；成功后删除对应扩展名的同名旧备份。
目标：维持个人知识库的恢复能力。未发现人生效用优化或长期决策准确性证明。
反馈：日志与15秒toast提示密码不可用；未验证普通用户能否持续看到降级历史。
隐私权限：默认本地目录与可选自定义目录；密码丢失触发明文备份路径；未验证目录权限、真实攻击或备份外泄。
解释性：源码可以追踪分支，文档描述加密设置；实际安全仪表盘与降级事件留存UNKNOWN。
费用：开源免费客户端；自托管需要自有设备，任何额外云服务均不在本项目使用范围。
局限：六处固定源码合同已检查，三个配置分支做了人工静态演绎，未运行上游Vitest、完整应用或真实磁盘错误注入；未认定已发生真实用户数据泄露。

## 候选控制，均未采用
C1 将加密设为强制策略时密码不可用应暂停写入，或者仅在用户明确接受后本地降级。
C2 备份列表直接展示每个文件实际encrypted标记及降级原因。
C3 同名替换前核验加密级别，禁止低级别覆盖更高级别的唯一可用恢复点。
C4 密码轮换时枚举旧备份并提示未加密历史副本。
C5 恢复前校验与同步集群的版本关系，允许用户保存恢复前副本。

下一轮MKT102检查Trilium备份错误处理测试覆盖和同名替换条件，或者比较另一开源系统的加密降级策略。
