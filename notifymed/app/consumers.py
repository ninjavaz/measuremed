from asyncio import SendfileNotAvailableError
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        """
        enables a connection to a channel group
        """

        user = self.scope['user']
        print(type(user.username))
        self.room_group_name = user.username
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
   
    def disconnect(self, close_code):
        """
        Enables a disconnection from a channel group

        Args:
            close_code 
        """
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        """
        Enables receiving notifications from doctor to patient

        Args:
            text_data 
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        topic = text_data_json['topic']
        plannedOnDate = text_data_json['plannedOnDate']
        doctorFullName = text_data_json['doctorFullName']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "sendNotification",
                "topic": topic,
                "message": message,
                "plannedOnDate": plannedOnDate,
                "doctorFullName": doctorFullName
            },
        )

    def sendNotification(self, event):
        """
        Enables sending notifications by doctor

        Args:
            event _
        """
        message = event['message']
        topic = event['topic']
        plannedOnDate = event['plannedOnDate']
        doctorFullName = event['doctorFullName']

        self.send(text_data=json.dumps(
            {
                "type":"notification",
                "topic": topic,
                "message": message,
                "plannedOnDate": plannedOnDate,
                "doctorFullName": doctorFullName
            }
        ))


