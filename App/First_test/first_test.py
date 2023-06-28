import openai
import os
import speech_recognition as sr
import tkinter as tk
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
        #{"role": "assistant", "content": "ふざけんな！"},
        #{"role": "user", "content": "もう少し簡単に教えて！！"},
    ]
)

#ChatGPTからの返答の内容
res_content = res["choices"][0]["message"]["content"]
print(res_content)