
# スクレイピング関連
from selenium import webdriver
import chromedriver_binary
from bs4 import BeautifulSoup

# 順序がある辞書を作成
import collections as cl
import json

# model
from manager.models import infection, prefecture

def get_scraping():
  # ドライバーをUIなしで使用するための設定
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-gpu')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--log-level=0')
  driver = webdriver.Chrome('chromedriver',options=options)
  driver.implicitly_wait(10)
  url = 'https://mainichi.jp/covid19'

  driver.get(url)
  html = driver.page_source.encode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')

  # 更新日時部分をスクレイピングしてる
  data = soup.find('g', { 'id' : 'mc1'}).text
  updated_time = soup.findAll('span', { 'class' : 'title-block-note'})[1].text

  print(updated_time)

  # 変数の初期化
  result = cl.OrderedDict()
  result["updated_time"] = updated_time
  result["masculine_people"] = cl.OrderedDict()

  # 実際にデータを取得している
  for i in range(1,48,1):
    prefecture_data = soup.find('g', { 'id' : f'mc{i}'}).text.split()
    
    prefecture = prefecture_data[0]
    prefecture_num = int(prefecture_data[1])

    result['masculine_people'][prefecture] = prefecture_num
  
  return result

def run():
    r = get_scraping()
    i = 0

    date = ''
    for key,val in r.items():
        i += 1
        if i == 1:
            date = val
            # 更新日時情報
            continue
        else:
            j = 1
            for p,n in val.items():
                obj = prefecture.objects.filter(id=j).first()
                infection.objects.create(prefecture=obj,infection=n,date_string=date)
                j += 1
    
    print('スクレイピング終了')