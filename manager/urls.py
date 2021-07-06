from django.urls import path

from . import views

# path(webのURLの後ろにどの文字が書いてあるか,viewsの中のどの関数を実行するか,name)
urlpatterns = [
    path('webhook',views.webhook,name='webhook'),

]