import os

os.system('gunicorn --config gunicorn-conf.py  run:app')