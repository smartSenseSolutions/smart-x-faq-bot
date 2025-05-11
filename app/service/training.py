import os
import joblib
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer

from app.core.config import INTENT_ANSWER_JSON

def train_model(file_location: str, model_type: str = 'svm'):
    # Load dataset from the uploaded Excel file
    try:
        df = pd.read_excel(file_location)
    except Exception as e:
        raise Exception(f"Error reading the dataset: {e}")

    # Validate the columns
    if "Question" not in df.columns or "Label" not in df.columns:
        raise Exception("Uploaded file must contain 'Question' and 'Label' columns.")

    # Extract questions and labels
    questions = df["Question"].astype(str).tolist()
    labels = df["Label"].astype(str).tolist()

    # Encode questions with SentenceTransformer
    embedder = SentenceTransformer("all-mpnet-base-v2")
    embeddings = embedder.encode(questions, normalize_embeddings=True)

    # Encode labels
    le = LabelEncoder()
    encoded_labels = le.fit_transform(labels)

    # Stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        embeddings,
        encoded_labels,
        test_size=0.1,
        random_state=42,
        stratify=encoded_labels,
    )

    if model_type == 'catboost':
        # Define and train the CatBoost classifier
        clf = CatBoostClassifier(
            iterations=1000,
            learning_rate=0.05,
            depth=6,
            early_stopping_rounds=50,
            use_best_model=True,
            verbose=100,
            loss_function="MultiClass",
            eval_metric="Accuracy",
            random_seed=42,
        )

        clf.fit(X_train, y_train, eval_set=(X_test, y_test))

        model_dir = f"models/catboost_model_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}"
        os.makedirs(model_dir, exist_ok=True)

        joblib.dump(clf, os.path.join(model_dir, "intent_classifier.pkl"))
        joblib.dump(le, os.path.join(model_dir, "label_encoder.pkl"))
        # embedder.save(model_dir)

    elif model_type == 'svm':
        # Define parameter grid for GridSearchCV
        param_grid = {
            'C': [0.1, 1, 10, 100, 1000],
            'kernel': ['linear'],
            'probability': [True],
        }

        clf = SVC(random_state=42)

        grid_search = GridSearchCV(clf, param_grid, cv=5, n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)

        best_svm_model = grid_search.best_estimator_

        model_dir = f"models/svm_model_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}"
        os.makedirs(model_dir, exist_ok=True)

        joblib.dump(best_svm_model, os.path.join(model_dir, "intent_classifier.pkl"))
        joblib.dump(le, os.path.join(model_dir, "label_encoder.pkl"))
        # embedder.save(model_dir)

    else:
        raise Exception(f"Unknown model type: {model_type}")

    # Evaluate model performance
    if model_type == 'catboost':
        y_pred = clf.predict(X_test)
    elif model_type == 'svm':
        y_pred = best_svm_model.predict(X_test)

    y_pred_labels = le.inverse_transform(y_pred)
    y_true_labels = le.inverse_transform(y_test)
    report = classification_report(y_true_labels, y_pred_labels)

    # Return classification report
    return report
