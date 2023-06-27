import openai
import os

openai.api_key = os.environ['uBulLxdhNUxkWjw7x3veT3BlbkFJGBD21ioNk3j5wNEnDFV6']


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "あなたは学校の先生です。"},
        {"role": "user", "content": "おはようございます"},
    ]   
)


print(f"ChatGPT:{response['choices'][0]['message']['content']}")
print(response['usage'])