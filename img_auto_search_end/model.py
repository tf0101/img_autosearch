from keras.preprocessing import image
import numpy as np
import sys
from PIL import Image
from keras.models import model_from_json

class Model:
    
    #コンストラクタでモデルのロードを行う
    def __init__(self):
        #モデルファイル名
        model_filename='yes_no'
        #分類するクラス
        self.classes = ['no','yes']
        # モデルロード
        self.model = model_from_json(open(model_filename+'.json').read())
        self.model.load_weights(model_filename+'.h5')




    #取得画像を前処理し、読み込んだモデルでラベル(yes or no)を予測し返すメソッド
    def modellabel(self,filename):
        #入力画像の前処理
        img = image.load_img(filename, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        #学習時に正規化してるので、ここでも正規化
        x = x / 255
        #predict:入力サンプルに対する予測値の出力生成
        pred = self.model.predict(x)[0]

        #モデルのラベルを表示
        top = 1
        top_indices = pred.argsort()[-top:][::-1]
        result = [(self.classes[i], pred[i]) for i in top_indices]
        print(filename+':====>'+result[0][0])

        return result[0][0]