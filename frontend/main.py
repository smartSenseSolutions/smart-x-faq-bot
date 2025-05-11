import requests
import streamlit as st

API_URL = "http://localhost:8001"

st.set_page_config(page_title="Smart-X FAQ Bot", layout="wide")

# --- Sidebar: Upload and Model Selection ---
with st.sidebar:
    st.header("📂 Train Model")

    uploaded_file = st.file_uploader(
        "Upload Excel file",
        type=["xlsx"],
        help="File must contain 'Question' and 'Label' columns",
    )

    if uploaded_file:
        model_type_display = st.selectbox("Select Model Type", ["Support Vector Machine", "Catboost"], index=0)
        model_type_map = {
            "Support Vector Machine": "svm",
            "Catboost": "catboost"
        }
        model_type = model_type_map[model_type_display]

        if st.button("🚀 Train"):
            with st.spinner("Training model..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/train",
                        files={"file": uploaded_file},
                        data={"model_type": model_type}
                    )
                    if response.status_code == 200:
                        st.success("✅ Training completed successfully!")
                    else:
                        st.error(f"❌ Training failed: {response.text}")
                except Exception as e:
                    st.error(f"🚫 Connection error: {e}")

    st.markdown("---")
    st.header("🧠 Choose a Model")
    try:
        model_response = requests.get(f"{API_URL}/api/models")
        if model_response.status_code == 200:
            models = model_response.json().get("models", [])
            selected_model = st.selectbox("Available Models", models)
        else:
            st.warning("⚠️ Could not fetch model list.")
            selected_model = None
    except Exception as e:
        st.warning(f"⚠️ Failed to load models: {e}")
        selected_model = None

# --- Main Area: Query and Response ---
st.title("`Smart-X FAQ Bot:` Intent Classification")

st.markdown(
    """
Enter a question below to classify its intent and fetch the corresponding answer based on the selected model.
"""
)

if "response" not in st.session_state:

    st.session_state.response = None

user_input = st.text_area("💬 Enter your query")

if st.button("🔍 Predict Intent") and user_input.strip():
    try:
        payload = {"query": user_input}
        params = {"model": selected_model} if selected_model else {}

        response = requests.post(f"{API_URL}/api/predict", json=payload, params=params)
        if response.status_code == 200:
            st.session_state.response = response.json()
        else:
            st.error(f"❌ API Error: {response.status_code}")
    except Exception as e:
        st.error(f"🚫 Connection error: {e}")

# --- Show Prediction ---
if st.session_state.response:
    st.success(f"🧠 **Predicted Intent:** `{st.session_state.response['intent']}`")
    st.info(f"📖 **Answer:** {st.session_state.response['answer']}")
    st.write(
        f"📊 **Confidence:** `{st.session_state.response['confidence'] * 100:.2f}%`"
    )
