# 自主认知：v0.8原生数量周期发生位置绑定、候选排序及截断诊断
2026-11-27。RESEARCH_CANDIDATE / FIXED_NATIVE_FRAGMENTS_EXECUTED / PUBLIC_SYNTHETIC_DEVELOPMENT_REPLAY / NO_TRAINING / FULL_NATIVE_NOT_RUN / INDEPENDENT_NOT_RUN。

## 基线、去重和运行环境
起点及写前main 903aad6cd6ae053a0d01beaf6b1668eaa5f54fe2。核对20近期提交、15开放PR、v3.2及同步规程全文、唯一交接前20行、decision_hub相关目录。#63 head 734686980b19da9291bdd08b67d4e2519c011acf仍Draft、未合并。实际读取PUBLIC_DEVELOPMENT.md blob 8557baeceba18a1630b769ac027889f14de16a45，其历史原生报告词法数值25/28、数值单位7/23、条件0/5、修订链0/10；本轮不追认重跑这些指标。读此前口语数词f6684299a3720a533e44343b123edff085c7ee05、开放跨度175f8b48a4cc46cb3b41b7b65b13b06448bf461a、币种周期d7eedbca02da7f66f06911fffedc8f8b82be3f90、否定方向2c7810d1cad4986b9ecabdf727adab5600ed6fca、引述原生审计8fb6c4a7b4ad9d8251ea3137a998730a2e21f5e4、修订链cfb296cff72e8cbb140744ca6e77d5e12d6e1100及实际容器再执行604c6b237ea4ca0d56447f771786c3e572e51e82前段。新增重点为多个已识别数量与同句多个周期发生位置的精确关联及192候选截断；不重复旧币种、数词或一般跨度搜索，不作全库查重证明。
容器实际git ls-remote DNS失败，不能完整克隆或运行原生应用。连接器可读固定源码及写原创研究报告。Python 3.13.5标准库运行转录片段，非完整项目锁定Python3.12环境。原生以下片段未修改函数体；仅抽取必要标准库及依赖常量。FNV1a32按Unicode标量、去尾空白校对转录，不是完整原文件密码学证明。首次校验因将7位十六进制指纹与8位格式比较而停止，修正补零后全部13项匹配；该次未计入运行结果。

固定PR源码 platform/future_model/src/psychohistory/decision_language.py blob c01217b6d6f4c2465ffc0959f3c0219e9638e052：
| 原文行（1-based inclusive） | 片段 | FNV |
| --- | --- | --- |
|36..38|句界引号及自述恢复|8c67932d|
|42|标签角色|f66d4f67|
|48..55|数词词元|0817f432|
|71|周周期|8c7f1cb2|
|105..113|日期|bddaa959|
|135..196|数字映射及_number、_numeric_integer|cf9496bf|
|197..228|_parts|e3c0f262|
|587..603|词法日期、数值、单位及周期|dfe1e4eb|
|734..736|_span|9c7f0e60|
|747..809|_lexical_candidates|129b115d|

decision_semantics.py blob 8c6ea6914b5b6e4f01d70331ed5c75c0dc32221b：
16..22 CNY/NON_CNY e65a5b51；29 MONTH 55375800；112..116 source_anchor 66fc37c8。
静态读interpret输出中的候选切片、outside True、coverage BOUNDED_RULES，未执行interpret、真实API、账本、确认、硬门、授权或数学筛查。不能判断完整入口可达性或用户事故。

## 实际发现
原生_lexical_candidates对每个数量查其分句，若该分句仅有一种周期标签，使用该分句首个周期匹配，不按数量或具体发生位置分离；若多种标签共存则period=None。因而“每月工资5000元每年奖金10000元”两个周期均丢失；“房租3000元/月押金6000元”押金也获得month；“每月收入5000元通勤30分钟”30分钟也获得month；“每月工资5000元每月奖金2000元”两者均锚向首个每月。候选authority NONE，不能因此认定硬门或实际计划被错误放行。
另一诊断：固定191、192、193、200个各自独立金额原文发生位置，_lexical_candidates分别返回191、192、192、192项；超过192静默丢尾，列表自身没有截断状态。interpret明确outside True，尚未执行完整入口长度门或后续确认，不声称整个产品无未知防护。未来应单列已搜索数量、截断边界、待处理原文和未知覆盖，不把返回列表当完整域。
12项边界控制的全部原文、候选及锚校验随本轮本地回执。额外观察“亏损负300元”原生候选数值300，负号语义未进入该词法候选；“价格USD 500”候选500无单位，前置币种未绑定。这些只记录片段行为，未扩大为已验证缺陷修复或数值完整性结论。

## 研究候选和实测
复用原生数量及分句/周期匹配，对每数量枚举同分句的全部不与该数量及单位重叠的周期锚。排序按直接相邻的斜线后缀优先，然后前置周期，再其他后缀/后置前缀；各级内按跨越数量数、距离及原文位置。输出最多2个关系候选，另给实际候选计数、是否截断、unknown_retained=True、authority NONE。排名不是概率或资格；并列周期可能共享、词面相同不同发生位置也可能指同一周期，人工生成金标仅为明确局部标记的测试合同，不能据此拒绝共享作用域或自动确认关系。前缀/后缀、标点、同分句、词法输入和候选全域仍有限制；没有资格判断、真正句法树或学习。

五周期（每月/每周/每年/每天/每次及对应/单位后缀）两两组合×3组指标词对（工资奖金、房租停车费、费用维修费）×前后缀两两组合×三种边界（无标点、中文逗号、分号）×两个金额对（5000/2000、3000/3000）=1800组，3600人工明确局部关联目标。目标以生成时精确周期发生位置及标签为参照；并非自然语言独立标注，原生与候选复用同一词表。没有用生成目标辅助排序。相同词面同一标签但不同位置不能算本实验的精确关联成功。无标点组1200目标中原生精确120、改进1200；分隔组2400目标均正确。全量：
| 指标 | 原生 | 候选 |
| --- | ---: | ---: |
|精确周期及原文锚首位匹配|2520/3600|3600/3600|
|仅标签正确|2640/3600|3600/3600|
|无周期|960|不作确定映射|
|同标签但错误发生位置|120|0首位|
|前2位目标保留|不适用|3600/3600|
|未知解释保留|未按此指标比较|3600/3600|

30个第二金额无明确局部周期的专项模板（五周期×三指标对×两位置形式），原生30/30为第二金额附加分句周期；候选30/30保留未知。该批不能视为30个已证实错误归属或真实意图，因为上下文可能共享周期；新方法仍可能提出该周期候选。禁止把这30个当作精确识别未知语义成功。12固定控制核对原生候选/单位/周期锚原文；4种候选上限测试。普通与-O实际完整运行输出逐字节一致。所选模板、评分、评估范围均是研究者选择、已见开发数据；非独立验收，不把受控100%外推。

## 实际公共开发语料片段回放
实际完整读取固定公开合成资产 research/decision_hub/2026-11-24-language-evidence-corpus/language_corpus.json blob be1cddcc80e78e3df9a35775279c4b4f7f3ae1bb 及 research/decision_hub/2026-11-24-semantic-proposal-contract/corpus.json blob 05c239f3f3b1f46235fa2464d2945c21c6c08132。连接器提供blob身份，未重算Git原始字节；逐行id.0/id.1<TAB>原文的TSV去尾空白FNV 9cedb661，容器实际转录校验通过。32情节64轮。原生片段输出61数量候选、12日期候选，其中4个数量有周期标签；研究候选亦仅4个数量有任何周期边。未实现自动发现遗漏的表达如“一年”、四周总时域、当前月份及无明示周期；没有全面周期人工金标，不报告开放语义精度/召回。具体公开开发反例S07.0“比较每月还款额和应急储蓄这两个指标”，数量“两”(count)被关联到month；本轮排序仍提出这条边并保留UNKNOWN，说明排序本身没有解决类型及谓词作用域。接下来需把数量角色（金额、人数、指标数量、持续时间等）、周期类型（重复率、观察窗口、截止时间等）、原文句法及明确绑定的证据共同纳入候选资格，不能把语句中一个周期机械广播。现有两套语料为项目公开ChatGPT辅助合成开发材料，不是独立留出、真实用户或授权训练材料。

## 可执行研究候选核心
以下为本轮实际study.py中的关系生成函数，native为上述固定源码依赖，qend为max(数量span.end, unit_anchor.span.end)，缺单位锚时后项0。
```python
def proposals(raw, qs, limit=2):
    segments=[(c,s+o) for x,s in n._parts(raw,n._SENTENCE_ENDS) for c,o in n._parts(x,',，')]
    result=[]
    for q in qs:
        if q['kind']!='quantity': continue
        p=q['span']['start']; e=qend(q)
        loc,start=next(((c,s) for c,s in segments if s<=p<s+len(c)),('',0))
        edges=[]
        for m in n._PERIODS.finditer(loc):
            a,b=start+m.start(),start+m.end()
            suffix=m[0].startswith(('/', '／'))
            if a<e and b>p: continue
            if suffix:
                direct=a>=e and not raw[e:a].strip()
                if a<e: distance=e-a
                else: distance=a-e
                barrier=sum(e<=z['span']['start']<a for z in qs if z is not q and z['kind']=='quantity') if a>=e else 1
                orient=0 if direct else 2
            else:
                direct=False
                orient=1 if b<=p else 3
                distance=p-b if b<=p else a-e
                barrier=sum(b<=z['span']['start']<p for z in qs if z is not q and z['kind']=='quantity') if b<=p else 1
            score=(orient,barrier,max(0,distance),a)
            edges.append({'label':m.lastgroup,'anchor':{'source':m[0],'span':{'start':a,'end':b}},'score':score})
        edges.sort(key=lambda x:x['score'])
        result.append({'quantity':q['span'],'candidates':edges[:limit],'all_count':len(edges),'truncated':len(edges)>limit,'unknown_retained':True,'authority':'NONE'})
    return result
```
完整本地ZIP native_quantity_scope_20261127.zip（本轮聊天附件，未把ZIP字节上传GitHub，报告与摘要已同步）SHA256 ccc7512d9e4c8b7bdc645b0a819bc290c9e0d5c684a318ea4957c4e200e7374e。实际unzip -t通过。文件SHA256：
native.py fdfce2eb8fe5528d792efcdb035f7aa131f215b187446c9be8912a27b0959a35
study.py d0b886ac44a2779a31ca057a93e34c497ae8cc05f9d13cc1552f884995bd345b
corpus.tsv 1b60c57c1b0bd823acf82e1ba21e3773605af1114696fe0e0779005728852861
result.json/result_opt.json 65d92b121fe431e4475b5bb699083bb70ab345550e9b239e52d1a110a3dd58b7
解包后执行 python study.py > result.json；python -O study.py > result_opt.json；cmp result.json result_opt.json。无第三方包、网络请求或外部AI运行时。

## 治理与边界
未修改生产、训练、合并PR、部署、主动CI或新增费用。未执行完整v0.8、独立留出、真人、Mac/iPhone设备、竞品或权限与数学门；当前研究候选需要实际原生输入输出合同与独立验收后才可考虑产品接入。冻结、历史证据等级和唯一交接不变。
