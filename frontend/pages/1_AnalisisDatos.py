import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Configuración de la Página ---
st.set_page_config(page_title="Análisis de Datos", page_icon="📊", layout="wide")
st.title("📊 Análisis Exploratorio de Datos (EDA)")

st.markdown("""
Esta página muestra un análisis visual de los datos utilizados para entrenar el modelo.
A diferencia de la página de predicción, aquí sí cargamos el dataset para poder explorarlo.
""")

# --- Carga de Datos con Caché ---
# Usamos un decorador de caché para que Streamlit no tenga que recargar el archivo
# cada vez que interactuamos con la página. Es mucho más eficiente.
@st.cache_data
def load_data():
    """Carga los datos desde el archivo train.csv"""
    try:
        # Asumimos que la app se ejecuta desde la raíz del proyecto
        data_path = os.path.join("datasets", "train.csv")
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        st.error("No se pudo encontrar el archivo 'train.csv' en la carpeta 'datasets'.")
        st.info("Asegúrate de que la aplicación se ejecuta desde la carpeta raíz del proyecto.")
        return None


# Cargamos los datos usando nuestra función cacheada
df = load_data()

# Si la carga de datos fue exitosa, mostramos los gráficos
if df is not None:
    
    # --- Resumen de Datos ---
    st.header("Vistazo General y Estadísticas")
    st.write("Primeras 5 filas del dataset:")
    st.dataframe(df.head())
    
    st.write("Estadísticas descriptivas de las columnas numéricas:")
    st.dataframe(df.describe())

    st.markdown("---")

    # --- Visualizaciones ---
    st.header("Visualizaciones Clave")

    # Usamos columnas para organizar mejor los gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico 1: Distribución de la Satisfacción
        st.subheader("1. Distribución de Satisfacción")
        fig1, ax1 = plt.subplots()
        sns.countplot(x='satisfaction', data=df, ax=ax1, palette='viridis', hue='satisfaction', legend=False)
        ax1.set_title('Distribución de Satisfacción')
        st.pyplot(fig1)
        st.write("Observamos un ligero desbalance, con más pasajeros 'neutral or dissatisfied' que 'satisfied'.")

    with col2:
        # Gráfico 2: Satisfacción por Clase de Vuelo
        st.subheader("2. Satisfacción por Clase")
        fig2, ax2 = plt.subplots()
        sns.countplot(x='Class', hue='satisfaction', data=df, ax=ax2, palette='magma')
        ax2.set_title('Satisfacción según la Clase de Vuelo')
        st.pyplot(fig2)
        st.write("Clara tendencia: la clase 'Business' tiene una proporción mucho mayor de pasajeros satisfechos.")

    st.markdown("---")
    
    col3, col4 = st.columns(2)

    with col3:
        # Gráfico 3: Histograma de Edad
        st.subheader("3. Histograma de Edades")
        fig3, ax3 = plt.subplots()
        sns.histplot(df['Age'], kde=True, ax=ax3, bins=30, color='skyblue')
        ax3.set_title('Distribución de Edades')
        st.pyplot(fig3)
        st.write("La mayoría de pasajeros se concentran entre los 20 y 60 años.")

    with col4:
        # Gráfico 4 (NUEVO): Box Plot de Distancia de Vuelo
        st.subheader("4. Distancia de Vuelo vs Satisfacción")
        fig4, ax4 = plt.subplots()
        sns.boxplot(x='satisfaction', y='Flight Distance', data=df, ax=ax4, palette='coolwarm', hue='satisfaction', legend=False)
        ax4.set_title('Distribución de Distancia de Vuelo por Satisfacción')
        st.pyplot(fig4)
        st.write("Los pasajeros satisfechos tienden a tener una mediana de distancia de vuelo ligeramente mayor.")

    st.markdown("---")

    # Gráfico 5 (NUEVO): Mapa de Calor de Correlaciones
    st.header("Mapa de Calor de Correlaciones")
    st.write("""
    Este mapa muestra la correlación de Pearson entre las variables numéricas. 
    Un valor cercano a 1 (azul oscuro) significa una fuerte correlación positiva.
    Un valor cercano a -1 (rojo oscuro) significa una fuerte correlación negativa.
    Nos interesa especialmente la última fila/columna, que muestra la correlación con 'satisfaction'.
    """)
    
    # Preparamos los datos para el mapa de calor
    df_corr = df.select_dtypes(include=['number']).copy()
    df_corr['satisfaction'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)
    
    fig5, ax5 = plt.subplots(figsize=(16, 12))
    sns.heatmap(df_corr.corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax5, annot_kws={"size": 8})
    ax5.set_title('Mapa de Calor de Correlaciones', fontsize=16)
    st.pyplot(fig5)
    st.write("Observaciones clave: 'Online boarding', 'Inflight entertainment', y 'Seat comfort' tienen algunas de las correlaciones positivas más altas con la satisfacción.")
