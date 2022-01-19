import datetime

from django.db import models


# Create your models here.


class Data(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.EmailField(max_length=255)
    content = models.CharField(max_length=500)
    edit_date = models.DateTimeField(auto_now=True)
    write_date = models.DateTimeField(auto_now=True)
    diary_date = models.DateTimeField(auto_now=True)
