#!/usr/bin/env python
# coding: utf-8
import time
import re

from twython import Twython,TwythonError

import config

global user_name
user_name = "zishin3255"


#twitterの認証情報を入力
api = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, config.ACCESS_KEY, config.ACCESS_SECRET)
print('Auth Done!')


def get_new_tweet():
    global user_name
    try:
        user_timeline = api.get_user_timeline(screen_name=user_name, count=1)
        for tweet in user_timeline:
            now_tweet = tweet['text']
        return now_tweet
    except KeyboardInterrupt:
        pass
    except TwythonError as e:
        write_error(e)


def write_error(string):
    f = open('error.txt', 'a')  # 書き込みモードで開く
    f.write("\n" + str(string))  # 引数の文字列をファイルに書き込む
    f.close()  # ファイルを閉じる


def write_earthquake_info(string):
    string = str(string)
    f = open('last_earthquake.txt', 'a')  # 書き込みモードで開く
    f.write("\n" + string)  # 引数の文字列をファイルに書き込む
    f.close()  # ファイルを閉じる


def read_last_line():
    f = open('last_earthquake.txt')
    data1 = f.read()  # ファイル終端まで全て読んだデータを返す
    f.close()
    lines = data1.split('\n')  # 改行で区切る(改行文字そのものは戻り値のデータには含まれない)
    return lines[-1]


def earthquake_log(new_tweet):
    if new_tweet != read_last_line():
        write_earthquake_info(new_tweet)
        return True
    else:
        return False


def get_info_earthquake(string):
    try:
        announce_num = str(re.search(r'■■緊急地震速報\(第?最?(\D+)報\)■■', string).group(1))
        epicienter = str(re.search(r' (\D+)で地震', string).group(1))
        intensity = str(re.search(r'最大震度 (\d)', string).group(1))
        return announce_num, epicienter, intensity
    except Exception as e:
        write_error(e)


def main():
    # 起動処理　地震速報アカウントの最新ツイートを取得　書き込み
    earthquake_log(get_new_tweet())
    try:
        while True:
            new_earthquake = get_new_tweet() #real
            if earthquake_log(new_earthquake):
                if int(get_info_earthquake(new_earthquake)[2]) >= 3:
                    print("close")
                    #処理送信
            else:
                pass
            time.sleep(5)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        write_error(e)


if __name__ == '__main__':
    main()
