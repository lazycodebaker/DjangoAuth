
from django.db import models
from django.contrib.auth.models import User

import uuid
import os

class UserModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    joined_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

