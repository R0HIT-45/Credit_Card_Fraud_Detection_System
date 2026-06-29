import os
import sys
import time
import pandas as pd

from src.data_loader import load_data, get_features_and_target
from src.eda import generate_eda_report
from src.preprocessing import scale_features, split_data, apply_smote

from src.model import (
    train_logistic_regression,
    train_random_forest,
    train_xgboost,
    train_lightgbm,
    train_catboost,
    cross_validate_model,
    compare_models,
    save_comparison_report,
    get_best_model,
    save_model
)

from src.evaluate import evaluate_model

DATA_PATH = os.path.join("data", "creditcard.csv")
PLOTS_DIR = os.path.join("outputs", "plots")
MODELS_DIR = os.path.join("outputs", "models")
REPORTS_DIR = os.path.join("outputs", "reports")


def main():

    start_time = time.time()

    print("=" * 70)
    print(" CREDIT CARD FRAUD DETECTION PIPELINE ")
    print("=" * 70)

    if not os.path.exists(DATA_PATH):

        print("\nDataset not found.")
        print("Download creditcard.csv from Kaggle.")
        sys.exit(1)

    for directory in [PLOTS_DIR, MODELS_DIR, REPORTS_DIR]:
        os.makedirs(directory, exist_ok=True)

    print("\nLoading dataset...")
    df = load_data(DATA_PATH)

    print("Running EDA...")
    generate_eda_report(df, PLOTS_DIR)

    print("Preprocessing...")
    df = scale_features(df)

    X, y = get_features_and_target(df)

    X_train, X_test, y_train, y_test = split_data(X, y)

    print("Applying SMOTE...")
    X_train_res, y_train_res = apply_smote(
        X_train,
        y_train
    )

    models = {

        "Logistic Regression":
            train_logistic_regression(
                X_train_res,
                y_train_res
            ),

        "Random Forest":
            train_random_forest(
                X_train_res,
                y_train_res
            ),

        "XGBoost":
            train_xgboost(
                X_train_res,
                y_train_res
            ),

        "LightGBM":
            train_lightgbm(
                X_train_res,
                y_train_res
            ),

        "CatBoost":
            train_catboost(
                X_train_res,
                y_train_res
            )
    }

    results = []

    print("\nEvaluating Models...\n")

    for name, model in models.items():

        print(f"Evaluating {name}")

        roc_auc = cross_validate_model(
            model,
            X_train_res,
            y_train_res
        )

        evaluate_model(
            model,
            X_test,
            y_test,
            name,
            PLOTS_DIR
        )

        save_model(
            model,
            os.path.join(
                MODELS_DIR,
                f"{name.lower().replace(' ','_')}.pkl"
            )
        )

        results.append({

            "Model": name,

            "ROC_AUC": roc_auc

        })

    comparison_df = compare_models(results)

    save_comparison_report(comparison_df)

    best = get_best_model(results)

    best_model = models[best["Model"]]

    save_model(
        best_model,
        os.path.join(
            MODELS_DIR,
            "best_model.pkl"
        )
    )

    print("\n")
    print(comparison_df)

    print("\nBest Model")

    print(best["Model"])

    print("ROC-AUC :", round(best["ROC_AUC"],4))

    elapsed = time.time() - start_time

    print("\nPipeline Finished Successfully")

    print(f"Execution Time : {elapsed:.2f} seconds")


if __name__ == "__main__":

    main()