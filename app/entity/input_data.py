class InputData:

    def __init__(self):
        self.text = None
        self.image_data = None
        self.voice_data = None
        self.file_data = None
        self.stream = None

    # def to_dict(self):
    #     # 将对象转换为字典，便于保存到 YAML 文件
    #     return {
    #         'img_name': self.img_name,
    #         'img_path': self.img_path,
    #         'img_folder': self.img_folder,
    #         'img_tile_path': self.img_tile_path,
    #         'camera_tag': self.camera_tag,
    #         'img_width': self.img_width,
    #         'img_height': self.img_height,
    #         'is_work': self.is_work
    #     }
