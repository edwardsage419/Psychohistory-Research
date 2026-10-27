"use strict";
// Source-only audit, no participant-level data. Five pinned author MATLAB files.
function audit(f){
 const multi=f.defStudy.split("if multi_num == 1")[1].split("elseif multi_num == 0")[0];
 if(!/study\.trials\s*=\s*3\s*;/.test(multi))throw Error("repeats changed");
 const pom=multi.match(/study\.POM\.val\s*=\s*\{([\s\S]*?)\};/);
 if(!pom)throw Error("POM missing");
 const count=(pom[1].match(/\[/g)||[]).length;
 if(count!==20)throw Error("POM count changed");
 const match=f.defStudy.match(/study\.combos\s*=\s*\[([\s\S]*?)\];/);
 if(!match)throw Error("combos missing");
 const rows=match[1].split(";").map(v=>(v.match(/\d+/g)||[]).map(Number)).filter(x=>x.length);
 if(rows.length!==5||rows.some(r=>r.length!==6||new Set(r).size!==6||r.some(n=>n<1||n>6)))throw Error("combos invalid");
 const pairs=new Map();for(let r of rows)for(let i=0;i<6;i+=2){let k=[r[i],r[i+1]].sort((a,b)=>a-b).join(":");pairs.set(k,(pairs.get(k)||0)+1);}
 if(pairs.size!==15||[...pairs.values()].some(n=>n!==1))throw Error("pairing factorization changed");
 if(!/for i = 1:length\(study\.POM\.val\)/.test(f.playTheGame)||!/for trials_POM_loop = 1:study\.trials/.test(f.playTheGame))throw Error("loop changed");
 if(!/data\.values\(trials_loop,col\.IDother\)\s*=\s*participant\.other/.test(f.playTheGame))throw Error("opponent field changed");
 if(!/study\.combosOrder\s*=\s*input/.test(f.defBasics))throw Error("manual order changed");
 if(!/data\.Exp_1\(:,4\)\s*=\s*NaN/.test(f.formatData))throw Error("Exp1 ID changed");
 let resets=[...f.formatData.matchAll(/mod\(iRow - 1,\s*300\)\s*==\s*0/g)].length;
 if(resets!==4)throw Error("four lag resets changed");
 if(!/exclude_manually\s*=\s*\[135,\s*231,\s*255,\s*246\]/.test(f.exclude))throw Error("duplicate exclusions changed");
 return {audit:"A_KUPER_2023_PAIRING_SOURCE_STATIC_GATE",designed_POMs_per_block:count,repeats_per_POM:3,
  designed_trials_per_block:60,designed_blocks:5,designed_global_trials:300,
  unique_six_person_matching_patterns:rows.length,distinct_unordered_partner_pairs:pairs.size,
  all_15_pairs_once_in_design:true,actual_block_order:"UNKNOWN_MANUAL_INPUT",
  experiment_1_opponent_ID:"MISSING_IN_FORMAT_SCRIPT",previous_action_lag_resets_at_300_only:true,
  documented_cross_experiment_duplicate_exclusions:[135,231,255,246],
  actual_CSV_row_recount_this_audit:false,R073_original_frozen_direct_transfer:"BLOCKED",new_E2_scores:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),crypto=require("crypto"),names=["defStudy","playTheGame","defBasics","formatData","exclude"];
 const sha=["1bc7f0ab4b3c83136db277475aa85c7840b403a","c985af146613aef8bfc9d0563fe0f1f5554e1376","356666d810d212afb86f6e22faf426f3ca53b976","6965e66ac05ec67b519f0674a708fcdcef917785","0188f3d6f7d7c3a803c9a6a8f95ef83af0355e27"];
 if(process.argv.length!==7)throw Error("usage: node script.js defStudy.m playTheGame.m defBasics.m format_data.m exclude.m");
 let files={};for(let i=0;i<5;i++){let buf=fs.readFileSync(process.argv[i+2]),actual=crypto.createHash("sha1").update("blob "+buf.length+"\0").update(buf).digest("hex");
 if(actual!==sha[i])throw Error("author source Git blob SHA mismatch "+names[i]);files[names[i]]=buf.toString("utf8");}
 process.stdout.write(JSON.stringify(audit(files),null,2)+"\n");
}