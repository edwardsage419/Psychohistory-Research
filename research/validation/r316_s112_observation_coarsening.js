#!/usr/bin/env node
'use strict';
// Frozen R316 S112, E1 artificial source only. Read immutable original JSON.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..', '..');
const SOURCE = path.join(ROOT, 'research/R316/R316_EXACT_128_GRAPH_LIKELIHOODS.json');
const RECEIPT = path.join(__dirname, 'R316_S112_OBSERVATION_COARSENING_EXACT.json');
const SOURCE_BLOB = '36da587adbc6e1d92824a5fd39516e506569166c';
const FREEZE = 'af948405bc682f10cdf6f3add73ab2f35e10c0b4';
function assert(condition, msg) { if (!condition) throw new Error(msg); }
function gitBlob(buffer) { return crypto.createHash('sha1').update(Buffer.from(`blob ${buffer.length}\0`)).update(buffer).digest('hex'); }
function gcd(a, b) { while (b) [a, b] = [b, a % b]; return a; }
function frac(n, d) { const g = gcd(n, d); return `${n / g}/${d / g}`; }
const maps = {
  full: g => g.edge_vector,
  within_cross: g => `${g.within_edges},${g.cross_edges}`,
  signed_difference: g => String(g.within_edges - g.cross_edges),
  within_only: g => String(g.within_edges),
  cross_only: g => String(g.cross_edges),
  total_only: g => String(g.within_edges + g.cross_edges),
};
function score(data) {
  assert(data.schema === 'r316_sbm_known_block_4node_all_graphs_exact_E1_v1', 'schema');
  assert(data.original_catalogue_id === '04-019' && data.source_scope === 'SYNTHETIC_EXACT_E1_ONLY', 'scope');
  assert(JSON.stringify(data.fixed_blocks) === '[0,0,1,1]', 'blocks');
  assert(JSON.stringify(data.dyads) === '[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]', 'dyads');
  assert(data.source_atom_count === 768 && data.graph_count === 128 && data.total_variation_A_D === '203/256', 'source summary');
  assert(data.regimes.length === 2, 'regime count');
  const params = [['A', '3/4', '1/4'], ['D', '1/4', '3/4']];
  for (let i = 0; i < 2; i++) {
    const r = data.regimes[i];
    assert(r.regime === params[i][0] && r.within_p === params[i][1] && r.cross_p === params[i][2], 'parameters');
    assert(r.complete_graphs.length === 64, 'graph count');
    const seen = new Set();
    let total = 0;
    for (const g of r.complete_graphs) {
      assert(Number.isInteger(g.mask) && g.mask >= 0 && g.mask < 64 && !seen.has(g.mask), 'mask identity');
      seen.add(g.mask);
      const bits = g.mask.toString(2).padStart(6, '0');
      assert(g.edge_vector === bits && g.within_edges === Number(bits[0]) + Number(bits[5]) && g.cross_edges === [...bits.slice(1, 5)].reduce((a, x) => a + Number(x), 0), 'graph counts');
      const match = /^(\d+)\/(\d+)$/.exec(g.probability);
      assert(match && Number(match[2]) === 4096, 'probability representation');
      total += Number(match[1]);
    }
    assert(seen.size === 64 && total === 4096, 'normalization');
  }
  const observations = {};
  for (const [name, observe] of Object.entries(maps)) {
    const groups = new Map();
    for (let regime = 0; regime < 2; regime++) for (const g of data.regimes[regime].complete_graphs) {
      const key = observe(g);
      const row = groups.get(key) || [0, 0];
      row[regime] += Number(g.probability.split('/')[0]);
      groups.set(key, row);
    }
    let maxSum = 0, absoluteSum = 0;
    for (const pair of groups.values()) { maxSum += Math.max(...pair); absoluteSum += Math.abs(pair[0] - pair[1]); }
    observations[name] = {bins: groups.size, accuracy: frac(maxSum, 8192), total_variation: frac(absoluteSum, 8192)};
  }
  const accuracyNumerators = Object.fromEntries(Object.entries(observations).map(([k, v]) => [k, Number(v.accuracy.split('/')[0]) / Number(v.accuracy.split('/')[1])]));
  assert(accuracyNumerators.full === accuracyNumerators.within_cross && accuracyNumerators.full === accuracyNumerators.signed_difference, 'signed sufficiency');
  for (const k of ['within_only', 'cross_only', 'total_only']) assert(accuracyNumerators.full >= accuracyNumerators[k], 'coarsening');
  return {schema: 'r316_s112_equal_prior_observation_coarsening_E1_v1', source_blob_sha1: SOURCE_BLOB, freeze_commit: FREEZE, evidence_grade: 'E1_SYNTHETIC_ONLY', graph_count: 128, observations};
}
function main() {
  const bytes = fs.readFileSync(SOURCE);
  assert(gitBlob(bytes) === SOURCE_BLOB, 'original source Git blob changed');
  const result = score(JSON.parse(bytes.toString('utf8')));
  if (process.argv.includes('--check')) {
    const archived = JSON.parse(fs.readFileSync(RECEIPT, 'utf8'));
    assert(JSON.stringify(result) === JSON.stringify(archived), 'persisted receipt mismatch');
    console.log('PASS R316 S112 archived source and six observation maps');
  } else console.log(JSON.stringify(result, null, 2));
}
if (require.main === module) main();
module.exports = {score, gitBlob};
