# django
from manager.infection_manager import infection_manager
from django.shortcuts import render
from django.http import HttpResponseForbidden,HttpResponse
from linebot.models.actions import MessageAction
from linebot.models.send_messages import QuickReply, QuickReplyButton
from .models import infection,prefecture

from django.shortcuts import render

#csrf無効化
from django.views.decorators.csrf import csrf_exempt

# linebot関連
from linebot import LineBotApi,WebhookHandler
from linebot.models import MessageEvent,TextMessage,TextSendMessage,FollowEvent,TemplateSendMessage,ButtonsTemplate,URIAction

# .env関連
import os
from os.path import join, dirname
from dotenv import load_dotenv

# error関連
from linebot.exceptions import InvalidSignatureError

# message.py
from .message import *

# Load .env
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

def index(request):
    return render(request, 'template.html')
@csrf_exempt
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

    return HttpResponse('送信完了')


# テキストメッセージが送信された時のハンドルイベント
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if prefecture.manager.check_region(user_message):
        region_data = prefecture.manager.get_region_data(user_message)
        items = [QuickReplyButton(action=MessageAction(label=f'{prefecture.name}', text=f'{prefecture.name}')) for prefecture in region_data]

        infection_region_data = infection.manager.latest_region_prefecture_data(region_data)
        region_sum = 0
        for prefecture_obj in infection_region_data:
            region_sum += prefecture_obj.infection

        messages = TextSendMessage(text=f"{infection_region_data[0].date_string}　{user_message}の合計感染者は、{region_sum}人でした。\n県ごとの感染者数が知りたい場合は下のボタンをタップしてください。", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
    elif prefecture.manager.check_prefecture(user_message):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=create_message(user_message))
        )
    
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='地方または都道府県の名前を正しく入力してください')
        )
    # reply_text = create_message(event.message.text)

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=reply_text)
    # )
    
# def make_button_template():
#     message_template = TemplateSendMessage(
#         alt_text="にゃーん",
#         template=ButtonsTemplate(
#             text="どこに表示されるかな？",
#             title="タイトルですよ",
#             image_size="cover",
#             thumbnail_image_url="https://example.com/gazou.jpg",
#         )
#     )
#     return message_template

# @handler.add(MessageEvent, message=TextMessage)
# def handle_image_message(event):
#     messages = make_button_template()
#     line_bot_api.reply_message(
#         event.reply_token,
#         messages
#     )
