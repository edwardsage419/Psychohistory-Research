"""Shared CLI/API application boundary; no private or empirical execution in v0.1."""
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from .engine import run_experiment
from .evidence import Admission, scan_asset
from .plugins import registry
from .runtime import Scheduler
from .storage import Store

class ExperimentInput(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False,strict=True)
    seed:int=Field(default=7,ge=0,lt=2**32)
    rounds:int=Field(default=8,ge=1,le=100)
    population:int=Field(default=24,ge=1,le=1000)
    intervention:float=Field(default=.2,ge=0,le=1)
    permission:str='SYNTHETIC_ONLY'

class Service:
    def __init__(self,root,repo):
        self.store=Store(root);self.repo=Path(repo).resolve();self.scheduler=Scheduler(self.store)
    def submit(self,request):
        Admission.require(request.permission)
        config=request.model_dump(exclude={'permission'})
        if config['rounds']*config['population']>10000:raise ValueError('Combined work budget exceeds 10000 individual ticks')
        return self.scheduler.submit(config)
    def discover(self,path):return self.store.register_asset(scan_asset(self.repo,path))
    def close(self):self.scheduler.close()
