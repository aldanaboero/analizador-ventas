import streamlit as st
import pandas as pd
from pandasai import SmartDataframe

st.title("🤖 Analizador Inteligente de Excel")

file = st.file_uploader("Sube un archivo CSV o Excel", type=["csv","xlsx"])

if file is not None:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file, encoding="latin1")
    else:
        df = pd.read_excel(file)

    st.subheader("📋 Datos cargados")
    st.dataframe(df)

    st.subheader("💬 Pregunta algo sobre tus datos")

    pregunta = st.text_input("Ejemplo: ¿Cuál es el producto más vendido?")

    if pregunta:

        sdf = SmartDataframe(df)

        respuesta = sdf.chat(pregunta)

        st.write("### 🤖 Respuesta:")
        st.write(respuesta)
