import json
from channels.generic.websocket import WebsocketConsumer

class testConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'hello'
            
        }))
        
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        self.send(text_data=json.dumps({
            'type':'message',
            'message':f'{user}, You go to hell!'
            
        }))
        
        print(f'Message from {user} : "{message}"')