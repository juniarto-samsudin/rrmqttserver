from app import create_app
from decouple import config
from config import config_dict

get_config_mode = config('DEPLOY_OPT', default='Development')

try:
    app_config = config_dict[get_config_mode.capitalize()]
except:
    exit('Error: Invalid <config_mode>. Expected values [Development]')

app = create_app(app_config)

#FORCE RELEASE PREVIOUS LOCK INCASE IT IS NOT PROPERLY RELEASED
print("get_config_mode: ", get_config_mode)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, use_reloader=False)
