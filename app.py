import streamlit as st
import pandas as pd

st.title("Analizador de Ventas")

file = st.file_uploader("Sube un archivo CSV o Excel", type=["csv","xlsx"])

if file is not None:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file, encoding="latin1")
    else:
        df = pd.read_excel(file)

    st.write("Datos cargados:")
    st.dataframe(df)
