from django.contrib.admin.helpers import AdminReadonlyField
from selenium import webdriver
from bs4 import BeautifulSoup
import chromedriver_binary
import json
import collections as cl

# -----------------------------

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

# -----------------------------------------------

def put_jsondata(result):
  # jsonに書き出し
  with open('./today_covid19.json', 'w',encoding="utf-8") as f:
      json.dump(result, f, ensure_ascii=False, indent=2)

# -----------------------------------------------

# データベースに書き出す処理
def covid19_add_database(result):
  # infection.objects.create() 
	return False



# -----------------------------------------------

# ここがメインでほかの関数を呼び出してる
def main():
  
  result = get_scraping()
  #covid19_add_database(result)
  put_jsondata(result)

if __name__ == '__main__':
  main()