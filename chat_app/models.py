from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    chat_id = models.CharField(max_length=500)
    user1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    user2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='receiver')
    # message = models.ManyToManyField(Message)

    def __str__(self):
        return f'{self.chat_id}'


class Message(models.Model):
    text = models.CharField(max_length=500)
    user_sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender_message', default=None)
    date_posted = models.DateTimeField(auto_now_add=True)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        return f'{self.user_sender}: <{self.text}>'
