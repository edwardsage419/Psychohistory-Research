'use strict';
// MKT144: synthetic Health Connect origin migration and export-merge identity controls.
const assert = require('node:assert/strict');
let checks = 0;
const ok = (x, message) => { assert.ok(x, message); checks++; };
const eq = (a, b) => { assert.deepEqual(a, b); checks++; };
const reject = (fn) => { assert.throws(fn, TypeError); checks++; };
function validate(rows) {
  if (!Array.isArray(rows) || rows.length === 0) throw new TypeError('rows required');
  const ids = new Set();
  for (const r of rows) {
    if (!r || typeof r.recordId !== 'string' || !r.recordId || ids.has(r.recordId) ||
        typeof r.origin !== 'string' || !r.origin || !/^\d{4}-\d{2}-\d{2}$/.test(r.day) ||
        !Number.isSafeInteger(r.steps) || r.steps < 0) throw new TypeError('invalid row');
    ids.add(r.recordId);
  }
  return rows;
}
function sum(rows) { return validate(rows).reduce((n,r) => n + r.steps, 0); }
function group(rows, field) {
  const result = {};
  for (const r of validate(rows)) result[r[field]] = (result[r[field]] || 0) + r.steps;
  return result;
}
function oracleDedup(rows, trustedIdentity) {
  validate(rows);
  if (!trustedIdentity || typeof trustedIdentity !== 'object') throw new TypeError('trusted identity missing');
  const seen = new Map();
  for (const r of rows) {
    const id = trustedIdentity[r.recordId];
    if (typeof id !== 'string' || !id) throw new TypeError('identity unproven');
    const old = seen.get(id);
    if (old && (old.day !== r.day || old.steps !== r.steps)) throw new TypeError('conflicting event');
    if (!old) seen.set(id, r);
  }
  return [...seen.values()].reduce((n,r) => n+r.steps,0);
}
const rows = [
  {recordId:'legacy1', day:'2026-06-01',origin:'android',steps:1200},
  {recordId:'current2',day:'2026-06-02',origin:'spn_appA_deviceX',steps:1400},
  {recordId:'mirror1', day:'2026-06-01',origin:'spn_appA_deviceX',steps:1200}
];
const oracle = {legacy1:'E1',current2:'E2',mirror1:'E1'};
eq(sum(rows),3800);
eq(oracleDedup(rows,oracle),2600);
eq(sum(rows)-oracleDedup(rows,oracle),1200);
eq((sum(rows)-oracleDedup(rows,oracle))/oracleDedup(rows,oracle),6/13);
eq(group(rows,'origin'),{android:1200,spn_appA_deviceX:2600});
eq(group(rows,'day'),{'2026-06-01':2400,'2026-06-02':1400});
eq(sum(rows.filter(r=>r.origin==='android')),1200);
eq(sum(rows.filter(r=>r.origin!=='android')),2600);
const migrationOnly=rows.slice(0,2);
eq(sum(migrationOnly),2600);
eq(oracleDedup(migrationOnly,{legacy1:'E1',current2:'E2'}),2600);
ok(rows[0].recordId!==rows[2].recordId,'ID-only dedup cannot identify mirror');
ok(rows[1].origin!==rows[0].origin,'origin migrated');
reject(()=>validate([...rows,rows[0]]));
reject(()=>validate([{...rows[0],steps:-1}]));
reject(()=>validate([{...rows[0],steps:1.5}]));
reject(()=>oracleDedup(rows,{legacy1:'E1',current2:'E2'}));
reject(()=>oracleDedup(rows,{legacy1:'E1',current2:'E1',mirror1:'E1'}));
const report={evidence:'E1_ARTIFICIAL_NONBLIND',rows:rows.length,raw:sum(rows),
  hypothetical_oracle_dedup:oracleDedup(rows,oracle),inflation_fraction:'6/13',
  migration_only_total:sum(migrationOnly),checks};
console.log(JSON.stringify(report));
