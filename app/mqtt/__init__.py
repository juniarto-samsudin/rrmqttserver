from flask import Blueprint

blueprint = Blueprint(
    'mqtt_blueprint',
    __name__,
    url_prefix='/api/mqtt',
    template_folder='templates',
    static_folder='static'
)
