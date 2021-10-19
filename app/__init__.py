from flask import Flask
from importlib import import_module
import logging

def register_blueprints(app):
    for module_name in ('errorhandlers','mqtt'):
        print("MODULE NAME:", module_name)
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    if app.config['FILELOGGING']:
        print('FILELOGGIN')
        logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    if app.config['DEBUG']:
        print('DEBUG')
        logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    register_blueprints(app)
    return app