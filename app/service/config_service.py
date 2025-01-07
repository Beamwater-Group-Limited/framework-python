import logging
import os
import shutil

import yaml
from app import config

logger = logging.getLogger(config.app_name)


class ConfigService:
    # 将摄像头信息添加到yaml配置文件中
    def add_input_camera_data(self, yaml_path, camera_id, camera):
        # 如果文件不存在，先创建文件
        if not os.path.exists(yaml_path):
            with open(yaml_path, 'w', encoding="utf-8") as file:
                # 将数据写入新文件
                yaml.dump({camera_id: camera}, file)
        else:
            # 如果文件已存在，读取文件中的内容
            with open(yaml_path, 'r') as file:
                existing_data = yaml.safe_load(file)

            # 将新数据添加到现有数据中
            existing_data[camera_id] = camera

            print(existing_data)
            with open(yaml_path, 'w', encoding="utf-8") as file:
                # 将数据写入新文件
                yaml.dump(existing_data, file)

        return 'success'

    # 修改摄像头数据
    def update_input_camera_data(self, yaml_path, camera_id, camera):
        # 如果文件已存在，读取文件中的内容
        with open(yaml_path, 'r') as file:
            existing_data = yaml.safe_load(file)

        # 将新数据添加到现有数据中
        existing_data[camera_id] = camera

        print(existing_data)
        with open(yaml_path, 'w', encoding="utf-8") as file:
            # 将数据写入新文件
            yaml.dump(existing_data, file)

        return 'success'

    # 删除摄像头数据
    def del_input_camera_data(self, yaml_path, camera_id):
        # 如果文件已存在，读取文件中的内容
        with open(yaml_path, 'r') as file:
            existing_data = yaml.safe_load(file)

        # 将新数据添加到现有数据中
        del existing_data[camera_id]

        print(existing_data)
        with open(yaml_path, 'w', encoding="utf-8") as file:
            # 将数据写入新文件
            yaml.dump(existing_data, file)

        return 'success'

    # 根据id返回摄像头数据
    def get_camera_data_with_id(self, yaml_path, camera_id):
        # 如果文件已存在，读取文件中的内容
        with open(yaml_path, 'r') as file:
            existing_data = yaml.safe_load(file)

        existing_data[camera_id]["id"] = camera_id
        return existing_data[camera_id]
