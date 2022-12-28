from django.db.models import Q


import datetime

from .consumers import NotificationConsumer

from .models import Notification

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import pytz


def scheduleNotification(notificationId):
    """
    enables doctor to put a time in which notification should be received by specific patient
    
    Args:
        notificationId 
    """

    
    channel_layer = get_channel_layer()

    notification = Notification.objects.get(id=notificationId)

    print("notification")
    print(notification)

    print(str(notification.plannedOnDate))

    doctorFullName = notification.doctor.firstName + ' ' + notification.doctor.lastName
    plannedOnDate = notification.plannedOnDate.astimezone(pytz.timezone('Europe/Warsaw')).strftime("%m-%d-%Y, %H:%M:%S")
    userGroup = notification.patient.user.username

    async_to_sync(channel_layer.group_send)(
            userGroup,
            {
                "type":"sendNotification",
                "topic": notification.topic,
                "message": notification.message,
                "plannedOnDate": plannedOnDate,
                "doctorFullName": doctorFullName
            }
        )



