# containomaly

A Python-based anomaly detection system that monitors containers, collects runtime data via an agent, and detects anomalies using Isolation Forest.

## Components
- **Agent**: Collects output (for example something like `docker ps -a --format json`) and sends it to the server.
- **Server**: Receives, stores, and analyzes data for anomalies.

## Setup
```bash
git clone https://github.com/ramadasmr/containamoly.git
cd containamoly
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Structure
- **agent/** → collects Docker info
- **server/** → receives & stores data
- **ml/** → machine learning models

### To be implemented
- Agent data collector
- Server endpoint
- TSDB integration
- Anomaly detection
