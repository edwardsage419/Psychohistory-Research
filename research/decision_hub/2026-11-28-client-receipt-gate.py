"""Synthetic client host messages; no network or native UI."""
from itertools import permutations, product

class Gate:
    def __init__(self, epoch, generation, scope):
        self.epoch=epoch;self.generation=generation;self.scope=scope;self.shown=None;self.connected=True
    def host(self,epoch,generation,scope):
        if epoch!=self.epoch or generation<self.generation:return False
        if generation==self.generation:
            if scope!=self.scope:
                self.disconnect() # conflicting authoritative notification: fail closed
                return False
            return self.connected
        self.generation=generation;self.scope=scope;self.shown=None
        return self.connected
    def disconnect(self):
        self.connected=False;self.shown=None
    def receipt(self,epoch,generation,scope,complete):
        if not self.connected or self.scope is None or not complete:return False
        if (epoch,generation,scope)!=(self.epoch,self.generation,self.scope):return False
        self.shown=(epoch,generation,scope);return True

def run():
    schedules=old_reject=early_reject=weak_final=0
    for field in range(6):
        old=(1,)*6;new=tuple(v+int(i==field) for i,v in enumerate(old))
        for order in permutations(('host','old','new','stale_host','retry')):
            if order.index('retry')<max(order.index('new'),order.index('host')):continue
            g=Gate(1,0,old);weak=None
            for e in order:
                if e=='host':assert g.host(1,1,new);weak=None
                elif e=='stale_host':g.host(1,0,old)
                elif e=='old':
                    ok=g.receipt(1,0,old,True);weak=old
                    assert ok==(g.generation==0)
                    old_reject+=not ok
                else:
                    ok=g.receipt(1,1,new,True);weak=new
                    assert ok==(g.generation==1)
                    early_reject+=not ok
                assert g.shown is None or g.shown==(g.epoch,g.generation,g.scope)
            assert g.shown==(1,1,new);weak_final+=weak==old;schedules+=1
    negatives=0
    for mode,epoch,generation,complete in product(('revoke','disconnect','conflict','normal'),(0,1,2),(0,1,2),(False,True)):
        g=Gate(1,1,(1,)*6)
        assert g.receipt(1,1,(1,)*6,True)
        if mode=='revoke':g.host(1,2,None)
        elif mode=='disconnect':g.disconnect()
        elif mode=='conflict':assert not g.host(1,1,(2,)*6)
        ok=g.receipt(epoch,generation,(1,)*6,complete)
        assert ok==(mode=='normal' and epoch==generation==1 and complete)
        if mode!='normal':assert g.shown is None
        negatives+=not ok
    print('schedules',schedules,'old_reject',old_reject,'early_reject',early_reject,'weak_final',weak_final,'negative_receipts',negatives)
if __name__=='__main__':run()
