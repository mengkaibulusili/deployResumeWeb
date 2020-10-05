cd /root/myServer && \
source /root/.bashrc && \
yum install mysql-devel -y && \
pip3 install -r  /root/myServer/requirements.txt && \
uwsgi -x /root/myServer/myServer.xml && \
nginx -t  -c /root/myServer/nginx/myNginx.conf && \
nginx  -c /root/myServer/nginx/myNginx.conf 
tail -f /dev/null