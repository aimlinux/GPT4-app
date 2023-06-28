import os 
import io
import openai
import speech_recognition as sr

#音声認識の初期化
r = sr.Recognizer()

def transcribe_speech():
    with sr.Microphone() as source:
        print("話しかけてください...")
        audio = r.listen(source)
        print("音声認識中...")

    try:
        text = r.recognize_google_cloud(audio, language="ja-JP")
        print("音声認識結果:", text)
        return text
    except sr.UnknownValueError:
        print("音声が理解できませんでした。もう一度お試しください。")
    except sr.RequestError as e:
        print("音声認識サービスでエラーが発生しました:", str(e))

