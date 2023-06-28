import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='ja-JP')
        print(query)
    except Exception:
        print("Error")
                            