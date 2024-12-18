# 框架-python
树莓派开发板后台代码的python版本（适用于amd框架）
---
## 介绍
### 依赖的docker镜像
#### 树莓派开发板环境 (arm)：
```shell
docker run -d \
--name framework-python \
--network=host \
-v /mapdata:/home/ya/mapdata \
cbtai-hao.tencentcloudcr.com/cbtai/pydocker-gstreamer-arm:0.1.1
```
#### amd64 环境：
```shell
docker run -d \
--name framework-python \
--network=host \
-v /mapdata:/home/ya/mapdata \
cbtai-hao.tencentcloudcr.com/cbtai/pydocker-gstreamer-amd:0.1.1
```
#### 注意：
docker镜像包含运行项目所需要的全部依赖

---
## 运行
将项目代码下载到本地后，根据上面的环境运行对应的docker镜像，然后将代码映射到启动的docker容器内，映射路径为 `~/framework-python -> /home/ya`，然后 `docker exec -it framework-python /bin/bash` 进入到容器内，并且输入`service ssh start && cd /home/ya && gunicorn -c gunicorn_conf.py app.wsgi:app`启动项目

