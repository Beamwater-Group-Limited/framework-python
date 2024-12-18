import falcon


# 项目启动测试
class HelloWorldController:
    def on_get(self, request, response):
        response.body = f'成功\nHello World'
        response.status = falcon.HTTP_200
