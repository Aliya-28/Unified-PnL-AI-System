import pandas as pd
import os
from sklearn.ensemble import IsolationForest

def detect_anomalies(file_path):

    # Load dataset
    df = pd.read_csv(file_path)

    # Select features for anomaly detection
    features = df[["revenue", "expense"]]

    # Create Isolation Forest model
    model = IsolationForest(contamination=0.05, random_state=42)

    # Fit model and predict anomalies
    df["anomaly"] = model.fit_predict(features)

    anomalies = df[df["anomaly"] == -1]

    print("\n------ ANOMALY DETECTION AGENT ------")
    print("\nDetected Anomalies:\n")

    print(anomalies[["date","department","revenue","expense"]].to_string(index=False))


if __name__ == "__main__":

    current_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(current_dir, "..", "data", "financial_data.csv")

    detect_anomalies(file_path)