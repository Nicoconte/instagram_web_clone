from django.db import models

from django.contrib.auth.models import User

# Create your models here.

#Cuando un usuario se registra, podemos decir que hay un nueva en la plataforma
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Follower(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE) # La otra persona como cuenta obtiene
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Un usuario (Seguidos)

    def __str__(self):
        return f"La cuenta {self.user.username} comenzo a seguir a {self.account.user.username}"