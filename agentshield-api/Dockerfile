FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy AgentShield package from parent directory
COPY agentshield ./agentshield
COPY pyproject.toml ./
COPY requirements-hackathon.txt ./

# Install AgentShield dependencies
RUN pip install --no-cache-dir -r requirements-hackathon.txt

# Copy API code
COPY agentshield-api/requirements.txt ./api-requirements.txt
RUN pip install --no-cache-dir -r api-requirements.txt

COPY agentshield-api/main.py ./

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
