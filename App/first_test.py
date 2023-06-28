import openai
import os
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox


# ---- APIKey設定 ----
#openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = "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"



# r = sr.Recognizer()
# with sr.Microphone() as source:
#     messagebox.showinfo("title", "Say something!!")
#     audio = r.listen(source)

# try:
#     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))


role_sys = str(input("感性は？"))
if not role_sys:
    role_sys:str = "teacher"

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
        {"role": "system", "content": role_sys}, 
        {"role": "user", "content": question_1}, #質問１つ目
        #{"role": "assistant", "content": "ふざけんな！"}, #返答１つ目
        #{"role": "user", "content": "もう少し簡単に教えて！！"}, #質問２つ目
    ]
)

#ChatGPTからの返答の内容
res_content = res["choices"][0]["message"]["content"]
print(res_content)