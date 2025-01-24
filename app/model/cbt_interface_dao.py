# Copyright(c) 2020 -$today.year.by Nanjing Shushui Intelligent Technology Co., Ltd.,
# All rights reserved.
# @Project       : pytf
# @File          : cbt_model_interface.py
# @Author        : henryren
# @Time          : 2025/1/12 17:04
# @Function      : 
# @Desc          : 模型的接口类型
from dataclasses import dataclass
from typing import Dict

from app.error.PyTFError import catchexcept
from app.model.data_item import DataItem
@dataclass
class CbtInterfaceBpmn:
    id:str
    interface_name: str
    req_comes: [DataItem] = None
    resp_comes: [DataItem] = None

    def obj2dct(self) ->Dict:
        some = self.__dict__
        if self.req_comes is not None:
            some["req_comes"] = [entry.obj2dct() for entry in self.req_comes]
        if self.resp_comes is not None:
            some["resp_comes"] = [entry.obj2dct() for entry in self.resp_comes]
        return some

    @staticmethod
    def as_CbtInterfaceBpmn(dct: Dict):
        some = CbtInterfaceBpmn(
            id=dct.get('id'),
            interface_name=dct.get('interface_name'),
        )
        req_comes = dct.get('req_comes', None)
        resp_comes = dct.get('resp_comes', None)
        some.req_comes = [DataItem.as_DataItem(di) for di in req_comes] if req_comes is not None else None
        some.resp_comes = [DataItem.as_DataItem(di) for di in resp_comes] if resp_comes is not None else None
        return some


@dataclass
class CbtInterfaceDao:
    id:str
    interface_name: str
    api_endpoint:str
    headers : str
    method: str
    request_body_json: str
    response_json: str
    in_comes: str
    out_comes: str
    req_comes: [DataItem] = None
    resp_comes: [DataItem] = None

    def obj2dct(self) ->Dict:
        some = self.__dict__
        if self.req_comes is not None:
            some["req_comes"] = [entry.obj2dct() for entry in self.req_comes]
        if self.resp_comes is not None:
            some["resp_comes"] = [entry.obj2dct() for entry in self.resp_comes]
        return some

    @staticmethod
    def as_CbtInterfaceDao(dct: Dict):
        some = CbtInterfaceDao(
            id=dct.get('id'),
            interface_name=dct.get('interface_name'),
            api_endpoint=dct.get('api_endpoint'),
            headers=dct.get('headers'),
            method=dct.get('method'),
            request_body_json=dct.get("request_body_json"),
            response_json=dct.get("response_json"),
            in_comes=dct.get("in_comes"),
            out_comes=dct.get("out_comes"),
        )
        req_comes = dct.get('req_comes', None)
        resp_comes = dct.get('resp_comes', None)
        some.req_comes = [DataItem.as_DataItem(di) for di in req_comes ] if req_comes is not None else None
        some.resp_comes = [DataItem.as_DataItem(di) for di in resp_comes] if resp_comes is not None else None
        # some.showContent()
        return some
    @catchexcept(f'CbtInterfaceDao:to_bpmn:')
    def to_bpmn(self):
        return CbtInterfaceBpmn(
            id=self.id,
            interface_name=self.interface_name,
            req_comes = [self.req_comes[i] for i in  [int(x) for x in self.in_comes.split(",")]] if self.req_comes else None,
            resp_comes =[self.resp_comes[i] for i in  [int(x) for x in self.out_comes.split(",")]] if self.resp_comes else None
        )

    def showContent(self):
        print(f"CbtInterfaceDao 展示内容")
        for key, value in self.__dict__.items():
            if key == "req_comes" or key == "resp_comes":
                if value is None:
                    print(f"{key}: None")
                else:
                    for data in value:
                        print(f"{key} : {data.data_type} {data.data_format} {data.content}")
            else:
                print(f"{key}: {value}")
    def get_req_comes_keys(self) -> str:
        """
        获取 req_comes 所有项的第一个 key 组成的字符串
        :return: 以逗号分隔的字符串，由 req_comes 的每项的第一个 key 组成
        """
        if self.req_comes is None:
            return ""
        # 提取每个 DataItem 的第一个 key
        keys = [entry.data_type for entry in self.req_comes ]
        # 将 keys 转换为以逗号分隔的字符串
        return ",".join(keys)

    def get_resp_comes_keys(self) -> str:
        """
        获取 resp_comes 所有项的第一个 key 组成的字符串
        :return: 以逗号分隔的字符串，由 resp_comes 的每项的第一个 key 组成
        """
        if self.resp_comes is None:
            return ""
        # 提取每个 DataItem 的第一个 key
        keys = [entry.data_type for entry in self.resp_comes ]
        # 将 keys 转换为以逗号分隔的字符串
        return ",".join(keys)