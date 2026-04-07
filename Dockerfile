# 1. Use Bullseye (Full Debian) to avoid the "Short Read/EOF" network errors
FROM python:3.10-bullseye

# 2. Set necessary environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# 3. Install minimal system tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy your code
COPY . .

# 6. Initialize your packages
RUN touch env/__init__.py server/__init__.py

# 7. Start the simulation server
CMD ["python", "-m", "server.app"]