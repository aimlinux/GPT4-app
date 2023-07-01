import tkinter as tk
import speech_recognition as sr

def start_listening():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="ja-JP")
        text_label.config(text=text)
    except sr.UnknownValueError:
        text_label.config(text="音声が認識できませんでした。")
    except sr.RequestError:
        text_label.config(text="Google Speech Recognition APIに接続できませんでした。")

root = tk.Tk()
root.title("マイク入力の表示")

button = tk.Button(root, text="マイクを開始", command=start_listening)
button.pack()

text_label = tk.Label(root, text="")
text_label.pack()

root.mainloop()
