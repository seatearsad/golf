class Api:
    def __init__(self, action):
        self.action = action

    def init_data(self, data: dict):
        print('Api init_data', self.action)
        if self.action == '' or self.action is None:
            return self.error("违规操作")
        else:
            return 'OK'

    def success(self, data: dict):
        return dict(code=1, data=data)

    def error(self, message):
        return dict(code=0, msg=message)