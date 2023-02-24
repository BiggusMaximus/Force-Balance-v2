from tkinter import *

root = Tk()  # create root window
root.title("Force Balance Application")
root.config(bg="#8B0000")
root.attributes('-fullscreen', True)

port_frame = Frame(root, width=200, height=200)
port_frame.grid(row=0, column=0, padx=5, pady=5)
root.mainloop()
