from common.Date import DateHelper
from flask import Flask, jsonify, request, Response
from api import *
import os


@app.route('/')
@app.route('/index')
def home():
    dateStr = DateHelper.date_string()
    return jsonify({'time': dateStr})


@app.route('/admin', methods=['GET', 'POST'], defaults={'apiName': 'admin'})
@app.route('/admin/<apiName>', methods=['GET', 'POST'])
def admin_api(apiName):
    request_data = request.form.to_dict()
    print("admin_api", apiName)
    # if request_data.get("action") == "" or request_data.get("action") is None:
    #     return jsonify({'code': 0})
    # else:
    # match apiName:
    #     case 'admin':
    #         currClass = admin.AdminAdmin(request_data.get("action"))
    #     case 'store':
    #         if request.args.get('action') == 'uploadImg':
    #             request_data["action"] = 'uploadImg'
    #
    #         currClass = store.StoreAdmin(request_data.get("action"))
    #     case 'user':
    #         currClass = user.UserAdmin(request_data.get('action'))
    #     case 'orders':
    #         currClass = orders.OrdersAdmin(request_data.get('action'))
    #     case _:
    #         currClass = None
    #
    # resp_data = currClass.init_data(request_data)
    # print(resp_data)
    # return jsonify(resp_data)


@app.route('/api/<apiName>', methods=['GET', 'POST'])
def api_port(apiName):
    request_data = request.form.to_dict()
    print("api", apiName)
    # match apiName:
    #     case 'user':
    #         currClass = user.UserApi(request_data.get("action"))
    #     case 'store':
    #         currClass = store.StoreApi(request_data.get("action"))
    #     case 'orders':
    #         currClass = orders.OrdersApi(request_data.get('action'))
    #     case _:
    #         currClass = None
    #
    # resp_data = currClass.init_data(request_data)
    # print(resp_data)
    # return jsonify(resp_data)
