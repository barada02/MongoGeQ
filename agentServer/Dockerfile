FROM python:3.10-slim

WORKDIR /app

# Copy all code before install
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) Create non-root user
# RUN adduser --disabled-password --gecos "" myuser && chown -R myuser:myuser /app
# USER myuser
# ENV PATH="/home/myuser/.local/bin:$PATH"

# Start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
