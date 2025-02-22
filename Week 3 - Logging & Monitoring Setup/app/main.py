import time
import random
from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram
from starlette.responses import Response
from loguru import logger

app = FastAPI()

# Configure Loguru Logging
logger.add("logs/app.log", rotation="10MB", retention="10 days", level="INFO")

# Prometheus Metrics
REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency in seconds")

@app.get("/")
def read_root():
    """Dummy Endpoint to Simulate API Calls"""
    REQUEST_COUNT.inc()  # Increment request count

    start_time = time.time()
    time.sleep(random.uniform(0.1, 1))  # Simulate processing time
    duration = time.time() - start_time
    REQUEST_LATENCY.observe(duration)

    logger.info(f"Request completed in {duration:.2f} seconds")
    
    return {"message": "Hello, World!", "response_time": f"{duration:.2f} sec"}

@app.get("/metrics")
def metrics():
    """Expose Prometheus Metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
