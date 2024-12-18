class OutputData:

    def __init__(self):
        self.text = None
        self.image_list = None
        self.stream = None
        self.voice = None

    def to_dict(self):
        # 将对象转换为字典，便于保存到 YAML 文件
        return {
            'text': self.text,
            'image_list': self.image_list,
            'stream': self.stream,
            'voice': self.voice
        }
