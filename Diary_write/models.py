import datetime

from django.db import models


# Create your models here.


class Data(models.Model):
    diary_cnt = models.AutoField(primary_key=True)
    id = models.IntegerField()
    email = models.EmailField(max_length=255)
    content = models.CharField(max_length=500)
    edit_date = models.DateTimeField()
    write_date = models.DateTimeField(auto_now=True)
    diary_date = models.DateTimeField()
