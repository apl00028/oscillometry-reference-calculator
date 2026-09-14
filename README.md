# Oscillometry Reference Calculator

Reference-value calculator for impulse oscillometry based on the segmented regression equations published by Gochicoa-Rangel et al.

The project provides two implementations of the same reference-equation logic:

- a browser-based calculator for individual patients and Excel batch processing;
- a Windows desktop application for individual calculations and Excel batch processing.

## Live web application

https://apl00028.github.io/oscillometry-reference-calculator/

The web version requires no installation.

---

## Scientific basis

This calculator implements reference equations derived from:

**Gochicoa-Rangel L, Martínez-Briseño D, Guerrero-Zúñiga S, et al.**  
*Reference equations using segmented regressions for impulse oscillometry in healthy subjects aged 2.7-90 years.*  
**ERJ Open Research. 2023;9(6):00503-2023.**

- DOI: https://doi.org/10.1183/23120541.00503-2023
- PubMed: https://pubmed.ncbi.nlm.nih.gov/38111542/
- PubMed Central: https://pmc.ncbi.nlm.nih.gov/articles/PMC10726221/

The original study included 830 healthy nonsmokers aged 2.7 to 90 years and used multivariable segmented regression to derive reference equations across the lifespan.

This implementation does **not extrapolate outside the published age range of 2.7 to 90 years**.

The original publication remains the authoritative scientific source. The equations below are documented here so that the software implementation can be reviewed and audited directly.

---

## Supported parameters

The calculator currently implements reference values for:

| Parameter | Classification implemented |
| --- | --- |
| R5-R20 | ALTERADO if observed > ULN |
| X5 | ALTERADO if observed < LLN |
| Fres | ALTERADO if observed > ULN |
| AX | ALTERADO if observed > ULN |

For every oscillometric parameter entered, the calculator can return:

- predicted value;
- lower limit of normal (LLN);
- upper limit of normal (ULN);
- z-score;
- NORMAL / ALTERADO classification.

LLN and ULN are reference limits, not 95% confidence intervals for the predicted mean.

---

# Mathematical implementation

## Notation

The following notation is used:

```text
A   = age in years
H   = height in centimetres
W   = weight in kilograms
BMI = body mass index
S   = sex indicator
```

Sex is coded as:

```text
S = 1 for male
S = 0 for female
```

BMI is calculated internally as:

```text
BMI = W / (H / 100)^2
```

The implementation uses the one-sided reference-limit constant:

```text
z_limit = 1.6449
```

For R5-R20, X5 and Fres:

```text
LLN = predicted - 1.6449 * RMSE
ULN = predicted + 1.6449 * RMSE

z-score = (observed - predicted) / RMSE
```

The equations are segmented by age. The calculator automatically selects the appropriate coefficients for the subject's age.

---

## R5-R20

Prediction equation:

```text
R5-R20_pred =
    alpha
    + 0.004813 * S
    + beta_A * A
    + 43.014247 / H
    - 1.794838 / BMI
```

Age-dependent coefficients:

| Age interval | alpha | beta_A | RMSE |
| --- | ---: | ---: | ---: |
| A <= 23.55 | 0.013349 | -0.0075403 | 0.0739 |
| A >= 23.56 | -0.18775 | 0.00099579 | 0.0348 |

Reference limits and z-score:

```text
LLN = R5-R20_pred - 1.6449 * RMSE
ULN = R5-R20_pred + 1.6449 * RMSE

z = (R5-R20_observed - R5-R20_pred) / RMSE
```

Classification:

```text
R5-R20_observed > ULN  ->  ALTERADO
```

---

## X5

Prediction equation:

```text
X5_pred =
    alpha
    + 0.009133 * S
    + beta_A * A
    - 57.924822 / H
    + 1.090394 / BMI
```

Age-dependent coefficients:

| Age interval | alpha | beta_A | RMSE |
| --- | ---: | ---: | ---: |
| A <= 5.29 | -0.089509 | 0.043369 | 0.0922 |
| 5.30 <= A <= 18.68 | 0.1172 | 0.0043487 | 0.0575 |
| A >= 18.69 | 0.19728 | 0.00006377 | 0.0408 |

Reference limits and z-score:

```text
LLN = X5_pred - 1.6449 * RMSE
ULN = X5_pred + 1.6449 * RMSE

z = (X5_observed - X5_pred) / RMSE
```

Classification:

```text
X5_observed < LLN  ->  ALTERADO
```

---

## Fres

Prediction equation:

```text
Fres_pred =
    alpha
    + 0.07493 * S
    + beta_A * A
    + 2781.55206 / H
    - 99.15807 / BMI
```

Age-dependent coefficients:

| Age interval | alpha | beta_A | RMSE |
| --- | ---: | ---: | ---: |
| A <= 9.69 | 3.63228 | 0.14349 | 2.71 |
| 9.70 <= A <= 20.98 | 7.518 | -0.2571 | 3.20 |
| A >= 20.99 | 1.2542 | 0.041179 | 3.89 |

Reference limits and z-score:

```text
LLN = Fres_pred - 1.6449 * RMSE
ULN = Fres_pred + 1.6449 * RMSE

z = (Fres_observed - Fres_pred) / RMSE
```

Classification:

```text
Fres_observed > ULN  ->  ALTERADO
```

---

## AX

AX is modelled on the natural-logarithmic scale.

Prediction equation:

```text
log_AX_pred =
    alpha
    - 0.06776 * S
    + beta_A * A
    + 544.962 / H
    - 18.97076 / BMI
```

Age-dependent coefficients:

| Age interval | alpha | beta_A | RMSE |
| --- | ---: | ---: | ---: |
| A <= 6.98 | -3.42268 | 0.10429 | 0.366 |
| 6.99 <= A <= 23.21 | -2.367 | -0.046624 | 0.461 |
| A >= 23.22 | -3.597 | 0.0063497 | 0.621 |

Prediction on the original AX scale:

```text
AX_pred = exp(log_AX_pred)
```

Reference limits:

```text
LLN = exp(log_AX_pred - 1.6449 * RMSE)
ULN = exp(log_AX_pred + 1.6449 * RMSE)
```

z-score:

```text
z = (ln(AX_observed) - log_AX_pred) / RMSE
```

AX must therefore be strictly greater than zero.

Classification:

```text
AX_observed > ULN  ->  ALTERADO
```

---

## Required patient information

Reference calculations require:

- sex;
- age;
- height in centimetres;
- weight in kilograms.

BMI is calculated automatically.

Oscillometry measurements are optional. A parameter can therefore be omitted when it is unavailable.

---

# Web calculator

The public browser version is available at:

https://apl00028.github.io/oscillometry-reference-calculator/

It supports:

- individual calculations;
- automatic BMI calculation;
- predicted values;
- LLN and ULN;
- z-scores;
- normal/abnormal classification;
- Excel batch processing;
- downloadable Excel template.

The browser application is entirely static and does not require a backend.

---

# Excel batch processing

The web and desktop applications support `.xlsx` batch processing.

The recommended workflow is to download the template supplied by the web application.

## Template structure

The template contains:

- a `Datos` worksheet;
- an `Instrucciones` worksheet;
- a `Mujer / Hombre` dropdown for sex;
- input validation for relevant fields.

## Required columns

```text
Sexo
Edad
Talla_cm
Peso_kg
```

## Optional oscillometry columns

```text
R5_R20
X5
Fres
AX
```

After processing, the application generates a `Resultados` worksheet containing:

- original input values;
- calculated BMI;
- predicted values;
- LLN;
- ULN;
- z-scores;
- NORMAL / ALTERADO status;
- warnings;
- row-level errors.

Rows receive anonymous processing identifiers such as:

```text
P001
P002
P003
```

These identifiers are generated by the software and are not patient identifiers.

---

# Data-quality validation

The software performs checks intended to reduce common data-entry errors.

These include:

- missing demographic fields;
- age outside 2.7-90 years;
- invalid sex values;
- height apparently entered in metres rather than centimetres;
- non-positive height or weight;
- unusually low or high height;
- unusually low or high weight;
- unusually low or high calculated BMI;
- Fres <= 0;
- AX <= 0.

The height, weight and BMI plausibility checks are software data-quality checks. They are not clinical reference limits from the Gochicoa-Rangel publication.

---

# Privacy

The web application performs calculations locally in the browser.

Values entered into the individual form and Excel files selected for batch processing are not sent to an application backend.

The web host still receives the ordinary HTTP requests required to serve the static application files.

The Excel-processing JavaScript library is vendored inside this repository, so Excel processing does not require loading the library from an external CDN.

---

# Desktop application

The desktop implementation is written in Python.

Main dependencies:

- Python;
- CustomTkinter;
- openpyxl.

Install dependencies from the repository root with:

```bash
pip install -r desktop/requirements.txt
```

Then run:

```bash
cd desktop
python app.py
```

The desktop application supports both individual calculations and Excel batch processing.

---

# Running the web application locally

No backend is required.

For example:

```bash
cd web
python -m http.server 8001
```

Then open:

```text
http://localhost:8001
```

---

# Tests and validation

Automated tests are available for both implementations.

## Desktop

Run from the `desktop/` directory:

```bash
python -m unittest discover -s tests -v
```

Current suite:

**33 tests passing**

The desktop tests cover equations, demographic validation, oscillometry validation and Excel processing.

## Web

Run from the `web/` directory:

```bash
npm test
```

Current suite:

**15 tests passing**

The web tests cover reference calculations, BMI, decimal-comma handling, demographic validation, oscillometry validation and Excel processing.

The JavaScript implementation has been cross-checked against the Python implementation using the same reference calculations.

The Excel template and browser-based Excel workflow have also been manually validated.

GitHub Actions automatically execute the test suites.

---

# Repository structure

```text
oscillometry-reference-calculator/
|-- desktop/
|   |-- app.py
|   |-- equations.py
|   |-- excel_processor.py
|   |-- validation.py
|   |-- requirements.txt
|   |-- requirements-build.txt
|   `-- tests/
|
|-- web/
|   |-- index.html
|   |-- app.js
|   |-- calculator.js
|   |-- excel_processor.js
|   |-- excel_ui.js
|   |-- styles.css
|   |-- assets/
|   |   `-- Plantilla_Oscilometria.xlsx
|   |-- vendor/
|   `-- tests/
|
`-- .github/
    `-- workflows/
```

The calculator is maintained independently from study-specific statistical analysis repositories. This avoids duplicating the user-facing software and allows the reference implementation to be developed and validated separately.

---

# Intended use and limitations

This software is intended for:

- reference-value calculation;
- research support;
- data-quality checking;
- reproducible implementation of published equations.

It is **not a medical device** and does not establish a clinical diagnosis.

`NORMAL` and `ALTERADO` indicate only whether an observed value lies within or outside the implemented reference limits.

Results must be interpreted together with the clinical context, measurement quality, equipment, testing conditions and professional judgment.

The original Gochicoa-Rangel publication should be consulted when the reference methodology itself is being evaluated or cited.

---

# Citation

If this software is used in research, please cite the scientific publication from which the reference equations were derived:

Gochicoa-Rangel L, Martínez-Briseño D, Guerrero-Zúñiga S, et al.  
**Reference equations using segmented regressions for impulse oscillometry in healthy subjects aged 2.7-90 years.**  
*ERJ Open Research.* 2023;9(6):00503-2023.  
DOI: https://doi.org/10.1183/23120541.00503-2023

The software repository may additionally be cited by its repository URL:

https://github.com/apl00028/oscillometry-reference-calculator
