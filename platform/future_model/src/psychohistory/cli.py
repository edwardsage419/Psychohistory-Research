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
    args=parser.parse_args(argv)
    exit_code=0
    try:
        if args.command=='models':
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
            if args.command=='runs':output=store.runs()
            elif args.command=='status':output=store.get_run(args.run_id)
            elif args.command=='result':
                run=store.get_run(args.run_id)
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
                    service.scheduler.approve(args.run_id);service.scheduler.execute_approved(args.run_id);output=service.scheduler.wait(args.run_id,30)
                    if output['status']!='COMPLETED':exit_code=1
                elif args.command=='cancel':output=service.scheduler.cancel(args.run_id)
                elif args.command=='result':output=service.store.get(service.scheduler.get(args.run_id)['result_hash'])
            finally:service.close()
        print(canonical(output));return exit_code
    except (ValueError,PermissionError,KeyError,OSError,TimeoutError) as exc:
        print(json.dumps({'status':'FAILED','error':str(exc)},ensure_ascii=False),file=sys.stderr);return 1

if __name__=='__main__':raise SystemExit(main())
