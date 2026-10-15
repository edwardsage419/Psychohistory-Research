#!/usr/bin/env python3
"""R023: reproduce respondent-paired descriptive contrast from original author CSV.
Original source Git blob SHA1 is pinned. No claim of experimental causal effect.
Usage: python r023_analysis.py data.csv --output results.json
"""
import csv,hashlib,io,json,random,argparse
from collections import defaultdict
from pathlib import Path
EXPECTED_BLOB='11c4ccb53944a79b1f1def49d358e04c944e42f1'

def blob_sha(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def analyze(text, boot=10000, seed=12823):
    rows=list(csv.DictReader(io.StringIO(text)))
    if not rows:raise ValueError('empty CSV')
    groups=defaultdict(lambda:{0:[],1:[]})
    cells={0:[],1:[]}
    for row in rows:
        inc=int(row['Incongruency']); agree=float(row['Agreement']); y=float(row['Comment_Likelihood'])
        if inc not in (0,1) or not(1<=agree<=7) or not(1<=y<=7):raise ValueError('invalid scale')
        groups[row['Participant']][inc].append(y);cells[inc].append(y)
    paired=[sum(x[1])/len(x[1])-sum(x[0])/len(x[0]) for x in groups.values() if x[0] and x[1]]
    if not paired:raise ValueError('no within-person paired conditions')
    result={'n_rows':len(rows),'n_people':len(groups),'n_incongruent':len(cells[1]),
      'n_congruent':len(cells[0]),'n_people_with_both':len(paired),
      'cell_means':{str(k):sum(x)/len(x) for k,x in cells.items()},
      'paired_difference':sum(paired)/len(paired)}
    if boot:
        rng=random.Random(seed);n=len(paired)
        draws=sorted(sum(paired[rng.randrange(n)] for _ in range(n))/n for _ in range(boot))
        result['bootstrap_95']=[draws[int(.025*boot)],draws[min(boot-1,int(.975*boot))]]
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--output',default='results.json');p.add_argument('--allow-unpinned',action='store_true');p.add_argument('--bootstrap',type=int,default=10000);a=p.parse_args()
    b=a.source.read_bytes();digest=blob_sha(b)
    if not a.allow_unpinned and digest!=EXPECTED_BLOB:raise SystemExit(f'Unexpected source Git blob: {digest}')
    res=analyze(b.decode('utf-8-sig'),a.bootstrap);res['source_git_blob']=digest
    Path(a.output).write_text(json.dumps(res,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(res,indent=2))
if __name__=='__main__':main()