# 心理史学 R002 补档包

日期：2026-10-15（追补日期）
状态：RETROSPECTIVE GAPFILL, SYNTHETIC ONLY

## 重要出处声明

经检索最早版本研究主控台和过往研究进度，R001教学演示后直接出现R003机制识别实验。目前未找到此前独立执行的R002报告或正式包，无法证明历史上绝对不存在。因此这份文件是**2026-10-15新执行的追补研究**，绝不能冒充2026-10-14已经完成的原始R002或事前注册研究。

此包在学术目标上连接R001教学演示与R003三模型合成识别。但缺乏R001、R003原始全部代码的逐行比对，所设M0、M1、M2是概念等价的全新简化实验设计，并非旧R003实现的数值复刻。

## 文件

- `R002_RESEARCH_AUDIT.md`：正式研究报告、数学和边界
- `ROUND_CONTINUITY_R001_R063.csv`：连续性审计状态表；区分历史摘要与本地归档
- `UNRESOLVED_EVIDENCE_GATES.md`：真实证据与归档缺口
- `r002_method_bridge.py`：合成数据、时间顺序、模型拟合与留出集评分
- `test_r002_method_bridge.py`：21项本地软件测试
- `R002_SYNTHETIC_RESULTS.json`：冻结随机种子下的实际合成运行结果
- `SHA256SUMS.txt`：包内文件指纹（不含自身）

## 复现

本地 Python 3.10 或更新，无第三方依赖：

```bash
python -m unittest -v test_r002_method_bridge.py
python r002_method_bridge.py --output R002_SYNTHETIC_RESULTS.json
```

实际输出只检验人造数据上的程序行为，**不构成人类社会学习机制、因果效应或历史变化的实证支持**。PESEN v0.1未改动。
