from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from equations import (
    gochicoa_r5r20,
    gochicoa_x5,
    gochicoa_fres,
    gochicoa_ax,
)

from excel_processor import (
    process_excel,
    create_template,
)

from validation import (
    validate_demographics,
    validate_oscillometry_value,
)


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


def format_number(value, decimals=3):
    return f"{value:.{decimals}f}"


def set_result(
    value_label,
    lln_label,
    uln_label,
    z_label,
    status_label,
    result,
    decimals=3,
):
    value_label.configure(
        text=format_number(result["predicted"], decimals)
    )

    lln_label.configure(
        text="LLN: "
        + format_number(result["lln"], decimals)
    )

    uln_label.configure(
        text="ULN: "
        + format_number(result["uln"], decimals)
    )

    z_label.configure(
        text=f"z = {format_number(result['z_score'], 2)}"
    )

    if result["abnormal"]:
        status_label.configure(
            text="ALTERADO",
            text_color="#B42318",
            fg_color="#FEE4E2",
        )
    else:
        status_label.configure(
            text="NORMAL",
            text_color="#067647",
            fg_color="#D1FADF",
        )


def reset_result(
    value_label,
    lln_label,
    uln_label,
    z_label,
    status_label,
):
    value_label.configure(text="-")
    lln_label.configure(text="LLN: -")
    uln_label.configure(text="ULN: -")
    z_label.configure(text="z = -")

    status_label.configure(
        text="SIN CALCULAR",
        text_color="#667085",
        fg_color="#F2F4F7",
    )


def set_not_introduced(
    value_label,
    lln_label,
    uln_label,
    z_label,
    status_label,
):
    value_label.configure(text="-")
    lln_label.configure(text="LLN: -")
    uln_label.configure(text="ULN: -")
    z_label.configure(text="z = -")

    status_label.configure(
        text="NO INTRODUCIDO",
        text_color="#475467",
        fg_color="#F2F4F7",
    )


def calculate():
    bmi_value.configure(text="-")

    warning_label.configure(
        text="",
        fg_color="transparent",
        text_color="#667085",
    )

    reset_result(
        r5r20_predicted,
        r5r20_lln,
        r5r20_uln,
        r5r20_z,
        r5r20_status,
    )

    reset_result(
        x5_predicted,
        x5_lln,
        x5_uln,
        x5_z,
        x5_status,
    )

    reset_result(
        fres_predicted,
        fres_lln,
        fres_uln,
        fres_z,
        fres_status,
    )

    reset_result(
        ax_predicted,
        ax_lln,
        ax_uln,
        ax_z,
        ax_status,
    )

    sex = sex_var.get()

    demographics = validate_demographics(
        sex=sex,
        age=age_entry.get(),
        height_cm=height_entry.get(),
        weight_kg=weight_entry.get(),
    )

    if demographics["errors"]:
        messagebox.showerror(
            "Datos no v?lidos",
            "\n".join(demographics["errors"]),
        )
        return

    if demographics["warnings"]:
        warning_label.configure(
            text=(
                "ADVERTENCIA: "
                + " | ".join(demographics["warnings"])
            ),
            text_color="#B54708",
            fg_color="#FFFAEB",
        )

    age = demographics["age"]
    height = demographics["height_cm"]
    weight = demographics["weight_kg"]
    bmi = demographics["bmi"]

    try:
        r5r20_value = validate_oscillometry_value(
            "R5_R20",
            r5r20_entry.get(),
        )

        x5_value = validate_oscillometry_value(
            "X5",
            x5_entry.get(),
        )

        fres_value = validate_oscillometry_value(
            "Fres",
            fres_entry.get(),
        )

        ax_value = validate_oscillometry_value(
            "AX",
            ax_entry.get(),
        )

    except ValueError as exc:
        messagebox.showerror(
            "Datos no v?lidos",
            str(exc),
        )
        return

    bmi_value.configure(
        text=format_number(bmi, 2)
    )

    if r5r20_value is None:
        set_not_introduced(
            r5r20_predicted,
            r5r20_lln,
            r5r20_uln,
            r5r20_z,
            r5r20_status,
        )
    else:
        result = gochicoa_r5r20(
            age,
            sex,
            height,
            weight,
            r5r20_value,
        )

        set_result(
            r5r20_predicted,
            r5r20_lln,
            r5r20_uln,
            r5r20_z,
            r5r20_status,
            result,
        )

    if x5_value is None:
        set_not_introduced(
            x5_predicted,
            x5_lln,
            x5_uln,
            x5_z,
            x5_status,
        )
    else:
        result = gochicoa_x5(
            age,
            sex,
            height,
            weight,
            x5_value,
        )

        set_result(
            x5_predicted,
            x5_lln,
            x5_uln,
            x5_z,
            x5_status,
            result,
        )

    if fres_value is None:
        set_not_introduced(
            fres_predicted,
            fres_lln,
            fres_uln,
            fres_z,
            fres_status,
        )
    else:
        result = gochicoa_fres(
            age,
            sex,
            height,
            weight,
            fres_value,
        )

        set_result(
            fres_predicted,
            fres_lln,
            fres_uln,
            fres_z,
            fres_status,
            result,
            decimals=2,
        )

    if ax_value is None:
        set_not_introduced(
            ax_predicted,
            ax_lln,
            ax_uln,
            ax_z,
            ax_status,
        )
    else:
        result = gochicoa_ax(
            age,
            sex,
            height,
            weight,
            ax_value,
        )

        set_result(
            ax_predicted,
            ax_lln,
            ax_uln,
            ax_z,
            ax_status,
            result,
        )


def process_excel_from_ui():
    input_file = filedialog.askopenfilename(
        title="Seleccionar Excel con datos de oscilometr?a",
        filetypes=[
            ("Archivos Excel", "*.xlsx"),
            ("Todos los archivos", "*.*"),
        ],
    )

    if not input_file:
        return

    try:
        result = process_excel(
            Path(input_file)
        )

        messagebox.showinfo(
            "Proceso completado",
            (
                "El archivo se ha procesado correctamente.\n\n"
                "Se ha creado la hoja "
                f"'{result['results_sheet']}' "
                "dentro del mismo Excel.\n\n"
                f"Pacientes procesados: {result['processed']}\n"
                f"Filas con errores: {result['errors']}\n\n"
                f"Archivo:\n{result['output_path']}"
            ),
        )

    except PermissionError:
        messagebox.showerror(
            "No se puede guardar el archivo",
            (
                "El Excel parece estar abierto en otra aplicaci?n.\n\n"
                "Ci?rrelo y vuelva a intentarlo."
            ),
        )

    except Exception as exc:
        messagebox.showerror(
            "Error al procesar el Excel",
            str(exc),
        )


def create_template_from_ui():
    if sys.platform.startswith("win"):
        output_file = filedialog.asksaveasfilename(
            title="Guardar plantilla de oscilometría",
            defaultextension=".xlsx",
            initialfile="plantilla_oscilometria.xlsx",
            filetypes=[
                ("Archivo Excel", "*.xlsx"),
            ],
        )

        if not output_file:
            return

        output_file = Path(output_file)

    else:
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta para guardar la plantilla"
        )

        if not folder:
            return

        output_file = Path(folder) / "plantilla_oscilometria.xlsx"

    if output_file.exists():
        overwrite = messagebox.askyesno(
            "El archivo ya existe",
            (
                "Ya existe un archivo con ese nombre.\n\n"
                "¿Quieres reemplazarlo?"
            ),
        )

        if not overwrite:
            return

    try:
        path = create_template(output_file)

        messagebox.showinfo(
            "Plantilla creada",
            (
                "La plantilla se ha creado correctamente.\n\n"
                f"Guardada en:\n{path}"
            ),
        )

    except Exception as exc:
        messagebox.showerror(
            "Error al crear la plantilla",
            str(exc),
        )


def add_input(parent, label, row):
    ctk.CTkLabel(
        parent,
        text=label,
        font=ctk.CTkFont(size=14),
        text_color="#344054",
    ).grid(
        row=row,
        column=0,
        sticky="w",
        padx=(0, 18),
        pady=5,
    )

    entry = ctk.CTkEntry(
        parent,
        width=190,
        height=38,
        corner_radius=8,
        border_color="#D0D5DD",
    )

    entry.grid(
        row=row,
        column=1,
        sticky="ew",
        pady=5,
    )

    return entry


def create_result_card(parent, column, title):
    card = ctk.CTkFrame(
        parent,
        fg_color="#FFFFFF",
        corner_radius=12,
        border_width=1,
        border_color="#EAECF0",
    )

    card.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=6,
        pady=4,
    )

    ctk.CTkLabel(
        card,
        text=title,
        font=ctk.CTkFont(
            size=15,
            weight="bold",
        ),
        text_color="#344054",
    ).pack(
        anchor="w",
        padx=16,
        pady=(14, 2),
    )

    predicted = ctk.CTkLabel(
        card,
        text="-",
        font=ctk.CTkFont(
            size=27,
            weight="bold",
        ),
        text_color="#101828",
    )

    predicted.pack(
        anchor="w",
        padx=16,
        pady=(4, 2),
    )

    ctk.CTkLabel(
        card,
        text="Valor predicho",
        font=ctk.CTkFont(size=11),
        text_color="#667085",
    ).pack(
        anchor="w",
        padx=16,
    )

    lln = ctk.CTkLabel(
        card,
        text="LLN: -",
        font=ctk.CTkFont(size=12),
        text_color="#475467",
    )

    lln.pack(
        anchor="w",
        padx=16,
        pady=(12, 2),
    )

    uln = ctk.CTkLabel(
        card,
        text="ULN: -",
        font=ctk.CTkFont(size=12),
        text_color="#475467",
    )

    uln.pack(
        anchor="w",
        padx=16,
        pady=(0, 2),
    )

    z_value = ctk.CTkLabel(
        card,
        text="z = -",
        font=ctk.CTkFont(size=12),
        text_color="#475467",
    )

    z_value.pack(
        anchor="w",
        padx=16,
    )

    status = ctk.CTkLabel(
        card,
        text="SIN CALCULAR",
        width=130,
        height=28,
        corner_radius=14,
        fg_color="#F2F4F7",
        text_color="#667085",
        font=ctk.CTkFont(
            size=11,
            weight="bold",
        ),
    )

    status.pack(
        anchor="w",
        padx=16,
        pady=(14, 16),
    )

    return predicted, lln, uln, z_value, status


app = ctk.CTk()

app.title("Calculadora de oscilometría")
app.geometry("1120x780")
app.minsize(1000, 680)

app.configure(
    fg_color="#F8FAFC"
)

app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)


header = ctk.CTkFrame(
    app,
    fg_color="transparent",
)

header.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=34,
    pady=(26, 14),
)

ctk.CTkLabel(
    header,
    text="Calculadora de oscilometría",
    font=ctk.CTkFont(
        size=28,
        weight="bold",
    ),
    text_color="#101828",
).pack(anchor="w")

ctk.CTkLabel(
    header,
    text=(
        "Valores de referencia de Gochicoa-Rangel · "
        "R5-R20, X5, Fres y AX"
    ),
    font=ctk.CTkFont(size=14),
    text_color="#667085",
).pack(
    anchor="w",
    pady=(4, 0),
)


content = ctk.CTkFrame(
    app,
    fg_color="transparent",
)

content.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=34,
    pady=(0, 26),
)

content.grid_columnconfigure(0, weight=0)
content.grid_columnconfigure(1, weight=1)
content.grid_rowconfigure(0, weight=1)


input_panel = ctk.CTkFrame(
    content,
    width=350,
    fg_color="#FFFFFF",
    corner_radius=14,
    border_width=1,
    border_color="#EAECF0",
)

input_panel.grid(
    row=0,
    column=0,
    sticky="ns",
    padx=(0, 16),
)

ctk.CTkLabel(
    input_panel,
    text="Datos del paciente",
    font=ctk.CTkFont(
        size=18,
        weight="bold",
    ),
    text_color="#101828",
).pack(
    anchor="w",
    padx=22,
    pady=(14, 2),
)

ctk.CTkLabel(
    input_panel,
    text="Se acepta coma o punto decimal.",
    font=ctk.CTkFont(size=12),
    text_color="#667085",
).pack(
    anchor="w",
    padx=22,
    pady=(0, 8),
)


form = ctk.CTkFrame(
    input_panel,
    fg_color="transparent",
)

form.pack(
    fill="x",
    padx=22,
)

form.grid_columnconfigure(1, weight=1)


ctk.CTkLabel(
    form,
    text="Sexo",
    font=ctk.CTkFont(size=14),
    text_color="#344054",
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=(0, 18),
    pady=8,
)

sex_var = tk.StringVar(value="Mujer")

sex_menu = ctk.CTkOptionMenu(
    form,
    variable=sex_var,
    values=[
        "Mujer",
        "Hombre",
    ],
    width=190,
    height=38,
    corner_radius=8,
)

sex_menu.grid(
    row=0,
    column=1,
    sticky="ew",
    pady=8,
)


age_entry = add_input(
    form,
    "Edad (años)",
    1,
)

height_entry = add_input(
    form,
    "Talla (cm)",
    2,
)

weight_entry = add_input(
    form,
    "Peso (kg)",
    3,
)


ctk.CTkLabel(
    input_panel,
    text="Oscilometría pre-BD",
    font=ctk.CTkFont(
        size=15,
        weight="bold",
    ),
    text_color="#344054",
).pack(
    anchor="w",
    padx=22,
    pady=(12, 2),
)


osc_form = ctk.CTkFrame(
    input_panel,
    fg_color="transparent",
)

osc_form.pack(
    fill="x",
    padx=22,
)

osc_form.grid_columnconfigure(1, weight=1)


r5r20_entry = add_input(
    osc_form,
    "R5−R20",
    0,
)

x5_entry = add_input(
    osc_form,
    "X5",
    1,
)

fres_entry = add_input(
    osc_form,
    "Fres",
    2,
)


ax_entry = add_input(
    osc_form,
    "AX",
    3,
)


calculate_button = ctk.CTkButton(
    input_panel,
    text="Calcular resultados",
    command=calculate,
    height=44,
    corner_radius=9,
    font=ctk.CTkFont(
        size=14,
        weight="bold",
    ),
)

calculate_button.pack(
    fill="x",
    padx=22,
    pady=(12, 14),
)


right_panel = ctk.CTkFrame(
    content,
    fg_color="transparent",
)

right_panel.grid(
    row=0,
    column=1,
    sticky="nsew",
)

right_panel.grid_columnconfigure(0, weight=1)
right_panel.grid_rowconfigure(1, weight=1)


summary = ctk.CTkFrame(
    right_panel,
    fg_color="#FFFFFF",
    corner_radius=14,
    border_width=1,
    border_color="#EAECF0",
)

summary.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=(0, 14),
)

ctk.CTkLabel(
    summary,
    text="IMC calculado",
    font=ctk.CTkFont(size=13),
    text_color="#667085",
).pack(
    side="left",
    padx=(20, 8),
    pady=16,
)

bmi_value = ctk.CTkLabel(
    summary,
    text="—",
    font=ctk.CTkFont(
        size=18,
        weight="bold",
    ),
    text_color="#101828",
)

bmi_value.pack(
    side="left",
    pady=16,
)


warning_label = ctk.CTkLabel(
    summary,
    text="",
    font=ctk.CTkFont(size=11),
    text_color="#667085",
    fg_color="transparent",
    corner_radius=8,
    wraplength=440,
    justify="left",
)

warning_label.pack(
    side="left",
    padx=(16, 16),
    pady=10,
)


results_panel = ctk.CTkFrame(
    right_panel,
    fg_color="#FFFFFF",
    corner_radius=14,
    border_width=1,
    border_color="#EAECF0",
)

results_panel.grid(
    row=1,
    column=0,
    sticky="nsew",
)

results_panel.grid_columnconfigure(
    (0, 1, 2, 3),
    weight=1,
)

ctk.CTkLabel(
    results_panel,
    text="Resultados",
    font=ctk.CTkFont(
        size=18,
        weight="bold",
    ),
    text_color="#101828",
).grid(
    row=0,
    column=0,
    columnspan=4,
    sticky="w",
    padx=20,
    pady=(18, 8),
)


cards = ctk.CTkFrame(
    results_panel,
    fg_color="transparent",
)

cards.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="ew",
    padx=14,
)

cards.grid_columnconfigure(
    (0, 1, 2, 3),
    weight=1,
)


(
    r5r20_predicted,
    r5r20_lln,
    r5r20_uln,
    r5r20_z,
    r5r20_status,
) = create_result_card(
    cards,
    0,
    "R5-R20",
)


(
    x5_predicted,
    x5_lln,
    x5_uln,
    x5_z,
    x5_status,
) = create_result_card(
    cards,
    1,
    "X5",
)


(
    fres_predicted,
    fres_lln,
    fres_uln,
    fres_z,
    fres_status,
) = create_result_card(
    cards,
    2,
    "Fres",
)


(
    ax_predicted,
    ax_lln,
    ax_uln,
    ax_z,
    ax_status,
) = create_result_card(
    cards,
    3,
    "AX",
)


excel_panel = ctk.CTkFrame(
    results_panel,
    fg_color="#F9FAFB",
    corner_radius=12,
)

excel_panel.grid(
    row=2,
    column=0,
    columnspan=4,
    sticky="ew",
    padx=20,
    pady=(20, 16),
)

excel_panel.grid_columnconfigure(0, weight=1)


ctk.CTkLabel(
    excel_panel,
    text="Procesamiento por lotes",
    font=ctk.CTkFont(
        size=15,
        weight="bold",
    ),
    text_color="#344054",
).grid(
    row=0,
    column=0,
    columnspan=2,
    sticky="w",
    padx=18,
    pady=(16, 2),
)

ctk.CTkLabel(
    excel_panel,
    text=(
        "Carga una cohorte completa o crea una "
        "plantilla preparada para introducir los datos."
    ),
    font=ctk.CTkFont(size=12),
    text_color="#667085",
).grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="w",
    padx=18,
    pady=(0, 12),
)


ctk.CTkButton(
    excel_panel,
    text="Procesar Excel",
    command=process_excel_from_ui,
    height=38,
    corner_radius=8,
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=(18, 8),
    pady=(0, 16),
)


ctk.CTkButton(
    excel_panel,
    text="Crear plantilla Excel",
    command=create_template_from_ui,
    height=38,
    corner_radius=8,
    fg_color="#FFFFFF",
    hover_color="#F2F4F7",
    border_width=1,
    border_color="#D0D5DD",
    text_color="#344054",
).grid(
    row=2,
    column=1,
    sticky="w",
    padx=(0, 18),
    pady=(0, 16),
)


ctk.CTkLabel(
    results_panel,
    text=(
        "Referencia: Gochicoa-Rangel et al. "
        "ERJ Open Research 2023;9:00503-2023"
    ),
    font=ctk.CTkFont(size=11),
    text_color="#98A2B3",
).grid(
    row=3,
    column=0,
    columnspan=4,
    sticky="w",
    padx=20,
    pady=(0, 16),
)


app.mainloop()
