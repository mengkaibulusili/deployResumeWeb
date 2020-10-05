# 华为云链接

https://mirrors.huaweicloud.com/

# centos 安装 docker

1、若您安装过 docker，需要先删掉，之后再安装依赖:

## 1 centos 安装 docker 依赖

```bash
sudo yum remove docker docker-common docker-selinux docker-engine
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

2、根据版本不同，下载 repo 文件。您使用的发行版：
CentOS/RHEL

## 2 软件仓库地址替换为：

```bash
wget -O /etc/yum.repos.d/docker-ce.repo https://mirrors.huaweicloud.com/docker-ce/linux/centos/docker-ce.repo
```

```bash
sudo sed -i 's+download.docker.com+mirrors.huaweicloud.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
```

## 3、更新索引文件并安装

```bash
sudo yum makecache fast
sudo yum install docker-ce
```
