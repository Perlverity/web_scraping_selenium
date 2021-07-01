# 必要なライブラリのインポート
import os
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request

# 1枚の画像を保存する関数


def save_img(url, file_path):
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        urllib.request.urlretrieve(url, file_path)
        # print(url)

# 複数の画像のダウンロードを行う関数


def download_imgs(img_urls, save_dir):
    for i, url in enumerate(img_urls):
        file_name = f"{i}.jpg"  # 画像ファイル名
        save_img_path = os.path.join(save_dir, file_name)  # 保存パス

        save_img(url, save_img_path)  # 画像の保存

        if (i + 1) % 10 == 0 or (i + 1) == len(img_urls):
            print(f"{i + 1} / {len(img_urls)} done")


# word = "レム"  # 検索するワード
save_dir = "./images/no-copyright-girl"  # スクレイピングした画像を保存するディレクトリパス

# ディレクトリが存在しなければ作成する
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Webdriverの設定
options = Options()
options.add_argument('--headless')   # UI無しで操作する
driver = webdriver.Chrome(options=options)  # WebDriverのパスを設定

# yahoo画像へアクセス
url = "https://fromtheasia.com/illustration/2020-2021"
driver.get(url)  # 指定したURLへアクセス

urls = []  # 画像URLを格納するリスト

# 止まるまでスクロールする
while True:
    prev_html = driver.page_source  # スクロール前のソースコード
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")  # 最下部までスクロール
    sleep(1.0)   # 1秒待機
    current_html = driver.page_source  # スクロール後のソースコード

    # スクロールの前後で変化が無ければループを抜ける
    if prev_html != current_html:
        prev_html = current_html
    else:
        # 「もっと見る」ボタンがあればクリック
        try:
            button = driver.find_element_by_class_name("sw-Button")
            button.click()
        except:
            break

# 画像タグをすべて取得
elements = driver.find_elements_by_tag_name("img")
# print(elements)
# すべての画像URLを抜き出す
for elem in elements:
    url = elem.get_attribute("src")
    print(url)
    if url not in urls:
        urls.append(url)  # urlをリストに追加する

# print(urls)
driver.close()   # driverをクローズする
download_imgs(urls, save_dir)   # 画像をダウンロードする
