import os
import logging
import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

# -------------------------------------------------
# Logging
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

LOGGER = logging.getLogger(__name__)


# -------------------------------------------------
# Logistic Regression
# -------------------------------------------------

def train_logistic_regression(X_train, y_train):

    LOGGER.info("Training Logistic Regression...")

    model = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train, y_train)

    LOGGER.info("Logistic Regression completed.")

    return model


# -------------------------------------------------
# Random Forest
# -------------------------------------------------

def train_random_forest(X_train, y_train):

    LOGGER.info("Training Random Forest...")

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    LOGGER.info("Random Forest completed.")

    return model


# -------------------------------------------------
# XGBoost
# -------------------------------------------------

def train_xgboost(X_train, y_train):

    LOGGER.info("Training XGBoost...")

    scale_pos_weight = (
        float((y_train == 0).sum())
        /
        float((y_train == 1).sum())
    )

    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=5,
        gamma=1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        eval_metric="logloss",
        verbosity=0
    )

    model.fit(X_train, y_train)

    LOGGER.info("XGBoost completed.")

    return model


# -------------------------------------------------
# LightGBM
# -------------------------------------------------

def train_lightgbm(X_train, y_train):

    LOGGER.info("Training LightGBM...")

    model = LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        num_leaves=31,
        random_state=42
    )

    model.fit(X_train, y_train)

    LOGGER.info("LightGBM completed.")

    return model


# -------------------------------------------------
# CatBoost
# -------------------------------------------------

def train_catboost(X_train, y_train):

    LOGGER.info("Training CatBoost...")

    model = CatBoostClassifier(
        iterations=100,
        learning_rate=0.05,
        depth=6,
        verbose=False,
        random_state=42
    )

    model.fit(X_train, y_train)

    LOGGER.info("CatBoost completed.")

    return model


# -------------------------------------------------
# Cross Validation
# -------------------------------------------------

def cross_validate_model(model, X, y):

    LOGGER.info("Performing 5-Fold Cross Validation...")

    scores = cross_val_score(
        model,
        X,
        y,
        cv=3,
        scoring="roc_auc",
        n_jobs=-1
    )

    LOGGER.info(f"Average ROC-AUC: {scores.mean():.4f}")

    return scores.mean()


# -------------------------------------------------
# Compare Models
# -------------------------------------------------

def compare_models(results):

    df = pd.DataFrame(results)

    df = df.sort_values(
        by="ROC_AUC",
        ascending=False
    )

    return df


# -------------------------------------------------
# Save Comparison Report
# -------------------------------------------------

def save_comparison_report(df):

    os.makedirs(
        "outputs/reports",
        exist_ok=True
    )

    path = "outputs/reports/model_comparison.csv"

    df.to_csv(
        path,
        index=False
    )

    LOGGER.info(f"Comparison report saved at {path}")


# -------------------------------------------------
# Best Model
# -------------------------------------------------

def get_best_model(results):

    best = max(
        results,
        key=lambda x: x["ROC_AUC"]
    )

    LOGGER.info(
        f"Best Model: {best['Model']} | ROC-AUC={best['ROC_AUC']:.4f}"
    )

    return best


# -------------------------------------------------
# Save Model
# -------------------------------------------------

def save_model(model, filepath):

    os.makedirs(
        os.path.dirname(filepath),
        exist_ok=True
    )

    joblib.dump(model, filepath)

    LOGGER.info(f"Model saved at {filepath}")


# -------------------------------------------------
# Load Model
# -------------------------------------------------

def load_model(filepath):

    LOGGER.info(f"Loading model from {filepath}")

    return joblib.load(filepath)