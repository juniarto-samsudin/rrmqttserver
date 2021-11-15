from flask import Blueprint

blueprint = Blueprint(
    'azml_blueprint',
    __name__,
    url_prefix='/api/azml',
    template_folder='templates',
    static_folder='static'
)