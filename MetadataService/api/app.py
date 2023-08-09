from flask import Flask, g
from api.routes import artist_bp, song_bp, playlist_bp
from api.middleware.auth import load_jwt_claims

def create_app(sessionmaker):
    app = Flask(__name__)

    @app.before_request
    def init_db_context():
        g.db_session = sessionmaker()

    @app.before_request
    def init_auth():
        load_jwt_claims

    @app.after_request
    def teardown_db_context(response):
        db_session = getattr(g, 'db_session', None)
        if db_session is not None:
            db_session.close()
        return response
    
    app.register_blueprint(artist_bp, url_prefix='/artists')
    app.register_blueprint(song_bp, url_prefix='/songs')
    app.register_blueprint(playlist_bp, url_prefix='/playlists')
    
    return app