from django.db import models

# Create your models here.

class Diary(models.Model):
    email = models.EmailField()