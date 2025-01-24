import yaml

def create_test_yaml():
    """
    创建用于执行流程的yaml文件
    """
    # 开始
    start_event = {
        "pipeline_id": "cbtai/6d7904c7-564c-4864-910e-725d359cb49d",
        "pipeline_author": "cbtai",
        "pipeline_name": "6d7904c7-564c-4864-910e-725d359cb49d",
        "pipeline_comes": [
            {
                "type": "text",
                "format": "fstring",
                "content": "提问大模型的问题"
            },
            {
                "type": "image",
                "format": "fbase64",
                "content": "视频流的帧图像数据"
            }
        ]
    }

    # 调用的任务列表
    task_event = [
        {
            "task_id": "xxxxxxxx",
            "task_url": "http://192.168.0.70:28386/v1/process",
            "task_parameters":{
                "model_id": "xxxxx",
                "comes": [
                    {
                        "type": "text",
                        "format": "fstring",
                        "content": "process"
                    },
                    {
                        "type": "application",
                        "format": "fstring",
                        "content": '{"$schema": "http://json-schema.org/draft-07/schema#", "type": "array", "items": {"type": "object", "properties": {"come_type": {"type": "string"}, "come_format": {"type": "string"}, "content": {"type": "string"}}, "required": ["come_type", "come_format", "content"], "additionalProperties": false}}'
                    },
                    {
                        "type": "text",
                        "format": "fstring",
                        "content": "关于图片的问题的回答字数不要超过 10个字"
                    },
                    {
                        "type": "text",
                        "format": "fstring",
                        "content": "描述一下图片的内容"
                    },
                    {
                        "type": "image",
                        "format": "fbase64",
                        "content": "视频流的帧图像数据"
                    }
                ]
            }
        }
    ]
    # 结束
    yaml_content = {
        "start_event": start_event,
        "task_event": task_event,
        "end_event": {}
    }
    yaml_file_path = "/home/ya/mapdata/flow_yaml/cbtai/bpmn_to_yaml_test.yaml"

    with open(yaml_file_path, 'w', encoding="utf-8") as file:
        # 使用 allow_unicode=True 保证中文能正常写入，并且默认会按照插入顺序保存
        yaml.dump(yaml_content, file, allow_unicode=True, default_flow_style=False)
    print("yaml文件保存成功")

    # 如果文件已存在，读取文件中的内容
    with open(yaml_file_path, 'r') as file:
        existing_data = yaml.safe_load(file)
        print(existing_data)
create_test_yaml()