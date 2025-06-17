FROM python:3.13-slim

ENV PORT=8080
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN adduser --disabled-password --gecos "" myuser && \
    chown -R myuser:myuser /app

# Copy application code
COPY . .

# Set non-root user
USER myuser

# Add user-local bin to PATH
ENV PATH="/home/myuser/.local/bin:$PATH"

# Expose port
EXPOSE ${PORT}

# Start server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]