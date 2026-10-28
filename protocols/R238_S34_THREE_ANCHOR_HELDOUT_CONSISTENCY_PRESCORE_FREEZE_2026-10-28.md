# R238 S34 三锚点留一交叉核验：计算前冻结协议

日期：2026-10-28。原目录 10-012 Historical Text Embeddings。证据 E1，仅限 R238 已冻结九个人工二维双时期世界。原 R238 正式验收状态不变。

## 输入及范围
固定输入为 `research/R238/R238_ALL_144_ORIGINAL_HIDDEN_SENSE_AND_OBSERVED_EMBEDDING_SOURCES.csv`，已归档原始 SHA256 `a3939283f67d40fc74d289daecde449566870cdeb1943a8431ae6d27457feceb`，及 `research/R238/R238_EXACT_RESULTS.json`。固定世界九个，时期0/1，观察词 A、B、C、D，D 为目标，A/B/C 为候选锚点。所有人工观察向量与潜在真值、频率、原源概率保持不变。禁止增加或调参世界。

## 事先指定的评分
每个世界按字典顺序使用三种有序锚点对 AB、AC、BC。对每一对 `(i,j)`，构造唯一线性二维变换 `T_ij`，满足 `T_ij(v1_i)=v0_i` 及 `T_ij(v1_j)=v0_j`。若锚点矩阵行列式为零，输出 `SINGULAR` 并停止该世界，禁止伪逆或任意选择。对未参与拟合的第三锚点 k，报告平方残差 `h_ij=||T_ij(v1_k)-v0_k||²`。对目标 D，报告 `d_ij=||T_ij(v1_D)-v0_D||²`。计算每世界 `h` 的零值数量、最小值、最大值、三项 `d` 及其最小最大值。使用严格有理数，禁止浮点容差。

## 事先指定的判定及反例
`ANCHOR_CONSISTENT` 当且仅当三项 `h` 都严格为0；否则 `ANCHOR_INCONSISTENT`。此判定只检测三锚点能否由同一个线性映射连接，不能定位漂移的锚点，也不能验证目标 D 的真实语义。固定负对照 STABLE_BASE、GLOBAL_ROTATION、GLOBAL_SCALE_2、FREQUENCY_COMPOSITION_ONLY 的一致性；固定真实目标漂移正对照 TARGET_SEMANTIC_DRIFT、ROTATED_TARGET_DRIFT、FREQUENCY_PLUS_TARGET_DRIFT；固定污染锚点负对照 ANCHOR_DRIFT_FALSE_ALIGNMENT；SENSE_RECONFIGURATION_ALIAS 与 STABLE_BASE 必须保持所有观察诊断一致。若出现任何与冻结原源冲突的记录，判 FAIL，禁止替换输入。

## 两条程序路线及验收
R 路线从144条完整原始 CSV 聚合每个世界/时期/词的唯一观察坐标，严格检查每世界16条、每时期概率1/2、每词两个 sense 及坐标一致，然后通过 2×2 矩阵求逆计算全部27个 `h,d`。
B 路线独立读取冻结 R238 已验收 JSON 的观察向量，以行列式系数表达每个第三锚点及目标 D 在拟合两锚点基底中的坐标，再计算其时点0预测和残差。B 不调用 R 的变换矩阵或计算结果，只在末端比对27组两种残差和9组判定。错误注入将一项 R 收据中的 `h` 改为999，必须检出。
额外验证：所有9世界原始观察向量与冻结 R238 JSON 相同；对完全观察别名，结果完全一致；不得将人工 E1 宣称为真人 E2、历史 E3、训练词向量、历史文本语义或外部独立复现。

## 操作约束
仅新增路径。写入前重新读取 main HEAD、目标文件存在性与权限。提交时使用 `[skip ci]`，不主动触发任何收费 GitHub Actions。R073 冻结模型和评分、PESEN v0.1 均不得改动。原239交叉索引和154项待核队列只读。研究顺序仍为完成原R系列、再统一分类、最后模型熔炼。
