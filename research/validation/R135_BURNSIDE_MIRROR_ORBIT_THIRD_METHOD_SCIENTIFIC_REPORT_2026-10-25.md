# R135 第三方法科学报告：4096种二元信誉规则的镜像群作用

日期：2026-10-25。状态：`PASS_BOUNDED_LOCAL_BURNSIDE_MIRROR_E1`；新CI未执行，原R135 ESS验收不改变。

一手文献：Ohtsuki & Iwasa (2004), *How should we define goodness? Reputation dynamics in indirect reciprocity*, *Journal of Theoretical Biology* 231:107–120, DOI 10.1016/j.jtbi.2004.06.005。已有 `research/R135/` 对原作者4096规范策略和61440次入侵判定完成历史有界研究，本轮专门审计其信誉标签镜像约化计数。

冻结协议先于执行提交 `dd153e092c608ec97696fb13460a06654d477245`。独立JavaScript逐一构造256种八位规范与16种四位行动策略的镜像，核验4096次双次作用还原、4096个唯一像和每个轨道大小。结果：规范固定点16，策略固定点4，联合固定点64；大小为1的轨道64个，大小为2的轨道2016个，共2080个。独立Burnside计算 `(4096+64)/2=2080`，与逐项轨道枚举及原R135历史2080一致。

两项预设错误变换负对照均被拒绝。另在本轮本地Python环境使用独立位数组和集合枚举，得到固定点64、大小1轨道64、大小2轨道2016、总轨道2080、完整覆盖4096，结果相同。

可重放源码：`research/validation/r135_burnside_mirror_orbit_third_method.js`；机器收据：`research/validation/R135_BURNSIDE_MIRROR_ORBIT_RECEIPT_2026-10-25.json`。运行环境：项目内标准JavaScript计算及本地Python标准库，无外部计费计算。没有启动新GitHub Actions。

**边界**：镜像轨道计数正确不保证原有161个ESS、136个AllD、25个非平凡ESS或五组福利敏感性数字正确。本轮没有重新执行原R135 61440次入侵扫描，也没有调用原作者计算软件。该结果属于项目内部有限合成E1方法复核。E2真人预测0，E3历史预测0，外部研究团队独立复现0。R073与PESEN v0.1冻结。original239队列保持不变。
