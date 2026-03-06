import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Analizador Inteligente de Datos",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analizador Inteligente de Ventas")
st.write("Sube un archivo Excel o CSV y analiza tus datos automáticamente.")

file = st.file_uploader("Sube tu archivo", type=["csv","xlsx"])

if file is not None:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file, encoding="latin1")
    else:
        df = pd.read_excel(file)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Datos")
        st.dataframe(df)

    with col2:
        st.subheader("📊 Estadísticas")
        st.write(df.describe())

    st.subheader("📈 Visualización")

    columnas_numericas = df.select_dtypes(include="number").columns

    if len(columnas_numericas) > 0:
        columna = st.selectbox("Selecciona una columna", columnas_numericas)
        st.bar_chart(df[columna])
