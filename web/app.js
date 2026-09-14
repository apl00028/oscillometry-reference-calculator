import {
  gochicoaR5R20,
  gochicoaX5,
  gochicoaFres,
  gochicoaAx,
  validateDemographics,
  validateOscillometryValue,
} from "./calculator.js";


const form = document.querySelector("#calculator-form");
const clearButton = document.querySelector("#clear-button");
const messages = document.querySelector("#messages");
const bmiElement = document.querySelector("#bmi");


const inputs = {
  sex: document.querySelector("#sex"),
  age: document.querySelector("#age"),
  height: document.querySelector("#height"),
  weight: document.querySelector("#weight"),
  r5r20: document.querySelector("#r5r20"),
  x5: document.querySelector("#x5"),
  fres: document.querySelector("#fres"),
  ax: document.querySelector("#ax"),
};


function formatNumber(value, decimals = 3) {
  return value.toLocaleString("es-ES", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}


function getCard(name) {
  return document.querySelector(
    `[data-result="${name}"]`
  );
}


function resetCard(name) {
  const card = getCard(name);

  card.querySelector(".predicted-value").textContent = "—";
  card.querySelector(".lln-value").textContent = "—";
  card.querySelector(".uln-value").textContent = "—";
  card.querySelector(".z-value").textContent = "—";

  const status = card.querySelector(".status");
  status.textContent = "SIN CALCULAR";
  status.className = "status neutral";
}


function setNotIntroduced(name) {
  resetCard(name);

  const status = getCard(name).querySelector(".status");
  status.textContent = "NO INTRODUCIDO";
}


function setResult(name, result) {
  const card = getCard(name);

  card.querySelector(".predicted-value").textContent =
    formatNumber(result.predicted);

  card.querySelector(".lln-value").textContent =
    formatNumber(result.lln);

  card.querySelector(".uln-value").textContent =
    formatNumber(result.uln);

  card.querySelector(".z-value").textContent =
    formatNumber(result.zScore, 2);

  const status = card.querySelector(".status");

  if (result.abnormal) {
    status.textContent = "ALTERADO";
    status.className = "status abnormal";
  } else {
    status.textContent = "NORMAL";
    status.className = "status normal";
  }
}


function resetResults() {
  bmiElement.textContent = "—";

  ["r5r20", "x5", "fres", "ax"].forEach(
    resetCard
  );

  messages.className = "messages hidden";
  messages.innerHTML = "";
}


function showMessages(type, messageList) {
  if (messageList.length === 0) {
    messages.className = "messages hidden";
    messages.innerHTML = "";
    return;
  }

  messages.className = `messages ${type}`;

  messages.innerHTML = messageList
    .map((message) => `<div>${message}</div>`)
    .join("");
}


form.addEventListener("submit", (event) => {
  event.preventDefault();

  resetResults();

  const demographics = validateDemographics({
    sex: inputs.sex.value,
    age: inputs.age.value,
    heightCm: inputs.height.value,
    weightKg: inputs.weight.value,
  });

  if (demographics.errors.length > 0) {
    showMessages("error", demographics.errors);
    return;
  }

  if (demographics.warnings.length > 0) {
    showMessages(
      "warning",
      demographics.warnings
    );
  }

  bmiElement.textContent =
    formatNumber(demographics.bmi, 1);

  let observed;

  try {
    observed = {
      r5r20: validateOscillometryValue(
        "R5_R20",
        inputs.r5r20.value
      ),
      x5: validateOscillometryValue(
        "X5",
        inputs.x5.value
      ),
      fres: validateOscillometryValue(
        "Fres",
        inputs.fres.value
      ),
      ax: validateOscillometryValue(
        "AX",
        inputs.ax.value
      ),
    };
  } catch (error) {
    showMessages("error", [error.message]);
    return;
  }

  const common = [
    demographics.age,
    inputs.sex.value,
    demographics.heightCm,
    demographics.weightKg,
  ];

  if (observed.r5r20 === null) {
    setNotIntroduced("r5r20");
  } else {
    setResult(
      "r5r20",
      gochicoaR5R20(
        ...common,
        observed.r5r20
      )
    );
  }

  if (observed.x5 === null) {
    setNotIntroduced("x5");
  } else {
    setResult(
      "x5",
      gochicoaX5(
        ...common,
        observed.x5
      )
    );
  }

  if (observed.fres === null) {
    setNotIntroduced("fres");
  } else {
    setResult(
      "fres",
      gochicoaFres(
        ...common,
        observed.fres
      )
    );
  }

  if (observed.ax === null) {
    setNotIntroduced("ax");
  } else {
    setResult(
      "ax",
      gochicoaAx(
        ...common,
        observed.ax
      )
    );
  }
});


clearButton.addEventListener("click", () => {
  form.reset();
  resetResults();
});
