#!/usr/bin/env node
'use strict';
/* Independent R140 exact audit using ternary action codes and bit flags.
   No original R140 ZIP source is imported. Synthetic E1 only. */
const fs = require('node:fs');
const crypto = require('node:crypto');
const path = require('node:path');
const hash = s => crypto.createHash('sha256').update(s).digest('hex');
const asAction = id => [Math.floor(id / 9), Math.floor(id / 3) % 3, id % 3];
const config = id => ({
  boundary: (id & 64) ? 3 : 2,
  position: (id & 32) ? 'steward' : 'all',
  cap: (id & 16) ? 2 : 1,
  aggregation: (id & 8) ? 'quota4' : 'independent',
  information: (id & 4) ? 'public' : 'private',
  fee: (id & 2) ? 2 : 0,
  scope: (id & 1) ? 6 : 4
});
const encode = a => a[0] * 9 + a[1] * 3 + a[2];
function feasible(c, a) {
  if (a.some(x => x > c.cap)) return false;
  for (let i = 0; i < 3; ++i) {
    if (i >= c.boundary && a[i] !== 0) return false;
  }
  if (c.position === 'steward' && a[2] !== 0) return false;
  const sum = a[0] + a[1] + a[2];
  return sum <= c.scope && (c.aggregation !== 'quota4' || sum <= 4);
}
function values(c, a) {
  const sum = a[0] + a[1] + a[2];
  const active = c.boundary === 3 && c.position === 'steward' && c.information === 'public' && c.fee === 2;
  return a.map(x => x * (8 - sum) - (active ? 2 * Math.max(0, x - 1) : 0));
}
function replay(c) {
  const admissible = [];
  for (let code = 0; code < 27; ++code) {
    const a = asAction(code);
    if (feasible(c, a)) admissible.push(a);
  }
  const codes = new Set(admissible.map(encode));
  const rows = [];
  const ne = [];
  let nEdges = 0;
  let maxResource = -Infinity;
  for (const a of admissible) {
    const sum = a[0] + a[1] + a[2];
    maxResource = Math.max(maxResource, sum * (8 - sum));
  }
  for (const a of admissible) {
    const u = values(c, a);
    let largest = -Infinity;
    for (let player = 0; player < 3; ++player) {
      for (let x = 0; x <= c.cap; ++x) {
        if (x === a[player]) continue;
        const candidate = [...a];
        candidate[player] = x;
        if (!codes.has(encode(candidate))) continue;
        nEdges++;
        const gain = values(c, candidate)[player] - u[player];
        if (gain > largest) largest = gain;
      }
    }
    const equilibrium = largest <= 0;
    if (equilibrium) ne.push(a);
    rows.push([a, u, Number(equilibrium)]);
  }
  return {
    profiles: admissible.length,
    deviations: nEdges,
    game_rows: rows,
    pure_ne: ne,
    resource_optimum: maxResource,
    has_resource_optimal_ne: ne.some(a => {
      const sum = a[0] + a[1] + a[2];
      return sum * (8 - sum) === maxResource;
    }),
    canonical_game_sha256: hash(JSON.stringify(rows))
  };
}
function main() {
  const file = path.join(__dirname, 'R140_EFFECTIVE_RULE_GRAPH_128_EXACT_RESULTS_2026-10-25.json');
  const python = JSON.parse(fs.readFileSync(file, 'utf8'));
  const sizes = new Map();
  const fingerprints = [];
  const allOptimal = [];
  let rows = 0, edges = 0, good = 0;
  for (let id = 0; id < 128; ++id) {
    const c = config(id);
    const current = replay(c);
    const other = python.records[id];
    for (const k of ['profiles','deviations','pure_ne','resource_optimum','has_resource_optimal_ne','canonical_game_sha256','game_rows']) {
      if (JSON.stringify(current[k]) !== JSON.stringify(other[k])) throw Error(`R140 ${id} ${k} mismatch`);
    }
    fingerprints.push(current.canonical_game_sha256);
    allOptimal.push(current.pure_ne.every(a => {const t = a[0]+a[1]+a[2]; return t*(8-t) === current.resource_optimum;}));
    rows += current.profiles;
    edges += current.deviations;
    good += Number(current.has_resource_optimal_ne);
    sizes.set(current.canonical_game_sha256, (sizes.get(current.canonical_game_sha256) || 0) + 1);
  }
  const pairs = [...sizes.values()].reduce((s, n) => s + n * (n - 1) / 2, 0);
  const counts = [128, rows, edges, sizes.size, pairs, good];
  if (JSON.stringify(counts) !== JSON.stringify([128,1136,4584,6,2272,124])) throw Error(`Frozen totals mismatch ${counts}`);
  const axisLabels = ['boundary','position','cap','aggregation','information','fee','scope'];
  const unchangedByAxis = Object.fromEntries(axisLabels.map((label,j) => {
    const mask = 1 << (6-j);
    let same = 0;
    for (let id=0; id<128; ++id) if (!(id & mask) && fingerprints[id] === fingerprints[id | mask]) same++;
    return [label, same];
  }));
  if (allOptimal.filter(Boolean).length !== 124) throw Error('All equilibrium optimality check mismatch');
  console.log(JSON.stringify({independent_language:'Node.js', cross_language_exact_rows:128, synthetic_profiles:rows,
    directed_unilateral_edges:edges, signatures:sizes.size, equivalent_pairs:pairs, optimal_ne_cases:good,
    signature_sizes:[...sizes.values()].sort((a,b)=>a-b), all_ne_resource_optimal_cases:allOptimal.filter(Boolean).length,
    unchanged_one_axis_pairs:unchangedByAxis, status:'PASS_INTERNAL_E1'}, null, 2));
}
main();
