# A轨 2026年10月28日 社会网络与真人博弈公开数据来源资格审计

## 候选一：Grujić与Lenaerts（2020）空间重复囚徒困境
论文DOI `10.1098/rsos.200618`，数据DOI `10.5061/dryad.7fq25s8`，Dryad英文页面：https://datadryad.org/dataset/doi:10.5061/dryad.7fq25s8 。已实际核验数据归档列出`DataSet.csv`（215.22 KB）、`README_for_DataSet.txt`（1.41 KB）及两份英文实验说明PDF。实验有两个信息条件，参与者在方格网络上重复进行囚徒困境互动，涉及自身行动、邻居行动及收益信息的潜在比较。实际尝试下载CSV端点`https://datadryad.org/downloads/file_stream/296893`和README端点`https://datadryad.org/downloads/file_stream/296894`，均返回HTTP 403。未取得原始CSV字节，字段、参与者身份、独立网络/场次、轮次和原始记录数量均未逐行核验；许可须以数据归档具体版本确认。R073冻结双人100轮协议兼容性未知且方格多人互动结构存在差异，正式评分资格NO。复现准备状态SOURCE_METADATA_VERIFIED_RAW_BLOCKED。

## 候选二：ICPSR 37070真实学校社会网络干预研究，隐私与许可阻塞
公开的第三方英文GitHub仓库 https://github.com/jnieser/ExperimentsUnderInterference ，当前公开树包含`ICPSR_37070/DS0001/37070-0001-Data.rda`（5,037,279字节）、研究说明、清单及使用条款。清单Git blob `68f8db2f4ea2055acf05f7be164ec44efaa54304` 标注24,471行、499变量，RDA MD5 `73f1491734f683a52dc955a3f5016c83`，原ICPSR版本2020年9月14日。研究为2012至2013年新泽西州56所学校的社会网络反冲突干预，具有群组和前后调查结构。清单、研究描述与使用条款已实际读取。条款Git blob `3064db916b65ea2aea563377267c1bbe78d1373d` 明确禁止未经许可再分发及识别研究对象，且数据涉及未成年学生与敏感个体信息。本轮主动不读取、不下载、不复制个人级RDA，不进行身份或网络重识别。授权和隐私条件未满足，E2资格NO，状态METADATA_ONLY_PRIVACY_LICENSE_BLOCKED。

两个候选均未产生新真人预测分数。网络干扰R222 S18仅使用原人工E1来源；R073/PESEN v0.1保持冻结。下一轮优先寻找可公开合法读取的匿名化、完整逐轮双人实验数据及明确许可。
