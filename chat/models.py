from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    system_prompt = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    presence_penalty = models.FloatField()
    top_p = models.FloatField()
    max_tokens = models.IntegerField()
    is_active = models.BooleanField(default=True)

class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    roles = {
        "user": "user",
        "assistant": "assistant"
    }
    role = models.CharField(max_length=50, choices=roles)
    index = models.IntegerField(null=False)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    tokens = models.IntegerField()

class Requests(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    input_tokens = models.IntegerField(null=True, blank=True)
    output_tokens = models.IntegerField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)