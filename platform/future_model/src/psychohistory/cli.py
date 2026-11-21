"""Local CLI. Same service/admission as Web; backups never include bearer tokens."""
import argparse
import json
import os
from pathlib import Path
import sys
from .contracts import canonical


def main(argv=None):
    parser=argparse.ArgumentParser(prog='psychohistory')
    default_root=Path('/workspace/psychohistory-data') if Path('/workspace').exists() else Path.home()/'.local/share/psychohistory'
    parser.add_argument('--data',type=Path,default=default_root)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[4])
    sub=parser.add_subparsers(dest='command',required=True)
    from . import decision_cli
    decision_cli.add_parser(sub)
    sub.add_parser('models')
    demo=sub.add_parser('demo');demo.add_argument('--seed',type=int,default=7);demo.add_argument('--rounds',type=int,default=8);demo.add_argument('--population',type=int,default=24);demo.add_argument('--intervention',type=float,default=.2)
    scan=sub.add_parser('discover');scan.add_argument('path')
    sub.add_parser('runs')
    for name in ['status','approve','cancel','result']:
        p=sub.add_parser(name);p.add_argument('run_id')
    submit=sub.add_parser('submit');submit.add_argument('--seed',type=int,default=7)
    backup=sub.add_parser('backup');backup.add_argument('destination',type=Path)
    restore=sub.add_parser('restore');restore.add_argument('source',type=Path)
    serve=sub.add_parser('serve');serve.add_argument('--port',type=int,default=8765)
    sub.add_parser('token')
    research = sub.add_parser("research", help="v0.2 sources, protocols and experiments")
    actions = research.add_subparsers(dest="action", required=True)
    for name in ("catalog", "models", "sources", "protocols", "experiments"):
        actions.add_parser(name)
    register = actions.add_parser("register")
    register.add_argument("research_id")
    register.add_argument("--commit")
    protocol = actions.add_parser("protocol")
    protocol.add_argument("source_id")
    protocol.add_argument("--seed", type=int, default=7)
    for name in ("verify", "approve-protocol", "submit", "retry", "status", "approve", "cancel", "result"):
        actions.add_parser(name).add_argument("identity")
    mechanism = sub.add_parser("mechanism", help="v0.3 synthetic trajectories and checkpoints")
    actions = mechanism.add_subparsers(dest="action", required=True)
    for name in ("models", "experiments"):
        actions.add_parser(name)
    for name in ("status", "approve", "cancel", "result"):
        actions.add_parser(name).add_argument("identity")
    trajectory = actions.add_parser("submit")
    trajectory.add_argument("model_id")
    trajectory.add_argument("model_version")
    trajectory.add_argument("source_id")
    trajectory.add_argument("--parameters", required=True, help="Bounded JSON method parameters")
    trajectory.add_argument("--branch-from")
    comparison = actions.add_parser("compare")
    comparison.add_argument("left")
    comparison.add_argument("right")
    comparison.add_argument("--metric", default="trajectory")
    args=parser.parse_args(argv)
    exit_code=0
    try:
        if args.command == "decision":
            output = decision_cli.run(args)
        elif args.command == "research":
            output, exit_code = research_command(args)
        elif args.command == "mechanism":
            output, exit_code = mechanism_command(args)
        elif args.command=='models':
            from .plugins import registry
            output=registry.describe()
        elif args.command=='restore':
            from .storage import restore_backup
            output={'restored_to':str(restore_backup(args.source,args.data).root)}
        elif args.command=='token':
            from .api import local_token
            print(local_token(args.data));return 0
        elif args.command=='serve':
            from .api import create_app,local_token
            import uvicorn
            local_token(args.data)
            print('Local token file:',args.data/'token','(never commit or paste into logs)',file=sys.stderr)
            uvicorn.run(create_app(args.data,args.repo),host='127.0.0.1',port=args.port,access_log=False);return 0
        elif args.command in {'runs','status','result','discover'}:
            from .storage import Store
            store=Store(args.data)
            if args.command=='runs':output=store.runs(kind="legacy")
            elif args.command=='status':output=legacy_run(store, args.run_id)
            elif args.command=='result':
                run=legacy_run(store, args.run_id)
                if run['status']!='COMPLETED':raise ValueError('No completed result available')
                output=store.get(run['result_hash'])
            else:
                from .evidence import scan_asset
                output=store.register_asset(scan_asset(args.repo,args.path))
        else:
            from .service import Service,ExperimentInput
            service=Service(args.data,args.repo,dispatch=False)
            try:
                if args.command in {'submit','demo'}:
                    request=ExperimentInput(**{k:getattr(args,k) for k in ['seed','rounds','population','intervention'] if hasattr(args,k)})
                    output=service.submit(request)
                    if args.command=='demo':
                        service.scheduler.approve(output['id']);service.scheduler.execute_approved(output['id']);output=service.scheduler.wait(output['id'],30)
                        if output['status']!='COMPLETED':raise ValueError(output['error'] or output['status'])
                        output={'run':output,'result':service.store.get(output['result_hash'])}
                elif args.command=='discover':output=service.discover(args.path)
                elif args.command=='runs':output=service.store.runs()
                elif args.command=='backup':output=service.scheduler.backup(args.destination)
                elif args.command=='status':output=service.scheduler.get(args.run_id)
                elif args.command=='approve':
                    legacy_run(service.store, args.run_id)
                    service.scheduler.approve(args.run_id);service.scheduler.execute_approved(args.run_id);output=service.scheduler.wait(args.run_id,30)
                    if output['status']!='COMPLETED':exit_code=1
                elif args.command=='cancel':
                    legacy_run(service.store, args.run_id)
                    output=service.scheduler.cancel(args.run_id)
                elif args.command=='result':output=service.store.get(service.scheduler.get(args.run_id)['result_hash'])
            finally:service.close()
        print(canonical(output));return exit_code
    except (ValueError,PermissionError,KeyError,OSError,TimeoutError) as exc:
        print(json.dumps({'status':'FAILED','error':str(exc)},ensure_ascii=False),file=sys.stderr);return 1

def legacy_run(store, identity):
    run = store.get_run(identity)
    if run.get("kind", "legacy") != "legacy":
        raise KeyError("Use the matching versioned experiment command")
    return run


def research_command(args):
    from . import sources
    from .service import Service
    from .storage import Store
    from .v02_execution import RUN_KIND
    from .workflow import Workflow, models

    action = args.action
    if action == "catalog":
        return sources.catalog(), 0
    if action == "models":
        return models(), 0
    store = Store(args.data)
    workflow = Workflow(store, args.repo)
    if action in {"sources", "protocols"}:
        return store.research_records(action), 0
    if action == "register":
        return workflow.register_source(args.research_id, args.commit), 0
    if action == "verify":
        return workflow.verify_source(args.identity), 0
    if action == "protocol":
        return workflow.create_protocol(args.source_id, args.seed, "r123-degroot", "1.0.0"), 0
    if action == "approve-protocol":
        return workflow.approve_protocol(args.identity), 0
    if action == "experiments":
        return store.runs(kind=RUN_KIND), 0
    if action == "status":
        return workflow.run(args.identity), 0
    if action == "result":
        return workflow.result(args.identity), 0
    service = Service(args.data, args.repo, dispatch=False)
    scheduler = service.scheduler
    try:
        if action == "submit":
            return workflow.submit(scheduler, args.identity), 0
        if action == "retry":
            return workflow.retry(scheduler, args.identity), 0
        workflow.run(args.identity)
        if action == "cancel":
            return scheduler.cancel(args.identity), 0
        scheduler.approve(args.identity)
        scheduler.execute_approved(args.identity)
        result = scheduler.wait(args.identity)
        return result, int(result["status"] != "COMPLETED")
    finally:
        service.close()


def mechanism_command(args):
    from .mechanisms import Mechanisms, models
    from .service import Service
    from .storage import Store
    from .v02_execution import RUN_KIND_TRAJECTORY

    action = args.action
    if action == "models":
        return models(), 0
    store = Store(args.data)
    mechanisms = Mechanisms(store, args.repo)
    if action == "experiments":
        return store.runs(kind=RUN_KIND_TRAJECTORY), 0
    if action == "status":
        return mechanisms.run(args.identity), 0
    if action == "result":
        return mechanisms.result(args.identity), 0
    if action == "compare":
        return mechanisms.compare(args.left, args.right, args.metric), 0

    service = Service(args.data, args.repo, dispatch=False)
    scheduler = service.scheduler
    try:
        if action == "submit":
            if len(args.parameters.encode()) > 16384:
                raise ValueError("Parameters exceed 16 KiB")
            parameters = json.loads(args.parameters)
            return mechanisms.submit(scheduler, args.model_id, args.model_version,
                                     args.source_id, parameters, args.branch_from), 0
        mechanisms.run(args.identity)
        if action == "cancel":
            return scheduler.cancel(args.identity), 0
        scheduler.approve(args.identity)
        scheduler.execute_approved(args.identity)
        result = scheduler.wait(args.identity)
        return result, int(result["status"] != "COMPLETED")
    finally:
        service.close()


if __name__=='__main__':raise SystemExit(main())
