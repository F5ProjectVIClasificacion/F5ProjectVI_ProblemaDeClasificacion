# F5ProjectVI_ProblemaDeClasificacion
[gestión del proyecto](https://anthonycpcode.atlassian.net/jira/software/projects/AIR/summary)

[Airline Passenger Satisfaction dataset in Kaggle](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction/data)

## Resumen

Este proyecto entrena un modelo de clasificación supervisada que predice la satisfacción de los pasajeros de una aerolínea (satisfecho vs. neutral o insatisfecho) utilizando un dataset público de Kaggle. El flujo de trabajo limpia los datos, codifica las variables categóricas y ajusta un pipeline de random forest balanceado que supera el 96 % de exactitud en la partición de entrenamiento.

## ✨ Características Principales

🚀 **Aplicación Web Completa**: Interfaz intuitiva desarrollada con Streamlit para predicciones en tiempo real
🔮 **Predicciones Instantáneas**: Modelo ML integrado con >96% precisión para predecir satisfacción de pasajeros
📊 **Análisis Visual**: Dashboard completo con métricas y gráficos del dataset
🐳 **Despliegue Docker**: Configuración completa frontend-backend con Docker Compose
⚡ **API RESTful**: Backend FastAPI para integración y escalabilidad

## 🎯 Funcionalidades de la Aplicación

### 📊 **Página Principal**
- Métricas rápidas del dataset (103,904 pasajeros analizados)
- Comparación de satisfacción por clase (Business vs Economy)
- Estadísticas de clientes leales y edad promedio
- Navegación directa a funcionalidades específicas

### 📈 **Página de Análisis de Datos**
- Análisis exploratorio completo (EDA)
- Visualizaciones detalladas con gráficos profesionales
- Métricas empresariales relevantes
- Información contextual para toma de decisiones

### 🔮 **Página de Predicción**
- Formulario completo con todos los parámetros del pasajero
- Predicciones en tiempo real con el modelo entrenado
- Probabilidad de satisfacción y nivel de confianza
- Resultados formateados profesionalmente

## 🚀 Ejecutar el Proyecto (con Docker)

Si el modelo no está entrenado (no ves un fichero "satisfaction_model.joblib" en la carpeta `models/`), ejecuta:

```bash
cd /ruta/al/proyecto
docker compose --profile training up train-model
```

con el modelo entrenado (ya hay un fichero "satisfaction_model.joblib" en la carpeta `models/`), ejecuta:

```bash
# Construir e iniciar todos los servicios
docker-compose up

# Acceder a la aplicación desde tu navegador:
# http://localhost:8501
```

## 📋 Arquitectura del Proyecto

```
F5ProjectVI_ProblemaDeClasificacion/
├── 📁 frontend/                 # Aplicación web Streamlit
│   ├── app.py                  # Página principal
│   ├── pages/                  # Páginas adicionales
│   │   ├── 1_AnalisisDatos.py  # Análisis exploratorio
│   │   └── 2_Prediccion.py     # Formulario de predicción
│   ├── api_client.py           # Cliente API para backend
│   ├── Dockerfile              # Configuración contenedor
│   └── .env                    # Variables de entorno
├── 📁 backend/                  # API FastAPI
├── 📁 datasets/                 # Datos de entrenamiento
├── 📁 models/                   # Modelos entrenados
├── 📁 reports/                  # Métricas y reportes
└── 📁 src/                      # Scripts de entrenamiento
```

## 📊 Métricas del Modelo

La configuración predeterminada reporta las siguientes métricas sobre el conjunto de validación:

| Métrica     | Puntaje |
|-------------|---------|
| Exactitud   | 0.9635 |
| Precisión   | 0.9697 |
| Recall      | 0.9454 |
| F1-score    | 0.9574 |
| ROC AUC     | 0.9943 |

## 📁 Archivos Generados

### **Modelo**
- `models/satisfaction_model.joblib`: Pipeline completo serializado

### **Reportes**
- `reports/metrics.json`: Métricas detalladas del modelo
- `reports/classification_report.txt`: Reporte de clasificación completo
- `reports/confusion_matrix.png`: Matriz de confusión visual

## 🎨 Tecnologías Utilizadas

### **Backend**
- **FastAPI**: Framework web rápido y moderno
- **Scikit-learn**: Librería de machine learning
- **Pandas**: Manipulación y análisis de datos
- **Joblib**: Serialización de modelos

### **Frontend**
- **Streamlit**: Framework para aplicaciones web de datos
- **Plotly/Matplotlib**: Visualizaciones interactivas
- **Requests**: Cliente HTTP para API

### **DevOps**
- **Docker**: Containerización de aplicaciones
- **Docker Compose**: Orquestación de servicios

## 🔄 Flujo de Trabajo Completo

1. **📥 Carga de Datos**: Dataset de 103,904 pasajeros desde Kaggle
2. **🧹 Preprocesamiento**: Limpieza, codificación y preparación de datos
3. **🤖 Entrenamiento**: Modelo Random Forest optimizado
4. **📊 Evaluación**: Métricas superiores al 96% de precisión
5. **🌐 Despliegue**: Aplicación web completa con Docker
6. **🔮 Predicciones**: Interface para predicciones en tiempo real

## 🎯 Próximos Pasos Sugeridos

- ✅ **Completado**: Interfaz web completa con Streamlit
- ✅ **Completado**: Integración Docker frontend-backend
- ✅ **Completado**: Sistema de navegación multipágina
- 🔄 **Próximo**: Validación en conjunto de prueba separado
- 🔄 **Próximo**: Sistema de monitoreo para producción
- 🔄 **Próximo**: Tests automatizados para CI/CD

## 📚 Documentación Adicional

- [Guía Backend Completa](GUIA_BACKEND_COMPLETA.md)
- [Guía de Implementación Backend](GUIA_IMPLEMENTACION_BACKEND.md)
- [Guía Frontend](GUIA_FRONTEND.md)

---

## Columnas del conjunto de datos

El dataset de entrenamiento ubicado en `datasets/train.csv` contiene 103 904 filas con los siguientes campos:

- `Gender`, `Customer Type`, `Type of Travel`, `Class`: descriptores categóricos de cada pasajero.
- `Age`, `Flight Distance`, calificaciones de servicio (wifi, reserva, ubicación de la puerta, comida, embarque, comodidad del asiento, entretenimiento, servicio a bordo, espacio para las piernas, equipaje, check-in, servicio en vuelo, limpieza) y mediciones de retrasos: entradas numéricas en una escala de 0 a 5 o en minutos.
- `satisfaction`: etiqueta objetivo que indica `satisfied` o `neutral or dissatisfied`.

Para entrenar el modelo se eliminan las columnas no predictivas `Unnamed: 0` e `id`, se imputan los retrasos faltantes con la mediana y se aplica codificación one-hot a los atributos categóricos.

## Resumen de evaluación

La configuración predeterminada divide los datos 80/20 (estratificada) y reporta las siguientes métricas sobre el conjunto de validación:

| Métrica     | Puntaje |
|-------------|---------|
| Exactitud   | 0.9635 |
| Precisión   | 0.9697 |
| Recall      | 0.9454 |
| F1-score    | 0.9574 |
| ROC AUC     | 0.9943 |

Las métricas de clasificación detalladas y la matriz de confusión se almacenan en `reports/metrics.json`.

- `models/satisfaction_model.joblib`: pipeline de scikit-learn serializado para inferencia.
- `reports/metrics.json`: archivo JSON con los resultados de evaluación (exactitud, precisión, recall, F1, ROC AUC, informe de clasificación, matriz de confusión).

