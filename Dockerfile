# Base image
FROM python:3.10-bullseye

WORKDIR /app

# Install dependencies for Qiskit Aer
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential gcc git libgomp1 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Start the Flask app
CMD ["python", "Qunix.py"]