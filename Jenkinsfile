#!/usr/bin/env groovy
pipeline {
    agent any
    environment {
        registry = "cbtai-hao.tencentcloudcr.com/cbtai"
        name = 'framework-python'
        tag = "0.1.1-amd"
        // dev表示开发状态 prod表示发布状态
//         build = 'dev'
         build = 'prod'
        // 分别指定开发中对外的端口号v
        http_port = '28481'
        ssh_port = '28122'
        basepath = '/mapdata'
        // 指定配置文件路径
        confpath = '/config/pyjetson'
    }

    stages {
        stage('Checkout') {
            steps {
              checkout scm
            }
        }
         stage('Build Image'){
                steps {
                   script{
                     env.PATH = "/usr/local/bin:" + "${env.PATH}"
                     env.PATH = "/usr/bin:" + "${env.PATH}"
                   sh "docker build -t $registry/$name:$tag ."
                   }
                }
             }
         stage('Push Image'){
                steps {
                    script{
                       sh "docker push $registry/$name:$tag"
                   }
                }
           }
        stage('stop run image'){
            steps{
                script{
                    if(build == 'dev'){
                        try{
                            sh  "docker stop $name"
                        } catch(Exception e){
                            echo '异常发生' + e.toString()
                        }
                       sleep(time:1,unit:"SECONDS")
                       try{
                            sh  "docker rm $name"
                        } catch(Exception e){
                            echo '异常发生' + e.toString()
                        }
                    }else{
                        // 保存到tar包
                        sh "docker rmi $registry/$name:$tag"
                        echo "sudo docker run --rm -d --name $name -p $http_port:8080 -p $ssh_port:8022 " +
                        "-v $confpath:/home/ya/config " +
                        "-v $basepath:/home/ya/mapdata " +
                        "--gpus all " +
                        "$registry/$name:$tag " +
                        " sh -c \"service ssh start && cd /home/ya && celery -A app.tasks multi start worker -Q celery.train -P solo --pidfile=/var/run/celery/celery.pid && gunicorn -c gunicorn_conf.py app.wsgi:app\" "
                    }
                }
            }
        }
        stage('run image'){
            steps{
                script{
//                 发布环境不需要运行
                   if(build == 'dev'){
                      sh  "sudo docker run --rm -d --name $name -p $http_port:8080 -p $ssh_port:8022 " +
                      "-v $bonfpath:/home/ya/config " +
                      "-v $basepath:/home/ya/mapdata " +
                      "--gpus all  " +
                      "$registry/$name:$tag "
                   }
                }
            }
        }
         stage('test image'){
            steps{
                script{
                   if(build == 'dev'){
                      sh "netstat -lntu |grep $ssh_port"
                   }
                }
            }
        }
    }
}
