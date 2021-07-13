from django.db import models

class infection_manager(models.Manager):

    def latest_date_time(self):
        return super().get_queryset().order_by('date').reverse()[0].date_string
    
    def latest_prefecture_data(self, prefecture_obj):
        return super().get_queryset().filter(prefecture=prefecture_obj).order_by('date').last()
    
    def latest_prefecture_all_data(self):
        return super().get_queryset().order_by('date').reverse()[:47]

    def latest_region_prefecture_data(self, region_array):
        result = []
        for p in region_array:
            result.append(self.latest_prefecture_data(p))

        return result
