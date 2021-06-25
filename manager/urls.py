from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scraping',views.scraping,name='scraping'),
    path('test',views.test,name='test'),
    path('webhook',views.webhook,name='webhook'),
]