import tweepy
import os
import time

#アクセスpathとトークン
#取得した自身のキーとトークンと以下に書き込む
Consumer_key = ''
Consumer_secret = ''
Access_token = ''
Access_secret = ''

#loginメソッド
def login(acount):
  if acount=="自分のユーザーID":
    auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
    auth.set_access_token(Access_token, Access_secret)
    api = tweepy.API(auth)
    return api
  else:
    exit()