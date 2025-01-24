import threading
import time

from gi.repository import Gst, GLib

Gst.init(None)
loop = GLib.MainLoop()  # 创建和管理主循环
import base64
import io
import json
import os
import wave

import cv2
import numpy as np
import requests

gstreamer_command = """
alsasrc device="hw:1,0" ! audioconvert ! audioresample ! tee name=t1
t1. ! queue ! appsink name=usbaudio drop=false max-buffers=10 \
rtspsrc location=rtsp://192.168.0.70:8554/mainstream latency=0 ! \
rtph264depay ! \
avdec_h264 ! \
videoconvert ! \
tee name=t ! \
queue ! \
appsink name=mysink drop=false max-buffers=10 
appsrc name=audio_appsrc is-live=true format=time do-timestamp=true ! \
decodebin ! audioconvert ! audioresample ! alsasink device="hw:1,0"
"""


class GstreamerPiePline:
    """
    gstreamer启动，关闭流程
    """

    # GStreamer类初始化
    def __init__(self):
        # 默认第一个列表
        self.loop = GLib.MainLoop()
        self.pipeline = None  # 推迟创建管道的时机，用于进程适配
        self.collected_data = bytearray()
        self.target_duration = 5  # 目标时间（秒）
        self.target_bytes = 44100 * 2 * 2 * self.target_duration  # 5 秒的音频数据量（以字节为单位）
        self.start_time = None  # 用于记录开始时间

        # 音频格式参数
        self.sample_rate = 44100  # 采样率 (Hz)
        self.channels = 2  # 声道数
        self.sample_width = 2  # 每个样本的字节数（16-bit）
        self.audio_format = 'h'  # 对应于 16-bit PCM 格式

        # 是否开始记录
        self.is_recording = False
        self.duration_time = 0

        self.is_recording_duration_time = 0
        self.is_restart_duration_time = 0

        self.ask_question = ""

        self.is_during_ask_question = False

        self.is_detect = False

        # 获取gstreamer语句
        self.gstreamer_command = """
            alsasrc device="hw:1,0" ! audioconvert ! audioresample ! tee name=t1
            t1. ! queue ! appsink name=usbaudio drop=false max-buffers=10 \
            rtspsrc location=rtsp://192.168.0.70:8554/mainstream latency=0 ! \
            rtph264depay ! \
            avdec_h264 ! \
            videoconvert ! \
            tee name=t ! \
            queue ! \
            appsink name=mysink drop=false max-buffers=10 
            appsrc name=audio_appsrc is-live=true format=time do-timestamp=true ! \
            decodebin ! audioconvert ! audioresample ! alsasink device="hw:1,0"
        """

        """
        alsasrc device="hw:1,0" ! audioconvert ! audioresample ! alsasink device="hw:1,0"
        
        alsasrc device="hw:1,0" ! audioconvert ! audioresample ! rtspclientsink location=rtsp://192.168.0.70:8554/stream
        
        
        """

    # 创建GStreamer管道
    def _create_pipeline(self):
        self.pipeline = Gst.parse_launch(gstreamer_command)

        self.usbaudioappsink = self.pipeline.get_by_name(f"usbaudio")
        self.usbaudioappsink.set_property("emit-signals", True)
        self.usbaudioappsink.connect("new-sample", self.audio_process_frame)

        self.appsink = self.pipeline.get_by_name(f"mysink")
        self.appsink.set_property("emit-signals", True)
        self.appsink.connect("new-sample", self.process_frame)

        # 设置时间
        self.audio_appsrc = self.pipeline.get_by_name("audio_appsrc")
        caps = Gst.Caps.from_string(
            "audio/x-raw, format=S16LE, rate=44100, channels=1, layout=interleaved")
        self.audio_appsrc.set_property("format", Gst.Format.TIME)
        self.audio_appsrc.set_property("is-live", True)
        self.audio_appsrc.set_property("do-timestamp", True)
        self.audio_appsrc.set_property("emit-signals", True)
        self.audio_appsrc.set_property("caps", caps)
        # 获取 appsrc 元素
        self.appsrc = self.pipeline.get_by_name("source")

        return self.pipeline

    # 开启管道
    def start(self):
        print("启动流程开始")
        self.pipeline = self._create_pipeline()
        self.pipeline.set_state(Gst.State.PLAYING)
        http_url = "http://192.168.0.70:28686/v1/ttsController"
        kwargs = {
            "text": "我现在是开始的状态"
        }
        response = requests.post(http_url, data=kwargs)
        json_string = response.content.decode('utf-8')
        # 将字符串解析为 JSON 对象
        json_data = json.loads(json_string)
        back = json_data['data']
        data = base64.b64decode(back["voice_data"])
        buffer = Gst.Buffer.new_allocate(None, len(data), None)
        buffer.fill(0, data)
        print("正在发送音频111111111111")
        self.audio_appsrc.emit("push-buffer", buffer)
        self.loop.run()


    def calculate_rms(self, data):
        # 将数据转为numpy数组
        np_data = np.frombuffer(data, dtype=np.int16)  # 假设数据是16位的音频数据
        rms = np.sqrt(np.mean(np_data ** 2))  # 计算均方根
        return rms


    # 回调函数处理
    def audio_process_frame(self, sink):
        try:
            # 请求视频帧
            sample = sink.emit("pull-sample")
            if sample:
                # 获取缓冲区
                buffer = sample.get_buffer()
                # 处理音频数据
                # 获取音频数据的大小和内容
                data = buffer.extract_dup(0, buffer.get_size())
                rms = self.calculate_rms(data)

                if self.is_during_ask_question:
                    # 如果这是第一次调用回调，记录开始时间
                    if self.start_time is None:
                        self.start_time = time.time()
                    self.collected_data += data
                    # 计算已收集的时长
                    elapsed_time = time.time() - self.start_time
                    print(f"Elapsed time: {elapsed_time:.2f} seconds, Collected data size: {len(self.collected_data)} bytes")

                    # 如果已经收集到足够的数据，停止管道并保存音频文件
                    if len(self.collected_data) >= self.target_bytes:
                        print("Collected 5 seconds of audio data")
                        kwargs = {
                            "audio": self.convert_to_base64(self.collected_data)
                        }
                        response = requests.post("http://192.168.0.70:28686/v1/asrController", data=kwargs)
                        json_string = response.content.decode('utf-8')
                        # 将字符串解析为 JSON 对象
                        json_data = json.loads(json_string)
                        print(json_data["data"]["response"])
                        self.is_during_ask_question = False
                        self.collected_data = bytearray()
                        self.ask_question = json_data["data"]["response"]
                else:
                    if self.is_recording:
                        if rms > 70:
                            self.collected_data += data
                            print("记录中。。。。。。")
                        else:
                            if self.duration_time < 50:
                                self.duration_time = self.duration_time + 1
                                self.collected_data += data
                                print("记录中。。。。。。")
                            else:
                                self.collected_data += data
                                kwargs = {
                                    "audio": self.convert_to_base64(self.collected_data)
                                }
                                response = requests.post("http://192.168.0.70:28686/v1/asrController", data=kwargs)
                                json_string = response.content.decode('utf-8')
                                # 将字符串解析为 JSON 对象
                                json_data = json.loads(json_string)
                                print(json_data["data"]["response"])

                                if "值班" in str(json_data["data"]["response"]):
                                    if self.ask_question != "":
                                        self.ask_question = ""
                                        http_url = "http://192.168.0.70:28686/v1/ttsController"
                                        kwargs = {
                                            "text": "正在停止上一个问题"
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
                                        self.is_during_ask_question = True
                                        self.collected_data = bytearray()
                                        time.sleep(4)
                                    # print(f'翻译信息是   {json_data["data"]["response"]}')
                                    http_url = "http://192.168.0.70:28686/v1/ttsController"
                                    kwargs = {
                                        "text": "请说"
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
                                    self.is_during_ask_question = True
                                    self.collected_data = bytearray()

                                self.collected_data = bytearray()
                                # pipeline.set_state(Gst.State.NULL)  # 停止管道
                                self.is_recording = False
                                self.start_time = None
                                self.duration_time = 0
                                print("记录结束")
                    else:
                        if rms > 70:
                            if self.is_recording_duration_time >= 3:
                                print("开始记录")
                                self.is_recording = True
                                self.collected_data += data
                            else:
                                print("开始待记录")
                                self.is_recording_duration_time = self.is_recording_duration_time + 1
                                self.collected_data += data
                        else:
                            if self.is_recording_duration_time != 0:
                                if self.is_restart_duration_time > 40:
                                    self.is_recording_duration_time = 0
                                    self.collected_data = bytearray()
                                    self.is_restart_duration_time = 0
                                    print("取消记录")
                                else:
                                    self.is_restart_duration_time = self.is_restart_duration_time + 1
                                    self.collected_data += data

                return Gst.FlowReturn.OK
            else:
                print("未获取到样本")
                return Gst.FlowReturn.ERROR
        except Exception as e:
            print(f"处理声音帧时发生错误: {e}")
            return Gst.FlowReturn.ERROR


    """
    将gstreamer获取的sample转化为rgb图像
    """
    def get_rgb_frame(self, sample):
        # 将数据转换为 NumPy 数组
        buf = sample.get_buffer()
        data = buf.extract_dup(0, buf.get_size())
        height = sample.get_caps().get_structure(0).get_value("height")
        width = sample.get_caps().get_structure(0).get_value("width")
        format = sample.get_caps().get_structure(0).get_value("format")

        print("------------------------------------")
        print(f"图像格式为： {format}")
        print("------------------------------------")

        if format == "I420":  # YUV I420
            y_size = width * height
            u_size = (width // 2) * (height // 2)
            v_size = (width // 2) * (height // 2)

            y_plane = data[0:y_size]
            u_plane = data[y_size:y_size + u_size]
            v_plane = data[y_size + u_size:y_size + u_size + v_size]

            y = np.frombuffer(y_plane, np.uint8).reshape((height, width))
            u = np.frombuffer(u_plane, np.uint8).reshape((height // 2, width // 2))
            v = np.frombuffer(v_plane, np.uint8).reshape((height // 2, width // 2))

            # 上采样 U 和 V
            u_upsampled = cv2.resize(u, (width, height), interpolation=cv2.INTER_LINEAR)
            v_upsampled = cv2.resize(v, (width, height), interpolation=cv2.INTER_LINEAR)

            # 注意通道顺序：可能需要交换 U 和 V
            yuv = cv2.merge([y, v_upsampled, u_upsampled])  # 交换 U 和 V
            rgb_image = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB)

        elif format == "BGR":  # BGR 格式
            rgb_image = cv2.cvtColor(np.frombuffer(data, np.uint8).reshape((height, width, 3)),
                                     cv2.COLOR_BGR2RGB)

        elif format == "RGB":  # RGB 格式
            rgb_image = np.frombuffer(data, np.uint8).reshape((height, width, 3))

        elif format == "Y444":
            y_size = width * height
            u_size = width * height
            v_size = width * height

            # 提取 Y、U 和 V 分量
            y_plane = data[0:y_size]
            u_plane = data[y_size:y_size + u_size]
            v_plane = data[y_size + u_size:y_size + u_size + v_size]

            # 将 Y、U 和 V 数据转换为 NumPy 数组
            y = np.frombuffer(y_plane, np.uint8).reshape((height, width))
            u = np.frombuffer(u_plane, np.uint8).reshape((height, width))
            v = np.frombuffer(v_plane, np.uint8).reshape((height, width))

            # 将 YUV 转换为 RGB
            rgb_image = cv2.cvtColor(cv2.merge([y, u, v]), cv2.COLOR_YUV2RGB)

        else:
            rgb_image = None

        return rgb_image


    # 回调函数处理
    # 调用prefect流，调用相关的函数
    def process_frame(self, sink):
        # 调用一次判断，是否停止
        try:
            sample = sink.emit("pull-sample")
            if sample:
                buf = sample.get_buffer()
                data = buf.extract_dup(0, buf.get_size())

                '''
                非阻塞运行
                '''
                if self.ask_question != "":
                    if not self.is_detect:
                        print("进入到图像回调了")
                        def save_img_detect():
                            self.is_detect = True
                            if self.ask_question != "":
                                # 获取图像Base64字符串
                                rgb_frame = self.get_rgb_frame(sample)
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
                                        "model_id": "/home/ya/mapdata/safe/results/unsloth/llava-ov-7b-people-1208",
                                        "image_data": rgb_frame_base64,
                                        "text": self.ask_question
                                    }

                                    response = requests.post("http://192.168.0.70:28486/v1/inferenceController",
                                                             data=input_data)
                                    json_string = response.content.decode('utf-8')
                                    # 将字符串解析为 JSON 对象
                                    json_data = json.loads(json_string)
                                    back = json_data['data']
                                    http_url = "http://192.168.0.70:28686/v1/ttsController"
                                    kwargs = {
                                        "text": back["text"]
                                    }
                                    print(f"识别结果为： {back['text']}")
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
                                    time.sleep(15)
                                    self.is_detect = False

                        thread = threading.Thread(target=save_img_detect)
                        thread.start()

                return Gst.FlowReturn.OK
            else:
                print("未获取到样本")
                return Gst.FlowReturn.ERROR
        except Exception as e:
            print(f"处理视频帧时发生错误: {e}")
            return Gst.FlowReturn.ERROR


    def convert_to_base64(self, collected_data):
        # 创建一个内存中的字节流
        audio_data = np.frombuffer(collected_data, dtype=np.int16)
        with io.BytesIO() as wav_io:
            # 创建一个 WAV 文件对象
            with wave.open(wav_io, 'wb') as wf:
                wf.setnchannels(self.channels)  # 设置声道数
                wf.setsampwidth(self.sample_width)  # 设置样本宽度（通常为 2 或 4 字节）
                wf.setframerate(self.sample_rate)  # 设置采样率
                wf.writeframes(audio_data.tobytes())  # 写入音频数据

            # 获取 WAV 文件的字节流
            wav_bytes = wav_io.getvalue()

        # 将字节流编码为 Base64 字符串
        base64_audio = base64.b64encode(wav_bytes).decode('utf-8')

        return base64_audio

yun = GstreamerPiePline()
yun.start()
