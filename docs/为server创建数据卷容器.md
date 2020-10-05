## 构建后台数据卷镜像

```bash
docker build -f DockerfileDataVolum  -t registry.cn-hangzhou.aliyuncs.com/mkmk/data_volume:resumeweb .
```

## 构建 服务镜像

docker build -f resumeDockerFile -t registry.cn-hangzhou.aliyuncs.com/mkmk/centos:resumeServer .

## 创建数据容器但不运行

docker create --name djangoVolume registry.cn-hangzhou.aliyuncs.com/mkmk/data_volume:resumeweb

## 启动服务

docker run -d --name resumeServer --net resumeweb --ip 192.168.200.201 -p 15000:5000 --volumes-from djangoVolume --privileged=true registry.cn-hangzhou.aliyuncs.com/mkmk/centos:resumeServer

# 查看启动日志

docker logs resumeServer

# 暂停与删除所有容器

docker stop $(docker ps -aq) | docker rm  $(docker ps -aq)
