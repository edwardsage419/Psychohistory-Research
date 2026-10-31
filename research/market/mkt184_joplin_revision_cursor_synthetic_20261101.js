"use strict";
// Bounded state-machine illustration of Joplin's pinned RevisionService.ts cursor behavior.
// This is a model of documented source branches, not execution of Joplin itself.
function collect(changes, cursor, failedId, encryptedFailure) {
  const created=[], skipped=[];
  for (const change of changes.filter(x=>x>cursor).sort((a,b)=>a-b)) {
    if (change===failedId) {
      if (encryptedFailure) break; // special encrypted exception stops the loop before advancing cursor
      skipped.push(change); // generic creation error is logged, then processing advances
    } else created.push(change);
    cursor=change;
  }
  return {cursor,created,skipped};
}
function run() {
  const check=(v,m)=>{if(!v)throw Error(m);};
  const events=[1,2,3];
  const ordinary=collect(events,0,2,false);
  check(ordinary.cursor===3,"ordinary cursor");
  check(ordinary.created.join(",")==="1,3","ordinary created");
  check(ordinary.skipped.join(",")==="2","ordinary skip");
  const later=collect(events,ordinary.cursor,null,false);
  check(later.created.length===0,"generic failure not retried");
  const encrypted=collect(events,0,2,true);
  check(encrypted.cursor===1,"encrypted failure stops before advance");
  const recovered=collect(events,encrypted.cursor,null,false);
  check(recovered.created.join(",")==="2,3","encrypted retry");
  const disabledCursor=Math.max(...events);
  check(collect(events,disabledCursor,null,false).created.length===0,"disabled mode skips pending");
  return {checks:7,ordinary,ordinary_retry:later,encrypted_first:encrypted,encrypted_retry:recovered,disabled_cursor:disabledCursor};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
