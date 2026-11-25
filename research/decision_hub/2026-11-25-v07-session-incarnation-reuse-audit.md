# v0.7 会话实例身份复用与迟到请求审计
2026-11-25。SOURCE_SLICE_EXECUTED / SYNTHETIC_FIXTURE / NATIVE_API_NOT_RUN / INDEPENDENT_NOT_RUN。起始main f3708addeea0344826d49ea41dfd7e1ff2a5c44f；Draft #62 固定 e61bbad10932edabc9a87483e5407fdae6c751cc。核对近期12提交、14开放PR（#61/#62仍待审）、v3.2、前轮同步规程与局部输出审计、唯一产品交接前18行 blob 5e74f4f0b37141d631740e844ad8bbbfed232e07。第36轮 a6440d99b24a8b5972de8983959c4364cef4a411 已研究首次关闭与不可复用租约；第107轮 2f0c17a303bde8ef3e9711a08fcbbbaa8d5e78ec 已研究计算代次ABA及发布事务。本轮仅新增v0.7真实生命周期方法的同ID跨实例复用诊断，不宣称新的通用代次算法。全库去重不能保证。

## 源码依据与发现
候选 platform/future_model/src/psychohistory/decision_conversation.py blob ed1c5aa8407f53ef3dfc1484ba1a18ef1edabcad。Conversation初始revision=1；_expire 207–214行移除超时会话及到期关闭记录，_read 216–225行检查ID及revision，_update 227–236行容量淘汰，start 238–260行接受客户端提供的ID，拒绝活动/待处理/关闭记录中的重复ID。turn 301–329行解析在锁外，最后再次以原ID和revision核验，未独立检查实例身份。end 529行起只按ID关闭。decision_conversation_api.py 的StartInput允许客户端ID，SessionInput仅ID/revision，EndInput仅ID。前轮第36轮提出不可复用租约，本候选未完整实现该身份保证。
可达的源码片段路径：旧实例A revision=1，过期/容量淘汰/关闭记录到期，客户端再次start同ID的新实例B revision=1。旧请求的_read返回B；旧end删除B。若旧turn在锁外停留且新实例复用了ID和revision，末次_read也可能通过，旧快照覆盖新实例为待原生验证的推论，未执行该路径。需要同ID重用以及迟到/重放请求；未测真实客户端生成ID方式、认证、中间件、请求延迟或真实事故。不是跨账户攻击或已观察数据泄露。现有不同ID、活跃重复及关闭记录未到期时的保护仍有效。

## 复算
实际Python标准库运行：从连接器固定源码逐字转录上述五个方法，使用人工时钟及虚构最小会话对象、解析器、知识和视图夹具；没有运行实际ConversationHub依赖、完整turn、HTTP、数据库或设备。三条旧_read匹配新实例、三条迟到end移除新实例，5项正常控制通过。以下另写AST复算入口已对逐字转录片段运行并获得相同结果；尚未以完整固定仓库文件运行。将以下代码保存为probe.py，在候选隔离检出后执行 python probe.py platform/future_model/src/psychohistory/decision_conversation.py。只执行固定来源中经审查的五个方法，其他依赖全为夹具。
```python
import ast, json, sys
from collections import OrderedDict
from dataclasses import dataclass
from threading import RLock
from copy import deepcopy
from uuid import uuid4
SESSION_TTL=2700; MAX_SESSIONS=48; MAX_CANCELLATIONS=512
clock=0
def monotonic(): return clock
@dataclass
class Conversation:
    session_id: str
    base: object
    domain: str
    revision: int=1
    reuse_authority: object=None
    touched: float=0
class DecisionStateV05:
    model_validate=staticmethod(lambda x:x)
class Hub:
    def start(self,question): return {'state':question}
def discover_knowledge(question): return None
class Probe:
    def __init__(self):
        self.hub=Hub(); self._lock=RLock(); self._sessions=OrderedDict(); self._generation=0
        self._pending={}; self._cancelled={}; self._reject_client_starts_until=0
    def _parse(self,question): return {'domain':'fixture'}
    def _ingest(self,*args): pass
    def _view(self,row): return {'session_id':row.session_id,'revision':row.revision,'question':row.base}
def bind(path):
    tree=ast.parse(open(path,encoding='utf-8').read())
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name in ('ConversationHub','Probe'))
    names={'_expire','_read','_update','start','end'}
    for node in cls.body:
        if isinstance(node,ast.FunctionDef) and node.name in names:
            exec(compile(ast.Module(body=[node],type_ignores=[]),path,'exec'),globals())
            setattr(Probe,node.name,globals()[node.name]); names.remove(node.name)
    assert not names
def rejects(fn):
    try: fn()
    except (KeyError,ValueError): return True
    return False
def run():
    global clock
    out={}
    for mode in ('expiry','capacity','end_tombstone'):
        clock=0; p=Probe(); old=p.start('old',session_id='same')
        if mode=='expiry': clock=SESSION_TTL
        elif mode=='capacity':
            for i in range(MAX_SESSIONS): p.start('other',session_id=f'other{i}')
        else: p.end('same'); clock=SESSION_TTL
        assert rejects(lambda:p._read('same',1))
        new=p.start('new',session_id='same')
        observed=p._read(old['session_id'],old['revision']).base
        assert observed=='new' and old['revision']==new['revision']==1
        p.end(old['session_id']); assert rejects(lambda:p._read('same',1))
        out[mode]={'old_request_resolved_to':observed,'delayed_end_removed_new':True}
    clock=0; p=Probe(); p.start('old',session_id='same')
    assert rejects(lambda:p.start('new',session_id='same'))
    p.end('same'); assert rejects(lambda:p.start('new',session_id='same'))
    clock=SESSION_TTL-1; assert rejects(lambda:p.start('new',session_id='same'))
    clock=SESSION_TTL; p.start('new',session_id='different')
    assert rejects(lambda:p._read('same',1)); p.end('same'); assert p._read('different',1).base=='new'
    out['controls']=5
    return out
if __name__=='__main__':
    bind(sys.argv[1]); print(json.dumps(run(),indent=2))
```
实测两个夹具路径的三个模式输出均为 old_request_resolved_to=new, delayed_end_removed_new=true，controls=5。重复运行同一源码片段不构成独立样本。普通Python模式运行，不使用-O。

## 接入候选及后续验收
沿用第36/107轮，以服务端新建不可复用实例令牌区分生命周期，用户可见会话标签或首次取消请求标识仅作为关联线索。所有后续操作包括end必须绑定实例身份；turn开始及最后发布在同一服务端身份/修订/授权校验规则下通过，过期、淘汰、关闭、重新创建均使旧实例请求失效。局部结果收据同样绑定实例身份，不因数值或revision相同恢复。首次关闭可通过无敏感数据的短期预约处理；不能仅增加墓碑TTL、无限存储已用ID或把客户端新字段当授权。需设计旧协议迁移（缺实例身份的旧客户端保守拒绝有风险操作或独立隔离，不能静默允许重放）；不擅自破坏历史读档。原生验收重点：同ID跨生命周期、迟到turn与end、并行解析/关闭/新建、授权撤回与重建、旧API客户端、真实设备；证明错误结果未持久化及无跨实例显示。由独立轨执行未见回归；产品轨维护唯一交接。选择夹具和修复候选由研究者提出，非正式版本授权。无产品修改、合并、训练、部署、主动触发CI、冻结变更或新增费用。
