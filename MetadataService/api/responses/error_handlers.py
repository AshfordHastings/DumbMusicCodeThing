
from exc import ResourceNotFound
from api.responses.responses import (
    NOT_FOUND_404,
    ERROR_500
)
from api.responses import response_with


def init_app(app):

    @app.errorhandler(ResourceNotFound)
    def handle_not_found(error):
        response_with(NOT_FOUND_404, error)

    @app.errorhandler(Exception)
    def handle_exceptions(error):
        response_with(ERROR_500, error)