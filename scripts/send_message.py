import os
import sys

# linebot関連
from linebot import LineBotApi
from linebot.models import TextSendMessage

# django.models
from manager.models import infection

# message.pyをimportするために、親ディレクトリへ移動
sys.path.append('../')
from manager.message import send_message

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

def run():
    send_message()