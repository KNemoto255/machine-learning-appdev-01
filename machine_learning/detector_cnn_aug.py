"""
データ分類の精度（テスト精度）を改善させる方法を考える。
１、データ数を増やす
２、ハイパーパラメータ・アルゴリズムを見直す
３、モデルを見直す
"""

#データを学習・評価するためのモデルを定義する

import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50

My_epochs=100
My_validation_split=0.25
My_decoder_name = "Animal_Decoder_aug"
My_data_name = "npydata01_aug"

#メイン関数
def main():
    #allow_pickle=Trueをnpyデータを読む際は追加
    X_train, X_test, Y_train, Y_test = np.load("./" + My_data_name + ".npy",allow_pickle=True)

    #説明変数 - 値を標準化する
    X_train = X_train.astype("float") / 256
    X_test = X_test.astype("float") / 256

    #目的変数はワンホットベクター形式にする
    Y_train = np_utils.to_categorical(Y_train, num_classes)
    Y_test = np_utils.to_categorical(Y_test, num_classes)

    #学習を開始
    model = model_train(X_train, Y_train)
    #model_eval(model, X_test, Y_test)

#モデルの学習
def model_train(X,Y):

    model = Sequential()
    #一番最初の入力層には、モデルの画像サイズを使う
    #全結合をした後ドロップアウトすることで若干精度が向上する
    model.add(Conv2D(filters=32, kernel_size=(3,3), padding="same", input_shape=X.shape[1:]))
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

    #モデルをコンパイル + 損失関数を定義
    model.compile(loss = "categorical_crossentropy", optimizer="adam", metrics = ["accuracy"])

    #モデルを学習してフィッティングする
    model.fit(X, Y, batch_size=32, epochs=My_epochs, validation_split=My_validation_split)

    #学習したモデルを保存する
    model.save("./" + My_decoder_name + ".h5")

def model_eval(model, X, Y):

    scores = model.evaluate(X, Y, verbose = 1)
    print("更新された損失量", scores[0])
    print("テスト精度", scores[1])

if __name__ == "__main__":
    main()
