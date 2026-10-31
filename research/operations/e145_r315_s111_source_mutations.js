function check(scoreSource,sourceText,receiptText) {
  const start=scoreSource.indexOf("const score=function score(data){");
  const end=scoreSource.indexOf("const root=path.resolve");
  if(start<0||end<=start)throw Error("unexpected scorer source");
  const score=Function(scoreSource.slice(start,end)+";return score;")();
  const source=JSON.parse(sourceText),receipt=JSON.parse(receiptText);
  const baseline=JSON.stringify(score(source));
  if(baseline!==JSON.stringify(receipt))throw Error("original receipt mismatch");
  const cases=[
    ["catalogue_id_change",x=>{x.original_catalogue_id="tampered_catalogue";},true],
    ["baseline_edges_change",x=>{x.parameter_worlds[0].baseline_edges="0-1";},true],
    ["baseline_clustering_change",x=>{x.parameter_worlds[0].baseline_clustering="999";},true],
    ["positive_path_action_change",x=>{x.parameter_worlds[0].complete_paths[0].first_action="invalid_action";},true],
    ["source_atom_count_change",x=>{x.source_atom_count=209;},false],
    ["source_scope_change",x=>{x.source_scope="FAKE_E2";},false],
    ["path_mass_change",x=>{x.parameter_worlds[0].complete_paths[0].probability="0";},false]
  ];
  const results=[];
  for(const [name,mutate,shouldAccept] of cases){
    const altered=JSON.parse(sourceText);mutate(altered);
    let accepted=false,unchanged=false;
    try{const output=score(altered);accepted=true;unchanged=JSON.stringify(output)===baseline;}catch(e){}
    if(accepted!==shouldAccept||(accepted&&!unchanged))throw Error("unexpected mutation result "+name);
    results.push({name,accepted,receipt_unchanged:unchanged});
  }
  return {original:"PASS",mutations:results,unexpected:0,accepted_unchanged:4,rejected:3};
}

if(require.main===module){
  const fs=require("node:fs"),path=require("node:path");
  const root=path.resolve(__dirname,"../..");
  const score=fs.readFileSync(path.join(root,"research/validation/r315_s111_three_p_exact.js"),"utf8");
  const source=fs.readFileSync(path.join(root,"research/R315/R315_EXACT_180_TWO_EVENT_GRAPH_PATHS.json"),"utf8");
  const receipt=fs.readFileSync(path.join(root,"research/validation/R315_S111_THREE_P_CLASSIFICATION_EXACT.json"),"utf8");
  process.stdout.write(JSON.stringify(check(score,source,receipt),null,2)+"\n");
}
module.exports={check};
