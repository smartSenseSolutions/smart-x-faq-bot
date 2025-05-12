# **Smart-X FAQ Bot**

# 1. Overview

**Smart-X FAQ Bot** is an intent classification system designed to assist users by identifying their queries underlying intent and providing a corresponding pre-defined response. It integrates modern NLP techniques with traditional machine learning classifiers to offer accurate question-answering capabilities.

![Smart-X FAQ Bot](smart-x-faq-bot.svg)


# 2. Motivation

With an increasing number of repetitive and predictable queries in customer support, there is a growing demand for systems that can automatically understand and respond to these.

# 3. Architectural Components

The system comprises the following core components:

## 3.1 FastAPI Backend

* Handles **REST API** requests.  
* Routes include /predict, /train, and /models.  
* Responsible for invoking model training and inference logic.

## 3.2 SentenceTransformer (MPNet)

* Used to generate semantic embeddings of user queries.  
* Pretrained model “**all-mpnet-base-v2**” selected for its high accuracy and performance on semantic similarity tasks.  
* Leveraging **pretrained** **embeddings** significantly reduces training time and improves generalization, even on smaller datasets.

## 3.3 Intent Classifiers

* **Support Vector Machine** (SVM): Performs well for high-dimensional, sparse data like sentence embeddings.  
* **CatBoost**: Chosen for its robustness, built-in handling of categorical data, and superior accuracy in classification tasks.

## 3.4 Model Management

* Trained models are saved in timestamped folders under the **models/directory**.  
* Each model contains a label\_encoder.pkl and **intent\_classifier.pkl**.

## 3.5 Streamlit Frontend

* Allows users to **upload** training data and **chat** with the bot.  
* **Visual interface** for selecting models, entering queries, and viewing predictions.

## 3.6 Dockerized Deployment

* Enables the **combined deployment** of backend (FastAPI) and frontend (Streamlit) services.

# 4. Model Training, Accuracy, and Decisions

## 4.1 Data Format

The model expects training data in Excel format with the following columns:

* **Question**: The user query.  
* **Label**: The target intent.

## 4.2 Accuracy and Evaluation

* The system uses a **stratified** train-test split (90/10) to maintain class distribution.  
* **Evaluation metric**: Classification report including precision, recall, and F1-score.

Observed Performance

* Depending on the **dataset**, classification accuracy is subject to **data balance**.  
* **SVM**: Tends to be more consistent and interpretable for smaller datasets.  
* **CatBoost**: Often yields higher accuracy for large datasets, faster convergence, and better performance.  
* **Why SentenceTransformer?**  
  * Provides contextualized sentence embeddings, improving classification accuracy over traditional TF-IDF.  
* **Why MPNet pretrained embeddings?**  
  * Reduces the dependency on large training data and accelerates the training pipeline. MPNet is known for its state-of-the-art results on semantic textual similarity tasks.  
* **Why Model Flexibility (SVM/CatBoost)?**  
  * Enables benchmarking and performance comparison.

# 5. Conclusion and Observations

Smart-X FAQ Bot combines the simplicity of classical ML with the effectiveness of modern embeddings to deliver a high-performance FAQ system. Its modular, Dockerized structure ensures ease of deployment, retraining, and extension. The use of pretrained MPNet embeddings contributes to its robustness and minimizes the need for extensive training data, making it a reliable and efficient solution for applications.

* **Model accuracy** is dependent on training **data quality**.  
* Does not handle **multi-intent** queries.  
* **Answers** are limited to predefined mappings in **intent\_answers.json**.