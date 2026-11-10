"use strict";
// New Codex B invocation adapter. Original S96 files expose modules, not CLIs.
// No numerical implementation lives here; this calls their original exports.
const fs=require("fs"),path=require("path");
const [mode,source,first,second]=process.argv.slice(2);
if(mode==="emit"){
 const original=require(source);if(typeof original.run!=="function")throw Error("missing original run export");
 const out=original.run();if(typeof out.csv!=="string"||typeof out.json!=="string"||out.rows.length!==288||out.groups.length!==18)throw Error("original export shape");
 fs.mkdirSync(first,{recursive:true});
 fs.writeFileSync(path.join(first,"R300_S96_ALL_288_MISSPECIFIED_HMM_PREFIX_SOURCES.csv"),out.csv);
 fs.writeFileSync(path.join(first,"R300_S96_EXACT_MISSPECIFICATION_BRIER_RESULTS.json"),out.json);
 console.log(JSON.stringify({adapter:"NEW_CODEX_B_CALLS_ORIGINAL_EXPORT",rows:out.rows.length,groups:out.groups.length}));
}else if(mode==="audit"){
 const original=require(source);if(typeof original.audit!=="function")throw Error("missing original audit export");
 const out=original.audit(fs.readFileSync(first,"utf8"),JSON.parse(fs.readFileSync(second,"utf8")));
 console.log(JSON.stringify(out));
}else throw Error("mode must be emit or audit");
