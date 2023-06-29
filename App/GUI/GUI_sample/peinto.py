import tkinter

paint_app = tkinter.Tk()

paint_app.geometry(
    "500x500"
    )
paint_app.title(
    "ぺいんと"
    )

canvas = tkinter.Canvas(
    paint_app,
    width = 500,
    height = 500,
    bg = "white"
    )

press = False

def mouse_move_func(event):
    global canvas

    x = event.x
    y = event.y

    if press:
        canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue")

def mouse_click_func(event):
    global press
    press = True

def mouse_release_func(event):
    global press
    press = False

canvas.grid()

paint_app.bind(
    "<Motion>",
    mouse_move_func
    )

paint_app.bind(
    "<ButtonPress>",
    mouse_click_func
    )

paint_app.bind(
    "<ButtonRelease>",
    mouse_release_func
    )
    
paint_app.mainloop()