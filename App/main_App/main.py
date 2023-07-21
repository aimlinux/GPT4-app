import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from tkinter import scrolledtext 
import tkinter.ttk as ttk
import PySimpleGUI as sg
#import pyautogui as pg
#「pyautoguiでウィンドウの大きさを測るとバグってしまう
import openai
from io import BytesIO
import os
import logging
import speech_recognition as sr
#import pyaudio
#import requests
#import simpleaudio
import wave
import json
import pyttsx3 #voicevoxの代役
import time
import random as rand
import sys
import atexit
import webbrowser
#カレントディレクトリ内
from mic_now import voice_to_text
from voicevox import text_to_voice


# -------- APIKey設定 --------
#openai.api_key = os.environ["OPENAI_API_KEY"] #環境変数に指定する場合
openai.api_key = "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" 



# -------- Logの各設定 --------
#logの出力名を設定
logger = logging.getLogger('Log')
#logLevelを設定
logger.setLevel(10)
#logをコンソール出力するための設定
sh = logging.StreamHandler()
logger.addHandler(sh)
#logのファイル出力先設定
fh = logging.FileHandler('./log/test.log')
logger.addHandler(fh)
#全てのフォーマットオプションとその役割
# %(asctime)s	実行時刻
# %(filename)s	ファイル名
# %(funcName)s	行番号
# %(levelname)s	ログの定義
# %(lineno)d	ログレベル名
# %(message)s	ログメッセージ
# %(module)s	モジュール名
# %(name)s	関数名
# %(process)d	プロセスID
# %(thread)d	スレッドID
formatter = logging.Formatter('%(asctime)s --- process : %(process)d --- message : %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)


#グローバル変数定義
main_bg = "#00ced1" 
sub1_bg = "#00ced1"
sub2_bg = "#00ced1"
sub3_bg = "#00ced1"
sub4_bg = "#00ced1"
title_btn_bg = "#cfd6e6"
sub1_btn_bg = "#cfd6e6"
sub2_btn_bg = "#cfd6e6"
sub3_btn_bg = "#cfd6e6"
sub4_btn_bg = "#191970"
link_fg = "#2f4f4f"
link_bg = "#cfd6e6"
title_font = "Arial"
main_font = "Arial"

button_1 = "しょうかい"
button_2 = "せってい"
button_3 = "たいとるへ"
button_4 = "くれじっと"

#ひらがなON, OFF
hiragana_on = True

#音声大きさ
engine = pyttsx3.init()
engine.setProperty('volume', 1.0) #デフォルト値は1.0
volume = engine.getProperty('volume')

#音声スピード
engine = pyttsx3.init()
engine.setProperty('rate', 200)#デフォルト値は200
rate = engine.getProperty('rate')

# ウィンドウが生成されたフラグを取得するため（各ウィンドウが開いたときTrue、閉じたときFalseへ）
#global count_main, count_sub1, count_sub2, count_sub3, .....
count_main = False
count_sub1 = False
count_sub2 = False
count_sub3 = False
count_sub4 = False
count_mic = False
count_ans_sub1 = False
count_type = False



BUTTON_OPUTIONS = {
    "expand" : "True",
    "fill" : "tk.NONE",
}

TOOLBAR_OPUTIONS = {
    "font" : "main_font, 15",
    "bg" : "#cfe2e6",
    "fg" : "#00334d"
}

# 各person_list_windowに表示するリストの初期値
global all_person_list
all_person_list = ["せんせい", "おかあさん", "おじいさん", "ともだち", "ちゅうがくせい", "かしこいはかせ", "えいごのせんせい", "こいびと", "ろぼっと", "がいこくじん", "かんさいじん", "こうせんせい"]
# 各person_list_windowの大きさと初期配置を決める（メインウィンドウに関してはコード最下部）
global all_person_list_window_size
all_person_list_window_size = "500x600+400+100"
# 設定ウィンドウの大きさと初期配置を決める
global config_window_size
config_window_size = "500x650+400+100"
# オプション or 右クリックウィンドウの大きさと初期配置
global option_window_size
option_window_size = "800x500"
#くれじっとウィンドウの大きさと初期配置
global credit_window_size
credit_window_size = "500x700+400+100"



# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
        
    def create_widgets(self):
        
        #Logファイルに記録を残す
        logger.log(100, "App Start")
        
        print(f"{window_width}x{window_height}+{x}+{y}")
        
        global count_main
        count_main = True
        
        global pw_main, fm_main, fm_toolbar
        
        
        #メインウィンドウ作成
        pw_main = tk.PanedWindow(self.master, bg=main_bg, orient="vertical")
        pw_main.pack(expand=True, fill=tk.BOTH, side="left")
        
        #メインフレーム作成
        fm_main = tk.Frame(pw_main, bd=15, bg=main_bg, relief="ridge")
        pw_main.add(fm_main)
        
    # -------- メインフレームのオブジェクト作成 --------
    
        
        # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_main, bg=main_bg)
        fm_toolbar.pack(anchor="nw")
        
        #toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS, command=self.show_option)
        #toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        
        space_label = tk.Label(fm_main, text="", bg=main_bg, height=2)
        space_label.pack(side=tk.TOP)

        title_label = tk.Label(fm_main, text="**** ちゃっとじーぴーてぃーのあぷり ****", bg=main_bg, font=(title_font, 30), height=2)
        title_label.pack(side=tk.TOP)
        
        space_label = tk.Label(fm_main, text="", bg=main_bg, height=7)
        space_label.pack(side=tk.TOP)
    
        start_button = tk.Button(fm_main, text=" ことばでおはなし ", font=(main_font, 20), bg=title_btn_bg, width=30, command=self.create_1)
        start_button.pack(side=tk.TOP, pady=12)
        #start_button = tk.Button(fm_main, text=" てがきでおはなし", font=(main_font, 20), bg=title_btn_bg, width=30, command=self.create_2)
        #start_button.pack(side=tk.TOP, pady=10)
        start_button = tk.Button(fm_main, text=" てうちでおはなし ", font=(main_font, 20), bg=title_btn_bg, width=30, command=self.create_3)
        start_button.pack(side=tk.TOP, pady=12)
        start_button = tk.Button(fm_main, text=" せってい ", font=(main_font, 20), bg=title_btn_bg, width=30, command=self.create_4)
        start_button.pack(side=tk.TOP, pady=12)
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""


    
    #sub1
    def create_1(self):
        
        global count_sub1, count_main
        count_sub1 = True
        count_main = False
        
        global person_list_sub1
        person_list_sub1 = None
        
        global fm_sub1, pw_sub1
        pw_main.destroy()
        
        pw_sub1 = tk.PanedWindow(self.master, bg=sub1_bg, orient="vertical")
        pw_sub1.pack(expand=True, fill=tk.BOTH, side="left")
        
        fm_sub1 = tk.Frame(bd=15, bg=sub1_bg, relief="ridge")
        pw_sub1.add(fm_sub1)
    
    # -------- メインフレームのオブジェクト作成 --------
        # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_sub1, bg=sub1_bg)
        fm_toolbar.pack(anchor="nw")
        
        #toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS, command=self.show_option)
        #toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        space_label = tk.Label(fm_sub1, text="", bg=sub1_bg, height=2)
        space_label.pack(side=tk.TOP)

        title_label = tk.Label(fm_sub1, text="**** ことばでおはなし ****", bg=sub1_bg, font=(title_font, 42), height=2)
        title_label.pack(side=tk.TOP)
        
        space_label = tk.Label(fm_sub1, text="", bg=sub1_bg, height=2)
        space_label.pack(side=tk.TOP)
        label = tk.Label(fm_sub1, text="よこにあるまいくにちかづいてしつもんしてね", bg=sub1_bg, font=(main_font, 25), width=45)
        label.pack(side=tk.TOP, pady=10)
        space_label = tk.Label(fm_sub1, text="", bg=sub1_bg, height=1)
        space_label.pack(side=tk.TOP)
        label = tk.Label(fm_sub1, text="じょうずにこえがきこえないこともあるよ \n そんなときはくりかえしやってみて！", bg=sub1_bg, font=(main_font, 25), width=45)
        label.pack(side=tk.TOP, pady=10)
        
        start_button = tk.Button(fm_sub1, text=" ことばでしつもん ", font=(main_font, 35), bg=sub1_btn_bg, width=30, command=self.ans_person_sub1)
        start_button.pack(side=tk.BOTTOM, pady=50)
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
    
    
    #sub2
    def create_2(self):
                
        global count_sub2, count_main
        count_sub2 = True
        count_main = False
        
        global person_list_sub2
        person_list_sub2 = None
        global paint_window
        paint_window = None
        
        global fm_sub2, pw_sub2
        pw_main.destroy()
        
        pw_sub2 = tk.PanedWindow(self.master, bg=sub2_bg, orient="vertical")
        pw_sub2.pack(expand=True, fill=tk.BOTH, side="left")
        
        fm_sub2 = tk.Frame(bd=15, bg=sub2_bg, relief="ridge")
        pw_sub2.add(fm_sub2)
        
    # -------- メインフレームのオブジェクト作成 --------
    # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_sub2, bg=sub2_bg)
        fm_toolbar.pack(anchor="nw")
        
        #toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS, command=self.show_option)
        #toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        space_label = tk.Label(fm_sub2, text="", bg=sub2_bg, height=2)
        space_label.pack(side=tk.TOP)

        title_label = tk.Label(fm_sub2, text="**** てがきでおはなし ****", bg=sub2_bg, font=(title_font, 42), height=2)
        title_label.pack(side=tk.TOP)
        
        space_label = tk.Label(fm_sub2, text="", bg=sub2_bg, height=2)
        space_label.pack(side=tk.TOP)
        label = tk.Label(fm_sub2, text="このぱそこんにもじをかいてね", bg=sub2_bg, font=(main_font, 25), width=45)
        label.pack(side=tk.TOP, pady=10)
        space_label = tk.Label(fm_sub2, text="", bg=sub2_bg, height=1)
        space_label.pack(side=tk.TOP)
        label = tk.Label(fm_sub2, text="じょうずにもじがよめないこともあるよ \n そんなときはくりかえしやってみて！", bg=sub2_bg, font=(main_font, 25), width=45)
        label.pack(side=tk.TOP, pady=10)
        
        start_button = tk.Button(fm_sub2, text=" てがきでしつもん ", font=(main_font, 35), bg=sub2_btn_bg, width=30, command=self.ans_person_sub2)
        start_button.pack(side=tk.BOTTOM, pady=50)
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        
    
    #sub3
    def create_3(self):
                
        global count_sub3, count_main
        count_sub3 = True
        count_main = False
        
        global person_list_sub3
        person_list_sub3 = None
        
        global fm_sub3, pw_sub3
        pw_main.destroy()
        
        global config_window
        
        pw_sub3 = tk.PanedWindow(self.master, bg=sub3_bg, orient="vertical")
        pw_sub3.pack(expand=True, fill=tk.BOTH, side="left")
        
        fm_sub3 = tk.Frame(bd=15, bg=sub3_bg, relief="ridge")
        pw_sub3.add(fm_sub3)
        
    # -------- メインフレームのオブジェクト作成 --------
        # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_sub3, bg=sub3_bg)
        fm_toolbar.pack(anchor="nw")
        
        #toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS, command=self.show_option)
        #toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        space_label = tk.Label(fm_sub3, text="", bg=sub3_bg, height=2)
        space_label.pack(side=tk.TOP)

        title_label = tk.Label(fm_sub3, text="**** てうちでおはなし ****", bg=sub3_bg, font=(title_font, 42), height=2)
        title_label.pack(side=tk.TOP)
        
        space_label = tk.Label(fm_sub3, text="", bg=sub3_bg, height=2)
        space_label.pack(side=tk.TOP)
        label = tk.Label(fm_sub3, text="ぱそこんのきーぼーどから\nことばをにゅうりょくしてね", bg=sub3_bg, font=(main_font, 25), width=30)
        label.pack(side=tk.TOP, pady=10)
        space_label = tk.Label(fm_sub3, text="", bg=sub3_bg, height=1)
        space_label.pack(side=tk.TOP)
        #label = tk.Label(fm_sub3, text="しょうがくせいにはむずかしいかも", bg=sub3_bg, font=(main_font, 25), width=30)
        #label.pack(side=tk.TOP, pady=10)
        
        start_button = tk.Button(fm_sub3, text=" てうちでしつもん ", font=(main_font, 35), bg=sub3_btn_bg, width=30, command=self.ans_person_sub3)
        start_button.pack(side=tk.BOTTOM, pady=50)
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
    
    
    #config sub4（設定）
    def create_4(self):
                
        global count_sub4, count_main
        count_sub4 = True
        count_main = False
        
        global fm_sub4, pw_sub4
        pw_main.destroy()
        
        pw_sub4 = tk.PanedWindow(self.master, bg=sub4_bg, orient="vertical")
        pw_sub4.pack(expand=True, fill=tk.BOTH, side="left")
        
        fm_sub4 = tk.Frame(bd=15, bg=sub4_bg, relief="ridge")
        pw_sub4.add(fm_sub4)
        
    # -------- メインフレームのオブジェクト作成 --------
        # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_sub4, bg=sub4_bg)
        fm_toolbar.pack(anchor="nw")
        
        #toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS, command=self.show_option)
        #toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        space.pack()
        label = tk.Label(fm_sub4, text="---- おとのおおきさ ----", bg=sub4_bg, font=(main_font, 25), width=30)
        label.pack()
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        space.pack()
        
        #サウンドバー
        self.sound_var = tk.DoubleVar()
        soundH = tk.Scale(
            fm_sub4, 
            variable=self.sound_var, 
            orient=tk.HORIZONTAL, 
            bg="#e6e6fa",
            fg="#191970", 
            font=(main_font, 10),
            length=400, 
            width=30, 
            sliderlength=20, 
            from_=0, 
            to=10,
            resolution=1, 
            tickinterval=2,
            command=self.slider_scroll_1
        )
        soundH.pack()
        
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        space.pack()
        label = tk.Label(fm_sub4, text="---- おとのスピード ----", bg=sub4_bg, font=(main_font, 25), width=30)
        label.pack()
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        space.pack()
        
        #スピードバー
        self.speed_var = tk.DoubleVar()
        speedH = tk.Scale(
            fm_sub4, 
            variable=self.speed_var, 
            orient=tk.HORIZONTAL, 
            bg="#e6e6fa",
            fg="#191970", 
            font=(main_font, 10),
            length=400, 
            width=30, 
            sliderlength=20, 
            from_=0, 
            to=10,
            resolution=1, 
            tickinterval=2,
            command=self.slider_scroll_2
        )
        speedH.pack()
        
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), height=4)
        space.pack()
        label = tk.Label(fm_sub4, text="---- ひらがなのみモード ----", bg=sub4_bg, font=(main_font, 25), width=30)
        label.pack(pady=1)
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        #space.pack()

        label = tk.Button(fm_sub4, text="OK", font=(main_font, 22), bg="#e6e6fa", width=5, command=self.exit_sub4)
        label.pack(side=tk.RIGHT, padx=80)
        
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), height=1)
        space.pack(side=tk.RIGHT, padx=100)
        
        hiragana_off_button = tk.Button(fm_sub4, text=" OFF ", font=(main_font, 20), bg="#e6e6fa", command=self.hiragana_off)
        hiragana_off_button.pack(side=tk.RIGHT, padx=20)
        hiragana_on_button = tk.Button(fm_sub4, text=" ON ", font=(main_font, 20), bg="#e6e6fa", command=self.hiragana_on)
        hiragana_on_button.pack(side=tk.RIGHT, padx=20)
        
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), height=1)
        space.pack()

        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        

    #config Toplevelウィンドウ（設定）
    def config(self):
        
        global config_window
        
        config_window = tk.Toplevel(bg=sub4_bg, bd=2)
        config_window.geometry(config_window_size)
        config_window.title("config_window")
        
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        space.pack()
        label = tk.Label(config_window, text="---- おとのおおきさ ----", bg=sub4_bg, font=(main_font, 25), width=30)
        label.pack()
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        space.pack()
        
        #サウンドバー
        self.sound_var = tk.DoubleVar()
        soundH = tk.Scale(
            config_window, 
            variable=self.sound_var, 
            orient=tk.HORIZONTAL, 
            bg="#e6e6fa",
            fg="#191970", 
            font=(main_font, 10),
            length=400, 
            width=30, 
            sliderlength=20, 
            from_=0, 
            to=10,
            resolution=1, 
            tickinterval=2,
            command=self.slider_scroll_1
        )
        soundH.pack()
        
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        space.pack()
        label = tk.Label(config_window, text="---- おとのスピード ----", bg=sub4_bg, font=(main_font, 25), width=30)
        label.pack()
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        space.pack()
        
        #スピードバー
        self.speed_var = tk.DoubleVar()
        speedH = tk.Scale(
            config_window, 
            variable=self.speed_var, 
            orient=tk.HORIZONTAL, 
            bg="#e6e6fa",
            fg="#191970", 
            font=(main_font, 10),
            length=400, 
            width=30, 
            sliderlength=20, 
            from_=0, 
            to=10,
            resolution=1, 
            tickinterval=2,
            command=self.slider_scroll_2
        )
        speedH.pack()
        
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=4)
        space.pack()
        label = tk.Label(config_window, text="---- ひらがなのみモード ----", bg=sub4_bg, font=(main_font, 25), width=30)
        label.pack(pady=1)
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=2)
        #space.pack()
        
        label = tk.Button(config_window, text="OK", font=(main_font, 22), bg="#e6e6fa", width=4, command=self.exit_config)
        label.pack(side=tk.RIGHT, padx=80)
        
        hiragana_off_button = tk.Button(config_window, text=" OFF ", font=(main_font, 18), bg="#e6e6fa", command=self.hiragana_off)
        hiragana_off_button.pack(side=tk.RIGHT, padx=30)
        hiragana_on_button = tk.Button(config_window, text=" ON ", font=(main_font, 18), bg="#e6e6fa", command=self.hiragana_on)
        hiragana_on_button.pack(side=tk.RIGHT, padx=10)
        
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=1)
        space.pack()
        
        return 0
    
    
    #ひらがなON
    def hiragana_on(self, event=None):
        global hiragana_on
        hiragana_on = True
        print("hiragana_on : " + str(hiragana_on))
        
        return hiragana_on
    
    
    #ひらがなOFF
    def hiragana_off(self, event=None):
        global hiragana_on
        hiragana_on = False
        print("hiragana_on : " + str(hiragana_on))
        
        return hiragana_on
    
    
    #sound_varが動かされたとき
    def slider_scroll_1(self, event=None):
        
        global volume
        #sound_valueの大きさをリアルタイムで取得する
        sound_value = self.sound_var.get()
        print(sound_value)
        engine = pyttsx3.init()
        # 「/5」については実行環境により任意で変更
        engine.setProperty('volume', sound_value / 5)#デフォルト値は1.0
        volume = engine.getProperty('volume')
        
    
    #speed_varが動かされたとき
    def slider_scroll_2(self, event=None):
        
        global rate
        #speed_valueの大きさをリアルタイムで取得する
        speed_value = self.speed_var.get()
        print(speed_value)
        engine = pyttsx3.init()
        #「*40」については実行環境により任意で変更
        engine.setProperty('rate', speed_value * 40)#デフォルト値は200
        rate = engine.getProperty('rate')
        
        
    #config_windowから戻る
    def exit_config(self):
        global config_window
        config_window.destroy()
    
    
    #オプション
    def show_option(self):
        pass
    
    #クレジットに記載するテキスト
    global programmer_name_1, programmer_name_2
    programmer_name_1 = "田中友陽"
    programmer_name_2 = "小原和真"
    
    global teacher_name
    teacher_name = "角田直輝"
    
    global github_link
    github_link = "https://github.com/aimlinux/GPT4-app/tree/main/App/main_App/main.py"
    
    global github_owner
    github_owner = "aimlinux"
    
    global kousen_link
    kousen_link = "https://www.yonago-k.ac.jp/"
    
    global used_library
    used_library = "Tkinter, PySimpleGUI, openai, pyautogui, BytesIO, os, logging, speech_recognition, pyaudio, simpleaudio, wave, json, pyttsx3, time, random, sys, atexit, webbrowser, requests"
    
    
    #クレジット
    def credit(self):
        
        global credit_window
        
        credit_window = tk.Toplevel(bg=main_bg, bd=2)
        credit_window.geometry(credit_window_size)
        credit_window.title("credit")
        
        space_label = tk.Label(credit_window, text="", bg=main_bg, height=3)
        space_label.pack(side=tk.TOP)

        title_label = tk.Label(credit_window, text=f"作成者 : {programmer_name_1}, {programmer_name_2}", bg=main_bg, font=(main_font, 22))
        title_label.pack(side=tk.TOP)
        
        space_label = tk.Label(credit_window, text="", bg=main_bg, height=2)
        space_label.pack(side=tk.TOP)
        
        label = tk.Label(credit_window, text=f"指導教員 : {teacher_name}", bg=main_bg, font=(main_font, 22))
        label.pack(side=tk.TOP)
        
        space_label = tk.Label(credit_window, text="", bg=sub3_bg, height=3)
        space_label.pack(side=tk.TOP)
        
        github_link_label = tk.Label(credit_window, text=f"GitHubリンク : {github_owner}", bg=link_bg, fg=link_fg, font=(main_font, 22), cursor="hand2")
        github_link_label.pack(side=tk.TOP)
        github_link_label.bind("<Button-1>", lambda e: self.open_github_link())
        
        space_label = tk.Label(credit_window, text="", bg=main_bg, height=2)
        space_label.pack(side=tk.TOP)
        
        kousen_link_label = tk.Label(credit_window, text=f"米子高専ホームページ", bg=link_bg, fg=link_fg, font=(main_font, 22), cursor="hand2")
        kousen_link_label.pack(side=tk.TOP)
        kousen_link_label.bind("<Button-1>", lambda e: self.open_kousen_link())
        
        space_label = tk.Label(credit_window, text="", bg=main_bg, height=3)
        space_label.pack(side=tk.TOP)
        
        label = tk.Label(credit_window, text="python使用ライブラリ : ", bg=main_bg, font=(main_font, 18))
        label.pack(side=tk.TOP)
        space_label = tk.Label(credit_window, text="", bg=main_bg, height=1)
        space_label.pack()
        #オブジェクト配置初期はstateの値を変更できるようにしなければならない
        self.text_new_question_sub1 = scrolledtext.ScrolledText(credit_window, width=40, height=3, font=(main_font, 20), bg="#fff", state="normal")
        self.text_new_question_sub1.pack()
        self.text_new_question_sub1.insert(tk.END, used_library)
        #stateの値を変更できないよう（normalからtk.DISABLED）に設定
        self.text_new_question_sub1.config(state=tk.DISABLED)
        
        space_label = tk.Label(credit_window, text="", bg=main_bg, height=3)
        space_label.pack()
        start_button = tk.Button(credit_window, text="とじる", font=(main_font, 20), bg=title_btn_bg, command=self.exit_credit)
        start_button.pack()
        
        return 0
    
    
    #webブラウザでgithubリンクを開く
    def open_github_link(self):
        webbrowser.open_new(github_link)
        return 0
    
    #webブラウザで米子高専ホームページを開く
    def open_kousen_link(self):
        webbrowser.open_new(kousen_link)
        return 0
        

    #credit_windowから戻る
    def exit_credit(self):
        global credit_window
        credit_window.destroy()
        
    
    
    #on_select_sub1
    def on_select_sub1(event):
        #選択された値を取得する
        global selected_value_sub1
        selected_value_sub1 = listbox_sub1.get(listbox_sub1.curselection())
        print(selected_value_sub1)
    
    #ans_person_sub1
    def ans_person_sub1(self):
        global person_list_sub1
        global listbox_sub1
        if person_list_sub1 == None or not person_list_sub1.winfo_exists():
            person_list_sub1 = tk.Toplevel(bg=sub1_bg, bd=2)
            person_list_sub1.geometry(all_person_list_window_size)
            person_list_sub1.title("person_list_sub1")
            
            list_sub1_value = tk.StringVar()
            list_sub1_value.set(all_person_list)
            
            space = tk.Label(person_list_sub1, text="", bg=sub1_bg, height=2)
            space.pack()
            label = tk.Label(person_list_sub1, text="どんなひとにしつもんする？", font=(main_font, 20), bg=sub1_bg)
            label.pack()
            space = tk.Label(person_list_sub1, text="", bg=sub1_bg, height=1)
            space.pack()
            
            #selectmodeの種類(single:1つだけ選択できる、multiple:複数選択できる、extended：複数選択可能＋ドラッグでも選択可能)
            listbox_sub1 = tk.Listbox(person_list_sub1, height=12, width=15, font=(main_font, 20), listvariable=list_sub1_value, selectmode="single", relief="sunken", bd=5)
            listbox_sub1.pack()
            space = tk.Label(person_list_sub1, text="", bg=sub1_bg, height=1)
            space.pack()
            button = tk.Button(person_list_sub1, text="けってい", font=(main_font, 20), bg=sub1_btn_bg, command=self.mic_on)
            button.pack()
            space = tk.Label(person_list_sub1, text="", bg=sub1_bg, height=1)
            space.pack()
            
            listbox_sub1.bind('<<ListboxSelect>>', lambda e: self.on_select_sub1())


    #マイクオン
    def mic_on(self):
        person_list_sub1.destroy()
        
        global count_mic, count_sub1
        count_mic = True
        count_sub1 = False
        
        global fm_mic, pw_mic
        pw_sub1.destroy()
        
        global mic_text_label
        
        pw_mic = tk.PanedWindow(self.master, bg=sub1_bg, orient="vertical")
        pw_mic.pack(expand=True, fill=tk.BOTH, side="left")
        
        fm_mic = tk.Frame(bd=15, bg=sub1_bg, relief="ridge")
        pw_mic.add(fm_mic)
            
    # -------- メインフレームのオブジェクト作成 --------
        # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_mic, bg=sub1_bg)
        fm_toolbar.pack(anchor="nw")
        
        #toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS, command=self.show_option)
        #toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        space = tk.Label(fm_mic, text="", bg=sub1_bg, height=3)
        space.pack()
        label = tk.Label(fm_mic, text="～～マイクにむかってしつもんしてね～～", font=(main_font, 28), bg=sub1_bg)
        label.pack()
        space = tk.Label(fm_mic, text="", bg=sub1_bg, height=1)
        space.pack()
        button = tk.Button(fm_mic, text="しつもんすたーと", font=(main_font, 23), bg=sub1_btn_bg, command=self.mic_now)
        button.pack()
        space = tk.Label(fm_mic, text="", bg=sub1_bg, height=3)
        space.pack()
        label = tk.Label(fm_mic, text=" **** しつもんないよう **** ", font=(main_font, 24), bg=sub1_bg)
        label.pack()
        space = tk.Label(fm_mic, text="", bg=sub1_bg, height=1)
        space.pack()
        #state --- tk.NORMAL：編集できる・tk.DISABLED：編集できない 
        #DISABLEDにするとテキストがアウトプット出来なくなります...
        self.mic_question = scrolledtext.ScrolledText(fm_mic, width=60, height=6, font=(main_font, 25), bg="#fff", fg="#191970", state="normal")
        #self.text_output = tk.Text(fm_type, width=80, height=9, state=tk.DISABLED, font=(main_font, 15), bg="#ffffff")
        self.mic_question.pack()
        space = tk.Label(fm_mic, text="", bg=sub1_bg, height=2)
        space.pack()
        button = tk.Button(fm_mic, text="もういっかいしつもんする", font=(main_font, 20), bg=sub1_btn_bg, command=self.mic_now)
        button.pack(side=tk.RIGHT, padx=20, pady=10)
        button = tk.Button(fm_mic, text="これにきめた！", font=(main_font, 20), bg=sub1_btn_bg, command=self.ai_answer_window_sub1)
        button.pack(side=tk.RIGHT, padx=20, pady=10)
                
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        
        
    #マイクの音声を取得
    def mic_now(self):
        
        self.mic_question.delete("0.0", tk.END) 
        #エラー防止（関数呼び出しより先に文字を消去）
        time.sleep(1.1)
        
        #mic_on.pyの内容を実行
        global new_question_sub1
        #new_question_sub1 = voice_to_text()
        #マイクなしテスト
        no_mic_new_question_list = ["よなごこうせんのとくちょうはなに", "わたしはだーれ", "おはようございます"]
        new_question_sub1 = rand.choice(no_mic_new_question_list)
        
        print("new_qestion : " + new_question_sub1)
        self.mic_question.insert(tk.END, new_question_sub1)
        
        return new_question_sub1


    #ai_answer_window_sub1
    def ai_answer_window_sub1(self):

        fm_mic.destroy()
        
        global count_ans_sub1, count_mic, count_sub1
        count_ans_sub1 = True
        count_mic = False
        count_sub1 = False
        
        global fm_ans_sub1, pw_ans_sub1
        pw_mic.destroy()

        pw_ans_sub1 = tk.PanedWindow(self.master, bg=sub1_bg, orient="vertical")
        pw_ans_sub1.pack(expand=True, fill=tk.BOTH, side="left")
    
        fm_ans_sub1 = tk.Frame(bd=15, bg=sub1_bg, relief="ridge")
        pw_ans_sub1.add(fm_ans_sub1)
            
    # -------- メインフレームのオブジェクト作成 --------
        # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_ans_sub1, bg=sub1_bg)
        fm_toolbar.pack(anchor="nw")
        
        #toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS, command=self.show_option)
        #toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)

        space = tk.Label(fm_ans_sub1, text="", bg=sub1_bg, height=1)
        space.pack()
        label = tk.Label(fm_ans_sub1, text=f"\"{selected_value_sub1}\"にしつもんすることは↓にかいてあるよ", font=(main_font, 23), bg=sub3_bg)
        label.pack()
        space = tk.Label(fm_ans_sub1, text="", bg=sub1_bg, height=1)
        space.pack()
        
        global new_question_sub1
        new_question = new_question_sub1
        #オブジェクト配置初期はstateの値を変更できるようにしなければならない
        self.text_new_question_sub1 = scrolledtext.ScrolledText(fm_ans_sub1, width=60, height=5, font=(main_font, 20), bg="#fff", state="normal")
        self.text_new_question_sub1.pack()
        self.text_new_question_sub1.insert(tk.END, new_question)
        #stateの値を変更できないよう（normalからtk.DISABLED）に設定
        self.text_new_question_sub1.config(state=tk.DISABLED)
        
        space = tk.Label(fm_ans_sub1, text="", bg=sub1_bg, height=1)
        space.pack()
        
        button = tk.Button(fm_ans_sub1, text="けってい", font=(main_font, 20), bg=sub1_btn_bg, command=self.ai_answer_sub1)
        button.pack()
        
        space = tk.Label(fm_ans_sub1, text="", bg=sub1_bg, height=1)
        space.pack()
        label = tk.Label(fm_ans_sub1, text=f"\"{selected_value_sub1}\"からのしつもんのこたえ", font=(main_font, 21), bg=sub3_bg)
        label.pack()
        #state --- tk.NORMAL：編集できる・tk.DISABLED：編集できない 
        self.text_output_sub1 = scrolledtext.ScrolledText(fm_ans_sub1, width=60, height=5, font=(main_font, 20), bg="#fff", state="normal")
        #self.text_output_sub1 = tk.Text(fm_ans_sub1, width=80, height=9, state=tk.DISABLED, font=(main_font, 15), bg="#ffffff")
        self.text_output_sub1.pack()
        space = tk.Label(fm_ans_sub1, text="", bg=sub1_bg, height=1)
        space.pack()
        button = tk.Button(fm_ans_sub1, text="おわる", font=(main_font, 20), bg=sub1_btn_bg, command=self.return_title)
        button.pack(side=tk.RIGHT, padx=30, pady=10)
        button = tk.Button(fm_ans_sub1, text="もういちど", font=(main_font, 20), bg=sub1_btn_bg, command=self.return_sub1)
        button.pack(side=tk.RIGHT, padx=10, pady=10)
        space = tk.Label(fm_ans_sub1, text="", bg=sub1_bg, height=1)
        space.pack()
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        
            
    #sub3で入力された質問へのAIの回答
    def ai_answer_sub1(self):
        global new_question_sub1
        global selected_value_sub1
        
        #質問する対象を選んでなかった場合
        if selected_value_sub1 == 0:
            selected_value_sub1 = "teacher"
            res = messagebox.showerror("Error", "しつもんするひとがえらばれていないよ。\n たいとるへもどるよ。")
            print(res, "Error : No PersonList")
            
            self.return_title()            
            
        logger.log(100, f"AnswerPerson_sub1 : {selected_value_sub1}")
        logger.log(100, f"TypeQuestion_sub1 : {new_question_sub1}")
        print("AnswerPerson : " + selected_value_sub1)
        print("TypeQuestion : " + new_question_sub1)

        #エラー防止
        time.sleep(0.1) 
        
        #roleについて設定
        role_sys_1 = str(selected_value_sub1)
        if not role_sys_1:
            role_sys_1:str = "あなた"
        
        #質問について設定
        question_sub1 = new_question_sub1
        if not question_sub1:
            question_sub1:str = "しつもんがにゅうりょくされていなかったみたいだね。\n もういっかいしつもんしたかったら「もういちど」ボタンをおしてね！"
        #ひらがなだけで解答
        if hiragana_on == True:
            question_sub1 = question_sub1 + "という質問について分かりやすくひらがなだけで解答して"
            print(question_sub1)
        else:
            pass
                        
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                #role : 役割, 
                # system :（このチャットのシステム） 
                # user :（チャットを使う側 = 私たち） 
                # assistant : ChatGPT側, 
                # content : メッセージ内容
                {"role": "system", "content": role_sys_1}, 
                {"role": "user", "content": question_sub1},
                #{"role": "assistant", "content": "どういうこと？"},
                #{"role": "user", "content": "もう少し簡単に教えて！！"},
            ]
        )
        
        # #ChatGPTからの返答の内容
        global res_content_sub1
        res_content_sub1 = res["choices"][0]["message"]["content"]
        print("AI_answer : " + res_content_sub1)
        logger.log(100, f"AI_answer : {res_content_sub1}")
        
        #ChatGPTが使えない場合
        #global res_content_sub1
        #res_content_sub1 = "おおはよう"
        
        global new_answer
        new_answer = f"{selected_value_sub1}：{res_content_sub1}"
        print(new_answer)
        
        #エラー防止
        time.sleep(0.1)
        
        self.output_now_sub1()


    def output_now_sub1(self):
        
        print("output_now_sub1")
        #ウィンドウのテキストを表示
        self.text_output_sub1.delete("0.0", tk.END) 
        self.text_output_sub1.insert(tk.END, res_content_sub1)
        
        #テキストが表示されてから音声を読み上げる
        time.sleep(0.5)
        
        # Voicevoxで音声を読み上げる
        #print(res_content_sub1)
        #text_to_voice(res_content_sub1)
        
        # pyttsx3で音声を読み上げる
        engine = pyttsx3.init()
        engine.say(res_content_sub1) 
        engine.runAndWait()
        
        return 0
            
            
    #on_select_sub2
    def on_select_sub2(event):
        #選択された値を取得する
        global selected_value_sub2
        selected_value_sub2 = listbox_sub2.get(listbox_sub2.curselection())
        print(selected_value_sub2)

    #ans_person_sub2
    def ans_person_sub2(self):
        global person_list_sub2
        global listbox_sub2
        if person_list_sub2 == None or not person_list_sub2.winfo_exists():
            person_list_sub2 = tk.Toplevel(bg=sub2_bg, bd=2)
            person_list_sub2.geometry(all_person_list_window_size)
            person_list_sub2.title("person_list_sub2")
            
            list_sub2_value = tk.StringVar()
            list_sub2_value.set(all_person_list)
            
            space = tk.Label(person_list_sub2, text="", bg=sub2_bg, height=2)
            space.pack()
            label = tk.Label(person_list_sub2, text="どんなひとにしつもんする？", font=(main_font, 20), bg=sub2_bg)
            label.pack()
            space = tk.Label(person_list_sub2, text="", bg=sub2_bg, height=1)
            space.pack()
            
            #selectmodeの種類(single:1つだけ選択できる、multiple:複数選択できる、extended：複数選択可能＋ドラッグでも選択可能)
            listbox_sub2 = tk.Listbox(person_list_sub2, height=12, width=15, font=(main_font, 20), listvariable=list_sub2_value, selectmode="single", relief="sunken", bd=5)
            listbox_sub2.pack()
            space = tk.Label(person_list_sub2, text="", bg=sub2_bg, height=1)
            space.pack()
            button = tk.Button(person_list_sub2, text="けってい", font=(main_font, 20), bg=sub2_btn_bg, command=self.paint_now)
            button.pack()
            space = tk.Label(person_list_sub2, text="", bg=sub2_bg, height=1)
            space.pack()

            listbox_sub2.bind("<<ListboxSelect>>", lambda e: self.on_select_sub2())


    #おえかき
    def paint_now(self):
        person_list_sub2.destroy()
        global paint_window
        
        if paint_window == None or not paint_window.winfo_exists():
            paint_window= tk.Toplevel(bg=sub2_bg, bd=2)
            paint_window.geometry("600x600")
            paint_window.title("paint_window")
        
        
        
    #on_select_sub3
    def on_select_sub3(event):
        #選択された値を取得する
        global selected_value_sub3
        selected_value_sub3 = listbox_sub3.get(listbox_sub3.curselection())
        print(selected_value_sub3)
        
    #ans_person_sub3
    def ans_person_sub3(self):
        global person_list_sub3
        global listbox_sub3
        if person_list_sub3 == None or not person_list_sub3.winfo_exists():
            person_list_sub3 = tk.Toplevel(bg=sub3_bg, bd=2)
            person_list_sub3.geometry(all_person_list_window_size)
            person_list_sub3.title("person_list_sub3")
            
            list_sub3_value = tk.StringVar()
            list_sub3_value.set(all_person_list)
            
            space = tk.Label(person_list_sub3, text="", bg=sub3_bg, height=2)
            space.pack()
            label = tk.Label(person_list_sub3, text="どんなひとにしつもんする？", font=(main_font, 20), bg=sub3_bg)
            label.pack()
            space = tk.Label(person_list_sub3, text="", bg=sub3_bg, height=1)
            space.pack()
            
            #selectmodeの種類(single:1つだけ選択できる、multiple:複数選択できる、extended：複数選択可能＋ドラッグでも選択可能)
            listbox_sub3 = tk.Listbox(person_list_sub3, height=12, width=15, font=(main_font, 20), listvariable=list_sub3_value, selectmode="single", relief="sunken", bd=5)
            listbox_sub3.pack()
            space = tk.Label(person_list_sub3, text="", bg=sub3_bg, height=1)
            space.pack()
            button = tk.Button(person_list_sub3, text="けってい", font=(main_font, 20), bg=sub3_btn_bg, command=self.type_now)
            button.pack()
            space = tk.Label(person_list_sub3, text="", bg=sub3_bg, height=1)
            space.pack()

            listbox_sub3.bind("<<ListboxSelect>>", lambda e: self.on_select_sub3())


    #タイピング
    def type_now(self):
        
        person_list_sub3.destroy()
        
        global count_type, count_sub3
        count_type = True
        count_sub3 = False
        
        global fm_type, pw_type
        pw_sub3.destroy()
        
        pw_type = tk.PanedWindow(self.master, bg=sub3_bg, orient="vertical")
        pw_type.pack(expand=True, fill=tk.BOTH, side="left")
        
        fm_type = tk.Frame(bd=15, bg=sub3_bg, relief="ridge")
        pw_type.add(fm_type)
        
    # -------- メインフレームのオブジェクト作成 --------
        # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_type, bg=sub3_bg)
        fm_toolbar.pack(anchor="nw")
        
        #toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS, command=self.show_option)
        #toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS, command=self.credit)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        space = tk.Label(fm_type, text="", bg=sub3_bg, height=1)
        space.pack()
        label = tk.Label(fm_type, text=f"\"{selected_value_sub3}\"にしつもんしたいことを↓ににゅうりょくしてね！", font=(main_font, 23), bg=sub3_bg)
        label.pack()
        space = tk.Label(fm_type, text="", bg=sub3_bg, height=1)
        space.pack()
        self.text_input = scrolledtext.ScrolledText(fm_type, width=60, height=5, font=(main_font, 20), bg="#fff", state="normal")
        self.text_input.pack()
        space = tk.Label(fm_type, text="", bg=sub3_bg, height=1)
        space.pack()
        
        button = tk.Button(fm_type, text="けってい", font=(main_font, 20), bg=sub3_btn_bg, command=self.ai_answer_sub3)
        button.pack()
        
        space = tk.Label(fm_type, text="", bg=sub3_bg, height=1)
        space.pack()
        label = tk.Label(fm_type, text=f"\"{selected_value_sub3}\"からのしつもんのこたえ", font=(main_font, 21), bg=sub3_bg)
        label.pack()
        #state --- tk.NORMAL：編集できる・tk.DISABLED：編集できない 
        self.text_output = scrolledtext.ScrolledText(fm_type, width=60, height=5, font=(main_font, 20), bg="#fff", state="normal")
        #self.text_output = tk.Text(fm_type, width=80, height=9, state=tk.DISABLED, font=(main_font, 15), bg="#ffffff")
        self.text_output.pack()
        space = tk.Label(fm_type, text="", bg=sub3_bg, height=1)
        space.pack()
        button = tk.Button(fm_type, text="おわる", font=(main_font, 20), bg=sub3_btn_bg, command=self.return_title)
        button.pack(side=tk.RIGHT, padx=30, pady=10)
        button = tk.Button(fm_type, text="もういちど", font=(main_font, 20), bg=sub3_btn_bg, command=self.return_sub3)
        button.pack(side=tk.RIGHT, padx=10, pady=10)
        space = tk.Label(fm_type, text="", bg=sub3_bg, height=1)
        space.pack()
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        
        
    #sub3で入力された質問へのAIの回答
    def ai_answer_sub3(self):
        global type_text_value_sub3
        global selected_value_sub3
        
        #質問する対象を選んでなかった場合
        if len(selected_value_sub3) == 0:
            selected_value_sub3 = "teacher"
            res = messagebox.showerror("Error", "しつもんするひとがえらばれていないよ。\n たいとるへもどるよ。")
            print(res, "Error : No PersonList")
            
            self.return_title()            
            
            
        type_text_value_sub3 = self.text_input.get( "1.0", "end-1c")
        print("AnswerPerson : " + selected_value_sub3)
        print("TypeQuestion : " + type_text_value_sub3)
        logger.log(100, f"AnswerPerson_sub3 : {selected_value_sub3}")
        logger.log(100, f"TypeQuestion_sub3 : {type_text_value_sub3}")

        #エラー防止
        time.sleep(0.1) 
        
        #roleについて設定
        role_sys_1 = str(selected_value_sub3)
        if not role_sys_1:
            role_sys_1:str = "teacher"
        
        #質問について設定
        question_sub3 = str(type_text_value_sub3) 
        if not question_sub3:
            question_sub3:str = "しつもんがにゅうりょくされていなかったみたいだね。\n もういっかいしつもんしたかったら「もういちど」ボタンをおしてね！"
        #ひらがなだけで解答
        if hiragana_on == True:
            question_sub3 = question_sub3 + "という質問について分かりやすくひらがなだけで解答して"
            print(question_sub3)
        else:
            pass
                        
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                #role : 役割, 
                # system :（このチャットのシステム） 
                # user :（チャットを使う側 = 私たち） 
                # assistant : ChatGPT側, 
                # content : メッセージ内容
                {"role": "system", "content": role_sys_1}, 
                {"role": "user", "content": question_sub3},
                #{"role": "assistant", "content": "どういうこと？"},
                #{"role": "user", "content": "もう少し簡単に教えて！！"},
            ]
        )
        
        #ChatGPTからの返答の内容
        global res_content_sub3
        res_content_sub3 = res["choices"][0]["message"]["content"]
        print("AI_Answer : " + res_content_sub3)
        logger.log(100, f"AI_answer : {res_content_sub3}")
        
        global new_answer
        new_answer = f"{selected_value_sub3}：{res_content_sub3}"
        print(new_answer)
        
        #ChatGPTが使えない場合
        #global res_content_sub3
        #res_content_sub3 = "おはよう"
        
        # #エラー防止
        # time.sleep(0.1)
        
        self.output_now_sub3()


    def output_now_sub3(self):
        
        print("output_now_sub3")
        #ウィンドウのテキストを表示
        self.text_output.delete("0.0", tk.END) 
        self.text_output.insert(tk.END, new_answer)
<<<<<<< Updated upstream
        
        #テキストが表示されてから音声を読み上げる
        time.sleep(0.5)
        
        # Voicevoxで音声を読み上げる
        #print(res_content_sub1)
        #text_to_voice(res_content_sub1)
=======
>>>>>>> Stashed changes
        
        # pyttsx3で音声を読み上げる
        engine = pyttsx3.init()
        engine.say(res_content_sub3) 
        engine.runAndWait()
        
        return 0


    #もう一度（sub1）
    def return_sub1(self):
        global count_main, count_sub1, count_sub2, count_sub3, count_sub4, count_mic, count_ans_sub1, count_type
        
        if count_main == True:
            pw_main.destroy()
        elif count_sub1 == True:
            pw_sub1.destroy()
        elif count_sub2 == True:
            pw_sub2.destroy()
        elif count_sub3 == True:
            pw_sub3.destroy()
        elif count_sub4 == True:
            pw_sub4.destroy()
        elif count_mic == True:
            pw_mic.destroy()
        elif count_ans_sub1 == True:
            pw_ans_sub1.destroy()
        elif count_type == True:
            pw_type.destroy()
        else:
            print("Error")
        
        print(str(count_main) + " : " + str(count_sub1) + " : " + str(count_sub2) + " : " + str(count_sub3) + " : " + str(count_sub4) + " : " + str(count_mic) + " : " + str(count_ans_sub1) + " : " + str(count_type))
        
        count_main = False
        count_sub1 = False
        count_sub2 = False
        count_sub3 = False
        count_sub4 = False
        count_mic = False
        count_ans_sub1 = False
        count_type = False
        
        self.create_1()
        
        return 0
    
    
    #もう一度（sub3）
    def return_sub3(self):
        global count_main, count_sub1, count_sub2, count_sub3, count_sub4, count_mic, count_ans_sub1, count_type
        
        if count_main == True:
            pw_main.destroy()
        elif count_sub1 == True:
            pw_sub1.destroy()
        elif count_sub2 == True:
            pw_sub2.destroy()
        elif count_sub3 == True:
            pw_sub3.destroy()
        elif count_sub4 == True:
            pw_sub4.destroy()
        elif count_mic == True:
            pw_mic.destroy()
        elif count_ans_sub1 == True:
            pw_ans_sub1.destroy()
        elif count_type == True:
            pw_type.destroy()
        else:
            print("Error")
        
        print(str(count_main) + " : " + str(count_sub1) + " : " + str(count_sub2) + " : " + str(count_sub3) + " : " + str(count_sub4) + " : " + str(count_mic) + " : " + str(count_ans_sub1) + " : " + str(count_type))
        
        count_main = False
        count_sub1 = False
        count_sub2 = False
        count_sub3 = False
        count_sub4 = False
        count_mic = False
        count_ans_sub1 = False
        count_type = False
        
        self.create_3()
    
    
    #sub4（設定ウィンドウを閉じる）
    def exit_sub4(self):
        global count_main, count_sub1, count_sub2, count_sub3, count_sub4, count_mic, count_ans_sub1, count_type

        if count_sub4 == True:
            pw_sub4.destroy()
        else:
            print("Error")
            
        count_main = False
        count_sub1 = False
        count_sub2 = False
        count_sub3 = False
        count_sub4 = False
        count_mic = False
        count_ans_sub1 = False
        count_type = False
        
        self.create_widgets()
    

    # タイトルへ戻る
    def return_title(self):
        global count_main, count_sub1, count_sub2, count_sub3, count_sub4, count_mic, count_ans_sub1, count_type
        
        if count_main == True:
            pw_main.destroy()
        elif count_sub1 == True:
            pw_sub1.destroy()
        elif count_sub2 == True:
            pw_sub2.destroy()
        elif count_sub3 == True:
            pw_sub3.destroy()
        elif count_sub4 == True:
            pw_sub4.destroy()
        elif count_mic == True:
            pw_mic.destroy()
        elif count_ans_sub1 == True:
            pw_ans_sub1.destroy()
        elif count_type == True:
            pw_type.destroy()
        else:
            print("Error")
        
        print(str(count_main) + " : " + str(count_sub1) + " : " + str(count_sub2) + " : " + str(count_sub3) + " : " + str(count_sub4) + " : " + str(count_mic) + " : " + str(count_ans_sub1) + " : " + str(count_type))
        
        count_main = False
        count_sub1 = False
        count_sub2 = False
        count_sub3 = False
        count_sub4 = False
        count_mic = False
        count_ans_sub1 = False
        count_type = False
        
        self.create_widgets()


#アプリケーションが終了されたとき
def goodbye():
    popup = sg.popup_ok_cancel('アプリケーションを終了しますか？', font=(main_font, 16), text_color='#000000', background_color=main_bg)
    print(popup)
    
    if popup == "OK":
        exit_message = "App Exit"
        #messagebox.showinfo("App Exit", "アプリケーションを終了しました。")
        logger.log(100, exit_message)
        print(exit_message)
        pass
    
    elif popup == "Cancel":
        restart_message = "continue" 
        # 「continue」を引数と捨て再起動関数を実行
        restart(restart_message)
        
        
#再起動
def restart(restart_message):
    
    if restart_message == "continue":
        print("continue... ")
        logger.log(100, "continue")
    
    #Restart python script itself
    os.execv(sys.executable, ['python'] + sys.argv)
    

#pythonプログラムが終了したことを取得してgoodbye関数を実行
atexit.register(goodbye)


        
# 実行
main_window = tk.Tk()       

#画面の幅と高さを取得
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

window_width = 1200
window_height = 720
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 3) - (window_height // 3)

#pyautoguiとモジュールが干渉するためFHDの時（1200x720+168+48）
#x = 168
#y = 48
myapp = Application(master=main_window)
myapp.master.title("GPT-3.5-turbo") # メインウィンドウの名前
myapp.master.geometry(f"{window_width}x{window_height}+{x}+{y}") # ウィンドウの幅と高さピクセル単位で指定（width x height）
#myapp.master.attributes('-fullscreen', True) # フルスクリーン（終了ボタンがなくなるので非推奨）
myapp.mainloop()