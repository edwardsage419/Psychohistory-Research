#!/usr/bin/env node
"use strict";
// Run: node research/validation/r224_s20_standalone_node_replay_20261028.js
// Requires Node.js with BigInt, no external packages or network.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const vm = require("node:vm");
const root = path.resolve(__dirname, "../..");
const read = rel => fs.readFileSync(path.join(root, rel), "utf8");
const csv = read("research/R224/R224_ALL_4096_ORIGINAL_NEGATIVE_CONTROL_SOURCE_ATOMS.csv");
const sha256 = crypto.createHash("sha256").update(Buffer.from(csv, "utf8")).digest("hex");
const expectedSourceSha = "cdbc43e01c115c20e551fa0088fed47962ac0b5547c8d4b74e4f257f16772f38";
if (sha256 !== expectedSourceSha) throw new Error("Original R224 source SHA256 mismatch");
const baseline = JSON.parse(read("research/R224/R224_EXACT_RESULTS.json"));
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(read("research/validation/r224_s20_negative_control_measurement_exact_20261028.js"), sandbox);
vm.runInContext(read("research/evidence_audit/b_r224_s20_joint_matrix_independent_20261028.js"), sandbox);
const actualR = sandbox.runR(csv, baseline);
const actualB = sandbox.runB(csv, baseline, actualR);
const expectedR = JSON.parse(read("research/validation/R224_S20_40_CONDITION_EXACT_RECEIPT_2026-10-28.json"));
const expectedB = JSON.parse(read("research/evidence_audit/B_R224_S20_MATRIX_INDEPENDENT_AUDIT_RECEIPT_2026-10-28.json"));
const equal = (a,b) => JSON.stringify(a) === JSON.stringify(b);
if (!equal(actualR,expectedR)) throw new Error("R receipt mismatch");
if (!equal(actualB,expectedB)) throw new Error("B receipt mismatch");
if (actualB.exact_field_comparisons !== 320 || actualB.additional_assertions !== 184 ||
    actualB.failures !== 0 || actualB.mutation_detected !== 2) {
  throw new Error("Independent audit check count mismatch");
}
process.stdout.write(JSON.stringify({
  status:"PASS",original_source_sha256:sha256,conditions:actualR.conditions,
  source_slots:actualR.source_slots,exact_field_comparisons:actualB.exact_field_comparisons,
  additional_assertions:actualB.additional_assertions,mutation_detected:actualB.mutation_detected,
  new_E2:0,new_E3:0
},null,2)+"\n");
