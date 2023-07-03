import tkinter as tk

def on_select(event):
    # 選択された値を取得する
    selected_value = listbox.get(listbox.curselection())
    print(selected_value)

root = tk.Tk()

listbox = tk.Listbox(root)
listbox.pack()

# Listboxに要素を追加
listbox.insert(tk.END, "Option 1")
listbox.insert(tk.END, "Option 2")
listbox.insert(tk.END, "Option 3")

# 選択イベントと関数を関連付ける
listbox.bind("<<ListboxSelect>>", on_select)

root.mainloop()