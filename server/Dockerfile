# Builder stage
FROM python:3.10-slim as builder

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app  # Consistent APP_HOME
WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.10-slim  # Use the same Python version as the builder

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app  # Consistent APP_HOME
WORKDIR $APP_HOME

RUN addgroup --system app && adduser --system --group app

# Copy only the installed dependencies from the builder stage
# This assumes your requirements install into the default site-packages path
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy your application code
COPY . .

USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
