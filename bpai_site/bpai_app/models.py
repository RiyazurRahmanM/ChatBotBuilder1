from django.db import models

# Create your models here.
class Messages(models.Model):
    input_message = models.CharField(max_length=1000,default="NULL")
    output_message = models.CharField(max_length=1000,default="NULL")
    system_message = models.CharField(max_length=100,default="NULL")
    chatbot_name = models.CharField(max_length=100,default="NULL")
    initial_message = models.CharField(max_length=100,default="NULL")
    