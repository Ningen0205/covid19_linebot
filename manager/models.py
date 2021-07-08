from django.db import models
from django.db.models.fields import CharField, DateField

class infection(models.Model):
    # prefecture_id = models.IntegerField(null=True)
    prefecture = models.ForeignKey("prefecture",null=True,on_delete=models.CASCADE)
    infection = models.IntegerField()
    date_string = models.CharField(max_length=100,default="no_value")
    date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def latest_all_infections(cls):
        return cls.objects.order_by('date').reverse()[:47]
    
    @classmethod
    def latest_infection(cls, prefecture_name):
        pass

    @classmethod
    def check_messeage(cls, message):
        from .models import prefecture
        prefecture_obj = prefecture.objects.filter(name=message).first()

        if message == '全国':
            return cls.latest_all_infections()
        elif prefecture_obj != None:
            return cls.objects.filter(prefecture=prefecture_obj).order_by('date').last()
        else:
            return False

    @classmethod
    def create_message(cls):
        return 'てすとだよ'


class prefecture(models.Model):
    name = models.CharField(max_length=100)