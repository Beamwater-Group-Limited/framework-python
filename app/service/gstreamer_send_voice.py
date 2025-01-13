import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GLib

import requests
import json
import base64

Gst.init(None)

def on_message(bus, message, loop):
    """
    回调函数：监听 EOS & ERROR
    """
    if message.type == Gst.MessageType.EOS:
        print("GStreamer: End-of-stream")
        # 收到 EOS 后，退出循环
        loop.quit()
    elif message.type == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"GStreamer: Error {err}, debug: {debug}")
        loop.quit()

def play_once(text):
    gstreamer_command = f'''
        appsrc name=audio_appsrc is-live=true format=time do-timestamp=true !
        decodebin ! audioconvert ! audioresample ! autoaudiosink
    '''
    print("Gstreamer pipeline:", gstreamer_command)

    # 解析 pipeline
    pipeline = Gst.parse_launch(gstreamer_command)

    # 获取 appsrc
    audio_appsrc = pipeline.get_by_name("audio_appsrc")
    caps = Gst.Caps.from_string(
        "audio/x-raw, format=S16LE, rate=44100, channels=1, layout=interleaved"
    )
    audio_appsrc.set_property("format", Gst.Format.TIME)
    audio_appsrc.set_property("is-live", True)
    audio_appsrc.set_property("do-timestamp", True)
    audio_appsrc.set_property("emit-signals", True)
    audio_appsrc.set_property("caps", caps)

    # 从 TTS 接口获取语音数据
    http_url = "http://192.168.0.70:28686/v1/ttsController"
    kwargs = {
        "text": str(text)
    }
    response = requests.post(http_url, data=kwargs)
    json_string = response.content.decode('utf-8')
    json_data = json.loads(json_string)
    back = json_data['data']
    data = base64.b64decode(back["voice_data"])

    # 创建并填充 Gst.Buffer
    buffer = Gst.Buffer.new_allocate(None, len(data), None)
    buffer.fill(0, data)

    # 设置 pipeline 为 PLAYING
    pipeline.set_state(Gst.State.PLAYING)

    # 往 appsrc 推数据
    print("正在发送音频...")
    audio_appsrc.emit("push-buffer", buffer)
    # 发送 end-of-stream，让 pipeline 只播放一次
    audio_appsrc.emit("end-of-stream")

    # 启动 MainLoop，用于异步地等待 EOS
    loop = GLib.MainLoop()

    # 监听 pipeline bus 消息
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message, loop)

    # 进入事件循环，等待 EOS 或 ERROR
    loop.run()

    # 收到 EOS 或 ERROR 后，退出循环，停止并释放 pipeline
    pipeline.set_state(Gst.State.NULL)
    print("播放结束，已停止。")
