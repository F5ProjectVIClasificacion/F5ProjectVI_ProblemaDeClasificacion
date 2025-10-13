"""Train a supervised classifier to predict airline passenger satisfaction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
TARGET_COLUMN = "satisfaction"
DROP_COLUMNS = ["Unnamed: 0", "id"]# "Unnamed: 0" and "id" are common artifacts: the former often appears when a CSV file has its index saved as a column, and the latter is typically just a unique identifier that carries no predictive value. Dropping them helps ensure models learn from meaningful features rather than redundant or non-informative columns
#CATEGORICAL_MAPPINGS is dict[str, dict[str, int]] transforms the target column into a binary representation suitable for scikit-learn estimators that expect numeric targets.
CATEGORICAL_MAPPINGS = {
    TARGET_COLUMN: {"satisfied": 1, "neutral or dissatisfied": 0},
}
# Mapeo inverso para interpretar las predicciones numéricas del modelo
INV_CATEGORICAL_MAPPINGS = {v: k for k, v in CATEGORICAL_MAPPINGS[TARGET_COLUMN].items()}
PROJECT_ROOT = Path.cwd().resolve()
if not (PROJECT_ROOT / "datasets").exists():#if this notebook is not run from the project root, move up one level
    PROJECT_ROOT = PROJECT_ROOT.parent
DATA_PATH = PROJECT_ROOT / "datasets/train.csv"
MODEL_PATH = PROJECT_ROOT / "models/satisfaction_model.joblib"
METRICS_PATH = PROJECT_ROOT / "reports/metrics.json"
TEST_SIZE = 0.2

# ==============================================================================
# FUNCIONES PARA EL FRONTEND
# ==============================================================================

def load_model(model_path: Path = MODEL_PATH) -> Pipeline:
    """
    Carga el pipeline de modelo entrenado desde el disco.
    Esta es la función que usará el frontend.
    """
    if not model_path.exists():
        raise FileNotFoundError(f"El archivo del modelo no se encontró en {model_path}. Por favor, entrena el modelo primero ejecutando: python backend/train_model.py")
    
    pipeline = joblib.load(model_path)
    return pipeline

def make_prediction(pipeline: Pipeline, input_df: pd.DataFrame) -> list[str]:
    """
    Realiza una predicción usando el pipeline cargado.
    Devuelve la etiqueta de texto ('satisfied' o 'neutral or dissatisfied').
    """
    # El pipeline se encarga de todo el preprocesamiento y la predicción (0 o 1)
    prediction_numeric = pipeline.predict(input_df)
    
    # Se traduce la predicción numérica (0 o 1) a su etiqueta de texto correspondiente.
    prediction_text = [INV_CATEGORICAL_MAPPINGS[pred] for pred in prediction_numeric]
    
    return prediction_text

# ==============================================================================
# LÓGICA DE ENTRENAMIENTO 
# ==============================================================================

def load_data(csv_path: Path) -> pd.DataFrame:
    """Load dataset and perform initial cleaning."""
    df = pd.read_csv(csv_path)

    # Drop columns that do not add predictive value if present.
    for column in DROP_COLUMNS:
        if column in df.columns:
            df = df.drop(columns=column)

    # Map target labels to numeric values. Calling .map(mapping_dict) walks through that Series value-by-value and looks up each entry in the dictionary you provide. When it finds a match, it replaces the original string with the associated numeric value; if it can’t find a key, it returns NaN.
    df[TARGET_COLUMN] = df[TARGET_COLUMN].map(CATEGORICAL_MAPPINGS[TARGET_COLUMN])

    if df[TARGET_COLUMN].isna().any():#checks if prior mapping generated any NaN value, in that case throws an exception with a message and since this exception is not handled execution stops
        missing_targets = df[df[TARGET_COLUMN].isna()].shape[0]
        raise ValueError(f"Target column '{TARGET_COLUMN}' contains {missing_targets} unmapped values.")

    return df


def build_pipeline(categorical_features: list[str], numeric_features: list[str]) -> Pipeline:
    """Return a preprocessing + model pipeline."""
    '''
    Pipeline is a convenient wrapper that chains multiple preprocessing steps and a final estimator into a single object.
    You give it an ordered list of (name, column transformer) tuples —typically imputers, scalers, encoders, etc.— and it learns
    or applies them in sequence every time you call fit, transform, or predict.
    '''
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_features),
            ("categorical", categorical_transformer, categorical_features),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=300,#trains 300 trees. More trees generally yield more stable accuracy at the cost of extra training time
        random_state=RANDOM_STATE,
        class_weight="balanced",#target distribution is not balanced (57% “neutral or dissatisfied” vs 43% “satisfied), so if model is trained without compensation, the forest can get great accuracy by leaning toward the majority class and still appear “good”. scikit-learn can automatically adjust weights inversely proportional to class frequencies in the input data using class_weight="balanced"
        n_jobs=-1,#tells scikit-learn to use all available CPU cores, dramatically speeding up training and prediction.
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", model),
        ]
    )

    return pipeline


def evaluate_model(pipeline: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict[str, object]:
    """Compute evaluation metrics for the fitted pipeline."""
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]#with a classifier that supports probability estimates (like this RandomForestClassifier), the result is a NumPy array shaped (n_samples, n_classes). Each row corresponds to one sample, and each column corresponds to the probability of belonging to a particular class. Column order follows the classifier’s internal class ordering (which is accessible via pipeline.classes_). In our case, the target was mapped to {0: "neutral or dissatisfied", 1: "satisfied"}, so column 0 contains the probability of being neutral/dissatisfied and column 1 contains the probability of being satisfied.

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }

    return metrics


def main() -> None:

    df = load_data(DATA_PATH)

    y = df[TARGET_COLUMN]
    X = df.drop(columns=[TARGET_COLUMN])

    categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()
    numeric_features = [col for col in X.columns if col not in categorical_features]
    
    pipeline = build_pipeline(categorical_features, numeric_features) #Pipeline. ensures every fit or prediction shares the exact imputation, scaling, and encoding configuration alongside the random forest classifier.

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,#tells train_test_split to preserve the class proportions from the full dataset in both the training and test partitions. Because y contains the target labels, the function uses those labels to enforce the same balance of satisfied vs. neutral/dissatisfied passengers across the split, which prevents evaluation metrics from being skewed by class imbalance
        random_state=RANDOM_STATE,
    )

    pipeline.fit(X_train, y_train) #impute missing values, scale numeric features, one-hot encode categoricals, and finally fit the RandomForestClassifier, all in the proper order.
                                   #after this call the pipeline object is updated in place. It remains the same instance in memory, but now it’s “trained,” holding all the learned weights and metadata so later calls to predict or joblib.dump use the fit configuration

    metrics = evaluate_model(pipeline, X_test, y_test)

    # Ensure result directories exist.
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, MODEL_PATH)#persists the fitted pipeline object to disk at MODEL_PATH, allowing the exact preprocessing and model configuration to be reloaded later for inference or analysis without retraining.

    # Round key scalar metrics for readability before saving.
    serialisable_metrics = {
        key: (round(value, 4) if isinstance(value, float) else value)
        for key, value in metrics.items()
    }

    with METRICS_PATH.open("w", encoding="utf-8") as f:#Opening METRICS_PATH with .open("w", encoding="utf-8") creates a context-managed text file handle ready for writing, ensuring the directory path resolves cleanly and that the file is closed automatically even if errors occur json.dump(serialisable_metrics, f, indent=2) serializes the metrics dictionary into human-readable JSON, using two-space indentation so the saved report is easy to inspect or diff later.
        json.dump(serialisable_metrics, f, indent=2)#serializes the serialisable_metrics dictionary into human-readable JSON, using two-space indentation so the saved report is easy to inspect or diff later

    print("Model training complete.")
    print(json.dumps(serialisable_metrics, indent=2))#serializes the serialisable_metrics dictionary into human-readable JSON and returns it as a string, which is then printed to the console 


if __name__ == "__main__":
    main()
