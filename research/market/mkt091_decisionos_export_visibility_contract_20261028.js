#!/usr/bin/env node
/** MKT091 fixed-source and synthetic visibility audit. Node standard library only.
 * Usage: node mkt091_decisionos_export_visibility_contract_20261028.js /path/to/DecisionOS
 * Upstream checkout: af288e9f1e6c6c097e3eccd30f3b97a85ac22a69.
 */
const fs=require('node:fs'),path=require('node:path'),root=process.argv[2]||process.cwd();
const paths={export:'src/app/api/account/export/route.ts',versions:'src/app/api/decisions/[id]/versions/route.ts',update:'src/app/api/decisions/[id]/route.ts',tenant:'src/lib/tenant.ts',schema:'prisma/schema.prisma'};
const s=Object.fromEntries(Object.entries(paths).map(([k,p])=>[k,fs.readFileSync(path.join(root,p),'utf8')]));
let passed=0;
function check(ok,label){if(!ok)throw Error('FAIL '+label);passed++;}
check(s.export.includes('require: "auth"'),'auth');
check(s.export.includes('createdDecisions: true'),'created decisions');
check(s.export.includes('decisionVersions: true'),'version contributions');
check(s.export.includes('events: true'),'events');
check(s.export.includes('account: profile'),'account bundle');
check(!s.export.includes('decisionVisibilityWhere'),'no decision visibility filter');
check(!s.export.includes('visibleDecision'),'no row visibility predicate');
check(!s.export.includes('where: { changedById:'),'no explicit changedBy filter');
check(s.versions.includes('visibleDecision('),'versions visibility');
check(s.versions.includes('decisionVersion.findMany'),'versions query');
check(s.update.includes('snapshotJson: JSON.stringify(existing)'),'before snapshot');
check(s.update.includes('changedById: session.userId'),'editor provenance');
check(s.update.includes('data.visibility === "private"'),'private transition');
check(s.tenant.includes('row.visibility === "workspace" || row.createdByUserId === session.userId'),'visibility rule');
check(s.schema.includes('model DecisionVersion'),'model');
check(s.schema.includes('changedBy User'),'editor relation');
check(s.schema.includes('snapshotJson String'),'snapshot data');
const decision={createdByUserId:'author',workspaceId:'w',visibility:'private'},editor='editor';
const snapshot={title:'Past decision',rationale:'Past rationale',visibility:'workspace'};
const version={changedById:editor,decisionId:'d',snapshotJson:JSON.stringify(snapshot)};
const visible=decision.workspaceId==='w'&&(decision.visibility==='workspace'||decision.createdByUserId===editor);
const exported=[version].filter(v=>v.changedById===editor);
check(visible===false,'current version endpoint denies former editor');
check(exported.length===1,'contribution version in personal export');
check(JSON.parse(exported[0].snapshotJson).rationale===snapshot.rationale,'past rationale retained');
console.log(JSON.stringify({audit:'MKT091',evidence:'fixed source + synthetic',passed,failed:0}));
