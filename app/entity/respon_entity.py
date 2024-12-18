from http import HTTPStatus


class InfoEntity:
    def __init__(self):
        self.name = None
        self.status = None

    def ok(self, name: str) -> object:
        self.name = name
        self.status = HTTPStatus.OK
        return self

    def exception(self, name: str) -> object:
        self.name = name
        self.status = HTTPStatus.INTERNAL_SERVER_ERROR
        return self

    def obj2dct(self) -> []:
        dct = {}
        if self.name is not None:
            dct['name'] = self.name
        if self.status is not None:
            dct['status'] = self.status
        return dct

    @staticmethod
    def as_InfoEntity(dct):
        hao = InfoEntity()
        hao.name = dct['name']
        hao.status = dct['status']
        return hao


class ResponEntity:
    def __init__(self):
        self.info = None
        self.data = None

    def ok(self, name: str, obj: object) -> []:
        self.info = InfoEntity().ok(name)
        self.data = obj
        return self.obj2dct()

    def exception(self, name: str, e: Exception) -> []:
        self.info = InfoEntity().exception(name)
        self.data = str(e)
        return self.obj2dct()

    def obj2dct(self) -> []:
        dct = {}
        if self.info is not None:
            dct['info'] = InfoEntity.obj2dct(self.info)
        if self.data is not None:
            dct['data'] = self.data
        return dct

    @staticmethod
    def as_ResponEntity(dct):
        hao = ResponEntity()
        hao.info = InfoEntity.obj2dct(dct['info'])
        hao.data = dct['data']
        return hao
