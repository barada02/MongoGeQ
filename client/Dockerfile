FROM nginx:alpine

# Copy the static files to nginx html directory
COPY . /usr/share/nginx/html

# Copy the nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Create script to replace environment variables at runtime
RUN echo "#!/bin/sh" > /docker-entrypoint.d/40-generate-env-config.sh && \
    echo "envsubst '\$API_URL' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf.tmp" >> /docker-entrypoint.d/40-generate-env-config.sh && \
    echo "mv /etc/nginx/conf.d/default.conf.tmp /etc/nginx/conf.d/default.conf" >> /docker-entrypoint.d/40-generate-env-config.sh && \
    chmod +x /docker-entrypoint.d/40-generate-env-config.sh

# Expose port 80
EXPOSE 80

# The default nginx entrypoint will run our script
