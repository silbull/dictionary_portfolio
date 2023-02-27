# -*- coding: utf-8 -*-
import tkinter as tk
import pandas as pd
import numpy as np
from tkinter import ttk
from search import Search

# 検索ウィンドウのサイズ <class 'str'>
MAIN_WINDOW_SIZE = "360x170"

# 英単語帳を表示するウィンドウのサイズ <class 'str'>
VIEWER_WINDOW_SIZE = "500x500"

# 英単語帳が格納されているフォルダパス<class 'str'>
PATH = 'wordbook/'

# 英単語帳の名前 <class 'str'>
WORDS_NAME = 'list_en.csv'

# 英単語帳の列名 <class 'dict'>
COLUMN_NAME = {0:'word', 1:'count', 2:'mean'}

class App:
    # GUIを表示するクラス
    
    def __init__(self):
        # 検索ウィンドウ
        self.root = tk.Tk()
        
        # 検索ウィンドウのウィジェット作成
        self._create_window()
        
        # 検索ウィンドウのメニューバー作成
        self._create_menu()
        
        # 検索ウィンドウのメインフレーム作成
        self._create_main_frame()
        
        # 検索機能を実装
        self.search = Search()
        
    def _create_window(self):
        # 検索ウィンドウの設定をする関数
        
        # ウィンドウタイトルを決定
        self.root.title("調べる英単語帳")

        # ウィンドウの大きさを決定
        self.root.geometry(MAIN_WINDOW_SIZE)

        # ウィンドウのグリッドを 1x1 にする
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def _create_menu(self):
        # メニューバーを作成する関数
        
        # メニューバーの作成
        menu = tk.Menu()
        self.root.config(menu=menu)
        
        # ファイルバーの作成
        menu_file = tk.Menu()
        menu.add_cascade(label='ファイル', menu=menu_file)
        menu_file.add_command(label='終了', command=lambda:self._close())
        
        # 表示バーの作成
        menu_display = tk.Menu()
        menu.add_cascade(label='表示', menu=menu_display)
        menu_display.add_command(label='英単語一覧', command=lambda:self._open_viewer())

    def _create_main_frame(self):
        # 検索ウィンドウのウィジェットを作成する関数
        
        # メインページフレーム作成
        self.main_frame = tk.Frame()
        self.main_frame.pack(fill=tk.X)
        
        # 検索テキストボックス
        self.search_box = ttk.Entry(self.main_frame, font=('Constantia', '20'))
        self.search_box.grid(row=0, column=0, sticky=tk.EW, padx=5, pady=10)
        self.search_box.bind('<Return>', self._search)
        
        # 検索画像ボタン
        self.img = tk.PhotoImage(file='materials/search.png').subsample(8,8)
        self.search_button = tk.Button(self.main_frame, image=self.img, relief='flat', command=lambda:self._search())
        self.search_button.grid(row=0, column=1, pady=5)
        
        # 結果テキストボックス
        self.result_box = tk.Text(self.main_frame, width=47, height=6, font=('Constantia', '10'))
        self.result_box.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5)
        # 縦方向のスクロールバーの追加
        ybar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL)
        ybar.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E)
        ybar.config(command=self.result_box.yview)
        self.result_box.config(yscrollcommand=ybar.set)

    def _search(self, event='<Return>'):
        # 検索を行う関数
        # 引数: event <class 'str'>
        
        # 検索した英単語の意味 <class 'str'>
        mean = ""
        
        # 検索した英単語のこれまでの表示回数 <class 'str'>
        count = ""
        
        # 結果テキストボックスに文字が含まれていたときクリアする
        if self.result_box.get('1.0', tk.END):
            self.result_box.delete('1.0', tk.END)
        
        # 検索ボックスに入力された文字を取得 <class 'str'>
        word = self.search_box.get()
        
        # 検索する英単語を渡す
        self.search.set_word(word)
        
        # 単語帳を渡す(デフォルトで'list_en.csv')
        self.search.set_csv(PATH + WORDS_NAME)
        
        # 検索する英単語が過去に検索したか確認
        if self.search.is_searched():
            # 意味と検索回数を取得し、検索回数を1追加する
            mean, count = self.search.get_mean_count()
            self.search.add_count()
        
        else:
            # 検索して意味を取得
            mean = self.search.search()
        
        # 結果ボックスに意味と検索回数を格納
        self.result_box.insert('1.0', mean)
        self.result_box.insert(tk.END, count)
        
        # 単語帳を更新
        self.search.update()
    
    def _open_viewer(self):
        # 単語帳の内容を表示する関数
        Viewer(self.root, PATH + WORDS_NAME)
        
    def _close(self):
        # アプリを終了する関数
            self.root.destroy()

class Viewer:
    # 単語帳の内容を表示するクラス
    
    def __init__(self, root, name):
        # ビューウィンドウ
        self.root = tk.Toplevel(root)
        
        # 単語帳の読み込み
        self.df = pd.read_csv(name)
        
        # 単語帳の内容を表示するテーブル
        self.tree = None
        
        # ソートの切り替え
        self.is_accending = [True, True, True]
        
        # ビューウィンドウを作成
        self._create_window()
        
        # テーブルの作成
        self._create_tree_view()
        
        # 単語帳の内容を表示
        self._show_words()

    def _create_window(self):
        # ビューウィンドウを作成する関数
        
        self.root.title =('My英単語')
        self.root.geometry(VIEWER_WINDOW_SIZE)
        
        # ウィンドウのグリッドを 1x1 にする
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def _create_tree_view(self):
        # テーブルを作成する関数
        
        # フレームの作成
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # テーブルの作成
        self.tree = ttk.Treeview(frame)
        self.tree.column('#0', width=50, stretch=tk.NO, anchor=tk.E)
        self.tree.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)

        # 縦方向のスクロールバーを追加
        vscrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=vscrollbar.set)
        vscrollbar.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S)
        
        # 列を３列作る
        self.tree["column"] = (1, 2, 3)
        self.tree["show"] = "headings"
        
        # ヘッダーテキスト
        self.tree.heading(1, text="英単語", command=lambda:self._sort(COLUMN_NAME[0]))
        self.tree.heading(2, text="検索回数", command=lambda:self._sort(COLUMN_NAME[1]))
        self.tree.heading(3, text="意味", command=lambda:self._sort(COLUMN_NAME[2]))
        
        # 列の幅
        self.tree.column(1, width=100)
        self.tree.column(2, width=50)
        self.tree.column(3, width=300)
    
    def _show_words(self):
        # 単語帳の内容を表示する関数
        
        # 内容をクリア
        self.tree.delete(*self.tree.get_children())
        
        # データ挿入
        for i in self.df.index:
            self.tree.insert("", "end", values=(self.df['word'][i], self.df['count'][i], self.df['mean'][i]))
        
    def _sort(self, col_name):
        # 単語帳にある英単語を並び替える関数
        # 引数: col_name <class 'str'>
        
        # 列名からキーを取得
        key = [k for k, v in COLUMN_NAME.items() if v == col_name][0]
        
        # 英単語を並び替え
        self.df = self.df.sort_values(col_name, ascending=self.is_accending[key])
        
        # ソート方法の切り替え
        if self.is_accending[key]:
            self.is_accending[key] = False
        else:
            self.is_accending[key] = True
        
        # 単語帳の表示
        self._show_words()
