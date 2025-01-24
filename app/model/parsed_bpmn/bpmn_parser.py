import xml.etree.ElementTree as ET


def parse_bpmn(file_path):
    """
    解析 BPMN 文件，提取指定的 startEvent 和 userTask 的属性值。

    :param file_path: BPMN 文件路径
    :return: 字典，包含 startEvent 和 userTask 信息
    """
    # 解析 BPMN 文件
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        namespace = {
            'bpmn2': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
            'magic': 'http://magic',
            'cbtai': 'http://cbtai'
        }

        # Namespace helpers for attributes
        magic_prefix = '{http://magic}'
        cbtai_prefix = '{http://cbtai}'

        # 获取 <bpmn2:startEvent>
        process = root.find('.//bpmn2:process', namespace)
        process_data = None
        if process is not None:
            process_data = process.get(f'id')

        # 获取 <bpmn2:startEvent>
        start_event = root.find('.//bpmn2:startEvent', namespace)
        start_event_data = None
        if start_event is not None:
            pipeline_id = start_event.get(f'{magic_prefix}pipelineId')
            input_params = start_event.get(f'{magic_prefix}inputparams')
            start_event_data = {
                'pipelineId': pipeline_id,
                'inputParams': input_params
            }

        # 获取多个 <bpmn2:userTask>
        user_tasks = root.findall('.//bpmn2:userTask', namespace)
        user_task_data = []
        for user_task in user_tasks:
            model_id = user_task.get(f'{cbtai_prefix}modelId')
            interface_id = user_task.get(f'{cbtai_prefix}interfaceId')
            up_params = user_task.get(f'{cbtai_prefix}upParams')
            down_params = user_task.get(f'{cbtai_prefix}downParams')
            user_task_data.append({
                'modelId': model_id,
                'interfaceId': interface_id,
                'upParams': up_params,
                'downParams': down_params
            })

        # 获取 <bpmn2:endEvent>
        end_event = root.find('.//bpmn2:endEvent', namespace)
        end_event_data = None
        if end_event is not None:
            outputParams = end_event.get(f'{magic_prefix}outputParams')
            end_event_data = {
                'outputParams': outputParams
            }

        return {
            'process': process_data,
            'startEvent': start_event_data,
            'userTasks': user_task_data,
            'endEvent': end_event_data
        }

    except Exception as e:
        print(f"解析 BPMN 文件出错: {e}")
        return None

def parse_params(param_str):
    """
    将参数字符串解析为列表格式。

    :param param_str: 参数字符串，例如 "text→fstring→提问大模型的问题✓image→fbase64→视频流的帧图像数据"
    :return: 列表，每个元素是一个字典，表示 type, format, content
    """
    if not param_str:  # 如果传入为空
        return []

    params_list = []
    try:
        # 分解多项参数，使用"✓"作为分隔符
        param_items = param_str.split('✓')
        for item in param_items:
            # 分解单项参数，使用"→"作为分隔符
            parts = item.split('→')
            if len(parts) == 3:  # 确保格式正确
                param_type, param_format, param_content = parts
                params_list.append({
                    "type": param_type,
                    "format": param_format,
                    "content": param_content
                })
    except Exception as e:
        print(f"解析参数失败: {e}")

    return params_list


# 整合到 BPMN 数据解析中
def parse_bpmn_and_params(file_path):
    """
    解析 BPMN 文件，同时将 inputParams、upParams 和 downParams 转换成标准列表格式。

    :param file_path: BPMN 文件路径
    :return: 整合后的字典结果
    """
    bpmn_data = parse_bpmn(file_path)  # 调用前面定义的 BPMN 解析方法
    if not bpmn_data:
        return None

    # 解析 startEvent 的 inputParams
    if bpmn_data['startEvent'] and bpmn_data['startEvent']['inputParams']:
        bpmn_data['startEvent']['inputParamsParsed'] = parse_params(bpmn_data['startEvent']['inputParams'])

    # 解析 userTask 的 upParams 和 downParams
    for task in bpmn_data['userTasks']:
        if 'upParams' in task and task['upParams']:
            task['upParamsParsed'] = parse_params(task['upParams'])
        if 'downParams' in task and task['downParams']:
            task['downParamsParsed'] = parse_params(task['downParams'])

    # 解析 endEvent 的 outputParams
    if bpmn_data['endEvent'] and bpmn_data['endEvent']['outputParams']:
        bpmn_data['endEvent']['outputParamsParsed'] = parse_params(bpmn_data['endEvent']['outputParams'])

    return bpmn_data
