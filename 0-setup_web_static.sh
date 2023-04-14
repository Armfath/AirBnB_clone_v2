#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

command -v nginx &> /dev/null || sudo apt update &> /dev/null && sudo apt install -y nginx &> /dev/null
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server ipv6only=on;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files $uri $uri/ =404;
    }

    location /hbnb_static/ {
        alias /data/web_static/current/;
        autoindex off;
    }
}" > /etc/nginx/sites-available/hbnb_static
ln -sf /etc/nginx/sites-available/hbnb_static /etc/nginx/sites-enabled/
service nginx restart
