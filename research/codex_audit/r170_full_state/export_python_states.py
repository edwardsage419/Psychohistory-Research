#!/usr/bin/env python3
"""Read-only B adapter; imports only the archived B module, never JavaScript."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
path=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('archived_r170_b',path)
b=importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
records=[]
for graph,edges in b.GRAPHS.items():
    for initial,start in b.INITIALS.items():
        for nu in b.NU:
            for mode in b.MODES:
                snapshots=b.full_path(edges,start,nu,mode)
                for t,law in enumerate(snapshots):
                    records.append({'graph':graph,'initial':initial,'nu':str(nu),'mode':mode,'t':t,
                                    'law':{''.join(map(str,s)):str(p) for s,p in sorted(law.items())}})
print(json.dumps({'route':'archived_Python_undirected_utterance_flip',
                  'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'records':records},indent=2))
