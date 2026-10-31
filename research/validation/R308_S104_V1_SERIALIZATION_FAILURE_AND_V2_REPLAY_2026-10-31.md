# R308 S104 原生输出序列化缺陷与修正记录

UTC 2026-10-31。原始脚本 research/validation/r308_s104_gate_observability.js 的 Node 字符串常量包含双反斜杠，CLI emit 将字面 \\n 写入CSV和JSON。实际以 V8 执行其原样脚本并注入内存文件系统，观察到 CSV 输出 21163 字符，与归档 CSV 20730 字符不相等。该失败保留，不覆盖原脚本。

v2 文件 research/validation/r308_s104_gate_observability_v2.js 仅修正输出序列化换行字符串。再次通过 V8 原样函数体和模拟 Node 文件接口执行 --emit，完整CSV和JSON均与远端归档文本逐字符一致。v1与v2算法主体相同，432个世界和16组计算没有改变。

测试性质：真实 V8 函数执行及模拟 Node CLI 文件接口；原生 node 进程 CLI 尚未在本轮执行，状态 NOT_RUN。原 v1 的 CLI 归档重放失败不得抹去，后续需在有Node环境下运行 v2 --selftest 和 --emit 并对比归档字节。E1 内部非盲态工程审计，非外部科学复现。
