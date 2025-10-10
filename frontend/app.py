from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.train_model import load_model, make_prediction

st.set_page_config(
    page_title="Home",
    page_icon="✈️",
)

# Titulo de la app
st.title ("Welcome to AirGemini")


DATA_PATH = Path(__file__).resolve().parents[1] / "datasets" / "train.csv"


@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


@st.cache_resource(show_spinner=False)
def load_trained_model():
    return load_model()


def _collect_user_input(sample: pd.DataFrame) -> pd.DataFrame:
    feature_names = list(model.feature_names_in_)
    user_values: dict[str, object] = {}

    st.sidebar.header("Passenger survey inputs")

    for column in feature_names:
        label = column.replace("_", " ")
        if pd.api.types.is_numeric_dtype(sample[column]):
            col_series = sample[column].dropna()
            min_value = float(col_series.min()) if not col_series.empty else 0.0
            max_value = float(col_series.max()) if not col_series.empty else 5.0
            default = float(col_series.median()) if not col_series.empty else 0.0
            value = st.sidebar.number_input(
                label,
                min_value=min_value,
                max_value=max_value,
                value=default,
                key=f"num_{column}",
            )
            if pd.api.types.is_integer_dtype(sample[column]):
                user_values[column] = int(value)
            else:
                user_values[column] = float(value)
        else:
            options = sorted(sample[column].dropna().unique().tolist()) or [""]
            default_index = 0
            value = st.sidebar.selectbox(
                label,
                options,
                index=default_index,
                key=f"cat_{column}",
            )
            user_values[column] = value

    return pd.DataFrame([user_values], columns=feature_names)

# Load the trained model
dataset = load_dataset()
model = load_trained_model()

# Make predictions based on user inputs
input_df = _collect_user_input(dataset)

if st.sidebar.button("Predict satisfaction"):
    try:
        prediction = make_prediction(model, input_df)[0]
        st.subheader("Prediction")
        st.write(prediction)

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            st.caption("Class probabilities")
            st.json(
                {
                    "neutral or dissatisfied": float(probabilities[0]),
                    "satisfied": float(probabilities[1]),
                }
            )
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
