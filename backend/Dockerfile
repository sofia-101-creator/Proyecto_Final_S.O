FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --uid 10001 --create-home appuser
COPY --chown=appuser:appuser app.py .
USER appuser
EXPOSE 5000
CMD ["gunicorn", "--workers", "1", "--threads", "8", "--bind", "0.0.0.0:5000", "--timeout", "60", "--access-logfile", "-", "app:app"]
