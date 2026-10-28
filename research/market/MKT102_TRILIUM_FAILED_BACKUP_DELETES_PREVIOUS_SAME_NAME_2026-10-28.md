# MKT102 Trilium同名备份失败清理可能删除既有恢复点

日期：2026-10-28。证据等级：MARKET E1，固定英文源码、同版本上游测试及隔离文件系统语义重演。未运行Trilium完整应用，实际用户影响UNKNOWN。零新增费用。

## 去重与固定来源
MKT101已经记录密码不可用时的未加密本地降级及成功写入后删除另一扩展名的同名旧备份。本轮新增独立问题：**写入失败的异常清理分支可能删除此前成功生成的同名备份**，与MKT101成功路径不同。

TriliumNext/Trilium main固定提交 `5285da233c1182539b70e43caee8c957b0e499cd`，本轮复核上游main仍为该提交。
生产源码 `apps/server/src/backup_provider.ts`，Git blob `b3de0029f608d769a3badec2f307d4a5bfc1aaff`：
https://github.com/TriliumNext/Trilium/blob/5285da233c1182539b70e43caee8c957b0e499cd/apps/server/src/backup_provider.ts
测试源码 `apps/server/src/backup_provider.spec.ts`，Git blob `72900209a4428c8b085e9df19b62ce381a10c660`：
https://github.com/TriliumNext/Trilium/blob/5285da233c1182539b70e43caee8c957b0e499cd/apps/server/src/backup_provider.spec.ts
官方英文备份说明：https://docs.triliumnotes.org/user-guide/setup/backup

## 本轮真实增量
生产函数 `writeBackup` 使用确定的 `backup-{name}.db` 或 `.tnbackup` 目标路径。其try块中，明文备份直接调用 `sql.copyDatabase(backupFile)`；容器备份调用 `writeContainer`，先写临时快照和 `.part`，成功后才 `renameSync(partial,backupFile)`。外层catch无条件调用 `fs.rmSync(backupFile,{force:true})` 再抛出异常。

条件性反例A：同目录已经存在有效 `backup-daily.db`；下一次相同名称的 `sql.copyDatabase` 在触及目标之前抛错；catch仍删除目标路径，因此原有有效备份被移除。
条件性反例B：同目录已经存在有效 `backup-daily.tnbackup`；下一次 `writeContainer` 在临时快照阶段或重命名前失败；旧目标原本未被新文件触及，外层catch仍删除旧容器。
若自定义目录写入失败，`backupNow`尝试默认目录；该回退不能恢复已删除的自定义目录旧备份。默认目录自身失败时，异常向上传播。若原先没有同名备份，清理部分文件的设计合理；关键缺口是旧目标与本次不完整输出没有区分。

本轮使用Python标准库临时目录做两种**合成文件系统语义重演**：在已有同名文件时注入写入前异常并执行相同 `unlink(missing_ok=True)` 清理，两种模式均观察到旧文件消失。该重演没有执行Trilium源代码，不能称为产品动态复现或已发生用户数据丢失。

## 测试覆盖核对
固定 `backup_provider.spec.ts` 共51个 `it` 测试。已覆盖空目录下的写入失败清理、自定义目录失败回退、缺密码时转默认目录、格式切换、读取容器头中的 `encrypted` 标记、损坏容器可见性。未在这51项中发现“已有有效同名备份且新备份写入失败后必须保留旧文件”的专门断言。测试缺口不证明生产事故。上游测试未在本轮执行，不能报告Vitest PASS。

## 产品机制矩阵
输入：本地SQLite个人笔记及元数据、备份名称、压缩/加密选项、系统密钥环、目录、I/O异常。
状态：原同名备份、临时快照、部分文件、完成的目标文件、错误日志、回退目录、容器头的加密标志。
算法：SQLite备份复制或快照转容器，失败时删除目标路径，成功后删除另一扩展名的同名副本。
目标：保持可恢复数据库副本；没有人生决策效用或长期预测准确性证明。
反馈与自我修正：自定义目录失败可回退默认目录，密码失败有toast；未发现对“原有备份被异常清理移除”的专门告警与自动恢复。
隐私与权限：本地存储，可选加密和自定义目录；容器头可以报告真实加密状态；未验证文件权限和用户真实泄露。
解释性：源码及51个测试可审阅；缺少真实错误发生率与完整运行收据。
费用：开源源码和公开文档可免费审阅；本轮没有部署、注册、购买或收费调用。
局限：只验证固定源码分支、测试存在性和隔离文件语义；不同文件系统、SQLite实际备份实现及用户真实配置未复现。

## 候选控制，全部UNADOPTED
C1 同名旧备份始终保留，先写唯一临时文件，完成验证后再原子替换。
C2 失败清理仅删除本轮新建的临时文件，禁止无条件清理旧完成文件。
C3 测试矩阵分别覆盖明文、压缩、加密、同名旧备份、写入前失败、部分写入失败及回退目录。
C4 记录备份完成状态、实际加密状态、最后一次失败与最近成功恢复点，用户可检查。
C5 涉及个人决策未来知识库时，默认保护最后一个可验证恢复点，避免不可逆自动操作。

研究证据分级：固定源码及测试为文档/源码E1；隔离重演是人工合同测试；生产实际风险发生率、数据泄露和科学决策改善均UNKNOWN。下一轮MKT103优先检查同名写入失败在不同开源知识库中的原子替换策略，避免重复MKT101/102。
