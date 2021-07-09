from django.db import models

class infection_manager(models.Manager):
    def latest_prefecture_data(self, prefecture_name):
        prefecture_obj = super().get_queryset().filter(name=prefecture_name).first()
        return super().get_queryset().filter(prefecture=prefecture_obj).order_by('date').last()
    
    def latest_prefecture_all_data(self):
        return super().get_queryset().objects.order_by('date').reverse()[:47]

    def region_prefecture_data(self, region_array):
        result = []
        for p in region_array:
            result.append(self.latest_prefecture_data(p.name))

        return result
