import tkinter as tk

def display_text():
    text = entry.get()  # 入力したテキストを取得
    text_area.insert(tk.END, text + "\n")  # テキストエリアに表示
    entry.delete(0, tk.END)  # 入力欄をクリア

# Tkinterウィンドウを作成
window = tk.Tk()

# 入力欄を作成
entry = tk.Entry(window)
entry.pack()

# テキストエリアを作成
text_area = tk.Text(window)
text_area.pack()

# ボタンを作成して、display_text関数を呼び出す
button = tk.Button(window, text="表示", command=display_text)
button.pack()

# Tkinterウィンドウを実行
window.mainloop()
