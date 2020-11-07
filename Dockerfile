FROM python:alpine3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "opensight_restserver.py"]
