import os
from api.app import create_app

config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

bind = "0.0.0.0:8000"
workers = 4