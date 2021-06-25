from django.db import models
from django.db.models.fields import CharField, DateField

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey("User",on_delete=models.CASCADE)
    title = models.CharField(max_length=100,default="notitle")
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True,null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class User(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True,null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class infection(models.Model):
    # prefecture_id = models.IntegerField(null=True)
    prefecture = models.ForeignKey("prefecture",null=True,on_delete=models.CASCADE)
    infection = models.IntegerField()
    date_string = models.CharField(max_length=100,default="no_value")
    date = models.DateTimeField(auto_now_add=True)

class prefecture(models.Model):
    name = models.CharField(max_length=100)