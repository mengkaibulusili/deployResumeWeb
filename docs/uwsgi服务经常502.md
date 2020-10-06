# 现象 nginx 报错 502

# 日志报错

[pid: 1097|app: 0|req: 3/14] 106.119.3.43 () {44 vars in 1034 bytes} [Tue Oct 6 15:07:50 2020] GET /api/adminApp/getCandidateInfo/?data=%7B%22query_job_id%22:%22-1%22,%22page_index%22:%221%22,%22deliver_status%22:%22%E7%94%B3%E8%AF%B7%E4%B8%AD%22%7D => generated 66 bytes in 22 msecs (HTTP/1.1 200) 5 headers in 165 bytes (1 switches on core 0)
invalid request block size: 5814 (max 4096)...skip
invalid request block size: 5814 (max 4096)...skip
invalid request block size: 4894 (max 4096)...skip
invalid request block size: 4894 (max 4096)...skip

# 解决 buffer-size

```bash
<uwsgi>
   <socket>127.0.0.1:8999</socket> <!-- 内部端口，自定义 -->
   <chdir>/var/www/myServer/</chdir> <!-- 项目路径 -->
   <module>myServer.wsgi</module>  <!-- shopServer为wsgi.py所在目录名-->
   <processes>16</processes> <!-- 进程数 -->
   <buffer-size>65536</buffer-size>
   <daemonize>uwsgi.log</daemonize> <!-- 日志文件 -->
</uwsgi>
```
