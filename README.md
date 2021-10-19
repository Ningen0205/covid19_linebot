# 初期のセットアップ
※秘匿情報の登録は省略しています。

git clone https://github.com/Ningen0205/covid19_linebot.git  
pip install -r requirements.txt  
local_settings_example.pyをコピーしてlocal_settings.pyを作成。
.env.exampleをコピーして.envを作成（アクセストークンなどは書き換えてください。)
python manage.py migrate  
python manage.py runscript init_database  
python manage.py runscript scraping  

python manage.py runserver  

# 概要
[毎日新聞社](https://mainichi.jp/covid19)のサイトにある1日における感染者数を取得して返信するラインボットです。


プラットフォームとしてHerokuを使用し、Python(Django)でスクレイピングし、Lineメッセージとして送信する機能があるリポジトリです。

# 利用方法
秘匿情報の登録(.envに記載か環境変数に登録)や、データベースのマイグレーションを完了していることが前提です。  
python manage.py runscript scraping を実行すると、毎日新聞社のコロナ情報のページから情報をスクレイピングしてDBに格納します。  
python manage.py runscript send_message　を実行するとLineメッセージとして、取得している最新の感染者数を全員に送信します。  
