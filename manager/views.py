# django
from django.shortcuts import render
from django.http import HttpResponseForbidden,HttpResponse
from linebot.models.actions import MessageAction
from linebot.models.send_messages import QuickReply, QuickReplyButton
from .models import infection,prefecture

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

        messages = TextSendMessage(text="県ごとの感染者数が知りたい場合は下のボタンをタップしてください。", quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='地方の名前を正しく入力してください')
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

# 友達追加した際のイベントを仮組で追加
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='追加してくれてありがとう!')
    )
