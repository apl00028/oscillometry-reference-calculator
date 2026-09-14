# Oscillometry Reference Calculator

Reference-value calculator for impulse oscillometry based on the segmented
regression equations published by **Gochicoa-Rangel et al.**

The project provides two implementations of the same reference-equation logic:

- a browser-based calculator for individual patients and Excel batch processing;
- a Windows desktop application for individual calculations and Excel batch processing.

## Live web application

**https://apl00028.github.io/oscillometry-reference-calculator/**

The web version requires no installation.

---

## Scientific basis

This calculator implements reference equations derived from:

**Gochicoa-Rangel L, Mart?nez-Brise?o D, Guerrero-Z??iga S, et al.**
*Reference equations using segmented regressions for impulse oscillometry in healthy subjects aged 2.7?90 years.*
**ERJ Open Research. 2023;9(6):00503-2023.**

- DOI: https://doi.org/10.1183/23120541.00503-2023
- PubMed: https://pubmed.ncbi.nlm.nih.gov/38111542/
- PubMed Central: https://pmc.ncbi.nlm.nih.gov/articles/PMC10726221/

The original study used multivariable segmented regression to derive
reference equations across the lifespan.

The published reference population covers ages **2.7 to 90 years**.

This implementation does **not extrapolate outside that age range**.

The original publication remains the authoritative scientific source.
The equations below are documented here to make the software implementation
transparent and auditable.

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

LLN and ULN are **reference limits**, not 95% confidence intervals for the
predicted mean.

---

# Mathematical implementation

## Notation

Let:

- \(A\) = age in years;
- \(H\) = height in centimetres;
- \(W\) = weight in kilograms;
- \(BMI\) = body mass index;
- \(S\) = numerical sex indicator.

Sex is coded as:

$$
S =
\begin{cases}
1, & \text{male} \\
0, & \text{female}
\end{cases}
$$

BMI is calculated internally as:

$$
BMI =
\frac{W}
{\left(H/100\right)^2}
$$

The implementation uses:

$$
z_{0.95}=1.6449
$$

to obtain the one-sided lower and upper reference limits from the residual
standard deviation (RMSE).

For R5-R20, X5 and Fres:

$$
LLN = \widehat{Y} - 1.6449 \times RMSE
$$

$$
ULN = \widehat{Y} + 1.6449 \times RMSE
$$

and:

$$
z =
\frac{Y_{observed}-\widehat{Y}}
{RMSE}
$$

The equations are segmented by age. The appropriate coefficients are selected
according to the subject's age.

---

## R5-R20

The implemented prediction equation is:

$$
\widehat{R5-R20}
=
\alpha
+
0.004813S
+
\beta_A A
+
\frac{43.014247}{H}
-
\frac{1.794838}{BMI}
$$

Age-dependent coefficients:

| Age interval | \(\alpha\) | \(\beta_A\) | RMSE |
| --- | ---: | ---: | ---: |
| \(A \leq 23.55\) | 0.013349 | -0.0075403 | 0.0739 |
| \(A \geq 23.56\) | -0.18775 | 0.00099579 | 0.0348 |

Reference limits:

$$
LLN_{R5-R20}
=
\widehat{R5-R20}
-
1.6449 \times RMSE
$$

$$
ULN_{R5-R20}
=
\widehat{R5-R20}
+
1.6449 \times RMSE
$$

z-score:

$$
z_{R5-R20}
=
\frac{
(R5-R20)_{observed}
-
\widehat{R5-R20}
}{
RMSE
}
$$

Classification used by the calculator:

$$
(R5-R20)_{observed} > ULN
\quad\Rightarrow\quad
\text{ALTERADO}
$$

---

## X5

The implemented prediction equation is:

$$
\widehat{X5}
=
\alpha
+
0.009133S
+
\beta_A A
-
\frac{57.924822}{H}
+
\frac{1.090394}{BMI}
$$

Age-dependent coefficients:

| Age interval | \(\alpha\) | \(\beta_A\) | RMSE |
| --- | ---: | ---: | ---: |
| \(A \leq 5.29\) | -0.089509 | 0.043369 | 0.0922 |
| \(5.30 \leq A \leq 18.68\) | 0.1172 | 0.0043487 | 0.0575 |
| \(A \geq 18.69\) | 0.19728 | 0.00006377 | 0.0408 |

Reference limits:

$$
LLN_{X5}
=
\widehat{X5}
-
1.6449 \times RMSE
$$

$$
ULN_{X5}
=
\widehat{X5}
+
1.6449 \times RMSE
$$

z-score:

$$
z_{X5}
=
\frac{
X5_{observed}
-
\widehat{X5}
}{
RMSE
}
$$

Classification:

$$
X5_{observed} < LLN
\quad\Rightarrow\quad
\text{ALTERADO}
$$

---

## Fres

The implemented prediction equation is:

$$
\widehat{Fres}
=
\alpha
+
0.07493S
+
\beta_A A
+
\frac{2781.55206}{H}
-
\frac{99.15807}{BMI}
$$

Age-dependent coefficients:

| Age interval | \(\alpha\) | \(\beta_A\) | RMSE |
| --- | ---: | ---: | ---: |
| \(A \leq 9.69\) | 3.63228 | 0.14349 | 2.71 |
| \(9.70 \leq A \leq 20.98\) | 7.518 | -0.2571 | 3.20 |
| \(A \geq 20.99\) | 1.2542 | 0.041179 | 3.89 |

Reference limits:

$$
LLN_{Fres}
=
\widehat{Fres}
-
1.6449 \times RMSE
$$

$$
ULN_{Fres}
=
\widehat{Fres}
+
1.6449 \times RMSE
$$

z-score:

$$
z_{Fres}
=
\frac{
Fres_{observed}
-
\widehat{Fres}
}{
RMSE
}
$$

Classification:

$$
Fres_{observed} > ULN
\quad\Rightarrow\quad
\text{ALTERADO}
$$

---

## AX

AX is modelled on the natural-logarithmic scale.

The implemented equation is:

$$
\log(\widehat{AX})
=
\alpha
-
0.06776S
+
\beta_A A
+
\frac{544.962}{H}
-
\frac{18.97076}{BMI}
$$

Age-dependent coefficients:

| Age interval | \(\alpha\) | \(\beta_A\) | RMSE |
| --- | ---: | ---: | ---: |
| \(A \leq 6.98\) | -3.42268 | 0.10429 | 0.366 |
| \(6.99 \leq A \leq 23.21\) | -2.367 | -0.046624 | 0.461 |
| \(A \geq 23.22\) | -3.597 | 0.0063497 | 0.621 |

The predicted value on the original scale is:

$$
\widehat{AX}
=
\exp\left[
\log(\widehat{AX})
\right]
$$

Because the residual model is defined on the log scale, the limits are:

$$
LLN_{AX}
=
\exp\left[
\log(\widehat{AX})
-
1.6449 \times RMSE
\right]
$$

$$
ULN_{AX}
=
\exp\left[
\log(\widehat{AX})
+
1.6449 \times RMSE
\right]
$$

The z-score is:

$$
z_{AX}
=
\frac{
\ln(AX_{observed})
-
\log(\widehat{AX})
}{
RMSE
}
$$

For this reason, AX must be strictly greater than zero.

Classification:

$$
AX_{observed} > ULN
\quad\Rightarrow\quad
\text{ALTERADO}
$$

---

## Required patient information

Reference calculations require:

- sex;
- age;
- height in centimetres;
- weight in kilograms.

BMI is calculated automatically.

Oscillometry measurements are optional. A parameter can therefore be omitted
when it is unavailable.

---

# Web calculator

The public browser version is available at:

**https://apl00028.github.io/oscillometry-reference-calculator/**

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

The recommended workflow is to download the template supplied by the web
application.

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

After processing, the application generates a `Resultados` worksheet
containing:

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

These identifiers are generated by the software and are not patient
identifiers.

---

# Data-quality validation

The software performs checks intended to reduce common data-entry errors.

These include:

- missing demographic fields;
- age outside 2.7?90 years;
- invalid sex values;
- height apparently entered in metres rather than centimetres;
- non-positive height or weight;
- unusually low or high height;
- unusually low or high weight;
- unusually low or high calculated BMI;
- Fres <= 0;
- AX <= 0.

The height, weight and BMI plausibility checks are **software data-quality
checks**.

They are not clinical reference limits from the Gochicoa-Rangel publication.

---

# Privacy

The web application performs calculations locally in the browser.

Values entered into the individual form and Excel files selected for batch
processing are not sent to an application backend.

The web host still receives the ordinary HTTP requests required to serve the
static application files.

The Excel-processing JavaScript library is vendored inside this repository,
so Excel processing does not require loading the library from an external CDN.

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

The desktop application supports both individual calculations and Excel batch
processing.

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

```bash
cd desktop
python -m unittest discover -s tests -v
```

Current suite:

**33 tests passing**

The desktop tests cover:

- equations;
- demographic validation;
- oscillometry validation;
- Excel processing.

## Web

```bash
cd web
npm test
```

Current suite:

**15 tests passing**

The web tests cover:

- reference calculations;
- BMI;
- decimal-comma handling;
- demographic validation;
- oscillometry validation;
- Excel row processing;
- required Excel columns;
- missing oscillometry values.

The JavaScript implementation has been cross-checked against the Python
implementation using the same reference calculations.

The Excel template and browser-based Excel workflow have also been manually
validated.

GitHub Actions automatically execute the test suites.

---

# Repository structure

```text
oscillometry-reference-calculator/
??? desktop/
?   ??? app.py
?   ??? equations.py
?   ??? excel_processor.py
?   ??? validation.py
?   ??? requirements.txt
?   ??? requirements-build.txt
?   ??? tests/
?
??? web/
?   ??? index.html
?   ??? app.js
?   ??? calculator.js
?   ??? excel_processor.js
?   ??? excel_ui.js
?   ??? styles.css
?   ??? assets/
?   ?   ??? Plantilla_Oscilometria.xlsx
?   ??? vendor/
?   ??? tests/
?
??? .github/
    ??? workflows/
```

The calculator is maintained independently from study-specific statistical
analysis repositories. This avoids duplicating the user-facing software and
allows the reference implementation to be developed and validated separately.

---

# Intended use and limitations

This software is intended for:

- reference-value calculation;
- research support;
- data-quality checking;
- reproducible implementation of published equations.

It is **not a medical device** and does not establish a clinical diagnosis.

`NORMAL` and `ALTERADO` indicate only whether an observed value lies within or
outside the implemented reference limits.

Results must be interpreted together with the clinical context, measurement
quality, equipment, testing conditions and professional judgment.

The original Gochicoa-Rangel publication should be consulted when the
reference methodology itself is being evaluated or cited.

---

# Citation

If this software is used in research, please cite the scientific publication
from which the reference equations were derived:

Gochicoa-Rangel L, Mart?nez-Brise?o D, Guerrero-Z??iga S, et al.
**Reference equations using segmented regressions for impulse oscillometry in
healthy subjects aged 2.7?90 years.**
*ERJ Open Research.* 2023;9(6):00503-2023.

https://doi.org/10.1183/23120541.00503-2023

The software repository may additionally be cited by its repository URL:

https://github.com/apl00028/oscillometry-reference-calculator
