"""
Modelos Pydantic para validación de datos en la API
Adaptados exactamente a los nombres que espera el modelo entrenado
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class PassengerData(BaseModel):
    """Modelo para los datos de entrada de un pasajero - nombres exactos del modelo"""

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

    # Calificaciones de servicio (0-5)
    Inflight_wifi_service: int = Field(
        ...,
        ge=0,
        le=5,
        alias="Inflight wifi service",
        description="Calificación del servicio de wifi",
    )
    Departure_Arrival_time_convenient: int = Field(
        ...,
        ge=0,
        le=5,
        alias="Departure/Arrival time convenient",
        description="Conveniencia del horario",
    )
    Ease_of_Online_booking: int = Field(
        ...,
        ge=0,
        le=5,
        alias="Ease of Online booking",
        description="Facilidad de reserva online",
    )
    Gate_location: int = Field(
        ..., ge=0, le=5, alias="Gate location", description="Ubicación de la puerta"
    )
    Food_and_drink: int = Field(
        ..., ge=0, le=5, alias="Food and drink", description="Comida y bebida"
    )
    Online_boarding: int = Field(
        ..., ge=0, le=5, alias="Online boarding", description="Embarque online"
    )
    Seat_comfort: int = Field(
        ..., ge=0, le=5, alias="Seat comfort", description="Comodidad del asiento"
    )
    Inflight_entertainment: int = Field(
        ...,
        ge=0,
        le=5,
        alias="Inflight entertainment",
        description="Entretenimiento a bordo",
    )
    On_board_service: int = Field(
        ..., ge=0, le=5, alias="On-board service", description="Servicio a bordo"
    )
    Leg_room_service: int = Field(
        ..., ge=0, le=5, alias="Leg room service", description="Espacio para piernas"
    )
    Baggage_handling: int = Field(
        ..., ge=0, le=5, alias="Baggage handling", description="Manejo de equipaje"
    )
    Checkin_service: int = Field(
        ..., ge=0, le=5, alias="Checkin service", description="Servicio de check-in"
    )
    Inflight_service: int = Field(
        ...,
        ge=0,
        le=5,
        alias="Inflight service",
        description="Servicio durante el vuelo",
    )
    Cleanliness: int = Field(..., ge=0, le=5, description="Limpieza")

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

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
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
                "Arrival Delay in Minutes": 0,
            }
        }


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

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "satisfied",
                "satisfaction_probability": 0.85,
                "neutral_probability": 0.15,
                "confidence_level": "high",
            }
        }


class ModelMetrics(BaseModel):
    """Modelo para las métricas del modelo"""

    accuracy: float = Field(..., description="Exactitud del modelo")
    precision: float = Field(..., description="Precisión del modelo")
    recall: float = Field(..., description="Recall del modelo")
    f1: float = Field(..., description="F1-score del modelo")
    roc_auc: float = Field(..., description="ROC AUC del modelo")

    class Config:
        json_schema_extra = {
            "example": {
                "accuracy": 0.9635,
                "precision": 0.9697,
                "recall": 0.9454,
                "f1": 0.9574,
                "roc_auc": 0.9943,
            }
        }
