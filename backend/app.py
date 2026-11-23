import os
import socket
import time
from flask import Flask, jsonify, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
INSTANCE = os.getenv("SERVER_NAME", "sin-nombre")
REQUESTS = Counter("backend_http_requests_total", "Respuestas de la aplicacion", ["instance_name", "method", "route", "status"])
LATENCY = Histogram("backend_http_request_duration_seconds", "Latencia del backend en segundos", ["instance_name", "method", "route"], buckets=(.005, .01, .025, .05, .1, .25, .5, 1, 2, 5, 10))

@app.before_request
def start_timer():
    g.started = time.perf_counter()

@app.after_request
def record_response(response):
    response.headers["X-Backend"] = INSTANCE
    if request.path not in ("/metrics", "/health"):
        route = request.url_rule.rule if request.url_rule else "unmatched"
        REQUESTS.labels(INSTANCE, request.method, route, str(response.status_code)).inc()
        LATENCY.labels(INSTANCE, request.method, route).observe(time.perf_counter() - g.started)
    return response

@app.get("/")
def index():
    time.sleep(.03)
    return f"<h1>Proyecto final - {INSTANCE}</h1><p>Contenedor: {socket.gethostname()}</p>\n"

@app.get("/health")
def health():
    return jsonify(status="ok", server=INSTANCE)

@app.get("/headers")
def headers():
    return jsonify(server=INSTANCE, ip_que_ve_flask=request.remote_addr, cabeceras=dict(request.headers))

@app.get("/slow")
def slow():
    try:
        ms = max(0, min(int(request.args.get("ms", "500")), 2000))
    except ValueError:
        return jsonify(error="ms debe ser un entero"), 400
    time.sleep(ms / 1000)
    return jsonify(server=INSTANCE, espera_ms=ms)

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
