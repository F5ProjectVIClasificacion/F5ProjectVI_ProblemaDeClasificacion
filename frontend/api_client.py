"""
Cliente para conectar con la API de FastAPI
"""

import requests
import streamlit as st
from typing import Dict, Any, Optional
import json

class APIClient:
    """Cliente para interactuar con la API de FastAPI"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def health_check(self) -> bool:
        """Verificar si la API está funcionando"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Obtener información del modelo"""
        try:
            response = requests.get(f"{self.base_url}/model/info", timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error conectando con la API: {e}")
        return None
    
    def get_model_metrics(self) -> Optional[Dict[str, Any]]:
        """Obtener métricas del modelo"""
        try:
            response = requests.get(f"{self.base_url}/metrics", timeout=10)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error obteniendo métricas: {e}")
        return None
    
    def predict_satisfaction(self, passenger_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Realizar predicción de satisfacción"""
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json=passenger_data,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error en la predicción: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error conectando con la API: {e}")
        return None

# Instancia global del cliente
@st.cache_resource
def get_api_client():
    """Obtener instancia del cliente API (con cache)"""
    return APIClient()

def check_api_connection():
    """Verificar conexión con la API y mostrar estado"""
    client = get_api_client()
    
    if client.health_check():
        st.success("✅ API conectada correctamente")
        return True
    else:
        st.error("❌ No se puede conectar con la API. Asegúrate de que el backend esté ejecutándose en http://localhost:8000")
        st.info("💡 Para iniciar el backend, ejecuta: `uvicorn backend.main:app --reload`")
        return False
