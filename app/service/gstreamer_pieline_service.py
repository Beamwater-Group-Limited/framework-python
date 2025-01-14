import json
import time

import requests
from gi.repository import Gst, GLib

Gst.init(None)
import cv2
import threading
from app.service.prefect_service import PrefectRun
from app.untils.frame_deal import get_rgb_frame
import base64
import os
import yaml

gstreamer_run_yaml_path = "/home/ya/mapdata/gstreamer_run.yaml"


class GstreamerPiePline:
    """
    gstreamer启动，关闭流程
    """

    # GStreamer类初始化
    def __init__(self, gstreamer_config, camera_data):
        print(gstreamer_config)
        self.camera_data = camera_data
        self.gstreamer_config = gstreamer_config
        # 设置挂载
        self.process_mount = gstreamer_config['process_mount']
        # 默认第一个列表
        self.loop = GLib.MainLoop()
        # 判断是否在识别
        self.is_detect = False
        # 文字输出
        self.text_overlay = None
        # 语音输出
        self.audio_appsrc = None
        # 获取gstreamer语句
        self.gstreamer_command = self._create_gs_command(gstreamer_config, camera_data)
        print(self.gstreamer_command)

        self.pipeline = None  # 推迟创建管道的时机，用于进程适配

    # 创建GStreamer语句
    def _create_gs_command(self, gstreamer_config, camera_data):
        if gstreamer_config["gs_output_type"] == "Audio":
            output = "autoaudiosink"
        else:
            output = f"rtspclientsink location={gstreamer_config['gs_output_data']}"
        if gstreamer_config["gs_input_type"] != "Stream":
            return f"""
            appsrc name=source is-live=true format=time caps="image/png, framerate=30/1" ! \
            pngdec ! \
            videoconvert ! \
            tee name=t ! \
            queue ! \
            textoverlay name=overlay text="初始文本" valignment=top halignment=left ! \
            x264enc tune=zerolatency speed-preset=ultrafast bitrate=3000 key-int-max=60 bframes=0 ! \
            queue max-size-buffers=50 ! mux. \
            appsrc name=audio_appsrc is-live=true format=time do-timestamp=true ! \
            decodebin ! audioconvert ! avenc_aac ! queue max-size-buffers=50 ! mux. \
            mpegtsmux name=mux ! \
            {output} \
            t. ! queue max-size-buffers=10 ! appsink name=mysink drop=false max-buffers=10
            """
        else:
            return f"""
            rtspsrc location={camera_data['rtsp_url']} latency=0 ! \
            {'rtph264depay' if camera_data["encode"] == 'H264' else 'rtph265depay'} ! \
            {'avdec_h264' if camera_data["encode"] == 'H264' else 'avdec_h265'} ! \
            videoconvert ! \
            tee name=t ! \
            queue ! \
            textoverlay name=overlay text="初始文本" valignment=top halignment=left ! \
            x264enc tune=zerolatency speed-preset=ultrafast bitrate=3000 key-int-max=60 bframes=0 ! \
            queue ! mux. \
            appsrc name=audio_appsrc is-live=true format=time do-timestamp=true ! \
            decodebin ! audioconvert ! avenc_aac ! queue ! mux. \
            mpegtsmux name=mux ! \
            {output} \
            t. ! queue ! appsink name=mysink drop=false max-buffers=10
            """

    # 创建GStreamer管道
    def _create_pipeline(self):
        pipeline = Gst.parse_launch(self.gstreamer_command)
        appsink = pipeline.get_by_name(f"mysink")
        appsink.set_property("emit-signals", True)
        appsink.connect("new-sample", self.process_frame)
        self.text_overlay = pipeline.get_by_name(f"overlay")
        # 设置时间
        self.audio_appsrc = pipeline.get_by_name("audio_appsrc")
        caps = Gst.Caps.from_string(
            "audio/x-raw, format=S16LE, rate=44100, channels=1, layout=interleaved")
        self.audio_appsrc.set_property("format", Gst.Format.TIME)
        self.audio_appsrc.set_property("is-live", True)
        self.audio_appsrc.set_property("do-timestamp", True)
        self.audio_appsrc.set_property("emit-signals", True)
        self.audio_appsrc.set_property("caps", caps)
        # 获取 appsrc 元素
        self.appsrc = pipeline.get_by_name("source")
        return pipeline

    # 回调函数处理
    # 调用prefect流，调用相关的函数
    def process_frame(self, sink):
        # 调用一次判断，是否停止
        self.judge_stop()
        try:
            sample = sink.emit("pull-sample")
            if sample:
                buf = sample.get_buffer()
                data = buf.extract_dup(0, buf.get_size())

                flow_yaml_path = f"/home/ya/mapdata/flow/{self.process_mount}.yaml"
                if os.path.exists(flow_yaml_path):
                    if not self.is_detect:
                        '''
                        非阻塞运行
                        '''
                        def save_img_detect():
                            self.is_detect = True
                            # 获取图像Base64字符串
                            rgb_frame = get_rgb_frame(sample)
                            if rgb_frame is not None:
                                # 获取图像的长和宽
                                height, width = rgb_frame.shape[:2]

                                # 如果长宽中的一个超过1000，进行缩放
                                if height > 1000 or width > 1000:
                                    # 计算缩放比例
                                    scale_factor = min(1000 / height, 1000 / width)
                                    new_size = (int(width * scale_factor), int(height * scale_factor))
                                    rgb_frame = cv2.resize(rgb_frame, new_size)
                                _, buffer = cv2.imencode('.jpg', rgb_frame)
                                rgb_frame_base64 = base64.b64encode(buffer).decode('utf-8')
                                input_data = {
                                    "image_data": rgb_frame_base64,
                                    "text": "画面中有什么"
                                }
                                # 定义访问的参数
                                flow_back = PrefectRun(flow_yaml_path, input_data)
                                # 遍历并输出每个键和值
                                if self.text_overlay is not None:
                                    self.text_overlay.set_property("text", flow_back["text"])
                                if self.audio_appsrc is not None:
                                    http_url = "http://192.168.0.70:28686/v1/ttsController"
                                    kwargs = {
                                        "text": flow_back["text"]
                                    }
                                    response = requests.post(http_url, data=kwargs)
                                    json_string = response.content.decode('utf-8')
                                    # 将字符串解析为 JSON 对象
                                    json_data = json.loads(json_string)
                                    back = json_data['data']
                                    data = base64.b64decode(back["voice_data"])
                                    buffer = Gst.Buffer.new_allocate(None, len(data), None)
                                    buffer.fill(0, data)
                                    print("正在发送音频")
                                    self.audio_appsrc.emit("push-buffer", buffer)

                            time.sleep(5)
                            self.is_detect = False

                        thread = threading.Thread(target=save_img_detect)
                        thread.start()

                return Gst.FlowReturn.OK
            else:
                print("未获取到样本")
                return Gst.FlowReturn.ERROR
        except Exception as e:
            print(f"处理帧时发生错误: {e}")
            return Gst.FlowReturn.ERROR

    # 开启管道
    def start(self):
        print("启动流程开始")
        self.pipeline = self._create_pipeline()
        self.pipeline.set_state(Gst.State.PLAYING)
        if self.gstreamer_config["gs_input_type"] != "Stream":
            print("启动流程进行中...")
            self.loop_data()
        else:
            print("启动流程进行中...")
            self.loop.run()

    # 根据传入值的类型判断是否循环发送数据
    def loop_data(self):
        # 循环推送图像
        while True:
            if self.gstreamer_config["gs_input_type"] == "Image":
                # 读取图像
                image = cv2.imread(self.gstreamer_config["gs_input_data"])
                # 将图像编码为 PNG
                success, encoded_image = cv2.imencode('.png', image)
                if not success:
                    print("图像编码失败")
                    continue
                # 将编码后的图像转换为字节
                data = encoded_image.tobytes()

                buffer = Gst.Buffer.new_allocate(None, len(data), None)
                buffer.fill(0, data)
                # buffer.pts = Gst.util_uint64_scale(time.time(), Gst.SECOND, 0.9)  # 设置为每秒30帧
                self.appsrc.emit("push-buffer", buffer)
                # print('发送数据')
                # time.sleep(1 / 30)
            if self.gstreamer_config["gs_input_type"] == "Video":
                # 打开视频文件
                cap = cv2.VideoCapture(self.gstreamer_config["gs_input_data"])
                # 检查视频是否成功打开
                if not cap.isOpened():
                    print("无法打开视频文件")
                else:
                    while True:
                        # 读取每一帧
                        ret, frame = cap.read()

                        # 如果成功读取帧
                        if not ret:
                            break

                        # 将每一帧图像编码为 PNG
                        success, encoded_image = cv2.imencode('.png', frame)
                        if not success:
                            print("图像编码失败")
                            continue
                        # 将编码后的图像转换为字节
                        data = encoded_image.tobytes()

                        buffer = Gst.Buffer.new_allocate(None, len(data), None)
                        buffer.fill(0, data)
                        # buffer.pts = Gst.util_uint64_scale(time.time(), Gst.SECOND, 0.9)  # 设置为每秒30帧
                        self.appsrc.emit("push-buffer", buffer)
                        # print('发送数据')
                        time.sleep(1 / 30)
                    # 释放视频捕捉对象
                    cap.release()

    # 停止管道
    def judge_stop(self):
        with open(gstreamer_run_yaml_path, 'r') as file:
            existing_data = yaml.safe_load(file)
            if self.gstreamer_config['id'] not in existing_data:
                if self.pipeline:
                    self.pipeline.set_state(Gst.State.NULL)
                if self.loop:
                    self.loop.quit()
            else:
                gstreamer_info = existing_data[self.gstreamer_config['id']]
                self.process_mount = gstreamer_info['process_mount']
