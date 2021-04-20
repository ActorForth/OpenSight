FROM python:alpine3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn"  , "-b", "0.0.0.0:3001", "opensight_restserver:app", "--timeout=600", "-w 6"]
