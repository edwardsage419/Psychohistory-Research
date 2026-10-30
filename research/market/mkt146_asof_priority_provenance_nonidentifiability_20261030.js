"use strict";
function assert(ok, message) { if (!ok) throw Error(message); }
function fail(fn) { try { fn(); } catch (_) { return true; } return false; }
function aggregate(rows, priority) {
  if (!Array.isArray(rows) || rows.length === 0) throw Error("rows required");
  if (!["A","B"].includes(priority)) throw Error("invalid priority");
  const cells = new Map();
  for (const r of rows) {
    if (!["A","B"].includes(r.origin) || !Number.isInteger(r.start) ||
        !Number.isInteger(r.end) || r.end <= r.start || r.start < 0 ||
        !Number.isSafeInteger(r.rate) || r.rate < 0) throw Error("bad row");
    for (let t = r.start; t < r.end; t++) {
      const key = String(t);
      if (!cells.has(key)) cells.set(key, {});
      const slot = cells.get(key);
      if (Object.prototype.hasOwnProperty.call(slot, r.origin)) throw Error("duplicate origin-minute");
      slot[r.origin] = r.rate;
    }
  }
  let total = 0;
  for (const slot of cells.values()) {
    total += slot[priority] === undefined ? slot[priority === "A" ? "B" : "A"] : slot[priority];
  }
  return total;
}
function asOf(rows, metadata) {
  const required = ["snapshot_id","priority","priority_version","data_version","permission_complete","window"];
  if (!metadata || required.some(k => metadata[k] === undefined || metadata[k] === null))
    return {status:"ABSTAIN",reason:"missing provenance"};
  if (metadata.permission_complete !== true)
    return {status:"ABSTAIN",reason:"incomplete permissions"};
  if (metadata.window !== "0:20")
    return {status:"ABSTAIN",reason:"window mismatch"};
  return {status:"OK",value:aggregate(rows,metadata.priority)};
}
function run() {
  let tests=0;
  const check=(ok,msg)=>{assert(ok,msg);tests++;};
  const world1=[{origin:"A",start:0,end:10,rate:100},{origin:"A",start:10,end:20,rate:50},{origin:"B",start:0,end:10,rate:80}];
  const world2=[{origin:"A",start:0,end:10,rate:200},{origin:"A",start:10,end:20,rate:50},{origin:"B",start:0,end:10,rate:80}];
  const md={snapshot_id:"s1",priority:"A",priority_version:"p1",data_version:"d1",permission_complete:true,window:"0:20"};
  check(aggregate(world1,"A")===1500,"A priority world1");
  check(aggregate(world1,"B")===1300,"B priority world1");
  check(aggregate(world2,"B")===1300,"same visible current aggregate");
  check(aggregate(world2,"A")===2500,"different historical aggregate");
  check(aggregate(world1,"A")-aggregate(world1,"B")===200,"priority difference");
  check(aggregate(world2,"A")-aggregate(world2,"B")===1200,"hidden difference");
  check(asOf(world1,md).status==="OK","complete provenance");
  check(asOf(world1,md).value===1500,"historical snapshot value");
  check(asOf(world1,{...md,priority:"B",priority_version:"p2"}).value===1300,"changed priority");
  check(asOf(world1,{...md,priority_version:undefined}).status==="ABSTAIN","missing version");
  check(asOf(world1,{...md,snapshot_id:undefined}).status==="ABSTAIN","missing snapshot");
  check(asOf(world1,{...md,data_version:null}).status==="ABSTAIN","missing data version");
  check(asOf(world1,{...md,permission_complete:false}).status==="ABSTAIN","partial permissions");
  check(asOf(world1,{...md,window:"10:20"}).status==="ABSTAIN","window mismatch");
  check(fail(()=>aggregate(world1,"C")),"invalid priority");
  check(fail(()=>aggregate([], "A")),"empty rows");
  check(fail(()=>aggregate([{origin:"A",start:1,end:1,rate:1}],"A")),"bad time");
  check(fail(()=>aggregate([{origin:"A",start:0,end:1,rate:-1}],"A")),"bad rate");
  check(fail(()=>aggregate([{origin:"A",start:0,end:1,rate:1},{origin:"A",start:0,end:1,rate:2}],"A")),"duplicate");
  check(fail(()=>aggregate([{origin:"X",start:0,end:1,rate:1}],"A")),"unknown origin");
  return {tests, world1_A:1500,world1_B:1300,world2_A:2500,world2_B:1300,interpretation:"same current B total, different earlier A totals"};
}
if (typeof module !== "undefined") module.exports={aggregate,asOf,run};
if (typeof require !== "undefined" && typeof module !== "undefined" && require.main===module) console.log(JSON.stringify(run()));
