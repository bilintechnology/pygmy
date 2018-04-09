import datetime

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from pygmy.config import config

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = False
app.config.setdefault('JWT_ACCESS_TOKEN_EXPIRES', datetime.timedelta(minutes=1))
app.config.setdefault('JWT_REFRESH_TOKEN_EXPIRES', datetime.timedelta(days=7))
app.config.setdefault('JWT_HEADER_NAME', 'JWT_Authorization')
app.secret_key = config.secret

jwt = JWTManager(app)

# This import is required. Removing this will break all hell loose.
import pygmy.rest.urls as _


def run():
    #app.run(host=config.host, port=int(config.port))
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(int(config.port), address=config.host)
    IOLoop.current().start()
