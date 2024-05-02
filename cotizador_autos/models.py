from django.db import models

# Create your models here.

class Modelos(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    clase = models.CharField(max_length=100)