import streamlit as st
import pandas as pd
from src.train_model import load_model, make_prediction
import os

st.set_page_config(
    page_title="Home",
    page_icon="✈️",
)

# Titulo de la app
st.title ("Welcome to AirGemini")

# Carga de datos
data = pd.read_csv('data/train.csv')

# Display del dataset
st.subheader("Dataset")
st.dataframe(data)

# sidebar 
st.sidebar.header("User Input Features -titulo TBD-")

# Example of user input fields (customize as needed)
feature1 = st.sidebar.number_input("Feature 1", min_value=0.0, max_value=100.0, value=50.0)
feature2 = st.sidebar.selectbox("Feature 2", options=data['feature2'].unique())

# Load the trained model
model = load_model()

# Make predictions based on user inputs
if st.sidebar.button("Predict"):
    prediction = make_prediction(model, feature1, feature2)
    st.subheader("Prediction")
    st.write(prediction)

# Display insights or visualizations
st.subheader("Data Insights")
st.line_chart(data['target_variable'])  # Replace 'target_variable' with the actual target column name