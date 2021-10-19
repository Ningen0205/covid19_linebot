from manager.models import infection, prefecture

def run():
    infection.objects.filter(id__lte=8000).delete()