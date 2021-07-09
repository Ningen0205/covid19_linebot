import os

# linebot関連
from linebot import LineBotApi
from linebot.models import TextSendMessage

# django.models
from manager.models import infection

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

def run():
    line_bot_api = LineBotApi(ACCESS_TOKEN)

    #　idが高い順番(最新情報)に並び替えして47件を取得(47都道府県)
    infections = infection.objects.order_by('date').reverse()
    infections = infections[:47]
    
    message = f'{infections[46].date_string}時点の感染者数を報告します。 \n'

    sum_infection = 0
    for i in range(46,-1,-1):
        message += f'{infections[i].prefecture.name}:{infections[i].infection} \n'
        sum_infection += infections[i].infection
    
    message += f'本日の合計感染者数は{sum_infection}人でした。'
    line_bot_api.broadcast(TextSendMessage(text=message))