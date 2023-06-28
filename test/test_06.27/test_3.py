import openai
import os

#openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = "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"


content = "Hello, what can you do for me today?"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "�X����"},
        {"role": "user", "content": content},
    ],
    temperature=1
)

print(response.choices[0]["message"]["content"].strip())