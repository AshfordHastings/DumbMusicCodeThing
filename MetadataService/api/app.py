from flask import Flask, g
from api.routes import artist_bp, song_bp, playlist_bp, user_bp, health_bp
from api.middleware import init_auth, init_db_session
from api.responses import init_error_handlers
from cfg import TestingConfig, DevelopmentConfig

CONFIG_MAPPER = {
    'testing': TestingConfig,
    'development': DevelopmentConfig
}

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAPPER[config_name])

    init_db_session(app)
    init_auth(app)
    init_error_handlers(app)

    
    app.register_blueprint(artist_bp, url_prefix='/artists')
    app.register_blueprint(song_bp, url_prefix='/songs')
    app.register_blueprint(playlist_bp, url_prefix='/playlists')
    app.register_blueprint(user_bp, url_prefix='/users')

    app.register_blueprint(health_bp, url_prefix='/health')
    
    return app