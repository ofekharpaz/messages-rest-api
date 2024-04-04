from django.db import models

class Message(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    message = models.TextField()
    subject = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        app_label = 'messages'
