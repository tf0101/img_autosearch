import sqlite3
import datetime




class DB:

    #コンストラクタでDB接続
    def __init__(self):
        
        #データベースに接続する
        self.conn = sqlite3.connect('log.db')
        self.c = self.conn.cursor()

    

    #DB閉じるメソッド
    def dbclose(self):
        # データベースへのアクセスが終わったら close する
        self.conn.close()
    
    

    #DB内のユーザーIDリストを取得するメソッド
    def dbuserid(self):

        useridlist=[]#ユーザーidリスト
        #テーブルの存在確認
        cur = self.c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='users'")
        if cur.fetchone() == None: #テーブルが存在してない
            self.c.execute("CREATE TABLE users(name text, logtime datetime)")#テーブル生成
        else:
            for row in self.c.execute('SELECT * FROM users'):
                print(type(row[0]),row[0])
                useridlist.append(row[0])#リストにユーザーid追加

        return useridlist        






    #DB内に存在するuseridを検索して前回取得したツイートの最新日時を返す(引数：userif, 戻り値：ツイート時間 datetime型)
    def dbmach(self,userid):
        time=datetime.datetime(1990,1,1)
        #テーブルの存在確認
        cur = self.c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='users'")
        if cur.fetchone() == None: #テーブルが存在してない
            self.c.execute("CREATE TABLE users(name text, logtime datetime)")#テーブル生成
        else:
            for row in self.c.execute('SELECT * FROM users'):#テーブル内に指定ユーザーIDがあれば更新するループ
                if row[0]==userid:
                    #row[1]をstr→datetime型に
                    time=datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                    break
                else:
                    print("Disagreement")
        
        return time
 




    #ユーザーの最新ツイート日時の記録と更新を行うメソッド
    def dbmemo(self,userid,tweettime):
         nameflag=False

         #テーブルの存在確認
         cur = self.c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='users'")
         if cur.fetchone() == None: #テーブルが存在してない
             self.c.execute("CREATE TABLE users(name text, logtime datetime)")#テーブル生成
         else:
             for row in self.c.execute('SELECT * FROM users'):#テーブル内に指定ユーザーIDがあれば更新するループ
                 if row[0]==userid:
                     print("update")
                     self.c.execute("UPDATE users SET logtime=? WHERE name=? ", [tweettime,userid])
                     nameflag=True
                     break
                 else:
                     print("no_update")

         if nameflag==False:#更新フラグがFalseならば新規ユーザIDなので追
             self.c.execute("INSERT INTO users VALUES ( ?, ?)", [userid,tweettime])

         for row in self.c.execute('SELECT * FROM users'):
             print(row)

         # 挿入した結果を保存（コミット）する
         self.conn.commit()
              