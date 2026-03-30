FROM python:3.12-slim

WORKDIR /app

# Install Docker client libs
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create dirs
RUN mkdir -p /app/logs /app/reports

CMD ["python", "monitor.py"]

