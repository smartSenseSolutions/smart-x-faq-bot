# Smart-X FAQ Bot

A FastAPI + Streamlit application for classifying user queries into intents using ML models like SVM and CatBoost. It supports training on custom data, intent prediction, and interactive querying via a web interface.

---

## 📁 Project Structure

```
smart-x-faq-bot/
├── app/
│   ├── controller/
│   │   └── intent_controller.py       # API endpoints for predict, train, and model list
│   ├── core/
│   │   └── config.py                  # Constants and config loading
│   ├── service/
│   │   ├── intent_service.py         # Logic to run predictions
│   │   └── training.py               # Model training logic
│   └── __init__.py
├── architecture/
│   ├── architecture.md               # Architecture description and explanation
│   └── smart-x-faq-bot.svg           # SVG diagram of system architecture
├── data/
│   ├── uploaded_data/                # Uploaded training files
│   ├── intent_answers.json           # Mapping of intent to answer
|   └── sample_sports_data.xlsx          # Sample training data
├── frontend/
│   └── main.py                       # Streamlit UI for training and prediction
├── models/                           # Auto-generated after training
├── main.py                           # FastAPI app entry
├── run.py                            # Runs both FastAPI and Streamlit apps
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Containerization setup
└── .gitignore
```
## 📁 Architecture

* Architecture: [Read detailed architecture explanation here](architecture/architecture.md)

---

## 🚀 Features

* Upload training data (`.xlsx`) with `Question` and `Label` columns.
* Choose and train models (`SVM` or `CatBoost`).
* View available trained models.
* Predict intent from user queries.
* Streamlit UI for ease of interaction.
* REST API support for integration.

---

## 📦 Installation

### 1. Clone and Set Up

```bash
git clone <repo-url>
cd <repo-folder>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python run.py
```

* FastAPI runs at: [http://localhost:8001/docs](http://localhost:8001/docs)
* Streamlit UI at: [http://localhost:8501](http://localhost:8501)

---

## 📊 Sample Data Format

Upload a `.xlsx` file with the following structure:

| Question                    | Label        |
| --------------------------- | ------------ |
| How many players in a team? | team\_info   |
| What is the duration?       | match\_rules |

Use `sample_sports_data.xlsx` as a reference.

---

## 🔧 API Endpoints

| Method | Endpoint       | Description                     |
| ------ | -------------- | ------------------------------- |
| POST   | `/api/predict` | Predicts intent from a query    |
| GET    | `/api/models`  | Lists all available models      |
| POST   | `/api/train`   | Trains model with uploaded file |

---
## 🐳 Docker

```dockerfile
# Build
docker build -t smart-x-faq-bot .

# Run with volume mounts
docker run -p 8001:8001 -p 8501:8501 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data/uploaded_data:/app/data/uploaded_data \
  smart-x-faq-bot
```

---

## 🧠 Model Logic

* Uses the pretrained transformer model `all-mpnet-base-v2` from `sentence-transformers` to embed queries into semantic vector space.
* Classifies intents using:

  * **SVM**: GridSearchCV-tuned Support Vector Classifier (linear kernel)
  * **CatBoost**: Optimized gradient boosting classifier for multiclass prediction
* Saves models to `/models/<model_type>_<timestamp>/`

---

