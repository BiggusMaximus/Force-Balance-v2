from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import sys
import csv

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)

root = Tk()  # create root window
root.title("Force Balance Application (by Annastya and Tulus)")
root.config(bg="#8B0000")
root.iconbitmap('logoBRIN.ico')
root.state('zoomed')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
