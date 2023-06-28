import tkinter as tk #tkinterのインポート
import openai
import os
import speech_recognition as sr
from tkinter import messagebox



# ---- APIKey設定 ----
#openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = ""



#messagebox.showinfo("title", "Say something!!")
# r = sr.Recognizer()
# with sr.Microphone() as source:
#     r.adjust_for_ambient_noise(source)
#     print("Listening...")
#     audio = r.listen(source)
#     try:
#         query = r.recognize_google(audio, language='ja-JP')
#         print(query)
#     except Exception:
#         print("Error")



role_sys_1 = str(input("特徴は？"))
if not role_sys_1:
    role_sys_1:str = "teacher"

#roleは２個目が適用されるのかな...
# role_sys_2 = str(input("特徴は？"))
# if not role_sys_2:
#     role_sys_2:str = "teacher"
    
question_1 = str(input("質問は？"))
if not question_1:
    question_1:str = "ご使用ありがとうございます。\nご質問されるのでしたら再起動してください。"


res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        #role : 役割, 
        # system :（このチャットのシステム） 
        # user :（チャットを使う側 = 私たち） 
        # assistant : ChatGPT側, 
        # content : メッセージ内容
        {"role": "system", "content": role_sys_1}, 
        #{"role": "system", "content": role_sys_2}, 
        {"role": "user", "content": question_1},
        {"role": "assistant", "content": "ふざけんな！"},
        #{"role": "user", "content": "もう少し簡単に教えて！！"},
    ]
)

#ChatGPTからの返答の内容
res_content = res["choices"][0]["message"]["content"]
print(res_content)



root = tk.Tk()
root.geometry("1200x720") #geometryだと表示サイズがminsizeより細かく調節できる
canvas = tk.Canvas(bg = "black", width=1200, height=720) #背景を設定
canvas.place(x=0, y=0) #背景を配置

default_x = 1900 #初期x座標
default_y = 5 #初期y座標
x=0 #リストカウント数
text_list=[res_content] #文言リスト
text_st = tk.StringVar() #文字更新用のStringVarを定義
text_st.set(text_list[x]) #リストのテキストをセット
label1 = tk.Label(textvariable=text_st,font=('',500),background ="black",foreground="aqua") #文字を置くラベルの設定
label1.place(x=default_x,y=default_y) #ラベルの初期配置位置を設定


def move(): #動作する関数
    global default_x #x座標を変更
    global x #リスト内要素の現在位置表示
    label1.place_forget() #ラベル消去
    label1.place(x=default_x,y=default_y) #ラベル再配置
    default_x -= 100 #スクロール速さ(xの座標の位置が減少することで、スクロールしているかのように見せている)

    n = len(text_list)-1 #リストの要素数を取得

    if default_x <=-3000: #画面左端まで文字が到達した場合
        default_x = 1900 #画面右に戻す
        x += 1 #取り込むリストの要素をひとつずらす
        text_st.set(text_list[x]) #StringVarに反映
        if x == n: #xが要素数+1に達した場合
            x=0 #最初にリセット
            text_st.set(text_list[len(text_list)-1]) #要素数の最大値の要素をStringVarに反映

for i in range (1,19999): #スクロール繰り返し回数
    root.after(int(i*100),move) #100ミリ秒ごとにスクロール
root.mainloop() #以上のコードの内容を繰り返す

