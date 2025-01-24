import yaml
from gi.repository import Gst, GLib

from app import config
from app.entity.gstreamer_piepline_config import GstreamerPiePlineConfig
from app.model.model.cbt_model_file import CbtModelFile
from app.model.parsed_bpmn.bpmn_entity import parsed_data_to_entity
from app.model.prefect_run.req_parameter import ReqParameter
from app.service.prefect_service import PrefectRun
from app.untils.bpmn_parser import parse_bpmn_and_params

Gst.init(None)

from app.model.come_entity import ComeEntity
from app.model.context_entity import ContextEntity
from app.model.data_item import DataItem, DaType, DaFormat

import io
import json
import wave

import numpy as np
import requests
import base64


class DealVoicePipeline:
    """
    gstreamer启动，关闭流程
    """

    # GStreamer类初始化
    def __init__(self, ):
        # print(gstreamer_config)
        # self.camera_data = camera_data
        # self.gstreamer_config = gstreamer_config
        # # 设置挂载
        # self.process_mount = gstreamer_config['process_mount']
        # 默认第一个列表
        self.collected_data = bytearray()
        self.target_duration = 5  # 目标时间（秒）
        self.target_bytes = 44100 * 2 * 2 * self.target_duration  # 5 秒的音频数据量（以字节为单位）
        self.start_time = None  # 用于记录开始时间

        # 音频格式参数
        self.sample_rate = 44100  # 采样率 (Hz)
        self.channels = 2  # 声道数
        self.sample_width = 2  # 每个样本的字节数（16-bit）
        self.audio_format = 'h'  # 对应于 16-bit PCM 格式

        self.loop = GLib.MainLoop()
        # 语音输出
        self.audio_appsrc = None
        # 获取gstreamer语句
        self.gstreamer_command = self._create_gs_command()
        print(self.gstreamer_command)

        self.ppp = 0

        self.collected_value = bytearray()

        # # 获取管道的输入和输出
        # gs_piepline_config = self.get_single_gstreamer_pipeline()
        # # 获取bpmn的流程
        #
        #
        # come_data_item = []
        # for data in gs_piepline_config.gs_comes:
        #     come_data_item.append(
        #         DataItem(DaType(str(data["type"])), DaFormat(str(data["format"])), data["content"]))
        #
        # gos_data_item = []
        # for data in gs_piepline_config.gs_gos:
        #     gos_data_item.append(
        #         DataItem(DaType(str(data["type"])), DaFormat(str(data["format"])), data["content"]))
        #
        # self.bpmn_entity = self.get_from_bpmn()
        # self.param_data = ReqParameter(come_data_item, gos_data_item, [])



        self.pipeline = None  # 推迟创建管道的时机，用于进程适配

    def get_single_gstreamer_pipeline(self):
        gs_config_id = "e072466d-74f0-49db-951b-1e8d2453ead9"
        yaml_path = f"/home/ya/mapdata/gstreamer_yaml/cbtai/{gs_config_id}.yaml"
        with open(yaml_path, 'r') as file:
            existing_data = yaml.safe_load(file) or {}
            # 遍历字典
            gs_piepline_config = GstreamerPiePlineConfig()
            gs_piepline_config.id = existing_data["id"]
            gs_piepline_config.gs_name = existing_data["gs_name"]
            if existing_data["output_type"] == "Audio":
                gs_piepline_config.output_type = "声音播放"
            else:
                gs_piepline_config.output_type = "视频流输出"

            gs_piepline_config.input_data = existing_data["input_data"]
            gs_piepline_config.output_data = existing_data["output_data"]
            gs_piepline_config.gs_comes = existing_data["gs_comes"]
            gs_piepline_config.gs_gos = existing_data["gs_gos"]
        return gs_piepline_config

    def get_from_bpmn(self):
        # 默认使用的文件地址
        bpmn_file_path = "/home/ya/mapdata/flow_bpmn/cbtai/Process_1.bpmn"
        # 获取bpmn原始数据
        bpmn_parse_data = parse_bpmn_and_params(bpmn_file_path)
        # 获取bpmn实体类数据
        bpmn_entity = parsed_data_to_entity(bpmn_parse_data)
        # 获取模型接口数据
        model_infos = CbtModelFile().scanModelDir()
        # 遍历用户任务，为每一个任务加上其他需要的参数和访问的路径
        for user_task in bpmn_entity["user_tasks"]:
            model_id = user_task["model_id"]
            interface_id = str(user_task["interface_id"])
            model_interface_need = next(
                (interface for model_info in model_infos if model_info["model_id"] == model_id
                 for interface in model_info["model_interfaces"] if str(interface["id"]) == interface_id),
                None
            )
            if model_interface_need:
                user_task["api_endpoint"] = f'http://{config.host}{model_interface_need["api_endpoint"]}'
                # user_task["parameters"] = model_interface_need["parameters"]
                in_comes = int(model_interface_need["in_comes"])
                req_comes = model_interface_need["req_comes"]
                for idx, req_come in enumerate(req_comes):
                    if idx != in_comes:
                        user_task["up_params_parsed"].append(req_come)
                # 取出第一个元素
                first_element = user_task["up_params_parsed"].pop(0)

                # 插入到指定的位置
                user_task["up_params_parsed"].insert(in_comes, first_element)
            else:
                raise ValueError(f"未找到用户任务 {user_task['task_id']} 的匹配模型接口配置")
        return bpmn_entity

    # 创建GStreamer语句
    def _create_gs_command(self):
        return """
        alsasrc device="hw:1,0" ! audioconvert ! audioresample ! queue ! appsink name=usbaudio drop=false max-buffers=10 \
            appsrc name=audio_appsrc is-live=true format=time do-timestamp=true ! \
            decodebin ! audioconvert ! audioresample ! rtspclientsink location=rtsp://192.168.0.70:8554/voice_stream
        """

    # 创建GStreamer管道
    def _create_pipeline(self):
        pipeline = Gst.parse_launch(self.gstreamer_command)

        self.usbaudioappsink = pipeline.get_by_name(f"usbaudio")
        self.usbaudioappsink.set_property("emit-signals", True)
        self.usbaudioappsink.connect("new-sample", self.audio_process_frame)

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
    def audio_process_frame(self, sink):
        try:
            # 请求视频帧
            sample = sink.emit("pull-sample")
            if sample:
                # 获取缓冲区
                buffer = sample.get_buffer()
                data = buffer.extract_dup(0, buffer.get_size())
                # 如果这是第一次调用回调，记录开始时间
                self.collected_data += data
                # 如果已经收集到足够的数据，停止管道并保存音频文件
                if len(self.collected_data) >= self.target_bytes:
                    print("声音识别中！！！")
                    audio_base64 = self.convert_to_base64(self.collected_data)

                    use_param_data = self.param_data
                    for data in use_param_data.gs_input_data:
                        data.data = audio_base64

                    flow_back = PrefectRun(self.bpmn_entity, use_param_data)

                    voice_data = flow_back.gs_output_data[0].data

                    back = []
                    for data in flow_back.gs_output_data:
                        back.append(data.obj2dct())

                    # # 声音识别
                    # asr_back = self.asr_task(audio_base64)
                    # asr_back = ComeEntity.as_ComeEntity(asr_back)
                    # voice_text = asr_back.comes[0].content
                    # print(f"声音识别结果为：{voice_text}")
                    # # 文字翻译
                    # translate_back = self.text_translation_task(voice_text)
                    # translate_back = ComeEntity.as_ComeEntity(translate_back)
                    # translate_text = translate_back.comes[0].content
                    # print(f"文字翻译结果为：{translate_text}")
                    # # 文字转声音
                    # ll = None
                    # try:
                    #     voice_back = self.tts_task(translate_text)
                    #     voice_back = ComeEntity.as_ComeEntity(voice_back)
                    #     voice_data = voice_back.comes[0].content
                    #
                    #     ll = voice_data
                    # except:
                    #     print("121212")
                    # if ll:
                    #     self.ppp = self.ppp + 1
                    #     self.collected_value += base64.b64decode(ll)
                    #     if self.ppp >= 5 :
                    #         # 播放声音
                    #         data = self.collected_value
                    #         buffer = Gst.Buffer.new_allocate(None, len(data), None)
                    #         buffer.fill(0, data)
                    #         print("正在发送音频")
                    #         self.audio_appsrc.emit("push-buffer", buffer)
                    #         self.ppp = 0
                    #         self.collected_value = bytearray()
                    # self.collected_data = bytearray()
                return Gst.FlowReturn.OK
            else:
                print("未获取到样本")
                return Gst.FlowReturn.ERROR
        except Exception as e:
            print(f"处理声音帧时发生错误: {e}")
            return Gst.FlowReturn.ERROR

    # 声音识别
    def asr_task(self, audio):
        try:
            cheng_schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "come_type": {
                            "type": "string"
                        },
                        "come_format": {
                            "type": "string"
                        },
                        "content": {
                            "type": "string"
                        }
                    },
                    "required": ["come_type", "come_format", "content"],
                    "additionalProperties": False  # 不允许额外的字段
                },
            }
            comes = [
                DataItem(content="bypass"),
                DataItem(DaType.TEXT, DaFormat.fstring, content="http://192.168.0.70:28686/v1/asrController"),
                DataItem(DaType.AUDIO, DaFormat.fbase64, content=audio),
            ]
            comeEntity = ComeEntity().setup(comes=comes, context=ContextEntity())
            # 定义请求的 URL
            url = "http://192.168.0.70:28386/v1/process"  # 替换为目标 URL
            # 定义 JSON 数据
            payload = comeEntity.obj2dct()
            # 发送 POST 请求
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            hao_comeEntity = ComeEntity.as_ComeEntity(response.json())
            return hao_comeEntity.obj2dct()
        except Exception as e:
            print(f"声音识别发生错误: {e}")

    # 文字转声音
    def tts_task(self, text):
        try:
            cheng_schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "come_type": {
                            "type": "string"
                        },
                        "come_format": {
                            "type": "string"
                        },
                        "content": {
                            "type": "string"
                        }
                    },
                    "required": ["come_type", "come_format", "content"],
                    "additionalProperties": False  # 不允许额外的字段
                },
            }
            comes = [
                DataItem(content="bypass"),
                DataItem(DaType.TEXT, DaFormat.fstring, content="http://192.168.0.70:28686/v1/ttsController"),
                DataItem(DaType.TEXT, DaFormat.fstring, content=text),
            ]
            comeEntity = ComeEntity().setup(comes=comes, context=ContextEntity())
            # 定义请求的 URL
            url = "http://192.168.0.70:28386/v1/process"  # 替换为目标 URL
            # 定义 JSON 数据
            payload = comeEntity.obj2dct()
            # 发送 POST 请求
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            hao_comeEntity = ComeEntity.as_ComeEntity(response.json())
            return hao_comeEntity.obj2dct()
        except Exception as e:
            print(f"文字转声音发生错误: {e}")

    # 文字翻译
    def text_translation_task(self, text):
        try:
            cheng_schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "come_type": {
                            "type": "string"
                        },
                        "come_format": {
                            "type": "string"
                        },
                        "content": {
                            "type": "string"
                        }
                    },
                    "required": ["come_type", "come_format", "content"],
                    "additionalProperties": False  # 不允许额外的字段
                },
            }
            comes = [
                DataItem(content="process"),
                DataItem(DaType.APPLICATION, DaFormat.fstring, content=json.dumps(cheng_schema)),
                DataItem(content='把我输入的文字翻译为中文'),
                DataItem(content=text)
            ]
            comeEntity = ComeEntity().setup(comes=comes, context=ContextEntity())
            # 定义请求的 URL
            url = "http://192.168.0.70:28386/v1/process"  # 替换为目标 URL
            # 定义 JSON 数据
            payload = comeEntity.obj2dct()
            # 发送 POST 请求
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            hao_comeEntity = ComeEntity.as_ComeEntity(response.json())
            return hao_comeEntity.obj2dct()
        except Exception as e:
            print(f"文字转声音发生错误: {e}")

    # 开启管道
    def start(self):
        print("启动流程开始")
        self.pipeline = self._create_pipeline()
        self.pipeline.set_state(Gst.State.PLAYING)

        voice_back = self.tts_task("我是一个开始的内容")
        voice_back = ComeEntity.as_ComeEntity(voice_back)
        voice_data = voice_back.comes[0].content

        data = base64.b64decode(voice_data)
        buffer = Gst.Buffer.new_allocate(None, len(data), None)
        buffer.fill(0, data)
        self.audio_appsrc.emit("push-buffer", buffer)
        self.loop.run()

    def calculate_rms(self, data):
        # 将数据转为numpy数组
        np_data = np.frombuffer(data, dtype=np.int16)  # 假设数据是16位的音频数据
        rms = np.sqrt(np.mean(np_data ** 2))  # 计算均方根
        return rms

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