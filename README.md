# Oscillometry Reference Calculator

Desktop and web calculator for oscillometry reference equations based on Gochicoa-Rangel et al.

The project provides two interfaces using the same reference equations:

- Desktop application for Windows, including individual calculation and Excel batch processing.
- Web application that runs entirely in the browser.

## Supported parameters

- R5-R20
- X5
- Fres
- AX

For each available parameter, the calculator provides the predicted value, LLN, ULN, z-score and normal/abnormal classification.

## Repository structure

- desktop/: Python desktop application and Excel processing
- web/: Browser-based static application

## Validation

- Desktop test suite: 33 tests passing
- Web test suite: 10 tests passing
- Web calculations validated against the Python implementation

## Privacy

The web calculator runs locally in the browser. Values entered in the form are not sent to an application backend.

## Scientific reference

Gochicoa-Rangel L, et al. Reference equations using segmented regressions for impulse oscillometry in healthy subjects aged 2.7-90 years. ERJ Open Research. 2023;9:00503-2023.

## Intended use

This software is intended as a reference-calculation and research-support tool. It does not replace clinical interpretation or professional medical judgment.
