import login
import datetime
import tweepy
from datetime import datetime as dt
from datetime import timedelta
import time
import requests
import shutil
import os
import sys
from model import Model
from db import DB


class storageandfication:
    
    #コンストラクタでインスタンス生成
    def __init__(self):
        self.modelset=Model()#モデルロードインスタンス生成
        self.dblord=DB()#db記録インスタンス生成





    #img保存メソッド
    def download_img(self,url,file_name):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)




    #自動保存分類メソッド
    def mainprosesing(self,Account):

        
        path='img/'+Account+'/' #保存先フォルダ
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)


        oldtime=self.dblord.dbmach(Account)#指定ユーザーidがDB内にある場合は前回の最新ツイートの日時を取得
        print("時間:"+str(oldtime))

        # timelineメソッドの一つである api.user_timeline()では１ページにつき最大２００ツイートしか取得できず、
        # 合計３２００ツイート、つまり最初のページから１６回しかページをめくれないようです。
        # そのページを数えるためリスト型を使っています。
        pages=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

        #ループ内での例外処理用のフラグ
        fasttweetflag=False
        timeflag=False 

        api=login.login("自分のユーザーID")#ログイン
        
        #画像を含むツイート取得するループ
        for page in pages:
            #Accountは検索するユーザID、countは１ページあたり取得するツイートの数（最大２００）、pageはページの番号
            tweets=api.user_timeline(Account, count=200, page=page)
            for tweet in tweets:
                try:

                    tweet.created_at+=timedelta(hours=9)#ツイート時間取得
                    print(tweet.created_at)
                    
                    
                    if tweet.created_at <= oldtime: #DB内に記録されている時間を下回ったらループ終了
                        print("roop_end")
                        timeflag=True
                        break

                    
                    if fasttweetflag==False: #一番最新のツイート時間をDBに記録しておくことで次のアクセスでの画像多重保存を防ぐ
                        print("dblogwrit")
                        self.dblord.dbmemo(Account,tweet.created_at)#ユーザー名と最新ツイート時間を渡す
                        fasttweetflag=True

                    
                    url=tweet.extended_entities['media'][0]['media_url']
                    tdatetime = dt.now()
                    filename=path+tdatetime.strftime('%Y%m%d%H%M%S')+'.jpg'  #"img"というサブフォルダに保存
                    self.download_img(url,filename)#取得したツイートの画像を保存
                    label=self.modelset.modellabel(filename)#取得した画像のラベルを返す
                   
                    #モデルのラベルがyesの時だけフォルダに保存、ラベルがnoの画像は削除
                    if label=='no':
                        os.remove(filename)#ファイル消去
                    else:
                        print("ラベル:yes")

                    time.sleep(1) #上書きされるので1秒待ってファイル名が変わるようにする
                except:
                    pass #画像がないときはなにもしない
            if timeflag:
                break      