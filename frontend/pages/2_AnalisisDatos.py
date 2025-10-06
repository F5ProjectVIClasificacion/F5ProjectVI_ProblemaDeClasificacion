import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Análisis de Datos", page_icon="📊")
st.title("📊 Análisis Exploratorio de Datos")

# Cargar datos
@st.cache_data
def load_data():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_path = os.path.join(project_root, 'datasets', 'train.csv')
    return pd.read_csv(data_path)

try:
    df = load_data()

    st.header("Distribución de la Satisfacción del Cliente")
    fig, ax = plt.subplots()
    sns.countplot(x='satisfaction', data=df, ax=ax)
    st.pyplot(fig)

    st.header("Satisfacción por Clase de Vuelo")
    fig, ax = plt.subplots()
    sns.countplot(x='Class', hue='satisfaction', data=df, ax=ax)
    st.pyplot(fig)

    st.header("Distribución de la Edad")
    fig, ax = plt.subplots()
    sns.histplot(df['Age'], kde=True, ax=ax)
    st.pyplot(fig)

except FileNotFoundError:
    st.error("No se pudo encontrar el archivo 'train.csv' en la carpeta 'datasets'.")
