import streamlit as st
import pandas as pd

st.title("📊 Analizador de Ventas")

file = st.file_uploader("Sube un archivo CSV o Excel", type=["csv","xlsx"])

if file is not None:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file, encoding="latin1")
    else:
        df = pd.read_excel(file)

    st.subheader("📋 Datos del archivo")
    st.dataframe(df)

    st.subheader("📈 Estadísticas")
    st.write(df.describe())

    st.subheader("📊 Gráfico de ventas")

    if "Producto" in df.columns and "Total" in df.columns:
        ventas = df.groupby("Producto")["Total"].sum()
        st.bar_chart(ventas)
