# B轨：R308 S104 独立Fraction复算、错误注入及真实失败保留

UTC 2026-10-31。任务键 (B,R308,S104,exact_fraction_gate_oracle)。审计已阅读原R308 README/原科学报告/原JSON/原冻结协议概要及S104冻结协议，属于内部非盲态复核。冻结提交 e3d2b690a794d4fd3e748b43a59e71d56eda09cf。

## 独立路线与实际执行

B独立Python 3标准库 Fraction 脚本 research/evidence_audit/b_r308_s104_independent_fraction_audit.py 从八种三元组和两个聚合规则重新生成432世界；逐个计算4种观测向量，并用 defaultdict 按精确有理数签名分组。没有导入R JavaScript生成器。

实际在本地Python普通模式和 python -O 优化模式执行自测，两个模式各得到432世界、16组、类别总数[56,186,276,276]、唯一识别世界[20,140,270,270]。八种有效数据变异各自被显式ValueError拒绝：删世界、重复世界、改B、改A、改单门查询、改双门查询、改类别数量、改单例数量。普通及-O均8/8拒绝。

独立Python重新生成远端432行CSV，字节数20730，Git blob SHA1=5a535fdb7f54737b2cc4af48707518176b7dd177，与GitHub归档文件一致。另经GitHub回读，远端CSV与JSON逐行字段及代数共4037项检查通过；远端JSON blob=7fed42e415e537c932203b41c251077c57392837。R主线另核对原R308 432世界B和A均一致。

## 失败证据与边界

首次R脚本v1使用双反斜杠换行常量，V8执行并模拟Node文件接口后生成21163字符CSV，未能与20730字符归档一致。此项 FAIL 保留在 research/validation/R308_S104_V1_SERIALIZATION_FAILURE_AND_V2_REPLAY_2026-10-31.md。v2修复序列化后，V8模拟文件接口对CSV与JSON逐字符一致。原生Node进程CLI仍为NOT_RUN。不得把模拟接口视作原生Node命令行通过。

审计范围限于原项目E1人工公式及结构完整性。没有真人数据、独立外部研究团队、独立样本、现实概率校准、因果效应或历史E3。B轨程序验证通过只支持计算一致性，S104正式科学验收PARTIAL。原R308历史正式E1验收状态未变。

下一步：在不产生额外费用的现有Node环境中运行v2 --selftest和--emit，验证原生进程字节一致；如失败继续保留原始日志。另检查B代码对JSON证据等级字段的强制验证，当前B脚本未建立完整证据标签白名单门，不能宣称已覆盖。
