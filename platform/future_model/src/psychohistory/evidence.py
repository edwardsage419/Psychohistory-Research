"""Read-only identity discovery, never execution or evidence promotion."""
import hashlib
import json
from pathlib import Path

class Admission:
    @staticmethod
    def require(permission):
        if permission!='SYNTHETIC_ONLY':
            raise PermissionError('BLOCKED: only built-in public synthetic experiments are approved; owner scientific review required')


def scan_asset(repo, relative):
    repo=Path(repo).resolve()
    rel=Path(relative)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts or rel.parts[0] not in {'research','theory','protocols','docs','manifests'}:
        raise ValueError('Research read path outside allowlist')
    path=repo/rel
    for parent in [path,*path.parents]:
        if parent==repo:break
        if parent.is_symlink():raise ValueError('Symlink sources forbidden')
    if not path.is_file() or path.suffix not in {'.json','.md'} or path.stat().st_size>1024*1024:
        raise ValueError('Missing or unsupported metadata source (1 MiB maximum)')
    raw=path.read_bytes()
    if path.suffix=='.json':
        try:data=json.loads(raw)
        except (ValueError,UnicodeDecodeError) as e:raise ValueError('Invalid source JSON') from e
        if not isinstance(data,dict):raise ValueError('Source receipt must be an object')
    else:data={'text':raw.decode('utf-8')}
    namespace='R_SERIES_ORIGINAL' if len(rel.parts)>1 and rel.parts[1].startswith('R') else 'REPOSITORY_ORIGINAL'
    return {'path':rel.as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw),
            'engineering_status':'HASHED_METADATA_ONLY','scientific_status':{'namespace':namespace,'original_record':data},
            'permission':'BROWSE_ONLY','source':'REPOSITORY_READ_ONLY','warning':'Discovery is not execution or scientific acceptance'}
