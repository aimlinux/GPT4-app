import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from tkinter import scrolledtext 
import tkinter.ttk as ttk
import openai
from io import BytesIO
import os
import speech_recognition as sr
import pyaudio
import wave
import time
import random as rand
import sys
#カレントディレクトリ内
from mic_now import voice_to_text


# ---- APIKey設定 ----
#openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = ""

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
title_font = "Arial"
main_font = "Arial"

button_1 = "ふぁいる"
button_2 = "せってい"
button_3 = "たいとるへ"
button_4 = "ろぐ"

#ひらがなON, OFF
hiragana_on = True

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
all_person_list = ["せんせい", "おかあさん", "あかちゃん", "こいびと", "ちゅうがくせい", "かしこいはかせ", "うま", "おこってるひと", "サッカー選手", "アメリカ人", "こうせんせい", "関西人"]
# 各person_list_windowの大きさと初期配置を決める（メインウィンドウに関してはコード最下部）
global all_person_list_window_size
all_person_list_window_size = "500x600+400+100"
global config_window_size
config_window_size = "500x600+400+100"


# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
        
    def create_widgets(self):
        
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
        
        toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        
        space_label = tk.Label(fm_main, text="", bg=main_bg, height=2)
        space_label.pack(side=tk.TOP)

        title_label = tk.Label(fm_main, text="**** ちゃっとじーぴーてぃーのあぷり ****", bg=main_bg, font=(title_font, 30), height=2)
        title_label.pack(side=tk.TOP)
        
        space_label = tk.Label(fm_main, text="", bg=main_bg, height=7)
        space_label.pack(side=tk.TOP)
    
        start_button = tk.Button(fm_main, text=" ことばでおはなし ", font=(main_font, 20), bg=title_btn_bg, width=30, command=self.create_1)
        start_button.pack(side=tk.TOP, pady=10)
        start_button = tk.Button(fm_main, text=" てがきでおはなし", font=(main_font, 20), bg=title_btn_bg, width=30, command=self.create_2)
        start_button.pack(side=tk.TOP, pady=10)
        start_button = tk.Button(fm_main, text=" てうちでおはなし ", font=(main_font, 20), bg=title_btn_bg, width=30, command=self.create_3)
        start_button.pack(side=tk.TOP, pady=10)
        start_button = tk.Button(fm_main, text=" せってい ", font=(main_font, 20), bg=title_btn_bg, width=30, command=self.create_4)
        start_button.pack(side=tk.TOP, pady=10)
        
        

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
        
        toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS)
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
        
        toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS)
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
        
        pw_sub3 = tk.PanedWindow(self.master, bg=sub3_bg, orient="vertical")
        pw_sub3.pack(expand=True, fill=tk.BOTH, side="left")
        
        fm_sub3 = tk.Frame(bd=15, bg=sub3_bg, relief="ridge")
        pw_sub3.add(fm_sub3)
        
    # -------- メインフレームのオブジェクト作成 --------
        # ボタンを作成してツールバーに配置
        fm_toolbar = tk.Frame(fm_sub3, bg=sub3_bg)
        fm_toolbar.pack(anchor="nw")
        
        toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS)
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
        label = tk.Label(fm_sub3, text="しょうがくせいにはむずかしいかも", bg=sub3_bg, font=(main_font, 25), width=30)
        label.pack(side=tk.TOP, pady=10)
        
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
        
        toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS)
        toolbar_button4.pack(side=tk.LEFT, padx=2, pady=2)
        
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), width=30, height=1)
        space.pack(side=tk.TOP)
        label = tk.Label(fm_sub4, text="---- ひらがなのみモード ----", bg=sub4_bg, font=(main_font, 25), width=30, height=3)
        label.pack(side=tk.TOP, pady=10)
        
        space = tk.Label(fm_sub4, text="", bg=sub4_bg, font=(main_font, 10), width=30, height=1)
        space.pack(side=tk.TOP)
        label = tk.Label(fm_sub4, text="---- おんせいのON OFF ----", bg=sub4_bg, font=(main_font, 25), width=30, height=3)
        label.pack(side=tk.TOP, pady=10)
        
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        

    #config Toplevelウィンドウ（設定）
    def config(self):
        config_window = tk.Toplevel(bg=sub4_bg, bd=2)
        config_window.geometry(config_window_size)
        config_window.title("config_window")
        
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=1)
        space.pack(side=tk.TOP)
        label = tk.Label(config_window, text="---- ひらがなのみモード ----", bg=sub4_bg, font=(main_font, 25), width=30, height=3)
        label.pack(side=tk.TOP, pady=10)
        
        space = tk.Label(config_window, text="", bg=sub4_bg, font=(main_font, 10), height=1)
        space.pack(side=tk.TOP)
        label = tk.Label(config_window, text="---- おんせいのON OFF ----", bg=sub4_bg, font=(main_font, 25), width=30, height=3)
        label.pack(side=tk.TOP, pady=10)
        
        return 0
    
    
    
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
        
        toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS)
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
        
        toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS)
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
        #ひらがなだけで解答する場合
        if hiragana_on == True:
            question_sub1 = str(question_sub1) + "という質問について分かりやすくひらがなで解答して"
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
        
        #ChatGPTからの返答の内容
        res_content = res["choices"][0]["message"]["content"]
        print("AI_Answer : " + res_content)
        
        global new_answer
        new_answer = f"{selected_value_sub1}：{res_content}"
        print(new_answer)
        
        #エラー防止
        time.sleep(0.1)
        
        self.output_now_sub1()

    def output_now_sub1(self):
        
        print("output_now_sub1")
        #ウィンドウのテキストを表示
        self.text_output_sub1.delete("0.0", tk.END) 
        self.text_output_sub1.insert(tk.END, new_answer)
        
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
        
        toolbar_button1 = tk.Button(fm_toolbar, text=button_1, **TOOLBAR_OPUTIONS)
        toolbar_button1.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button2 = tk.Button(fm_toolbar, text=button_2, **TOOLBAR_OPUTIONS, command=self.config)
        toolbar_button2.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button3 = tk.Button(fm_toolbar, text=button_3, **TOOLBAR_OPUTIONS, command=self.return_title)
        toolbar_button3.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar_button4 = tk.Button(fm_toolbar, text=button_4, **TOOLBAR_OPUTIONS)
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
            question_sub3 = question_sub3 + "という質問について分かりやすくひらがなで解答して"
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
        res_content = res["choices"][0]["message"]["content"]
        print("AI_Answer : " + res_content)
        
        global new_answer
        new_answer = f"{selected_value_sub3}：{res_content}"
        print(new_answer)
        
        #エラー防止
        time.sleep(0.1)
        
        self.output_now_sub3()

    def output_now_sub3(self):
        
        print("output_now_sub3")
        #ウィンドウのテキストを表示
        self.text_output.delete("0.0", tk.END) 
        self.text_output.insert(tk.END, new_answer)
        
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
        
        return 0
    
    

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
        
        return 0

        
        
# 実行
main_window = tk.Tk()       

#画面の幅と高さを取得
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()

window_width = 1200
window_height = 720
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 3) - (window_height // 3)

myapp = Application(master=main_window)
myapp.master.title("GPT-3.5-turbo") # メインウィンドウの名前
myapp.master.geometry(f"{window_width}x{window_height}+{x}+{y}") # ウィンドウの幅と高さピクセル単位で指定（width x height）
#myapp.master.attributes('-fullscreen', True) # フルスクリーン（終了ボタンがなくなるので非推奨）
myapp.mainloop()