# 第57轮：原生声明的主体归属与第三方义务隔离
2026-11-25。固定main 58a564c2893f4cf4b175bd75252d6c55f274e711，PR #61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e open Draft。核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一交接blob 5e74f4f0b37141d631740e844ad8bbbfed232e07、第23/24/35/55/56轮。第23轮（README blob 8b184edb783c69a59d2e9867c007b184afc16961）已证明选项提取存在第三方角色混淆及泛化失败；本轮不重计选项发现，实际执行声明提取中的_subject/_numeric_claims/_move_claim/_narrative，聚焦已知选项和第三方声明的归属丢失，新增有限测试与归属待核对原型。
## 源码与范围
decision_language.py blob fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4。复用第55轮本机源段并重验其5段FNV；新增5段：lines30-36 1ac4ba61、79-106 aab34ade、193-196 b793496d、269-301 296d72e6、404-449 554edfeb；连接器固定文本与本机实际执行段的FNV1a UTF16去尾空白全部匹配。FNV仅文本比对，不是完整文件Git字节哈希。原生函数体未修改，Python3.13.5超出正式支持范围。已知选项A/B由夹具提供，单子句路径调用原生函数，context/focus为空，不执行完整interpret、_options、跨句主体继承、ledger、confirm、build_state、hub、API、Qwen、浏览器或设备。另读decision_conversation_math.py aca1b4aa5cf4b4fd5b476e078b6e2aa9af197d30 sourced_key/build_state的field:subject及goal投影，decision_conversation.py f505aeab2d9e5e0a9c8957ce6e039dea174918a7 active_claims/blocking_constraints；仅静态追踪后续接口。
## 问题
A57-01：未知主体的普通前缀例如“朋友说预算最多3000元”“我同事的预算最多3000元”可能仍由_subject返回空主体，_numeric_claims把金额提为个人硬约束。_move_claim依据空主体选择个人搬家许可，第三方说法可能进入move_allowed。冒号标签可能被识别为非空主体，故不同句式行为不同；24条未生成同字段个人声明不能算正确理解。A57-02：_narrative并不接受subject参数，始终以空主体生成goal/preference/deadline。原生“方案A：目标是提高收入”“方案B：更看重稳定”“老板说最晚12月1日答复”各产生无主体叙事字段。第三方外部截止可能确实约束当前行动；错误在于归属、适用范围与采纳资格未表达，不能简单断言所有第三方条件无关。未验证用户最终确认或真实错误建议，不声称已复现生产绕过。
## 候选合同
分别记录说话人、被描述主体、决策所有者、作用对象、角色（个人底线、偏好、外部可行性条件、方案属性、转述、代理决策、假设）、时间/条件/来源及用户是否明确采纳。原文有“我”也可能在第三方名词内。亲友的偏好不得自动成为本人权重；雇主要求若经核实适用于行动，则作为外部可行性义务，而非本人偏好；替别人决策须明确决策所有者，不能套本人画像。用户可在确认后采纳相同底线，保留采纳身份和原始来源。第三方含隐私的记录默认不跨会话，授权独立。候选对有限前缀模板返回VERIFY_THIRD_PARTY_SCOPE或VERIFY_OPTION_NARRATIVE_SCOPE，保留原文、说话人线索及未解决义务，待确认前不生成个人字段。speaker仅前缀标记，不代表已正确识别真实说话人。明确自述模板原样保留原生待确认候选，模板外UNPARSED_SCOPE保留义务。不能作为通用生产拦截器；不能靠扩大词表解决开放语义。以当前相关义务控制完整建议，其他不依赖此义务的局部分析可保留。
## 实际结果
8类第三方前缀×3连接式×6字段=144条（人工构造目标是转述/归属未核对，非真人）。120条生成对应字段且subject为空，含48条硬约束、72条目标/偏好/截止叙事；24条无对应空主体字段，不计正确率。2已知选项×3叙事字段=6条，均生成空主体叙事。候选150/150保留归属待核对，无个人声明；18条明确自述控制18/18原生候选不变；6条复杂/未支持语句保留UNPARSED_SCOPE。合计174条测试（168条具逐条记录，6条额外控制）；所有计数是同研究者设计公开模板上的源片段行为，不是独立留出或总体准确率。未进行任何实际数学筛查或产品端到端运行，不声称150条已实现正确语义理解。实际本机probe.py SHA256 a07850e90340249ca833a39b49d9a121705b815d72e611982779ac206bbec22c；results.json SHA256 9916a164d45ab1371cea8295774f81103d0c55e35e23105c890d690656b00781；新增fragments.txt SHA256 aac855024d0e8f3b826d9bb7c106f0c0881aa95ab7910a9ed7e9171f50857730。下方为等价复跑器，固定完整源码路径运行尚未执行；本机实际使用上述逐字复制片段。
## 复跑器
从固定PR工作树运行 python probe.py /path/to/repo/platform/future_model/src/psychohistory。完整语言模块仅标准库；下方按固定源字节及片段校验，按原序执行必要片段，避免引入未测完整路径。
```python
import re,sys,json,hashlib,unicodedata
from decimal import Decimal
from collections.abc import Iterable
from pathlib import Path
b=(Path(sys.argv[1])/'decision_language.py').read_bytes()
if hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()!='fff9d6c8e20c6a57c4ae9756bf5d6fe0e81f61b4':raise RuntimeError('source identity')
def fnv(s):
 h=2166136261;b=s.encode('utf-16-le')
 for i in range(0,len(b),2):h=((h^(b[i]+256*b[i+1]))*16777619)&0xffffffff
 return f'{h:08x}'
ls=b.decode('utf-8').splitlines()
for a,z,h in [(30,36,'1ac4ba61'),(38,78,'e7d32c19'),(79,106,'aab34ade'),(108,178,'c3cb5d3f'),(193,196,'b793496d'),(269,301,'296d72e6'),(302,313,'ee37bc70'),(321,403,'58a938a5'),(404,449,'554edfeb')]:
 s='\n'.join(ls[a-1:z]).rstrip()
 if fnv(s)!=h:raise RuntimeError('fragment identity')
 exec(compile(s,'fragment','exec'),globals())
PARTIES=['朋友','同事','配偶','父母','老板','客户','我朋友','我同事']
PAYLOADS=['预算最多3000元','每周工时最多40小时','不能搬家','目标是提高收入','更看重稳定','最晚12月1日答复']
FIELDS=['cost_max','hours_max','move_allowed','goal','preference','deadline']
OPTIONS=['方案A','方案B']
NARRATIVE=PAYLOADS[3:]
ALIASES=_option_aliases(OPTIONS)
def old(s):
 sub,content=_subject(s,ALIASES)
 out=_numeric_claims(content,sub,s,'','')
 m=_move_claim(content,sub,s,'')
 if m:out.append(m)
 out.extend(_narrative(content,s,''))
 return out
def candidate(s):
 for p in sorted(PARTIES,key=len,reverse=True):
  for link in ['说','的','：']:
   prefix=p+link
   if s.startswith(prefix) and s[len(prefix):] in PAYLOADS:
    return {'state':'VERIFY_THIRD_PARTY_SCOPE','speaker':p,'source':s,'claims':[],'obligation':True}
 for o in OPTIONS:
  if s.startswith(o+'：') and s[len(o)+1:] in NARRATIVE:
   return {'state':'VERIFY_OPTION_NARRATIVE_SCOPE','speaker':o,'source':s,'claims':[],'obligation':True}
 for p in ['我','我本人','我的']:
  if s.startswith(p) and s[len(p):] in PAYLOADS:
   return {'state':'PROVISIONAL_SELF','speaker':'SELF','source':s,'claims':old(s),'obligation':True}
 return {'state':'UNPARSED_SCOPE','source':s,'claims':[],'obligation':True}
rows=[];stats={k:0 for k in ['third_cases','third_personal_claims','third_personal_hard','third_personal_narrative','third_no_personal_claim','option_cases','option_personal_narrative','self_cases','self_preserved','candidate_scoped','unknown_controls']}
for p in PARTIES:
 for link in ['说','的','：']:
  for body,field in zip(PAYLOADS,FIELDS):
   s=p+link+body;o=old(s);n=candidate(s)
   own=[c for c in o if c['subject']=='' and c['field']==field]
   stats['third_cases']+=1;stats['third_personal_claims']+=bool(own);stats['third_no_personal_claim']+=not bool(own)
   stats['third_personal_hard']+=bool(own) and field in FIELDS[:3];stats['third_personal_narrative']+=bool(own) and field in FIELDS[3:]
   assert n['state']=='VERIFY_THIRD_PARTY_SCOPE' and n['speaker']==p and n['obligation'] and not n['claims'];stats['candidate_scoped']+=1
   rows.append([s,o,n])
for op in OPTIONS:
 for body,field in zip(NARRATIVE,FIELDS[3:]):
  s=op+'：'+body;o=old(s);n=candidate(s);stats['option_cases']+=1;stats['option_personal_narrative']+=any(c['subject']=='' and c['field']==field for c in o)
  assert n['state']=='VERIFY_OPTION_NARRATIVE_SCOPE' and n['obligation'] and not n['claims'];stats['candidate_scoped']+=1;rows.append([s,o,n])
for p in ['我','我本人','我的']:
 for body,field in zip(PAYLOADS,FIELDS):
  s=p+body;o=old(s);n=candidate(s);stats['self_cases']+=1;assert n['state']=='PROVISIONAL_SELF' and n['claims']==o and any(c['subject']=='' and c['field']==field for c in o);stats['self_preserved']+=1;rows.append([s,o,n])
for s in ['我朋友说我不能搬家','我和配偶共同决定预算最多3000元','他说她更看重稳定','如果老板要求我搬家','我朋友说预算最多3000韩元','我目标是提高收入但不能搬家']:
 n=candidate(s);assert n['state']=='UNPARSED_SCOPE' and n['obligation'] and not n['claims'];stats['unknown_controls']+=1
print(json.dumps(stats,ensure_ascii=False))
Path('results_r57.json').write_text(json.dumps({'stats':stats,'rows':rows},ensure_ascii=False,indent=2))
```
实际输出：{"third_cases":144,"third_personal_claims":120,"third_personal_hard":48,"third_personal_narrative":72,"third_no_personal_claim":24,"option_cases":6,"option_personal_narrative":6,"self_cases":18,"self_preserved":18,"candidate_scoped":150,"unknown_controls":6}。
## 接入及后续
B02/B05/B06/B07/B08/B09/B11候选增量。与第55/56轮合并为声明级输入质量与未解决义务统一协议，避免继续以每类正则孤立修补。下一阶段优先验证完整interpret与多轮确认中的主体更正、外部约束采纳、个人偏好与方案属性区分、条件及原文覆盖；真实语言模型须使用冻结未见情节测试，不把公开模板当训练成效。原生语义模块可在当前Python执行，但完整平台、真实Qwen及独立验收仍未完成。未修改生产源码、启动Codex、CI、训练、合并、部署、冻结协议或新增费用。保留完整12项版本范围。
