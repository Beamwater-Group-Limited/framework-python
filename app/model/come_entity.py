# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : tg
# @File          : come_entity.py
# @Author        : henryren
# @Time          : 2024/12/21 10:00
# @Function      : Define a class to handle input parameter storage and transformation.
# @Desc          : This class represents the detailed input parameters for tasks, including metadata and context.
import uuid
from datetime import datetime
from typing import Dict

from app.model.context_entity import ContextEntity
from app.model.data_item import DataItem

# 主要的开发任务就是撰写和调试系统提示词，然后使用数据集来进行验证
system_promt = """你是一个模拟 RESTful 风格 API 的服务端。当用户发送请求时，你需要根据请求内容生成相应的回复，并将其包装成符合 RESTful API 规范的 JSON 格式。所有的回复必须严格遵循以下格式，不能包含任何其他形式的内容。

### 成功响应格式：
{
  "respon_status": "success",
  "data": {
    // 根据具体请求返回的数据内容
  }
}

### 错误响应格式：
{
  "respon_status": "error",
  "message": "错误描述信息"
}

### 响应要求：
1. **严格遵循 JSON 格式**：所有回复必须是有效的 JSON，不得包含任何额外的文字、解释或格式。
2. **状态字段**：
   - 成功时，`respon_status` 字段的值为 `"success"`，并包含一个 `data` 字段，用于存放具体的数据。
   - 发生错误时，`respon_status` 字段的值为 `"error"`，并包含一个 `message` 字段，用于描述错误信息。
3. **数据字段**：
   - 在成功响应中，`data` 字段应根据请求内容动态生成，确保数据的完整性和准确性。
4. **错误处理**：
   - 对于无效请求、参数错误、资源未找到等情况，返回符合错误响应格式的 JSON，并提供明确的错误描述。

### 示例：

**请求：**
获取用户信息，用户ID为12345

**成功响应：**
{
  "respon_status": "success",
  "data": [
        {
            "come_type"="TEXT",
            "come_format"="fstring",
            "content"="This is a sample text content."
        },
        {
            "come_type"="TEXT",
            "come_format"="fstring",
            "content"="这是一个例子"
        },
        {
            "come_type"="TEXT",
            "come_format"="fstring",
            "content"="{
                            \"name\": \"zs\",
                            \"age\": 20,
                            \"gender\": \"男\",
                            \"address\": None,
                            \"hobby\": [\"吃饭\", \"睡觉\", \"打豆豆\"]
                        }"
        },
  ]
}

**请求：**
获取用户信息，用户ID为不存在的ID

**错误响应：**
{
  "respon_status": "error",
  "message": "用户未找到"
}

### 注意事项：
- 无论请求内容为何，所有回复必须严格按照上述 JSON 格式进行。
- 不要在回复中添加任何额外的说明、注释或格式化内容。
- 确保 JSON 的语法正确，无语法错误。

请根据以上要求处理接下来的所有请求，并确保回复的每一个响应都符合上述规范。
"""
# 示范的一个请求数据 come_data 中的 comes
"""
# 示例协议范例
image_url = "https://www.baidu.com/img/bd_logo1.png"
comes = {
    DataItem(content="process"),
    DataItem(content=system_promt),
    DataItem(DaType.IMAGE,DaFormat.furl,content=f"{image_url}"),
    DataItem(content="图片中的内容是什么")
}
"""
class ComeEntity:
    def __init__(self):
        self.id = None  # 请求 ID，用于跟踪/排错
        self.timestamp = None  # 发起请求时间（ISO8601 格式）
        self.model = None  # 指定大模型的版本或引擎
        self.respon_status = None  # 返回状态
        self.comes = None # 多模态输入，可以存储多个图文/音频等数据块
        self.context = None  # 其他上下文信息（与用户有关）
    def setup(
            self,
            comes: [DataItem],
            respon_status: str='OK',
            context: ContextEntity = None,
    ) -> 'ComeEntity':
        """
        设置输入参数.
        :param id: 请求 ID
        :param timestamp: 请求时间，可以是字符串或 datetime 对象
        :param model: 使用的大模型版本或引擎
        :param respon_status: 指定返回状态
        :param comes: 输入信息数组（支持 text, image 等）
        :param context: 上下文信息（如用户和元数据）
        :return: 返回 self
        """
        
        self.id = str(uuid.uuid4()).replace('-', '')[:8]
        self.timestamp = datetime.now().isoformat()
        self.model = 'llava-hf/llava-onevision-qwen2-7b-ov-hf'
        self.respon_status = respon_status
        self.comes = comes
        self.context = context
        return self

    def obj2dct(self) -> Dict:
        """
        将对象转化为字典格式，以用于序列化/传输.
        :return: 字典格式的 ComeEntity
        """
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "model": self.model,
            "respon_status": self.respon_status,
            "comes": [di.obj2dct() for di in self.comes],
            "context": self.context.obj2dct(),
        }
    
    @staticmethod
    def as_ComeEntity(dct: Dict):
        """
        从字典重新构建对象
        :param dct: 字典输入
        :return: 重建的 ComeEntity 对象
        """
        con = ComeEntity()
        con.id = dct.get("id")
        con.timestamp = dct.get("timestamp")
        con.model = dct.get("model")
        con.respon_status = dct.get("respon_status")
        con.comes = [DataItem.as_DataItem(di) for di in dct.get("comes", [])]
        con.context = ContextEntity.as_ContextEntity(dct.get("context", {}))
        return con