import streamlit as st
import openai
import os
CHATGPT_API_KEY = os.environ[]
def generate_name(text,language):
    res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": f"Please output 10 candidates for appropriate variable or function names in English from the input Japanese. Naming conventions must follow the {language} language specification and the output must be on a single line in the format name1,name2,name3."
        },
        {
            "role": "user",
            "content": text
        },
    ],
    )
    return res["choices"][0]["message"]["content"]
language_list = ["Python", "JavaScript", "Java", "Go"]
st.title("AutoNamer")
st.header('変数名や関数名を自動で命名するアプリです')
selected_language = st.selectbox("言語を選択してください", language_list)
text_input = st.text_input("変数や関数にする処理の概要を記述してください", "")
if st.button("生成"):
    names = generate_name(text_input, language=selected_language)
    for name in names.split(","):
        st.code(name)