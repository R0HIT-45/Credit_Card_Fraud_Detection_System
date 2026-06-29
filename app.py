import os
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========================================================
# Paths
# ==========================================================

MODELS_DIR = os.path.join("outputs", "models")

RF_PATH = os.path.join(MODELS_DIR, "random_forest.pkl")
XGB_PATH = os.path.join(MODELS_DIR, "xgboost.pkl")
SCALER_PATH = os.path.join(MODELS_DIR, "scalers.pkl")

# ==========================================================
# Global Objects (Loaded Once)
# ==========================================================

rf_model = None
xgb_model = None
scalers = None


# ==========================================================
# Load Models
# ==========================================================

def load_models():
    global rf_model, xgb_model, scalers

    try:
        if os.path.exists(RF_PATH):
            rf_model = joblib.load(RF_PATH)
            print(f"[OK] Random Forest loaded")

        else:
            print("[ERROR] Random Forest model not found")

        if os.path.exists(XGB_PATH):
            xgb_model = joblib.load(XGB_PATH)
            print(f"[OK] XGBoost loaded")

        else:
            print("[ERROR] XGBoost model not found")

        if os.path.exists(SCALER_PATH):
            scalers = joblib.load(SCALER_PATH)
            print("[OK] Feature Scalers loaded")

        else:
            print("[ERROR] Scaler file not found")

    except Exception as e:
        print(f"[LOAD ERROR] {e}")


load_models()


# ==========================================================
# Utility Functions
# ==========================================================

def get_risk_level(prob):

    if prob >= 90:
        return "CRITICAL"

    elif prob >= 70:
        return "HIGH"

    elif prob >= 40:
        return "MEDIUM"

    else:
        return "LOW"


# ==========================================================
# Routes
# ==========================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "random_forest_loaded": rf_model is not None,
        "xgboost_loaded": xgb_model is not None,
        "scalers_loaded": scalers is not None
    })


@app.route("/model_status")
def model_status():

    return jsonify({
        "random_forest": rf_model is not None,
        "xgboost": xgb_model is not None,
        "scalers": scalers is not None
    })


# ==========================================================
# Prediction Endpoint
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        if rf_model is None and xgb_model is None:
            return jsonify({
                "success": False,
                "error": "Models are not loaded."
            }), 500

        if scalers is None:
            return jsonify({
                "success": False,
                "error": "Scaler file not loaded."
            }), 500

        data = request.get_json()

        # --------------------------------------------
        # Input Validation
        # --------------------------------------------

        try:
            amount = float(data.get("amount"))
            time_value = float(data.get("time"))

        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "error": "Amount and Time must be numeric."
            }), 400

        if amount < 0:

            return jsonify({
                "success": False,
                "error": "Amount cannot be negative."
            }), 400

        if time_value < 0:

            return jsonify({
                "success": False,
                "error": "Time cannot be negative."
            }), 400

        # --------------------------------------------
        # Scaling
        # --------------------------------------------

        amount_scaled = scalers["amount_scaler"].transform([[amount]])[0][0]
        time_scaled = scalers["time_scaler"].transform([[time_value]])[0][0]

        # --------------------------------------------
        # PCA Features
        # --------------------------------------------

        v_features = []

        for i in range(1, 29):
            v_features.append(float(data.get(f"v{i}", 0)))

        features = [time_scaled] + v_features + [amount_scaled]

        X = np.array(features).reshape(1, -1)

        print("\n==============================")
        print("Incoming Transaction")
        print("==============================")
        print(f"Amount : {amount}")
        print(f"Time   : {time_value}")
        print(f"Shape  : {X.shape}")

        results = {}

        # --------------------------------------------
        # Random Forest
        # --------------------------------------------

        if rf_model is not None:

            rf_prob = float(rf_model.predict_proba(X)[0][1])

            rf_pred = int(rf_prob >= 0.35)

            results["random_forest"] = {
                "prediction": rf_pred,
                "fraud_probability": round(rf_prob * 100, 2),
                "verdict": "FRAUD" if rf_pred else "LEGITIMATE"
            }

        # --------------------------------------------
        # XGBoost
        # --------------------------------------------

        if xgb_model is not None:

            xgb_prob = float(xgb_model.predict_proba(X)[0][1])

            xgb_pred = int(xgb_prob >= 0.35)

            results["xgboost"] = {
                "prediction": xgb_pred,
                "fraud_probability": round(xgb_prob * 100, 2),
                "verdict": "FRAUD" if xgb_pred else "LEGITIMATE"
            }

        # --------------------------------------------
        # Final Decision
        # --------------------------------------------

        probabilities = [m["fraud_probability"] for m in results.values()]

        average_probability = round(sum(probabilities) / len(probabilities), 2)

        final_verdict = (
            "FRAUD"
            if average_probability >= 35
            else "LEGITIMATE"
        )

        risk_level = get_risk_level(average_probability)

        print(f"Average Probability : {average_probability}%")
        print(f"Risk Level          : {risk_level}")
        print(f"Verdict             : {final_verdict}")
        print("==============================\n")

        return jsonify({

            "success": True,

            "final_verdict": final_verdict,

            "risk_level": risk_level,

            "confidence": average_probability,

            "amount": amount,

            "time": time_value,

            "models": results

        })

    except Exception as e:

        print(f"[ERROR] {e}")

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)