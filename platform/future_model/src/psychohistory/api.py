"""Authenticated same-origin loopback API; static client contains no secrets."""
from contextlib import asynccontextmanager
import hmac
from pathlib import Path
import secrets
from urllib.parse import urlsplit
from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from .plugins import registry
from .decision_api import MAX_DECISION_REQUEST, MAX_RESTORE_REQUEST
from .decision_api import DECISION_ROUTES, router as decision_router
from .decision_conversation_api import create_conversation_root, router as conversation_router
from .service import Service, ExperimentInput
from .storage import checked_path, write_new


def local_token(root):
    root=checked_path(root);root.mkdir(parents=True,exist_ok=True,mode=0o700)
    path=checked_path(root/'token')
    if not path.exists():write_new(path,secrets.token_urlsafe(32).encode())
    return path.read_text().strip()

class AssetInput(BaseModel):
    model_config=ConfigDict(extra='forbid')
    path:str


class SourceInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    research_id: str = Field(pattern=r"^R[0-9]{3}$")
    commit: str | None = Field(default=None, pattern=r"^[a-f0-9]{40}$")


class ProtocolInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    source_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    seed: int = Field(ge=0, lt=2**32)
    model_id: str
    model_version: str


class ComparisonInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    protocol_id: str = Field(pattern=r"^[a-f0-9]{64}$")


class TrajectoryInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    model_id: str
    model_version: str
    source_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    parameters: dict
    branch_from: str | None = Field(default=None, pattern=r"^[a-f0-9]{32}$")


class TrajectoryComparisonInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    left: str = Field(pattern=r"^[a-f0-9]{32}$")
    right: str = Field(pattern=r"^[a-f0-9]{32}$")
    metric: str = "trajectory"


def create_app(root,repo,token=None):
    token=token or local_token(root)
    @asynccontextmanager
    async def lifespan(app):
        app.state.service=Service(root,repo)
        try:yield
        finally:app.state.service.close()
    conversation = create_conversation_root(root)
    app=FastAPI(title='Psychohistory Platform v0.7',version='0.7.0',lifespan=lifespan,docs_url=None,redoc_url=None,openapi_url=None)

    @app.middleware('http')
    async def security(request:Request,call_next):
        if request.url.path.startswith('/api/') and request.url.path!='/api/v1/health':
            provided=request.headers.get('authorization','')
            if not hmac.compare_digest(provided,'Bearer '+token):return JSONResponse({'detail':'Local bearer token required'},status_code=401)
            origin=request.headers.get('origin')
            if origin and urlsplit(origin).netloc!=request.headers.get('host'):return JSONResponse({'detail':'Cross-origin request denied'},status_code=403)
            if request.method=='POST':
                length=request.headers.get('content-length')
                if length is None:return JSONResponse({'detail':'Content-Length required'},status_code=411)
                limit = 16384
                if request.url.path.startswith(DECISION_ROUTES):
                    limit = MAX_RESTORE_REQUEST if request.url.path.endswith("/restore") else MAX_DECISION_REQUEST
                if not length.isascii() or not length.isdecimal() or len(length) > 9 or int(length) > limit:
                    detail = 'Request exceeds 16 KiB' if limit == 16384 else 'Request exceeds the endpoint limit'
                    return JSONResponse({'detail':detail},status_code=413)
        response=await call_next(request)
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='no-referrer'
        response.headers['Content-Security-Policy']="default-src 'self'; connect-src 'self'; style-src 'self'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'"
        response.headers['Cache-Control']='no-store'
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        if request.url.path.startswith(DECISION_ROUTES):
            detail = [{"msg": "个人决策请求字段缺失或格式无效。"}]
            return JSONResponse({"detail": detail}, status_code=422)
        return await request_validation_exception_handler(request, exc)

    @app.exception_handler(ValueError)
    async def invalid(request,exc):return JSONResponse({'detail':str(exc)},status_code=422)
    @app.exception_handler(PermissionError)
    async def forbidden(request,exc):return JSONResponse({'detail':str(exc)},status_code=403)
    @app.exception_handler(KeyError)
    async def missing(request,exc):return JSONResponse({'detail':'Record not found'},status_code=404)

    @app.get('/api/v1/health')
    def health():return {'status':'ok','platform_version':'0.1.0','scientific_status':'SYNTHETIC_ONLY'}
    @app.get('/api/v1/models')
    def models():return registry.describe()
    @app.get('/api/v1/runs')
    def runs(limit:int=200,offset:int=0):return app.state.service.store.runs(limit,offset,kind="legacy")
    @app.get('/api/v1/runs/active')
    def active_runs():return app.state.service.store.active_runs(kind="legacy")
    @app.post('/api/v1/runs',status_code=201)
    def submit(data:ExperimentInput):return app.state.service.submit(data)
    def legacy_run(run_id):
        item = app.state.service.store.get_run(run_id)
        if item.get("kind", "legacy") != "legacy":
            raise KeyError("Unknown v1 run")
        return item

    @app.get('/api/v1/runs/{run_id}')
    def run(run_id:str):return legacy_run(run_id)
    @app.post('/api/v1/runs/{run_id}/approve')
    def approve(run_id: str):
        legacy_run(run_id)
        return app.state.service.scheduler.approve(run_id)
    @app.post('/api/v1/runs/{run_id}/cancel')
    def cancel(run_id: str):
        legacy_run(run_id)
        return app.state.service.scheduler.cancel(run_id)
    @app.get('/api/v1/runs/{run_id}/result')
    def result(run_id:str):
        run=legacy_run(run_id)
        if run['status']!='COMPLETED':raise ValueError('No completed result available')
        return app.state.service.store.get(run['result_hash'])
    @app.get('/api/v1/assets')
    def assets():return app.state.service.store.assets()
    @app.post('/api/v1/assets/discover')
    def discover(data:AssetInput):return app.state.service.discover(data.path)
    from . import sources
    from .v02_execution import RUN_KIND, RUN_KIND_TRAJECTORY
    from .workflow import models as comparison_models
    from .mechanisms import models as mechanism_models

    @app.get("/api/v2/source-catalog")
    def source_catalog():
        return sources.catalog()

    @app.get("/api/v2/models")
    def models_v2():
        return comparison_models()

    @app.get("/api/v2/sources")
    def source_list():
        return app.state.service.store.research_records("sources")

    @app.post("/api/v2/sources")
    def register_source(data: SourceInput):
        return app.state.service.workflow.register_source(data.research_id, data.commit)

    @app.post("/api/v2/sources/{identity}/verify")
    def verify_source(identity: str):
        return app.state.service.workflow.verify_source(identity)

    @app.get("/api/v2/protocols")
    def protocols():
        return app.state.service.store.research_records("protocols")

    @app.post("/api/v2/protocols")
    def create_protocol(data: ProtocolInput):
        return app.state.service.workflow.create_protocol(**data.model_dump())

    @app.post("/api/v2/protocols/{identity}/approve")
    def approve_protocol(identity: str):
        return app.state.service.workflow.approve_protocol(identity)

    @app.get("/api/v2/experiments")
    def experiments(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
        return app.state.service.store.runs(limit, offset, kind=RUN_KIND)

    @app.post("/api/v2/experiments")
    def submit_comparison(data: ComparisonInput):
        service = app.state.service
        return service.workflow.submit(service.scheduler, data.protocol_id)

    @app.get("/api/v2/experiments/{identity}")
    def comparison(identity: str):
        return app.state.service.workflow.run(identity)

    @app.post("/api/v2/experiments/{identity}/approve")
    def approve_comparison(identity: str):
        service = app.state.service
        service.workflow.run(identity)
        return service.scheduler.approve(identity)

    @app.post("/api/v2/experiments/{identity}/cancel")
    def cancel_comparison(identity: str):
        service = app.state.service
        service.workflow.run(identity)
        return service.scheduler.cancel(identity)

    @app.post("/api/v2/experiments/{identity}/retry")
    def retry_comparison(identity: str):
        service = app.state.service
        return service.workflow.retry(service.scheduler, identity)

    @app.get("/api/v2/experiments/{identity}/result")
    def comparison_result(identity: str):
        return app.state.service.workflow.result(identity)

    @app.get("/api/v3/models")
    def models_v3():
        return mechanism_models()

    @app.get("/api/v3/experiments")
    def trajectories(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
        return app.state.service.store.runs(limit, offset, kind=RUN_KIND_TRAJECTORY)

    @app.post("/api/v3/experiments", status_code=201)
    def submit_trajectory(data: TrajectoryInput):
        service = app.state.service
        return service.mechanisms.submit(service.scheduler, **data.model_dump())

    @app.get("/api/v3/experiments/{identity}")
    def trajectory(identity: str):
        return app.state.service.mechanisms.run(identity)

    @app.post("/api/v3/experiments/{identity}/approve")
    def approve_trajectory(identity: str):
        service = app.state.service
        service.mechanisms.run(identity)
        return service.scheduler.approve(identity)

    @app.post("/api/v3/experiments/{identity}/cancel")
    def cancel_trajectory(identity: str):
        service = app.state.service
        service.mechanisms.run(identity)
        return service.scheduler.cancel(identity)

    @app.get("/api/v3/experiments/{identity}/result")
    def trajectory_result(identity: str):
        return app.state.service.mechanisms.result(identity)

    @app.post("/api/v3/compare")
    def compare_trajectories(data: TrajectoryComparisonInput):
        return app.state.service.mechanisms.compare(**data.model_dump())

    app.include_router(decision_router(root, invalidate=conversation.invalidate,
                                       invalidate_record=conversation.invalidate_record))
    app.include_router(decision_router(root, advanced=True, invalidate=conversation.invalidate,
                                       invalidate_record=conversation.invalidate_record))
    app.include_router(conversation_router(conversation))
    app.include_router(conversation_router(conversation, legacy=True))

    dist=Path(__file__).resolve().parents[2]/'web/dist'
    if dist.is_dir():app.mount('/',StaticFiles(directory=dist,html=True),name='console')
    return app
