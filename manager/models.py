from django.db import models
from django.db.models.fields import CharField, DateField

class infection(models.Model):
    # prefecture_id = models.IntegerField(null=True)
    prefecture = models.ForeignKey("prefecture",null=True,on_delete=models.CASCADE)
    infection = models.IntegerField()
    date_string = models.CharField(max_length=100,default="no_value")
    date = models.DateTimeField(auto_now_add=True)

class prefecture(models.Model):
    name = models.CharField(max_length=100)