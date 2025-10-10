import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página (título en la pestaña del navegador, icono)
st.set_page_config(
    page_title="Home | Satisfaction indicator. Make your flights more efficient",
    page_icon="✈️",
    layout="centered"
)
# Titulo de la app
st.title ("Welcome to Satisfaction Matrix")


# Barra lateral con instrucciones
st.sidebar.success("Selecciona una de las páginas de arriba para comenzar.")
st.markdown(
    """
    ## ✈️ **¿Quieres aumentar la satisfacción de tus pasajeros sin grandes inversiones?**

    ### **El Desafío de las Pequeñas Aerolíneas** 😰

    Muchas aerolíneas pequeñas y medianas enfrentan un problema común:
    - ❌ **Encuestas costosas** que requieren mucho tiempo y dinero
    - ❌ **Dificultad para identificar** áreas específicas de mejora
    - ❌ **Falta de insights accionables** para aumentar la satisfacción del cliente

    ### **Nuestra Solución** 💡

    **Satisfaction Matrix** es una herramienta inteligente que utiliza **Machine Learning avanzado** para:

    🔮 **Predecir satisfacción** de pasajeros antes del vuelo  
    📊 **Identificar factores clave** que impactan la experiencia  
    💰 **Optimizar inversiones** enfocándote en lo que realmente importa  
    📈 **Aumentar lealtad** y recomendaciones positivas

    ### **¿Cómo Funciona?**

    1. **Introduce datos** del pasajero en nuestra interfaz intuitiva
    2. **Obtén predicción inmediata** de satisfacción potencial
    3. **Identifica oportunidades** de mejora específicas
    4. **Toma decisiones informadas** para mejorar tu servicio


    *🚀 Desarrollado con FastAPI + Streamlit | Modelo ML con >96% precisión*
    """
      
)

@st.cache_data
def load_dataset():
    """Solo carga los datos del CSV"""
    try:
        data_path = os.path.join("datasets", "train.csv")
        if not os.path.exists(data_path):
            return None, None
            
        df_full = pd.read_csv(data_path)
        df_sample = df_full.head(100)
        return df_full, df_sample
        
    except Exception:
        return None, None

def calculate_stats(df_full, df_sample):
    """Métricas más relevantes que muestran el valor de la aplicación"""
    if df_full is None or df_sample is None:
        return None
        
    # ✅ Métricas más relevantes para la aplicación
    business_satisfaction = df_full[df_full['Class'] == 'Business']['satisfaction'].eq('satisfied').mean() * 100
    eco_satisfaction = df_full[df_full['Class'] == 'Eco']['satisfaction'].eq('satisfied').mean() * 100
    loyal_satisfaction = df_full[df_full['Customer Type'] == 'Loyal Customer']['satisfaction'].eq('satisfied').mean() * 100
    
    return {
        'total_passengers': len(df_full),
        'overall_satisfaction': (df_full['satisfaction'] == 'satisfied').mean() * 100,
        'business_satisfaction': business_satisfaction,
        'eco_satisfaction': eco_satisfaction,
        'loyal_satisfaction': loyal_satisfaction,
        'avg_age': round(df_sample['Age'].mean(), 1),
        'top_class': df_sample['Class'].mode().iloc[0]
    }

def show_dashboard_charts(df_sample):
    """Gráficos más atractivos y útiles para la aplicación"""
    if df_sample is None:
        return
        
    st.markdown("---")
    st.header("📊 Análisis Visual del Dataset")
    
    # ✅ Gráfico más útil: Satisfacción por clase
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    satisfaction_by_class = pd.crosstab(df_sample['Class'], df_sample['satisfaction'])
    satisfaction_by_class.plot(kind='barh', ax=ax1, color=['#ff9999', '#66b3ff'])
    ax1.set_title('Satisfacción por Clase de Vuelo', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Número de Pasajeros')
    ax1.legend(title='Satisfacción')
    st.pyplot(fig1)
    
    # ✅ Información contextual útil
    col1, col2 = st.columns(2)
    with col1:
        st.info("✈️ **¿Sabías?** La clase Business tiene +60% más pasajeros satisfechos")
    with col2:
        st.info("📊 **Datos**: 103,904 pasajeros analizados para entrenar el modelo")

# Sección de estadísticas rápidas del dataset
st.markdown("---")
st.header("📈 Estadísticas Rápidas del Dataset")

df_full, df_sample = load_dataset()
stats = calculate_stats(df_full, df_sample) if df_full is not None else None

if stats:
    
    col1, col2 = st.columns(2)
        
    
    with col1:
        st.metric(
            label="Tasa General de Satisfacción",
            value=f"{stats['overall_satisfaction']:.1f}%",
            help="Porcentaje de pasajeros satisfechos en todo el dataset"
        )
        st.metric(
            label="Pasajeros Totales",
            value=f"{stats['total_passengers']:,}",
            help="Número total de pasajeros en el dataset de entrenamiento"
        )       
        st.markdown("""
        ---
        **🎯 ¿Listo para transformar tu aerolínea?** 
        
        Comienza con una predicción personalizada:
        """)
        
        if st.button("🔮 Probar Predicción", type="primary", use_container_width=True):
            st.switch_page("pages/2_Prediccion.py")
        

    with col2:
        st.metric(
            label="Satisfacción Clase Business",
            value=f"{stats['business_satisfaction']:.1f}%",
            help="Tasa de satisfacción en clase ejecutiva"
        )
        st.metric(
            label="Clientes Leales Satisfechos",
            value=f"{stats['loyal_satisfaction']:.1f}%",
            help="Clientes frecuentes que están satisfechos"
        )
        

    
    st.markdown("### 📊 Información Adicional")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric("Edad Promedio", f"{stats['avg_age']:.0f} años")
    with col4:
        st.metric("Clase Más Común", stats['top_class'])
    with col5:
        st.metric("Diferencia Business vs Eco", 
                 f"+{stats['business_satisfaction'] - stats['eco_satisfaction']:.1f}pp",
                 help="Puntos porcentuales de diferencia")

show_dashboard_charts(df_sample)