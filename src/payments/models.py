from django.db import models


class UserWithBalance(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    balance = models.IntegerField(default=0)
