import sys
import os

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)

iconFile = "logoBRIN.ico"
print(os.path.join(application_path, iconFile))
