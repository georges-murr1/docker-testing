FROM python:3.9

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py /app/main.py

# Run as non-root user
RUN adduser --disabled-password --gecos "" appuser
USER appuser

CMD ["python", "/app/main.py"]
