from requests import exceptions
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
    #WRITE INCOMING FEATURES
    myInfluxStorage = INFLUXSTORAGE('ml3features')
    try:
        myInfluxStorage.writeDbFzFeatures(myList)
    except Exception as e:
        print('ERROR: ', e)
        responseJson = {'status': 'error', 'message': 'Error writing features to InfluxDB'}
        return Response(json.dumps(responseJson), mimetype='application/json', status=500)
    else:
        try:
            #SEND DATA TO AZURE ML AND GET PREDICTION RESULT
            responseJson = myAzml.send(myList)
            #WRITE PREDICTION RESULT TO INFLUXDB
            myInfluxStorage = INFLUXSTORAGE('ml3')
            myInfluxStorage.writeDbFz(responseJson)
        except Exception as e:
            print('ERROR: ', e)
            responseJson = {'status': 'error', 'message': 'Error writing prediction result to InfluxDB'}
            return Response(json.dumps(responseJson), mimetype='application/json', status=500)
        else:
            print('ResponseJson: ', responseJson)
            return Response(json.dumps(responseJson),status=200, mimetype='application/json')



