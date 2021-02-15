from django.db import models

from django.contrib.auth.models import User

def path(instance, filename) -> str:
    return "{0}/profile/{1}".format(instance.user.username, filename)

class UserProfileImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=path, default='ig-default-user.png')