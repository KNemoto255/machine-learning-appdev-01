"""
コマンドプロンプトで以下のコードを実行することで、ローカルWEBサーバー上でFlaskが起動する
コマンドプロンプトの他にも、PyCharmで環境構築することでFlaskを実行できる

cd C:\Users\user\Desktop\AI_ML_Learning\画像判定AIアプリ開発・パート1
set FLASK_APP=flask_hello.py

flask run

Flaskが起動したら、以下のリンクにアクセスする
http://127.0.0.1:5000

"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    hello = "Hello world"
    return hello

if __name__ == "__main__":
    app.run()
