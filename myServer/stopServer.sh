nginx -s stop  -c /var/www/myServer/nginx/myNginx.conf && \
pkill -9  uwsgi && \
pkill -9  python3