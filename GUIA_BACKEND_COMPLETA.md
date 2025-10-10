# 🚀 GUÍA COMPLETA DEL BACKEND - LÍNEA POR LÍNEA

## 📋 ÍNDICE
1. [Estructura General](#estructura-general)
2. [Archivo main.py - Aplicación Principal](#archivo-mainpy---aplicación-principal)
3. [Archivo models.py - Modelos de Datos](#archivo-modelspy---modelos-de-datos)
4. [Flujo de Funcionamiento](#flujo-de-funcionamiento)
5. [Endpoints de la API](#endpoints-de-la-api)
6. [Validaciones y Seguridad](#validaciones-y-seguridad)
7. [Manejo de Errores](#manejo-de-errores)

---

## 🏗️ ESTRUCTURA GENERAL

El backend está compuesto por dos archivos principales:
- **`main.py`**: Aplicación FastAPI principal con todos los endpoints
- **`models.py`**: Modelos Pydantic para validación de datos

---

## 📄 ARCHIVO MAIN.PY - APLICACIÓN PRINCIPAL

### **Líneas 1-3: Documentación del Módulo**
```python
"""
FastAPI Backend para el Sistema de Predicción de Satisfacción de Pasajeros
"""
```
**Propósito**: Documentación del módulo principal del backend.

### **Líneas 5-12: Importaciones Básicas**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import json
from pathlib import Path
import sys
import os
```
**Propósito**: 
- `FastAPI`: Framework web para crear la API
- `HTTPException`: Para manejar errores HTTP
- `CORSMiddleware`: Para permitir requests desde el frontend
- `pandas`: Para manipular DataFrames
- `json`: Para manejar archivos JSON
- `pathlib.Path`: Para manejar rutas de archivos
- `sys`, `os`: Para configuración del sistema

### **Líneas 14-19: Configuración de Paths e Importaciones**
```python
# Añadir el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.train_model import load_model, make_prediction
from backend.models import PassengerData, PredictionResponse, ModelMetrics
```
**Propósito**:
- **Línea 15**: Obtiene la ruta del directorio raíz del proyecto
- **Línea 16**: Añade el directorio raíz al path de Python para poder importar módulos
- **Línea 18**: Importa funciones del modelo de ML
- **Línea 19**: Importa modelos Pydantic para validación

### **Líneas 21-26: Configuración de la Aplicación FastAPI**
```python
# Configuración de la aplicación
app = FastAPI(
    title="Airline Passenger Satisfaction API",
    description="API para predecir la satisfacción de pasajeros de aerolíneas",
    version="1.0.0",
)
```
**Propósito**: Crea la instancia de FastAPI con metadatos para la documentación automática.

### **Líneas 28-35: Configuración de CORS**
```python
# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
**Propósito**: 
- Permite que el frontend haga requests a la API desde cualquier dominio
- **⚠️ En producción**: Cambiar `["*"]` por dominios específicos por seguridad

### **Líneas 37-39: Variables Globales**
```python
# Variables globales para el modelo
model = None
model_metrics = None
```
**Propósito**: Variables globales para almacenar el modelo ML y sus métricas.

### **Líneas 42-62: Evento de Inicio**
```python
@app.on_event("startup")
async def load_model_on_startup():
    """Cargar el modelo al iniciar la aplicación"""
    global model, model_metrics

    try:
        # Cargar el modelo entrenado
        model_path = project_root / "models" / "satisfaction_model.joblib"
        model = load_model(model_path)

        # Cargar las métricas del modelo
        metrics_path = project_root / "reports" / "metrics.json"
        if metrics_path.exists():
            with open(metrics_path, "r") as f:
                model_metrics = json.load(f)

        print("✅ Modelo cargado exitosamente")

    except Exception as e:
        print(f"❌ Error cargando el modelo: {e}")
        raise e
```
**Propósito**:
- **Línea 42**: Decorador que ejecuta la función al iniciar la aplicación
- **Línea 45**: Declara que usará las variables globales
- **Líneas 48-50**: Carga el modelo ML desde el archivo joblib
- **Líneas 52-56**: Carga las métricas del modelo desde JSON
- **Línea 58**: Confirma que el modelo se cargó correctamente
- **Líneas 60-62**: Maneja errores durante la carga

### **Líneas 65-72: Endpoint de Bienvenida**
```python
@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": "API de Predicción de Satisfacción de Pasajeros",
        "version": "1.0.0",
        "status": "active",
    }
```
**Propósito**: Endpoint básico que devuelve información de la API.

### **Líneas 75-82: Health Check**
```python
@app.get("/health")
async def health_check():
    """Endpoint de salud del sistema"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "metrics_available": model_metrics is not None,
    }
```
**Propósito**: 
- Verifica que la API esté funcionando
- Confirma que el modelo esté cargado
- Confirma que las métricas estén disponibles

### **Líneas 85-132: Endpoint Principal de Predicción**
```python
@app.post("/predict", response_model=PredictionResponse)
async def predict_satisfaction(passenger_data: PassengerData):
    """
    Predecir la satisfacción de un pasajero basado en sus características
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")

    try:
        # Convertir los datos de entrada a DataFrame
        # El modelo espera los nombres originales del dataset (con espacios)
        input_data = passenger_data.dict(by_alias=True)
        input_df = pd.DataFrame([input_data])

        # El modelo fue entrenado sin las columnas 'Unnamed: 0', 'id' y 'satisfaction'
        # Estas columnas no deben estar presentes en el DataFrame de predicción
        print(f"🔍 Columnas en DataFrame: {list(input_df.columns)}")
        print(f"🔍 Shape del DataFrame: {input_df.shape}")

        # Realizar la predicción
        prediction = make_prediction(model, input_df)

        # Obtener probabilidades si es posible
        try:
            probabilities = model.predict_proba(input_df)
            satisfaction_prob = float(
                probabilities[0][1]
            )  # Probabilidad de estar satisfecho
            neutral_prob = float(
                probabilities[0][0]
            )  # Probabilidad de estar neutral/insatisfecho
        except:
            satisfaction_prob = None
            neutral_prob = None

        return PredictionResponse(
            prediction=prediction[0],
            satisfaction_probability=satisfaction_prob,
            neutral_probability=neutral_prob,
            confidence_level=(
                get_confidence_level(satisfaction_prob)
                if satisfaction_prob
                else "unknown"
            ),
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en la predicción: {str(e)}")
```
**Propósito**:
- **Línea 85**: Define endpoint POST que acepta datos de pasajero y devuelve predicción
- **Línea 90**: Verifica que el modelo esté cargado
- **Línea 96**: Convierte datos Pydantic a diccionario usando alias (nombres con espacios)
- **Línea 97**: Crea DataFrame de pandas con los datos
- **Líneas 101-102**: Debug: imprime columnas y forma del DataFrame
- **Línea 105**: Realiza la predicción usando el modelo
- **Líneas 108-118**: Obtiene probabilidades de cada clase
- **Líneas 120-129**: Crea respuesta con predicción y probabilidades
- **Líneas 131-132**: Maneja errores de predicción

### **Líneas 135-145: Endpoint de Métricas**
```python
@app.get("/metrics", response_model=ModelMetrics)
async def get_model_metrics():
    """
    Obtener las métricas de rendimiento del modelo
    """
    if model_metrics is None:
        raise HTTPException(
            status_code=404, detail="Métricas del modelo no disponibles"
        )

    return ModelMetrics(**model_metrics)
```
**Propósito**: Devuelve las métricas de rendimiento del modelo (accuracy, precision, etc.).

### **Líneas 148-162: Endpoint de Información del Modelo**
```python
@app.get("/model/info")
async def get_model_info():
    """
    Obtener información sobre el modelo cargado
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")

    return {
        "model_type": "RandomForestClassifier",
        "features_count": len(model.named_steps["preprocessor"].transformers_[0][2])
        + len(model.named_steps["preprocessor"].transformers_[1][2]),
        "classes": ["neutral or dissatisfied", "satisfied"],
        "model_loaded": True,
    }
```
**Propósito**: Devuelve información técnica sobre el modelo (tipo, número de características, clases).

### **Líneas 165-172: Función de Nivel de Confianza**
```python
def get_confidence_level(probability: float) -> str:
    """Determinar el nivel de confianza basado en la probabilidad"""
    if probability >= 0.8:
        return "high"
    elif probability >= 0.6:
        return "medium"
    else:
        return "low"
```
**Propósito**: Convierte probabilidad numérica a nivel de confianza textual.

### **Líneas 175-178: Punto de Entrada**
```python
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```
**Propósito**: Ejecuta el servidor cuando se ejecuta el archivo directamente.

---

## 📄 ARCHIVO MODELS.PY - MODELOS DE DATOS

### **Líneas 1-4: Documentación del Módulo**
```python
"""
Modelos Pydantic para validación de datos en la API
Adaptados exactamente a los nombres que espera el modelo entrenado
"""
```
**Propósito**: Documentación del módulo de modelos de datos.

### **Líneas 6-7: Importaciones**
```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
```
**Propósito**: 
- `BaseModel`: Clase base para modelos Pydantic
- `Field`: Para definir campos con validaciones
- `Optional`: Para campos opcionales
- `Literal`: Para valores literales específicos

### **Líneas 10-11: Clase Principal de Datos de Pasajero**
```python
class PassengerData(BaseModel):
    """Modelo para los datos de entrada de un pasajero - nombres exactos del modelo"""
```
**Propósito**: Define la estructura de datos que acepta la API para predicciones.

### **Líneas 13-27: Información Demográfica**
```python
# Información demográfica
Gender: Literal["Male", "Female"] = Field(..., description="Género del pasajero")
Customer_Type: Literal["Loyal Customer", "disloyal Customer"] = Field(
    ..., alias="Customer Type", description="Tipo de cliente"
)
Age: int = Field(..., ge=0, le=120, description="Edad del pasajero")
Type_of_Travel: Literal["Business travel", "Personal Travel"] = Field(
    ..., alias="Type of Travel", description="Tipo de viaje"
)
Class: Literal["Business", "Eco", "Eco Plus"] = Field(
    ..., description="Clase del vuelo"
)
Flight_Distance: float = Field(
    ..., ge=0, alias="Flight Distance", description="Distancia del vuelo en millas"
)
```
**Propósito**:
- **Gender**: Género del pasajero (Male/Female)
- **Customer_Type**: Tipo de cliente con alias "Customer Type"
- **Age**: Edad con validación (0-120 años)
- **Type_of_Travel**: Tipo de viaje con alias "Type of Travel"
- **Class**: Clase del vuelo
- **Flight_Distance**: Distancia con alias "Flight Distance" y validación ≥0

### **Líneas 29-89: Calificaciones de Servicio**
```python
# Calificaciones de servicio (0-5)
Inflight_wifi_service: int = Field(
    ...,
    ge=0,
    le=5,
    alias="Inflight wifi service",
    description="Calificación del servicio de wifi",
)
# ... (más campos similares)
```
**Propósito**: Define todas las calificaciones de servicio (0-5) con alias para nombres con espacios.

### **Líneas 91-103: Retrasos**
```python
# Retrasos
Departure_Delay_in_Minutes: int = Field(
    ...,
    ge=0,
    alias="Departure Delay in Minutes",
    description="Retraso en salida (minutos)",
)
Arrival_Delay_in_Minutes: int = Field(
    ...,
    ge=0,
    alias="Arrival Delay in Minutes",
    description="Retraso en llegada (minutos)",
)
```
**Propósito**: Define campos de retrasos con validación ≥0.

### **Líneas 105-132: Configuración de la Clase**
```python
class Config:
    populate_by_name = True
    json_schema_extra = {
        "example": {
            # ... ejemplo completo de datos
        }
    }
```
**Propósito**:
- **populate_by_name**: Permite usar tanto el nombre del campo como el alias
- **json_schema_extra**: Proporciona ejemplo para la documentación automática

### **Líneas 135-160: Modelo de Respuesta**
```python
class PredictionResponse(BaseModel):
    """Modelo para la respuesta de predicción"""

    prediction: Literal["satisfied", "neutral or dissatisfied"] = Field(
        ..., description="Predicción de satisfacción"
    )
    satisfaction_probability: Optional[float] = Field(
        None, ge=0, le=1, description="Probabilidad de estar satisfecho"
    )
    neutral_probability: Optional[float] = Field(
        None, ge=0, le=1, description="Probabilidad de estar neutral/insatisfecho"
    )
    confidence_level: Literal["high", "medium", "low", "unknown"] = Field(
        ..., description="Nivel de confianza de la predicción"
    )
```
**Propósito**: Define la estructura de la respuesta de predicción con probabilidades y nivel de confianza.

### **Líneas 162-181: Modelo de Métricas**
```python
class ModelMetrics(BaseModel):
    """Modelo para las métricas del modelo"""

    accuracy: float = Field(..., description="Exactitud del modelo")
    precision: float = Field(..., description="Precisión del modelo")
    recall: float = Field(..., description="Recall del modelo")
    f1: float = Field(..., description="F1-score del modelo")
    roc_auc: float = Field(..., description="ROC AUC del modelo")
```
**Propósito**: Define la estructura para las métricas de rendimiento del modelo.

---

## 🔄 FLUJO DE FUNCIONAMIENTO

### **1. Inicio de la Aplicación**
1. Se cargan las importaciones y configuraciones
2. Se crea la instancia de FastAPI
3. Se configura CORS
4. Se ejecuta `load_model_on_startup()`:
   - Carga el modelo ML desde `models/satisfaction_model.joblib`
   - Carga las métricas desde `reports/metrics.json`

### **2. Request de Predicción**
1. Cliente envía POST a `/predict` con datos del pasajero
2. Pydantic valida los datos usando `PassengerData`
3. Se convierte a DataFrame con nombres de columnas correctos
4. Se realiza la predicción usando `make_prediction()`
5. Se obtienen las probabilidades
6. Se calcula el nivel de confianza
7. Se devuelve la respuesta estructurada

### **3. Validaciones**
- **Campos requeridos**: Todos los campos son obligatorios
- **Rangos de valores**: Edad (0-120), calificaciones (0-5), retrasos (≥0)
- **Tipos de datos**: Validación estricta de tipos
- **Valores literales**: Solo valores específicos permitidos

---

## 🌐 ENDPOINTS DE LA API

| **Endpoint** | **Método** | **Propósito** |
|--------------|------------|---------------|
| `/` | GET | Información básica de la API |
| `/health` | GET | Estado de salud del sistema |
| `/predict` | POST | Realizar predicción de satisfacción |
| `/metrics` | GET | Obtener métricas del modelo |
| `/model/info` | GET | Información técnica del modelo |

---

## 🛡️ VALIDACIONES Y SEGURIDAD

### **Validaciones de Datos**
- **Campos obligatorios**: Todos los campos son requeridos
- **Rangos numéricos**: Validación de rangos para edad, calificaciones, retrasos
- **Tipos de datos**: Validación estricta de tipos (int, float, string)
- **Valores literales**: Solo valores específicos permitidos

### **Manejo de Errores**
- **Modelo no cargado**: Error 500
- **Datos inválidos**: Error 400 con detalles específicos
- **Métricas no disponibles**: Error 404
- **Errores de predicción**: Error 400 con mensaje descriptivo

### **CORS**
- Configurado para permitir requests desde cualquier origen
- **⚠️ En producción**: Cambiar a dominios específicos

---

## 🎯 CARACTERÍSTICAS DESTACADAS

### **1. Mapeo Perfecto de Columnas**
- Los nombres de campos en Pydantic coinciden exactamente con lo que espera el modelo ML
- Uso de `alias` para manejar nombres con espacios
- `by_alias=True` en la serialización para usar los nombres correctos

### **2. Validación Robusta**
- Validación automática de todos los campos
- Mensajes de error descriptivos
- Validación de rangos y tipos

### **3. Respuestas Estructuradas**
- Respuestas consistentes con probabilidades
- Niveles de confianza calculados automáticamente
- Documentación automática con ejemplos

### **4. Manejo de Errores**
- Errores HTTP apropiados
- Mensajes descriptivos
- Manejo de casos límite

---

## 🚀 CONCLUSIÓN

El backend está diseñado para ser:
- **Robusto**: Validaciones exhaustivas y manejo de errores
- **Escalable**: Estructura modular y bien organizada
- **Documentado**: Código bien comentado y documentación automática
- **Mantenible**: Separación clara de responsabilidades
- **Seguro**: Validaciones estrictas y manejo apropiado de errores

**¡El sistema está listo para producción!** 🎉
