from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

# Load and preprocess dataset
df = pd.read_csv(BASE_DIR / "anemia.csv")

df.rename(columns={
    'Gender': 'gender',
    'Hemoglobin': 'hemoglobin',
    'MCH': 'mch',
    'MCHC': 'mchc',
    'MCV': 'mcv',
    'Result': 'target'
}, inplace=True)

X = df[['gender', 'hemoglobin', 'mch', 'mchc', 'mcv']]
y = df['target']

x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(x_train, y_train)

print("Model Accuracy:", accuracy_score(y_test, model.predict(x_test)))


# Serve frontend
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/script.js")
def javascript():
    return send_from_directory(BASE_DIR, "script.js")


@app.route("/styles.css")
def stylesheet():
    return send_from_directory(BASE_DIR, "styles.css")


@app.route("/animation.js")
def animation():
    return send_from_directory(BASE_DIR, "animation.js")


# Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        features = [
            'gender',
            'hemoglobin',
            'mch',
            'mchc',
            'mcv'
        ]

        input_values = [
            float(data[feature]) for feature in features
        ]

        sample = pd.DataFrame(
            [input_values],
            columns=features
        )

        prediction = model.predict(sample)[0]

        result = (
            "You don't have any Anemic Disease"
            if prediction == 0
            else "You have Anemic Disease"
        )

        return jsonify({"result": result})

    except (ValueError, TypeError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({"error": "Prediction failed"}), 500
