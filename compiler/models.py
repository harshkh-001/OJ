from django.db import models
import uuid
from accounts.models import User
from ojapp.models import Problems

class Compilers(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    lang = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4 , editable=False, unique=True)
    sub_time = models.DateTimeField(auto_now_add=True)
    message = models.TextField(default="Empty")
    status = models.BooleanField()
    
    def __str__(self):
        return f"{self.user.username} - {self.lang} - {self.sub_time}"