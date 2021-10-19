from flask import current_app

from azure.iot.device import IoTHubDeviceClient, Message
import json



class AZ_MQTT:
    def __init__(self):
        with current_app.app_context():
            connectionString = current_app.config['CONNECTION_STRING']
            print(connectionString)
            self.client = IoTHubDeviceClient.create_from_connection_string(connectionString)

    def send(self, msgList):
        msgString = json.dumps(msgList)
        msg = Message(msgString)
        print("Sending message: {}".format(msg))
        self.client.send_message(msg)
        #self.client.disconnect()
        self.client.shutdown()
        return 0
