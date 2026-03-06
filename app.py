import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml

# --- Login de usuarios ---
# Puedes crear un archivo usuarios.yaml si quieres que sea más profesional
usuarios = {
    "usernames": {
        "aldana": {
            "name": "Aldana",
            "password": "1234"
        },
        "admin": {
            "name": "Admin",
            "password": "admin"
        }
    }
}

authenticator = stauth.Authenticate(
    usuarios['usernames'],
    "cookie_name",
    "signature_key",
    cookie_expiry_days=1
)

nombre, estado, username = authenticator.login("Login", "main")

# Solo mostrar la app si el login es correcto
if estado:

    st.set_page_config(
        page_title="Dashboard Inteligente de Ventas",
        page_icon="📊",
        layout="wide"
    )

    # --- Estilo profesional ---
    st.markdown("""
    <style>
    .main {background-color: #F5F7FB;}
    .stSidebar {background-color: #FFFFFF;}
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Dashboard Inteligente de Ventas")
    st.write("Sube un archivo Excel o CSV para analizar tus datos automáticamente.")

    # --- Subir archivo ---
    file = st.file_uploader("Sube tu archivo", type=["csv","xlsx"])

    if file is not None:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, encoding="latin1")
        else:
            df = pd.read_excel(file)

        st.success("Archivo cargado correctamente")

        # --- Menú lateral ---
        menu = st.sidebar.selectbox(
            "📊 Menú",
            ["Dashboard", "Datos", "Gráficos", "Predicción", "Preguntas IA"]
        )

        # --- Sección Dashboard ---
        if menu == "Dashboard":
            st.header("📊 Resumen general")
            col1, col2, col3 = st.columns(3)
            if "Total" in df.columns:
                with col1:
                    st.metric("💰 Ventas Totales", f"${df['Total'].sum():,.0f}")
            if "Cantidad" in df.columns:
                with col2:
                    st.metric("📦 Productos vendidos", df["Cantidad"].sum())
            if "Ciudad" in df.columns:
                with col3:
                    st.metric("🏙 Ciudades", df["Ciudad"].nunique())

        # --- Sección Datos ---
        if menu == "Datos":
            st.header("📋 Datos del archivo")
            st.dataframe(df)

        # --- Sección Gráficos ---
        if menu == "Gráficos":
            st.header("📈 Visualización de datos")
            col4, col5 = st.columns(2)
            if "Producto" in df.columns and "Total" in df.columns:
                with col4:
                    ventas_producto = df.groupby("Producto")["Total"].sum()
                    st.subheader("Ventas por producto")
                    st.bar_chart(ventas_producto)
            if "Ciudad" in df.columns and "Total" in df.columns:
                with col5:
                    ventas_ciudad = df.groupby("Ciudad")["Total"].sum()
                    st.subheader("Ventas por ciudad")
                    st.bar_chart(ventas_ciudad)

        # --- Sección Predicción simple ---
        if menu == "Predicción":
            st.header("🔮 Predicción simple de ventas")
            if "Total" in df.columns:
                promedio = df["Total"].mean()
                st.write("Promedio de ventas:", round(promedio,2))
                meses = st.slider("Meses a predecir", 1, 12)
                prediccion = promedio * meses
                st.success(f"Ventas estimadas para {meses} meses: ${prediccion:,.0f}")

        # --- Sección Preguntas con IA ---
        if menu == "Preguntas IA":
            st.header("🤖 Pregúntale algo a tus datos")
            pregunta = st.text_input("Escribe tu pregunta sobre los datos")
            if pregunta:
                # Solo respuestas básicas por ahora
                if "Producto" in df.columns and "Total" in df.columns:
                    producto_top = df.groupby("Producto")["Total"].sum().idxmax()
                    producto_min = df.groupby("Producto")["Total"].sum().idxmin()
                    if "mas vendido" in pregunta.lower():
                        st.success(f"El producto más vendido es: {producto_top}")
                    elif "menos vendido" in pregunta.lower():
                        st.success(f"El producto menos vendido es: {producto_min}")
                    else:
                        st.info("Todavía estoy aprendiendo. Intenta preguntar por el producto más vendido.")
                if "Ciudad" in df.columns and "Total" in df.columns:
                    ciudad_top = df.groupby("Ciudad")["Total"].sum().idxmax()
                    if "ciudad" in pregunta.lower() or "ventas ciudad" in pregunta.lower():
                        st.success(f"La ciudad con más ventas es: {ciudad_top}")

elif estado == False:
    st.error("Usuario o contraseña incorrectos")
elif estado == None:
    st.warning("Ingresa tu usuario y contraseña")
