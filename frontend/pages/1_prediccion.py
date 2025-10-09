import streamlit as st
import pandas as pd
import os
import sys

# Añadir el directorio raíz al path para poder importar módulos
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Importar el cliente de API
from frontend.api_client import get_api_client, check_api_connection

st.set_page_config(page_title="Página de Predicción", page_icon="🔮")

st.markdown("# Página de Predicción")
st.sidebar.header("Página de Predicción")
st.write("""Introduce los datos del pasajero para predecir su nivel de satisfacción.""")

# --- Verificación de Conexión con la API ---
if not check_api_connection():
    st.stop()

# Obtener cliente de API
api_client = get_api_client()

# Cargar datos para mostrar opciones en los selectores
DATA_PATH = os.path.join(project_root, "datasets", "train.csv")
try:
    data = pd.read_csv(DATA_PATH)
    st.success("✅ Datos cargados correctamente.")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo de datos.")
    st.info("Asegúrate de que 'train.csv' exista en la carpeta 'datasets'.")
    st.stop()


# --- Entradas de Usuario en la Barra Lateral ---
st.sidebar.header("Introduce los datos del pasajero:")


def user_input_features():
    # --- EJEMPLO ---
    # TODO Debes reemplazar esto con las columnas reales de tu dataset 'train.csv'
    # Aquí hay un ejemplo basado en un dataset de aerolíneas típico:
    gender = st.sidebar.selectbox("Género", data["Gender"].unique())
    customer_type = st.sidebar.selectbox(
        "Tipo de Cliente", data["Customer Type"].unique()
    )
    age = st.sidebar.slider(
        "Edad", int(data["Age"].min()), int(data["Age"].max()), int(data["Age"].mean())
    )
    type_of_travel = st.sidebar.selectbox(
        "Tipo de Viaje", data["Type of Travel"].unique()
    )
    flight_class = st.sidebar.selectbox("Clase", data["Class"].unique())
    flight_distance = st.sidebar.slider(
        "Distancia de Vuelo",
        int(data["Flight Distance"].min()),
        int(data["Flight Distance"].max()),
        int(data["Flight Distance"].mean()),
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Calificaciones del Servicio (0-5)")

    inflight_wifi_service = st.sidebar.slider("Servicio Wifi a bordo", 0, 5, 3)
    departure_arrival_time_convenient = st.sidebar.slider(
        "Conveniencia Horario Salida/Llegada", 0, 5, 3
    )
    ease_of_online_booking = st.sidebar.slider("Facilidad de Reserva Online", 0, 5, 3)
    gate_location = st.sidebar.slider("Ubicación de la Puerta de Embarque", 0, 5, 3)
    food_and_drink = st.sidebar.slider("Comida y Bebida", 0, 5, 3)
    online_boarding = st.sidebar.slider("Embarque Online", 0, 5, 3)
    seat_comfort = st.sidebar.slider("Comodidad del Asiento", 0, 5, 3)
    inflight_entertainment = st.sidebar.slider("Entretenimiento a bordo", 0, 5, 3)
    on_board_service = st.sidebar.slider("Servicio a bordo", 0, 5, 3)
    leg_room_service = st.sidebar.slider("Servicio de Espacio para Piernas", 0, 5, 3)
    baggage_handling = st.sidebar.slider("Manejo de Equipaje", 0, 5, 3)
    checkin_service = st.sidebar.slider("Servicio de Check-in", 0, 5, 3)
    inflight_service = st.sidebar.slider("Servicio durante el Vuelo", 0, 5, 3)
    cleanliness = st.sidebar.slider("Limpieza", 0, 5, 3)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Retrasos (en minutos)")

    departure_delay_in_minutes = st.sidebar.number_input(
        "Retraso en la Salida (minutos)", min_value=0, value=0
    )
    arrival_delay_in_minutes = st.sidebar.number_input(
        "Retraso en la Llegada (minutos)", min_value=0, value=0
    )

    # Crea un diccionario con los datos
    # Las claves deben coincidir EXACTAMENTE con los nombres de las columnas que espera tu modelo
    input_data = {
        "Gender": gender,
        "Customer Type": customer_type,
        "Age": age,
        "Type of Travel": type_of_travel,
        "Class": flight_class,
        "Flight Distance": flight_distance,
        "Inflight wifi service": inflight_wifi_service,
        "Departure/Arrival time convenient": departure_arrival_time_convenient,
        "Ease of Online booking": ease_of_online_booking,
        "Gate location": gate_location,
        "Food and drink": food_and_drink,
        "Online boarding": online_boarding,
        "Seat comfort": seat_comfort,
        "Inflight entertainment": inflight_entertainment,
        "On-board service": on_board_service,
        "Leg room service": leg_room_service,
        "Baggage handling": baggage_handling,
        "Checkin service": checkin_service,
        "Inflight service": inflight_service,
        "Cleanliness": cleanliness,
        "Departure Delay in Minutes": departure_delay_in_minutes,
        "Arrival Delay in Minutes": arrival_delay_in_minutes,
    }
    # Convierte el diccionario a un DataFrame de una sola fila
    features = pd.DataFrame(input_data, index=[0])
    return features


# Aquí se llama a la función definida arriba
input_df = user_input_features()

# Muestra los datos introducidos por el usuario
st.subheader("Datos del Pasajero Introducidos")
st.write(input_df)

# --- Predicción ---
if st.sidebar.button("Predecir Satisfacción"):
    with st.spinner("Calculando predicción..."):
        # Convertir DataFrame a diccionario para la API
        input_dict = input_df.iloc[0].to_dict()

        # Realizar predicción a través de la API
        prediction_result = api_client.predict_satisfaction(input_dict)

    if prediction_result:
        st.subheader("Resultado de la Predicción")

        col1, col2 = st.columns([1, 4])

        with col1:
            if prediction_result["prediction"] == "satisfied":
                st.image(
                    "https://em-content.zobj.net/source/apple/391/smiling-face-with-smiling-eyes.png",
                    width=100,
                )
            else:
                st.image(
                    "https://em-content.zobj.net/source/apple/391/neutral-face.png",
                    width=100,
                )

        with col2:
            if prediction_result["prediction"] == "satisfied":
                st.success("El pasajero estará **satisfecho**.")
            else:
                st.warning("El pasajero estará **insatisfecho o neutral**.")

        # Mostrar información adicional si está disponible
        if prediction_result.get("satisfaction_probability"):
            st.info(
                f"**Probabilidad de satisfacción:** {prediction_result['satisfaction_probability']:.2%}"
            )
            st.info(
                f"**Nivel de confianza:** {prediction_result['confidence_level'].upper()}"
            )

        # Mostrar métricas del modelo si están disponibles
        with st.expander("📊 Información del Modelo"):
            model_info = api_client.get_model_info()
            if model_info:
                st.json(model_info)

            model_metrics = api_client.get_model_metrics()
            if model_metrics:
                st.subheader("Métricas del Modelo")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Exactitud", f"{model_metrics['accuracy']:.3f}")
                with col2:
                    st.metric("Precisión", f"{model_metrics['precision']:.3f}")
                with col3:
                    st.metric("Recall", f"{model_metrics['recall']:.3f}")
                with col4:
                    st.metric("F1-Score", f"{model_metrics['f1']:.3f}")

# --- Visualización de Datos (Opcional) ---
st.subheader("Visualización de Datos del Dataset de Entrenamiento")
st.write("Distribución de la variable objetivo:")
# Un gráfico de barras es más útil para una variable categórica
target_counts = data[
    "satisfaction"
].value_counts()  # Reemplaza 'satisfaction' con tu columna objetivo
st.bar_chart(target_counts)
