import datetime
from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=200, null=False)
    lastName = models.CharField(max_length=200, null=False)

    def __str__(self):
        """
         defines doctor full name

        Returns:
            Name and surname
        """
        return self.firstName + ' ' + self.lastName 

class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='doctor')
    firstName = models.CharField(max_length=200, null=False)
    lastName = models.CharField(max_length=200, null=False)


    def __str__(self):
        """
        defines doctor full name

        Returns:
            Name and surname
        """
        return self.firstName + ' ' + self.lastName 



class Notification(models.Model):
    doctor =  models.ForeignKey(Doctor, null=True, on_delete=models.SET_NULL) #one-to-many relationship
    patient = models.ForeignKey(Patient, null=False, on_delete=models.DO_NOTHING) #one-to-many relationship
    topic = models.CharField(max_length=200, null=False)
    message = models.CharField(max_length=200, null=False)
    sendByEmail = models.BooleanField(null=False, default=False)
    isSentByEmail = models.BooleanField(null=True, default=False)
    isSent = models.BooleanField(null=True, default=False)
    createdAtDate = models.DateTimeField(auto_now_add=True, null=False)
    plannedOnDate = models.DateTimeField(null=False, default=datetime.datetime.now)
    

