import {
  validateDemographics,
  validateOscillometryValue,
  gochicoaR5R20,
  gochicoaX5,
  gochicoaFres,
  gochicoaAx,
} from "./calculator.js";


export const REQUIRED_COLUMNS = [
  "Sexo",
  "Edad",
  "Talla_cm",
  "Peso_kg",
];

export const OPTIONAL_COLUMNS = [
  "R5_R20",
  "X5",
  "Fres",
  "AX",
];

export const OUTPUT_COLUMNS = [
  "IMC",
  "R5_R20_predicho",
  "R5_R20_LLN",
  "R5_R20_ULN",
  "R5_R20_z",
  "R5_R20_estado",
  "X5_predicho",
  "X5_LLN",
  "X5_ULN",
  "X5_z",
  "X5_estado",
  "Fres_predicho",
  "Fres_LLN",
  "Fres_ULN",
  "Fres_z",
  "Fres_estado",
  "AX_predicho",
  "AX_LLN",
  "AX_ULN",
  "AX_z",
  "AX_estado",
  "Advertencias",
  "Error",
];


function status(abnormal) {
  return abnormal ? "ALTERADO" : "NORMAL";
}


function emptyParameterResult(prefix) {
  return {
    [`${prefix}_predicho`]: "",
    [`${prefix}_LLN`]: "",
    [`${prefix}_ULN`]: "",
    [`${prefix}_z`]: "",
    [`${prefix}_estado`]: "NO INTRODUCIDO",
  };
}


function isBlank(value) {
  return (
    value === null ||
    value === undefined ||
    String(value).trim() === ""
  );
}


export function validateHeaders(headers) {
  const missing = REQUIRED_COLUMNS.filter(
    (column) => !headers.includes(column)
  );

  if (missing.length > 0) {
    throw new Error(
      "Faltan columnas obligatorias: " +
      missing.join(", ")
    );
  }
}


export function processPatientRow(
  row,
  recordNumber
) {
  const result = {
    Registro:
      `P${String(recordNumber).padStart(3, "0")}`,
    ...row,
  };

  for (const column of OUTPUT_COLUMNS) {
    result[column] = "";
  }

  try {
    const demographics = validateDemographics({
      sex: row.Sexo,
      age: row.Edad,
      heightCm: row.Talla_cm,
      weightKg: row.Peso_kg,
    });

    result.Advertencias =
      demographics.warnings.join(" | ");

    if (demographics.errors.length > 0) {
      throw new Error(
        demographics.errors.join(" | ")
      );
    }

    result.IMC = demographics.bmi;

    const common = [
      demographics.age,
      row.Sexo,
      demographics.heightCm,
      demographics.weightKg,
    ];

    const r5r20 = validateOscillometryValue(
      "R5_R20",
      row.R5_R20
    );

    const x5 = validateOscillometryValue(
      "X5",
      row.X5
    );

    const fres = validateOscillometryValue(
      "Fres",
      row.Fres
    );

    const ax = validateOscillometryValue(
      "AX",
      row.AX
    );


    if (r5r20 === null) {
      Object.assign(
        result,
        emptyParameterResult("R5_R20")
      );
    } else {
      const calculated = gochicoaR5R20(
        ...common,
        r5r20
      );

      Object.assign(result, {
        R5_R20_predicho: calculated.predicted,
        R5_R20_LLN: calculated.lln,
        R5_R20_ULN: calculated.uln,
        R5_R20_z: calculated.zScore,
        R5_R20_estado:
          status(calculated.abnormal),
      });
    }


    if (x5 === null) {
      Object.assign(
        result,
        emptyParameterResult("X5")
      );
    } else {
      const calculated = gochicoaX5(
        ...common,
        x5
      );

      Object.assign(result, {
        X5_predicho: calculated.predicted,
        X5_LLN: calculated.lln,
        X5_ULN: calculated.uln,
        X5_z: calculated.zScore,
        X5_estado:
          status(calculated.abnormal),
      });
    }


    if (fres === null) {
      Object.assign(
        result,
        emptyParameterResult("Fres")
      );
    } else {
      const calculated = gochicoaFres(
        ...common,
        fres
      );

      Object.assign(result, {
        Fres_predicho: calculated.predicted,
        Fres_LLN: calculated.lln,
        Fres_ULN: calculated.uln,
        Fres_z: calculated.zScore,
        Fres_estado:
          status(calculated.abnormal),
      });
    }


    if (ax === null) {
      Object.assign(
        result,
        emptyParameterResult("AX")
      );
    } else {
      const calculated = gochicoaAx(
        ...common,
        ax
      );

      Object.assign(result, {
        AX_predicho: calculated.predicted,
        AX_LLN: calculated.lln,
        AX_ULN: calculated.uln,
        AX_z: calculated.zScore,
        AX_estado:
          status(calculated.abnormal),
      });
    }

  } catch (error) {
    result.Error = error.message;
  }

  return result;
}


export function processRows(rows, headers) {
  validateHeaders(headers);

  const relevantColumns = [
    ...REQUIRED_COLUMNS,
    ...OPTIONAL_COLUMNS,
  ].filter((column) =>
    headers.includes(column)
  );

  const nonEmptyRows = rows.filter((row) =>
    relevantColumns.some(
      (column) => !isBlank(row[column])
    )
  );

  return nonEmptyRows.map(
    (row, index) =>
      processPatientRow(row, index + 1)
  );
}


export function processWorkbook(workbook) {
  if (
    typeof XLSX === "undefined"
  ) {
    throw new Error(
      "La librería Excel no está disponible."
    );
  }

  const sourceName =
    workbook.SheetNames.includes("Datos")
      ? "Datos"
      : workbook.SheetNames[0];

  if (!sourceName) {
    throw new Error(
      "El archivo Excel no contiene hojas."
    );
  }

  const sourceSheet =
    workbook.Sheets[sourceName];

  const matrix = XLSX.utils.sheet_to_json(
    sourceSheet,
    {
      header: 1,
      defval: "",
      raw: true,
    }
  );

  if (matrix.length === 0) {
    throw new Error(
      "La hoja de datos está vacía."
    );
  }

  const headers = matrix[0].map(
    (value) => String(value).trim()
  );

  validateHeaders(headers);

  const rows = XLSX.utils.sheet_to_json(
    sourceSheet,
    {
      defval: "",
      raw: true,
    }
  );

  const processedRows =
    processRows(rows, headers);

  const resultHeaders = [
    "Registro",
    ...headers,
    ...OUTPUT_COLUMNS,
  ];

  const resultMatrix = [
    resultHeaders,
    ...processedRows.map((row) =>
      resultHeaders.map(
        (header) =>
          row[header] ?? ""
      )
    ),
  ];

  const resultsSheet =
    XLSX.utils.aoa_to_sheet(
      resultMatrix
    );

  resultsSheet["!autofilter"] = {
    ref:
      XLSX.utils.encode_range({
        s: { r: 0, c: 0 },
        e: {
          r: Math.max(
            resultMatrix.length - 1,
            0
          ),
          c: resultHeaders.length - 1,
        },
      }),
  };

  resultsSheet["!cols"] =
    resultHeaders.map((header) => ({
      wch:
        header === "Registro"
          ? 12
          : Math.min(
              Math.max(
                String(header).length + 3,
                14
              ),
              24
            ),
    }));

  if (workbook.SheetNames.includes(
    "Resultados"
  )) {
    delete workbook.Sheets.Resultados;

    workbook.SheetNames =
      workbook.SheetNames.filter(
        (name) => name !== "Resultados"
      );
  }

  const sourceIndex =
    workbook.SheetNames.indexOf(
      sourceName
    );

  workbook.SheetNames.splice(
    sourceIndex + 1,
    0,
    "Resultados"
  );

  workbook.Sheets.Resultados =
    resultsSheet;

  return {
    workbook,
    sourceName,
    processedRows,
    processed:
      processedRows.filter(
        (row) => !row.Error
      ).length,
    errors:
      processedRows.filter(
        (row) => row.Error
      ).length,
  };
}


export function createTemplateWorkbook() {
  if (
    typeof XLSX === "undefined"
  ) {
    throw new Error(
      "La librería Excel no está disponible."
    );
  }

  const workbook =
    XLSX.utils.book_new();

  const headers = [
    ...REQUIRED_COLUMNS,
    ...OPTIONAL_COLUMNS,
  ];

  const worksheet =
    XLSX.utils.aoa_to_sheet([
      headers,
    ]);

  worksheet["!cols"] =
    headers.map((header) => ({
      wch: Math.max(
        String(header).length + 4,
        14
      ),
    }));

  XLSX.utils.book_append_sheet(
    workbook,
    worksheet,
    "Datos"
  );

  return workbook;
}
