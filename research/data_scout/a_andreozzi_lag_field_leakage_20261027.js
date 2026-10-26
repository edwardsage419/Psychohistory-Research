"use strict";
// A public human-data leakage gate. Read-only: no individual-level rows are exported.
const EXPECTED_BLOB="bd4c1550002621bee7dfb50e0d15d317764d1ea9";
function parseCSV(content){
 let records=[],record=[],value="",quoted=false;
 for(let i=0;i<content.length;i++){
  const c=content[i];
  if(c==='"'){if(quoted&&content[i+1]==='"'){value+='"';i++}else quoted=!quoted}
  else if(c===','&&!quoted){record.push(value);value=""}
  else if((c==='\n'||c==='\r')&&!quoted){
   if(c==='\r'&&content[i+1]==='\n')i++;
   record.push(value);value="";if(record.length>1)records.push(record);record=[];
  }else value+=c;
 }
 if(quoted)throw Error("unclosed quote");
 if(value.length||record.length){record.push(value);records.push(record)}
 return records;
}
function analyze(content){
 const records=parseCSV(content),headers=records.shift();
 const pos=Object.fromEntries(headers.map((s,i)=>[s,i]));
 const fields=["subject_unq","session","subject","period","opp_cond_class_wide_o","opp_cond_class_wide_o_lag1","opp_cond_class_narrow","opp_cond_class_narrow_lag1","opp_cond_class_wide","opp_cond_class_wide_lag1"];
 for(const f of fields)if(pos[f]===undefined)throw Error("missing "+f);
 const people=new Map();
 for(const row of records){if(row.length!==headers.length)throw Error("CSV width");const id=row[pos.subject_unq];if(!people.has(id))people.set(id,[]);people.get(id).push(row)}
 const out={rows:records.length,columns:headers.length,subjects:people.size,period1:0,history_rows:0,wide_o_lag_matches_current:0,wide_o_lag_matches_previous:0,wide_o_lag_mismatch_previous:0,narrow_lag_matches_current:0,narrow_lag_matches_previous:0,narrow_lag_mismatch_previous:0,wide_lag_matches_previous:0,wide_lag_mismatch_previous:0,first_period_bad_lag_values:0,negative_controls_rejected:0};
 for(const records of people.values()){
  records.sort((a,b)=>Number(a[pos.period])-Number(b[pos.period]));
  for(let i=0;i<records.length;i++){
   const now=records[i],period=Number(now[pos.period]);
   if(period!==i+1)throw Error("noncontiguous subject periods");
   if(period===1){out.period1++;for(const f of ["opp_cond_class_wide_o_lag1","opp_cond_class_narrow_lag1","opp_cond_class_wide_lag1"])if(now[pos[f]]!=="NA")out.first_period_bad_lag_values++;continue}
   out.history_rows++;const prev=records[i-1];
   for(const [prefix,lag,base] of [["wide_o","opp_cond_class_wide_o_lag1","opp_cond_class_wide_o"],["narrow","opp_cond_class_narrow_lag1","opp_cond_class_narrow"],["wide","opp_cond_class_wide_lag1","opp_cond_class_wide"]]){
    if(out[prefix+"_lag_matches_current"]!==undefined&&now[pos[lag]]===now[pos[base]])out[prefix+"_lag_matches_current"]++;
    if(now[pos[lag]]===prev[pos[base]])out[prefix+"_lag_matches_previous"]++;
    else out[prefix+"_lag_mismatch_previous"]++;
   }
  }
 }
 if(out.rows!==1340||out.columns!==67||out.subjects!==134||out.history_rows!==1206||out.first_period_bad_lag_values!==0)throw Error("unexpected dataset structure");
 if(out.wide_o_lag_matches_current!==1206||out.narrow_lag_matches_current!==1206||out.wide_lag_mismatch_previous!==0)throw Error("source/lag relationship changed");
 if(out.wide_o_lag_mismatch_previous>0)out.negative_controls_rejected++;
 if(out.narrow_lag_mismatch_previous>0)out.negative_controls_rejected++;
 if(out.negative_controls_rejected!==2)throw Error("negative controls failed");
 return {source:"seyhunsaral/stabilitycondcoop",source_commit:"979abf87b5d3cfb7aa8be13b81ef233076c3bb75",source_csv_git_blob_sha1:EXPECTED_BLOB,...out,status:"TWO_MISLAGGED_CURRENT_PERIOD_CLASSIFICATION_FIELDS_CONFIRMED",human_model_scores_run:0,R073_direct_transfer:"BLOCKED",new_E2:0,new_E3:0};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs"),crypto=require("crypto");
 if(process.argv.length!==3)throw Error("usage: node a_andreozzi_lag_gate.js subjects.csv");
 const bytes=fs.readFileSync(process.argv[2]);
 const git=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+bytes.length+"\0"),bytes])).digest("hex");
 if(git!==EXPECTED_BLOB)throw Error("source git blob identity mismatch");
 console.log(JSON.stringify(analyze(bytes.toString("utf8")),null,2));
}
