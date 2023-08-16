import _io
import io
import os
import base64
import re
import common.Date as Date
import random


def save_image_base64(image, path, name='store', cid='1001'):
    current_path = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(current_path, '..'))
    img_path = ROOT_DIR + '/upload/' + name + '/' + path + '/' + cid

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    img_path = img_path + '/' + str(Date.DateHelper.date_number()) + '.png'

    request_base64 = image
    imgData = re.sub('^data:image/.+;base64,', '', request_base64)
    imgData = base64.b64decode(imgData)

    with open(img_path, "wb") as fh:
        fh.write(imgData)

    return re.sub('^'+ROOT_DIR, '', img_path)


def save_img_file(file, name='store', path='images'):
    rand_num = int(random.uniform(10, 99))
    current_path = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(current_path, '..'))
    img_path = ROOT_DIR + '/upload/' + name + '/' + path + '/' + str(rand_num)
    save_path = '/upload/' + name + '/' + path + '/' + str(rand_num)

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    fileName: str = file.filename
    nameList = fileName.split('.')
    typeName = nameList[len(nameList)-1]

    name = str(Date.DateHelper.date_number())
    saveName = img_path + '/' + name + '.' + typeName
    returnName = save_path + '/' + name + '.' + typeName
    if not file is None:
        file.save(saveName)

    return returnName


def del_image_path(path):
    current_path = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(current_path, '..'))
    img_path = ROOT_DIR + path

    if os.path.exists(img_path):
        os.remove(img_path)


def save_qr_code(code, userId):
    current_path = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(current_path, '..'))
    img_path = ROOT_DIR + '/upload/user/code/' + str(userId)

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    img_path = img_path + '/code.png'

    if not os.path.exists(img_path):
        with open(img_path, "wb") as fh:
            fh.write(code)

    return re.sub('^'+ROOT_DIR, '', img_path)
