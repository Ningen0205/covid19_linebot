import sys

# message.pyをimportするために、親ディレクトリへ移動
sys.path.append('../')
from manager.message import send_message

def run():
    send_message()