"use strict";
// Source-anchored control-flow model of Joplin RevisionService.collectRevisions()
// Pinned upstream 2e1310190489c5325dd69305bb762e887865c6c3.
// Isolated fault-injection model; original Joplin runtime was not executed.
async function collect(state, io) {
  if (state.isCollecting) return "SKIPPED";
  state.isCollecting = true;
  await io.waitForAllSaved(); // upstream line 133, before try
  try {
    for (const change of io.changes) {
      try {
        if (change.error) throw Object.assign(new Error("injected"), {code: change.error});
        io.saved.push(change.id);
      } catch (error) {
        if (error.code === "revision_encrypted") throw error;
        io.errors.push(change.id);
      }
      state.cursor = change.id; // upstream line 228
    }
  } catch (error) {
    if (error.code !== "revision_encrypted") io.errors.push("outer");
  }
  await io.saveAll(); // upstream line 244, after try
  await io.deleteProcessedChanges(); // upstream line 245, after try
  state.isCollecting = false; // upstream line 247, no finally
  return "DONE";
}
async function runTests() {
  const out = [];
  function fixture(failure, changes=[{id:1},{id:2},{id:3}]) {
    const state={isCollecting:false,cursor:0};
    const io={changes,saved:[],errors:[],
      waitForAllSaved:async()=>{if(failure==="wait")throw Error("injected wait failure");},
      saveAll:async()=>{if(failure==="save")throw Error("injected save failure");},
      deleteProcessedChanges:async()=>{if(failure==="delete")throw Error("injected cleanup failure");}};
    return {state,io};
  }
  function ok(x,label){if(!x)throw Error("FAIL "+label);out.push(label);}
  let x=fixture(null);
  ok(await collect(x.state,x.io)==="DONE" && !x.state.isCollecting && x.state.cursor===3,"baseline_clear");
  for(const stage of ["wait","save","delete"]){
    x=fixture(stage);let failed=false;
    try{await collect(x.state,x.io);}catch(e){failed=true;}
    ok(failed && x.state.isCollecting,stage+"_leaves_flag_true");
    ok(await collect(x.state,x.io)==="SKIPPED",stage+"_blocks_retry");
  }
  x=fixture(null,[{id:1},{id:2,error:"ordinary"},{id:3}]);
  ok(await collect(x.state,x.io)==="DONE" && x.state.cursor===3 && x.io.errors.join(",")==="2","generic_error_advances");
  x=fixture(null,[{id:1},{id:2,error:"revision_encrypted"},{id:3}]);
  ok(await collect(x.state,x.io)==="DONE" && x.state.cursor===1 && !x.state.isCollecting,"encrypted_error_pauses_and_clears");
  return {assertions:out.length,checks:out};
}
if(typeof module!=="undefined")module.exports={collect,runTests};
if(typeof require!=="undefined"&&require.main===module){runTests().then(x=>console.log(JSON.stringify(x))).catch(e=>{console.error(e);process.exitCode=1;});}
