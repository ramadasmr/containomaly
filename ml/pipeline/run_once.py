from ml.db.influx_reader import fetch_recent_snapshots
from ml.features.container_features import extract_features
from ml.rules.rule_engine import detect_anomalies
from ml.state.memory import feature_history


def run_once():
    print("Fetching snapshots from Influx...")
    raw = fetch_recent_snapshots(minutes=5)

    print(f"Total {len(raw)} raw records received")

    print("Extracting features...")
    features = extract_features(raw)

    print("Running rule engine...")
    anomalies = detect_anomalies(features, feature_history)

    print(f"Total {len(anomalies)} anomalies detected")

    from ml.db.influx_writer import write_anomalies
    write_anomalies(anomalies)

    print("Pipeline run completed")


if __name__ == "__main__":
    run_once()
