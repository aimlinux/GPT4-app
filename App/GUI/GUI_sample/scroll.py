import tkinter as tk #tkinterのインポート
root = tk.Tk()
root.geometry("1920x80") #geometryだと表示サイズがminsizeより細かく調節できる
canvas = tk.Canvas(bg = "black", width=1920, height=80) #背景を設定
canvas.place(x=0, y=0) #背景を配置

default_x = 1900 #初期x座標
default_y = 5 #初期y座標
x=0 #リストカウント数
text_list=["表示テストをしてみます。今朝はよく晴れています。","今朝の気温は15度です。","今日の最高気温は20度となる見込みです。"] #文言リスト
text_st = tk.StringVar() #文字更新用のStringVarを定義
text_st.set(text_list[x]) #リストのテキストをセット
label1 = tk.Label(textvariable=text_st,font=('',45),background ="black",foreground="orange") #文字を置くラベルの設定
label1.place(x=default_x,y=default_y) #ラベルの初期配置位置を設定


def move(): #動作する関数
    global default_x #x座標を変更
    global x #リスト内要素の現在位置表示
    label1.place_forget() #ラベル消去
    label1.place(x=default_x,y=default_y) #ラベル再配置
    default_x -= 50 #スクロール速さ(xの座標の位置が減少することで、スクロールしているかのように見せている)

    n = len(text_list)-1 #リストの要素数を取得

    if default_x <=-3000: #画面左端まで文字が到達した場合
        default_x = 1900 #画面右に戻す
        x += 1 #取り込むリストの要素をひとつずらす
        text_st.set(text_list[x]) #StringVarに反映
        if x == n: #xが要素数+1に達した場合
            x=0 #最初にリセット
            text_st.set(text_list[len(text_list)-1]) #要素数の最大値の要素をStringVarに反映

for i in range (1,19999): #スクロール繰り返し回数
    root.after(int(i*100),move) #100ミリ秒ごとにスクロール
root.mainloop() #以上のコードの内容を繰り返す

