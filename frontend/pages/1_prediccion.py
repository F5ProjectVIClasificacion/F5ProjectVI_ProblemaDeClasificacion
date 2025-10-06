import streamlit as st
import pandas as pd
import os
import sys

# Añadir el directorio raíz al path para poder importar módulos de 'src'
# Esto es crucial para que Streamlit encuentre tus funciones
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Ahora puedes importar tus funciones
# Es necesario que tengas un modelo guardado (ej: 'models/model.pkl')
# y que tu función load_model sepa cómo cargarlo.
from src.train_model import load_model, make_prediction

st.set_page_config(page_title="Página de Predicción", page_icon="🔮")

st.markdown("# Página de Predicción")
st.sidebar.header("Página de Predicción")
st.write(
    """Introduce los datos del pasajero para predecir su nivel de satisfacción."""
)

# --- Carga de Modelo y Datos ---
# Asegúrate de que la ruta al modelo sea correcta y que exista
# Por ejemplo, si tu modelo se guarda en la carpeta 'models' en la raíz del proyecto
MODEL_PATH = os.path.join(project_root, 'models', 'logistic_regression_model.pkl')
DATA_PATH = os.path.join(project_root, 'datasets', 'train.csv')

try:
    model = load_model(MODEL_PATH)
    data = pd.read_csv(DATA_PATH)
    st.success("Modelo cargado correctamente.")
except FileNotFoundError:
    st.error(f"Error: No se encontró el modelo o el archivo de datos.")
    st.info("Asegúrate de que el modelo entrenado ('logistic_regression_model.pkl') exista en la carpeta 'models' y 'train.csv' en 'datasets'.")
    st.stop()


# --- Entradas de Usuario en la Barra Lateral ---
st.sidebar.header("Introduce los datos del pasajero:")

def user_input_features():
    # --- EJEMPLO ---
    # TODO Debes reemplazar esto con las columnas reales de tu dataset 'train.csv'
    # Aquí hay un ejemplo basado en un dataset de aerolíneas típico:
    gender = st.sidebar.selectbox('Género', data['Gender'].unique())
    customer_type = st.sidebar.selectbox('Tipo de Cliente', data['Customer Type'].unique())
    age = st.sidebar.slider('Edad', int(data['Age'].min()), int(data['Age'].max()), int(data['Age'].mean()))
    type_of_travel = st.sidebar.selectbox('Tipo de Viaje', data['Type of Travel'].unique())
    flight_class = st.sidebar.selectbox('Clase', data['Class'].unique())
    flight_distance = st.sidebar.slider('Distancia de Vuelo', int(data['Flight Distance'].min()), int(data['Flight Distance'].max()), int(data['Flight Distance'].mean()))
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Calificaciones del Servicio (0-5)")
    
    inflight_wifi_service = st.sidebar.slider('Servicio Wifi a bordo', 0, 5, 3)
    departure_arrival_time_convenient = st.sidebar.slider('Conveniencia Horario Salida/Llegada', 0, 5, 3)
    ease_of_online_booking = st.sidebar.slider('Facilidad de Reserva Online', 0, 5, 3)
    gate_location = st.sidebar.slider('Ubicación de la Puerta de Embarque', 0, 5, 3)
    food_and_drink = st.sidebar.slider('Comida y Bebida', 0, 5, 3)
    online_boarding = st.sidebar.slider('Embarque Online', 0, 5, 3)
    seat_comfort = st.sidebar.slider('Comodidad del Asiento', 0, 5, 3)
    inflight_entertainment = st.sidebar.slider('Entretenimiento a bordo', 0, 5, 3)
    on_board_service = st.sidebar.slider('Servicio a bordo', 0, 5, 3)
    leg_room_service = st.sidebar.slider('Servicio de Espacio para Piernas', 0, 5, 3)
    baggage_handling = st.sidebar.slider('Manejo de Equipaje', 0, 5, 3)
    checkin_service = st.sidebar.slider('Servicio de Check-in', 0, 5, 3)
    inflight_service = st.sidebar.slider('Servicio durante el Vuelo', 0, 5, 3)
    cleanliness = st.sidebar.slider('Limpieza', 0, 5, 3)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Retrasos (en minutos)")

    departure_delay_in_minutes = st.sidebar.number_input('Retraso en la Salida (minutos)', min_value=0, value=0)
    arrival_delay_in_minutes = st.sidebar.number_input('Retraso en la Llegada (minutos)', min_value=0, value=0)


    # Crea un diccionario con los datos
    # Las claves deben coincidir EXACTAMENTE con los nombres de las columnas que espera tu modelo
    input_data = {
        'Gender': gender,
        'Customer Type': customer_type,
        'Age': age,
        'Type of Travel': type_of_travel,
        'Class': flight_class,
        'Flight Distance': flight_distance,
        'Inflight wifi service': inflight_wifi_service,
        'Departure/Arrival time convenient': departure_arrival_time_convenient,
        'Ease of Online booking': ease_of_online_booking,
        'Gate location': gate_location,
        'Food and drink': food_and_drink,
        'Online boarding': online_boarding,
        'Seat comfort': seat_comfort,
        'Inflight entertainment': inflight_entertainment,
        'On-board service': on_board_service,
        'Leg room service': leg_room_service,
        'Baggage handling': baggage_handling,
        'Checkin service': checkin_service,
        'Inflight service': inflight_service,
        'Cleanliness': cleanliness,
        'Departure Delay in Minutes': departure_delay_in_minutes,
        'Arrival Delay in Minutes': arrival_delay_in_minutes
    }
    # Convierte el diccionario a un DataFrame de una sola fila
    features = pd.DataFrame(input_data, index=[0])
    return features

# Aquí se llama a la función definida arriba
input_df = user_input_features()

# Muestra los datos introducidos por el usuario
st.subheader('Datos del Pasajero Introducidos')
st.write(input_df)

# --- Predicción ---
if st.sidebar.button('Predecir Satisfacción'):
    # La función make_prediction debe estar preparada para recibir un DataFrame
    with st.spinner('Calculando predicción...'):
        prediction = make_prediction(model, input_df)
    
    st.subheader('Resultado de la Predicción')
    
    col1, col2 = st.columns([1, 4])

    with col1:
        if prediction[0] == 'satisfied':
            st.image('https://em-content.zobj.net/source/apple/391/smiling-face-with-smiling-eyes.png', width=100)
        else:
            st.image('https://em-content.zobj.net/source/apple/391/neutral-face.png', width=100)
    
    with col2:
        if prediction[0] == 'satisfied':
            st.success('El pasajero estará **satisfecho**.')
        else:
            st.warning('El pasajero estará **insatisfecho o neutral**.')
            
# --- Visualización de Datos (Opcional) ---
st.subheader('Visualización de Datos del Dataset de Entrenamiento')
st.write("Distribución de la variable objetivo:")
# Un gráfico de barras es más útil para una variable categórica
target_counts = data['satisfaction'].value_counts() # Reemplaza 'satisfaction' con tu columna objetivo
st.bar_chart(target_counts)
