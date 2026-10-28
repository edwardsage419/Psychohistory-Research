"use strict";

/**
 * E071 R240 S36 source-first read-only exact check.
 * Usage from repository root:
 * node research/operations/e071_r240_s36_source_crossproduct_20261028.js
 * Requires only the Node.js standard library and committed source artifacts.
 * This is an internal E1 arithmetic audit, not a new human experiment.
 */
function verify(csvText, original, receipt) {
    const rows = csvText.trim().split(/\r?\n/);
    const columns = rows.shift().split(",");
    const ix = Object.fromEntries(columns.map((name, index) => [name, index]));
    const required = [
        "world", "original_structural_source_probability",
        "observed_pair_available", "observed_coder_A", "observed_coder_B"
    ];
    for (const name of required) {
        if (!(name in ix)) throw new Error("Missing column " + name);
    }

    let checks = 0;
    const assert = (condition, label) => {
        checks++;
        if (!condition) throw new Error("E071 check " + checks + ": " + label);
    };
    const totals = new Map();
    const tables = new Map();

    for (const [index, line] of rows.entries()) {
        const fields = line.split(",");
        const world = fields[ix.world];
        totals.set(world, (totals.get(world) || 0) + 1);
        assert(fields.length === columns.length, "CSV columns row " + index);
        assert(fields[ix.original_structural_source_probability] === "1/256", "mass " + index);
        const selected = fields[ix.observed_pair_available];
        assert(selected === "0" || selected === "1", "selection " + index);
        const a = fields[ix.observed_coder_A];
        const b = fields[ix.observed_coder_B];
        if (selected === "1") {
            assert(["0", "1"].includes(a) && ["0", "1"].includes(b), "visible pair " + index);
            if (!tables.has(world)) tables.set(world, [0, 0, 0, 0]);
            tables.get(world)[2 * Number(a) + Number(b)]++;
        } else {
            assert(a === "-1" && b === "-1", "missing pair " + index);
        }
    }

    const gcd = (a, b) => b === 0n ? (a < 0n ? -a : a) : gcd(b, a % b);
    const fraction = (a, b) => {
        if (b < 0n) { a = -a; b = -b; }
        const divisor = gcd(a, b);
        return b / divisor === 1n
            ? String(a / divisor)
            : String(a / divisor) + "/" + String(b / divisor);
    };
    const originals = new Map(original.world_results.map(item => [item.world, item]));

    assert(totals.size === 9, "nine worlds");
    assert(rows.length === 2304, "2304 source rows");
    assert(receipt.results.length === 36, "36 conditions");
    for (const [world, count] of totals) assert(count === 256, "256 rows " + world);
    for (const [world, table] of tables) {
        const originalRow = originals.get(world);
        assert(!!originalRow, "original baseline " + world);
        for (const [index, key] of ["00", "01", "10", "11"].entries()) {
            assert(table[index] === originalRow.observed_pair_table_2x2[key], world + " baseline " + key);
        }
    }

    for (const result of receipt.results) {
        const table = tables.get(result.world);
        const weight = result.weight_A1;
        const cells = table.map((value, index) => BigInt(value) * BigInt(index >= 2 ? weight : 1));
        const mass = cells.reduce((a, b) => a + b, 0n);
        const observedAgreement = cells[0] + cells[3];
        const a0 = cells[0] + cells[1], a1 = cells[2] + cells[3];
        const b0 = cells[0] + cells[2], b1 = cells[1] + cells[3];
        const expectedNumerator = a0 * b0 + a1 * b1;
        const kappaNumerator = observedAgreement * mass - expectedNumerator;
        const kappaDenominator = mass * mass - expectedNumerator;

        assert(result.unweighted_complete_pair_source_types === table.reduce((a, b) => a + b, 0), "N " + result.world);
        assert(result.weighted_mass === Number(mass), "W " + result.world);
        for (let index = 0; index < 4; index++) {
            assert(result.weighted_table_00_01_10_11[index] === Number(cells[index]), "cell " + result.world);
        }
        assert(result.observed_agreement === fraction(observedAgreement, mass), "Po " + result.world);
        assert(result.independent_marginal_chance_agreement === fraction(expectedNumerator, mass * mass), "Pe " + result.world);
        assert(result.cohens_kappa === (kappaDenominator === 0n ? "UNDEFINED" : fraction(kappaNumerator, kappaDenominator)), "kappa " + result.world);
    }

    const aliases = ["PERFECT_TRUTHFUL", "PERFECT_SYSTEMATICALLY_WRONG", "SHARED_SYSTEMATIC_ERROR"];
    for (const weight of [1, 2, 4, 8]) {
        const found = aliases.map(world => receipt.results.find(row => row.world === world && row.weight_A1 === weight));
        assert(found.every(row => row.cohens_kappa === found[0].cohens_kappa
            && row.observed_agreement === found[0].observed_agreement), "observational alias " + weight);
    }
    return { checks, failures: 0, original_rows: rows.length, worlds: totals.size, conditions: receipt.results.length };
}

if (typeof module !== "undefined") module.exports = { verify };

if (typeof require !== "undefined" && require.main === module) {
    const fs = require("fs");
    const source = fs.readFileSync("research/R240/R240_ALL_2304_ORIGINAL_TWO_CODER_ANNOTATION_ATOMS.csv", "utf8");
    const original = JSON.parse(fs.readFileSync("research/R240/R240_EXACT_RESULTS.json", "utf8"));
    const receipt = JSON.parse(fs.readFileSync("research/validation/R240_S36_CODER_A_REWEIGHT_EXACT_RECEIPT_2026-10-28.json", "utf8"));
    console.log(JSON.stringify(verify(source, original, receipt)));
}
