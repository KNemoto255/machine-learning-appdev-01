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

X = []
Y = []


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

        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

#データを学習用・テスト用に分割
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
xy = (X_train, X_test, Y_train, Y_test)
np.save("./npydata.npy", xy)

#分割したデータセットの数を確認
len(X_train)
len(X_test)
len(Y_train)
len(Y_test)
