#!/usr/bin/env node
'use strict';
// E146: complementary compensating source-mass mutation for R316 S112.
// This is nonblind function-level E1. The original CLI's Git-blob gate remains intact.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT=path.resolve(__dirname,'../..');
const SOURCE=path.join(ROOT,'research/R316/R316_EXACT_128_GRAPH_LIKELIHOODS.json');
const RECEIPT=path.join(ROOT,'research/validation/R316_S112_OBSERVATION_COARSENING_EXACT.json');
const {score}=require('../validation/r316_s112_observation_coarsening.js');
const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
const raw=fs.readFileSync(SOURCE);
const sha=crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+raw.length+'\0'),raw])).digest('hex');
assert(sha==='36da587adbc6e1d92824a5fd39516e506569166c','original source blob');
const source=JSON.parse(raw),receipt=JSON.parse(fs.readFileSync(RECEIPT,'utf8'));
assert(JSON.stringify(score(source))===JSON.stringify(receipt),'baseline');
const changed=JSON.parse(JSON.stringify(source));
const graphs=changed.regimes[0].complete_graphs;
const a=graphs.find(g=>g.mask===3),b=graphs.find(g=>g.mask===5);
assert(a.probability==='81/4096'&&b.probability==='81/4096','baseline likelihoods');
a.probability='82/4096';b.probability='80/4096';
assert(JSON.stringify(score(changed))===JSON.stringify(receipt),'compensating mutation should expose function blind spot');
const expected=(g,regime)=>String(3**(regime==='A'?g.within_edges+4-g.cross_edges:2-g.within_edges+g.cross_edges))+'/4096';
const wrong=changed.regimes[0].complete_graphs.filter(g=>g.probability!==expected(g,'A')).map(g=>g.mask);
assert(JSON.stringify(wrong)==='[3,5]','independent Bernoulli source oracle catches both');
const mutatedBytes=Buffer.from(JSON.stringify(changed));
const mutSha=crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+mutatedBytes.length+'\0'),mutatedBytes])).digest('hex');
assert(mutSha!==sha,'original CLI Git-blob gate would reject altered bytes');
console.log(JSON.stringify({status:'PASS',original_blob:sha,original_receipt_unchanged:true,compensating_masks:[3,5],mutated_likelihoods:['82/4096','80/4096'],source_formula_rejects:2,original_CLI_blob_guard_would_reject:true,evidence:'NONBLIND_INTERNAL_E1',E2:0,E3:0}));
