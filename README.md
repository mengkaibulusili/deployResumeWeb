# deployResumeWeb

部署招聘系统

# 部署过程

## 构建后台数据卷镜像

```bash
docker build -f DockerfileDataVolum  -t registry.cn-hangzhou.aliyuncs.com/mkmk/data_volume:resumeweb .
```

## 构建 服务镜像

docker build -f resumeDockerFile -t registry.cn-hangzhou.aliyuncs.com/mkmk/centos:resumeServer .

## 创建数据容器但不运行

docker create --name djangoVolume registry.cn-hangzhou.aliyuncs.com/mkmk/data_volume:resumeweb

docker run -d --name resumeServer --net resumeweb --ip 192.168.200.201 -p 13000:3000 -p 15000:5000 --volumes-from djangoVolume --privileged=true registry.cn-hangzhou.aliyuncs.com/mkmk/centos:resumeServer

## 注意

mysql 内部 ip 为 root@192.168.200.200
