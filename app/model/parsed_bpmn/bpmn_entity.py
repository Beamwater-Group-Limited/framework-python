from typing import Dict


class StartEvent:
    def __init__(self, pipeline_id, input_params, input_params_parsed=None):
        self.pipeline_id = pipeline_id
        self.input_params = input_params
        self.input_params_parsed = input_params_parsed

    def to_dict(self):
        return {
            'pipeline_id': self.pipeline_id,
            'input_params': self.input_params,
            'input_params_parsed': self.input_params_parsed
        }


class EndEvent:
    def __init__(self, output_params, output_params_parsed=None):
        self.output_params = output_params
        self.output_params_parsed = output_params_parsed

    def to_dict(self):
        return {
            'output_params': self.output_params,
            'output_params_parsed': self.output_params_parsed
        }


class UserTask:
    def __init__(self, model_id, interface_id, up_params, down_params, up_params_parsed=None, down_params_parsed=None):
        self.model_id = model_id
        self.interface_id = interface_id
        self.up_params = up_params
        self.down_params = down_params
        self.up_params_parsed = up_params_parsed
        self.down_params_parsed = down_params_parsed

    def to_dict(self):
        return {
            'model_id': self.model_id,
            'interface_id': self.interface_id,
            'up_params': self.up_params,
            'down_params': self.down_params,
            'up_params_parsed': self.up_params_parsed,
            'down_params_parsed': self.down_params_parsed
        }


class BPMNData:
    def __init__(self, start_event, user_tasks, end_event, process):
        self.process = process
        self.start_event = start_event
        self.user_tasks = user_tasks
        self.end_event = end_event

    def to_dict(self):
        return {
            'process': self.process,
            'start_event': self.start_event.to_dict() if self.start_event else None,
            'user_tasks': [task.to_dict() for task in self.user_tasks],
            'end_event': self.end_event.to_dict() if self.end_event else None,
        }


def parsed_data_to_entity(parsed_data):
    """
    将解析后的数据转换为实体类实例

    :param parsed_data: 解析后的 BPMN 数据（字典形式）
    :return: BPMNData 实例
    """
    # 构造 Process 实例
    process_data = parsed_data.get('process', "")

    # 构造 StartEvent 实例
    start_event_data = parsed_data.get('startEvent', {})
    start_event = StartEvent(
        pipeline_id=start_event_data.get('pipelineId'),
        input_params=start_event_data.get('inputParams'),
        input_params_parsed=start_event_data.get('inputParamsParsed')
    )

    # 构造 UserTask 实例列表
    user_tasks = []
    for task_data in parsed_data.get('userTasks', []):
        user_task = UserTask(
            model_id=task_data.get('modelId'),
            interface_id=task_data.get('interfaceId'),
            up_params=task_data.get('upParams'),
            down_params=task_data.get('downParams'),
            up_params_parsed=task_data.get('upParamsParsed'),
            down_params_parsed=task_data.get('downParamsParsed')
        )
        user_tasks.append(user_task)

    end_event_data = parsed_data.get('endEvent', {})
    end_event = EndEvent(
        output_params=end_event_data.get('outputParams'),
        output_params_parsed=end_event_data.get('outputParamsParsed')
    )

    # 返回 BPMNData 实例
    return BPMNData(start_event=start_event, user_tasks=user_tasks, end_event=end_event, process=process_data).to_dict()
