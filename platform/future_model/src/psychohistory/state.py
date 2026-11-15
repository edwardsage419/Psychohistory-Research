"""Immutable content-addressed snapshots with independently restored payloads."""
from dataclasses import dataclass
import hashlib
import json
from .contracts import canonical

@dataclass(frozen=True)
class Snapshot:
    serialized: str
    content_hash: str

    @classmethod
    def create(cls, model_id, version, state, branch, parent, events, environment, random_state=None):
        payload={'snapshot_version':'1.0.0','model_id':model_id,'model_version':version,'state':state,
                 'branch':branch,'parent_hash':parent,'events':events,'environment':environment,'random_state':random_state}
        raw=canonical(payload)
        return cls(raw, hashlib.sha256(raw.encode()).hexdigest())

    def restore(self):
        if hashlib.sha256(self.serialized.encode()).hexdigest()!=self.content_hash:
            raise ValueError('Snapshot hash mismatch')
        data=json.loads(self.serialized)
        if data['snapshot_version']!='1.0.0':
            raise ValueError('Incompatible snapshot version')
        return data

    def to_dict(self):
        return {'content_hash':self.content_hash,'payload':self.restore()}

    @classmethod
    def from_dict(cls,data):
        obj=cls(canonical(data['payload']),data['content_hash']);obj.restore();return obj

    def fork(self, name):
        if not name or name==self.restore()['branch']:
            raise ValueError('New branch identity required')
        d=self.restore()
        return self.create(d['model_id'],d['model_version'],d['state'],name,self.content_hash,d['events'],d['environment'],d['random_state'])
