# Calculadora de oscilometría

Herramienta en Python para calcular valores de referencia de oscilometría a partir de las ecuaciones publicadas por Gochicoa-Rangel et al.

## Parámetros

- R5-R20
- X5
- Fres
- AX

Para cada parámetro disponible se calcula:

- valor predicho;
- LLN;
- ULN;
- z-score;
- clasificación NORMAL / ALTERADO.

Los parámetros oscilométricos son opcionales. Sexo, edad, talla y peso son necesarios para calcular los valores de referencia.

## Referencia científica

Gochicoa-Rangel L, Martínez-Briseño D, Guerrero-Zúñiga S, et al.
*Reference equations using segmented regressions for impulse oscillometry in healthy subjects aged 2.7-90 years.*
ERJ Open Research. 2023;9(6):00503-2023.
DOI: https://doi.org/10.1183/23120541.00503-2023

## Rango de edad

Las ecuaciones se aplican exclusivamente entre 2,7 y 90 años.

No se realiza extrapolación fuera de ese intervalo.

## LLN y ULN

LLN y ULN son límites de referencia, no intervalos de confianza del 95%.

La clasificación utiliza:

- R5-R20: alterado si observado > ULN;
- X5: alterado si observado < LLN;
- Fres: alterado si observado > ULN;
- AX: alterado si observado > ULN.

## Modos de uso

La aplicación permite:

- cálculo de un paciente individual mediante interfaz gráfica;
- procesamiento de cohortes mediante Excel.

El archivo de salida genera identificadores anónimos `P001`, `P002`, etc.

## Validaciones

La herramienta detecta:

- campos demográficos obligatorios ausentes;
- edad fuera del rango publicado;
- talla aparentemente introducida en metros;
- peso o talla no válidos;
- valores extremos de peso o IMC;
- AX <= 0;
- Fres <= 0.

Los controles de plausibilidad de talla, peso e IMC son controles técnicos de calidad de datos y no límites clínicos publicados por Gochicoa-Rangel.

## Ejecutar

Desde esta carpeta (`desktop/`):

```bash
python app.py
```

## Tests

Desde esta carpeta (`desktop/`):

```bash
python -m unittest discover -s tests -v
```

La suite contiene actualmente 33 tests y cubre ecuaciones, validación y procesamiento Excel.

## Aviso

Herramienta destinada al cálculo de valores de referencia y apoyo a investigación. Los resultados deben interpretarse en su contexto clínico y no sustituyen el juicio profesional.
