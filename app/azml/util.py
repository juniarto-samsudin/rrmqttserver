from flask import current_app, jsonify, Response
import json
import encodings
import requests
from werkzeug.datastructures import ResponseCacheControl

from influxdb import InfluxDBClient
import json
import datetime
import dateutil.parser

import logging
from decouple import config


featureLogger = logging.getLogger('featureLogger')
featureLogger.setLevel(logging.INFO)


predictionLogger = logging.getLogger('predictionLogger')
predictionLogger.setLevel(logging.INFO)


feature_file_handler = logging.FileHandler(config('FEATURE_LOG_FILE',default='feature_log.log'))
prediction_file_handler = logging.FileHandler(config('PREDICTION_LOG_FILE',default='prediction_log.log'))

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

feature_file_handler.setFormatter(formatter)
prediction_file_handler.setFormatter(formatter)

featureLogger.addHandler(feature_file_handler)
predictionLogger.addHandler(prediction_file_handler)

dummyData = {
    "Inputs": {
        "WebServiceInput0":
        [
            {
                'S1F1': "0.294584751",
                'S1F2': "0.487396256",
                'S1F3': "0.769794781",
                'S1F4': "0.167549024",
                'S1F5': "0.109226423",
                'S1F6': "0.268328812",
                'S1F7': "0.302326047",
                'S1F8': "0.022780794",
                'S1F9': "0.78553996",
                'S1F10': "0.191243954",
                'S1F11': "0.713627382",
                'S1F12': "0.123727668",
                'S1F13': "0.126918181",
                'S1F14': "0.445810625",
                'S1F15': "0.582253277",
                'S1F16': "0.068632711",
                'S1F17': "0.31566398",
                'S1F18': "0.032231778",
                'S1F19': "0.809674016",
                'S1F20': "0.4050147",
                'S1F21': "0.983478115",
                'S1F22': "0.416501495",
                'S1F23': "0.599061898",
                'S1F24': "0.771137511",
                'S1F25': "0.05532688",
                'S1F26': "0.058607237",
                'S1F27': "0.010102743",
                'S1F28': "0.848603671",
                'S1F29': "0.741882415",
                'S1F30': "0.704891292",
                'S1F31': "0.988421997",
                'S1F32': "0.457799714",
                'S1F33': "0.990502142",
                'S1F34': "0.157884472",
                'S1F35': "0.4342679",
                'S1F36': "0.999633252",
                'S1F37': "0.910603304",
                'S1F38': "0.515012406",
                'S1F39': "0.179352802",
                'S1F40': "0.127069348",
                'S1F41': "0.997265886",
                'S1F42': "0.983483734",
                'S1F43': "0.008501646",
                'S1F44': "0.449631529",
                'S1F45': "0.299063712",
                'S1F46': "0.068793294",
                'S1F47': "0.059141722",
                'S1F48': "0.568626433",
                'S1F49': "0.090449348",
                'S1F50': "0.328074454",
                'S2F1': "0.147874222",
                'S2F2': "0.42354462",
                'S2F3': "0.122678465",
                'S2F4': "0.377277288",
                'S2F5': "0.389498664",
                'S2F6': "0.301429097",
                'S2F7': "0.180368128",
                'S2F8': "0.313944322",
                'S2F9': "0.574417691",
                'S2F10': "0.147667603",
                'S2F11': "0.1949325",
                'S2F12': "0.723252118",
                'S2F13': "0.804065242",
                'S2F14': "0.399095189",
                'S2F15': "0.364180778",
                'S2F16': "0.052428004",
                'S2F17': "0.942052862",
                'S2F18': "0.388893116",
                'S2F19': "0.753503502",
                'S2F20': "0.893525972",
                'S2F21': "0.03163632",
                'S2F22': "0.647832088",
                'S2F23': "0.499892004",
                'S2F24': "0.239551401",
                'S2F25': "0.181208493",
                'S2F26': "0.731060657",
                'S2F27': "0.828798181",
                'S2F28': "0.733995672",
                'S2F29': "0.708840187",
                'S2F30': "0.853464068",
                'S2F31': "0.206428333",
                'S2F32': "0.665341643",
                'S2F33': "0.778581064",
                'S2F34': "0.598440154",
                'S2F35': "0.385669506",
                'S2F36': "0.799736931",
                'S2F37': "0.714690467",
                'S2F38': "0.476843679",
                'S2F39': "0.01579012",
                'S2F40': "0.517540132",
                'S2F41': "0.187287064",
                'S2F42': "0.99155651",
                'S2F43': "0.235423153",
                'S2F44': "0.442819884",
                'S2F45': "0.418993485",
                'S2F46': "0.12135721",
                'S2F47': "0.076399958",
                'S2F48': "0.378907537",
                'S2F49': "0.321099029",
                'S2F50': "0.918876285",
                'S3F1': "0.811502923",
                'S3F2': "0.27300865",
                'S3F3': "0.003574238",
                'S3F4': "0.382784414",
                'S3F5': "0.548961055",
                'S3F6': "0.456008975",
                'S3F7': "0.150400638",
                'S3F8': "0.4080599",
                'S3F9': "0.837162397",
                'S3F10': "0.16181485",
                'S3F11': "0.490054582",
                'S3F12': "0.634464384",
                'S3F13': "0.699969992",
                'S3F14': "0.060777064",
                'S3F15': "0.095701443",
                'S3F16': "0.615862263",
                'S3F17': "0.223657408",
                'S3F18': "0.406784229",
                'S3F19': "0.202964489",
                'S3F20': "0.257581987",
                'S3F21': "0.638602059",
                'S3F22': "0.450694523",
                'S3F23': "0.006034771",
                'S3F24': "0.410584459",
                'S3F25': "0.809753995",
                'S3F26': "0.70262032",
                'S3F27': "0.516329205",
                'S3F28': "0.084453086",
                'S3F29': "0.513257532",
                'S3F30': "0.428329398",
                'S3F31': "0.245538211",
                'S3F32': "0.491108127",
                'S3F33': "0.847196112",
                'S3F34': "0.80055122",
                'S3F35': "0.649229892",
                'S3F36': "0.502744801",
                'S3F37': "0.090435852",
                'S3F38': "0.070936416",
                'S3F39': "0.849875657",
                'S3F40': "0.960330102",
                'S3F41': "0.318707967",
                'S3F42': "0.235032173",
                'S3F43': "0.542276114",
                'S3F44': "0.548835887",
                'S3F45': "0.099629187",
                'S3F46': "0.88481247",
                'S3F47': "0.743295759",
                'S3F48': "0.739154656",
                'S3F49': "0.182671935",
                'S3F50': "0.753718133",
                'S4F1': "0.693124132",
                'S4F2': "0.526640625",
                'S4F3': "0.376363824",
                'S4F4': "0.835261867",
                'S4F5': "0.928751107",
                'S4F6': "0.460644846",
                'S4F7': "0.445062821",
                'S4F8': "0.443475547",
                'S4F9': "0.152958132",
                'S4F10': "0.05477746",
                'S4F11': "0.219753165",
                'S4F12': "0.120399836",
                'S4F13': "0.919925607",
                'S4F14': "0.592622525",
                'S4F15': "0.63123112",
                'S4F16': "0.733068328",
                'S4F17': "0.958133153",
                'S4F18': "0.496372232",
                'S4F19': "0.223252535",
                'S4F20': "0.368211792",
                'S4F21': "0.816776312",
                'S4F22': "0.323219663",
                'S4F23': "0.359627712",
                'S4F24': "0.776838147",
                'S4F25': "0.922003806",
                'S4F26': "0.06217513",
                'S4F27': "0.796770771",
                'S4F28': "0.343721901",
                'S4F29': "0.309364883",
                'S4F30': "0.517852546",
                'S4F31': "0.165956896",
                'S4F32': "0.776460616",
                'S4F33': "0.016338952",
                'S4F34': "0.012245247",
                'S4F35': "0.059756109",
                'S4F36': "0.685801684",
                'S4F37': "0.567493456",
                'S4F38': "0.936015558",
                'S4F39': "0.557886241",
                'S4F40': "0.947910194",
                'S4F41': "0.744111903",
                'S4F42': "0.950919686",
                'S4F43': "0.663759344",
                'S4F44': "0.877879842",
                'S4F45': "0.329401209",
                'S4F46': "0.000217876",
                'S4F47': "0.548545699",
                'S4F48': "0.796220081",
                'S4F49': "0.586416205",
                'S4F50': "0.549697861",
                'S5F1': "0.325351575",
                'S5F2': "0.698965302",
                'S5F3': "0.6419336",
                'S5F4': "0.248446395",
                'S5F5': "0.805193658",
                'S5F6': "0.161876477",
                'S5F7': "0.174990816",
                'S5F8': "0.717025598",
                'S5F9': "0.652885092",
                'S5F10': "0.010878503",
                'S5F11': "0.825924633",
                'S5F12': "0.985820856",
                'S5F13': "0.610660814",
                'S5F14': "0.321965426",
                'S5F15': "0.198707614",
                'S5F16': "0.646748962",
                'S5F17': "0.969831223",
                'S5F18': "0.589314354",
                'S5F19': "0.646055754",
                'S5F20': "0.166579276",
                'S5F21': "0.607912944",
                'S5F22': "0.737544646",
                'S5F23': "0.805543253",
                'S5F24': "0.447362488",
                'S5F25': "0.270195667",
                'S5F26': "0.389842195",
                'S5F27': "0.995199374",
                'S5F28': "0.914513754",
                'S5F29': "0.934248577",
                'S5F30': "0.80834157",
                'S5F31': "0.645180208",
                'S5F32': "0.467111521",
                'S5F33': "0.827354254",
                'S5F34': "0.014694884",
                'S5F35': "0.655419242",
                'S5F36': "0.191966982",
                'S5F37': "0.067904473",
                'S5F38': "0.923737386",
                'S5F39': "0.614296095",
                'S5F40': "0.677521231",
                'S5F41': "0.342975883",
                'S5F42': "0.239293632",
                'S5F43': "0.505157435",
                'S5F44': "0.241181337",
                'S5F45': "0.85889587",
                'S5F46': "0.784682317",
                'S5F47': "0.63243057",
                'S5F48': "0.48721099",
                'S5F49': "0.437193557",
                'S5F50': "0.494887057",
            },
        ],
    },
    "GlobalParameters": {
    }
}


def convertToAzmlSchema(msgList: list):
    """
    Converts a list of messages to the Azml schema.
    """
    azmlSchema = {
        "Inputs": {
            "WebServiceInput0":
            [

            ]
        },
        "GlobalParameters": {
        }
    }
    myDict = {}
    for msg in msgList:
        sensorName = msg['sensorName']
        features = msg['features']
        for fName, fValue in features.items():
            newFName = sensorName + fName
            myDict[newFName] = fValue
    print("+++++MYDICT++++++:", myDict)
    azmlSchema['Inputs']['WebServiceInput0'].append(myDict)
    #print('AZMLSCHEMA: ', azmlSchema)
    
    return azmlSchema

class AZ_MLWS:
    def __init__(self):
        '''
        self.RestUrl = 'http://20.44.230.134:80/api/v1/service/sixmodeldeployeddummy/score'
        self.api_key = 'GdLy07BiRnK89Y4RQZNqaGGx5eHfoAKF' # Replace this with the API key for the web service
        self.headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ self.api_key)}
        
        self.RestUrl = 'http://20.212.96.113:80/api/v1/service/sixmodelstwowebservice/score'
        self.api_key = 'RHxb6ngMrcsHyvtpejo6Zv0HA38RZVlV' # Replace this with the API key for the web service
        self.headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ self.api_key)}
        
        self.RestUrl = 'http://20.44.230.134:80/api/v1/service/all18modelsdummy/score'
        self.api_key = 'xtS5DQDDQ32BR6zYlpNJ18CmQpi1dreH' # Replace this with the API key for the web service
        self.headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ self.api_key)}
        '''
        self.RestUrl = 'http://20.43.146.68:80/api/v1/service/s4ml1deployment/score' 
        self.api_key = 'uKAoWY9fpa8aVjgIYPIFMHAUj5XVGWeu' # Replace this with the API key for the web service
        self.headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ self.api_key)}

    
    def send(self, msgList):
        print('Sending to Azure ML...')
        mySchema = convertToAzmlSchema(msgList)
        print('MYSCHEMA: ', mySchema)
        body = json.dumps(mySchema)
        try:
            response = requests.post(self.RestUrl, data=body, headers=self.headers)
            response.raise_for_status()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.RequestException, requests.exceptions.HTTPError) as err:
            return err
        else:
            print(response.content.decode('utf-8'))
            print('Response Json: ', response.json()['Results'])
            print('Response Json Type: ', type(response.json()))
            return response.json()
            
def blobtoJson(blob):
    myString = blob.decode('utf-8')
    myJson = json.loads(myString)
    return myJson

def getTimeStamp(dateString):
    #myDateObject = datetime.datetime.strptime(dateString, "%Y-%m-%dT%H:%M:%S.%f)
    myDateObject = dateutil.parser.parse(dateString)
    return int(myDateObject.timestamp() * 1000000000)

def getInfluxMsg(myJson):
    try:
        sensorName = myJson['sensorNames']
        timestamp = getTimeStamp(myJson['Time'])
        prediction = myJson['Predicted_Status_decisionforest']
    except Exception as e:
        print('getInfluxMsg: ', e)
        raise ValueError('JsonStructureError: {} does not exist'.format(e))

    MSG_TXT = "{sensorName} prediction={prediction} {timestamp}"   
    MSG_TXT_FORMATTED = MSG_TXT.format(sensorName=sensorName, prediction=prediction, timestamp=timestamp)
    return MSG_TXT_FORMATTED

def getInfluxMsgFzFeatures(myJson):
    MSG_JSON = []
    try:
        for sensor in myJson:
            sensorName = sensor['sensorName']
            featureDict = sensor['features']
            MSG_JSON.append({'measurement': sensorName, 'fields': featureDict})
    except Exception as e:
        print('getInfluxMsgFeatures: ', e)
        raise ValueError('getInfluxMsgFeatures JsonStructureError: {} does not exist'.format(e))   
    else:
        return MSG_JSON

def getInfluxMsgFz(myJson) -> str:
    MSG_JSON = []
    try:
        predResult = myJson['Results']
        for key, value in predResult.items(): #S1ModelsOutput
            fieldsML1 = {}
            fieldsML2 = {}
            fieldsML3 = {}
            for key2, value2 in value[0].items():
                if key2.startswith('ML1'):
                    fieldsML1.update({key2: value2})
                elif key2.startswith('ML2'):
                    fieldsML2.update({key2: value2})
                elif key2.startswith('ML3'):
                    fieldsML3.update({key2: value2})
            '''
            for key2, value2 in value[0].items():          #Scored Labels_1=1.0
                if key2 == 'Scored Labels_1' or key2 == 'Scored Probabilities_1':
                    fieldsML1.update({key2[:-2]: value2})
                elif key2 == 'Scored Labels_2' or key2 == 'Scored Probabilities_2':
                    fieldsML2.update({key2[:-2]: value2})
                elif key2 == 'Scored Labels' or key2 == 'Scored Probabilities':
                    fieldsML3.update({key2: value2})
            '''       
            MSG_JSON.append({'measurement': key, 'tags': {'Model': 'ML1'}, 'fields': fieldsML1})
            MSG_JSON.append({'measurement': key, 'tags': {'Model': 'ML2'}, 'fields': fieldsML2})
            MSG_JSON.append({'measurement': key, 'tags': {'Model': 'ML3'}, 'fields': fieldsML3})
    except Exception as e:
        print('getInfluxMsgFz: ', e)
        raise ValueError('JsonStructure: {} does not exist'.format(e))
    return MSG_JSON

class INFLUXSTORAGE:
    def __init__(self, db, host="localhost", port=8086):
        try:
            self.client = InfluxDBClient(host=host, port=port, database=db)
            self.db = db
        except Exception as err:
            print('INFLUX STORAGE INITIALIZATION FAILED: ', err)
            return 1
        else:
            print('INITIALIZATION COMPLETED')
            self.db = db

    def writeDb(self, blob):
        print('INSIDE WRITEDB:')
        #BLOB FORMAT: {"sensorName":"S1","Time":"2021-10-29T07:07:35.4790000Z","Predicted_Status_decisionforest":"1"}
        print(blob)
        myJson = blobtoJson(blob)
        try:
            influxMsg = getInfluxMsg(myJson)
        except Exception as err:
            print('writedb: ', err)
            return 1

        print(influxMsg)
        try:
            self.client.write([influxMsg],{'db':self.db}, 204,'line')
        except Exception as err:
            print(err)
        else:
            print('written')

    def writeDbFzFeatures(self, myJson):
        print("INSIDE WRITING FEATURES")
        featureLogger.info(myJson)
        try:
            influxMsg = getInfluxMsgFzFeatures(myJson)
            print('INFLUX FEATURES MESSAGES: ', influxMsg)
            self.client.write_points(influxMsg)
        except Exception as err:
            print(err)
            raise ValueError('writeDbFzFeatures: {} error'.format(err))
        else:
            return 0

    def writeDbFz(self, myJson):
        print('INSIDE WRITEDBFZ: WRITE PREDICTION')
        '''
        AZURE ML OUTPUT FORMAT:
        {'Results': {'S2ModelsOutput': [{'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9934365970893647, 
                                         'ML2 Bearing Fault Scored Labels': 0.0, 'ML2 Bearing Fault Scored Probabilities': 7.790251381015847e-05, 
                                         'ML3 Gearbox Fault Scored Labels': 0.0, 'ML3 Gearbox Fault Scored Probabilities': 0.006167442709467959}], 
                     'S3ModelsOutput': [{'ML1 Anomaly Scored Labels': 0.0, 'ML1 Anomaly Scored Probabilities': 0.003526396544994745, 
                                         'ML2 Bearing Fault Scored Labels': 0.0, 'ML2 Bearing Fault Scored Probabilities': 0.09611832145987317, 
                                         'ML3 Gearbox Fault Scored Labels': 0.0, 'ML3 Gearbox Fault Scored Probabilities': 6.396071431781235e-06}], 
                     'S1ModelsOutput': [{'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9999811413264189, 
                                         'ML2 Bearing Fault Scored Labels': 1.0, 'ML2 Bearing Fault Scored Probabilities': 0.9345917698981047, 
                                         'ML3 Gearbox Fault Scored Labels': 1.0, 'ML3 Gearbox Fault Scored Probabilities': 0.9994189598215983}], 
                     'S12345ModelsOutput': [{'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9999298973353226, 
                                            'ML2 Bearing Fault Scored Labels': 1.0, 'ML2 Bearing Fault Scored Probabilities': 0.9995586735495678, 
                                            'ML3 Gearbox Fault Scored Labels': 1.0, 'ML3 Gearbox Fault Scored Probabilities': 0.959437785217065}], 
                     'S4ModelsOutput': [{'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9999983195822132, 
                                         'ML2 Bearing Fault Scored Labels': 1.0, 'ML2 Bearing Fault Scored Probabilities': 0.9965093015974997, 
                                        'ML3 Gearbox Fault Scored Labels': 1.0, 'ML3 Gearbox Fault Scored Probabilities': 0.9998034847355525}], 
                     'S5ModelsOutput': [{'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9971159222336053, 
                                         'ML2 Bearing Fault Scored Labels': 0.0, 'ML2 Bearing Fault Scored Probabilities': 0.00014449799626174535, 
                                         'ML3 Gearbox Fault Scored Labels': 0.0, 'ML3 Gearbox Fault Scored Probabilities': 0.0039150529813327724}]
                    }
        }
        '''
        predictionLogger.info(myJson)
        influxMsg = getInfluxMsgFz(myJson)
        '''
        PREDICITON RESULT FORMAT FOR INFLUXDB:
        [
        {'measurement': 'S2ModelsOutput', 'tags': {'Model': 'ML1'}, 'fields': {'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9934365970893647}},
        {'measurement': 'S2ModelsOutput', 'tags': {'Model': 'ML2'}, 'fields': {'ML2 Bearing Fault Scored Labels': 0.0, 'ML2 Bearing Fault Scored Probabilities': 7.790251381015847e-05}}, 
        {'measurement': 'S2ModelsOutput', 'tags': {'Model': 'ML3'}, 'fields': {'ML3 Gearbox Fault Scored Labels': 0.0, 'ML3 Gearbox Fault Scored Probabilities': 0.006167442709467959}}, 
        {'measurement': 'S3ModelsOutput', 'tags': {'Model': 'ML1'}, 'fields': {'ML1 Anomaly Scored Labels': 0.0, 'ML1 Anomaly Scored Probabilities': 0.003526396544994745}}, 
        {'measurement': 'S3ModelsOutput', 'tags': {'Model': 'ML2'}, 'fields': {'ML2 Bearing Fault Scored Labels': 0.0, 'ML2 Bearing Fault Scored Probabilities': 0.09611832145987317}}, 
        {'measurement': 'S3ModelsOutput', 'tags': {'Model': 'ML3'}, 'fields': {'ML3 Gearbox Fault Scored Labels': 0.0, 'ML3 Gearbox Fault Scored Probabilities': 6.396071431781235e-06}}, 
        {'measurement': 'S1ModelsOutput', 'tags': {'Model': 'ML1'}, 'fields': {'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9999811413264189}}, 
        {'measurement': 'S1ModelsOutput', 'tags': {'Model': 'ML2'}, 'fields': {'ML2 Bearing Fault Scored Labels': 1.0, 'ML2 Bearing Fault Scored Probabilities': 0.9345917698981047}}, 
        {'measurement': 'S1ModelsOutput', 'tags': {'Model': 'ML3'}, 'fields': {'ML3 Gearbox Fault Scored Labels': 1.0, 'ML3 Gearbox Fault Scored Probabilities': 0.9994189598215983}}, 
        {'measurement': 'S12345ModelsOutput', 'tags': {'Model': 'ML1'}, 'fields': {'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9999298973353226}}, 
        {'measurement': 'S12345ModelsOutput', 'tags': {'Model': 'ML2'}, 'fields': {'ML2 Bearing Fault Scored Labels': 1.0, 'ML2 Bearing Fault Scored Probabilities': 0.9995586735495678}}, 
        {'measurement': 'S12345ModelsOutput', 'tags': {'Model': 'ML3'}, 'fields': {'ML3 Gearbox Fault Scored Labels': 1.0, 'ML3 Gearbox Fault Scored Probabilities': 0.959437785217065}}, 
        {'measurement': 'S4ModelsOutput', 'tags': {'Model': 'ML1'}, 'fields': {'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9999983195822132}}, 
        {'measurement': 'S4ModelsOutput', 'tags': {'Model': 'ML2'}, 'fields': {'ML2 Bearing Fault Scored Labels': 1.0, 'ML2 Bearing Fault Scored Probabilities': 0.9965093015974997}}, 
        {'measurement': 'S4ModelsOutput', 'tags': {'Model': 'ML3'}, 'fields': {'ML3 Gearbox Fault Scored Labels': 1.0, 'ML3 Gearbox Fault Scored Probabilities': 0.9998034847355525}}, 
        {'measurement': 'S5ModelsOutput', 'tags': {'Model': 'ML1'}, 'fields': {'ML1 Anomaly Scored Labels': 1.0, 'ML1 Anomaly Scored Probabilities': 0.9971159222336053}}, 
        {'measurement': 'S5ModelsOutput', 'tags': {'Model': 'ML2'}, 'fields': {'ML2 Bearing Fault Scored Labels': 0.0, 'ML2 Bearing Fault Scored Probabilities': 0.00014449799626174535}}, 
        {'measurement': 'S5ModelsOutput', 'tags': {'Model': 'ML3'}, 'fields': {'ML3 Gearbox Fault Scored Labels': 0.0, 'ML3 Gearbox Fault Scored Probabilities': 0.0039150529813327724}}
        ]
        '''
        print('MSGJSON :', influxMsg)
        try:
            self.client.write_points(influxMsg)
        except Exception as err:
            print(err)
            raise ValueError('writeDbFz: {} error'.format(err))
        else:
            return 0



