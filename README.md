# 使用方法

git clone https://github.com/Ningen0205/covid19_linebot.git  
pip install -r requirements.txt  
python manage.py migrate  
python manage.py runscript init_database  
python manage.py runscript scraping  

python manage.py runserver  

# 概要
[毎日新聞社](https://mainichi.jp/covid19)のサイトにある1日における感染者数を取得して返信するラインボットです。
