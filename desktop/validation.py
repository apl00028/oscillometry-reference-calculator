from math import isfinite

from equations import calculate_bmi, encode_sex


GOCHICOA_AGE_MIN = 2.7
GOCHICOA_AGE_MAX = 90.0


def parse_number(value, label):
    if value is None or str(value).strip() == "":
        raise ValueError(f"Falta {label}.")

    if isinstance(value, (int, float)):
        number = float(value)
    else:
        try:
            number = float(
                str(value).strip().replace(",", ".")
            )
        except ValueError as exc:
            raise ValueError(
                f"{label} no es un número válido: {value}"
            ) from exc

    if not isfinite(number):
        raise ValueError(
            f"{label} no es un número finito."
        )

    return number


def parse_optional_number(value, label):
    if value is None or str(value).strip() == "":
        return None

    return parse_number(value, label)


def validate_demographics(
    sex,
    age,
    height_cm,
    weight_kg,
):
    errors = []
    warnings = []

    try:
        encode_sex(sex)
    except ValueError:
        errors.append(
            "Sexo no válido. Seleccione Mujer u Hombre."
        )

    try:
        age = parse_number(age, "Edad")
    except ValueError as exc:
        errors.append(str(exc))
        age = None

    try:
        height_cm = parse_number(
            height_cm,
            "Talla",
        )
    except ValueError as exc:
        errors.append(str(exc))
        height_cm = None

    try:
        weight_kg = parse_number(
            weight_kg,
            "Peso",
        )
    except ValueError as exc:
        errors.append(str(exc))
        weight_kg = None

    if age is not None:
        if not GOCHICOA_AGE_MIN <= age <= GOCHICOA_AGE_MAX:
            errors.append(
                "Edad fuera del rango publicado de "
                "Gochicoa-Rangel (2,7-90 años)."
            )

    if height_cm is not None:
        if height_cm <= 0:
            errors.append(
                "La talla debe ser mayor que 0."
            )
        elif 0.8 <= height_cm <= 2.5:
            errors.append(
                "La talla parece estar expresada en metros. "
                "Introduzca centímetros, por ejemplo 165 en vez de 1,65."
            )
        elif height_cm < 80 or height_cm > 220:
            warnings.append(
                "Talla fuera del rango habitual; revise que esté "
                "expresada en centímetros."
            )

    if weight_kg is not None:
        if weight_kg <= 0:
            errors.append(
                "El peso debe ser mayor que 0."
            )
        elif weight_kg < 20 or weight_kg > 250:
            warnings.append(
                "Peso fuera del rango habitual; revise el valor introducido."
            )

    bmi = None

    if (
        not errors
        and height_cm is not None
        and weight_kg is not None
    ):
        bmi = calculate_bmi(
            weight_kg,
            height_cm,
        )

        if bmi < 12 or bmi > 60:
            warnings.append(
                f"IMC calculado de {bmi:.1f}, fuera del rango habitual; "
                "revise peso y talla."
            )

    return {
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "bmi": bmi,
        "warnings": warnings,
        "errors": errors,
    }


def validate_oscillometry_value(
    parameter,
    value,
):
    value = parse_optional_number(
        value,
        parameter,
    )

    if value is None:
        return None

    if parameter == "AX" and value <= 0:
        raise ValueError(
            "AX debe ser mayor que 0."
        )

    if parameter == "Fres" and value <= 0:
        raise ValueError(
            "Fres debe ser mayor que 0."
        )

    return value
