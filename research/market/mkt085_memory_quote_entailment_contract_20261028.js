#!/usr/bin/env node
'use strict';
// Zero-dependency, bounded source-contract check. It does not execute the full Electron app.
// Usage: node mkt085_memory_quote_entailment_contract_20261028.js validate.ts store.ts context.ts validate.test.ts README.md
const fs = require('node:fs');
const assert = require('node:assert/strict');
if (process.argv.length !== 7) {
  console.error('Usage: node script.js validate.ts store.ts context.ts validate.test.ts README.md');
  process.exit(2);
}
const [validate, store, context, tests, readme] = process.argv.slice(2).map(p => fs.readFileSync(p, 'utf8'));
let checks = 0;
function check(v, label) { checks++; assert.ok(v, label); }
check(validate.includes('if (normalizeForMatch(value).includes(needle)) return field'), 'excerpt substring check');
check(validate.includes('if (excerpt.length < MIN_EXCERPT_CHARS)'), 'minimum quote length');
check(validate.includes('if (!field)'), 'quote missing rejection');
check(validate.includes("kind !== 'explicit' && kind !== 'self-described' && kind !== 'tentative'"), 'kind enum');
check(validate.includes('const field = locateExcerpt(fields, excerpt)'), 'field located from source');
check(validate.includes('accepted.push({'), 'accepted proposals');
check(store.includes("return kind === 'tentative' ? 'pending' : 'approved'"), 'auto approval');
check(store.includes('state: initialStateFor(p.kind)'), 'insert uses state');
check(context.includes("listItems(db, ['approved'])"), 'approved items rendered');
check(tests.includes("expect(initialStateFor('explicit')).toBe('approved')"), 'upstream regression test');
check(readme.includes('nothing is used until you approve it'), 'readme wording');
const norm = x => x.toLowerCase().replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim();
const fields = { situation: 'I do not want to quit my job now.' };
const excerpt = 'do not want to quit my job now';
const statement = 'I want to quit my job now.';
const locate = (f,e) => Object.entries(f).find(([,v]) => norm(v).includes(norm(e)))?.[0] ?? null;
check(locate(fields,excerpt) === 'situation', 'quote exists');
check(excerpt.length >= 8, 'quote length');
check(statement !== fields.situation, 'different statement');
check(statement.includes('want to quit') && fields.situation.includes('not want to quit'), 'negation reversal');
check(('explicit' === 'tentative' ? 'pending' : 'approved') === 'approved', 'auto approved');
check(!norm(fields.situation).includes(norm(statement)), 'unsupported claim');
console.log(JSON.stringify({checks, failures:0, scope:'source fragments plus synthetic logical counterexample', approved_without_entailment:true}));
