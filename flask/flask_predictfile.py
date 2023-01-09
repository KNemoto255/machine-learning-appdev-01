#ファイル操作、フラスクのファイル操作やページのリダイレクトに必要な機能をインポートする
#secure_filenameには、SQLインジェクション等のハッキングを防ぐ機能をつけている
import os
from flask import Flask, request, redirect, url_for
from flask import flash
from werkzeug.utils import secure_filename

#Kerasと画像予測に必要なモジュールをインポート
import sys
import numpy as np
from PIL import Image

import tensorflow
import keras
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
#from tensorflow.keras.optimizers import Adam # - Works

#モデル
My_decoder_name = "Animal_Decoder_aug"
classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50

#アップロード先
UPLOAD_FOLDER = "./uploads"
ALLOWD_FILES = set(["png","jpg","gif"])


#Flaskの本体コード
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#キーをセットしないといけない仕様変更に対応
app.secret_key = "super secret key"

#拡張子がpng, jpg, gifかをチェックする
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWD_FILES

#ファイルをアップロードし、リダイレクトする処理

@app.route("/", methods = ["GET","POST"])

def upload_file():
    if request.method == "POST":
        #ファイルがアップロードされていない場合
        if "file" not in request.files:
            flash("ファイルが見つかりません")
            return redirect(request.url)

        file = request.files["file"]

        #ファイルネームが空欄の場合
        if file.filename == "":
            flash("ファイルが見つかりません")
            return redirect(request.url)

        #ファイルネームが拡張子チェックを通った場合
        #アップロードしたファイルはuploadsフォルダーに送信される
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            #送信した画像を読み込んだCNNモデルで分類・予測する
            #compile=Falseを追加しないと最適化関数の読み込みでエラーが起きる
            fliepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            model = load_model("./" + My_decoder_name + ".h5", compile=False)

            #読み込んだイメージをテンソルに変換
            image = Image.open(fliepath)
            image = image.convert("RGB")
            image = image.resize((image_size,image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            #モデルを使って予測 → 予測結果を返り値にする
            result = model.predict([X])[0]
            predicted = result.argmax()
            percentage = int(result[predicted] * 100)

            #return redirect(url_for("upload_file", filename=filename))
            return "Predict: " + classes[predicted] + " Percentage: " + str(percentage) + "%"

    return """
    <!doctype html>
    <html>
    <meta charset="UTF-8">
    <head>
    <title>File upload page</title>
    </head>
    <body>
    <h1>ファイルをアップロードして判定開始</h1>

    <form method = post enctype = multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload>
        </p>
    </form>

    </body>
    </html>
    """
