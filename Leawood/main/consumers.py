
from channels.generic.websocket import WebsocketConsumer
from  channels.consumer import SyncConsumer
import json

class DeviceConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("Recevied data {}".format(message))
        self.send(text_data=json.dumps({
            'message': message
        }))
        
        
class DeviceChannelConsumer(SyncConsumer):
	
	def test_print(self, message):
		print("Test {}".format( message["text"]))
        
