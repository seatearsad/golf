from models.store import Store, Course, db
from api.api import Api
from common.saveImg import save_image_base64, save_img_file, del_image_path
import json
from flask import request


class StoreApi(Api):
    def init_data(self, data: dict):
        print("init_data", data)
        is_continue = super().init_data(data)
        if is_continue != 'OK':
            return is_continue
        else:
            match self.action:
                case 'getStoreList':
                    index = data.get('page')
                    size = data.get('pageSize')
                    keyword = data.get('keyword')
                    lat = data.get("lat")
                    lng = data.get("lng")
                    currData = Store.getListOrderByDistance(keyword, index, size, lat, lng)
                case 'getStoreInfo':
                    storeId = data.get('id')
                    store = Store.getStoreById(storeId)
                    currData = Store.handleStore(store)
                case 'getCourseInfo':
                    id = data.get('id')
                    storeId = data.get('storeId')
                    currData = eval(str(Course.getCourseById(id)))
                case 'searchStoreList':
                    index = data.get('page')
                    size = data.get('pageSize')
                    keyword = data.get('keyword')
                    lat = data.get("lat")
                    lng = data.get("lng")
                    storeType = data.get('type')
                    cityId = data.get('cityId')
                    currData = Store.getListOrderByDistance(keyword, index, size, lat, lng, storeType, cityId)
                case _:
                    currData = None

            print(currData)

        return self.success(currData)


class StoreAdmin(Api):
    def init_data(self, data: dict):
        print("init_data", data)
        is_continue = super().init_data(data)
        if is_continue != 'OK':
            return is_continue
        else:
            match self.action:
                case 'save':
                    # img_path = save_image_base64(data.get('data'), 'logo')
                    # currStore = dict(img_path=img_path)
                    storeData = data.get('data')
                    storeData: dict = json.loads(storeData)

                    if storeData.get('id') == 0 or storeData.get('id') is None:
                        store = Store.insertData(storeData)
                        if not 'http://' in storeData.get('logo') and not 'https://' in storeData.get('logo'):
                            img_path = save_image_base64(storeData.get('logo'), 'logo', 'store', str(store.id))
                            store.logo = img_path
                        db.session.commit()
                        currData = dict(id=store.id)
                    else:
                        store = Store.getStoreById(storeData.get('id'))
                        if not 'http://' in storeData.get('logo') and not 'https://' in storeData.get('logo'):
                            img_path = save_image_base64(storeData.get('logo'), 'logo', 'store', str(store.id))
                            store.logo = img_path
                        store.name = storeData.get('name')
                        store.type = storeData.get('type')
                        store.address = storeData.get('address')
                        store.city_id = storeData.get('city')[2]
                        store.lng = storeData.get('lng')
                        store.lat = storeData.get('lat')
                        store.status = storeData.get('status')
                        store.intro = storeData.get('intro')
                        store.phone = storeData.get('phone')
                        store.designer = storeData.get('designer')
                        store.images = ';'.join(storeData.get('images'))
                        db.session.commit()
                        currData = dict(id=store.id)
                case 'getStoreList':
                    keyword = data.get('keyword')
                    index = data.get('page')
                    size = data.get('pageSize')
                    currData = Store.getList(keyword, index, size)
                case 'saveCourse':
                    courseData = data.get('data')
                    courseData: dict = json.loads(courseData)
                    if courseData.get('id') == 0 or courseData.get('id') is None:
                        course = Course.insertData(courseData)
                        currData = dict(id=course.id)
                    else:
                        course = Course.getCourseById(courseData.get('id'))
                        course.name = courseData.get('name')
                        course.open_time = courseData.get('open_time')
                        course.close_time = courseData.get('close_time')
                        course.hole_count = courseData.get('hole_count')
                        course.pars = courseData.get('pars')
                        course.normal_price = courseData.get('normal_price')
                        course.holiday_price = courseData.get('holiday_price')
                        course.distance = courseData.get('distance')
                        course.status = courseData.get('status')
                        course.intro = courseData.get('intro')
                        course.unit = courseData.get('unit')
                        course.unit_vol = courseData.get('unit_vol')
                        db.session.commit()
                        currData = eval(str(course))
                case 'uploadImg':
                    savePath = save_img_file(request.files.get('file'))
                    currData = dict(imgPath=savePath)
                case 'delImg':
                    del_image_path(data.get('path'))
                    currData = None
                case _:
                    currData = None

            print(currData)

        return self.success(currData)
