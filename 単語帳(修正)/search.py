# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup
import mojimoji as moji

# 検索エンジン名 <class 'str'>
SEARCH_ENGINE = 'https://ejje.weblio.jp/content/'

# 表示する意味の個数 <class 'int'>
MEAN_N = 3

class Search:
    # 英単語を検索・単語帳に英単語を追加するクラス
    
    def __init__(self):
        # 読み込む単語帳の名前(ファイルパス) <class 'str'>
        self.name = None
        
        # 読み込んだ単語帳をデータフレームで格納 <class 'pandas.core.frame.DataFrame'>
        self.df = None
        
        # 検索する英単語 <class 'str'>
        self.word = None
    
    def set_word(self, word):
        # 検索する英単語を格納する関数
        # 引数: word <class 'str'>
        self.word = word
        
    def set_csv(self, name):
        # 単語帳を格納する関数
        # デフォルトで'list_en.csv'を取得する
        # 引数: name <class 'str'>
        
        self.name = name
        
        # 単語帳をを読み取る
        self.df = pd.read_csv(self.name)
        self.df = self.df.set_index('word')
    
    def is_searched(self):
        # 検索した英単語が過去に検索したか確認する関数
        # 戻り値: <class 'bool'>
        
        if self.word in self.df.index.values:
            return True
        return False
    
    def get_mean_count(self):
        # 単語帳に保存されている、検索された英単語の「意味」と「検索回数」を渡す関数
        # 戻り値: mean <class 'str'>, count <class 'str'>
        
        mean = self.df.at[self.word, 'mean']
        count = f"\n※この単語は{moji.han_to_zen(str(self.df.at[self.word, 'count']))}回検索しました。"
        return mean, count
    
    def add_count(self):
        # 「検索回数」を増やす関数
        self.df.at[self.word, 'count'] += 1
        
    def search(self):
        # 英単語を検索・意味を表示する関数
        # 戻り値: mean <class 'str'> or error_msg <class 'str'>
        
        # urlを検索・スクレイピング
        try:
            search_word = SEARCH_ENGINE + self.word
            url = requests.get(search_word)
        except:
            error_msg = "何らかの問題で検索することが出来ません。ネットに繋がっているか確認してください。"
            return error_msg
        
        try:
            soup = BeautifulSoup(url.text, "html.parser")
            
            # 「、」区切りでMEAN_N(3つ)まで意味を取得
            mean = soup.find(class_='content-explanation ej').get_text().strip().split('、')[:MEAN_N]
            mean = '、'.join(mean)
            
            # 英単語をCSVに追加
            self.df.loc[self.word] = [1, mean]
        
        except:
            error_msg = "入力された英単語は存在しません。"
            return error_msg
        
        return mean
    
    def update(self):
        # 単語帳を更新する関数
        self.df.to_csv(self.name)