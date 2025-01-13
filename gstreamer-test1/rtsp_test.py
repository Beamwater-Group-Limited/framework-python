from gi.repository import Gst, GLib
Gst.init(None)
import base64
import json
import time

import requests
class GstreamerPiePline:
    """
    gstreamer启动，关闭流程
    """

    def __init__(self, gstreamer_config):
        print(gstreamer_config)
        self.gstreamer_config = gstreamer_config
        # 设置编码
        self.encode = gstreamer_config['encode']
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

        # 定义gstreamer命令
        self.gstreamer_command = f'''
            rtspsrc location={self.gstreamer_config['rtsp_url']} latency=0 ! \
            {'rtph264depay' if self.encode == 'H264' else 'rtph265depay'} ! \
            {'avdec_h264' if self.encode == 'H264' else 'avdec_h265'} ! \
            videoconvert ! \
            tee name=t ! \
            queue ! \
            textoverlay name=overlay text="初始文本" valignment=top halignment=left ! \
            x264enc tune=zerolatency speed-preset=ultrafast bitrate=3000 key-int-max=60 bframes=0 ! \
            queue ! mux. \
            appsrc name=audio_appsrc is-live=true format=time do-timestamp=true ! \
            decodebin ! audioconvert ! avenc_aac ! queue ! mux.
            mpegtsmux name=mux ! \
            rtspclientsink location={self.gstreamer_config['ts_url']} \
            t. ! queue ! appsink name=mysink drop=false max-buffers=10'''


        # filesrc name=video_mix location=/0output_test.wav ! decodebin ! audioconvert ! avenc_aac ! queue ! mux. \

        print(self.gstreamer_command)

        self.pipeline = None  # 推迟创建管道的时机，用于进程适配

    def _create_pipeline(self):
        pipeline = Gst.parse_launch(self.gstreamer_command)
        self.text_overlay = pipeline.get_by_name("overlay")
        self.audio_appsrc = pipeline.get_by_name("audio_appsrc")
        caps = Gst.Caps.from_string(
            "audio/x-raw, format=S16LE, rate=44100, channels=1, layout=interleaved")
        self.audio_appsrc.set_property("format", Gst.Format.TIME)
        self.audio_appsrc.set_property("is-live", True)
        self.audio_appsrc.set_property("do-timestamp", True)
        self.audio_appsrc.set_property("emit-signals", True)
        self.audio_appsrc.set_property("caps", caps)


        appsink = pipeline.get_by_name(f"mysink")
        appsink.set_property("emit-signals", True)
        appsink.connect("new-sample", self.process_frame)
        # self.video_mix.set_property("location", "/sample-15s.wav")
        return pipeline

    # 回调函数处理
    # 调用prefect流，调用相关的函数
    def process_frame(self, sink):
        try:
            sample = sink.emit("pull-sample")
            if sample:
                buf = sample.get_buffer()
                data = buf.extract_dup(0, buf.get_size())
                print("回调正在运行")
                # print(self.video_mix)
                # print(self.text_overlay)
                # if not self.is_update:
                #     try:
                #         self.video_mix.set_property("location", "/sample-15s.wav")
                #         # self.is_update = True
                #     except Exception as e:
                #         print("不给修改，文件打开了")

                if self.text_overlay is not None:
                    self.text_overlay.set_property("text", str("123"))

                return Gst.FlowReturn.OK
            else:
                print("未获取到样本")
                return Gst.FlowReturn.ERROR
        except Exception as e:
            print(f"处理帧时发生错误: {e}")
            return Gst.FlowReturn.ERROR

    # 推送音频
    def send_audio(self):
        while True:
            http_url = "http://192.168.0.70:28686/v1/ttsController"
            kwargs = {
                "text": "你知道我是谁吗，我们都是程序员"
            }
            response = requests.post(http_url, data=kwargs)
            json_string = response.content.decode('utf-8')
            # 将字符串解析为 JSON 对象
            json_data = json.loads(json_string)
            back = json_data['data']
            print(back["voice_data"])
            data = base64.b64decode(back["voice_data"])
            buffer = Gst.Buffer.new_allocate(None, len(data), None)
            buffer.fill(0, data)
            print("正在发送音频")
            self.audio_appsrc.emit("push-buffer", buffer)
            time.sleep(5)

            # file_path = "/0output_test.wav"
            # with open(file_path, 'rb') as f:
            #     data = f.read()
            #     buffer = Gst.Buffer.new_allocate(None, len(data), None)
            #
            #     buffer.fill(0, data)
            #     print("正在发送音频")
            #     self.audio_appsrc.emit("push-buffer", buffer)
            #     time.sleep(1)

    def start(self):
        print("启动流程开始")
        self.pipeline = self._create_pipeline()
        self.pipeline.set_state(Gst.State.PLAYING)
        print("启动流程进行中...")
        self.send_audio()
        # thread = threading.Thread(target=self.send_audio)
        # thread.start()
        # self.loop.run()

    def judge_stop(self):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
        if self.loop:
            self.loop.quit()

gstreamer_config = {'camera_name': '测试源', 'rtsp_url': 'rtsp://admin:yuanm201109@192.168.0.112:554/cam/realmonitor?channel=1', 'encode': 'H264', 'ts_url': 'rtsp://192.168.0.70:8554/yuan', 'process_mount': 'e01261f0-72f3-4ff8-a812-e7327bd75a69', 'is_work': '', 'gstreamer_instance': ''}
pp = GstreamerPiePline(gstreamer_config)
pp.start()