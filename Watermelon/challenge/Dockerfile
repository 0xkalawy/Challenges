FROM php:8.2-fpm

# Install NGINX and other utils
RUN apt update && apt install -y nginx

# Setup directory
RUN mkdir -p /var/www/html/uploads

# Copy app and config
COPY www /var/www/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY flag.txt /flag.txt

# Permissions
RUN chmod 644 /flag.txt

# Start PHP and NGINX
EXPOSE 80
CMD service nginx start && php-fpm
