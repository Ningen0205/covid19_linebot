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

from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FollowEvent,
    TemplateSendMessage,
    ButtonsTemplate,
    URIAction,
    ConfirmTemplate,
    PostbackAction,
    PostbackEvent,
    PostbackTemplateAction
)

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

# 変数の初期化
valid_check = True
items = None
user_message = None


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


# テキストメッセージが送信された時のハンドルイベント(メッセージを返すときも)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    # グローバル変数ということを宣言
    global items
    global valid_check
    global user_message

    # ユーザから送信されたメッセージの取得
    user_message = event.message.text
    
    # 送信されたテキストメッセージが地方名と同じ場合
    if prefecture.manager.check_region(user_message):
        region_data = prefecture.manager.get_region_data(user_message)
        items = [QuickReplyButton(action=MessageAction(label=f'{prefecture.name}', text=f'{prefecture.name}')) for prefecture in region_data]

        infection_region_data = infection.manager.latest_region_prefecture_data(region_data)
        region_sum = 0
        for prefecture_obj in infection_region_data:
            region_sum += prefecture_obj.infection
        
        # 地方の感染者数を返す
        messages = [TextSendMessage(text=f"{infection_region_data[0].date_string}　{user_message}の合計感染者は{region_sum}人でした。"), confirm()]
        valid_check = True
        line_bot_api.reply_message(event.reply_token, messages=messages)


    # 地方名ではなく県名だった場合
    elif prefecture.manager.check_prefecture(user_message):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=create_message(user_message))
        )

    # 地方名でも県名でもない場合
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='地方または都道府県の名前を正しく入力してください')
        )


# 確認テンプレート
def confirm():
    global user_message
    confirm_template_massage = TemplateSendMessage(
        # ここを変更すればlineで通知される文字が変更される
        alt_text='メッセージを選択してください',
        template=ConfirmTemplate(
            text=user_message+'の県ごとの感染者数が知りたい場合はYESをタップしてください。',
            # actionの中身は必ず二つだけ
            actions=[
                PostbackAction(
                    # labelが押したときに送信される文字
                    label='YES',
                    data='yes'
                ),
                PostbackAction(
                    label='NO',
                    data='no'
                )                                 
            ]
        )
    )
    return confirm_template_massage




# ポストバックアクションが送信されたときのハンドルイベント
@handler.add(PostbackEvent)
def handle_postback(event):

    # グローバル変数ということを宣言
    global items
    global valid_check


    # 確認メッセージが地方名が送られた後、一回目なら処理を行う
    if valid_check == True:

        # ポストバックアクションのdataの中身がyesならクイックリプライ
        if event.postback.data=='yes':
            message = TextSendMessage(text="感染者数を知りたい県のボタンをタップしてください。", quick_reply=QuickReply(items=items))
            line_bot_api.reply_message(event.reply_token, messages=message)

        elif event.postback.data=='no':
            # noが選択された場合はitemsの中身を削除
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='NOを選択しました。')
            )
        
        # 使用した変数の初期化
        items = None
        valid_check = False
    



