# R063 正式研究包

2026-10-15。继续 R063：Najar et al. (2020) 作者 metaVS 与固定 VS2 的机制源审计和 Fig6 来源数值核对。

本包不包含作者原始 task1.csv / task2.csv，本地没有这些原始源字节。也不包含完整作者 MATLAB 源码，只提供其固定 Git SHA 和对应 GitHub 网址。

文件说明：

* `R063_EVIDENCE_AUDIT.md`：科研结论、模型和实证边界。
* `r063_metavs_audit.py`：与所见 MATLAB 更新分支对齐的独立 Python 状态机制翻译和合成反例。
* `test_r063_metavs_audit.py`：状态、更新顺序、边界反例测试。
* `r063_fig6_check.py`：从作者 Figure 6 CSV 连接器输出转录的公开参数数列独立重算。
* `test_r063_fig6_check.py`：人数、条件、模型频率、论文精确 P 值验证。
* `FIG6_RESULTS.json`：本地重算结果。
* `MECHANISM_EXAMPLE.json`：合成反例轨迹总结。
* `SHA256SUMS.txt`：包中各文件的本地校验。

重跑（Python 3.10+）：

```bash
python -m unittest discover -v
python r063_metavs_audit.py --example
python r063_fig6_check.py
```

基本机制不依赖第三方库。Figure 6 的精确 Wilcoxon 和 Mann–Whitney P 值需要 `scipy`；若没安装 scipy，程序仍输出人数、频率、分层均值，但标记 P 值计算未执行。

原文：https://doi.org/10.1371/journal.pbio.3001028
作者固定提交：https://github.com/hrl-team/mfree_imitation/tree/554ee8007ff6fd1c51cd68d7d254f22a34e6dab1
原作者 MATLAB：https://github.com/hrl-team/mfree_imitation/blob/554ee8007ff6fd1c51cd68d7d254f22a34e6dab1/models/VS/metaVS.m
原作者固定 VS2：https://github.com/hrl-team/mfree_imitation/blob/554ee8007ff6fd1c51cd68d7d254f22a34e6dab1/models/VS/VS2.m

科研级别：作者源码实读 + 作者 Figure 6 汇总数值复核 + 本地合成反例测试。没有原始 trial CSV 的本地端到端模型验证。
