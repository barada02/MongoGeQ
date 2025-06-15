FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Expose is optional in Cloud Run, but helps documentation
#EXPOSE 8000

# CMD uses the PORT provided by Cloud Run
CMD ["uvicorn", "main:app"]
