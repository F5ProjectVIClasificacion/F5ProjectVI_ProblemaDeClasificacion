# 🚀 Guía Completa: Implementación de Backend con FastAPI

## 📋 Resumen del Proyecto

arquitectura completa:

- **🤖 Modelo ML**: Random Forest con 96.35% de precisión
- **🎨 Frontend**: Streamlit con interfaz interactiva
- **⚡ Backend**: FastAPI con endpoints REST
- **🐳 Docker**: Contenedores para desarrollo y producción

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Frontend      │ ──────────────► │   Backend       │
│   (Streamlit)    │                 │   (FastAPI)     │
│   Port: 8501     │                 │   Port: 8000    │
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │   Modelo ML     │
                                    │   (joblib)      │
                                    └─────────────────┘
```
## 🔗 Endpoints de la API

### Documentación Interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### 1. Health Check
```bash
GET /health
```
Respuesta:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "metrics_available": true
}
```

#### 2. Predicción de Satisfacción
```bash
POST /predict
```

Ejemplo de request:
```json
{
  "Gender": "Male",
  "Customer Type": "Loyal Customer",
  "Age": 35,
  "Type of Travel": "Business travel",
  "Class": "Business",
  "Flight Distance": 1000.0,
  "Inflight wifi service": 4,
  "Departure/Arrival time convenient": 3,
  "Ease of Online booking": 4,
  "Gate location": 3,
  "Food and drink": 4,
  "Online boarding": 3,
  "Seat comfort": 4,
  "Inflight entertainment": 4,
  "On-board service": 4,
  "Leg room service": 3,
  "Baggage handling": 4,
  "Checkin service": 4,
  "Inflight service": 4,
  "Cleanliness": 4,
  "Departure Delay in Minutes": 0,
  "Arrival Delay in Minutes": 0
}
```

Respuesta:
```json
{
  "prediction": "satisfied",
  "satisfaction_probability": 0.85,
  "neutral_probability": 0.15,
  "confidence_level": "high"
}
```

#### 3. Métricas del Modelo
```bash
GET /metrics
```

#### 4. Información del Modelo
```bash
GET /model/info
```

## 🧪 Pruebas de la API

### Usando curl
```bash
# Health check
curl http://localhost:8000/health

# Predicción
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "Gender": "Male",
       "Customer Type": "Loyal Customer",
       "Age": 35,
       "Type of Travel": "Business travel",
       "Class": "Business",
       "Flight Distance": 1000.0,
       "Inflight wifi service": 4,
       "Departure/Arrival time convenient": 3,
       "Ease of Online booking": 4,
       "Gate location": 3,
       "Food and drink": 4,
       "Online boarding": 3,
       "Seat comfort": 4,
       "Inflight entertainment": 4,
       "On-board service": 4,
       "Leg room service": 3,
       "Baggage handling": 4,
       "Checkin service": 4,
       "Inflight service": 4,
       "Cleanliness": 4,
       "Departure Delay in Minutes": 0,
       "Arrival Delay in Minutes": 0
     }'
```

### Usando Python
```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Predicción
data = {
    "Gender": "Male",
    "Customer Type": "Loyal Customer",
    "Age": 35,
    # ... resto de campos
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```
