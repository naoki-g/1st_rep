import datetime
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--incognito')

# 環境に応じてchromedriver.exe格納パスを設定
driver = webdriver.Chrome(executable_path=r'C:\******\chromedriver.exe',
                            options=options)
driver.implicitly_wait(3)

url = 'https://www.myprotein.jp/'
driver.get(url)
sleep(2)

# 虫めがねマークを押して検索ボックスを表示
search_button = driver.find_element_by_css_selector('button.headerSearch_toggleForm')
search_button.click()

search_word = 'Impact ホエイ プロテイン'
search_flavor = 'ナチュラルチョコレート'

# 検索ボックスに検索ワードを入力して検索
search_box = driver.find_element_by_css_selector('input.headerSearch_input')
sleep(2)
search_box.send_keys(search_word)
sleep(2)
search_box.submit()
sleep(2)

# 検索結果からURLを取得
product_list = driver.find_elements_by_css_selector('li.productListProducts_product ')
product_url = ''
for product_block in product_list:
    product_title = product_block.find_element_by_css_selector('h3').text
    if product_title == search_word:
        product_url = product_block.find_element_by_css_selector('a.athenaProductBlock_linkImage').get_attribute('href')
        print(product_url)
        break

driver.get(product_url)
sleep(2)

# ドロップダウンからフレーバーを選択
dropdown = driver.find_element_by_id('athena-product-variation-dropdown-5')
select = Select(dropdown)
select.select_by_visible_text(search_flavor)
sleep(2)

# 選択中のフレーバーの容量選択肢を取得
product_size_bottons = driver.find_elements_by_css_selector('button.athenaProductVariations_box')

# 容量ごとの価格を取得する
# 2つ目以降のボタンクリック時にエラーとなるため1ボタン押下ごとにリフレッシュする
d_list = []
for i, _ in enumerate(product_size_bottons):
    
    # ドロップダウンからフレーバーを選択
    dropdown = driver.find_element_by_id('athena-product-variation-dropdown-5')
    select = Select(dropdown)
    select.select_by_visible_text(search_flavor)
    sleep(2)

    # 選択中のフレーバーの容量選択肢を取得
    size_bottons = driver.find_elements_by_css_selector('button.athenaProductVariations_box')
    size_bottons[i].click()
    product_size = size_bottons[i].text
    sleep(2)
    product_container = driver.find_element_by_css_selector('div.athenaProductPage_productDetailsContainer')
    product_price = product_container.find_element_by_css_selector('p.productPrice_price ').text
    
    d_list.append({
        'product_size':product_size,
        'product_price':product_price
    })

    driver.refresh()
    sleep(2)

# 取得結果をcsv出力
df = pd.DataFrame(d_list)
list_filename = str(datetime.date.today()) + '_myprotein.csv'
df.to_csv(list_filename, index=None, encoding='utf-8-sig')

driver.quit()