"""
FastAPI Backend para el Sistema de Predicción de Satisfacción de Pasajeros
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import pandas as pd
import json
from pathlib import Path
import sys
import os

# Añadir el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.train_model import load_model, make_prediction
from backend.models import PassengerData, PredictionResponse, ModelMetrics

# Variables globales para el modelo
model = None
model_metrics = None

# FastAPI lifespan handler: carga el modelo al iniciar la aplicación
# FastAPI calls this function once when the app begins serving, passing as arg
# the FastAPI instance so any resources can be initialized before yielding control
# and cleaned up afterward.
@asynccontextmanager
async def lifespan(app: FastAPI):
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
        print(f"❌ Error cargando el modelo: debes entrenar el modelo primero. Ejecuta 'docker compose --profile training up train-model' y luego 'docker compose up --build'{e}")
        raise e
    try:
        yield#control back to the framework
    finally:
        # Limpia las referencias cuando la aplicación se detiene (liberación de memoria)
        model = None
        model_metrics = None


# Configuración de la aplicación
app = FastAPI(
    title="Airline Passenger Satisfaction API",
    description="API para predecir la satisfacción de pasajeros de aerolíneas",
    version="1.0.0",
    lifespan=lifespan,
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint de bienvenida"""
    return {
        "message": "API de Predicción de Satisfacción de Pasajeros",
        "version": "1.0.0",
        "status": "active",
    }


@app.get("/health")
async def health_check():
    """Endpoint de salud del sistema"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "metrics_available": model_metrics is not None,
    }


@app.post("/predict", response_model=PredictionResponse)#In FastAPI decorators, response_model names the schema that outgoing responses must satisfy. So, FastAPI uses that model to validate, filter, and document the JSON sent back to clients.
async def predict_satisfaction(passenger_data: PassengerData):
    """
    Predecir la satisfacción de un pasajero basado en sus características.
    passenger_data is the request body that FastAPI binds to the PassengerData Pydantic model
    in models.py. When a client sends a POST /predict with JSON fields in the request body 
    —for example {"Gender": "...", "Age": 39, ...}— FastAPI automatically parses that payload,
    validates it against PassengerData, and injects the resulting model instance into the 
    passenger_data argument (which is a PassengerData Pydantic model instance. FastAPI deserializes
    the incoming JSON body into that class, so inside the handler you receive a fully validated
    PassengerData object rather than a plain dict). If the JSON payload sent to POST /predict is missing required fields,
    includes values of the wrong type, or otherwise fails the PassengerData schema, FastAPI raises
    a 422 Unprocessable Entity response. The request never reaches your predict_satisfaction function
    —the framework intercepts the error, returns a validation report in the body, and the handler never runs.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")

    try:
        # Convertir los datos de entrada (en el body de la http request) a DataFrame manteniendo los nombres de columnas del dataset original (separacion con espacios)
        # ya que en el body del request los nombres de las columnas vienen en snake_case (por ejemplo, "customer_type")
        # serializes the validated PassengerData model into a plain dictionary, respecting any field
        # aliases so the keys match the feature names in the original dataset expected by the downstream
        # pipeline, in order to align the runtime payload with the column names used during training; without that step, the model would see mismatched headers
        input_data = passenger_data.model_dump(by_alias=True)
        input_df = pd.DataFrame([input_data])

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


def get_confidence_level(probability: float) -> str:
    """Determinar el nivel de confianza basado en la probabilidad"""
    if probability >= 0.8:
        return "high"
    elif probability >= 0.6:
        return "medium"
    else:
        return "low"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
