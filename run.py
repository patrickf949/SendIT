"""
Initiate application
"""
from Application import create_app
from Application.config import app_config

Config = app_config['production']
APP = create_app(Config)

if __name__ == '__main__':
    APP.run(debug=Config.DEBUG)
