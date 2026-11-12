# R275/S71 有界缺陷工作包

2026-11-12，main d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c，12-005/P0。
原S71报告和B远端addendum明确：归档Python gate与开发副本blob不同，原生完整文件执行
NOT_RUN；原Node CLI也NOT_RUN。当前无R275开放PR；R276已有native addendum，不重复。

先复现：只将归档人工结果JSON的evidence改为E3，原精确B CLI普通模式exit1、stdout空；
同一代码同一输入加-O却exit0/PASS/3072行。证据保存evidence/baseline*，修复前取得。
原因是数学/资格验证依赖assert，优化模式会删除检查。这不是默认运行错误，也不能由此
推断历史数值或真人结论已变化。S71完全人工；真人评分NOT_RUN。

拟最小候选：仅在独立patch内把原B assert改显式require/ValueError，保留全部Fraction
公式、K计数、参数、模型顺序、列和输出结构。原文件不改，不建另一个数学算法。
用AST证明所有原条件逐一保留且其余原AST不变；保留普通与-O的原失败/候选通过证据。

复用原Node --emit再生2份人工产物、逐字节比较；原B普通/优化模式先对真实归档及再生
执行，再分别以原6类坏输入暴露/确认检查。候选在两模式读取同一输入，所有坏输入必须
领域ValueError拒绝；源公式变异（条件被删除）必须被AST身份门拒绝。
来源前后固定哈希、原始输出与退出码归档、独立只读复核、独立draft PR。
不改冻结程序/模型/结果/协议，不接入生产，不升级科学等级，不运行未知费用CI。
