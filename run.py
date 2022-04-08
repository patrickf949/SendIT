"""
Initiate application
"""
from Application import create_app
from Application.config import app_config
from flask_cors import CORS

Config = app_config['production']
APP = create_app(Config)
CORS(APP)

if __name__ == '__main__':
    APP.run(debug=Config.DEBUG)
