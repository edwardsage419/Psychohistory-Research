"use strict";
// E062: independent source-level verification of selected R231 S27 tetrad cases.
// Node.js standard library only. No network calls and no personal data.
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const root = path.resolve(__dirname, "../..");
const sourcePath = path.join(root, "research/R231/R231_ALL_512_ORIGINAL_CFA_STRUCTURAL_ATOMS.csv");
const receiptPath = path.join(root, "research/validation/R231_S27_FINITE_SAMPLE_TETRAD_RECEIPT_2026-10-28.json");
function gitBlob(buffer) {
  return crypto.createHash("sha1").update(Buffer.from("blob " + buffer.length + "\0")).update(buffer).digest("hex");
}
const raw = fs.readFileSync(sourcePath), receiptRaw = fs.readFileSync(receiptPath);
const expectedSource = "f56003f4b18f1dfcbdcd00aabc22fa0815205b64";
const expectedReceipt = "e9e436d837832763a77586adc7616f7c82e9b45d";
if (gitBlob(raw) !== expectedSource || gitBlob(receiptRaw) !== expectedReceipt) throw Error("SOURCE_IDENTITY_CHANGED");
const lines = raw.toString("utf8").trim().split(/\r?\n/), header = lines.shift().split(",");
const xi = [1, 2, 3, 4].map(i => header.indexOf("observed_X" + i));
const wi = header.indexOf("world"), pi = header.indexOf("original_probability");
if ([wi, pi, ...xi].some(i => i < 0) || lines.length !== 512) throw Error("SOURCE_SCHEMA_CHANGED");
const groups = new Map(); let sourceChecks = 0;
for (const line of lines) {
  const row = line.split(",");
  if (row[pi] !== "1/64") throw Error("SOURCE_PROBABILITY_CHANGED");
  sourceChecks++;
  const x = xi.map(i => Number(row[i]));
  for (const v of x) { if (!Number.isInteger(v)) throw Error("NON_INTEGER_OBSERVATION"); sourceChecks++; }
  if (!groups.has(row[wi])) groups.set(row[wi], []);
  groups.get(row[wi]).push(x);
}
if (groups.size !== 8 || [...groups.values()].some(x => x.length !== 64)) throw Error("SOURCE_WORLD_MASS_CHANGED");
const receipt = JSON.parse(receiptRaw.toString("utf8"));
const selected = new Set(["ONE_FACTOR_VALID", "TWO_FACTOR_BLOCK", "TETRAD_FALSE_REASSURANCE"]);
let comparedFields = 0, evaluatedTriples = 0;
const results = [];
function zeroTetrad(a,b,c) {
  // A_ij = n*sum(x_i*x_j)-sum(x_i)*sum(x_j)
  // For n=3 this equals the sum over unordered sample pairs of difference products.
  const p = a.map((v,i) => v-b[i]), q = a.map((v,i) => v-c[i]), t = b.map((v,i) => v-c[i]);
  const A = (i,j) => p[i]*p[j] + q[i]*q[j] + t[i]*t[j];
  const u = A(0,1)*A(2,3), v = A(0,2)*A(1,3), w = A(0,3)*A(1,2);
  return u === v && v === w;
}
function compare(world,n,total,zero) {
  const rec = receipt.worlds.find(x => x.world === world && x.n === n);
  if (!rec) throw Error("MISSING_RECEIPT_CASE " + world + " " + n);
  for (const [field,value] of Object.entries({ordered_sequences:total,tetrad_all_zero:zero,tetrad_any_nonzero:total-zero})) {
    comparedFields++;
    if (rec[field] !== value) throw Error("RECEIPT_MISMATCH " + world + " " + n + " " + field);
  }
}
for (const [world,rows] of groups) {
  // n=2: centered covariance is rank <=1, hence all three tetrads are identically zero.
  // This is an algebraic proof, not a claim to have enumerated the 4096 ordered pairs.
  compare(world,2,4096,4096);
  if (!selected.has(world)) continue;
  let zero = 0;
  for (let i=0;i<64;i++) for (let j=0;j<64;j++) for (let k=0;k<64;k++) {
    if (zeroTetrad(rows[i],rows[j],rows[k])) zero++;
    evaluatedTriples++;
  }
  compare(world,3,262144,zero);
  results.push({world,n:3,zero,nonzero:262144-zero});
}
if (evaluatedTriples !== 786432 || comparedFields !== 33 || sourceChecks !== 2560) throw Error("COVERAGE_MISMATCH");
process.stdout.write(JSON.stringify({status:"PASS",source_blob:expectedSource,receipt_blob:expectedReceipt,worlds:groups.size,source_rows:lines.length,source_checks:sourceChecks,receipt_field_checks:comparedFields,n2_worlds_algebraically_verified:8,enumerated_n3_triples:evaluatedTriples,results},null,2)+"\n");
