FROM python:alpine3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3001", "opensight_restserver:app"]
