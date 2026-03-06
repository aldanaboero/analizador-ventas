import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

# -----------------------------
# USUARIOS Y CONTRASEÑAS
# -----------------------------

credentials = {
    "usernames": {
        "aldana": {
            "name": "Aldana",
            "password": "1234"
        },
        "admin": {
            "name": "Administrador",
            "password": "admin"
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "cookie_dashboard",
    "abcdef",
    cookie_expiry_days=1
)

# -----------------------------
# LOGIN
# -----------------------------

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:

    authenticator.logout("Cerrar sesión", "sidebar")

    st.set_page_config(
        page_title="Dashboard de Ventas",
        page_icon="📊",
        layout="wide"
    )

    # -----------------------------
    # ESTILO
    # -----------------------------

    st.markdown("""
    <style>
    .main {background-color: #F5F7FB;}
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Dashboard Inteligente de Ventas")

    file = st.file_uploader("Sube tu archivo Excel o CSV", type=["csv","xlsx"])

    if file:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.success("Archivo cargado correctamente")

        menu = st.sidebar.selectbox(
            "Menú",
            ["Dashboard","Datos","Gráficos"]
        )

        # -----------------------------
        # DASHBOARD
        # -----------------------------

        if menu == "Dashboard":

            st.header("Resumen")

            col1, col2 = st.columns(2)

            if "Total" in df.columns:
                col1.metric("Ventas Totales", f"${df['Total'].sum():,.0f}")

            if "Cantidad" in df.columns:
                col2.metric("Productos Vendidos", df["Cantidad"].sum())

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
                ventas = df.groupby("Producto")["Total"].sum()
                st.bar_chart(ventas)

            if "Ciudad" in df.columns and "Total" in df.columns:
                ciudad = df.groupby("Ciudad")["Total"].sum()
                st.bar_chart(ciudad)

elif authentication_status == False:
    st.error("Usuario o contraseña incorrectos")

elif authentication_status == None:
    st.warning("Ingrese usuario y contraseña")
