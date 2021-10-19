from manager.models import infection, prefecture

def run():
    infection.objects.filter(id__gt=8000).delete()