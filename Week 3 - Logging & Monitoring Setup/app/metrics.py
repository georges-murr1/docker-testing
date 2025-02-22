from prometheus_client import Counter, Histogram
import time

# Define metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

def track_request():
    REQUEST_COUNT.inc()

def track_latency(start_time):
    duration = time.time() - start_time
    REQUEST_LATENCY.observe(duration)
