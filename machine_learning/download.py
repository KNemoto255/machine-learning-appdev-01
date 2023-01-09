from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

#APIキーの情報を入力

key = "5cbe8ad61a207659b9ea39a367fed2a0"
secret = "e563ea2aa86ae449"
wait_time = 0.5
amount = 100
objectname = "ass"

savedir = "object_images/" + objectname

flickr = FlickrAPI(key, secret, format = "parsed-json")
result = flickr.photos.search(
    text = animalname,
    per_page = amount,
    media = "photos",
    sort = "relevance",

    #１はセーフ状態、3がレストリクトを表す
    #safe_seach = 1,
    safe_seach = 3,
    #extras = "url_q, licence"
    extras = "url_o, licence"
)


photos = result["photos"]
#pprint(photos)

#シークエント演算でphotoのデータを取り出す
#per_pageに指定した数だけ画像がスクレイピングされる
for i,photo in enumerate(photos["photo"]):

    #スクレイピングした画像を.jpg方式で保存する
    #url_q = photo["url_q"]
    url_q = photo["url_o"]
    filepath = savedir + "/" + photo["id"] + ".jpg"

    #ファイルが存在するかフェイルセーフする
    if os.path.exists(filepath): continue
    urlretrieve(url_q)
    time.sleep(wait_time)
