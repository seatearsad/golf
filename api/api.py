class Api:
    def __init__(self, action):
        self.action = action

    def init_data(self, data: dict):
        print('Api init_data', self.action)
        print("init_data", data)
        if self.action == '' or self.action is None:
            return self.error("违规操作")
        else:
            return self.handleRequest(data)

    def success(self, data: dict):
        return dict(code=1, data=data)

    def error(self, message):
        return dict(code=0, msg=message)

    def handleRequest(self, data):
        return self.error("未找到执行方法")
