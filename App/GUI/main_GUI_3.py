import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox 
import tkinter.ttk as ttk
import os
import speech_recognition as sr
import pyaudio
import wave
import time
import random as rand
import sys



#グローバル変数定義
main_bg = "aqua"
sub1_bg = "aqua"
sub2_bg = "#ffff8e"
sub3_bg = "lightblue"
sub4_bg = "black"
title_font = "Arial"
main_font = "Arial"

button_1 = "ふぁいる"
button_2 = "せってい"
button_3 = "たいとるへ"
button_4 = "ろぐ"


# ウィンドウが生成されたフラグを取得するため（各ウィンドウが開いたときTrue、閉じたときFalseへ）
#global count_main, count_sub1, count_sub2, count_sub3
count_main = False
count_sub1 = False
count_sub2 = False
count_sub3 = False
count_sub4 = False



BUTTON_OPUTIONS = {
    "expand" : "True",
    "fill" : "tk.NONE",
    
}


root = tk.Tk()
root.title("UI_only")
root.geometry("1200x720")


pw_sub1 = tk.PanedWindow(root, bg="red", orient="vertical")
pw_sub1.pack(expand=True, fill=tk.BOTH, side="left")

fm_sub1 = tk.Frame(bd=15, bg=sub1_bg, relief="ridge")
pw_sub1.add(fm_sub1)

# -------- メインフレームのオブジェクト作成 --------
space_label = tk.Label(fm_sub1, text="", bg=sub1_bg, height=2)
space_label.pack(side=tk.TOP)

title_label = tk.Label(fm_sub1, text="**** ことばでおはなし ****", bg=sub1_bg, font=(title_font, 42), height=2)
title_label.pack(side=tk.TOP)

space_label = tk.Label(fm_sub1, text="", bg=sub1_bg, height=3)
space_label.pack(side=tk.TOP)

start_button = tk.Label(fm_sub1, text=" ** 返答 ** ", font=(main_font, 35), width=30)
start_button.pack(side=tk.TOP, pady=10)

start_button = tk.Button(fm_sub1, text=" ことばでしつもん ", font=(main_font, 35), width=30)
start_button.pack(side=tk.BOTTOM, pady=50)


root.mainloop()