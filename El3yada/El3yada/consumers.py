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

from asgiref.sync import async_to_sync
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from urllib.parse import parse_qs

class AdminNotificationConsumer(WebsocketConsumer):
    def connect(self):
        query_params = parse_qs(self.scope['query_string'].decode('utf8'))
        token = query_params.get('token', [None])[0]
        
        is_val_admin = False
        if token:
            try:
                access_token = AccessToken(token)
                user = User.objects.get(id=access_token['user_id'])
                if user.is_staff or user.is_superuser:
                    is_val_admin = True
            except Exception:
                pass
                
        if is_val_admin:
            self.group_name = 'admin_alerts'
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def send_notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))