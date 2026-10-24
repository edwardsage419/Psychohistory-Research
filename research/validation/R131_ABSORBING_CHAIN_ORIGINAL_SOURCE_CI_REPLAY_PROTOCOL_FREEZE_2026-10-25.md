# R131 84行吸收链原始源码 CI 重放预冻结协议

日期：2026-10-25。对应 original239 05-007。目标：补齐已归档 R131 第三种算法尚未运行的 CI 和未直接执行原作者项目Python程序的缺口。固定已有源码和CSV，不新增模型参数、调参、预测分数或研究假设。

来源锁定：独立JS吸收链源码 `research/validation/r131_independent_absorbing_chain_exact.js`，Git blob `db7eed80c4210eec8c9bde1d500952da6a4873d6`；原始84行CSV `research/validation/R131_ABSORBING_CHAIN_84_EXACT_FIXATION_ROWS_2026-10-25.csv`，Git blob `5d2637d19abac6d963d5bac320d35c16747f4769`；既有R131原Python `research/R131/r131_taylor_jonker_1978_evolutionary_game_exact.py`，Git blob `3c61e0c3c0fe7a6d4458eccd8fc18e9714e7152f`。

验证门：在公开仓库免费标准 Ubuntu runner 使用Node标准库vm重新运行既有JS `runAudit()`，确认84内部固着概率、126转移概率行、84个零残差、21个原公式比较、两项负例，以及再生CSV与仓库原始CSV逐字节一致。另以Python标准库导入未修改R131源码，核验Git blob身份，针对N=2..8及(3,2),(1,1),(2,3)三适应度组合实际调用原函数21次，与已归档CSV的初始单个突变者行精确Fraction一致。运行原R131 63项单元测试。任何不一致都必须失败并保留日志。禁用外部API、收费runner、上传artifacts、额外依赖和覆盖已有文件。

通过等级上限：`PASS_BOUNDED_INTERNAL_ABSORBING_CHAIN_ORIGINAL_SOURCE_CI_E1`。这仍是项目内部方法独立性，非外部团队独立复现；E2=0，E3=0。保留R073和PESEN v0.1冻结，原239共享索引不自动更改。
