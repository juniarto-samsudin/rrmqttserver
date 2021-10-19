from app.mqtt import blueprint
from flask import current_app, Response, request
import json
from app.mqtt.util import AZ_MQTT


@blueprint.route('', strict_slashes=False, methods=['POST'])
def mqtt_send():
    request_data = request.get_json()
    print('REQUEST_DATA: ', request_data)
    
    myList = request_data
    myMqtt = AZ_MQTT()
    myMqtt.send(myList)

    response_dict={}
    response_dict['status'] = 'OK'
    return Response(json.dumps(response_dict), status=200, mimetype='application/json')