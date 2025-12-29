from flask import Flask, jsonify, render_template
import psutil
import pandas as pd
from sklearn.ensemble import IsolationForest
from joblib import dump, load
import os

app = Flask(__name__)
HISTORY_FILE = "process_history.csv"
MODEL_FILE = "isolation_forest_model.joblib"

def get_process_data():
    process_data = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'io_counters']):
        try:
            io = proc.info['io_counters']
            disk = io.read_bytes + io.write_bytes if io else 0
            process_data.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_percent'],
                'disk': disk
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return pd.DataFrame(process_data)

def update_history(df):
    if not df.empty:
        if not os.path.exists(HISTORY_FILE):
            df.to_csv(HISTORY_FILE, index=False)
        else:
            df.to_csv(HISTORY_FILE, mode='a', index=False, header=False)

def train_model():
    historical_df = pd.read_csv(HISTORY_FILE) if os.path.exists(HISTORY_FILE) else pd.DataFrame()
    current_df = get_process_data()
    update_history(current_df)

    combined_df = pd.concat([historical_df, current_df], ignore_index=True)
    combined_df.fillna(0, inplace=True)
    if combined_df.empty:
        return None

    X = combined_df[['cpu','memory','disk']]
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    dump(model, MODEL_FILE)
    return model

def detect_anomalies():
    current_df = get_process_data()
    if current_df.empty:
        return []

    model = load(MODEL_FILE) if os.path.exists(MODEL_FILE) else train_model()
    if model is None:
        return []

    current_df['anomaly'] = model.predict(current_df[['cpu','memory','disk']])
    anomalies = current_df[current_df['anomaly'] == -1]
    return anomalies.to_dict(orient='records')

@app.route("/data")
def data():
    anomalies = detect_anomalies()
    return jsonify(anomalies)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # Always run on localhost:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
