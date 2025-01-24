from typing import Dict

from app.model.data_item import DaType, DaFormat, DataItem


class DataItemRealData:
    """
    数据类（增加data，区分参数描述和参数真实数据），用于表示输入信息的单个数据块
    """

    def __init__(self, come_type: DaType = DaType.TEXT, come_format: DaFormat = DaFormat.fstring, content: str = None, data = None):
        """
        初始化单个数据块
        """
        self.data_type = come_type.value  # 输入类型
        self.data_format = come_format.value  # 数据格式
        self.content = content  # 输入内容
        self.data = data

    def obj2dct(self) -> Dict:
        """
        将对象转换为字典格式
        :return: 字典形式的数据块
        """
        return {
            "type": self.data_type,
            "format": self.data_format,
            "content": self.content,
            "data": self.data
        }

class ReqParameter:
    """
    prefect调用模型接口时，使用到的参数和过程产生的数据
    """
    def __init__(self, gs_input: [DataItem], gs_output: [DataItem], process_param: [DataItem]):
        self.gs_input = gs_input
        self.gs_output = gs_output
        self.process_param = process_param

        self.gs_input_data = []
        self.gs_output_data = []
        self.process_param_data = []

        for data in self.gs_input:
            self.gs_input_data.append(DataItemRealData(DaType(data.data_type), DaFormat(data.data_format), data.content))
        for data in self.gs_output:
            self.gs_output_data.append(DataItemRealData(DaType(data.data_type), DaFormat(data.data_format), data.content))
        for data in self.process_param:
            self.process_param_data.append(DataItemRealData(DaType(data.data_type), DaFormat(data.data_format), data.content))