# django
from django.shortcuts import render
from django.http import HttpResponseForbidden,HttpResponse
from .models import infection,prefecture
from .scraping import get_scraping

# json
import json
from collections import OrderedDict

# linebot関連
from linebot import LineBotApi,WebhookHandler
from linebot.models import MessageEvent, TextMessage,TextSendMessage

# .env関連
import os
from os.path import join, dirname
from dotenv import load_dotenv

# error関連
from linebot.exceptions import InvalidSignatureError

# Load .env
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Create your views here.
def index(request):
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

def webhook(request):
    # signatureの取得
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')

    try:
        # 署名の検証を行い、成功した場合にhandleされたメソッドを呼び出す
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        return HttpResponseForbidden()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


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
