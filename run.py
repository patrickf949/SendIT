"""
Initiate application
"""
from Application import create_app
from Application.config import app_config

config = app_config['development']
app = create_app(config)

if __name__ == '__main__':
    app.run(debug=True)
