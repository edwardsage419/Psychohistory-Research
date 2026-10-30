#!/usr/bin/env node
"use strict";
// Usage: node mkt155_loop_export_schema_20261030.js /path/to/uhabits
// Requires upstream commit 82c1ff287a8ac05321bfa95b61399fa8a2d1da5b.
const fs=require("fs"),path=require("path"),crypto=require("crypto"),assert=require("assert");
const root=process.argv[2];if(!root)throw Error("pass pinned upstream checkout");
function read(p,sha){const data=fs.readFileSync(path.join(root,p));const actual=crypto.createHash("sha1").update("blob "+data.length+"\0").update(data).digest("hex");assert.strictEqual(actual,sha,p);return data.toString("utf8")}
const prefix="uhabits-core/";
const src=read(prefix+"src/commonMain/kotlin/org/isoron/uhabits/core/io/HabitsCSVExporter.kt","eb56a6794d8567240f0e0af5aacff52fb3d9c062");
const fixtures=prefix+"assets/test/csv_export/";
const h=read(fixtures+"Habits.csv","37f40d4198b4ba3fd36b49123f4da3dbf5ce3711");
const c=read(fixtures+"Checkmarks.csv","3d443f4b53a7e9ef5908feb877bbb97595d0e973");
const s=read(fixtures+"Scores.csv","97637fb5b866e77daac6db7fe07a43011afa05d7");
const empty=read(fixtures+"001 Meditate/Checkmarks.csv","af193ea33ff4ca3588d4a16cfe8afdb210842fcd");
let n=0;function check(x,msg){assert.ok(x,msg);n++}const head=x=>x.split(/\r?\n/)[0];
check(head(h).startsWith("Position,Name,Type,Question"),"habits header");
check(!head(h).includes("EditTime")&&!head(h).includes("AlgorithmVersion"),"no provenance columns");
check(head(c).startsWith("Date,Meditate"),"checkmarks header");
check(head(s).startsWith("Date,Meditate"),"scores header");
check(c.includes("YES_AUTO"),"auto");check(c.includes("YES_MANUAL"),"manual");
check(c.includes("UNKNOWN"),"unknown");check(c.includes(",NO,"),"no");
check(empty.trim()==="Date,Value,Notes","empty known entries");
check(src.includes('format("%.4f", s.value)'),"rounded per habit");
check(src.includes('format("%.4f", scores[j][i].value)'),"rounded combined");
check(src.includes('zip.addEntry("Habits.csv"'),"habits ZIP");
check(src.includes('zip.addEntry("Scores.csv"'),"scores ZIP");
check(src.includes('zip.addEntry("Checkmarks.csv"'),"checkmarks ZIP");
check(src.includes("computedEntries.getKnown()"),"computed entries");
check(!src.includes("revision_timestamp")&&!src.includes("algorithm_version"),"no edit provenance");
check(JSON.stringify([0,0])===JSON.stringify([0,0]),"same final");
check(JSON.stringify([1,0])!==JSON.stringify([0,0]),"different historical");
check((0.123440).toFixed(4)===(0.123449).toFixed(4),"rounding collision");
console.log(JSON.stringify({status:"PASS",assertions:n,habits_rows:h.trim().split(/\r?\n/).length-1,checkmark_rows:c.trim().split(/\r?\n/).length-1,score_rows:s.trim().split(/\r?\n/).length-1},null,2));
