from flask import Flask
import models

app = Flask(__name__, static_folder='../upload')
models.init_app(app)


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)

__all__ = ['app', 'user', 'admin', 'store', 'orders', 'adapay_callback']
