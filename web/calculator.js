export const GOCHICOA_Z_LIMIT = 1.6449;
export const GOCHICOA_AGE_MIN = 2.7;
export const GOCHICOA_AGE_MAX = 90.0;


export function parseNumber(value, label) {
  if (
    value === null ||
    value === undefined ||
    String(value).trim() === ""
  ) {
    throw new Error(`Falta ${label}.`);
  }

  let normalized = value;

  if (typeof value === "string") {
    normalized = value.trim().replace(",", ".");
  }

  const number = Number(normalized);

  if (!Number.isFinite(number)) {
    throw new Error(
      `${label} no es un número válido: ${value}`
    );
  }

  return number;
}


export function parseOptionalNumber(value, label) {
  if (
    value === null ||
    value === undefined ||
    String(value).trim() === ""
  ) {
    return null;
  }

  return parseNumber(value, label);
}


export function calculateBmi(weightKg, heightCm) {
  if (weightKg <= 0 || heightCm <= 0) {
    throw new Error(
      "Peso y talla deben ser mayores que 0."
    );
  }

  return weightKg / ((heightCm / 100) ** 2);
}


export function encodeSex(sex) {
  const value = String(sex).trim().toLowerCase();

  if (["h", "hombre", "male"].includes(value)) {
    return 1.0;
  }

  if (
    ["m", "mujer", "female", "f"].includes(value)
  ) {
    return 0.0;
  }

  throw new Error(
    "Sexo no válido. Use Hombre o Mujer."
  );
}


function validateReferenceAge(age) {
  if (
    age < GOCHICOA_AGE_MIN ||
    age > GOCHICOA_AGE_MAX
  ) {
    throw new Error(
      "Edad fuera del rango publicado de " +
      "Gochicoa-Rangel (2.7-90 años)."
    );
  }
}


export function gochicoaR5R20(
  age,
  sex,
  heightCm,
  weightKg,
  observed
) {
  age = Number(age);
  heightCm = Number(heightCm);
  weightKg = Number(weightKg);
  observed = Number(observed);

  validateReferenceAge(age);

  let intercept;
  let ageCoefficient;
  let rmse;

  if (age <= 23.55) {
    intercept = 0.013349;
    ageCoefficient = -0.0075403;
    rmse = 0.0739;
  } else if (age >= 23.56) {
    intercept = -0.18775;
    ageCoefficient = 0.00099579;
    rmse = 0.0348;
  } else {
    throw new Error(
      "Edad situada entre los intervalos " +
      "publicados para R5-R20."
    );
  }

  const bmi = calculateBmi(weightKg, heightCm);
  const sexNumeric = encodeSex(sex);

  const predicted =
    intercept +
    0.004813 * sexNumeric +
    ageCoefficient * age +
    43.014247 / heightCm -
    1.794838 / bmi;

  const lln =
    predicted - GOCHICOA_Z_LIMIT * rmse;

  const uln =
    predicted + GOCHICOA_Z_LIMIT * rmse;

  const zScore =
    (observed - predicted) / rmse;

  return {
    observed,
    predicted,
    rmse,
    lln,
    uln,
    zScore,
    abnormal: observed > uln,
  };
}


export function gochicoaX5(
  age,
  sex,
  heightCm,
  weightKg,
  observed
) {
  age = Number(age);
  heightCm = Number(heightCm);
  weightKg = Number(weightKg);
  observed = Number(observed);

  validateReferenceAge(age);

  let intercept;
  let ageCoefficient;
  let rmse;

  if (age <= 5.29) {
    intercept = -0.089509;
    ageCoefficient = 0.043369;
    rmse = 0.0922;
  } else if (age >= 5.30 && age <= 18.68) {
    intercept = 0.1172;
    ageCoefficient = 0.0043487;
    rmse = 0.0575;
  } else if (age >= 18.69) {
    intercept = 0.19728;
    ageCoefficient = 0.00006377;
    rmse = 0.0408;
  } else {
    throw new Error(
      "Edad situada entre los intervalos " +
      "publicados para X5."
    );
  }

  const bmi = calculateBmi(weightKg, heightCm);
  const sexNumeric = encodeSex(sex);

  const predicted =
    intercept +
    0.009133 * sexNumeric +
    ageCoefficient * age -
    57.924822 / heightCm +
    1.090394 / bmi;

  const lln =
    predicted - GOCHICOA_Z_LIMIT * rmse;

  const uln =
    predicted + GOCHICOA_Z_LIMIT * rmse;

  const zScore =
    (observed - predicted) / rmse;

  return {
    observed,
    predicted,
    rmse,
    lln,
    uln,
    zScore,
    abnormal: observed < lln,
  };
}


export function gochicoaFres(
  age,
  sex,
  heightCm,
  weightKg,
  observed
) {
  age = Number(age);
  heightCm = Number(heightCm);
  weightKg = Number(weightKg);
  observed = Number(observed);

  validateReferenceAge(age);

  let intercept;
  let ageCoefficient;
  let rmse;

  if (age <= 9.69) {
    intercept = 3.63228;
    ageCoefficient = 0.14349;
    rmse = 2.71;
  } else if (age >= 9.70 && age <= 20.98) {
    intercept = 7.518;
    ageCoefficient = -0.2571;
    rmse = 3.20;
  } else if (age >= 20.99) {
    intercept = 1.2542;
    ageCoefficient = 0.041179;
    rmse = 3.89;
  } else {
    throw new Error(
      "Edad situada entre los intervalos " +
      "publicados para Fres."
    );
  }

  const bmi = calculateBmi(weightKg, heightCm);
  const sexNumeric = encodeSex(sex);

  const predicted =
    intercept +
    0.07493 * sexNumeric +
    ageCoefficient * age +
    2781.55206 / heightCm -
    99.15807 / bmi;

  const lln =
    predicted - GOCHICOA_Z_LIMIT * rmse;

  const uln =
    predicted + GOCHICOA_Z_LIMIT * rmse;

  const zScore =
    (observed - predicted) / rmse;

  return {
    observed,
    predicted,
    rmse,
    lln,
    uln,
    zScore,
    abnormal: observed > uln,
  };
}


export function gochicoaAx(
  age,
  sex,
  heightCm,
  weightKg,
  observed
) {
  age = Number(age);
  heightCm = Number(heightCm);
  weightKg = Number(weightKg);
  observed = Number(observed);

  validateReferenceAge(age);

  if (observed <= 0) {
    throw new Error(
      "AX debe ser mayor que 0 porque la " +
      "ecuación utiliza logaritmo natural."
    );
  }

  let intercept;
  let ageCoefficient;
  let rmse;

  if (age <= 6.98) {
    intercept = -3.42268;
    ageCoefficient = 0.10429;
    rmse = 0.366;
  } else if (age >= 6.99 && age <= 23.21) {
    intercept = -2.367;
    ageCoefficient = -0.046624;
    rmse = 0.461;
  } else if (age >= 23.22) {
    intercept = -3.597;
    ageCoefficient = 0.0063497;
    rmse = 0.621;
  } else {
    throw new Error(
      "Edad situada entre los intervalos " +
      "publicados para AX."
    );
  }

  const bmi = calculateBmi(weightKg, heightCm);
  const sexNumeric = encodeSex(sex);

  const logPredicted =
    intercept -
    0.06776 * sexNumeric +
    ageCoefficient * age +
    544.962 / heightCm -
    18.97076 / bmi;

  const predicted = Math.exp(logPredicted);

  const lln = Math.exp(
    Math.log(predicted) -
    GOCHICOA_Z_LIMIT * rmse
  );

  const uln = Math.exp(
    Math.log(predicted) +
    GOCHICOA_Z_LIMIT * rmse
  );

  const zScore =
    (
      Math.log(observed) -
      Math.log(predicted)
    ) / rmse;

  return {
    observed,
    predicted,
    rmse,
    lln,
    uln,
    zScore,
    abnormal: observed > uln,
  };
}


export function validateDemographics({
  sex,
  age,
  heightCm,
  weightKg,
}) {
  const errors = [];
  const warnings = [];

  try {
    encodeSex(sex);
  } catch {
    errors.push(
      "Sexo no válido. Seleccione Mujer u Hombre."
    );
  }

  try {
    age = parseNumber(age, "Edad");
  } catch (error) {
    errors.push(error.message);
    age = null;
  }

  try {
    heightCm = parseNumber(heightCm, "Talla");
  } catch (error) {
    errors.push(error.message);
    heightCm = null;
  }

  try {
    weightKg = parseNumber(weightKg, "Peso");
  } catch (error) {
    errors.push(error.message);
    weightKg = null;
  }

  if (age !== null) {
    if (
      age < GOCHICOA_AGE_MIN ||
      age > GOCHICOA_AGE_MAX
    ) {
      errors.push(
        "Edad fuera del rango publicado de " +
        "Gochicoa-Rangel (2,7-90 años)."
      );
    }
  }

  if (heightCm !== null) {
    if (heightCm <= 0) {
      errors.push(
        "La talla debe ser mayor que 0."
      );
    } else if (
      heightCm >= 0.8 &&
      heightCm <= 2.5
    ) {
      errors.push(
        "La talla parece estar expresada en metros. " +
        "Introduzca centímetros, por ejemplo 165 " +
        "en vez de 1,65."
      );
    } else if (
      heightCm < 80 ||
      heightCm > 220
    ) {
      warnings.push(
        "Talla fuera del rango habitual; revise " +
        "que esté expresada en centímetros."
      );
    }
  }

  if (weightKg !== null) {
    if (weightKg <= 0) {
      errors.push(
        "El peso debe ser mayor que 0."
      );
    } else if (
      weightKg < 20 ||
      weightKg > 250
    ) {
      warnings.push(
        "Peso fuera del rango habitual; revise " +
        "el valor introducido."
      );
    }
  }

  let bmi = null;

  if (
    errors.length === 0 &&
    heightCm !== null &&
    weightKg !== null
  ) {
    bmi = calculateBmi(weightKg, heightCm);

    if (bmi < 12 || bmi > 60) {
      warnings.push(
        `IMC calculado de ${bmi.toFixed(1)}, ` +
        "fuera del rango habitual; revise peso y talla."
      );
    }
  }

  return {
    age,
    heightCm,
    weightKg,
    bmi,
    warnings,
    errors,
  };
}


export function validateOscillometryValue(
  parameter,
  value
) {
  const parsed = parseOptionalNumber(
    value,
    parameter
  );

  if (parsed === null) {
    return null;
  }

  if (parameter === "AX" && parsed <= 0) {
    throw new Error(
      "AX debe ser mayor que 0."
    );
  }

  if (parameter === "Fres" && parsed <= 0) {
    throw new Error(
      "Fres debe ser mayor que 0."
    );
  }

  return parsed;
}
