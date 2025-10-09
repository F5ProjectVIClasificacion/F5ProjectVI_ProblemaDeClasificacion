# F5ProjectVI_ProblemaDeClasificacion
[gestión del proyecto](https://anthonycpcode.atlassian.net/jira/software/projects/AIR/code?atlOrigin=eyJpIjoiYjlhOTA5ZGNkZmUyNDVmZjk1MDFhMDNkNDJmNTM3NTYiLCJwIjoiaiJ9)

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

## 🚀 Inicio Rápido con Docker (Recomendado)

### **Opción 1: Usar Docker Compose (Más Fácil)**
```bash
# Construir e iniciar todos los servicios
cd /ruta/al/proyecto
docker-compose up

# Acceder a la aplicación:
# Frontend (Interfaz web): http://localhost:8501
# Backend (API): http://localhost:8000
```

### **Opción 2: Docker Individual**
```bash
# Construir imágenes
docker build -f backend/Dockerfile -t airline-backend .
docker build -f frontend/Dockerfile -t airline-frontend .

# Ejecutar servicios
docker run -p 8000:8000 airline-backend
docker run -p 8501:8501 airline-frontend
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

## 💻 Desarrollo Local

### **Configuración del Entorno**
```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### **Entrenar el Modelo**
```bash
python src/train_model.py
```

### **Ejecutar Servicios Individualmente**
```bash
# Backend API
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Frontend Web (nueva terminal)
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
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

## 🔧 Variables de Entorno

### **Frontend (.env)**
```env
# URL del backend para conexión Docker
API_BASE_URL=http://backend:8000
```

### **Backend (opcional)**
```env
# Configuración de la API
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=models/satisfaction_model.joblib
```

## 📁 Archivos Generados

### **Modelos**
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

## 🏆 Estado del Proyecto: **COMPLETO Y FUNCIONAL** 🎉

**Aplicación 100% operativa con todas las funcionalidades implementadas y documentadas.**

## Columnas del conjunto de datos

El dataset de entrenamiento ubicado en `datasets/train.csv` contiene 103 904 filas con los siguientes campos:

- `Gender`, `Customer Type`, `Type of Travel`, `Class`: descriptores categóricos de cada pasajero.
- `Age`, `Flight Distance`, calificaciones de servicio (wifi, reserva, ubicación de la puerta, comida, embarque, comodidad del asiento, entretenimiento, servicio a bordo, espacio para las piernas, equipaje, check-in, servicio en vuelo, limpieza) y mediciones de retrasos: entradas numéricas en una escala de 0 a 5 o en minutos.
- `satisfaction`: etiqueta objetivo que indica `satisfied` o `neutral or dissatisfied`.

El script elimina automáticamente las columnas no predictivas `Unnamed: 0` e `id`, imputa los retrasos faltantes con la mediana y aplica codificación one-hot a los atributos categóricos.

## Configuración del entorno

Instala las dependencias listadas en `requirements.txt` (se recomienda un entorno virtual):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Entrenar el modelo

Ejecuta el pipeline de entrenamiento desde la raíz del repositorio:

```powershell
.venv\Scripts\python.exe src/train_model.py
```

Los argumentos opcionales permiten personalizar las rutas de los datos, el modelo y las métricas. Usa `--help` para ver todas las opciones.

## Ejecutar con Docker

Si prefieres aislar el entorno y evitar instalaciones locales, puedes usar la imagen Docker incluida:

```powershell
docker build -t airline-satisfaction .
docker run --rm -v ${PWD}\models:/app/models -v ${PWD}\reports:/app/reports airline-satisfaction
```

El montaje de volúmenes es opcional pero recomendable para conservar el pipeline con el modelo en `models/` y las métricas en `reports/` en el host. Crea las carpetas si aún no existen:

```powershell
New-Item -ItemType Directory -Force models
New-Item -ItemType Directory -Force reports
```

Puedes sobreescribir el comando por defecto agregando argumentos al final de `docker run`, por ejemplo `docker run --rm airline-satisfaction python src/train_model.py`.

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

## Resultados

- `models/satisfaction_model.joblib`: pipeline de scikit-learn serializado para inferencia.
- `reports/metrics.json`: archivo JSON con los resultados de evaluación (exactitud, precisión, recall, F1, ROC AUC, informe de clasificación, matriz de confusión).

## Próximos pasos

- Validar el modelo en un conjunto separado o en el split de prueba de Kaggle.
- Crear scripts de inferencia y monitoreo para puntuar nuevas encuestas de pasajeros en producción.
