FROM cbtai-hao.tencentcloudcr.com/cbtai/pydocker-gstreamer-arm:0.1.1
EXPOSE 8080 8022
# Add main app2
COPY ./app /home/ya/app
COPY ./config /home/ya/config
COPY ./gunicorn_conf.py /home/ya/
COPY ./README.md /home/ya/

CMD ["sh","-c","service ssh start && tail -f /dev/null 2>&1"]
