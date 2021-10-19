from flask import Blueprint

blueprint = Blueprint(
    'error_blueprint',
    __name__,
    url_prefix='/error',
    template_folder='templates',
    static_folder='static'
)