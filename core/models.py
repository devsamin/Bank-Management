from django.db import models

# Create your models here.

class Bank(models.Model):
    name = models.CharField(max_length=22)
    status = models.BooleanField(default=False)
    is_bankrupt = models.BooleanField(default=False)

    def __str__(self):
        return self.name