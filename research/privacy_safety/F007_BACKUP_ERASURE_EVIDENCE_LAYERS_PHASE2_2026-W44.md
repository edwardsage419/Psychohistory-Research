# F007 备份快照、共享数据块及多密钥删除证明（第二阶段）

日期：2026-10-29，第44周。状态：IN_PROGRESS_UNADOPTED。第一阶段已归档。本轮为零费用、人工数据状态机与公开英文文档核验。F006本周已完成，无须重复专题。

## 原始来源及适用范围

S1 restic官方当前快照删除说明 https://restic.readthedocs.io/en/stable/060_forget.html ：forget删除快照引用，prune才处理不再引用的数据块，仍被其他快照引用的数据块需要保留。
S2 restic官方加密与密钥管理 https://restic.readthedocs.io/en/stable/070_encryption.html ：一个仓库允许多个访问密钥，支持list/add/remove/passwd。删除一个访问密钥不能推出其他密钥失效。
S3 restic官方仓库准备 https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html ：仓库可含多个访问密钥。
S4 NIST SP 800-88 Rev.2最终版 https://csrc.nist.gov/pubs/sp/800/88/r2/final ：介质清除应按具体方法与验证程序留存证据。
S5 英国ICO存储限制指导 https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/ ：备份副本仍属于生命周期治理范围。
上述为文档支持的机制，实际清除结果须由具体部署独立证明。

## 本轮人工状态机验证

使用 research/privacy_safety/f007_backup_erasure_state_20261029.js，Node 22.16.0本地运行22项断言，失败0。人工快照S1引用数据块P和Q，S2引用P和R。forget S1后P、Q仍存在；prune后Q清理，P仍因S2引用保留。移除访问密钥K1后K2仍可访问P。随后forget S2但尚未prune时P仍在；最后prune后人工仓库中的P、R均不存在。另建只有密钥被清空的人工状态，密文数据块仍存在。以上只模拟引用计数和访问条件，没有调用restic二进制程序或删除真实文件。

任何人工状态下的GLOBAL_ERASED均为UNVERIFIED，因为离线副本、对象存储版本、缓存、存储介质残留和外部保存的密钥均未独立核验。即使人工本地数据块已经不存在，也不能推出实际世界完全删除。密钥全部不在模拟集合中只能说明该模拟的本地访问失败，不能证明所有外部密钥或密钥副本已经销毁。

## 候选控制与阻塞

C1 分开记录快照元数据删除、prune完成、共享数据块存活、剩余密钥、外部副本与介质清除证据。C2 每次撤销授权先停止活跃推理使用，再追踪备份删除与到期。C3 只有实际复核对应仓库和介质，才允许标记对应范围已验证；全局清除必须保留UNKNOWN直至完整证据。C4 数据块共享引用与仓库级加密密钥的作用域必须分开审计。C5 任何实际清理前需要独立授权、备份恢复风险评估和失败回滚计划。全部UNADOPTED。

本轮没有读取真实个人数据、密钥、备份仓库，也没有实际执行forget/prune或删除命令。F007仍IN_PROGRESS。下一阶段研究存储版本化、不可变对象保留期及可审计的删除证明边界。