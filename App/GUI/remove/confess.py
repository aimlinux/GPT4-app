# https://github.com/PySimpleGUI/PySimpleGUI
# https://github.com/aimlinux/computer-festival-2023/blob/main/GUI/pysimplegui/main_3/main_3.py

# -*- coding: utf-8 -*-

#----[pip install pysimplegui]----
#----[pip install pyttsx3]----
#----[pip install pyautogui]----
#----[pip install screeninfo]----
#----[pip install pillow]----
#----[pip install pandas]----
#----[pip install pickle]----
#----[pip install scikit-learn]----


import os
import PySimpleGUI as sg
import random as rand
import pyttsx3
from msilib.schema import Upgrade
from msilib.schema import Binary
from re import U
from turtle import update
import pyautogui as pg
import time
import threading
from PIL import ImageGrab
import win32gui
import sys
import ctypes


#--------機械学習で使用--------
import pandas as pd
import pickle
import warnings
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import KFold
from sklearn import svm

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

warnings.simplefilter('ignore')
#ファイル読み込み
df = pd.read_csv(resource_path("namelist.csv"),sep=",")#Githubとメイン環境はPathは共通



#--------モニターの解像度を取得--------
from screeninfo import get_monitors as gm
monitor = gm()[0]
window_size = (monitor.width, monitor.height)
#print(window_size)



#--------ウィンドウのテーマ--------
#sg.theme('Material1')
sg.theme('LightBlue3')
#ランダムにテーマを変える : sg.theme('SystemDefault8')
#メインテーマ候補 : [LightGreen2, DarkTeal5, LightBlue3]

#--------タイトルバーのアイコンの画像指定（use_custom_titlebar=Trueが指定されている場合のみ有効）--------
#icon_image = 'main_folder/img/icon_img.ico'


a111 = 0
b111 = 0
c111 = 0
d111 = 0
e111 = 0
f111 = 0

com = [0]*12
complete = 0

#time.sleep(0.1)
#sg.popup_ok('アプリケーションを起動します。', font=('Arial', 12), text_color='#ff1493')
#pg.confirm('本当に起動しますか？')
time.sleep(0.2)



#--------各ウィンドウのオブジェクト定義--------
def make_main():
    # ------------ メインウィンドウ作成 ------------
    top_col = [
                [sg.Button('〓メニュー', key='-TopMenu-'), 
                sg.Button('〓テキスト保存', key='-TopPreservation_main-'), 
                sg.Button('〓画面スクショ', key='-Scrot-'),
                sg.Button('〓音声オプション', key='-TopVoice-')], 
    ]
    main_layout = [ 
                [sg.Column(top_col)], 
                [sg.Text('', size=(70, 1))], 
                [sg.Text('ユニークな新単語を生成するアプリケーション', font=('Helvetica', 25),
                text_color='#ff1493', size=(45,2))], 
                [sg.Text('・モードを選択してください', font=('Noto Serif CJK JP', 20),
                text_color='#191970', size=(45, 2))], 
                [sg.Button('入力された文字からユニークな新単語を生成するモード', font=('Arial', 11), size=(50, 2), key='-sub1-')],
                [sg.Button('ひらがなでランダムに単語を生成するモード', font=('Arial', 11), size=(50, 2), key='-sub2-')],
                [sg.Button('カタカナでランダムに単語を生成するモード', font=('Arial', 11), size=(50, 2), key='-sub3-')],
                [sg.Button('ローマ字でランダムに単語を生成するモード', font=('Arial', 11), size=(50, 2), key='-sub4-')],
                [sg.Button('ひらがなで名前をランダムに生成するモード', font=('Arial', 11), size=(50, 2), key='-sub5-')],
                [sg.Button('二つの単語から省略された新しい単語を生成するモード', font=('Arial', 11), size=(50, 2), key='-sub6-')],
                [sg.Text('', size=(70, 1))],
                #[sg.Checkbox('音声OFF', default=None, font=('Arial', 16), key='-volume-')],
                [sg.Text('', size=(70, 1))],
                [sg.Button('アプリケーションを終了する', font=('Arial, 13'), size=(40, 2), key='-exit-')]
    ]
    return sg.Window("アプリ君・甲", main_layout, finalize=True, size=(1300, 920), relative_location=(0, -75), border_depth=2,
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False)


def make_sub1():
    # ------------ サブ１ウィンドウ作成 ------------
    top_col_sub1 = [
                [sg.Button('〓メニュー', key='-TopMenu-'), 
                sg.Button('〓テキスト保存', key='-TopPreservation_sub1-'), 
                sg.Button('〓画面スクショ', key='-Scrot-'),
                sg.Button('〓音声オプション', key='-TopVoice-')], 
    ]
    sub1_layout = [ 
                [sg.Column(top_col_sub1)], 
                #[sg.Text('', size=(80, 1))],  
                [sg.Text('入力された文字からユニークな新単語を生成するよ！！', text_color='#191970', font=('Arial', 18))],
                [sg.Text('', size=(80, 1))],
                [sg.Text('・文字を入力してね', font=('Helvetica', 14))],
                [sg.Text('※ひらがなとカタカナのみで入力して。', font=('Arial', 10))],
                # 文章入力欄を設置
                [sg.Multiline('', font=('Arial', 13), text_color='#191970', size=(60, 4), key='-sentence_1-')],
                [sg.Text('', size=(80, 1))],
                [sg.Button('新単語生成', font=('Arial', 13), key='-generate_1-')], 
                [sg.Button('新単語を読み上げる', font=('Arial', 13), key='-speak_1-')],
                [sg.Output(size=(70, 10), font=('Arial', 13), text_color='#9400d3')], 
                #[sg.Text('言語設定', font=('Arial', 13), text_color='#191970')],
                #[sg.Spin(['ひらがなのみ', 'ひらがな・カタカナ'], font=('Arial', 13), 
                #size=(30,1), initial_value='ひらがな・カタカナ', key='-language-')], 
                [sg.Text('', size=(80, 1))],
                [sg.Button('モード選択画面に戻る',  font=('Arial', 13), size=(60, 1), key='-back-')],
    ]    
    return sg.Window("アプリ君・甲", sub1_layout, finalize=True, size=(1300, 920), relative_location=(0, -75), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False)


def make_sub2():
    # ------------ サブ２ウィンドウ作成 ------------
    top_col_sub2 = [
                [sg.Button('〓メニュー', key='-TopMenu-'), 
                sg.Button('〓テキスト保存', key='-TopPreservation_sub2-'), 
                sg.Button('〓画面スクショ', key='-Scrot-'),
                sg.Button('〓音声オプション', key='-TopVoice-')], 
    ]
    col2 = [    [sg.Text('文字数の上限と下限を入力してね', font=('Arial, 10')), 
                sg.Text('(デフォルトの値は上限が5、下限が2だよ)', font=('Arial, 10'))],
                [sg.Text('※何も値が入っていない時や、ありえないような値が入っているとアプリが落ちる事があるよ。', font=('Arial', 10))],
                [sg.Multiline('5', font=('Arial', 9), text_color='#191970', size=(12, 2), key='-jog_2-'), 
                sg.Multiline('2', font=('Arial', 9), text_color='#191970', size=(12, 2), key='-kag_2-')], 
    ]
    sub2_layout = [ 
                [sg.Column(top_col_sub2)], 
                #[sg.Text('', size=(80, 1))],  
                [sg.Text('ひらがなでランダムに文字を生成するよ！！', font=('Arial', 18), text_color='#191970')],     
                [sg.Text('', size=(80, 1))],
                [sg.Column(col2)], 
                [sg.Button('新単語生成', font=('Arial', 13), key='-generate_2-')],
                [sg.Button('新単語を読み上げる', font=('Arial', 13), key='-speak_2-')],
                [sg.Output(size=(70, 12), font=('Arial', 13), text_color='#9400d3')],
                [sg.Text('', size=(80, 2))],
                [sg.Button('モード選択画面に戻る', font=('Arial', 13), size=(60, 1), key='-back-')],
                [sg.Text('', size=(80, 1))],
    ]    
    return sg.Window('アプリ君・甲', sub2_layout, finalize=True, size=(1300,920), relative_location=(0, -75), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False)


def make_sub3():
    # ------------ サブ３ウィンドウ作成 ------------
    top_col_sub3 = [
                [sg.Button('〓メニュー', key='-TopMenu-'), 
                sg.Button('〓テキスト保存', key='-TopPreservation_sub3-'), 
                sg.Button('〓画面スクショ', key='-Scrot-'),
                sg.Button('〓音声オプション', key='-TopVoice-')], 
    ]
    col3 = [    [sg.Text('文字数の上限と下限を入力してね', font=('Arial, 10')), 
                sg.Text('(デフォルトの値は上限が5、下限が2だよ)', font=('Arial, 10'))],
                [sg.Text('※何も値が入っていない時や、ありえないような値が入っているとアプリが落ちる事があるよ。', font=('Arial', 10))],
                [sg.Multiline('5', font=('Arial', 9), text_color='#191970', size=(12, 2), key='-jog_3-'), 
                sg.Multiline('2', font=('Arial', 9), text_color='#191970', size=(12, 2), key='-kag_3-')], 
    ]
    sub3_layout = [ 
                [sg.Column(top_col_sub3)], 
                #[sg.Text('', size=(80, 1))],  
                [sg.Text('カタカナでランダムに文字を生成するよ！！', font=('Arial', 18), text_color='#191970')],     
                [sg.Text('', size=(80, 1))],
                [sg.Column(col3)], 
                [sg.Button('新単語生成', font=('Arial', 13), key='-generate_3-')],
                [sg.Button('新単語を読み上げる', font=('Arial', 13), key='-speak_3-')],
                [sg.Output(size=(70, 12), font=('Arial', 13), text_color='#9400d3')],
                [sg.Text('', size=(80, 2))],
                [sg.Button('モード選択画面に戻る', font=('Arial', 13), size=(60, 1), key='-back-')],
                [sg.Text('', size=(80, 1))],
    ]    
    return sg.Window('アプリ君・甲', sub3_layout, finalize=True, size=(1300, 920), relative_location=(0, -75), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False)


def make_sub4():
    # ------------ サブ４ウィンドウ作成 ------------
    top_col_sub4 = [
                [sg.Button('〓メニュー', key='-TopMenu-'), 
                sg.Button('〓テキスト保存', key='-TopPreservation_sub4-'), 
                sg.Button('〓画面スクショ', key='-Scrot-'),
                sg.Button('〓音声オプション', key='-TopVoice-')], 
    ]
    col4 = [    [sg.Text('文字数の上限と下限を入力してね', font=('Arial, 10')), 
                sg.Text('(デフォルトの値は上限が5、下限が2だよ)', font=('Arial, 10'))],
                [sg.Text('※何も値が入っていない時や、ありえないような値が入っているとアプリが落ちる事があるよ。', font=('Arial', 10))],
                [sg.Multiline('5', font=('Arial', 9), text_color='#191970', size=(12, 2), key='-jog_4-'), 
                sg.Multiline('2', font=('Arial', 9), text_color='#191970', size=(12, 2), key='-kag_4-')], 
    ]
    sub4_layout = [ 
                [sg.Column(top_col_sub4)],
                #[sg.Text('', size=(80, 1))],  
                [sg.Text('ローマ字でランダムに文字を生成するよ！！', font=('Arial', 18), text_color='#191970')],     
                [sg.Text('', size=(80, 1))],
                [sg.Column(col4)], 
                [sg.Button('新単語生成', font=('Arial', 13), key='-generate_4-')],
                [sg.Button('新単語を読み上げる', font=('Arial', 13), key='-speak_4-')],
                [sg.Output(size=(70, 12), font=('Arial', 13), text_color='#9400d3')],
                [sg.Text('', size=(80, 2))],
                [sg.Button('モード選択画面に戻る', font=('Arial', 13), size=(60, 1), key='-back-')],
                [sg.Text('', size=(80, 1))],
    ]    
    return sg.Window('アプリ君・甲', sub4_layout, finalize=True, size=(1300, 920), relative_location=(0, -75), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False)     


def make_sub5():
    # ------------ サブ５ウィンドウ作成 ------------
    top_col_sub5 = [
                [sg.Button('〓メニュー', key='-TopMenu-'), 
                sg.Button('〓テキスト保存', key='-TopPreservation_sub5-'), 
                sg.Button('〓画面スクショ', key='-Scrot-'),
                sg.Button('〓音声オプション', key='-TopVoice-')], 
    ]
    col5 = [    [sg.Text('文字数の上限と下限を入力してね', font=('Arial, 10')), 
                sg.Text('(デフォルトの値は上限が3、下限が2だよ)', font=('Arial, 10'))],
                [sg.Text('※何も値が入っていない時や、ありえないような値が入っているとアプリが落ちる事があるよ。', font=('Arial', 10))],
                [sg.Multiline('3', font=('Arial', 9), text_color='#191970', size=(12, 2), key='-jog_5-'), 
                sg.Multiline('2', font=('Arial', 9), text_color='#191970', size=(12, 2), key='-kag_5-')], 
    ]  
    sub5_layout = [ 
                [sg.Column(top_col_sub5)],
                #[sg.Text('', size=(80, 1))],  
                [sg.Text('ひらがなで名前をランダムに生成するよ！！', font=('Arial', 18), text_color='#191970')],
                [sg.Text('', size=(80, 1))],                
                [sg.Column(col5)], 
                [sg.Button('新単語生成', font=('Arial', 13), key='-generate_5-')],
                [sg.Button('新単語を読み上げる', font=('Arial', 13), key='-speak_5-')],
                [sg.Output(size=(70,11), font=('Arial', 13), text_color='#9400d3')],
                [sg.Button('機械学習ボタン', font=('Arial', 13), key='-JudgeButton-'), 
                sg.Text('  ', font=('Arial', 13)),
                sg.T('名前がまだ生成されていません。', font=('Arial', 13), text_color='#ff1493', key='-JudgeAnswer-')],
                [sg.Text('珍名コンプリート率 : {} %'.format(complete*100//12),font=('Arial', 13), text_color='#ff1493', key='-complete-')],
                [sg.Text('', size=(80, 1))],
                [sg.Button('モード選択画面に戻る', font=('Arial', 13), size=(60, 1), key='-back-')],
                #[sg.Text('', size=(80, 1))],
    ]    
    return sg.Window('アプリ君・甲', sub5_layout, finalize=True, size=(1300, 920), relative_location=(0, -75), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False)


def make_sub6():
    # ------------ サブ６ウィンドウ作成 ------------
    top_col_sub6 = [
                [sg.Button('〓メニュー', key='-TopMenu-'), 
                sg.Button('〓テキスト保存', key='-TopPreservation_sub6-'), 
                sg.Button('〓画面スクショ', key='-Scrot-'),
                sg.Button('〓音声オプション', key='-TopVoice-')], 
    ]
    sub6_layout = [ 
                [sg.Column(top_col_sub6)],
                [sg.Text('二つの単語をいい感じに組み合わせるよ！！', font=('Arial', 18), text_color='#191970')],
                [sg.Text('', size=(80, 1))],  
                [sg.Text('・二つの単語を入力してね', font=('Helvetica', 14))], 
                [sg.Text('※ひらがなとカタカナのみで入力して。', font =('Arial', 10))],
                [sg.Text('１単語目 : ', font=('Arial', 12)), 
                sg.Multiline('', font=('Arial', 10), text_color='#191970', size=(40, 2), key='-FirstItem-')], 
                [sg.Text('２単語目 : ', font=('Arial', 12)), 
                sg.Multiline('', font=('Arial', 10), text_color='#191970', size=(40, 2), key='-SecondItem-')], 
                [sg.Text('', size=(80, 1))],
                [sg.Button('新単語生成', font=('Arial', 13), key='-generate_6-')],
                [sg.Button('新単語を読み上げる', font=('Arial', 13), key='-speak_6-')],
                [sg.Output(size=(70, 10), font=('Arial', 13), text_color='#9400d3')],
                [sg.Text('', size=(80, 1))],
                [sg.Text('', size=(80, 1))],
                [sg.Button('モード選択画面に戻る',  font=('Arial', 13), size=(60, 1), key='-back-')],
    ]           
    return sg.Window('アプリ君・甲', sub6_layout, finalize=True, size=(1300, 920), relative_location=(0, -75), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False)



# --------起動時アニメーション（本物）--------

voc = pd.read_csv(resource_path("voc.csv"))#メイン環境
#voc = pd.read_csv("main_folder/voc.csv")#Github環境
tex = pd.read_csv(resource_path("test1.csv"))#メイン環境
#tex = pd.read_csv("main_folder/test1.csv")#Github環境

voc = voc.sample(frac=1, ignore_index=True)


canvas = sg.Canvas(size=(1300,920),pad=((0,0),(0,0)))

def openning(canvas):
    openning = [
        [canvas]
                ]
    return sg.Window("アプリ君・甲", openning,size=(1300,920),relative_location=(0, -75),
                    border_depth=2, resizable=False, finalize=True, 
                    right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)

window = openning(canvas)

def click():
    while True:
        if ctypes.windll.user32.GetAsyncKeyState(0x01) == 0x8000:
            global stop_thread,lap
            lap = 0
            if stop_thread:
                break

stop_thread = False
lap = 22
thread1 = threading.Thread(target=click)
thread1.start()

# 各デフォルト値を定義
default_voice_slider = 5
default_speed_slider = 5

# 音声を「滑らかな女性の声」に設定（男性の声は現在使用できない）
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices_woman', voices[1].id)


def kou():
    j=0
    for i in range(185):
        canvas.tk_canvas.delete("k")
        canvas.tk_canvas.create_line(0+i*17,110,-400+i*17,110,fill="#191970",width=38,tag="k")
        if i < 57:
            canvas.tk_canvas.create_line(-102+i*17,230,-502+i*17,230,fill="#191970",width=38,tag="k")
        else:
            canvas.tk_canvas.create_line(450,230,850,230,fill="#191970",width=38,tag="k")
        if i < 63:
            canvas.tk_canvas.create_line(-204+i*17,360,-604+i*17,360,fill="#191970",width=38,tag="k")
        else:
            canvas.tk_canvas.create_line(450,360,850,360,fill="#191970",width=38,tag="k")
        if i < 69:
            canvas.tk_canvas.create_line(-306+i*17,500,-706+i*17,500,fill="#191970",width=38,tag="k")
        else:
            canvas.tk_canvas.create_line(450,500,850,500,fill="#191970",width=38,tag="k")
        canvas.tk_canvas.create_line(-408+i*17,650,-808+i*17,650,fill="#191970",width=38,tag="k")
        canvas.tk_canvas.create_line(-510+i*17,810,-910+i*17,810,fill="#191970",width=38,tag="k")

        canvas.tk_canvas.create_line(50,2201-i*17,50,2517-i*17,fill="#191970",width=38,tag="k")  
        canvas.tk_canvas.create_line(250,-1003+i*17,250,-1319+i*17,fill="#191970",width=38,tag="k")
        if i <  130:
            canvas.tk_canvas.create_line(450,2405-i*17,450,2721-i*17,fill="#191970",width=38,tag="k") 
        else:
            canvas.tk_canvas.create_line(450,211,450,527,fill="#191970",width=38,tag="k")
        if i < 114:
            canvas.tk_canvas.create_line(650,-1207+i*17,650,-1696+i*17,fill="#191970",width=38,tag="k") 
        else:
            canvas.tk_canvas.create_line(650,211,650,700,fill="#191970",width=38,tag="k")
        if i < 142:
            canvas.tk_canvas.create_line(850,2607-i*17,850,2923-i*17,fill="#191970",width=38,tag="k") 
        else:
            canvas.tk_canvas.create_line(850,211,850,527,fill="#191970",width=38,tag="k")
        canvas.tk_canvas.create_line(1050,-1411+i*17,1050,-1727+i*17,fill="#191970",width=38,tag="k") 
        canvas.tk_canvas.create_line(1250,2811-i*17,1250,3127-i*17,fill="#191970",width=38,tag="k") 

        jimaku(voc,tex,i)
    
        j += 1
        canvas.tk_canvas.after(lap)
        canvas.tk_canvas.update()
    for j in range(100):
        j = j + 185
        jimaku(voc,tex,j)
        canvas.tk_canvas.after(lap)
        canvas.tk_canvas.update()


    for i in range(35):
        canvas.tk_canvas.delete("text","k")
        canvas.tk_canvas.create_text(280+i*7,400,fill="#c71585",text="アプリ君",font=("Arial",24+i),tag="text")
        canvas.tk_canvas.create_line(450+375/35*i,211+140/35*i,450+375/35*i,527-114/35*i,fill="#191970",width=38-0.8*i,tag="k")
        canvas.tk_canvas.create_line(450+375/35*i,230+126/35*i,850+51/35*i,230+126/35*i,fill="#191970",width=38-0.8*i,tag="k")
        canvas.tk_canvas.create_line(850+51/35*i,211+140/35*i,850+51/35*i,527-114/35*i,fill="#191970",width=38-0.8*i,tag="k")
        canvas.tk_canvas.create_line(450+375/35*i,360+21/35*i,850+51/35*i,360+21/35*i,fill="#191970",width=38-0.8*i,tag="k")
        canvas.tk_canvas.create_line(450+375/35*i,500-94/35*i,850+51/35*i,500-94/35*i,fill="#191970",width=38-0.8*i,tag="k")
        canvas.tk_canvas.create_line(650+212/35*i,211+145/35*i,650+212/35*i,700-256/35*i,fill="#191970",width=38-0.8*i,tag="k") 
        canvas.tk_canvas.after(lap)
        canvas.tk_canvas.update() 

#  ↑ 5.768s
def jimaku(voc,tex,i):
        canvas.tk_canvas.delete("text")
        if i < 186:
            canvas.tk_canvas.create_text(3240-i*16,400,fill="#ffffff",text="アプリ君",font=("Arial",24),tag="text")
        else:
            canvas.tk_canvas.create_text(280,400,fill="#ffffff",text="アプリ君",font=("Arial",24),tag="text")
        for j in range(len(tex)):
            x = tex["x"][j]-i*tex["speed"][j]
            if x > -100 :
                canvas.tk_canvas.create_text(x,int(tex["y"][j]),text=voc["voc"][j%352],fill="#ffffff",font=("Arial",12+int(tex["size"][j])*4),tag="text")


kou()
canvas.tk_canvas.after(2000)

stop_thread = True
window.close()
time.sleep(0.02)



# 各解の初期化
cc_sub1 = 'NULL'
cc_sub2 = 'NULL'
cc_sub3 = 'NULL'
cc_sub4 = 'NULL'
cc_sub5 = 'NULL'
cc_sub6 = 'NULL'


# 各デフォルト値を定義
default_voice_slider = 5
default_speed_slider = 5

# 音声を「滑らかな女性の声」に設定（男性の声は現在使用できない）
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices_woman', voices[1].id)




# ----------------最初に表示するウィンドウを指定する----------------
window = make_main()

#--------ウィンドウを繰り返し表示する--------
while True:
    event, values = window.read()
            


# ----------------右クリックオプション（Exitを除く）----------------
    if event == 'Click':
        pg.click(button='left')
        
        
    if event == 'Home':
        window.close()
        window = make_main()
        
        
    if event == 'Restart':
        sg.popup_ok_cancel('アプリケーションを再起動します。', font=('Arial', 12), text_color='#ff1493')
        #pg.confirm('本当に再起動します？')
        window.close()
        time.sleep(0.2)
        window = make_main()
        continue
    
    
    if event == 'Force Quit':
        window.close()
        pg.alert('アプリケーションを強制終了します。')
        break
    
    
#----------------Topオプション----------------

#--------Topメニューを押したとき--------
    if event == '-TopMenu-':
        pg.click(button='right')

        
#--------txtファイルへのテキストの保存--------

#--------メインウィンドウ--------
    if event == '-TopPreservation_main-':
        sg.popup_ok('ここではファイルを書き込みできないよ...',
                'モードを選択してね！！', text_color='#ff1493', font=('Arial', 12))
        
#--------サブ1ウィンドウ--------
    if event == '-TopPreservation_sub1-':
        Origin_window_sub1 = window
        TxtFile_sub1 = 0
        open_file_sub1 = [
            [sg.Text('出力されたテキストをtxtファイルに保存するよ。', font=('Helvetica', 15), text_color='#191970')],
            [sg.Text('', size=(10, 1))],
            [sg.FileBrowse('.txtファイル'),
            sg.InputText(key='-InputTxt_sub1-')], 
            [sg.Button('テキストを書き込む', key='-WriteTxt_sub1-')], 
            [sg.Text('', size=(10, 1))],
            [sg.Text('※必ず戻るボタンを押して戻ってね。')],
            [sg.Text('    ここでは右上の×ボタンは押さないでね。')],
            [sg.Button('戻る', key='-FileExit_sub1-')]
        ]   
        window = sg.Window('アプリ君・甲', open_file_sub1, relative_location=(0,0), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)

    if event == '-WriteTxt_sub1-' and not values['-InputTxt_sub1-']:
        sg.popup_ok('txtファイルが選択されていないよ...', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
    
    elif event == '-WriteTxt_sub1-':
        TxtFile_sub1 = values['-InputTxt_sub1-']
        f_txt = open(TxtFile_sub1, 'a', encoding='UTF-8')
        f_txt.write(cc_sub1)
        f_txt.write('\n')
        f_txt.close()
        
    if event == '-FileExit_sub1-':
        window.close()
        window = Origin_window_sub1
    

#--------サブ2ウィンドウ--------
    if event == '-TopPreservation_sub2-':
        Origin_window_sub2 = window
        TxtFile_sub2 = 0
        open_file_sub2 = [
            [sg.Text('出力されたテキストをtxtファイルに保存するよ。', font=('Helvetica', 15), text_color='#191970')],
            [sg.Text('', size=(10, 1))],
            [sg.FileBrowse('.txtファイル'),
            sg.InputText(key='-InputTxt_sub2-')], 
            [sg.Button('テキストを書き込む', key='-WriteTxt_sub2-')], 
            [sg.Text('', size=(10, 1))],
            [sg.Text('※必ず戻るボタンを押して戻ってね。')],
            [sg.Text('    ここでは右上の×ボタンは押さないでね。')],
            [sg.Button('戻る', key='-FileExit_sub2-')]
        ]   
        window = sg.Window('アプリ君・甲', open_file_sub2, relative_location=(0,0), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)
        
    if event == '-WriteTxt_sub2-' and not values['-InputTxt_sub2-']:
        sg.popup_ok('txtファイルが選択されていないよ...', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-WriteTxt_sub2-':
        TxtFile_sub2 = values['-InputTxt_sub2-']
        f_txt = open(TxtFile_sub2, 'a', encoding='UTF-8')
        f_txt.write(cc_sub2)
        f_txt.write('\n')
        f_txt.close()
    
    if event == '-FileExit_sub2-':
        window.close()
        window = Origin_window_sub2
        
        
#--------サブ3ウィンドウ--------
    if event == '-TopPreservation_sub3-':
        Origin_window_sub3 = window
        TxtFile_sub3 = 0
        open_file_sub3 = [
            [sg.Text('出力されたテキストをtxtファイルに保存するよ。', font=('Helvetica', 15), text_color='#191970')],
            [sg.Text('', size=(10, 1))],
            [sg.FileBrowse('.txtファイル'),
            sg.InputText(key='-InputTxt_sub3-')], 
            [sg.Button('テキストを書き込む', key='-WriteTxt_sub3-')], 
            [sg.Text('', size=(10, 1))],
            [sg.Text('※必ず戻るボタンを押して戻ってね。')],
            [sg.Text('    ここでは右上の×ボタンは押さないでね。')],
            [sg.Button('戻る', key='-FileExit_sub3-')]
        ]   
        window = sg.Window('アプリ君・甲', open_file_sub3, relative_location=(0,0), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)
        
    if event == '-WriteTxt_sub3-' and not values['-InputTxt_sub3-']:
        sg.popup_ok('txtファイルが選択されていないよ...', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-WriteTxt_sub3-':
        TxtFile_sub3 = values['-InputTxt_sub3-']
        f_txt = open(TxtFile_sub3, 'a', encoding='UTF-8')
        f_txt.write(cc_sub3)
        f_txt.write('\n')
        f_txt.close()
    
    if event == '-FileExit_sub3-':
        window.close()
        window = Origin_window_sub3


#--------サブ4ウィンドウ--------
    if event == '-TopPreservation_sub4-':
        Origin_window_sub4 = window
        TxtFile_sub4 = 0
        open_file_sub4 = [
            [sg.Text('出力されたテキストをtxtファイルに保存するよ。', font=('Helvetica', 15), text_color='#191970')],
            [sg.Text('', size=(10, 1))],
            [sg.FileBrowse('.txtファイル'),
            sg.InputText(key='-InputTxt_sub4-')], 
            [sg.Button('テキストを書き込む', key='-WriteTxt_sub4-')], 
            [sg.Text('', size=(10, 1))],
            [sg.Text('※必ず戻るボタンを押して戻ってね。')],
            [sg.Text('    ここでは右上の×ボタンは押さないでね。')],
            [sg.Button('戻る', key='-FileExit_sub4-')]
        ]   
        window = sg.Window('アプリ君・甲', open_file_sub4, relative_location=(0,0), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)
        
    if event == '-WriteTxt_sub4-' and not values['-InputTxt_sub4-']:
        sg.popup_ok('txtファイルが選択されていないよ...', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-WriteTxt_sub4-':
        TxtFile_sub4 = values['-InputTxt_sub4-']
        f_txt = open(TxtFile_sub4, 'a', encoding='UTF-8')
        f_txt.write(cc_sub4)
        f_txt.write('\n')
        f_txt.close()
    
    if event == '-FileExit_sub4-':
        window.close()
        window = Origin_window_sub4


#--------サブ5ウィンドウ--------
    if event == '-TopPreservation_sub5-':
        Origin_window_sub5 = window
        TxtFile_sub5 = 0
        open_file_sub5 = [
            [sg.Text('出力されたテキストをtxtファイルに保存するよ。', font=('Helvetica', 15), text_color='#191970')],
            [sg.Text('', size=(10, 1))],
            [sg.FileBrowse('.txtファイル'),
            sg.InputText(key='-InputTxt_sub5-')], 
            [sg.Button('テキストを書き込む', key='-WriteTxt_sub5-')], 
            [sg.Text('', size=(10, 1))],
            [sg.Text('※必ず戻るボタンを押して戻ってね。')],
            [sg.Text('    ここでは右上の×ボタンは押さないでね。')],
            [sg.Button('戻る', key='-FileExit_sub5-')]
        ]   
        window = sg.Window('アプリ君・甲', open_file_sub5, relative_location=(0,0), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)
        
    if event == '-WriteTxt_sub5-' and not values['-InputTxt_sub5-']:
        sg.popup_ok('txtファイルが選択されていないよ...', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-WriteTxt_sub5-':
        TxtFile_sub5 = values['-InputTxt_sub5-']
        f_txt = open(TxtFile_sub5, 'a', encoding='UTF-8')
        f_txt.write(cc_sub5)
        f_txt.write('\n')
        f_txt.close()
    
    if event == '-FileExit_sub5-':
        window.close()
        window = Origin_window_sub5


    
#--------サブ6ウィンドウ--------
    if event == '-TopPreservation_sub6-':
        Origin_window_sub6 = window
        TxtFile_sub6 = 0
        open_file_sub6 = [
            [sg.Text('出力されたテキストをtxtファイルに保存するよ。', font=('Helvetica', 15), text_color='#191970')],
            [sg.Text('', size=(10, 1))],
            [sg.FileBrowse('.txtファイル'),
            sg.InputText(key='-InputTxt_sub6-')], 
            [sg.Button('テキストを書き込む', key='-WriteTxt_sub6-')], 
            [sg.Text('', size=(10, 1))],
            [sg.Text('※必ず戻るボタンを押して戻ってね。')],
            [sg.Text('    ここでは右上の×ボタンは押さないでね。')],
            [sg.Button('戻る', key='-FileExit_sub6-')]
        ]   
        window = sg.Window('アプリ君・甲', open_file_sub6, relative_location=(0,0), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)
        
    if event == '-WriteTxt_sub6-' and not values['-InputTxt_sub6-']:
        sg.popup_ok('txtファイルが選択されていないよ...', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-WriteTxt_sub6-':
        TxtFile_sub6 = values['-InputTxt_sub6-']
        f_txt = open(TxtFile_sub6, 'a', encoding='UTF-8')
        f_txt.write(cc_sub6)
        f_txt.write('\n')
        f_txt.close()
    
    if event == '-FileExit_sub6-':
        window.close()
        window = Origin_window_sub6
    


    
#-------TopOptionのボイス設定--------
    if event == '-TopVoice-':
        Origin_window_Voice = window
        voice_option = [
            [sg.Text('アプリケーション内の音声設定画面', font=('Helvetica', 15), text_color='#191970')],
            [sg.Text('', size=(10, 1))],
            #音量調節
            [sg.Text('===音量調節===')],
            [sg.Slider(range=(0, 10), default_value=default_voice_slider, resolution=1, tick_interval=5, orientation='horizontal', 
                        enable_events=True, font='Helvetica', text_color='#000000', trough_color='#fae1e9', 
                        expand_x=True, expand_y=True, metadata=True, key='-VoiceSlider-'), 
            sg.Button('確定する', key='-VoiceChange-')],
            [sg.Text('', size=(10, 1))],
            #音声スピード調節
            [sg.Text('===音声スピード調節===')],
            [sg.Slider(range=(0, 10), default_value=default_speed_slider, resolution=1, tick_interval=5, orientation='horizontal', 
                        enable_events=True, font='Helvetica', text_color='#000000', trough_color='#fae1e9', 
                        expand_x=True, expand_y=True, metadata=True, key='-SpeedSlider-'), 
            sg.Button('確定する', key='-SpeedChange-')],
            [sg.Text('※必ず戻るボタンを押して戻ってね。', font=('Arial', 11))],
            [sg.Text('    ここでは右上の×ボタンは押さないでね。', font=('Arial', 11))],
            #ウィンドウを閉じる
            [sg.Button('戻る', key='-VoiceExit-')],
        ]
        window = sg.Window('アプリ君・甲', voice_option, size=(700, 500), relative_location=(0,0), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)

    #--------音量調節の設定--------
    if event == '-VoiceSlider-':
        voice_volume = int(values['-VoiceSlider-'])
        #print(voice_volume)
        window['-VoiceSlider-'].update
        
    if event == '-VoiceChange-':
        engine = pyttsx3.init()
        engine.setProperty('volume', voice_volume / 10)#デフォルト値は1.0
        volume = engine.getProperty('volume')
        sg.popup_ok('音量が変更されたよ。', text_color='#191970', keep_on_top=True)
        default_voice_slider = voice_volume
        
    #--------音声スピードの設定--------
    if event == '-SpeedSlider-':
        voice_speed = int(values['-SpeedSlider-'])
        #print(voice_speed)
        window['-SpeedSlider-'].update
        
    if event == '-SpeedChange-':
        engine = pyttsx3.init()
        engine.setProperty('rate', voice_speed * 40)#デフォルト値は200
        rate = engine.getProperty('rate')
        sg.popup_ok('音声スピードが変更されたよ', text_color='#191970', keep_on_top=True)
        default_speed_slider = voice_speed
        
    #--------戻るボタンが押されたとき--------
    if event == '-VoiceExit-':
        window.close()
        window = Origin_window_Voice




#--------Topオプションの画面スクショ---------
    if event == '-Scrot-':
        
        # 元のウィンドウを取得してスクショ
        handle = win32gui.GetForegroundWindow()
        rect = win32gui.GetWindowRect(handle)
        screenshot = ImageGrab.grab()
        croped_screenshot = screenshot = screenshot.crop(rect)
        
        #スクショした時刻をint型で取得
        time_scr = int(time.time())
        #sg.popup(time_scr)
        
        #----スクショ音声を読み上げる----
        engine = pyttsx3.init()
        engine.say('カシャっカシャっカシャっ')
        engine.runAndWait()
        
        Origin_window_scr = window
        time.sleep(0.2)
        
        make_scr = [
            [sg.Text('保存先を決めて画像を保存できるよ。', font=('Helvetica', 15), text_color='#191970')],
            [sg.Text('', size=(10, 1))],
            [sg.FolderBrowse('保存先フォルダ'),
            sg.InputText(key='-InputScrot-')], 
            [sg.Button('確定する', key='-SaveScrot-')], 
            [sg.Text('', size=(10, 1))],
            [sg.Text('Path :', font=('Arial', 12), text_color='#ff1493'), 
            sg.Text('なし', font=('Arial', 12), text_color='#ff1493', key='-ScrPathAnswer-'), 
            sg.Text('', font=('Arial', 12), text_color='#ff1493')], 
            [sg.Text('※必ず戻るボタンを押して戻ってね。')],
            [sg.Text('   ここでは右上の×ボタンは押さないでね。')],
            [sg.Button('戻る', key='-ScrotExit-')],
        ]   
        window = sg.Window('アプリ君・甲', make_scr, relative_location=(0,0), border_depth=2, 
                    use_default_focus=True, resizable=True, right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                    right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                    right_click_menu_tearoff=False, keep_on_top=True)


    #保存を確定が押されたとき
    if event == '-SaveScrot-':
        scr_path = values['-InputScrot-']
        #sg.popup(scr_path)
        
        if not scr_path:
            sg.popup('保存するフォルダが選択されていないよ...', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        else:
            scr_path_2 = str(scr_path) + '/screenshot_' + str(time_scr) + '.png'
            scr_popup = '画像は 「' + str(scr_path_2) + '」 に保存されたよ。'
            sg.popup(scr_popup, font=('Arial', 12), keep_on_top=True)
        
            #「scr_path_2」にスクショを保存
            croped_screenshot.save(scr_path_2, quality = 90)
            
            #「Path : なし」をアップデート（書き換え）
            window['-ScrPathAnswer-'].update(scr_path_2)


    #「戻る」が押されたとき
    if event == '-ScrotExit-':
        window.close()
        window = Origin_window_scr
        





#-------ウィンドウが閉じたとき or Exit（右クリックオプション）が押されたとき--------

    if (event == sg.WIN_CLOSED or event == 'Exit') and (a111+b111+c111+d111+e111+f111) == 6:     
            window.close()  
            #end_popup = sg.popup_ok('アプリケーションを終了します。', font=('Arial', 12), text_color='#ff1493')
            

    #--------パーフェクトエンディング--------
        # --------パーフェクトエンディングアニメーションの準備--------
            voc = pd.read_csv(resource_path("voc.csv"))#メイン環境
            #voc = pd.read_csv("main_folder/voc.csv")#Github環境
            tex = pd.read_csv(resource_path("test1.csv"))#メイン環境
            #tex = pd.read_csv("main_folder/test1.csv")#Github環境

            voc = voc.sample(frac=1, ignore_index=True)

            canvas = sg.Canvas(size=(1300,920),pad=((0,0),(0,0)))
        
            def ending_1(canvas):
                ending_1 = [
                    [canvas]
                            ]
                return sg.Window("アプリ君・甲", ending_1,size=(1300,920),relative_location=(0, -75),
                                border_depth=2, resizable=False, finalize=True, 
                                right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                                right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                                right_click_menu_tearoff=False, keep_on_top=True)


            window = ending_1(canvas)

            def kou():
                j=0
        
                for i in range(185):
            
                    jimaku(voc,tex,i)
                    j += 1
                    canvas.tk_canvas.after(22)
                    canvas.tk_canvas.update()
            
                for j in range(185):
                    j = j + 185
                    jimaku(voc,tex,j)
                    canvas.tk_canvas.after(22)
                    canvas.tk_canvas.update()

                for i in range(53):
                    canvas.tk_canvas.delete("text","k")
                    canvas.tk_canvas.create_text(280+i*7,400,fill="#c71585",text="パーフェクト",font=("Arial",24+i),tag="text")
                    canvas.tk_canvas.after(22)
                    canvas.tk_canvas.update() 

            #  ↑ 5.768s
            def jimaku(voc,tex,i):
                    canvas.tk_canvas.delete("text")
                    if i < 186:
                        canvas.tk_canvas.create_text(3240-i*16,400,fill="#c71585",text="パーフェクト",font=("Arial",24),tag="text")
                    else:
                        canvas.tk_canvas.create_text(280,400,fill="#c71585",text="パーフェクト",font=("Arial",24),tag="text")
                    for j in range(len(tex)):
                        x = tex["x"][j]-i*tex["speed"][j]
                        if x > -100 :
                            canvas.tk_canvas.create_text(x,int(tex["y"][j]),text=voc["voc"][j%100],fill="#c71585",font=("Arial",10+int(tex["size"][j])*4),tag="text")

            kou()

            time.sleep(2)

            window.close()
            end_popup = sg.popup_ok('全モードコンプリートおめでとう！！', font=('Arial', 12), text_color='#ff1493')
            break


    elif event == sg.WIN_CLOSED or event == 'Exit':
        window.close()  
        Origin_window_end = window
        #end_popup = sg.popup_ok('アプリケーションを終了します。', font=('Arial', 12), text_color='#ff1493')
        

    #if end_popup == 'Cancel':
        #message = 'Cancelが押されました。'
        #window['result'].update(message)
        #sg.popup('アプリケーションを続行します。')
        
    #if end_popup == 'OK':

    #--------エンディング--------
    # --------エンディングアニメーションの準備--------
        voc = pd.read_csv(resource_path("voc.csv"))#メイン環境
        #voc = pd.read_csv("main_folder/voc.csv")#Github環境
        tex = pd.read_csv(resource_path("test1.csv"))#メイン環境
        #tex = pd.read_csv("main_folder/test1.csv")#Github環境

        voc = voc.sample(frac=1, ignore_index=True)

        canvas = sg.Canvas(size=(1300,920),pad=((0,0),(0,0)))
    
        def ending_1(canvas):
            ending_1 = [
                [canvas]
                        ]
            return sg.Window("アプリ君・甲", ending_1,size=(1300,920),relative_location=(0, -75),
                            border_depth=2, resizable=False, finalize=True, 
                            right_click_menu=['Unused', ['Click', 'Home', 'Restart', 'Properties', 'Force Quit', 'Exit']], 
                            right_click_menu_font='Helvetica', right_click_menu_text_color='#000000', right_click_menu_selected_colors='#da70d6',
                            right_click_menu_tearoff=False, keep_on_top=True)


        window = ending_1(canvas)

        def kou():
            j=0
    
            for i in range(185):
        
                jimaku(voc,tex,i)
                j += 1
                canvas.tk_canvas.after(22)
                canvas.tk_canvas.update()
        
            for j in range(185):
                j = j + 185
                jimaku(voc,tex,j)
                canvas.tk_canvas.after(22)
                canvas.tk_canvas.update()

            for i in range(53):
                canvas.tk_canvas.delete("text","k")
                canvas.tk_canvas.create_text(280+i*7,400,fill="#c71585",text="おわり",font=("Arial",24+i),tag="text")
                canvas.tk_canvas.after(22)
                canvas.tk_canvas.update()
            canvas.tk_canvas.create_text(875,400,fill="#c71585",text='.',font=("Arial",78))
            canvas.tk_canvas.after(500)
            canvas.tk_canvas.update()
            canvas.tk_canvas.create_text(925,400,fill="#c71585",text='.',font=("Arial",78))
            canvas.tk_canvas.after(500)
            canvas.tk_canvas.update()
            canvas.tk_canvas.create_text(975,400,fill="#c71585",text='.',font=("Arial",78)) 
            canvas.tk_canvas.after(500)
            canvas.tk_canvas.update()


        #  ↑ 5.768s
        def jimaku(voc,tex,i):
                canvas.tk_canvas.delete("text")
                if i < 186:
                    canvas.tk_canvas.create_text(3240-i*16,400,fill="#c71585",text="おわり",font=("Arial",24),tag="text")
                else:
                    canvas.tk_canvas.create_text(280,400,fill="#c71585",text="おわり",font=("Arial",24),tag="text")
                for j in range(len(tex)):
                    x = tex["x"][j]-i*tex["speed"][j]
                    if x > -100 :
                        canvas.tk_canvas.create_text(x,int(tex["y"][j]),text=voc["voc"][j%100],fill="#c71585",font=("Arial",10+int(tex["size"][j])*4),tag="text")

        kou()

        time.sleep(2)

        window.close()
        break



    
    
    
    

#--------sub1ボタンが押された場合--------
    if event == "-sub1-":
        # メインウィンドウを閉じて、サブ１ウィンドウを作成して表示する
        window.close()
        window = make_sub1()
        
#--------サブ１のウィンドウについての設定--------    
    if event == '-generate_1-':
        a111 = 1
        c_sub1 = values['-sentence_1-']
        #print(c_sub1)
        #入力されたリストをランダムに並べ替える
        x_sub1=189
        f_sub1=open(resource_path("hrkt.bin"),"rb")
        a_sub1=[]
        for i_sub1 in range(x_sub1):
            aa_sub1=[]
            for j_sub1 in range(x_sub1):
                b_sub1=f_sub1.read(2)
                aaa_sub1=b_sub1[0]*256+b_sub1[1]
                aa_sub1=aa_sub1+[aaa_sub1]
            a_sub1=a_sub1+[aa_sub1]
        f_sub1.close

        cc_sub1=[0]
        enc_sub1=c_sub1.encode("utf-8")
        for i_sub1 in range(len(c_sub1)):
            cc_sub1=cc_sub1+[enc_sub1[i_sub1*3+2]-128+(enc_sub1[i_sub1*3+1]-129)*64]
        cc_sub1=cc_sub1+[0]

        n_sub1=0
        while True:
            n_sub1+=1
            sum_sub1=0
            while sum_sub1==0:
                r_sub1=rand.randint(0,len(c_sub1))
                aa_sub1=[0]*(x_sub1-1)
                sum_sub1=0
                for j_sub1 in range(x_sub1-1):
                    i_sub1=j_sub1+1
                    aa_sub1[j_sub1]=a_sub1[cc_sub1[r_sub1]][i_sub1]*a_sub1[i_sub1][cc_sub1[r_sub1+1]]
                    sum_sub1=sum_sub1+aa_sub1[j_sub1]
            #print(sum)

            rr_sub1=rand.randint(1,sum_sub1)
            count_sub1=0
            i_sub1=0
            while count_sub1<rr_sub1:
                count_sub1=count_sub1+aa_sub1[i_sub1]
                i_sub1=i_sub1+1
            cc_sub1=cc_sub1[:r_sub1+1]+[i_sub1]+cc_sub1[r_sub1+1:]
            #cc_sub1=cc_sub1[1:]
            if rand.randint(0,9+(n_sub1==1)*11)<6:
                break

        ccc_sub1=[]
        for i_sub1 in range(1,len(c_sub1)+n_sub1+1):
            ccc_sub1=ccc_sub1+[227,129+int(cc_sub1[i_sub1]/64),cc_sub1[i_sub1]+128-int(cc_sub1[i_sub1]/64)*64]
        c_sub1=bytes(ccc_sub1).decode("utf-8")
        print(c_sub1)
        # --ランダムに生成--
        # print(rand.choice(cc_sub1, k=len(cc_sub1)))

        #----新単語を読み上げる----
        engine = pyttsx3.init()
        engine.say(c_sub1)
        engine.runAndWait()

    # --ボタンを押したら繰り返し再生--
    #if event == '-speak_1-' and cc_sub1 == 'NULL':
        #sg.popup_ok('新単語が生成されていません。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-speak_1-':
        engine = pyttsx3.init()
        engine.say(c_sub1) 
        engine.runAndWait()
            
    # window右上のx印を押して閉じたとき
    if event == sg.WIN_CLOSED: 
        break
        
        
        
#--------sub2ボタンが押された場合--------
    elif event == '-sub2-':
        # メインウィンドウを閉じて、サブ２ウィンドウを作成して表示する
        window.close()
        window = make_sub2()
    
    
#--------サブ２のウィンドウについての設定--------    
    if event == '-generate_2-':
        b111 = 1
        #03.01修正箇所は最後にコメント
        kagen_sub2 = int(values['-kag_2-'])#
        jogen_sub2 = int(values['-jog_2-'])#
        #--------各環境で相対パスを変更しよう！！--------
        f_sub2=open(resource_path("hira2.bin"),"rb")#メイン環境
        #f_sub2=open("main_folder\hira2.bin","rb")#Github環境
        sum_sub2=[0]*85
        a_sub2=[]
        for i_sub2 in range(85):
            aa_sub2=[]
            for j_sub2 in range(85):
                b_sub2=f_sub2.read(2)
                aaa_sub2=b_sub2[0]*256+b_sub2[1]
                aa_sub2=aa_sub2+[aaa_sub2]
                sum_sub2[i_sub2]=sum_sub2[i_sub2]+aaa_sub2
            a_sub2=a_sub2+[aa_sub2]
        f_sub2.close
        
        #print(a)
        c_sub2=[]
        n_sub2 = 0#
        front_sub2=0
        while n_sub2 < jogen_sub2:#
            r_sub2=rand.randint(1+(n_sub2<kagen_sub2)*a_sub2[front_sub2][0],sum_sub2[front_sub2])#
            count_sub2=0
            i_sub2=-1
            while count_sub2<r_sub2:
                i_sub2=i_sub2+1
                count_sub2=count_sub2+a_sub2[front_sub2][i_sub2]
            #print(i_sub2)
            if i_sub2==0:
                break
            if n_sub2 == jogen_sub2-1 and a_sub2[i_sub2][0] == 0:
                continue
            #c_sub2=c_sub2+[i_sub2+(227*256+130)*256+160+(i_sub2>32)*192]
            c_sub2=c_sub2+[227,129+(i_sub2>63),i_sub2+128-(i_sub2>63)*64]
            front_sub2=i_sub2
            n_sub2 = n_sub2 + 1#
        #print
        cc_sub2=bytes(c_sub2).decode("utf-8")
        print(cc_sub2)
        
        #----新単語を読み上げる----
        engine = pyttsx3.init()
        engine.say(cc_sub2)
        engine.runAndWait()
        
    # --ボタンを押したら繰り返し再生--
    #if event == '-speak_2-' and cc_sub1 == 'NULL':
        #sg.popup_ok('新単語が生成されていません。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-speak_2-':
        engine = pyttsx3.init()
        engine.say(cc_sub2) 
        engine.runAndWait()
            
    # window右上のx印を押して閉じたとき
    if event == sg.WIN_CLOSED: 
        break



#--------sub3ボタンが押された場合--------
    elif event == '-sub3-':
        # メインウィンドウを閉じて、サブ３ウィンドウを作成して表示する
        window.close()
        window = make_sub3()


#--------サブ３のウィンドウについての設定--------    
    if event == '-generate_3-':
        c111 = 1
        kagen_sub3 = int(values['-kag_3-'])#
        jogen_sub3 = int(values['-jog_3-'])#
        #--------各環境で相対パスを変更しよう！！--------
        f_sub3=open(resource_path("kata.bin"),"rb")#メイン環境
        #f_sub3=open("main_folder\kata.bin","rb")#Github環境
        sum_sub3=[0]*93
        a_sub3=[]
        for i_sub3 in range(93):
            aa_sub3=[]
            for j_sub3 in range(93):
                b_sub3=f_sub3.read(2)
                aaa_sub3=b_sub3[0]*256+b_sub3[1]
                aa_sub3=aa_sub3+[aaa_sub3]
                sum_sub3[i_sub3]=sum_sub3[i_sub3]+aaa_sub3
            a_sub3=a_sub3+[aa_sub3]
        f_sub3.close
        #print(a_sub3)
        
        c_sub3=[]
        n_sub3 = 0
        front_sub3=0
        while n_sub3 < jogen_sub3:
            r_sub3=rand.randint(1+(n_sub3<kagen_sub3)*a_sub3[front_sub3][0],sum_sub3[front_sub3])#
            count_sub3=0
            i_sub3=-1
            while count_sub3<r_sub3:
                i_sub3=i_sub3+1
                count_sub3=count_sub3+a_sub3[front_sub3][i_sub3]
            #print(i_sub3)
            if i_sub3==0:
                break
            if n_sub3 == jogen_sub3-1 and a_sub3[i_sub3][0] == 0:
                continue
            #c_sub3=c_sub3+[i_sub3+(227*256+130)*256+160+(i_sub3>32)*192]
            c_sub3=c_sub3+[227,130+(i_sub3>31),i_sub3+160-(i_sub3>31)*64]
            front_sub3=i_sub3
            n_sub3 = n_sub3 + 1#
        #print(c_sub3)
        cc_sub3=bytes(c_sub3).decode("utf-8")
        print(cc_sub3)
        
        #----新単語を読み上げる----
        engine = pyttsx3.init()
        engine.say(cc_sub3)
        engine.runAndWait()
        
    # --ボタンを押したら繰り返し再生--
    # if event == '-speak_3-' and cc_sub1 == 'NULL':
        #sg.popup_ok('新単語が生成されていません。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-speak_3-':
        engine = pyttsx3.init()
        engine.say(cc_sub3) 
        engine.runAndWait()
            
    # window右上のx印を押して閉じたとき
    if event == sg.WIN_CLOSED: 
        break



#--------sub4ボタンが押された場合--------
    elif event == '-sub4-':
        # メインウィンドウを閉じて、サブ４ウィンドウを作成して表示する
        window.close()
        window = make_sub4()
        
        
#--------サブ４のウィンドウについての設定--------    
    if event == '-generate_4-':
        d111 = 1
        kagen_sub4 = int(values['-kag_4-'])#
        jogen_sub4 = int(values['-jog_4-'])#
        #--------各環境で相対パスを変更しよう！！--------
        f_sub4=open(resource_path("alp.bin"),"rb")#メイン環境
        #f_sub4=open("main_folder/alp.bin","rb")#Github環境
        sum_sub4=[0]*27
        a_sub4=[]
        for i_sub4 in range(27):
            aa_sub4=[]
            for j_sub4 in range(27):
                b_sub4=f_sub4.read(2)
                aaa_sub4=b_sub4[0]*256+b_sub4[1]
                aa_sub4=aa_sub4+[aaa_sub4]
                sum_sub4[i_sub4]=sum_sub4[i_sub4]+aaa_sub4
            a_sub4=a_sub4+[aa_sub4]
        f_sub4.close
        #print(a_sub4)
        
        c_sub4=[]
        n_sub4 = 0#
        front_sub4=0
        while n_sub4 < jogen_sub4:#
            r_sub4=rand.randint(1+(n_sub4<kagen_sub4)*a_sub4[front_sub4][0],sum_sub4[front_sub4])#
            count_sub4=0
            i_sub4=-1
            while count_sub4<r_sub4:
                i_sub4=i_sub4+1
                count_sub4=count_sub4+a_sub4[front_sub4][i_sub4]
            #print(i_sub4)
            if i_sub4==0:
                break
            if n_sub4 == jogen_sub4-1 and a_sub4[i_sub4][0] == 0:
                continue
            #c_sub4=c_sub4+[i_sub4+(227*256+130)*256+160+(i_sub4>32)*192]
            c_sub4=c_sub4+[i_sub4+96]
            front_sub4=i_sub4
            n_sub4 = n_sub4 + 1#
        #print(c_sub4)
        cc_sub4=bytes(c_sub4).decode("utf-8")
        print(cc_sub4)
        
        #----新単語を読み上げる----
        engine = pyttsx3.init()
        engine.say(cc_sub4)
        engine.runAndWait()
        
    # --ボタンを押したら繰り返し再生--
    #if event == '-speak_4-' and cc_sub4 == 'NULL:
        #sg.popup_ok('新単語が生成されていません。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-speak_4-':
        engine = pyttsx3.init()
        engine.say(cc_sub4) 
        engine.runAndWait()
            
    # window右上のx印を押して閉じたとき
    if event == sg.WIN_CLOSED: 
        break
        
        
        
#--------sub5ボタンが押された場合--------
    elif event == '-sub5-':
        # メインウィンドウを閉じて、サブ５ウィンドウを作成して表示する
        window.close()
        window = make_sub5()
        #機械学習のため初期化
        cc_sub5 = 'NULL'


    if event == '-generate_5' and int(values['-jog_5-']) > 81:
        e111 = 1
        #kagen_sub5 = int(values['-kag_5-'])
        #jogen_sub5 = int(values['-jog_5-'])
        sg.popup_ok('上限の値が大きすぎるよ。')
        

#--------サブ5のウィンドウについての設定--------    
    elif event == '-generate_5-' and int(values['-jog_5-']) < 80:
        e111 = 1
        r = rand.randint(0,100)
        kagen_sub5 = int(values['-kag_5-'])
        jogen_sub5 = int(values['-jog_5-'])
    
        #--------各環境で相対パスを変更しよう！！--------
        f_sub5=open(resource_path("human.bin"),"rb")#メイン環境
        #f_sub5=open("main_folder\human.bin","rb")#Github環境
        sum_sub5=[0]*85
        a_sub5=[]
        for i_sub5 in range(85): 
            aa_sub5=[]
            for j_sub5 in range(85):
                b_sub5=f_sub5.read(2)
                aaa_sub5=b_sub5[0]*256+b_sub5[1]
                aa_sub5=aa_sub5+[aaa_sub5]
                sum_sub5[i_sub5]=sum_sub5[i_sub5]+aaa_sub5
            a_sub5=a_sub5+[aa_sub5]
        f_sub5.close

        #print(a_sub5)
        
        c_sub5=[]
        n_sub5 = 0#
        front_sub5=0
        while n_sub5 < jogen_sub5:
            r_sub5=rand.randint(1+(n_sub5<jogen_sub5)*a_sub5[front_sub5][0],sum_sub5[front_sub5])#
            count_sub5=0
            i_sub5=-1
            while count_sub5<r_sub5:
                i_sub5=i_sub5+1
                count_sub5=count_sub5+a_sub5[front_sub5][i_sub5]
            #print(i_sub5)
            if i_sub5==0:
                break
            #c_sub5=c_sub5+[i_sub5+(227*256+130)*256+160+(i_sub5>32)*192]
            c_sub5=c_sub5+[227,129+(i_sub5>63),i_sub5+128-(i_sub5>63)*64]
            front_sub5=i_sub5
            n_sub5 = n_sub5 + 1#
        #print(c_sub5)
        cc_sub5=bytes(c_sub5).decode("utf-8")
        print(cc_sub5)
        
        #----新単語を読み上げる----
        engine = pyttsx3.init()
        engine.say(cc_sub5)
        engine.runAndWait()
        
    # --ボタンを押したら繰り返し再生--
    #if event == '-speak_5-' and cc_sub1 == 'NULL':
        #sg.popup_ok('新単語が生成されていません。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    if event == '-speak_5-':
        engine = pyttsx3.init()
        engine.say(cc_sub5) 
        engine.runAndWait()
            
    
    
    if event == '-JudgeButton-' and cc_sub5 == 'NULL':
        window['-JudgeAnswer-'].update('まだ名前が生成されていません。')
    
#--------サブ5について機械学習を用いて判定--------
    if event == '-JudgeButton-' and cc_sub5 != 'NULL':

        text = cc_sub5
        #sg.popup_ok(cc_sub5)
        
        list1 = [text, 0]
        index1 = ['name', 'label']
        target = pd.Series(data = list1, index = index1)
        
        # bi-gramを取る
        def bigram(text):
            return [text[i:i+2] for i in range(len(text) - 1)] + ['end_'+text[-2:], 'end_'+text[-1]]

        target['bi_yomi'] = bigram(text)
        df['bi_yomi'] = df.name.apply(bigram)
        mlb = MultiLabelBinarizer()
        mlb.fit(df.bi_yomi)
        
        mlb.classes_
        
        # 渡されたsikit-learnのclassifierに対して学習して評価する
        # probabilityが0.6以上だったら判定できたことにする
        def train_and_test(classifier, df, mlb, target, fcount=0, mcount=0, threshold=0.6):
            kf = KFold(n_splits=5)
            for train, test in kf.split(df):
                test_df = df.loc[test]
            
                test_df.loc[4998] = (target)
            
                # MultiLabelを使ってベクトルにする
                test_features = mlb.transform(test_df.bi_yomi)
            
                # 評価
                test_proba = classifier.predict_proba(test_features)
                test_df['proba_male'] = [p[0] for p in test_proba]
                test_df['proba_female'] = [p[1] for p in test_proba]
                test_df['predict'] = -1
                # probabilityがthreshold以上の場合だけ判定結果を採用（ここでは0.6）
                test_df.loc[test_df.proba_male >= threshold, 'predict'] = 0
                test_df.loc[test_df.proba_female >= threshold, 'predict'] = 1
                all_len = len(test_df)
                predictable = len(test_df[test_df.predict != -1])
                tp = sum(test_df['predict'] == test_df['label'])
                fp = sum((test_df.predict != -1) & (test_df['predict'] != test_df['label']))
                class_name = str(classifier.__class__).split('.')[-1][:-2]
                #print('{}: all={}, predictable={}, precision={:.03f}, recall={:.03f}'.format(
                #        class_name, all_len, predictable, tp / predictable, tp / all_len))
        
                s = test_df["predict"][4998]
        
                #chance = (test_df['proba_male'][4998])
                
                #if chance != 0:
                    #return chance
                #print(float(chance))
                #sg.popup_ok(test_df)

                if s==1:
                    fcount= fcount+1
                if s==0: 
                    mcount = mcount +1
            if fcount >= 3:
                return 1
            if mcount >= 3:
                return 0
            
            
            
            '''    
            if fcount+mcount<5:
                train_and_test(classifier, df, mlb,target)
            
            with open('model.pickle', mode='wb') as f:
                pickle.dump(classifier,f)
            '''
            
        # svm
        with open(resource_path("model.pickle"),mode="rb") as f:
            classifier=pickle.load(f)
        s = train_and_test(classifier, df, mlb,target)
        
            
        if s == 1:
            #Outputでだすかeventに入れてupdateさせるか...
            #sg.popup('女性に多い名前です')
            window['-JudgeAnswer-'].update('女性に多い名前です。')
            
        elif s == 0:
            #sg.popup('男性に多い名前です')
            window['-JudgeAnswer-'].update('男性に多い名前です。')


        elif r < 6:
            window['-JudgeAnswer-'].update('タツノオトシゴに多い名前です（☆☆☆）')
            com[0]=1
        elif r<16:
            window['-JudgeAnswer-'].update('ミジンコに多い名前です（☆☆）')
            com[1]=1
        elif r<26:
            window['-JudgeAnswer-'].update('アナコンダに多い名前です（☆☆）')
            com[2]=1
        elif r<32:
            window['-JudgeAnswer-'].update('ハシビロコウに多い名前です（☆☆☆）')
            com[3]=1
        elif r<50:
            window['-JudgeAnswer-'].update('カラスに多い名前です（☆）')
            com[4]=1
        elif r<54:
            window['-JudgeAnswer-'].update('スピノサウルスに多い名前です（☆☆☆☆）')
            com[5]=1
        elif r<60:
            window['-JudgeAnswer-'].update('アンモナイトに多い名前です（☆☆☆）')
            com[6]=1
        elif r<70:
            window['-JudgeAnswer-'].update('ラクダに多い名前です（☆☆）')
            com[7]=1
        elif r<88:
            window['-JudgeAnswer-'].update('RPGのモブキャラに多い名前です（☆）')
            com[8]=1
        elif r<92:
            window['-JudgeAnswer-'].update('来世のあなたの名前です（☆☆☆☆）')
            com[9]=1
        elif r<98:
            window['-JudgeAnswer-'].update('架空の地名に多い名前です（☆☆☆）')
            com[10]=1
        elif r<101:
            window['-JudgeAnswer-'].update('ツチノコに多い名前です（☆☆☆☆☆）')
            com[11]=1
        
        complete = 0
        for i in com:
            complete += i
        window['-complete-'].update('珍名コンプリート率 : {}%'.format(complete*100//12))
        

        
                
                
    # window右上のx印を押して閉じたとき
    if event == sg.WIN_CLOSED: 
        break
    
    
    
#--------sub6ボタンが押された場合--------
    if event == '-sub6-':
        # メインウィンドウを閉じて、サブ6ウィンドウを作成して表示する
        window.close()
        window = make_sub6()

#--------サブ6のウィンドウについての設定-------- 
    if event == '-generate_6-' and not values['-FirstItem-'] and not values['-SecondItem-']:
        sg.popup_ok('１単語目と２単語目が入力されていないよ。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)

    elif event == '-generate_6-' and not values['-FirstItem-']:
        sg.popup_ok('１単語目が入力されていないよ。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)

    elif event == '-generate_6-' and not values['-SecondItem-']:
        sg.popup_ok('２単語目が入力されていないよ。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-generate_6-':
        f111 = 1
        c1 = values['-FirstItem-']
        c2 = values['-SecondItem-']
        
        if len(c1)>1:
            r=int(rand.randint(4,9-(len(c1)<3))/3)#1/6で3,3/6で2,2/6で1になる、c1からとる文字数
            cf=c1[:r]
        else:
            cf=c1
        l=len(c2)
        if l==1:
            c = cf + c2
            print(c)
        else:
            r=int(rand.randint(4,9-(l==2))/3)#1/6で3,3/6で2,2/6で1になる、c2からとる文字数
            c=cf+c2[:r]
            r=rand.randint(0,7)#0-3なら後ろから,4-7なら前からとる
            if r<4:
                f=open(resource_path("hrkt.bin"),"rb")#つながりのファイル
                a=[]
                sum_sub6=[]
                for i in range(189):
                    aa=[]
                    su=0
                    for j in range(189):
                        b=f.read(2)
                        aaa=b[0]*256+b[1]
                        aa=aa+[aaa]
                        su=su+aaa
                    a=a+[aa]
                    sum_sub6=sum_sub6+[su]
                f.close
                front=cf[-1].encode("utf-8")
                nf=front[2]-128+(front[1]-129)*64
                b=[2,3,1]#1,2,3文字になる確率の比
                abc=3-(l==2)
                aa=[0]*abc
                su=0
                for i in range(abc):
                    back=c2[-i-1].encode("utf-8")
                    nb=back[2]-128+(back[1]-129)*64
                    aa[i]=a[nf][nb]*b[i]
                    su=su+aa[i]
                if su: #su=0(つながらない)のときは前からとる
                    r=rand.randint(1,su)
                    i=-1
                    count=0
                    while count<r:
                        i=i+1
                        count=count+aa[i]
                    c=cf+c2[-i-1:]
            
            cc_sub6 = c  #txtファイルへの保存のため...
            
            print(c)

        #----新単語を読み上げる----
        engine = pyttsx3.init()
        engine.say(c)
        engine.runAndWait()
        
    # --ボタンを押したら繰り返し再生--
    #if event == '-speak_6-' and cc_sub1 == 'NULL':
        #sg.popup_ok('新単語が生成されていません。', font=('Arial', 12), text_color='#ff1493', keep_on_top=True)
        
    elif event == '-speak_6-':
        engine = pyttsx3.init()
        engine.say(c) 
        engine.runAndWait()






    # 「メニュー選択画面に戻る」ボタンが押された場合
    elif event == "-back-":
        # サブウィンドウを閉じて、メインウィンドウを作成して表示する
        window.close()
        window = make_main()
        
        
    #「アプリケーションを終了する」ボタンが押された場合
    elif event == '-exit-':
        # メインウィンドウを閉じて、アプリケーションを終了する
        window.close()



# ウィンドウを終了する
window.close()

if __name__ == 'main':
    exit()
