
from gi.repository import Gst, GObject, GLib
Gst.init(None)
import os
import yaml
gstreamer_run_yaml_path = "/home/ya/mapdata/gstreamer_run.yaml"

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

        # 定义gstreamer命令
        self.gstreamer_command = f'''
            rtspsrc location={self.gstreamer_config['rtsp_url']} latency=0 ! \
            {'rtph264depay' if self.encode == 'H264' else 'rtph265depay'} ! \
            {'avdec_h264' if self.encode == 'H264' else 'avdec_h265'} ! \
            videoconvert ! \
            tee name=t ! \
            queue ! \
            x264enc tune=zerolatency speed-preset=ultrafast bitrate=3000 key-int-max=60 bframes=0 ! \
            rtspclientsink location={self.gstreamer_config['ts_url']} \
            t. ! queue ! appsink name=mysink drop=false max-buffers=10'''
        print(self.gstreamer_command)

        self.pipeline = None  # 推迟创建管道的时机，用于进程适配

    def _create_pipeline(self):
        pipeline = Gst.parse_launch(self.gstreamer_command)
        appsink = pipeline.get_by_name(f"mysink")
        appsink.set_property("emit-signals", True)
        appsink.connect("new-sample", self.process_frame)
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

                if (self.process_mount is None) or (self.process_mount == "") or (
                        not os.path.exists(self.process_mount)):
                    print("当前的流没有挂载")

                return Gst.FlowReturn.OK
            else:
                print("未获取到样本")
                return Gst.FlowReturn.ERROR
        except Exception as e:
            print(f"处理帧时发生错误: {e}")
            return Gst.FlowReturn.ERROR

    def start(self):
        print("启动流程开始")
        self.pipeline = self._create_pipeline()
        self.pipeline.set_state(Gst.State.PLAYING)
        print("启动流程进行中...")
        self.loop.run()

    def judge_stop(self):
        with open(gstreamer_run_yaml_path, 'r') as file:
            existing_data = yaml.safe_load(file)
            if self.gstreamer_config['id'] not in existing_data:
                if self.pipeline:
                    self.pipeline.set_state(Gst.State.NULL)
                if self.loop:
                    self.loop.quit()
