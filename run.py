"""
Initiate application
"""
from Application import create_app
from Application.config import APP_CONFIG

Config = APP_CONFIG['development']
APP = create_app(Config)

if __name__ == '__main__':
    APP.run(debug=Config.DEBUG)
