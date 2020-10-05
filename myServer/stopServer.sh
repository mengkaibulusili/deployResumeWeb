nginx -s stop  -c /root/myServer/nginx/myNginx.conf && \
pkill -9  uwsgi && \
pkill -9  python3