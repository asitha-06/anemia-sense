from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request, send_from_directory
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

DATASET_PATH = BASE_DIR / "anemia.csv"

df = pd.read_csv(DATASET_PATH)

df.rename(
    columns={
        "Gender": "gender",
        "Hemoglobin": "hemoglobin",
        "MCH": "mch",
        "MCHC": "mchc",
        "MCV": "mcv",
        "Result": "target",
    },
    inplace=True,
)

FEATURES = ["gender", "hemoglobin", "mch", "mchc", "mcv"]

missing_columns = [
    column for column in FEATURES + ["target"]
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in anemia.csv: {missing_columns}"
    )

# Convert model inputs and target to numeric values.
for column in FEATURES + ["target"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df.dropna(subset=FEATURES + ["target"], inplace=True)

if df.empty:
    raise ValueError("The dataset has no valid rows.")

X = df[FEATURES]
y = df["target"]

if y.nunique() < 2:
    raise ValueError("The dataset must contain at least two target classes.")

# --------------------------------------------------
# Train machine-learning model
# --------------------------------------------------

x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
)

model.fit(x_train, y_train)

accuracy = accuracy_score(y_test, model.predict(x_test))

print(f"Model Accuracy: {accuracy:.4f}")


# --------------------------------------------------
# Serve frontend
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(str(BASE_DIR), "index.html")


@app.route("/script.js", methods=["GET"])
def javascript():
    return send_from_directory(str(BASE_DIR), "script.js")


@app.route("/styles.css", methods=["GET"])
def stylesheet():
    return send_from_directory(str(BASE_DIR), "styles.css")


@app.route("/animation.js", methods=["GET"])
def animation():
    return send_from_directory(str(BASE_DIR), "animation.js")


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "AnemiaSense backend is running",
    })


# --------------------------------------------------
# Prediction API
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Please submit valid JSON input."
            }), 400

        input_values = []

        for feature in FEATURES:
            if feature not in data:
                return jsonify({
                    "error": f"Missing required field: {feature}"
                }), 400

            value = float(data[feature])

            if not pd.notna(value):
                return jsonify({
                    "error": f"Invalid value for {feature}"
                }), 400

            input_values.append(value)

        sample = pd.DataFrame(
            [input_values],
            columns=FEATURES,
        )

        prediction = model.predict(sample)[0]

        # This assumes the dataset uses 0 for negative
        # and 1 for positive. Verify this against your dataset.
        result = (
            "You don't have any Anemic Disease"
            if prediction == 0
            else "You have Anemic Disease"
        )

        return jsonify({
            "result": result,
            "prediction": int(prediction),
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid numeric values."
        }), 400

    except Exception:
        app.logger.exception("Prediction failed")

        return jsonify({
            "error": "Prediction failed. Please try again."
        }), 500


# --------------------------------------------------
# Local development
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
