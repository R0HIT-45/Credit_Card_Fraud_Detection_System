import os
import logging
import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTETomek

# -------------------------------------------------
# Logging Configuration
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

LOGGER = logging.getLogger(__name__)

# -------------------------------------------------
# Directory for saved preprocessing objects
# -------------------------------------------------

MODEL_DIR = "outputs/models"
os.makedirs(MODEL_DIR, exist_ok=True)

SCALER_PATH = os.path.join(MODEL_DIR, "feature_scaler.pkl")


# -------------------------------------------------
# Dataset Validation
# -------------------------------------------------

def validate_dataset(df: pd.DataFrame):

    required_columns = ["Time", "Amount"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    if df.isnull().sum().sum() > 0:
        raise ValueError("Dataset contains missing values.")

    LOGGER.info("Dataset validation successful.")


# -------------------------------------------------
# Feature Scaling
# -------------------------------------------------

def scale_features(df):
    df = df.copy()

    amount_scaler = StandardScaler()
    time_scaler = StandardScaler()

    df["Amount"] = amount_scaler.fit_transform(df[["Amount"]])
    df["Time"] = time_scaler.fit_transform(df[["Time"]])

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(
        {
            "amount_scaler": amount_scaler,
            "time_scaler": time_scaler
        },
        os.path.join(MODEL_DIR, "scalers.pkl")
    )

    print("[OK] Saved feature scalers")

    return df


# -------------------------------------------------
# Train Test Split
# -------------------------------------------------

def split_data(
    X,
    y,
    test_size=0.2,
    random_state=42
):

    LOGGER.info("Splitting dataset...")

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )


# -------------------------------------------------
# SMOTE
# -------------------------------------------------

def apply_smote(
    X_train,
    y_train,
    random_state=42
):

    LOGGER.info("Applying SMOTE...")

    smote = SMOTE(
        random_state=random_state,
        k_neighbors=5
    )

    X_res, y_res = smote.fit_resample(
        X_train,
        y_train
    )

    LOGGER.info(
        f"SMOTE Completed | Normal={(y_res==0).sum()} Fraud={(y_res==1).sum()}"
    )

    return X_res, y_res


# -------------------------------------------------
# Random Undersampling
# -------------------------------------------------

def apply_undersampling(
    X_train,
    y_train,
    random_state=42
):

    LOGGER.info("Applying Random Under Sampling...")

    rus = RandomUnderSampler(
        random_state=random_state
    )

    X_res, y_res = rus.fit_resample(
        X_train,
        y_train
    )

    return X_res, y_res


# -------------------------------------------------
# SMOTE + Tomek
# -------------------------------------------------

def apply_smote_tomek(
    X_train,
    y_train,
    random_state=42
):

    LOGGER.info("Applying SMOTE Tomek...")

    smt = SMOTETomek(
        random_state=random_state
    )

    X_res, y_res = smt.fit_resample(
        X_train,
        y_train
    )

    return X_res, y_res


# -------------------------------------------------
# Load Saved Scaler
# -------------------------------------------------

def load_scaler():

    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(
            "Scaler not found. Train the model first."
        )

    LOGGER.info("Loading saved scaler...")

    return joblib.load(SCALER_PATH)