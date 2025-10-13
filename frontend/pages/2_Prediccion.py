import streamlit as st
from api_client import get_api_client, check_api_connection
import os

# --- Configuración de la Página ---
st.set_page_config(page_title="Página de Predicción", page_icon="🔮", layout="wide")
st.title("🔮 Predicción de Satisfacción del Pasajero")

# --- Verificación de Conexión con la API ---
if not check_api_connection():
    st.stop()

# --- Formulario de Entrada de Datos en la Página Principal ---
st.header("Introduce los datos del pasajero:")

# DISEÑO ORIGINAL CON COLUMNAS (comentar if False y tabular hacia atras)
# if False:
    # Usamos columnas para un diseño más limpio
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Datos Personales")
    gender = st.selectbox('Género', ('Female', 'Male'))
    customer_type = st.selectbox('Tipo de Cliente', ('Loyal Customer', 'disloyal Customer'), index=0)
    age = st.slider('Edad', 1, 100, 40)

with col2:
    st.subheader("Detalles del Vuelo")
    type_of_travel = st.selectbox('Tipo de Viaje', ('Business travel', 'Personal Travel'), index=0)
    flight_class = st.selectbox('Clase de Vuelo', ('Business', 'Eco', 'Eco Plus'), key='flight_class', index=0)
    flight_distance = st.slider('Distancia de Vuelo (km)', 0, 5000, 1200)

with col3:
    st.subheader("Retrasos (minutos)")
    departure_delay_in_minutes = st.number_input('Retraso en Salida', min_value=0, value=0)
    arrival_delay_in_minutes = st.number_input('Retraso en Llegada', min_value=0, value=0)

st.markdown("---")
st.header("Calificaciones del Servicio (0-5)")

# Columnas para las calificaciones
c1, c2, c3, c4 = st.columns(4)
with c1:
    inflight_wifi_service = st.slider('Wifi a bordo', 0, 5, 4)
    departure_arrival_time_convenient = st.slider('Horario Salida/Llegada', 0, 5, 4)
    ease_of_online_booking = st.slider('Reserva Online', 0, 5, 4)
    gate_location = st.slider('Ubicación Puerta', 0, 5, 4)
with c2:
    food_and_drink = st.slider('Comida y Bebida', 0, 5, 4)
    online_boarding = st.slider('Embarque Online', 0, 5, 4)
    seat_comfort = st.slider('Comodidad Asiento', 0, 5, 5)
    inflight_entertainment = st.slider('Entretenimiento', 0, 5, 4)
with c3:
    on_board_service = st.slider('Servicio a bordo', 0, 5, 5)
    leg_room_service = st.slider('Espacio Piernas', 0, 5, 4)
    baggage_handling = st.slider('Manejo Equipaje', 0, 5, 4)
    checkin_service = st.slider('Servicio Check-in', 0, 5, 4)
with c4:
    inflight_service = st.slider('Servicio en Vuelo', 0, 5, 5)
    cleanliness = st.slider('Limpieza', 0, 5, 5)


# ALTERNATIVA CON st.expander (borrar el if False y tabular hacia atras)
# ...existing code...
        departure_arrival_time_convenient = st.slider('Horario Salida/Llegada', 0, 5, 3)
        ease_of_online_booking = st.slider('Reserva Online', 0, 5, 3)
        gate_location = st.slider('Ubicación Puerta', 0, 5, 3)
        food_and_drink = st.slider('Comida y Bebida', 0, 5, 3)
        online_boarding = st.slider('Embarque Online', 0, 5, 3)
        seat_comfort = st.slider('Comodidad Asiento', 0, 5, 3)
        inflight_entertainment = st.slider('Entretenimiento', 0, 5, 3)
        on_board_service = st.slider('Servicio a bordo', 0, 5, 3)
        leg_room_service = st.slider('Espacio Piernas', 0, 5, 3)
        baggage_handling = st.slider('Manejo Equipaje', 0, 5, 3)
        checkin_service = st.slider('Servicio Check-in', 0, 5, 3)
        inflight_service = st.slider('Servicio en Vuelo', 0, 5, 3)
        cleanliness = st.slider('Limpieza', 0, 5, 3)


# ALTERNATIVA CON st.tabs (borrar el if False y tabular hacia atras)
# ...existing code...
if False:
    tab1, tab2, tab3, tab4 = st.tabs(["Datos Personales", "Detalles del Vuelo", "Retrasos", "Calificaciones"])

    with tab1:
        gender = st.selectbox('Género', ('Female', 'Male'))
        customer_type = st.selectbox('Tipo de Cliente', ('Loyal Customer', 'disloyal Customer'))
        age = st.slider('Edad', 1, 100, 40)

    with tab2:
        type_of_travel = st.selectbox('Tipo de Viaje', ('Business travel', 'Personal Travel'))
        flight_class = st.selectbox('Clase de Vuelo', ('Business', 'Eco', 'Eco Plus'), key='flight_class')
        flight_distance = st.slider('Distancia de Vuelo (km)', 0, 5000, 1200)

    with tab3:
        departure_delay_in_minutes = st.number_input('Retraso en Salida', min_value=0, value=0)
        arrival_delay_in_minutes = st.number_input('Retraso en Llegada', min_value=0, value=0)

    with tab4:
        inflight_wifi_service = st.slider('Wifi a bordo', 0, 5, 3)
        departure_arrival_time_convenient = st.slider('Horario Salida/Llegada', 0, 5, 3)
        ease_of_online_booking = st.slider('Reserva Online', 0, 5, 3)
        gate_location = st.slider('Ubicación Puerta', 0, 5, 3)
        food_and_drink = st.slider('Comida y Bebida', 0, 5, 3)
        online_boarding = st.slider('Embarque Online', 0, 5, 3)
        seat_comfort = st.slider('Comodidad Asiento', 0, 5, 3)
        inflight_entertainment = st.slider('Entretenimiento', 0, 5, 3)
        on_board_service = st.slider('Servicio a bordo', 0, 5, 3)
        leg_room_service = st.slider('Espacio Piernas', 0, 5, 3)
        baggage_handling = st.slider('Manejo Equipaje', 0, 5, 3)
        checkin_service = st.slider('Servicio Check-in', 0, 5, 3)
        inflight_service = st.slider('Servicio en Vuelo', 0, 5, 3)
        cleanliness = st.slider('Limpieza', 0, 5, 3)


# --- Creación del Diccionario de Datos ---
passenger_data = {
    'Gender': gender, 'Customer Type': customer_type, 'Age': age,
    'Type of Travel': type_of_travel, 'Class': flight_class, 'Flight Distance': flight_distance,
    'Inflight wifi service': inflight_wifi_service,
    'Departure/Arrival time convenient': departure_arrival_time_convenient,
    'Ease of Online booking': ease_of_online_booking, 'Gate location': gate_location,
    'Food and drink': food_and_drink, 'Online boarding': online_boarding,
    'Seat comfort': seat_comfort, 'Inflight entertainment': inflight_entertainment,
    'On-board service': on_board_service, 'Leg room service': leg_room_service,
    'Baggage handling': baggage_handling, 'Checkin service': checkin_service,
    'Inflight service': inflight_service, 'Cleanliness': cleanliness,
    'Departure Delay in Minutes': departure_delay_in_minutes,
    'Arrival Delay in Minutes': arrival_delay_in_minutes
}

# --- Resumen en la Barra Lateral ---
st.sidebar.header("Resumen de Datos Introducidos")
st.sidebar.json(passenger_data)

# --- Botón de Predicción y Lógica de Llamada a la API ---
if st.button('Predecir Satisfacción', type="primary", use_container_width=True):
    client = get_api_client()
    
    with st.spinner('Realizando la predicción...'):
        prediction_result = client.predict_satisfaction(passenger_data)

    st.subheader('Resultado de la Predicción')

    # CORRECCIÓN: Este bloque ahora está DENTRO del if, por lo que solo se ejecuta
    # después de que prediction_result tenga un valor.
    if prediction_result:
        prediction = prediction_result.get('prediction')
        satisfaction_probability = prediction_result.get('satisfaction_probability')
        neutral_probability = prediction_result.get('neutral_probability')
        confidence = prediction_result.get('confidence_level')

        if prediction == 'satisfied':
            st.success('El pasajero estará **satisfecho** 😊')
        else:
            st.warning('El pasajero estará **insatisfecho o neutral** 😐')

        # Usamos columnas para mostrar las métricas
        mcol1, mcol2 = st.columns(2)

        # Mostrar probabilidad de satisfacción
        if satisfaction_probability is not None:
            prob_text = f"{satisfaction_probability:.2%}"
        else:
            prob_text = "No disponible"

        mcol1.metric(label="Probabilidad de Satisfacción", value=prob_text)

        # Manejar caso cuando confidence es None
        if confidence is not None:
            conf_text = str(confidence).capitalize()
        else:
            conf_text = "No disponible"

        mcol2.metric(label="Nivel de Confianza", value=conf_text)
    else:
        st.error("No se pudo obtener una predicción. Revisa los mensajes de error.")