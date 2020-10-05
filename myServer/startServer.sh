cd /var/www/myServer && \
source /root/.bashrc && \
pip3 install -r  /var/www/myServer/requirements.txt && \
uwsgi -x /var/www/myServer/myServer.xml && \
nginx -t  -c /var/www/myServer/nginx/myNginx.conf && \
nginx  -c /var/www/myServer/nginx/myNginx.conf && \
tail -f /dev/null