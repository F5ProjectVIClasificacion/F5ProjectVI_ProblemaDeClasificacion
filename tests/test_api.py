#!/usr/bin/env python3
"""
Script de pruebas para la API de FastAPI
"""

import json
import time
from typing import Dict, Any

import pytest
import requests

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Probar el endpoint de health check"""
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Health check exitoso: {data}")
        assert data.get("status") == "healthy"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"❌ Error conectando con la API: {e}")


def test_model_info():
    """Probar el endpoint de información del modelo"""
    print("🔍 Probando información del modelo...")
    try:
        response = requests.get(f"{API_BASE_URL}/model/info", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Información del modelo: {json.dumps(data, indent=2)}")
        assert data.get("model_loaded") is True
        assert "features_count" in data
    except requests.exceptions.RequestException as e:
        pytest.fail(f"❌ Error: {e}")


def test_model_metrics():
    """Probar el endpoint de métricas del modelo"""
    print("🔍 Probando métricas del modelo...")
    try:
        response = requests.get(f"{API_BASE_URL}/metrics", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Métricas del modelo:")
        for metric, value in data.items():
            if isinstance(value, float):
                print(f"   {metric}: {value:.4f}")
            else:
                print(f"   {metric}: {value}")
        assert "accuracy" in data
    except requests.exceptions.RequestException as e:
        pytest.fail(f"❌ Error: {e}")


def test_prediction():
    """Probar el endpoint de predicción"""
    print("🔍 Probando predicción...")

    # Datos de prueba - nombres exactos del modelo
    test_data = {
        "Gender": "Male",
        "Customer Type": "Loyal Customer",
        "Age": 35,
        "Type of Travel": "Business travel",
        "Class": "Business",
        "Flight_Distance": 1000.0,
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

    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=test_data, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Predicción exitosa:")
        print(f"   Predicción: {data['prediction']}")
        if data.get("satisfaction_probability") is not None:
            print(
                f"   Probabilidad de satisfacción: {data['satisfaction_probability']:.2%}"
            )
        print(f"   Nivel de confianza: {data['confidence_level']}")
        assert data["prediction"] in {
            "satisfied",
            "neutral or dissatisfied",
        }
    except requests.exceptions.RequestException as e:
        pytest.fail(f"❌ Error: {e}")


def test_multiple_predictions():
    """Probar múltiples predicciones con diferentes datos"""
    print("🔍 Probando múltiples predicciones...")

    test_cases = [
        {
            "name": "Pasajero satisfecho",
            "data": {
                "Gender": "Female",
                "Customer Type": "Loyal Customer",
                "Age": 28,
                "Type of Travel": "Personal Travel",
                "Class": "Eco",
                "Flight_Distance": 500.0,
                "Inflight wifi service": 5,
                "Departure/Arrival time convenient": 5,
                "Ease of Online booking": 5,
                "Gate location": 5,
                "Food and drink": 5,
                "Online boarding": 5,
                "Seat comfort": 5,
                "Inflight entertainment": 5,
                "On-board service": 5,
                "Leg room service": 5,
                "Baggage handling": 5,
                "Checkin service": 5,
                "Inflight service": 5,
                "Cleanliness": 5,
                "Departure Delay in Minutes": 0,
                "Arrival Delay in Minutes": 0,
            },
        },
        {
            "name": "Pasajero insatisfecho",
            "data": {
                "Gender": "Male",
                "Customer Type": "disloyal Customer",
                "Age": 45,
                "Type of Travel": "Business travel",
                "Class": "Eco",
                "Flight_Distance": 2000.0,
                "Inflight wifi service": 1,
                "Departure/Arrival time convenient": 1,
                "Ease of Online booking": 1,
                "Gate location": 1,
                "Food and drink": 1,
                "Online boarding": 1,
                "Seat comfort": 1,
                "Inflight entertainment": 1,
                "On-board service": 1,
                "Leg room service": 1,
                "Baggage handling": 1,
                "Checkin service": 1,
                "Inflight service": 1,
                "Cleanliness": 1,
                "Departure Delay in Minutes": 120,
                "Arrival Delay in Minutes": 120,
            },
        },
    ]

    results = []
    for test_case in test_cases:
        print(f"   Probando: {test_case['name']}")
        try:
            response = requests.post(
                f"{API_BASE_URL}/predict", json=test_case["data"], timeout=10
            )
            response.raise_for_status()
            data = response.json()
            print(f"   ✅ {test_case['name']}: {data['prediction']}")
            results.append(data["prediction"] in {
                "satisfied",
                "neutral or dissatisfied",
            })
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {test_case['name']}: {e}")
            results.append(False)

    assert all(results), "Una o más predicciones fallaron"


def main():
    """Ejecutar todas las pruebas"""
    print("🧪 Iniciando pruebas de la API...")
    print("=" * 50)

    tests = [
        ("Health Check", test_health_check),
        ("Model Info", test_model_info),
        ("Model Metrics", test_model_metrics),
        ("Single Prediction", test_prediction),
        ("Multiple Predictions", test_multiple_predictions),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Pausa entre pruebas

    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\nResultado: {passed}/{total} pruebas pasaron")

    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La API está funcionando correctamente.")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los logs arriba.")
        print("\n💡 Consejos:")
        print(
            "   - Asegúrate de que el backend esté ejecutándose: python start_backend.py"
        )
        print("   - Verifica que el modelo esté entrenado: python backend/train_model.py")
        print("   - Revisa que no haya errores en los logs del backend")


if __name__ == "__main__":
    main()
