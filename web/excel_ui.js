import {
  processWorkbook,
} from "./excel_processor.js";


const fileInput =
  document.querySelector("#excel-file");

const selectedFile =
  document.querySelector("#selected-file");

const processButton =
  document.querySelector("#process-excel");

const templateButton =
  document.querySelector("#download-template");

const excelMessage =
  document.querySelector("#excel-message");


function showExcelMessage(type, text) {
  excelMessage.className =
    `excel-message ${type}`;

  excelMessage.textContent = text;
}


function clearExcelMessage() {
  excelMessage.className =
    "excel-message hidden";

  excelMessage.textContent = "";
}


fileInput.addEventListener("change", () => {
  clearExcelMessage();

  const file = fileInput.files[0];

  if (!file) {
    selectedFile.textContent =
      "Ningún archivo seleccionado";

    processButton.disabled = true;
    return;
  }

  selectedFile.textContent = file.name;
  processButton.disabled = false;
});


templateButton.addEventListener(
  "click",
  () => {
    clearExcelMessage();

    const link =
      document.createElement("a");

    link.href =
      "assets/Plantilla_Oscilometria.xlsx";

    link.download =
      "Plantilla_Oscilometria.xlsx";

    document.body.appendChild(link);
    link.click();
    link.remove();

    showExcelMessage(
      "success",
      "Plantilla Excel descargada correctamente."
    );
  }
);


processButton.addEventListener(
  "click",
  async () => {
    clearExcelMessage();

    const file = fileInput.files[0];

    if (!file) {
      showExcelMessage(
        "error",
        "Seleccione primero un archivo Excel."
      );
      return;
    }

    processButton.disabled = true;
    processButton.textContent =
      "Procesando...";

    try {
      const buffer =
        await file.arrayBuffer();

      const workbook = XLSX.read(
        buffer,
        {
          type: "array",
          cellDates: true,
          cellStyles: true,
        }
      );

      const result =
        processWorkbook(workbook);

      const baseName =
        file.name.replace(
          /\.xlsx$/i,
          ""
        );

      const outputName =
        `${baseName}_resultados.xlsx`;

      XLSX.writeFile(
        result.workbook,
        outputName
      );

      showExcelMessage(
        result.errors > 0
          ? "warning"
          : "success",
        `${result.processed} registros procesados correctamente` +
        (
          result.errors > 0
            ? ` · ${result.errors} con error`
            : ""
        ) +
        `. Descargado: ${outputName}`
      );

    } catch (error) {
      showExcelMessage(
        "error",
        error.message
      );

    } finally {
      processButton.disabled = false;
      processButton.textContent =
        "Procesar Excel";
    }
  }
);

