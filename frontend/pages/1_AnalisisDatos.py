import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import os

# --- Configuración de la Página ---
st.set_page_config(page_title="Análisis de Datos", page_icon="📊", layout="wide")
st.title("📊 Análisis Exploratorio de Datos (EDA)")

st.markdown("""
Esta página muestra un análisis visual de los datos utilizados para entrenar el modelo.
A diferencia de la página de predicción, aquí sí cargamos el dataset para poder explorarlo.
""")

# --- Carga de Métricas del Modelo Entrenado con Caché ---
@st.cache_data
def load_model_metrics():
    """Carga las métricas del modelo desde metrics.json"""
    try:
        metrics_path = os.path.join("reports", "metrics.json")
        with open(metrics_path, 'r') as f:
            import json
            metrics = json.load(f)
        return metrics
    except FileNotFoundError:
        st.warning("No se pudo encontrar el archivo 'metrics.json' en la carpeta 'reports'.")
        return None
    except json.JSONDecodeError:
        st.error("Error al leer el archivo de métricas.")
        return None

# --- Carga de Datos con Caché ---
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

# Cargamos las métricas del modelo
model_metrics = load_model_metrics()

# Cargamos los datos usando nuestra función cacheada
df = load_data()

# Si la carga de datos fue exitosa, mostramos los gráficos
if df is not None:
    
    # --- Métricas del Modelo Entrenado ---
    st.header("📈 Métricas del Modelo Entrenado")
    if model_metrics is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Precisión (Accuracy)", f"{model_metrics['accuracy']:.4f}")
        with col2:
            st.metric("Precisión", f"{model_metrics['precision']:.4f}")
        with col3:
            st.metric("Recall", f"{model_metrics['recall']:.4f}")
        with col4:
            st.metric("F1-Score", f"{model_metrics['f1']:.4f}")
        
        st.metric("ROC-AUC", f"{model_metrics['roc_auc']:.4f}")
        
        st.success("💡 **Interpretación**: El modelo tiene un rendimiento excelente con métricas superiores al 94% en todas las categorías evaluadas.")
        
        st.markdown("---")
    else:
        st.warning("No se pudieron cargar las métricas del modelo. El modelo puede no haber sido entrenado aún.")
    
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
        # Gráfico 4: Box Plot de Distancia de Vuelo
        st.subheader("4. Distancia de Vuelo vs Satisfacción")
        fig4, ax4 = plt.subplots()
        sns.boxplot(x='satisfaction', y='Flight Distance', data=df, ax=ax4, palette='coolwarm', hue='satisfaction', legend=False)
        ax4.set_title('Distribución de Distancia de Vuelo por Satisfacción')
        st.pyplot(fig4)
        st.write("Los pasajeros satisfechos tienden a tener una mediana de distancia de vuelo ligeramente mayor.")

    st.markdown("---")

    # Información específica del modelo Random Forest utilizado en el proyecto
    st.header("🌳 Implementación de Random Forest en el Proyecto")

    # Mostrar el código específico utilizado
    st.subheader("📁 Archivo de Entrenamiento")
    st.code("""
    # Ubicación: src/train_model.py
    # Función: build_pipeline()

    model = RandomForestClassifier(
        n_estimators=300,        # 300 árboles
        random_state=42,         # Para reproducibilidad
        class_weight="balanced", # Manejo del desbalance
        n_jobs=-1                # Todos los cores disponibles
    )
    """, language="python")

    # Crear columnas para mostrar detalles específicos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ Parámetros Específicos")
        st.write("**Archivo fuente:** `src/train_model.py`")
        st.write("**Función:** `build_pipeline()` - línea 136")
        st.write("**Árboles:** 300 (n_estimators=300)")
        st.write("**Estado aleatorio:** 42 (reproducible)")

    with col2:
        st.subheader("🔧 Configuración del Proyecto")
        st.write("**Balanceo de clases:** Automático (class_weight='balanced')")
        st.write("**Procesamiento:** Paralelo (n_jobs=-1)")
        st.write("**Pipeline integrado:** Sí (con preprocesamiento)")
        st.write("**Evaluación:** Métricas calculadas automáticamente")

    st.markdown("---")

    # Contexto específico del proyecto
    st.subheader("📊 Uso en el Proyecto")
    st.write("""
    **Random Forest se utiliza específicamente para:**

    🔸 **Predecir satisfacción de pasajeros** basado en características como:
       - Clase de vuelo, edad, género
       - Servicios a bordo (wifi, entretenimiento, comida)
       - Tiempo de vuelo y demografía

    🔸 **Pipeline completo incluye:**
       - Carga y limpieza de datos desde `datasets/train.csv`
       - División estratificada (80% entrenamiento, 20% test)
       - Preprocesamiento automático (imputación + escalado + OHE)
       - Entrenamiento del Random Forest con parámetros optimizados
       - Evaluación automática con múltiples métricas

    🔸 **Resultado:** Modelo guardado en `models/satisfaction_model.joblib`
    """)

    st.info("💡 **Implementación específica:** El modelo se entrena ejecutando `python src/train_model.py` y queda disponible para predicciones en tiempo real vía la API FastAPI.")

    # Gráfico 5: Matriz de Confusión
    st.header("🔢 Matriz de Confusión del Modelo")
    if model_metrics is not None and 'confusion_matrix' in model_metrics:
        import plotly.figure_factory as ff
        
        # Preparar datos para la matriz de confusión
        conf_matrix = model_metrics['confusion_matrix']
        labels = ['Neutral/Dissatisfied', 'Satisfied']
        
        # Crear figura de matriz de confusión
        fig_conf = ff.create_annotated_heatmap(
            conf_matrix, 
            x=labels, 
            y=labels, 
            colorscale='Blues',
            showscale=True
        )
        fig_conf.update_layout(title='Matriz de Confusión del Modelo Entrenado')
        st.plotly_chart(fig_conf)
        
        st.write("Interpretación:")
        st.write(f"- **Verdaderos Negativos**: {conf_matrix[0][0]} pasajeros correctamente clasificados como neutral/dissatisfied")
        st.write(f"- **Falsos Positivos**: {conf_matrix[0][1]} pasajeros neutral/dissatisfied clasificados erróneamente como satisfied")
        st.write(f"- **Falsos Negativos**: {conf_matrix[1][0]} pasajeros satisfied clasificados erróneamente como neutral/dissatisfied")
        st.write(f"- **Verdaderos Positivos**: {conf_matrix[1][1]} pasajeros correctamente clasificados como satisfied")
    else:
        st.warning("No se pudo cargar la matriz de confusión del modelo.")
    
    st.markdown("---")

    # Gráfico 6: Reporte de Clasificación Detallado
    st.header("📋 Reporte de Clasificación por Clase")
    if model_metrics is not None and 'classification_report' in model_metrics:
        report = model_metrics['classification_report']
        
        # Crear DataFrame con el reporte
        report_data = []
        for class_label in ['0', '1']:
            if class_label in report:
                class_name = 'Neutral/Dissatisfied' if class_label == '0' else 'Satisfied'
                report_data.append({
                    'Clase': class_name,
                    'Precisión': f"{report[class_label]['precision']:.4f}",
                    'Recall': f"{report[class_label]['recall']:.4f}",
                    'F1-Score': f"{report[class_label]['f1-score']:.4f}",
                    'Soporte': f"{int(report[class_label]['support'])}"
                })
        
        report_df = pd.DataFrame(report_data)
        st.dataframe(report_df, use_container_width=True)
        
        st.info("💡 **Interpretación**: El modelo tiene un excelente rendimiento en ambas clases, con métricas superiores al 94% en todas las categorías. La clase 'Neutral/Dissatisfied' tiene un rendimiento ligeramente peor que la clase 'Satisfied'.")
    else:
        st.warning("No se pudo cargar el reporte de clasificación del modelo.")
        
    st.markdown("---")

    # Gráfico 7: Mapa de Calor de Correlaciones
    st.header("🔗 Mapa de Calor de Correlaciones")
    st.write("""
    Este mapa muestra la correlación de Pearson entre las variables numéricas.
    Un valor cercano a 1 (azul oscuro) significa una fuerte correlación positiva.
    Un valor cercano a -1 (rojo oscuro) significa una fuerte correlación negativa.
    Nos interesa especialmente la última fila/columna, que muestra la correlación con 'satisfaction'.
    """)

    # Preparamos los datos para el mapa de calor
    df_corr = df.select_dtypes(include=['number']).copy()
    df_corr['satisfaction'] = df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

    fig7, ax7 = plt.subplots(figsize=(16, 12))
    sns.heatmap(df_corr.corr(), annot=True, fmt='.2f', cmap='coolwarm', ax=ax7, annot_kws={"size": 8})
    ax7.set_title('Mapa de Calor de Correlaciones', fontsize=16)
    st.pyplot(fig7)
    st.write("Observaciones clave: 'Online boarding', 'Inflight entertainment', y 'Seat comfort' tienen algunas de las correlaciones positivas más altas con la satisfacción.")

    st.markdown("---")

    # Sección Educativa: One-Hot Encoding
    st.header("🔢 Ejemplo de One-Hot Encoding (OHE)")

    # Subconjunto de datos para demo (elige columnas categóricas como 'Gender', 'Class')
    sample_df = df[['Gender', 'Class']].head(5)  # Primeras 5 filas
    st.write("Datos originales (categóricos):")
    st.dataframe(sample_df)

    # Aplicar OHE
    ohe_df = pd.get_dummies(sample_df, columns=['Gender', 'Class'])
    st.write("Después de OHE (columnas binarias 0/1):")
    st.dataframe(ohe_df)

    st.info("OHE transforma categorías en columnas numéricas para que el modelo las procese sin asumir orden. Útil para evitar sesgos en clasificación.")
