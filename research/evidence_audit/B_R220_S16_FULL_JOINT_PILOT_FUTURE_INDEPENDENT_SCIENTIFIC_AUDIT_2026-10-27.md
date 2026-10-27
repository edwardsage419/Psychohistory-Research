# B轨：R220 S16独立全联合枚举科学审计

日期：2026-10-27（Asia/Singapore）。状态：INTERNAL_INDEPENDENT_ALGORITHM_PASS / NEW_CI_NOT_RUN。证据E1人工。原239 09-011原R220正式验收不变。

## 事前冻结与来源绑定

冻结协议 `protocols/R220_S16_INDEPENDENT_PILOT_TWO_NUISANCE_FUTURE_AIPW_PRESCORE_FREEZE_2026-10-27.md`，冻结提交 `88134446f64a1a6c866bed14ebdb86c42b0764af`。R正式精确收据 `research/validation/R220_S16_PILOT_TWO_NUISANCE_6_WORLD_EXACT_RECEIPT_2026-10-27.json`，Git blob `a75dd518a1b9094c329ecb4cf37c0c5863d787db`。B脚本 `research/evidence_audit/b_r220_s16_full_joint_future_enumeration_20261027.js`，Git blob `7e61019005ff8b4ef8258ab52fffb98046a91dba`。

R轨以BigInt有理数对256 pilot处理赋值积分，未来用独立Bernoulli条件矩直接求E与Var。B轨单独实现人工世界、pilot学习规则和观察分数，使用Number浮点逐项枚举256 pilot×256 future的全部联合处理赋值，直接对平方误差积分。B程序不导入R脚本或其方法输出；只在最终比较时读取R收据。两条计算路径分别使用解析矩与完整联合来源枚举。

## 实际核验

六个正值性世界各65536个联合来源槽，共**393216个**，全部实际枚举。每世界五种方法，分别比较均值、方差、偏差、MSE，共6×5×4=120个数值字段。另完成6世界各pilot质量、future质量、联合来源数量18项，无正值性null资格1项，未来Y1变异与未来Z泄漏及对应均值核对4项，合计**143项检查，失败0项**。最大数值绝对差7.638334409421077e-13，事前冻结容差1e-9。

故意将future第一个单位的Y1增加1，在固定pilot mask=0条件下，未来AIPW期望由11.72变为11.9075，与R精确收据293/25、4763/400一致。将future处理指示加入pilot倾向计数会将原qhat=1/6错误改成2/7，时间泄漏负对照检出。无正值性世界五方法均返回null；原固定AIPW基线六世界与原R220精确收据一致。

机器收据 `research/evidence_audit/B_R220_S16_120_FIELD_FULL_JOINT_ENUMERATION_RECEIPT_2026-10-27.json`，Git blob `0cafa119cf41f8bc6a7489fe3f56718e94173265`。首版B脚本与收据曾暂存占位符`__R_BLOB__`，发现后在已读取各自blob SHA条件下修订这两个本轮新增文件，保留Git提交历史。最终脚本与收据均绑定上述真实R收据blob。远端重新读取R/B程序和机器收据并执行，两个重放结果与归档JSON逐字段一致。

## 仍未覆盖的科学风险

这是同一项目内部的不同算法复算，**外部独立复现0项**。pilot与future虽使用不同人工单位ID和独立处理赋值，结构类型与潜在结果完全复制，不能称为外部真人留出实验。pilot只含八个合成单位，所有风险是冻结设计分布的数学期望；没有真人独立场次、实际倾向估计器交叉拟合、经验概率校准、簇重采样或现实因果识别检验。真实处理概率与潜在结果仅作为人工oracle和积分输入；若将其泄漏给公开学习器，结论无效。

A轨公开数据许可与R073协议资格仍需独立解决；原R073/PESEN v0.1冻结不变。新CI未运行，GitHub免费额度未独立核验，主动新增费用0。后续优先在真正独立真人实验中事前冻结训练、预测和评分，不能把此E1转写为E2或E3。
