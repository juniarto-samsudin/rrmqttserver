import os
from decouple import config
import requests
import json

class Config(object):
    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')
    API_KEY = config('API_KEY')
    TOKEN = config('TOKEN', default='password')
    
    PLATFORM_AGENT_API_URL = config('PLATFORM_AGENT_API_URL', default='http://172.20.10.152:8080/scaft-platform-agent/api')
    PLATFORM_AGENT_API_TOKEN = "Bearer " + config('PLATFORM_AGENT_API_TOKEN', default='password')

    ML_MODELS_DIR = config('ML_MODELS_DIR', default='/home/scaft-admin/ml-models')

    CONNECTION_STRING = config('CONNECTION_STRING')

    FEATURE_LOG_FILE = config('FEATURE_LOG_FILE', default='feature_log.log')
    PREDICTION_LOG_FILE = config('PREDICTION_LOG_FILE', default='prediction_log.log')

class DevelopmentConfig(Config):
    DEBUG = True         #LOGGING TO SCREEN, select either one
    FILELOGGING = False  #LOGGING TO 'record.log', select either one

class DevTestConfig(Config): #FOR DEVELOPMENT PURPOSE [JUNIARTO], edit .env to revert back to production
    #PLATFORM_AGENT_API_URL = 'http://172.20.10.152:8080/scaft-platform-agent/api'
    PLATFORM_AGENT_API_URL = 'http://172.20.98.138:8081/scaft-platform-agent/api'
    ML_MODELS_DIR = '/media/juniarto/TOSHIBAEXT/WORK/FUJITSU/ml-models'
    DEBUG = True         #LOGGING TO SCREEN , either one
    FILELOGGING = False  #LOGGING TO 'record.log', either one

config_dict = {
     'Development': DevelopmentConfig,
     'Devtest' : DevTestConfig
}
