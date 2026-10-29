# F007第三阶段：版本化存储、不可变保留与删除证明

日期：2026-10-29，第44周。轨道：privacy_safety。状态：BOUNDED_DESK_STUDY_COMPLETE_UNADOPTED。F007第一和第二阶段已归档。本轮零新增费用，未接入真实敏感数据。

## 官方来源与证据等级

S1 [官方文档] AWS S3 Versioning https://docs.aws.amazon.com/AmazonS3/latest/userguide/versioning-workflows.html ：开启版本化时，不指定versionId的DELETE创建删除标记，旧版本仍可按版本ID访问。
S2 [官方文档] AWS Delete Object Versions https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html ：永久删除特定版本需指定版本ID。
S3 [官方文档] AWS S3 Object Lock https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html ：保留期和法律保全作用于具体对象版本，compliance与governance模式权限不同；删除标记可以覆盖受保护旧版本。
S4 [官方文档] AWS Object Lock considerations https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html ：governance绕过需要特定权限及显式请求；法律保全独立生效；生命周期无法删除仍锁定的版本。
S5 [正式标准] NIST SP 800-88 Rev.2 (2025-09-26) https://csrc.nist.gov/pubs/sp/800/88/r2/final ：介质清除需要适用方法及验证证据。

本轮只阅读免费英文公开文档，没有AWS账户、对象、云资源或API请求。官方文档支持机制描述；模拟仅验证人工状态机，不证明真实服务或个人数据已经清除。

## 人工反例与运行

使用 `research/privacy_safety/f007_versioned_lock_erasure_synthetic_20261029.py`，Python标准库执行26项断言，失败0。模拟同一对象键的三个版本：v1为未到期COMPLIANCE保留，v2为未到期GOVERNANCE保留，v3处于LEGAL_HOLD。简单DELETE后默认GET返回NOT_FOUND，按版本ID仍可读取v1/v2/v3。v1在保留期内不可绕过删除；v2仅在有权限且显式绕过时可删；v3在法律保全未解除时拒绝删除。到期并满足相应条件后版本可删除。模拟仓库全部版本清空后，外部副本、密钥及介质清除未验证，GLOBAL_ERASED仍为UNVERIFIED。

风险：默认GET 404误作彻底清除；忽略历史版本；误以为保留期到期自动清除；误以为governance不可绕过；忽略法律保全；忽略复制和离线备份。

## 候选控制与研究边界

C1 分开记录停止参与推理、当前版本不可见、版本永久删除、备份与副本核验、介质或密钥清除验证。C2 保存每个版本的ID、锁定模式、截止时间、法律保全及证据。C3 撤销授权先阻断活跃使用，遇保留冲突时提供人工申诉与到期复查。C4 删除失败返回RETENTION_BLOCKED或LEGAL_HOLD_BLOCKED。C5 全局清除保持UNKNOWN直到全部副本与适用方法独立验证。C6 高影响删除必须人工授权，禁止自动开通收费云服务。全部UNADOPTED。

本周F006已完成。F007三阶段的官方资料与人工反例研究有界完成；真实部署清除验证、法律义务、跨供应商测试和外部复现仍OPEN。下一候选F008：跨设备同步与本地派生缓存撤销传播。
