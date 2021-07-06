# django
from django.shortcuts import render
from django.http import HttpResponse
from .models import infection,prefecture
from .scraping import get_scraping

# json
import json
from collections import OrderedDict

# linebot関連
from linebot import LineBotApi
from linebot.models import TextSendMessage

# .env関連
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Load .env
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

# Create your views here.
def index(request):
    line_bot_api = LineBotApi(ACCESS_TOKEN)

    infections = infection.objects.all().order_by('id')
    

    t = infection.objects.order_by('id').reverse()
    t = t[:47]
    message = f'{t[46].date_string}時点の感染者数を報告します。 \n'

    sum_infection = 0
    for i in range(46,-1,-1):
        message += f'{t[i].prefecture.name}:{t[i].infection} \n'
        sum_infection += t[i].infection
    # print(t[1].infection)
    
    message += f'本日の合計感染者数は{sum_infection}人でした。'
    line_bot_api.broadcast(TextSendMessage(text=message))
    return HttpResponse('メッセージ送信したよ')
    

    # return render(request, './manager/template.html', {'infections':infections})

def webhook(request):
    return HttpResponse('test')
