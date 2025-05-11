import subprocess
import time
import threading

def run_fastapi():
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "frontend/main.py","--server.port", "8501","--server.headless", "true" ])

# Start FastAPI in a thread
api_thread = threading.Thread(target=run_fastapi)
api_thread.start()

# Give FastAPI a second to boot
time.sleep(2)

# Run Streamlit in main thread
run_streamlit()
