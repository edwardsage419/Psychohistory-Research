#!/usr/bin/env node
'use strict';
// Artificial daily boolean-habit experiments using the pinned Loop Score.compute formula.
const assert = require('node:assert/strict');
function compute(freq, previous, value) {
  const m = Math.pow(0.5, Math.sqrt(freq) / 13.0);
  return previous * m + value * (1 - m);
}
function replay(events, freq=1) {
  let s = 0;
  const scores = [];
  for (const e of events) {
    if (e !== 'SKIP') s = compute(freq, s, e);
    scores.push(s);
  }
  return scores;
}
const early = replay([...Array(7).fill(1), ...Array(7).fill(0)]);
const late = replay([...Array(7).fill(0), ...Array(7).fill(1)]);
const first13 = replay(Array(13).fill(1)).at(-1);
const skipped = replay([...Array(13).fill(1), 'SKIP']).at(-1);
const missed = replay([...Array(13).fill(1), 0]).at(-1);
const completed = replay([...Array(13).fill(1), 1]).at(-1);
const multiplier = Math.pow(0.5, 1 / 13);
assert(Math.abs(first13 - 0.5) < 1e-12);
assert(Math.abs(skipped - first13) < 1e-12);
assert(missed < skipped && skipped < completed);
assert(early.at(-1) < late.at(-1));
assert(Math.abs(replay(Array(13).fill(0), 1).at(-1)) < 1e-12);
assert(Math.abs(replay(Array(13).fill(1), 1).at(-1) - .5) < 1e-12);
assert(Math.abs(replay(Array(13).fill(1), 3/7).at(-1) - (1-Math.pow(.5,Math.sqrt(3/7)))) < 1e-12);
const edited = replay([...Array(6).fill(1), 0, ...Array(7).fill(0)]).at(-1);
assert(edited < early.at(-1));
console.log(JSON.stringify({pinned_formula:'m=0.5^(sqrt(frequency)/13); score=m*previous+(1-m)*checkmark',
 multiplier,day13:first13,day14_skip:skipped,day14_miss:missed,day14_complete:completed,
 seven_yes_then_seven_no:early.at(-1),seven_no_then_seven_yes:late.at(-1),
 after_historical_edit:edited,assertions:8,evidence:'internal nonblind artificial; daily boolean simplification'},null,2));
