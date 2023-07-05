#ちゃっとじーぴーてぃーは神

# クラスのコンストラクタでインスタンス変数としてtext_inputを初期化
def __init__(self):
    self.text_input = None

# type_nowメソッド内でインスタンス変数に値をセット
def type_now(self):
    # ...
    self.text_input = scrolledtext.ScrolledText(fm_type, width=80, height=7, font=(main_font, 15), bg="#fff", state="normal")
    self.text_input.pack()
    # ...

# ai_answerメソッド内でインスタンス変数から値を取得
def ai_answer(self):
    type_text_value = self.text_input.get("1.0", "end-1c")
    print(type_text_value)