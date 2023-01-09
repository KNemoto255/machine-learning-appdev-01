"""
作成したモデルから逆に予測を行うコード。
害獣か否かをテスト精度と同じ制度で判定できる

import os, glob
import numpy as np
"""
#PIL、SKLearnを使ってデータを変換する
from PIL import Image
import os, time, sys

import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
from keras.optimize import adam

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50

My_decoder_name = "Animal_Decoder_aug"
My_data_name = "npydata01_aug"
My_input_shape = (50, 50, 3)


#予測に使うモデル → 学習に使ったモデルと全く同じ定義でOK。入力するテンソルのみ引数を変える
def build_model():
        model = Sequential()

        #一番最初の入力層には、モデルの画像サイズを使う
        #全結合をした後ドロップアウトすることで若干精度が向上する
        model.add(Conv2D(filters=32, kernel_size=(3,3), padding="same", input_shape=My_input_shape))
        model.add(Activation("relu"))
        model.add(Conv2D(filters=32, kernel_size=(3,3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(filters=64, kernel_size=(3,3),padding="same", input_shape=X.shape[1:]))
        model.add(Activation("relu"))
        model.add(Conv2D(filters=64, kernel_size=(3,3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2,2)))
        model.add(Dropout(0.25))

        #全結合層に入力するため、Flattenレイヤーで4階テンソルとなっている出力値を2階テンソルに直す
        model.add(Flatten())

        #全結合層
        model.add(Dense(units=512))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))
        model.add(Dense(units=3))
        model.add(Activation("softmax"))
        model.output_shape

        #モデルをコンパイル + 損失関数・最適化関数を定義
        model.compile(loss = "categorical_crossentropy", optimizer="adam", metrics = ["accuracy"])

        #学習したモデルをロードする
        model = load_model("./" + My_decoder_name + ".h5")

        return model

#メイン関数 - 任意のイメージがどの物体化を予測する
def main():
    image = Image.open(sys.argv[1])
    image = image.convert("RGB")
    image = image.resize((image_size,image_size))
    data = np.asarray(image)

    X = []
    X.append(data)
    X = np.array(X)
    model = build_model()

    result = model.predict([X])[0]
    predicted = result.argmax()
    percentage = int(result[predicted] * 100)
    print(result)
    print("Object is {0}, with {1} probability.".format(classes[predicted], percentage))

if __name == "__main__":
    main()
