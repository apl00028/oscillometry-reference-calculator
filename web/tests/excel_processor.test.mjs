import test from "node:test";
import assert from "node:assert/strict";

import {
  processPatientRow,
  processRows,
  validateHeaders,
} from "../excel_processor.js";


const HEADERS = [
  "Sexo",
  "Edad",
  "Talla_cm",
  "Peso_kg",
  "R5_R20",
  "X5",
  "Fres",
  "AX",
];


function closeTo(
  actual,
  expected,
  tolerance = 1e-12
) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    `Expected ${actual} to be close to ${expected}`
  );
}


test("complete Excel patient matches calculator", () => {
  const row = processPatientRow(
    {
      Sexo: "Mujer",
      Edad: 60,
      Talla_cm: 165,
      Peso_kg: 65,
      R5_R20: 0.08,
      X5: -0.15,
      Fres: 20,
      AX: 1,
    },
    1
  );

  assert.equal(row.Registro, "P001");
  assert.equal(row.Error, "");

  closeTo(
    row.IMC,
    23.8751147842057
  );

  closeTo(
    row.R5_R20_predicho,
    0.05751370675291377
  );

  closeTo(
    row.X5_predicho,
    -0.1042825939650349
  );

  closeTo(
    row.Fres_predicho,
    16.42963364849651
  );

  closeTo(
    row.AX_predicho,
    0.4927265194429299
  );

  assert.equal(
    row.R5_R20_estado,
    "NORMAL"
  );

  assert.equal(
    row.X5_estado,
    "NORMAL"
  );

  assert.equal(
    row.Fres_estado,
    "NORMAL"
  );

  assert.equal(
    row.AX_estado,
    "NORMAL"
  );
});


test("missing oscillometry is allowed", () => {
  const row = processPatientRow(
    {
      Sexo: "Mujer",
      Edad: 60,
      Talla_cm: 165,
      Peso_kg: 65,
    },
    2
  );

  assert.equal(row.Registro, "P002");
  assert.equal(row.Error, "");

  assert.equal(
    row.R5_R20_estado,
    "NO INTRODUCIDO"
  );

  assert.equal(
    row.X5_estado,
    "NO INTRODUCIDO"
  );

  assert.equal(
    row.Fres_estado,
    "NO INTRODUCIDO"
  );

  assert.equal(
    row.AX_estado,
    "NO INTRODUCIDO"
  );
});


test("invalid demographic row records error", () => {
  const row = processPatientRow(
    {
      Sexo: "Mujer",
      Edad: 60,
      Talla_cm: 1.65,
      Peso_kg: 65,
    },
    1
  );

  assert.match(
    row.Error,
    /metros/
  );
});


test("blank rows are skipped", () => {
  const rows = processRows(
    [
      {
        Sexo: "",
        Edad: "",
        Talla_cm: "",
        Peso_kg: "",
      },
      {
        Sexo: "Mujer",
        Edad: 60,
        Talla_cm: 165,
        Peso_kg: 65,
      },
    ],
    HEADERS
  );

  assert.equal(rows.length, 1);
  assert.equal(rows[0].Registro, "P001");
});


test("required Excel columns are enforced", () => {
  assert.throws(
    () =>
      validateHeaders([
        "Sexo",
        "Edad",
        "Talla_cm",
      ]),
    /Peso_kg/
  );
});
