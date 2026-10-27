#!/usr/bin/env node
"use strict";
// Run: node research/market/mkt089_decisionos_export_scope_20261028.js /path/to/DecisionOS
// Fixed upstream revision: af288e9f1e6c6c097e3eccd30f3b97a85ac22a69
const fs = require("node:fs");
const path = require("node:path");
const root = process.argv[2] || ".";
const paths = [
  "src/app/api/decisions/export/route.ts",
  "src/lib/decision-export.ts",
  "src/app/api/account/export/route.ts",
  "src/app/api/decisions/[id]/route.ts",
  "src/app/api/decisions/[id]/versions/route.ts",
  "prisma/schema.prisma",
];
const s = paths.map(p => fs.readFileSync(path.join(root,p),"utf8"));
const tests = [
  ["model_version", /model DecisionVersion \{/.test(s[5])],
  ["model_relations", /model DecisionRelation \{/.test(s[5])],
  ["model_notes", /model DecisionNote \{/.test(s[5])],
  ["version_snapshot_write", /decisionVersion\.create\(/.test(s[3])],
  ["version_endpoint_read", /decisionVersion\.findMany\(/.test(s[4])],
  ["workspace_export_only_current", /prisma\.decision\.findMany/.test(s[0]) && !/versions\s*:/.test(s[0])],
  ["workspace_export_reviews", /reviews:\s*\{/.test(s[0])],
  ["workspace_export_links", /links:\s*\{/.test(s[0])],
  ["serializer_versionless", !/versions\s*:/.test(s[1]) && !/snapshotJson/.test(s[1])],
  ["serializer_relations_missing", !/relationsFrom|relationsTo/.test(s[1])],
  ["serializer_notes_missing", !/notes\s*:/.test(s[1])],
  ["personal_export_versions", /decisionVersions:\s*true/.test(s[2])],
  ["personal_export_scoped_by_author", /where:\s*\{\s*id:\s*session\.userId\s*\}/.test(s[2])],
  ["personal_export_no_all_workspace", !/prisma\.decision\.findMany/.test(s[2])],
  ["workspace_export_visibility", /decisionVisibilityWhere\(session\)/.test(s[0])],
  ["workspace_export_versioned_envelope", /EXPORT_SCHEMA_VERSION\s*=\s*1/.test(s[1])],
];
const failed = tests.filter(x=>!x[1]).map(x=>x[0]);
console.log(JSON.stringify({checks:tests.length,passed:tests.length-failed.length,failed},null,2));
if(failed.length) process.exitCode=1;
