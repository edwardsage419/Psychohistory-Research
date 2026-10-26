# R196第三方法：变分后验的未来预测风险

日期：2026-10-27。状态：PASS_BOUNDED_INTERNAL_E1_POSTSCORE_ADDENDUM。原R196正式有限E1结题不变。事前冻结协议：protocols/R196_POSTERIOR_PREDICTIVE_BRIER_24_THIRD_METHOD_FREEZE_2026-10-27.md，先于本轮程序和计算收据提交（commit c825f673d5959bc0b28f02d2dff4453d86dae4dd）。

## 输入与设计

使用R196原有12个四态人工真后验（research/R196/R196_ALL_12_EXACT_POSTERIOR_SOURCES.json，Git blob 490c30eb8bd912afcb6e8d2d1cafacb1928b2f39）及原有24个已评分COARSE/FINE最优均值场近似（research/R196/R196_EXACT_RESULTS.json，blob f39ccf402edbfbc11f9d8eb135efec6fff838b0e）。没有重新优化ELBO，没有改动网格、likelihood、m=1/2、原后验或选择规则。

在同一个未变潜在状态z上，已有m次Y=1，预测下一个独立条件观测Y_new。真未来成功概率t=Σ_z P(z|Y_{1:m})w_z/M，M=max(w)。给定预测分布q，a=Σ_z q_z w_z/M。对每个源比较ORACLE、PRIOR、FORWARD_PRODUCT、COARSE、FINE五种预测，合计12×5=60条。逐条精确Fraction计算未来Brier=t(1-a)^2+(1-t)a^2，超额Brier=(a-t)^2。只限同潜变量的下一次观测，不能移用到独立新群组。

## 实际计算结果

12个来源条件中，FINE相对COARSE的未来Brier严格改善8个、相等4个、变差0个。FINE相对未更新均匀先验改善10个、相等2个、变差0个。对全部60个方法行，Brier超额与预测偏差平方逐Fraction严格相等。未出现“更低KL而未来Brier更差”的本次预定反例，记录0，不扩充来源寻找反例。

INDEPENDENT_SKEW在m=2时，真下一次成功率196/225，先验预测4/9，COARSE预测25/36，FINE预测121/144。对应超额Brier分别为1024/5625、2809/90000、1369/1440000；原始均值场两网格都错过真独立后验的1/10边际，细格点在本次目标下减少了预测误差。

POSITIVE_COUPLED在m=2时，真下一次成功率4097/4112；FORWARD_PRODUCT预测17/32，FINE预测407/512。两者均丢失潜在联合依赖，但对本次特定未来二元事件的预测差距不同。后验KL、隐变量边际拟合和单一未来事件Brier属于不同评价对象，不能由本轮风险结果证明潜在类别得到识别。

## 科学边界与负例

UNIFORM的m=1、m=2，所有五种方法给出相同未来成功概率，超额风险为0。独立新潜变量错误迁移负对照在10个非平凡来源被检测到，另外2个UNIFORM来源按预期不检出。省略未来Y=0损失项的错误Brier公式在50条方法行被检出，另10条因预测退化等代数原因不检出；检测数量由独立B程序给出。

本轮未来事件由已知人工机制条件生成，精确风险属于模型内条件预测评价；没有采集真人独立样本、没有校准曲线、没有真实历史事件。新真人E2=0，新历史E3=0，外部独立团队复现=0。R073和PESEN v0.1未改动。

## 复现与验收

R原生JavaScript脚本：research/validation/R196_POSTERIOR_PREDICTIVE_BRIER_THIRD_METHOD_2026-10-27.js。精确60条收据：research/validation/R196_POSTERIOR_PREDICTIVE_BRIER_60_EXACT_RECEIPT_2026-10-27.json。脚本读取原仓库JSON并在标准Node.js中输出完整JSON，使用BigInt有理数。R计算在本轮JavaScript执行环境实际运行；归档Node.js文件尚未在远端CI运行。

B轨独立潜在状态×未来事件枚举，180项精确字段比较全部一致，60项概率质量核验通过，错误机制负对照已执行。该复算属于同项目内部程序性独立验证，原R196正式科研验收不因本轮新增附录而提升证据等级。

主动新增费用0。GitHub Actions费用额度没有独立核验，本轮不启动CI。