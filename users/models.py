from django.db import models

from core.models import TimeStamp

class User(TimeStamp):
    email        = models.CharField(max_length=100, unique=True)
    name         = models.CharField(max_length=100)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    nickname     = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'

class Address(TimeStamp):
    user    = models.ForeignKey("User", on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

    class Meta:
        db_table = 'addresses'