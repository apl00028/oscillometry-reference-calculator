import test from "node:test";
import assert from "node:assert/strict";

import {
  calculateBmi,
  gochicoaR5R20,
  gochicoaX5,
  gochicoaFres,
  gochicoaAx,
  validateDemographics,
  validateOscillometryValue,
} from "../calculator.js";


function closeTo(actual, expected, tolerance = 1e-12) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    `Expected ${actual} to be close to ${expected}`
  );
}


test("BMI matches Python implementation", () => {
  closeTo(
    calculateBmi(65, 165),
    23.8751147842057
  );
});


test("adult R5-R20 matches Python", () => {
  const result = gochicoaR5R20(
    60,
    "Mujer",
    165,
    65,
    0.08
  );

  closeTo(
    result.predicted,
    0.05751370675291377
  );

  closeTo(
    result.lln,
    0.0002711867529137726
  );

  closeTo(
    result.uln,
    0.1147562267529138
  );

  closeTo(
    result.zScore,
    0.6461578519277653
  );

  assert.equal(result.abnormal, false);
});


test("adult X5 matches Python", () => {
  const result = gochicoaX5(
    60,
    "Mujer",
    165,
    65,
    -0.15
  );

  closeTo(
    result.predicted,
    -0.1042825939650349
  );

  closeTo(
    result.lln,
    -0.171394513965035
  );

  closeTo(
    result.uln,
    -0.03717067396503494
  );

  closeTo(
    result.zScore,
    -1.120524657719731
  );

  assert.equal(result.abnormal, false);
});


test("adult Fres matches Python", () => {
  const result = gochicoaFres(
    60,
    "Mujer",
    165,
    65,
    20
  );

  closeTo(
    result.predicted,
    16.42963364849651
  );

  closeTo(
    result.lln,
    10.0309726484965
  );

  closeTo(
    result.uln,
    22.82829464849651
  );

  closeTo(
    result.zScore,
    0.9178319669674794
  );

  assert.equal(result.abnormal, false);
});


test("adult AX matches Python", () => {
  const result = gochicoaAx(
    60,
    "Mujer",
    165,
    65,
    1
  );

  closeTo(
    result.predicted,
    0.4927265194429299
  );

  closeTo(
    result.lln,
    0.1774114112588278
  );

  closeTo(
    result.uln,
    1.3684543809200072
  );

  closeTo(
    result.zScore,
    1.1397761451752755
  );

  assert.equal(result.abnormal, false);
});


test("comma decimal is accepted", () => {
  const result = validateDemographics({
    sex: "Mujer",
    age: "60",
    heightCm: "165",
    weightKg: "65,5",
  });

  assert.equal(result.errors.length, 0);
  assert.equal(result.weightKg, 65.5);
});


test("height entered in metres is rejected", () => {
  const result = validateDemographics({
    sex: "Mujer",
    age: 60,
    heightCm: 1.65,
    weightKg: 65,
  });

  assert.ok(
    result.errors.some(
      (message) => message.includes("metros")
    )
  );
});


test("age outside published range is rejected", () => {
  const result = validateDemographics({
    sex: "Mujer",
    age: 91,
    heightCm: 165,
    weightKg: 65,
  });

  assert.ok(
    result.errors.some(
      (message) =>
        message.includes("rango publicado")
    )
  );
});


test("missing oscillometry value is allowed", () => {
  assert.equal(
    validateOscillometryValue("AX", ""),
    null
  );
});


test("AX must be positive", () => {
  assert.throws(
    () => validateOscillometryValue("AX", 0),
    /mayor que 0/
  );
});
