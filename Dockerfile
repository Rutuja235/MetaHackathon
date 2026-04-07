FROM python:3.10-slim

WORKDIR /app

# 1. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

# 2. Upgrade pip and install core dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the application
COPY . .

# 4. Ensure environment is recognized as a package
RUN touch env/__init__.py
RUN touch server/__init__.py

# 5. Set the PYTHONPATH so the server can find 'env' and 'server'
ENV PYTHONPATH=/app

# 6. Start the server using the module flag
# This bypasses the need for 'pip install -e .' but does the exact same thing
CMD ["python", "-m", "server.app"]
