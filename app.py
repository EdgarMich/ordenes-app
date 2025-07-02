
import time
import streamlit as st
import pandas as pd
import re
from datetime import date

# Load Excel
@st.cache_data
def load_data():
    df = pd.read_excel("ordenes.xlsx", sheet_name="Bitácora", header=1)
    df = df.dropna(subset=["No. de Orden"])
    return df

df = load_data()

st.title("📋 Órdenes de Trabajo - Departamento de Diseño")

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filtros")
    status = st.multiselect("Estado", options=df["Status"].dropna().unique())
    prioridad = st.multiselect("Prioridad", options=df["Prioridad"].dropna().unique())
    persona = st.multiselect("Requerido por", options=df["Requerido por"].dropna().unique())

# Apply Filters
filtered_df = df.copy()
if status:
    filtered_df = filtered_df[filtered_df["Status"].isin(status)]
if prioridad:
    filtered_df = filtered_df[filtered_df["Prioridad"].isin(prioridad)]
if persona:
    filtered_df = filtered_df[filtered_df["Requerido por"].isin(persona)]

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# Order Number Generator
def generate_next_order_number(df):
    pattern = r"OTD-MX-(\d+)"
    numbers = []

    for val in df["No. de Orden"].dropna():
        match = re.match(pattern, val)
        if match:
            numbers.append(int(match.group(1)))

    max_number = max(numbers) if numbers else 0
    next_number = max_number + 1
    return f"OTD-MX-{next_number:04d}"

st.header("➕ Agregar Nueva Orden")

# Dropdown values
departamentos = [
    "--- Selecciona ---",
    "Ingeniería",
    "Mantenimiento",
    "NPI",
    "Producción",
    "Programación CNC",
    "Seguridad"
]

tipos_trabajo = [
    "--- Selecciona ---",
    "Dibujo",
    "Fixtura",
    "Impresión 3D",
    "Investigación",
    "Modificación",
    "Otros",
    "PLC"
]

prioridades = ["--- Selecciona ---", "Alta", "Media", "Baja"]

new_no_orden = generate_next_order_number(df)
st.markdown(f"**No. de Orden generado automáticamente:** {new_no_orden}")

with st.form("new_order_form"):
    fecha_requerida = st.date_input("Fecha requerida", value=date.today())
    requerido_por = st.text_input("Requerido por")
    departamento = st.selectbox("Departamento", departamentos)
    fecha_deseada = st.date_input("Fecha deseada", value=date.today())
    prioridad_input = st.selectbox("Prioridad", prioridades)
    tipo_trabajo = st.selectbox("Tipo de trabajo", tipos_trabajo)
    descripcion = st.text_area("Descripción de trabajo")
    proyecto_fixtura = st.text_input("Proyecto / Fixtura (opcional)")
    notas = st.text_area("Notas / Comentarios (opcional)")

    submitted = st.form_submit_button("Guardar Orden")

if submitted:
    missing_fields = []

    if not requerido_por.strip():
        missing_fields.append("Requerido por")
    if departamento == "--- Selecciona ---":
        missing_fields.append("Departamento")
    if prioridad_input == "--- Selecciona ---":
        missing_fields.append("Prioridad")
    if tipo_trabajo == "--- Selecciona ---":
        missing_fields.append("Tipo de trabajo")
    if not descripcion.strip():
        missing_fields.append("Descripción de trabajo")

    if missing_fields:
        st.warning("⚠️ Faltan campos obligatorios: " + ", ".join(missing_fields))
    else:
        new_order = {
            "No. de Orden": new_no_orden,
            "Fecha requerida": fecha_requerida,
            "Requerido por": requerido_por,
            "Departamento": departamento,
            "Fecha deseada": fecha_deseada,
            "Prioridad": prioridad_input,
            "Tipo de trabajo": tipo_trabajo,
            "Descripción de trabajo": descripcion,
            "Proyecto / Fixtura": proyecto_fixtura,
            "Status": "Pendiente",
            "Fecha completada": pd.NaT,
            "Notas / Comentarios": notas
        }

        new_row_df = pd.DataFrame([new_order])
        df = pd.concat([df, new_row_df], ignore_index=True)


        # Save back to Excel
        with pd.ExcelWriter("ordenes.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name="Bitácora", index=False, startrow=1)

        st.success(f"✅ Orden '{new_no_orden}' guardada correctamente!")
        time.sleep(2)  # Wait 2 seconds so the user sees the message
        st.cache_data.clear()  # Clear Excel cache
        st.rerun()  # Reload app and data

=======
# Test

import time
import streamlit as st
import pandas as pd
import re
from datetime import date

# Load Excel
@st.cache_data
def load_data():
    df = pd.read_excel("ordenes.xlsx", sheet_name="Bitácora", header=1)
    df = df.dropna(subset=["No. de Orden"])

    # Format date columns to remove time
    date_columns = ["Fecha requerida", "Fecha deseada", "Fecha completada"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
    return df

df = load_data()

st.title("📋 Órdenes de Trabajo - Departamento de Diseño")

# Sidebar Filters
with st.sidebar:
    st.header("🔍 Filtros")
    status = st.multiselect("Estado", options=df["Status"].dropna().unique())
    prioridad = st.multiselect("Prioridad", options=df["Prioridad"].dropna().unique())
    persona = st.multiselect("Requerido por", options=df["Requerido por"].dropna().unique())

# Apply Filters
filtered_df = df.copy()
if status:
    filtered_df = filtered_df[filtered_df["Status"].isin(status)]
if prioridad:
    filtered_df = filtered_df[filtered_df["Prioridad"].isin(prioridad)]
if persona:
    filtered_df = filtered_df[filtered_df["Requerido por"].isin(persona)]

# Format date columns to only show date (not time)
date_cols = ["Fecha requerida", "Fecha deseada", "Fecha completada"]
for col in date_cols:
    if col in filtered_df.columns:
        filtered_df[col] = pd.to_datetime(filtered_df[col]).dt.date

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# Order Number Generator
def generate_next_order_number(df):
    pattern = r"OTD-MX-(\d+)"
    numbers = []

    for val in df["No. de Orden"].dropna():
        match = re.match(pattern, val)
        if match:
            numbers.append(int(match.group(1)))

    max_number = max(numbers) if numbers else 0
    next_number = max_number + 1
    return f"OTD-MX-{next_number:04d}"

st.header("➕ Agregar Nueva Orden")

# Dropdown values
departamentos = [
    "--- Selecciona ---",
    "Ingeniería",
    "Mantenimiento",
    "NPI",
    "Producción",
    "Programación CNC",
    "Seguridad"
]

tipos_trabajo = [
    "--- Selecciona ---",
    "Dibujo",
    "Fixtura",
    "Impresión 3D",
    "Investigación",
    "Modificación",
    "Otros",
    "PLC"
]

prioridades = ["--- Selecciona ---", "Alta", "Media", "Baja"]

new_no_orden = generate_next_order_number(df)
st.markdown(f"**No. de Orden generado automáticamente:** {new_no_orden}")

with st.form("new_order_form"):
    fecha_requerida = st.date_input("Fecha requerida", value=date.today())
    requerido_por = st.text_input("Requerido por")
    departamento = st.selectbox("Departamento", departamentos)
    fecha_deseada = st.date_input("Fecha deseada", value=date.today())
    prioridad_input = st.selectbox("Prioridad", prioridades)
    tipo_trabajo = st.selectbox("Tipo de trabajo", tipos_trabajo)
    descripcion = st.text_area("Descripción de trabajo")
    proyecto_fixtura = st.text_input("Proyecto / Fixtura (opcional)")
    notas = st.text_area("Notas / Comentarios (opcional)")

    submitted = st.form_submit_button("Guardar Orden")

if submitted:
    missing_fields = []

    if not requerido_por.strip():
        missing_fields.append("Requerido por")
    if departamento == "--- Selecciona ---":
        missing_fields.append("Departamento")
    if prioridad_input == "--- Selecciona ---":
        missing_fields.append("Prioridad")
    if tipo_trabajo == "--- Selecciona ---":
        missing_fields.append("Tipo de trabajo")
    if not descripcion.strip():
        missing_fields.append("Descripción de trabajo")

    if missing_fields:
        st.warning("⚠️ Faltan campos obligatorios: " + ", ".join(missing_fields))
    else:
        new_order = {
            "No. de Orden": new_no_orden,
            "Fecha requerida": fecha_requerida,
            "Requerido por": requerido_por,
            "Departamento": departamento,
            "Fecha deseada": fecha_deseada,
            "Prioridad": prioridad_input,
            "Tipo de trabajo": tipo_trabajo,
            "Descripción de trabajo": descripcion,
            "Proyecto / Fixtura": proyecto_fixtura,
            "Status": "Pendiente",
            "Fecha completada": pd.NaT,
            "Notas / Comentarios": notas
        }

        new_row_df = pd.DataFrame([new_order])
        df = pd.concat([df, new_row_df], ignore_index=True)


        # Save back to Excel
        with pd.ExcelWriter("ordenes.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df.to_excel(writer, sheet_name="Bitácora", index=False, startrow=1)

        st.success(f"✅ Orden '{new_no_orden}' guardada correctamente!")
        time.sleep(2)  # Wait 2 seconds so the user sees the message
        st.cache_data.clear()  # Clear Excel cache
        st.rerun()  # Reload app and data

