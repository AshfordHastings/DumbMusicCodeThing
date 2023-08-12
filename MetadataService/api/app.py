from flask import Flask, g
from api.routes import artist_bp, song_bp, playlist_bp, user_bp
from api.middleware import init_auth, init_db_session
from api.responses import init_error_handlers

def create_app(sessionmaker):
    app = Flask(__name__)

    init_db_session(app)
    init_auth(app)
    init_error_handlers(app)

    
    app.register_blueprint(artist_bp, url_prefix='/artists')
    app.register_blueprint(song_bp, url_prefix='/songs')
    app.register_blueprint(playlist_bp, url_prefix='/playlists')
    app.register_blueprint(user_bp, url_prefix='/users')
    
    return app