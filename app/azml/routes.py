from app.azml import blueprint
from flask import current_app, Response, request, jsonify
import json
from app.azml.util import AZ_MLWS, INFLUXSTORAGE

@blueprint.route('', strict_slashes=False, methods=['POST'])
def azml_send():
    request_data = request.get_json()
    print('REQUEST_DATA AZML: ', request_data)

    myList = request_data
    myAzml = AZ_MLWS()
    responseJson = myAzml.send(myList)

    myInfluxStorage = INFLUXSTORAGE('ml3')
    myInfluxStorage.writeDbFz(responseJson)


    print('ResponseJson: ', responseJson)

    return Response(json.dumps(responseJson),status=200, mimetype='application/json')



