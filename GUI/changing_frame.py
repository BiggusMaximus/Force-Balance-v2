from tkinter import *

root = Tk()
root.title("Force Balance Application")
root.iconbitmap("icon.ico")
root.config(bg="lightyellow")


def changeToMain():
    frame_main.pack(fill="both", expand=True)
    frame_port.forget()


frame_port = Frame(root)
frame_main = Frame(root)

title_main = Label(frame_main, text="Calibration and Simulation")
title_main.place(relx=0.5, rely=0, anchor=CENTER)

title_port = Label(frame_port, text="Choose Port")
title_port.place(relx=0.5, rely=0.9, anchor=CENTER)

start_button = Button(frame_port, text="Choose Port", command=changeToMain)
start_button.pack(pady=20)

frame_port.pack(fill="both", expand=True)


root.mainloop()
