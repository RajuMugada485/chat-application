from django.db import models
class User(models.Model):
    user_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mail=models.EmailField()
    password=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    secret=models.CharField(max_length=3)
class Conversation(models.Model):
    conversation_id=models.IntegerField(primary_key=True)
    message_count=models.BigIntegerField(default=0)
    group_members=models.ManyToManyField(User,through='Group')
class Group(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    conversation=models.ForeignKey(Conversation,on_delete=models.CASCADE,null=True)
    conversation_name=models.CharField(max_length=100)
    joined_datetime=models.DateTimeField(auto_now_add=True)
    left_datatime=models.DateTimeField(null=True)
class Message(models.Model):
    conversation=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    from_user=models.CharField(max_length=100)
    text=models.CharField(max_length=500)
    sent_datetime=models.DateTimeField(auto_now_add=True)