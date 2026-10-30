'use strict';
// Artificial snapshot reconciliation. No Health Connect API or personal data.
const assert = require('node:assert/strict');
function uniqueRecords(rows) {
  if (!Array.isArray(rows)) throw Error('ROWS_REQUIRED');
  const map = new Map();
  for (const r of rows) {
    if (!r || typeof r.id !== 'string' || !r.id ||
        !Number.isInteger(r.day) || !Number.isInteger(r.version) || r.version < 0 ||
        typeof r.value !== 'string') throw Error('BAD_RECORD');
    if (map.has(r.id)) throw Error('DUPLICATE_ID');
    map.set(r.id, r);
  }
  return map;
}
function reconcile(localRows, remoteRows, scope) {
  const local = uniqueRecords(localRows);
  const remote = uniqueRecords(remoteRows);
  if (!scope || !Number.isInteger(scope.start) || !Number.isInteger(scope.end) || scope.start > scope.end ||
      typeof scope.pagesComplete !== 'boolean' ||
      typeof scope.authorized !== 'boolean' || typeof scope.sourceSame !== 'boolean' ||
      typeof scope.consistentSnapshot !== 'boolean') throw Error('BAD_SCOPE');
  for (const r of remote.values()) if (r.day < scope.start || r.day > scope.end) throw Error('OUTSIDE_SCOPE');
  const trusted = scope.pagesComplete && scope.authorized && scope.sourceSame && scope.consistentSnapshot;
  const status = {};
  for (const [id, old] of local) {
    if (old.day < scope.start || old.day > scope.end) {
      status[id] = 'OUTSIDE_SCOPE_UNKNOWN';
    } else if (!trusted) {
      status[id] = 'SNAPSHOT_INCOMPLETE_UNKNOWN';
    } else if (!remote.has(id)) {
      status[id] = 'ABSENT_IN_AUTHORIZED_SNAPSHOT';
    } else if (remote.get(id).version < old.version) {
      status[id] = 'VERSION_CONFLICT';
    } else if (remote.get(id).version > old.version || remote.get(id).value !== old.value) {
      status[id] = 'RECONCILE_PRESENT';
    } else {
      status[id] = 'UNCHANGED';
    }
  }
  for (const [id] of remote) if (!local.has(id)) status[id] = trusted ? 'NEW_VISIBLE' : 'NEW_UNVERIFIED';
  return { trustedSnapshot: trusted, status,
    absentCount: Object.values(status).filter(x => x === 'ABSENT_IN_AUTHORIZED_SNAPSHOT').length,
    unknownCount: Object.values(status).filter(x => x.endsWith('UNKNOWN')).length };
}
const local = [
  {id:'a',day:-45,version:1,value:'1'},
  {id:'b',day:-40,version:1,value:'0'},
  {id:'c',day:-3,version:1,value:'1'},
  {id:'e',day:-2,version:1,value:'0'}
];
const recent = [{id:'c',day:-3,version:2,value:'0'}, {id:'d',day:-1,version:1,value:'1'}];
const full = [{id:'a',day:-45,version:1,value:'1'}, ...recent];
const good = {start:-60,end:0,pagesComplete:true,authorized:true,sourceSame:true,consistentSnapshot:true};
let checks=0;
function eq(a,b){assert.deepEqual(a,b);checks++;}
function rejects(fn,code){assert.throws(fn,e=>e.message===code);checks++;}
const windowed = reconcile(local,recent,{...good,start:-30});
eq(windowed.status.b,'OUTSIDE_SCOPE_UNKNOWN');
eq(windowed.status.e,'ABSENT_IN_AUTHORIZED_SNAPSHOT');
eq(windowed.status.c,'RECONCILE_PRESENT');
eq(windowed.status.d,'NEW_VISIBLE');
eq(windowed.absentCount,1);
const all = reconcile(local,full,good);
eq(all.status.b,'ABSENT_IN_AUTHORIZED_SNAPSHOT');
eq(all.status.a,'UNCHANGED');
eq(all.absentCount,2);
eq(all.unknownCount,0);
for (const key of ['pagesComplete','authorized','sourceSame','consistentSnapshot']) {
  const incomplete=reconcile(local,full,{...good,[key]:false});
  eq(incomplete.status.b,'SNAPSHOT_INCOMPLETE_UNKNOWN');
  eq(incomplete.absentCount,0);
}
const stale=reconcile(local,[{id:'c',day:-3,version:0,value:'x'}],good);
eq(stale.status.c,'VERSION_CONFLICT');
rejects(()=>reconcile([{...local[0]},{...local[0]}],full,good),'DUPLICATE_ID');
rejects(()=>reconcile(local,[{id:'x',day:100,version:0,value:'x'}],good),'OUTSIDE_SCOPE');
rejects(()=>reconcile(local,full,{...good,start:2,end:1}),'BAD_SCOPE');
rejects(()=>reconcile(local,full,[1,2]),'BAD_SCOPE');
rejects(()=>reconcile(local,[{id:'z',day:0,version:-1,value:'x'}],good),'BAD_RECORD');
console.log(JSON.stringify({study:'MKT143',checks,windowed,full:all,scope:'ARTIFICIAL_E1_ONLY',node:process.version}));
module.exports={reconcile};
