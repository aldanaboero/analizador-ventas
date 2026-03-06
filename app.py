import streamlit as st
import pandas as pd

st.title("Analizador de Ventas")

file = st.file_uploader("Sube un archivo Excel o CSV")

if file:
    df = pd.read_csv(file)
    
    st.write("Datos cargados:")
    st.dataframe(df)

    st.subheader("Gráfico automático")
    st.line_chart(df)
