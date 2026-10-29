#!/usr/bin/env python3
"""F007 phase 3: synthetic versioned-object delete and retention audit.
No cloud access, credentials, paid APIs, or real data.
"""
from dataclasses import dataclass

@dataclass
class Version:
    vid:str
    mode:str='NONE'
    retain_until:int=0
    legal_hold:bool=False
    marker:bool=False

class FakeVersionedStore:
    def __init__(self): self.versions=[]
    def add(self,v): self.versions.append(v)
    def simple_delete(self):
        self.versions.append(Version('marker'+str(len(self.versions)),marker=True))
        return 'DELETE_MARKER_CREATED'
    def get(self,vid=None):
        if vid is None:
            if not self.versions or self.versions[-1].marker:return 'NOT_FOUND'
            return self.versions[-1].vid
        return 'AVAILABLE' if any(v.vid==vid and not v.marker for v in self.versions) else 'NOT_FOUND'
    def delete_version(self,vid,day,can_bypass=False,explicit_bypass=False):
        v=next((v for v in self.versions if v.vid==vid),None)
        if v is None:return 'NOT_FOUND'
        if v.legal_hold:return 'DENIED_LEGAL_HOLD'
        if day < v.retain_until:
            if v.mode=='COMPLIANCE':return 'DENIED_COMPLIANCE'
            if v.mode=='GOVERNANCE' and not(can_bypass and explicit_bypass):return 'DENIED_GOVERNANCE'
        self.versions.remove(v)
        return 'VERSION_REMOVED'

checks=0
def ok(v,msg):
    global checks
    checks+=1
    assert v,msg

store=FakeVersionedStore()
store.add(Version('v1',mode='COMPLIANCE',retain_until=100))
store.add(Version('v2',mode='GOVERNANCE',retain_until=100))
store.add(Version('v3',legal_hold=True))
ok(store.get()=='v3','current v3')
ok(store.simple_delete()=='DELETE_MARKER_CREATED','simple delete returns marker')
ok(store.get()=='NOT_FOUND','default get after marker')
ok(store.get('v1')=='AVAILABLE','protected old version survives marker')
ok(store.get('v2')=='AVAILABLE','governance version survives marker')
ok(store.get('v3')=='AVAILABLE','held version survives marker')
ok(store.delete_version('v1',1,True,True)=='DENIED_COMPLIANCE','compliance cannot bypass')
ok(store.delete_version('v2',1,False,True)=='DENIED_GOVERNANCE','no bypass permission')
ok(store.delete_version('v2',1,True,False)=='DENIED_GOVERNANCE','no explicit bypass request')
ok(store.delete_version('v2',1,True,True)=='VERSION_REMOVED','explicit governance bypass allowed')
ok(store.get('v2')=='NOT_FOUND','v2 gone')
ok(store.delete_version('v3',1,True,True)=='DENIED_LEGAL_HOLD','legal hold independent')
ok(store.delete_version('v1',100)=='VERSION_REMOVED','compliance retention expired')
ok(store.get('v1')=='NOT_FOUND','v1 gone')
ok(store.delete_version('v3',100)=='DENIED_LEGAL_HOLD','hold still active')
store.versions[0].legal_hold=False
ok(store.delete_version('v3',100)=='VERSION_REMOVED','hold removed with authorization')
ok(store.get('v3')=='NOT_FOUND','v3 gone')
ok(store.get()=='NOT_FOUND','marker remains current')
ok(len(store.versions)==1 and store.versions[0].marker,'only marker remains')
ok(store.delete_version(store.versions[0].vid,100)=='VERSION_REMOVED','remove marker by ID')
ok(len(store.versions)==0,'no versions in this synthetic store')
external_replica_verified=False
physical_media_verified=False
all_keys_destroyed_verified=False
global_erased=(len(store.versions)==0 and external_replica_verified and physical_media_verified and all_keys_destroyed_verified)
ok(global_erased is False,'global erasure cannot be inferred')
store.add(Version('v4'))
ok(store.get()=='v4','new version accessible')
ok(store.delete_version('v4',1)=='VERSION_REMOVED','per-version lock not inherited')
store.add(Version('v5',mode='COMPLIANCE',retain_until=500))
ok(store.delete_version('v5',100)=='DENIED_COMPLIANCE','lifecycle equivalent blocked')
ok(store.delete_version('v5',500)=='VERSION_REMOVED','retention expired')
print({'status':'PASS','assertions':checks,'synthetic_only':True,
       'versioning_lock_delete_marker_reproduced':True,
       'global_erasure':'UNVERIFIED','real_cloud_calls':0,'added_cost':0})
