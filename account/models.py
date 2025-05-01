from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=10)
    address = models.CharField(max_length = 150)
    password = models.CharField(max_length = 150)

    def __str__(self) -> str:
        return self.username
    