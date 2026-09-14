# Calculadora de oscilometria

Herramienta en Python para calcular valores de referencia de oscilometria a partir de las ecuaciones publicadas por Gochicoa-Rangel et al.

## Parametros

- R5-R20
- X5
- Fres
- AX

Para cada parametro disponible se calcula:

- valor predicho
- LLN
- ULN
- z-score
- clasificacion NORMAL / ALTERADO

Los parametros oscilometricos son opcionales. Sexo, edad, talla y peso son necesarios para calcular los valores de referencia.

## Referencia

Gochicoa-Rangel et al.
Reference equations using segmented regressions for impulse oscillometry in healthy subjects aged 2.7-90 years.
ERJ Open Research. 2023;9:00503-2023.

## Rango de edad

Las ecuaciones se aplican exclusivamente entre 2.7 y 90 anos.
No se realiza extrapolacion fuera de ese intervalo.

## LLN y ULN

LLN y ULN son limites de referencia, no intervalos de confianza del 95%.

La clasificacion utiliza:

- R5-R20: alterado si observado > ULN
- X5: alterado si observado < LLN
- Fres: alterado si observado > ULN
- AX: alterado si observado > ULN

## Modos de uso

Paciente individual mediante interfaz grafica o procesamiento de cohortes mediante Excel.

El archivo de salida genera identificadores anonimos P001, P002, etc.

## Validaciones

La herramienta detecta:

- campos demograficos obligatorios ausentes
- edad fuera del rango publicado
- talla aparentemente introducida en metros
- peso o talla no validos
- valores extremos de peso o IMC
- AX <= 0
- Fres <= 0

Los controles de plausibilidad de talla, peso e IMC son controles tecnicos de calidad de datos y no limites clinicos publicados por Gochicoa-Rangel.

## Ejecutar

Desde esta carpeta:

    python app.py

## Tests

Desde esta carpeta (`desktop/`):

    python -m unittest discover -s tests -v

La suite cubre ecuaciones, validacion y procesamiento Excel.

## Aviso

Herramienta destinada al calculo de valores de referencia y apoyo a investigacion. Los resultados deben interpretarse en su contexto clinico.
