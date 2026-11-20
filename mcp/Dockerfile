FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY server.py ./

USER 10001:10001
CMD ["sh", "-c", "exec python -m uvicorn server:app --host \"${HOST:-0.0.0.0}\" --port \"${PORT:-8001}\""]
