import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# -----------------------------
# USUARIOS
# -----------------------------
credentials = {
    "usernames": {
        "aldana": {"name": "Aldana", "password": "1234"},
        "admin": {"name": "Admin", "password": "admin"}
    }
}

# -----------------------------
# AUTENTICADOR
# -----------------------------
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="app_dashboard_cookie",
    key="abcdef",
    cookie_expiry_days=1
)

# -----------------------------
# LOGIN
# -----------------------------
login_info = authenticator.login("Login")  # Nueva forma

if login_info["authentication_status"]:

    authenticator.logout("Cerrar sesión")

    st.set_page_config(
        page_title="Dashboard Inteligente de Ventas",
        page_icon="📊",
        layout="wide"
    )

    st.markdown("""
    <style>
    .main {background-color: #F5F7FB;}
    .stSidebar {background-color: #FFFFFF;}
    </style>
    """, unsafe_allow_html=True)

    st.title(f"📊 Bienvenida {login_info['name']}")

    # -----------------------------
    # SUBIR ARCHIVO
    # -----------------------------
    file = st.file_uploader("Sube tu archivo Excel o CSV", type=["csv","xlsx"])

    if file:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.success("Archivo cargado correctamente")

        # -----------------------------
        # MENÚ LATERAL
        # -----------------------------
        menu = st.sidebar.selectbox(
            "Menú",
            ["Dashboard","Datos","Gráficos","Predicción","Preguntas IA"]
        )

        # -----------------------------
        # DASHBOARD
        # -----------------------------
        if menu == "Dashboard":
            st.header("Resumen")
            col1, col2, col3 = st.columns(3)
            if "Total" in df.columns:
                col1.metric("Ventas Totales", f"${df['Total'].sum():,.0f}")
            if "Cantidad" in df.columns:
                col2.metric("Productos Vendidos", df["Cantidad"].sum())
            if "Ciudad" in df.columns:
                col3.metric("Ciudades", df["Ciudad"].nunique())

        # -----------------------------
        # DATOS
        # -----------------------------
        if menu == "Datos":
            st.header("Datos cargados")
            st.dataframe(df)

        # -----------------------------
        # GRÁFICOS
        # -----------------------------
        if menu == "Gráficos":
            st.header("Visualización")
            if "Producto" in df.columns and "Total" in df.columns:
                ventas_producto = df.groupby("Producto")["Total"].sum()
                st.subheader("Ventas por producto")
                st.bar_chart(ventas_producto)
            if "Ciudad" in df.columns and "Total" in df.columns:
                ventas_ciudad = df.groupby("Ciudad")["Total"].sum()
                st.subheader("Ventas por ciudad")
                st.bar_chart(ventas_ciudad)

        # -----------------------------
        # PREDICCIÓN SIMPLE
        # -----------------------------
        if menu == "Predicción":
            st.header("Predicción simple de ventas")
            if "Total" in df.columns:
                promedio = df["Total"].mean()
                st.write("Promedio de ventas:", round(promedio,2))
                meses = st.slider("Meses a predecir", 1, 12)
                prediccion = promedio * meses
                st.success(f"Ventas estimadas para {meses} meses: ${prediccion:,.0f}")

        # -----------------------------
        # PREGUNTAS CON IA SIMPLIFICADA
        # -----------------------------
        if menu == "Preguntas IA":
            st.header("Pregúntale algo a tus datos")
            pregunta = st.text_input("Escribe tu pregunta sobre los datos")
            if pregunta:
                if "Producto" in df.columns and "Total" in df.columns:
                    top = df.groupby("Producto")["Total"].sum().idxmax()
                    mino = df.groupby("Producto")["Total"].sum().idxmin()
                    if "mas vendido" in pregunta.lower():
                        st.success(f"El producto más vendido es: {top}")
                    elif "menos vendido" in pregunta.lower():
                        st.success(f"El producto menos vendido es: {mino}")
                    else:
                        st.info("Pregunta por el producto más vendido o menos vendido.")
                if "Ciudad" in df.columns and "Total" in df.columns:
                    ciudad_top = df.groupby("Ciudad")["Total"].sum().idxmax()
                    if "ciudad" in pregunta.lower():
                        st.success(f"La ciudad con más ventas es: {ciudad_top}")

elif login_info["authentication_status"] == False:
    st.error("Usuario o contraseña incorrectos")
elif login_info["authentication_status"] == None:
    st.warning("Ingrese usuario y contraseña")
