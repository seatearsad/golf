from flask_sqlalchemy import SQLAlchemy

HOST = "localhost"
PORT = 3306
DATA_BASE = "golfdb"
USER = "root"
PWD = "root"

DB_URI = f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DATA_BASE}"


db = SQLAlchemy()


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    global db
    db.init_app(app)
