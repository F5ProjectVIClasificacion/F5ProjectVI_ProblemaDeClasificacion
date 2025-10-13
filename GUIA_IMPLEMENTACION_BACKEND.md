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

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Entrenar el Modelo (si no existe)

```bash
python src/train_model.py
```

Esto creará:
- `models/satisfaction_model.joblib` - Modelo entrenado
- `reports/metrics.json` - Métricas del modelo

## 🎯 Opciones de Ejecución

### Opción 1: Desarrollo Local (Recomendado para desarrollo)

#### Terminal 1 - Backend (guia para levantar)
```bash
python start_backend.py
# O directamente:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend (guia para levantar)
```bash
python start_frontend.py
# O directamente:
streamlit run frontend/app.py --server.port 8501
```

### Opción 2: Docker Compose (Recomendado para producción)

```bash
# Iniciar todos los servicios
docker-compose up

# Solo backend
docker-compose up backend

# Solo frontend
docker-compose up frontend

# Entrenar modelo
docker-compose --profile training up train-model
```

### Opción 3: Docker Individual

#### Backend
```bash
docker build -f backend/Dockerfile -t airline-backend .
docker run -p 8000:8000 -v $(pwd)/models:/app/models -v $(pwd)/reports:/app/reports airline-backend
```

#### Frontend
```bash
docker build -t airline-frontend .
docker run -p 8501:8501 -v $(pwd)/frontend:/app/frontend airline-frontend
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

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear archivo `.env`:
```env
# Backend
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=models/satisfaction_model.joblib
METRICS_PATH=reports/metrics.json

# Frontend
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=8501
API_BASE_URL=http://localhost:8000
```

### Configuración de CORS

En `backend/main.py`, puedes personalizar los orígenes permitidos:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Solo frontend
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🚨 Solución de Problemas

### Error: "Modelo no cargado"
```bash
# Verificar que el modelo existe
ls -la models/
# Si no existe, entrenar el modelo
python src/train_model.py
```

### Error: "No se puede conectar con la API"
```bash
# Verificar que el backend está ejecutándose
curl http://localhost:8000/health

# Si no responde, iniciar el backend
python start_backend.py
```

### Error: "ModuleNotFoundError"
```bash
# Instalar dependencias
pip install -r requirements.txt

# Verificar que estás en el directorio correcto
pwd
# Debe mostrar: /ruta/a/F5ProjectVI_ProblemaDeClasificacion
```

### Error de Docker
```bash
# Limpiar contenedores y volúmenes
docker-compose down -v
docker system prune -f

# Reconstruir
docker-compose build --no-cache
docker-compose up
```

## 📊 Monitoreo y Logs

### Logs del Backend
```bash
# Ver logs en tiempo real
docker-compose logs -f backend

# O si ejecutas localmente, los logs aparecen en la consola
```

### Métricas de Rendimiento
- **Latencia**: Tiempo de respuesta de la API
- **Throughput**: Requests por segundo
- **Memoria**: Uso de RAM del modelo

## 🔄 Flujo de Trabajo de Desarrollo

1. **Desarrollo Local**:
   ```bash
   # Terminal 1
   python start_backend.py
   
   # Terminal 2
   python start_frontend.py
   ```

2. **Pruebas**:
   - Abrir http://localhost:8501 (Frontend)
   - Abrir http://localhost:8000/docs (API Docs)
   - Probar predicciones

3. **Despliegue**:
   ```bash
   docker-compose up -d
   ```

## 🎯 Próximos Pasos

1. **Autenticación**: Añadir JWT tokens
2. **Base de Datos**: Persistir predicciones
3. **Monitoreo**: Añadir métricas de uso
4. **Testing**: Tests unitarios y de integración
5. **CI/CD**: Pipeline de despliegue automático

## 📞 Soporte

Si encuentras problemas:

1. Verificar logs: `docker-compose logs`
2. Verificar conectividad: `curl http://localhost:8000/health`
3. Verificar modelo: `ls -la models/`
4. Reinstalar dependencias: `pip install -r requirements.txt`

