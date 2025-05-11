FROM python:3.12-slim-bullseye

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (for packages like sentence-transformers/torch)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Preload the sentence-transformer model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-mpnet-base-v2')"

# Copy all other files
COPY . /app

# Expose FastAPI and Streamlit ports
EXPOSE 8001 8501

# Start both services (FastAPI and Streamlit)
CMD ["python", "run.py"]
