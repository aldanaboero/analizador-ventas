import streamlit as st
import pandas as pd
menu = st.sidebar.selectbox(
    "📊 Menú",
    ["Dashboard", "Datos", "Gráficos", "Predicción"]
)
st.set_page_config(
    page_title="Dashboard Inteligente de Ventas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Inteligente de Ventas")
st.write("Sube un archivo Excel o CSV para analizar tus datos automáticamente.")

file = st.file_uploader("Sube tu archivo", type=["csv","xlsx"])
if menu == "Dashboard":

    st.header("📊 Resumen general")

    col1, col2, col3 = st.columns(3)

    if "Total" in df.columns:
        with col1:
            st.metric("Ventas Totales", f"${df['Total'].sum():,.0f}")

    if "Cantidad" in df.columns:
        with col2:
            st.metric("Productos vendidos", df["Cantidad"].sum())

    if "Ciudad" in df.columns:
        with col3:
            st.metric("Ciudades", df["Ciudad"].nunique())
if file is not None:

    # Leer archivo
    if file.name.endswith(".csv"):
        df = pd.read_csv(file, encoding="latin1")
    else:
        df = pd.read_excel(file)

    st.success("Archivo cargado correctamente")

    # Mostrar datos
    st.subheader("📋 Vista previa de los datos")
    st.dataframe(df)

    # Información del dataset
    st.subheader("ℹ Información del dataset")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Filas", df.shape[0])

    with col2:
        st.metric("Columnas", df.shape[1])

    with col3:
        st.metric("Columnas numéricas", len(df.select_dtypes(include="number").columns))

    st.divider()

    # Filtros
    st.sidebar.header("🔎 Filtros")

    if "Ciudad" in df.columns:
        ciudades = st.sidebar.multiselect(
            "Selecciona ciudad",
            df["Ciudad"].unique(),
            default=df["Ciudad"].unique()
        )

        df = df[df["Ciudad"].isin(ciudades)]

    st.subheader("📊 Métricas principales")

    col4, col5, col6 = st.columns(3)

    if "Total" in df.columns:

        with col4:
            st.metric("💰 Ventas Totales", f"${df['Total'].sum():,.0f}")

        if "Cantidad" in df.columns:
            with col5:
                st.metric("📦 Productos vendidos", df["Cantidad"].sum())

        if "Ciudad" in df.columns:
            with col6:
                st.metric("🏙 Ciudades", df["Ciudad"].nunique())

    st.divider()

    # Gráficos
    col7, col8 = st.columns(2)

    if "Producto" in df.columns and "Total" in df.columns:

        with col7:
            st.subheader("Ventas por producto")
            ventas_producto = df.groupby("Producto")["Total"].sum()
            st.bar_chart(ventas_producto)

    if "Ciudad" in df.columns and "Total" in df.columns:

        with col8:
            st.subheader("Ventas por ciudad")
            ventas_ciudad = df.groupby("Ciudad")["Total"].sum()
            st.bar_chart(ventas_ciudad)

    st.divider()

    # Análisis automático
    st.subheader("🤖 Insights automáticos")

    if "Producto" in df.columns and "Total" in df.columns:

        producto_top = df.groupby("Producto")["Total"].sum().idxmax()
        producto_min = df.groupby("Producto")["Total"].sum().idxmin()

        st.write(f"✅ El producto con más ventas es: **{producto_top}**")
        st.write(f"⚠️ El producto con menos ventas es: **{producto_min}**")

    if "Ciudad" in df.columns and "Total" in df.columns:

        ciudad_top = df.groupby("Ciudad")["Total"].sum().idxmax()
        st.divider()

st.subheader("🤖 Pregúntale algo a tus datos")

pregunta = st.text_input("Escribe tu pregunta sobre los datos")

if pregunta:

    if "Producto" in df.columns and "Total" in df.columns:
        producto_top = df.groupby("Producto")["Total"].sum().idxmax()
        producto_min = df.groupby("Producto")["Total"].sum().idxmin()

        if "mas vendido" in pregunta.lower():
            st.success(f"El producto más vendido es: {producto_top}")

        elif "menos vendido" in pregunta.lower():
            st.success(f"El producto menos vendido es: {producto_min}")

        else:
            st.info("Todavía estoy aprendiendo. Intenta preguntar por el producto más vendido.")

        if menu == "Predicción":

    st.header("🔮 Predicción simple de ventas")

    if "Total" in df.columns:

        promedio = df["Total"].mean()

        st.write("Promedio de ventas:", round(promedio,2))

        meses = st.slider("Meses a predecir", 1, 12)

        prediccion = promedio * meses

        st.success(f"Ventas estimadas para {meses} meses: ${prediccion:,.0f}")

        st.write(f"🏆 La ciudad con más ventas es: **{ciudad_top}**")
