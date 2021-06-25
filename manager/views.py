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

def scraping(request):
    def render_json_response(request, data, status=None):
        """response を JSON で返却"""
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        callback = request.GET.get('callback')
        if not callback:
            callback = request.POST.get('callback')  # POSTでJSONPの場合
        if callback:
            json_str = "%s(%s)" % (callback, json_str)
            response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=status)
        else:
            response = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
        return response

    r = get_scraping()
    for i in range(1,47,1):
        infection.objects.create(prefecture_id=i,infection=r["masculine_people"][i])
    
    return render_json_response(request,r)

# スクレイピングしてDBに保存
def test(request):
    r = get_scraping()
    i = 0

    date = ''
    for key,val in r.items():
        i += 1
        if i == 1:
            date = val
            # 更新日時情報
            continue
        else:
            j = 1
            for p,n in val.items():
                obj = prefecture.objects.filter(id=j).first()
                infection.objects.create(prefecture=obj,infection=n,date_string=date)
                j += 1
    
    return HttpResponse('成功')

def webhook(request):
    return HttpResponse('test')

def init_database(request):
    prefecture_list = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県",
"茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
"新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県",
"静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県",
"奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県",
"徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県",
"熊本県","大分県","宮崎県","鹿児島県","沖縄県"
    ] 
    for i in range(0,47,1):
        prefecture.objects.get_or_create(name=prefecture_list[i])
    
    return HttpResponse('初期化したよ')