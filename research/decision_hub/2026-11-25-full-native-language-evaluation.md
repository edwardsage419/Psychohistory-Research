# 第59轮：完整原生语言解释基线与本地模型训练准入
2026-11-25。固定main 6af88b73741515196d60589106590900c9dc58c1，PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。已核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一产品交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第24/25/55/56/57/58轮。第25轮评价器 runner.js fe63501cf3d54ddf1d70c137d37e476ece633d75，core.js 6f131ea9a879e2d95615760279b2e295a5db512d，settings.json 05f15044cb4d848e4132dcaaabdb7d6e051d8872。此前A臂只运行_options片段，B/C/D真实Ollama尚未验证。本轮不重复模拟模型，实际运行完整interpret入口。训练相关提交关键词查询（training/fine-tun/LoRA/Ollama）未找到可直接核验的当前本地适配模型训练数据与实际权重收据，不能由搜索无结果推断仓库或用户设备绝无这些资产；真实训练集与评价集隔离仍UNKNOWN。
## 源码与环境
固定PR完整decision_language.py，从连接器返回文本和第55/57轮保留的片段恢复全部587行，实际原始文件32353字节，Git blob SHA1 fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4 与固定PR一致；SHA256 1da2786ab038ed750d436cb197e6d5fd549457df6c6ab30a2351666bb3272290。直接导入完整模块，未改函数。Python3.13.5，超出应用支持范围，但该模块只需标准库。完整仓库git ls-remote仍DNS失败；当前容器无ollama命令，127.0.0.1:11434/api/version连接拒绝，Node22.16.0。不能访问用户Mac，未运行实际Qwen、已适配模型或训练。未运行完整平台账本、确认、数学引擎、API、UI、iPhone或独立验收。
## 公开开发语料实际测量
第24轮固定corpus.json blob 05c239f3f3b1f46235fa2464d2945c21c6c08132，14情节28轮69条标注。连接器提取每轮文本、本人当前新增未来提议行动严格字符串及所有constraint原文标注；本地转录的28轮三元数组与连接器JSON.stringify的FNV1a UTF16一致4acba819（非密码学完整语料字节验证）。每轮独立执行interpret(text)，无前文、focus或已知选项；是无上下文冷启动基线，非第25轮teacher-forced真实多轮测试。严格当前本人行动分数仅与指定目标比较，joint/other行动出现可计该窄指标额外项，不判定其语义必然错误。约束原文锚点是否出现在claim.source及是否进入硬字段是覆盖代理，不能当作完整语义判定；十项中包括权限/条件撤回/风险偏好等开放义务，不都是标量硬阈值。
实测：28轮全部完成；本人行动目标15个，TP6/FP6/FN9，严格行动集合匹配20/28（含无目标轮），10条约束标注中1条出现在某claim.source、0条进入已知硬约束字段；25轮无claims，20轮无claims且无options，全部只生成3条claims。S07.2“我只想先看现金流，不要把风险偏好设成激进。”产生preference=设成激进，原文否定作用域未由字段保留，候选待确认并非已采纳偏好。S07.1把两个指标提为选项，S05.1含第三方候选，S10.2把目标表达截短为“做到的目标”。无完整语义角色评分；没有把69条标注全作原生相同schema比较。实际result.json SHA256 31d416e7cbbaa871ff7999707dbe0cbbd1a5f9c1ede2f05f3d0e4ecc24c3d119。本地文件未直接上传，固定源码及下列复算方式可重生主要计数。
## 历史专项完整解释重放
实际使用此前本机R55/56/57逐条结果文件中的输入。R55 96条，测量子句补“方案A：”明确主体（72币种中模板索引1/2，24周期中偶数索引），R56 140原始句，R57 168条已保存行（额外6个控制不在rows内，未重放）；统一known_options=["方案A","方案B"]。共404条。新完整解释路径实测：R55 72条仍产生yuan/yuan/month金额字段；R56 25正确、71无硬字段、44反向；R57 120/144第三方对应字段无主体，6/6方案叙事对应字段无主体，18/18自述对应字段出现。完整解释复现此前已知缺陷的范围，不计为新独立样本。R55显式主体是人工补充，不是原句自然会话可达性保证；R56仍以静态BOUNDS/strict映射比较，没有执行实际数学筛查；R57不把第三方约束一律判无关。实际regression.json SHA256 2fe9975c9c73597456b8fd146dfd1a1c6478ee5221c377ff288087fdbf18fdec。28+404=432次完整interpret实际调用（无异常），非432真实或独立用户样本。
## 复算主要计数
从固定PR工作树取完整decision_language.py，从固定main取第24轮corpus.json。以下脚本根据原始语料自动投影，生成相同主要统计；历史模板按第55/56/57轮报告的固定生成规则重建（本地本轮实际使用旧rows）。下方整理版未另行执行，不冒充逐字同一实际脚本或远端CI。
```python
import sys,json,hashlib,collections,importlib.util
from pathlib import Path
src,corpus=map(Path,sys.argv[1:3])
def read(p,h):
 b=p.read_bytes()
 if hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()!=h:raise RuntimeError('source identity')
 return b
read(src,'fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4')
c=json.loads(read(corpus,'05c239f3f3b1f46235fa2464d2945c21c6c08132'))
sp=importlib.util.spec_from_file_location('native',src);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
s=collections.Counter();H={'cost_max','income_min','onsite_max','hours_max','move_allowed','move_if_onsite_max'}
for ep in c['cases']:
 for t in ep['turns']:
  gold=[x['quote'] for x in t['proposal']['claims'] if x['role']=='action' and x['op']=='add' and x['actor']=='self' and x['modality']=='proposed' and x['time']=='future']
  limits=[x['quote'] for x in t['proposal']['claims'] if x['role']=='constraint']
  o=m.interpret(t['text']);op=o['options'];claims=o['claims'];tp=sum((collections.Counter(gold)&collections.Counter(op)).values());fp=len(op)-tp;fn=len(gold)-tp
  s.update(dict(turns=1,actionTP=tp,actionFP=fp,actionFN=fn,actionExact=int(not fp and not fn),goldConstraints=len(limits),anyClaimAnchor=sum(any(q in x['source'] for x in claims) for q in limits),hardFieldAnchor=sum(any(q in x['source'] and x['field'] in H for x in claims) for q in limits),emptyClaims=int(not claims),emptyBoth=int(not claims and not op),candidateClaims=len(claims)))
print(dict(s))
r=collections.Counter()
def interp(text):return m.interpret(text,known_options=['方案A','方案B'])['claims']
def amount(text):
 r['r55_cases']+=1;r['r55_mislabeled']+=any(q['unit'] in ['yuan','yuan/month'] and q['field'] in ['cost','cost_max','income','income_min'] for q in interp(text))
for cur in ['韩元','韩币','KRW','₩','卢比','INR','泰铢','THB','瑞士法郎','CHF','越南盾','VND','美元','USD','日元','JPY','欧元','EUR']:
 for fmt in ['预算最多3000{}','方案A：费用2000{}','方案A：每月工资3000{}','每月预算最多3000{}']:amount(fmt.format(cur))
for p in ['每天','每日','按天','每小时','按小时','每周','每星期','每年','每季','每季度','按年','按季']:
 for fmt in ['方案A：{}费用200元','{}预算最多3000元']:amount(fmt.format(p))
for metric,n,suffix in [('预算',3000,'元'),('每周工时',40,'小时'),('每周到岗',3,'天'),('每月工资',3000,'元')]:
 for neg in ['不','不能','不得','不可','不可以']:
  for rel,expected in [('少于','>='),('低于','>='),('小于','>='),('多于','<='),('高于','<='),('大于','<='),('超过','<=')]:
   claims=interp(f'{metric}{neg}{rel}{n}{suffix}');ops=[('>' if q['field']=='income_min' else '<')+('=' if q['kind']=='constraint' else '') for q in claims if q['kind'] in ['constraint','strict_constraint'] and q['field'] in ['cost_max','hours_max','onsite_max','income_min'] and not q['subject']]
   r['r56_cases']+=1;r['r56_'+('missing' if not ops else 'correct' if ops==[expected] else 'reverse' if len(ops)==1 and ops[0][0]!=expected[0] else 'other')]+=1
body=['预算最多3000元','每周工时最多40小时','不能搬家','目标是提高收入','更看重稳定','最晚12月1日答复'];fields=['cost_max','hours_max','move_allowed','goal','preference','deadline']
def personal(text,field,k):
 r['r57_cases']+=1;r[k]+=any(q['field']==field and not q['subject'] for q in interp(text))
for p in ['朋友','同事','配偶','父母','老板','客户','我朋友','我同事']:
 for link in ['说','的','：']:
  for t,f in zip(body,fields):personal(p+link+t,f,'r57_third_personal')
for p in ['方案A','方案B']:
 for t,f in zip(body[3:],fields[3:]):personal(p+'：'+t,f,'r57_option_personal')
for p in ['我','我本人','我的']:
 for t,f in zip(body,fields):personal(p+t,f,'r57_self_personal')
print(dict(r))
```
## 训练决策与下一完整任务验收
状态：RULE_BASELINE_EXECUTED / FULL_LANGUAGE_MODULE_HASH_MATCH / REAL_LOCAL_MODEL_BLOCKED / TRAINING_DATA_LINEAGE_UNKNOWN / NO_NEW_TRAINING_AUTHORIZATION. 现有规则是窄领域确定性补助，已知缺口真实可复现；尚无证据判断微调一定改善开放语义。优先复用R25运行器，在用户已有Mac环境同一模型digest分别执行原始回复、结构化候选、结构化加可信语义义务层；另比较既有适配模型（若存在且身份可证）。先测实际错误及下游损害，再选择提示、检索、结构化约束、宿主校验或训练；不得以现有公开开发集充当独立留出。训练前逐条记录来源许可、合成/人工/真实类型、生成模型与版本、情节家族、训练/开发/未见组、去重和近义跨组审查、训练和评价模型身份、权重摘要及可回退基线。现有公开14情节及R55-57模板作为开发回归，禁止再作为未见效果证据；不得使用个人决策数据或未授权私人记录。实际独立轨另立留出，由其冻结并核查跨情节泄漏；不能声称已经完成。R25评分结构有效不等于事实或角色正确，C/D同一响应；真实Qwen测量同时报告拒答、错提取、漏义务、错误确认、错误推荐、追问负担和运行时间（按情节及交错顺序），不以单项词面分数决定训练或上线。权限必须真实宿主核对。保留B02/B03/B05/B06/B07/B08/B09/B11完整版本关联与第34/50轮12项范围；不拆分新Codex任务。未修改生产、训练、CI、工作流、合并、部署或冻结协议，零新增费用。
