def voice_to_text():
    audio = get_audio_from_mic()
    audio_data = BytesIO(audio.get_wav_data())
    audio_data.name = 'from_mic.wav'
    transcript = openai.Audio.transcribe('whisper-1', audio_data)
    return transcript['text']

import speech_recognition as sr
r = sr.Recognizer()

def get_audio_from_mic():
    with sr.Microphone(sample_rate=16000) as source:
        print("なにか話してください")
        audio = r.listen(source)
        print("考え中...")
        return audio
{
 'id': 'chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve',
 'object': 'chat.completion',
 'created': 1677649420,
 'model': 'gpt-3.5-turbo',
 'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
 'choices': [
   {
    'message': {
      'role': 'assistant',
      'content': 'The 2020 World Series was played in Arlington, Texas at the Globe Life Field, which was the new home stadium for the Texas Rangers.'},
    'finish_reason': 'stop',
    'index': 0
   }
  ]
}
def chat(messages: list) -> str:
    result = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    response_text = result['choices'][0]['message']['content']
    return response_text
def post_audio_query(text: str) -> dict:
    params = {'text': text, 'speaker': 1}
    res = requests.post('http://localhost:50021/audio_query', params=params)
    return res.json()

def post_synthesis(audio_query_response: dict) -> bytes:
    params = {'speaker': 1}
    headers = {'content-type': 'application/json'}
    audio_query_response_json = json.dumps(audio_query_response)
    res = requests.post(
        'http://localhost:50021/synthesis',
        data=audio_query_response_json,
        params=params,
        headers=headers
    )
    return res.content
def play_wavfile(wav_file: bytes):
    wr: wave.Wave_read = wave.open(io.BytesIO(wav_file))
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(wr.getsampwidth()),
        channels=wr.getnchannels(),
        rate=wr.getframerate(),
        output=True
    )
    chunk = 1024
    data = wr.readframes(chunk)
    while data:
        stream.write(data)
        data = wr.readframes(chunk)
    sleep(0.5)
    stream.close()
    p.terminate()
import openai
from chat import chat
from whisper import voice_to_text
from voicevox import text_to_voice
from conf import APIKEY

openai.api_key = APIKEY
EXIT_PHRASE = 'exit'

def main():
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': f'終了やストップなどの会話を終了する内容で話しかけられた場合は{EXIT_PHRASE}のみを返答してください。'}
    ]
    exit_flag = False
    while not exit_flag:
        text = voice_to_text()
        messages.append(
            {'role': 'user', 'content': text}
        )
        response = chat(messages)

        if response == EXIT_PHRASE:
            exit_flag = True
            response = 'またね！'

        messages.append(
            {'role': 'assistant', 'content': response}
        )
        print(f'User   : {text}')
        print(f'ChatGPT: {response}')
        text_to_voice(response)


if name == 'main':
    main()
END_PHRASES = ['終了', 'ストップ', 'stop']

text = voice_to_text()
if text in END_PHRASES:
    # 終了処理