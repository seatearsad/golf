import os
import common.Date as Date

class Adapay_callback:
    def init_data(self, request_data):
        print(request_data)
        current_path = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.abspath(os.path.join(current_path, '..'))
        path = ROOT_DIR + '/callback'

        if not os.path.exists(path):
            os.makedirs(path)

        file_path = path + '/' + str(Date.DateHelper.date_number()) + '.txt'

        with open(file_path, "w") as fh:
            fh.write(str(request_data))

