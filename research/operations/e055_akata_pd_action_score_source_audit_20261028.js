#!/usr/bin/env node
// E055 independent source audit. Supply downloaded original author files locally.
// No dependencies, network calls, paid APIs or participant-level data archiving.
const fs = require('node:fs');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const [csvPath, rmdPath, experimentPath] = process.argv.slice(2);
if (!csvPath || !rmdPath || !experimentPath) {
  console.error('Usage: node e055_akata_pd_action_score_source_audit_20261028.js repgames.csv repeated_games.Rmd script.js');
  process.exit(2);
}
function read(path) { return fs.readFileSync(path); }
function blobSha(data) {
  const h = crypto.createHash('sha1');
  h.update(Buffer.from('blob ' + data.length + '\0'));
  h.update(data);
  return h.digest('hex');
}
const csvBytes = read(csvPath), rmdBytes = read(rmdPath), expBytes = read(experimentPath);
assert.equal(blobSha(csvBytes), '2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95');
assert.equal(blobSha(rmdBytes), 'ca9991b6d0917156672e1e2fea923548562d945e');
assert.equal(blobSha(expBytes), '4b7be85e8b3b964bfd0722d796f5ed6c2b8f0a19');
const rmd = rmdBytes.toString('utf8'), exp = expBytes.toString('utf8');
assert.ok(rmd.includes('dpd$cooperated<-ifelse(dpd$score==5, 1, 0)'));
const pdFn = exp.slice(exp.indexOf('function calculate_points_pd('), exp.indexOf('function startCountdown('));
assert.ok(pdFn.includes('playerChoice === 1 && opponentChoice === "J"'));
assert.ok(pdFn.includes('playerPoints = 8'));
assert.ok(pdFn.includes('playerChoice === 0 && opponentChoice === "F"'));
assert.ok(pdFn.includes('playerPoints = 5'));
const lines = csvBytes.toString('utf8').trim().split(/\r?\n/);
assert.equal(lines.shift(), 'id,game,action,score,opponent,guess,coordination');
const rows = lines.map((line) => {
  const a = line.split(',');
  assert.equal(a.length, 7);
  return {id:a[0],game:a[1],action:Number(a[2]),score:Number(a[3]),opponent:a[4]};
});
const pd = rows.filter(x => x.game === 'PD');
const bos = rows.filter(x => x.game === 'BoS');
const count = fn => pd.filter(fn).length;
const actionScore = {};
for (const x of pd) { const k = x.action + '|' + x.score; actionScore[k] = (actionScore[k] || 0) + 1; }
assert.equal(rows.length, 3900);
assert.equal(new Set(rows.map(x => x.id)).size, 195);
assert.equal(pd.length, 1950);
assert.equal(bos.length, 1950);
assert.deepEqual(actionScore, {'0|10':235,'1|0':213,'0|5':783,'1|8':718,'0|0':1});
assert.equal(count(x => x.action === 1), 931);
assert.equal(count(x => x.score === 5), 783);
assert.equal(count(x => x.action === 1 && x.score === 5), 0);
assert.equal(count(x => (x.action === 1) !== (x.score === 5)), 1714);
assert.equal(count(x => x.opponent === 'Base'), 970);
assert.equal(count(x => x.opponent === 'Prompted'), 980);
console.log(JSON.stringify({
  status:'PASS',rows:rows.length,participants:195,pd:pd.length,bos:bos.length,
  action1:931,score5:783,actionScore,disagreement:1714,
  conclusion:'Rmd score==5 is not the source-coded PD cooperation action'
},null,2));
