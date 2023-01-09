"""
from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys
"""

#PIL、SKLearnを使ってデータを変換する
from PIL import Image
import os, glob
import numpy as np
from sklearn.model_selection import train_test_split

classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50
num_testdata = 100

X_train = []
X_test = []
Y_train = []
Y_test = []

#クラス数だけデータ変換の処理を繰り返す
for index, myclass in enumerate(classes):
    photos_dir = "object_images/" + myclass
    files = glob.glob(photos_dir + "/*.jpg")
    print(photos_dir)

#ファイルをNumpy形式に変換する
    for i, file in enumerate(files):
        if i >=300: break
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size,image_size))
        data = np.asarray(image)

        #最初に読み込んだデータはテストデータの方にアペンドする
        if i < num_testdata:
            X_test.append(data)
            Y_test.append(index)
        else:
            #学習データセットには、元画像を左右反転させたものを含める
            img_r = image.rotate(angle)
            data = np.asarray(img_r)
            X_train.append(data)
            Y_train.append(index)

            img_t = image.transpose(Image.FLIP_LEFT_RIGHT)
            data = np.asarray(img_t)
            X_train.append(data)
            Y_train.append(index)


X_train = np.array(X_train)
X_test = np.array(X_test)
Y_train = np.array(Y_train)
Y_test = np.array(Y_test)


#データを学習用・テスト用に分割
#X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
xy = (X_train, X_test, Y_train, Y_test)
np.save("./npydata01_aug.npy", xy)
