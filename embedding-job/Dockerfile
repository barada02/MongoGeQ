FROM python:3.11-slim

WORKDIR /app

COPY main.py .
COPY Corona2.json .

RUN pip install --no-cache-dir \
    google-cloud-aiplatform \
    pymongo \
    dnspython

CMD ["python", "main.py"]
