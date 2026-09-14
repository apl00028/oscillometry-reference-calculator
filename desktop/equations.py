GOCHICOA_Z_LIMIT = 1.6449


def calculate_bmi(weight_kg, height_cm):
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("Peso y talla deben ser mayores que 0.")

    return weight_kg / (height_cm / 100) ** 2


def encode_sex(sex):
    value = str(sex).strip().lower()

    if value in {"h", "hombre", "male"}:
        return 1.0

    if value in {"m", "mujer", "female", "f"}:
        return 0.0

    raise ValueError("Sexo no válido. Use Hombre o Mujer.")


def gochicoa_r5r20(age, sex, height_cm, weight_kg, observed):
    age = float(age)
    height_cm = float(height_cm)
    weight_kg = float(weight_kg)
    observed = float(observed)

    if not 2.7 <= age <= 90:
        raise ValueError(
            "Edad fuera del rango publicado de Gochicoa-Rangel (2.7-90 años)."
        )

    if age <= 23.55:
        intercept = 0.013349
        age_coefficient = -0.0075403
        rmse = 0.0739
    elif age >= 23.56:
        intercept = -0.18775
        age_coefficient = 0.00099579
        rmse = 0.0348
    else:
        raise ValueError(
            "Edad situada entre los intervalos publicados para R5-R20."
        )

    bmi = calculate_bmi(weight_kg, height_cm)
    sex_numeric = encode_sex(sex)

    predicted = (
        intercept
        + 0.004813 * sex_numeric
        + age_coefficient * age
        + 43.014247 / height_cm
        - 1.794838 / bmi
    )

    lln = predicted - GOCHICOA_Z_LIMIT * rmse
    uln = predicted + GOCHICOA_Z_LIMIT * rmse
    z_score = (observed - predicted) / rmse

    return {
        "observed": observed,
        "predicted": predicted,
        "rmse": rmse,
        "lln": lln,
        "uln": uln,
        "z_score": z_score,
        "abnormal": observed > uln,
    }


def gochicoa_x5(age, sex, height_cm, weight_kg, observed):
    age = float(age)
    height_cm = float(height_cm)
    weight_kg = float(weight_kg)
    observed = float(observed)

    if not 2.7 <= age <= 90:
        raise ValueError(
            "Edad fuera del rango publicado de Gochicoa-Rangel (2.7-90 años)."
        )

    if age <= 5.29:
        intercept = -0.089509
        age_coefficient = 0.043369
        rmse = 0.0922
    elif 5.30 <= age <= 18.68:
        intercept = 0.1172
        age_coefficient = 0.0043487
        rmse = 0.0575
    elif age >= 18.69:
        intercept = 0.19728
        age_coefficient = 0.00006377
        rmse = 0.0408
    else:
        raise ValueError(
            "Edad situada entre los intervalos publicados para X5."
        )

    bmi = calculate_bmi(weight_kg, height_cm)
    sex_numeric = encode_sex(sex)

    predicted = (
        intercept
        + 0.009133 * sex_numeric
        + age_coefficient * age
        - 57.924822 / height_cm
        + 1.090394 / bmi
    )

    lln = predicted - GOCHICOA_Z_LIMIT * rmse
    uln = predicted + GOCHICOA_Z_LIMIT * rmse
    z_score = (observed - predicted) / rmse

    return {
        "observed": observed,
        "predicted": predicted,
        "rmse": rmse,
        "lln": lln,
        "uln": uln,
        "z_score": z_score,
        "abnormal": observed < lln,
    }


def gochicoa_fres(age, sex, height_cm, weight_kg, observed):
    age = float(age)
    height_cm = float(height_cm)
    weight_kg = float(weight_kg)
    observed = float(observed)

    if not 2.7 <= age <= 90:
        raise ValueError(
            "Edad fuera del rango publicado de Gochicoa-Rangel (2.7-90 años)."
        )

    if age <= 9.69:
        intercept = 3.63228
        age_coefficient = 0.14349
        rmse = 2.71
    elif 9.70 <= age <= 20.98:
        intercept = 7.518
        age_coefficient = -0.2571
        rmse = 3.20
    elif age >= 20.99:
        intercept = 1.2542
        age_coefficient = 0.041179
        rmse = 3.89
    else:
        raise ValueError(
            "Edad situada entre los intervalos publicados para Fres."
        )

    bmi = calculate_bmi(weight_kg, height_cm)
    sex_numeric = encode_sex(sex)

    predicted = (
        intercept
        + 0.07493 * sex_numeric
        + age_coefficient * age
        + 2781.55206 / height_cm
        - 99.15807 / bmi
    )

    lln = predicted - GOCHICOA_Z_LIMIT * rmse
    uln = predicted + GOCHICOA_Z_LIMIT * rmse
    z_score = (observed - predicted) / rmse

    return {
        "observed": observed,
        "predicted": predicted,
        "rmse": rmse,
        "lln": lln,
        "uln": uln,
        "z_score": z_score,
        "abnormal": observed > uln,
    }


def gochicoa_ax(age, sex, height_cm, weight_kg, observed):
    import math

    age = float(age)
    height_cm = float(height_cm)
    weight_kg = float(weight_kg)
    observed = float(observed)

    if not 2.7 <= age <= 90:
        raise ValueError(
            "Edad fuera del rango publicado de Gochicoa-Rangel (2.7-90 años)."
        )

    if observed <= 0:
        raise ValueError(
            "AX debe ser mayor que 0 porque la ecuación utiliza logaritmo natural."
        )

    if age <= 6.98:
        intercept = -3.42268
        age_coefficient = 0.10429
        rmse = 0.366
    elif 6.99 <= age <= 23.21:
        intercept = -2.367
        age_coefficient = -0.046624
        rmse = 0.461
    elif age >= 23.22:
        intercept = -3.597
        age_coefficient = 0.0063497
        rmse = 0.621
    else:
        raise ValueError(
            "Edad situada entre los intervalos publicados para AX."
        )

    bmi = calculate_bmi(weight_kg, height_cm)
    sex_numeric = encode_sex(sex)

    log_predicted = (
        intercept
        - 0.06776 * sex_numeric
        + age_coefficient * age
        + 544.962 / height_cm
        - 18.97076 / bmi
    )

    predicted = math.exp(log_predicted)

    lln = math.exp(
        math.log(predicted)
        - GOCHICOA_Z_LIMIT * rmse
    )

    uln = math.exp(
        math.log(predicted)
        + GOCHICOA_Z_LIMIT * rmse
    )

    z_score = (
        math.log(observed)
        - math.log(predicted)
    ) / rmse

    return {
        "observed": observed,
        "predicted": predicted,
        "rmse": rmse,
        "lln": lln,
        "uln": uln,
        "z_score": z_score,
        "abnormal": observed > uln,
    }
