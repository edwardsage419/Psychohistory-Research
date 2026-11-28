from collections import OrderedDict
from threading import RLock, Event, Thread
from uuid import uuid4
from types import SimpleNamespace as NS
import json, sys

INIT = '''    def __init__(self, *, hub=None, provider=None, records=None):
        self.hub = hub or DecisionHubV05()
        self.provider = provider or ConversationOllama()
        self.records = records
        self._lock = RLock()
        self._sessions = OrderedDict()

'''
START = '''    def start(self, question, *, use_local_model=False):
        base = DecisionStateV05.model_validate(self.hub.start(question)["state"])
        reading = interpret(question)
        row = Conversation(uuid4().hex, base, reading["domain"])
        self._ingest(row, question, reading, use_local_model)
        with self._lock:
            self._expire()
            return self._update(row)

'''
CLEAR = '''    def end(self, session_id):
        with self._lock:
            self._sessions.pop(session_id, None)
        return {"status": "ENDED"}

    def clear(self):
        with self._lock:
            self._sessions.clear()

'''
NEW_INIT = INIT.replace('        self._sessions = OrderedDict()\n','        self._sessions = OrderedDict()\n        self._generation = 0\n')
NEW_START = START.replace('        base = DecisionStateV05', '        with self._lock:\n            generation = self._generation\n        base = DecisionStateV05').replace('            self._expire()','            if generation != self._generation:\n                raise KeyError("Session invalidated")\n            self._expire()')
NEW_CLEAR = CLEAR.replace('            self._sessions.clear()', '            self._generation += 1\n            self._sessions.clear()')

def fnv(s):
    h=2166136261; b=s.encode('utf-16-le')
    for i in range(0,len(b),2): h=((h^int.from_bytes(b[i:i+2],'little'))*16777619)&0xffffffff
    return f'{h:08x}'

assert [fnv(x) for x in (INIT,START,CLEAR)]==['27de3a72','fcb73f3b','675b4bf7']

def make(fixed):
    env=dict(globals(),DecisionStateV05=NS(model_validate=lambda x:x),interpret=lambda q: {'domain':'life'},Conversation=lambda sid,b,d:NS(session_id=sid,base=b,domain=d))
    exec('class Hub:\n'+''.join((NEW_INIT,NEW_START,NEW_CLEAR) if fixed else (INIT,START,CLEAR)),env)
    cls=env['Hub']; cls._expire=lambda self:None
    def update(self,row):
        self._sessions[row.session_id]=row
        return row.session_id
    cls._update=update
    cls._ingest=lambda self,row,q,reading,allowed:self.provider.propose(q)
    return cls

def case(fixed, mode):
    entered,release=Event(),Event()
    def propose(q):
        if q=='old':
            entered.set()
            if not release.wait(5): raise RuntimeError('timeout')
    hub=make(fixed)(hub=NS(start=lambda q:{'state':q}),provider=NS(propose=propose))
    outcome=[]
    def start():
        try: outcome.append(('accepted',hub.start('old',use_local_model=True)))
        except KeyError: outcome.append(('rejected',None))
    th=Thread(target=start);th.start()
    try:
        assert entered.wait(5)
        if mode!='no_clear':hub.clear()
        if mode=='double_clear':hub.clear()
        fresh=hub.start('new') if mode=='new_after_clear' else None
    finally:
        release.set();th.join(5)
    assert not th.is_alive() and len(outcome)==1
    old_status,old_id=outcome[0]
    expected='rejected' if fixed and mode!='no_clear' else 'accepted'
    assert old_status==expected
    if old_id:assert old_id in hub._sessions
    if fresh:assert fresh in hub._sessions
    assert len(hub._sessions)==int(old_status=='accepted')+int(fresh is not None)
    return dict(fixed=fixed,mode=mode,old_status=old_status,remaining=len(hub._sessions),fresh_preserved=fresh in hub._sessions if fresh else None)

rows=[case(f,m) for f in (False,True) for m in ('no_clear','clear','double_clear','new_after_clear') for _ in range(10)]
result=dict(python=sys.version.split()[0],source_hashes=[fnv(x) for x in (INIT,START,CLEAR)],patched_hashes=[fnv(x) for x in (NEW_INIT,NEW_START,NEW_CLEAR)],cases=len(rows),old_recreated=sum(not x['fixed'] and x['mode']!='no_clear' and x['old_status']=='accepted' for x in rows),new_recreated=sum(x['fixed'] and x['mode']!='no_clear' and x['old_status']=='accepted' for x in rows),groups=[dict(x,count=sum(y==x for y in rows)) for x in rows[::10]],scope='Native init/start/end/clear methods, mocked state, ingest, expire and update. Actual threads; no real Ollama, API, full registry or supported runtime.')
print(json.dumps(result,indent=2))
