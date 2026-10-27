# R210第三方法：正式原始材料SHA256及远端复算证明

日期：2026-10-27。冻结协议提交 `8f16b184400e3d925593a79b50de54492fe88e15`。正式研究及B轨归档提交 `455a70e6c7c406abd9d2c5e6b24f8aaa5fca5c66`。

远端归档完成后，重新通过GitHub连接器读取R、B两份原生JavaScript程序、R收据JSON、420行CSV及B审计JSON，分别在隔离JavaScript执行环境运行归档的程序。重新生成的R JSON、CSV及B JSON均与远端正式文件逐字节一致，复算失败0。R主程序结果420行、7世界、21世界规则组合；B轨18项独立解析期望比较、420项来源结构检查、12项可检出负对照，0失败。

下面的SHA256使用独立实现的标准SHA256算法对读取的ASCII原文件字节计算，算法已通过字符串abc的已知标准测试向量。Git blob SHA1为GitHub返回的文件对象身份，两种摘要含义不同。

| 归档路径 | Git blob SHA1 | SHA256 | 字节 |
| --- | --- | --- | ---: |
| `research/validation/r210_post_assignment_selection_third_method_20261027.js` | `755120bbd339c3105313c911d06d9d0a9bb7c9ec` | `90e7d53f843b7b658b82d7f37fe8caff35708ac8ef54904a289fb4948c08bbb1` | 5489 |
| `research/validation/R210_POST_ASSIGNMENT_SELECTION_21_WORLD_POLICY_RECEIPT_2026-10-27.json` | `b39dbc9db8cefe085475a0f05ccf7922814cd314` | `bd9a571c75786ed0cf886953b7829c30f111ae4a77da17890cbd48a775614de3` | 8436 |
| `research/validation/R210_POST_ASSIGNMENT_SELECTION_420_SOURCE_ROWS_2026-10-27.csv` | `1a66b2156b48eb998688431b780bb89e797c3db2` | `31becd433cf85e4d2d64eaa43b7ae0a003fabaef069275a2587e318b7f40ab0c` | 35347 |
| `research/evidence_audit/b_r210_selection_orderstat_independent_20261027.js` | `4c2b3effbe93cf19a74d58b56ae8bc406362d4dc` | `2b3c57e07c2967e7e36e4ba58e6a0df87387cbffee64380e40f8f0769adf2dd8` | 4882 |
| `research/evidence_audit/B_R210_SELECTION_ORDERSTAT_INDEPENDENT_AUDIT_2026-10-27.json` | `593ba34151fae964379813d593bb025bf49fc6cc` | `347b8a2ea340c4e41bc8044f0bac63bbb45722eb3946c74cd8d54251c3b4b146` | 3806 |

只证明人工研究材料的程序重演一致性。未运行远端GitHub Actions；CI状态另行核验。没有外部研究团队独立复现，没有新增E2/E3，也没有更新R073或PESEN v0.1。
