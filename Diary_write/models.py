from django.db import models


# Create your models here.

class data(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255)
    content = models.CharField(max_length=500)
    date = models.DateField()
    writeDate = models.DateField(auto_now=True)
