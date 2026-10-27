#!/usr/bin/env node
"use strict";
// Fetch the three upstream files from fixed commit af288e9f1e6c6c097e3eccd30f3b97a85ac22a69 before running.
// Usage: node mkt090_decisionos_history_20261028.js history_page.tsx versions_route.ts schema.prisma
const fs=require("fs");
function auditHistory(source, versionRoute, schema) {
 let checks=0;const check=(v,m)=>{checks++;if(!v)throw Error(m)};
 check(source.includes('orderBy: { versionNum: "desc" }'),"descending history");
 check(source.includes("const nextVersion = decision.versions[idx - 1];"),"predecessor used");
 check(source.includes("let nextSnap: Record<string, unknown> = {};"),"empty next");
 check(source.includes("if (nextVersion) {"),"conditional next");
 check(source.includes("after={nextSnap[field] != null ? String(nextSnap[field]) : null}"),"render after");
 check(source.includes("const changedFields = Object.keys(FIELD_LABELS).filter("),"field list");
 check(versionRoute.includes("export const GET = withApi"),"version GET");
 check(!versionRoute.includes("export const POST"),"no restore POST");
 check(schema.includes("model DecisionVersion {")&&schema.includes("snapshotJson String"),"snapshots");
 const display=(snapshots,idx,field)=>{const snap=snapshots[idx],nextVersion=snapshots[idx-1];const nextSnap=nextVersion??{};return {before:snap[field]!=null?String(snap[field]):null,after:nextSnap[field]!=null?String(nextSnap[field]):null}};
 const fields=["title","summary","rationale","assumptions","risks","chosenOption"];
 for(const n of [1,2,3,4]){
  const snapshots=Array.from({length:n},(_,i)=>Object.fromEntries(fields.map(f=>[f,f+"-before-"+(n-i)])));
  const current=Object.fromEntries(fields.map(f=>[f,f+"-current"]));
  for(const f of fields){const got=display(snapshots,0,f);check(got.after===null,"newest after should be empty in source "+n+" "+f);check(current[f]!==got.after,"current mismatch "+n+" "+f)}
  if(n>=2){for(const f of fields){const got=display(snapshots,1,f);check(got.after===snapshots[0][f],"older version next snapshot "+n+" "+f)}}
 }
 return {checks,failures:0,latest_edit_after_values_missing:24,older_edit_after_controls:18,scope:"fixed_source_contract_and_synthetic_only"};
}
if(require.main===module){
 if(process.argv.length!==5)throw Error("Provide fixed history page, versions route and schema files");
 const out=auditHistory(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8")));
 process.stdout.write(JSON.stringify(out,null,2)+"\n");
}
