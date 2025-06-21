FROM python:3.13-slim
WORKDIR /app

COPY app app
COPY config config
COPY data data
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]