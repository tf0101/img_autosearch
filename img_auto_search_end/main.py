from auto import storageandfication
from db import DB
import sys


if __name__ == '__main__':
    
    #コマンドラインから入力した引数
    args = sys.argv
    print(type(args[1]),args[1])
    
    #例外処理
    if args[1]!='manual' and args[1]!='auto':
        print("manual or auto plz")
        sys.exit()

    
    #保存分類処理のインスタンス生成
    activate=storageandfication()
    print("保存分類インスタンス生成")
    
    #データベースインスタンス生成
    db_userid_list=DB()
    print("dbインスタンス生成")
    

    #manual:新しいユーザーの画像を保存したい時、人間が入力することを想定
    #auto:既存ユーザーの画像を自動で取得、タスクスケジューラなどで画像を自動収集する。システムの自立入力として想定
    if args[1]=='manual':
        print("手動処理")
        Account=input("Account:@")#画像を取りたいユーザーのアカウント名入力
        activate.mainprosesing(Account)#手動の場合の処理
        db_userid_list.dbclose()#処理が終わったらDBを閉じる
    elif args[1]=='auto':
        print("自動処理")
        #自動処理の場合はDBからユーザーidリストを作りauto.pyの処理をループする
        userlist=db_userid_list.dbuserid()#ユーザーidリスト
        print(type(userlist))
        print(userlist)
        
        #保存分類処理ループ
        for user in userlist:
            print(type(user),user)
            activate.mainprosesing(user)


        db_userid_list.dbclose()#処理が終わったらDBを閉じる
        


