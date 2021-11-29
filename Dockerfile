FROM python:3.10.0-slim

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3001", "--workers", "4", "opensight_restserver:app"]
