FROM python:3.7.11-slim

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y python3-pip python3-setuptools autoconf libtool pkg-config python3-dev build-essential

RUN pip install -r requirements.txt
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "3001", "opensight_restserver:app"]
