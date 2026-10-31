# R308 S104 原生CLI重放补充

UTC 2026-10-31。本补充发生于首份科学报告及B审计报告归档之后，追加新证据，不改写先前NOT_RUN及v1失败记录。

## 真实执行

使用本地现有 Node v22.16.0，Python 3标准库。在隔离的 /mnt/data/r308_s104 工作目录执行：

node r308_s104_gate_observability_v2.js --selftest
node r308_s104_gate_observability_v2.js --emit /mnt/data/r308_s104/native
python b_r308_s104_fraction_audit.py /mnt/data/r308_s104/native/R308_S104_ALL_432_GATE_WORLDS.csv /mnt/data/r308_s104/native/R308_S104_EXACT_OBSERVABILITY_RESULTS.json
python -O b_r308_s104_fraction_audit.py /mnt/data/r308_s104/native/R308_S104_ALL_432_GATE_WORLDS.csv /mnt/data/r308_s104/native/R308_S104_EXACT_OBSERVABILITY_RESULTS.json

全部实际退出码0。Node原生自测输出 PASS 432 worlds, 16 groups, 4 schemes。Python两个模式均得到[56,186,276,276]类别、[20,140,270,270]单例，8项变异全部拒绝。

实际执行源码经Git blob重算与远端完全一致：
R v2 JS：6050d1f704c592767b2d396546379486536defe0，3686字节。
B Python：6a685c2e89256c84ca6c4636b38be16c2060d5a7，5182字节。

Node新生成的CSV：20730字节，Git blob 5a535fdb7f54737b2cc4af48707518176b7dd177，SHA256 4dd951f576d202e0db7ada5c4860a3e33d41d1b7e71182e146f92621fb092524。
Node新生成的JSON：147707字节，Git blob 7fed42e415e537c932203b41c251077c57392837，SHA256 a52154aabdf0256192fc3b399b74557613c34aa541664bd567a899c445a41b29。

两个新生成文件均与远端归档的Git blob完全一致，B程序在真实生成文件上直接执行成功。此项关闭 S104 v2原生Node重放关口。原始v1序列化失败仍保留；原R308的历史源码与结果未更改。

## 证据边界

属于同一项目内的非盲态E1计算与归档一致性复核。没有新真人E2、历史E3、外部研究团队独立复现或真实概率校准。S104新增科学结论仍限定PARTIAL，原R308正式有界E1验收不变。没有启动GitHub Actions，实际账户费用及额度未独立核验。
