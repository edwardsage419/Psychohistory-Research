# 自主认知：原生数量角色、周期关系类型与共享范围保留
2026-11-27。RESEARCH_CANDIDATE / FIXED_NATIVE_FRAGMENTS_EXECUTED / CONTROLLED_LANGUAGE_DIAGNOSTIC / PUBLIC_SYNTHETIC_DEVELOPMENT_REPLAY / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN / NO_TRAINING。

## 基线、资产及去重
起点main 72844dbc3f304c7e05954b5fbdb183535fd7df51。核对20近期提交、15开放PR、v3.2和同步规程全文、唯一产品交接前20行、PR #63固定head 734686980b19da9291bdd08b67d4e2519c011acf，仍Draft，未合并。前序原生周期发生位置审计 blob c56f3c17aa634d21ce5efddd035884b71ac50d82、时间词法分离 8a6b42f83b80283db6e215fe48f4fb2efbf8368c、数量单位周期证据 c89fbaede02776da34e6861328fa1933a855fb4c、类型数量原子 ada3d84a46e4d9a411ebf762884d13a5c5e87686、有限模态桥 093b787d4603a088d9bce9f83900a031d39d6365 各读前18行。已有时间词法候选、独立证据资格、周期发生位置及数学约束接口不重复计；新增是在原生数量输出和旧周期边上区分指代集合基数、事件计数、显式分母、观察/计划窗口及未决语境关系。局部查重，非全库证明。
实际恢复聊天附件 native_quantity_scope_20261127.zip，SHA256 ccc7512d9e4c8b7bdc645b0a819bc290c9e0d5c684a318ea4957c4e200e7374e，与前序一致。核对 native.py fdfce2eb8fe5528d792efcdb035f7aa131f215b187446c9be8912a27b0959a35、study.py d0b886ac44a2779a31ca057a93e34c497ae8cc05f9d13cc1552f884995bd345b、corpus.tsv 1b60c57c1b0bd823acf82e1ba21e3773605af1114696fe0e0779005728852861。实际调用原生_lexical_candidates、_parts及前序proposals/native/qend；后3函数经AST只提取已核对的函数定义，未执行旧主实验，避免重复计数。原生源码身份、13段转录检查范围及固定语料blob沿前序报告；本轮只复核所恢复文件SHA256，不声称重新取得完整Git原始源码字节或重跑13项FNV。Python 3.13.5标准库容器，非项目锁定Python3.12环境。固定公开合成语料仍为32情节64轮：language_corpus.json be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb 和 semantic-proposal-contract/corpus.json 05c239f3f3b1f46235fa2464d2945c21c6c08132 的前序已校验原文转录，不是独立留出/真人/训练。

## 研究问题与方法
原生数值及单位只表明词面量，不能单由count、hour或同句周期推导资源量或重复率。“比较每月还款额和应急储蓄这两个指标”中“两”指代指标集合，而“每月完成3次任务”的count可与频率相关。相同单位不同角色不能机械统一；“每月评估这两个指标”还可对固定成员集合执行重复评估，故不能通过基数角色推断评估事件不重复；“一周完成3次任务”可能是一次观察/计划窗口或惯常频率。
在原生数量的准确发生位置及前序边排序上：
1. 用相邻指示词这/那、count分类及有限显式名词头构造REFERENTIAL_CARDINALITY_CANDIDATE，保留从指示词到头的精确原文锚。次分类器形成EVENT_COUNT_CANDIDATE，其他count保留ENTITY_OR_EVENT_COUNT_UNKNOWN；其余暂作MEASUREMENT_CANDIDATE。此是受控词面角色候选，不是经过语义确认的维度或身份。
2. 每个数量与原有周期锚的关系分别标记：紧邻斜线后缀EXPLICIT_DENOMINATOR_CANDIDATE；周内/一周内等OBSERVATION_OR_PLAN_WINDOW_CANDIDATE；一周但无明确窗口尾词WINDOW_OR_RATE_AMBIGUOUS；指代集合GROUP_CONTEXT_CANDIDATE；事件计数EVENT_RATE_OR_WINDOW_CANDIDATE；其余RATE_OR_CONTEXT_CANDIDATE。
3. 所有原始边按前序顺序保留，显示前2并明确all_count/truncated；unknown_retained=True，authority NONE。未删除边，未建立完整互斥的语义类型域、可信证据或实际计算准入。所谓GROUP_CONTEXT只是可用的结构提示，不能直接证明周期修饰对象或否定其他解释；显式分母仍需确认单位、事件、时间身份、量值和来源。没有把观察时窗直接换算成每周/月频率，亦不自动把固定群体基数乘周期次数。真正过滤、确认或分配不同关系需独立语义资格。名词头仅9项、窗口词有限，不能靠无限扩充词表证明通用能力。
4. 复用原生192候选上限，原有截断状态仍未修复；边计数仅覆盖返回的数量及旧分句匹配，不是全原文覆盖。研究函数暂用大limit取局部全部边，非生产内存/时间防护。

## 实际执行
研究者设计的受控合成模板、标签、有限头词及参照。同一研究者设计解析候选和预期类型，测的是受控合同及源码连接，并非独立语义准确率。每例目标数量实际来自原生_lexical_candidates，检查候选角色、前2关系内预期类型、角色及关系原文坐标、未知保留和authority NONE。普通Python及-O各实际执行一次，输出逐字节相同。
| 族 | 数量 | 原生附周期 | 预期角色/关系匹配 | 未知保留 |
| --- | ---: | ---: | ---: | ---: |
| 指代集合 | 120 | 120 | 120 | 120 |
| 不确定对象/事件数量 | 120 | 120 | 120 | 120 |
| 事件计数 | 45 | 45 | 45 | 45 |
| 明确窗口 | 36 | 36 | 36 | 36 |
| 窗口或频率歧义 | 27 | 27 | 27 | 27 |
| 显式分母 | 30 | 30 | 30 | 30 |
| 合计 | 378 | 378 | 378 | 378 |
生成：5周期×6名词头×2指示词×2数量=120（前两族分别）；5周期×3动词×3数量=45；4明确窗口×3动词×3数量=36；3含糊窗口×3动词×3数量=27；5分母×3单位×2数量=30。部分族存在重复文本（不确定对象/事件数量不使用指示词，重复60次；因此总378配置不等于378个独立句子）。另16个手工边界诊断，检查所有返回数量的未知/权限状态并留存实际候选，不声称16项完整语义真值通过。若简单丢弃所有count周期边，仅不确定对象计数、事件计数及明确窗口三族即删除201处研究目标关系（其中包含重复配置及未决关系）；这不是实际错误率或全部损失统计，不代表所有201项都必须作为频率。显式分母含次/月等反例，也不能按count一律删除。所有类型判断只用于候选，没有原生计算、数据写入或推荐权限。

## 64轮实际语料回放
原生词法数量61，与前序相同；候选角色：MEASUREMENT_CANDIDATE 40、ENTITY_OR_EVENT_COUNT_UNKNOWN 15、EVENT_COUNT_CANDIDATE 5、REFERENTIAL_CARDINALITY_CANDIDATE 1。输出的周期边4个（未增加覆盖）：3个RATE_OR_CONTEXT_CANDIDATE、1个GROUP_CONTEXT_CANDIDATE。分别来自L01.0、L01.1、S10.0及S07.0。S07.0“比较每月还款额和应急储蓄这两个指标”的“两”现获得指代集合候选，原边重标GROUP_CONTEXT，仍保留未知与原始原文；不能声称正确完整解析“每月”修饰还款额、已消除原生错误或已确认集合成员。L01与S10的周期仍未确认；“两项”可能无原生count候选，日期与量词缺失未修复。无全面金标，不能报告真实精度/召回。16个控制包含共享周期、引述、无分隔双数量、窗口、分母、指标组及含糊对象计数；仍有真实语言中未识别的词面及关系，原型没有解决开放语义的能力瓶颈。

## 可复算核心
以下为本次实际role_study.py中的核心。n、qend、proposals来自固定资产，完整源码及结果随本轮聊天ZIP。
```python
HEADS=('指标','方案','选项','项目','岗位','目标','人','房子','设备')
WINDOW_ENDS=('内','里','期间','之内','时间内')
def anchor(raw,a,b):
    return n.source_anchor(raw[a:b],a,hashlib.sha256(raw.encode()).hexdigest())
def role(raw,q):
    a=q['span']['start']; b=qend(q); u=q['unit']; classifier=q.get('unit_source')
    d=next((x for x in ('这','那') if raw[:a].endswith(x)),None)
    head=next((x for x in HEADS if raw[b:].startswith(x)),None)
    if u=='count' and d and head:
        return {'label':'REFERENTIAL_CARDINALITY_CANDIDATE','anchor':anchor(raw,a-len(d),b+len(head)),'head':head}
    if u=='count' and classifier=='次':
        return {'label':'EVENT_COUNT_CANDIDATE','anchor':anchor(raw,a,b)}
    if u=='count':
        return {'label':'ENTITY_OR_EVENT_COUNT_UNKNOWN','anchor':anchor(raw,a,b)}
    return {'label':'MEASUREMENT_CANDIDATE','anchor':anchor(raw,a,b)}
def relation(raw,q,edge,r):
    a,b=edge['anchor']['span']['start'],edge['anchor']['span']['end']; token=raw[a:b]
    direct=token.startswith(('/','／')) and a>=qend(q) and not raw[qend(q):a].strip()
    window=(token=='一周' or token.startswith(('一星期','一礼拜')) or token=='周内')
    explicit_window=window and (token.endswith('内') or raw[b:].startswith(WINDOW_ENDS))
    if direct: kind='EXPLICIT_DENOMINATOR_CANDIDATE'
    elif explicit_window: kind='OBSERVATION_OR_PLAN_WINDOW_CANDIDATE'
    elif window: kind='WINDOW_OR_RATE_AMBIGUOUS'
    elif r['label']=='REFERENTIAL_CARDINALITY_CANDIDATE': kind='GROUP_CONTEXT_CANDIDATE'
    elif r['label']=='EVENT_COUNT_CANDIDATE': kind='EVENT_RATE_OR_WINDOW_CANDIDATE'
    else: kind='RATE_OR_CONTEXT_CANDIDATE'
    return {**edge,'relation':kind,'authority':'NONE','unknown_retained':True}
def typed(raw,qs,limit=2):
    old=proposals(raw,qs,limit=10**6); rows=[]
    for q,p in zip((x for x in qs if x['kind']=='quantity'),old):
        r=role(raw,q); edges=[relation(raw,q,e,r) for e in p['candidates']]
        rows.append({'quantity':q['span'],'role':r,'relations':edges[:limit],'all_count':len(edges),'truncated':len(edges)>limit,'unknown_retained':True,'authority':'NONE'})
    return rows
```
本地附件 quantity_role_research_20261127.zip SHA256 4006bdf05dccb19f9a3c917b072b52142df3bf13e928b6a213bcec7238b7775c，unzip -t通过。新文件：
role_study.py 1d78e5bb47799a27d9cd8498cc823174a152553ca9653ff799a01f57df8156e3
role_result.json及role_result_opt.json 1c2d3662b0748659ffa002a9f182029f1d54c8a58778f02860865c5ccf1bfc62。
复算 python role_study.py > role_result.json；python -O role_study.py > role_result_opt.json；cmp role_result.json role_result_opt.json。ZIP含旧native.py、study.py、corpus.tsv及新文件，未上传ZIP字节至仓库，本报告含核心及摘要。

## 下一责任与治理
后续高价值缺口：从开放原文中独立发现名词/事件谓词及角色，建立数量锚与谓词的联合候选，保留共享周期与不同时间口径；在真实原生入口测未处理原文及截断覆盖。由模型与手动研究形成接口和算法，授权后工程轨接入，独立轨另行验证。研究者自行选择词表、规则、分支标签及试验结构；未变更产品规范。未运行完整v0.8、实际来源确认、真实用户、独立留出、竞品、真机、训练、生产修改、PR合并、部署、主动CI或费用。冻结、历史证据与唯一交接不变。
