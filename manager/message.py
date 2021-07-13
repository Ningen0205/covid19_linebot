import os
from os.path import join, dirname

from .models import infection, prefecture

from linebot import LineBotApi
from linebot.models import TextSendMessage


from dotenv import load_dotenv

# .envに格納されている、アクセストークンを取得
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


def create_message_header():
    return f'{infection.manager.latest_date_time()}の感染者数を報告します \n'

def create_message_body(target, message=''):
    if prefecture.manager.check_region(target):
        # 地方のDBレコードを配列として取得
        region_data = prefecture.manager.get_region_data(target)
        infection_array = infection.manager.latest_region_prefecture_data(region_data)

        # メッセージの作成
        for i in infection_array:
            message += f'{i.prefecture.name}:{i.infection} \n'

    elif prefecture.manager.check_prefecture(target):
        # 最新の都道府県の情報を取得
        prefecture_obj = prefecture.manager.get_prefecture_data(target)
        latest_infection_data = infection.manager.latest_prefecture_data(prefecture_obj=prefecture_obj)
        message += f'{latest_infection_data.prefecture.name}:{latest_infection_data.infection}'
    elif target == '全国':
        # 最新47都道府県の情報を取得
        japan_infection_data = infection.manager.latest_prefecture_all_data()
        for i in reversed(japan_infection_data):
            message += f'{i.prefecture.name}:{i.infection} \n'
    
    else:
        message = '都道府県を正しく入力してください。'
    
    return message

def create_message(target):
    message = create_message_header()
    message = create_message_body(target, message)

    return message

def send_message(target='全国'):
    line_bot_api = LineBotApi(ACCESS_TOKEN)
    
    message = create_message(target)
    line_bot_api.broadcast(TextSendMessage(text=message))
