# framework-python
Raspberry PI development board background framework code python version

---
## Instructions
### Dependent docker image
#### Raspberry PI development (arm)：
```shell
docker run -d \
--name framework-python \
--network=host \
-v /mapdata:/home/ya/mapdata \
cbtai-hao.tencentcloudcr.com/cbtai/pydocker-gstreamer-arm:0.1.1
```
#### amd64 development：
```shell
docker run -d \
--name framework-python \
--network=host \
-v /mapdata:/home/ya/mapdata \
cbtai-hao.tencentcloudcr.com/cbtai/pydocker-gstreamer-amd:0.1.1
```
#### NOTE：
The docker image contains all the dependencies needed to run the project

---
## RUN
After downloading the project code to the local, run the corresponding docker image according to the above environment, and then map the code to the startup docker container, the mapping path is `~/framework-python -> /home/ya`. Then `docker exec-it framework-python /bin/bash` goes into the container, And enter `service ssh start && cd /home/ya && gunicorn -c gunicorn_conf.py app.wsgi:app` to start the project

