from tkinter import *
from tkinter import ttk
import serial.tools.list_ports
from PIL import Image, ImageTk


root = Tk()  # create root window
root.title("Force Balance Application")
root.config(bg="#8B0000")
root.iconbitmap("logoBRIN.ico")
root.state('zoomed')
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=7)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

serialInst = serial.Serial(baudrate=9600, timeout=0)


def get_port(selection):
    global selected_text
    selected_text.configs(text=str(selection) + " Selected")
    serialInst.port = str(selection)
    try:
        serialInst.open()
        print("Connection with Device successfully opened")
        return True
    except (FileNotFoundError, OSError):
        print("ERROR: Can't connect to this port!")
        return False


port_frame = Frame(root, relief=RAISED, bd=2, background="white")
port_frame.grid(row=0,  column=0, rowspan=3, padx=10,  pady=10, sticky=N+S+E+W)
port_frame.columnconfigure(0, weight=9)
port_frame.columnconfigure(1, weight=1)
port_frame.rowconfigure(tuple(range(100)), weight=1)
ports = [str(port.device) for port in serial.tools.list_ports.comports()]
selected_text = Label(port_frame).grid(
    row=2, column=0, columnspan=2,  padx=5, pady=5, sticky=N+S+W+E)

port_value = StringVar(port_frame)
port_value.set("Select Ports")
start_calibration_button = Button(
    port_frame, text="START CALIBRATE", activebackground='#00ff00').grid(row=0,  padx=5, column=0, columnspan=2, sticky=W+E)
port_selection = OptionMenu(port_frame, port_value, *ports, command=get_port)
port_selection.grid(row=1, column=0,  padx=5, pady=5, sticky=N+S+E+W)


# insert_port_text = "Insert Port"
# not_connected_text =
def listPorts():
    ''' Refreshes the available COM ports and updates the Options Menu
    '''
    global insert_port_text
    selected_text.config(text='Insert Port')
    status_frame
    connected_text.config(text='Not Connected')
    ports = [port.device for port in serial.tools.list_ports.comports()
             ]    # get the available ports
    # ports = [1,2,3]     # for testing. comment later
    print("Ports found:", ports)
    menu = port_selection['menu']
    menu.delete(0, 'end')   # Clear the previous items
    if len(ports) == 0:
        port_value.set('No ports found. refresh again')
    else:
        for port in ports:
            menu.add_command(
                label=port, command=lambda p=port: port_value.set(p))
        port_value.set('Choose a port:')


refresh_port_button = Button(
    port_frame, text="Refresh", activebackground='#00ff00', highlightbackground="red", command=listPorts).grid(row=1, column=1, padx=5, pady=5, sticky=N+S+W+E)

image = Image.open("logoBRIN2.jpeg")
basewidth = 150
wpercent = (basewidth/float(image.size[0]))
hsize = int((float(image.size[1])*float(wpercent)))
image = image.resize((basewidth, hsize), Image.Resampling.LANCZOS)
image = ImageTk.PhotoImage(image)
brin_img = Label(port_frame, image=image).grid(
    row=99, column=0,  columnspan=2, rowspan=10, padx=5, pady=5)


status_frame = Frame(root, relief=RAISED, bd=2)
status_frame.grid(row=0,  column=1,
                  padx=10,  pady=10, sticky=N+S+E+W)
showing_status = Label(status_frame, text=" Selected", font=(
    'Times 14')).grid(row=1, column=0,  padx=5, pady=5)
status_frame.rowconfigure(tuple(range(3)), weight=1)
status_frame.columnconfigure(0, weight=1)

status_1 = Frame(status_frame, relief=RAISED, bd=2, bg="#8B0000").grid(
    row=0,  column=0,  padx=5,  pady=5, sticky=N+S+E+W)
text_1 = Label(status_frame, text="TARE", font=('Times 14')
               ).grid(row=0, column=0,  padx=5, pady=5, sticky=N+S+E+W)

status_2 = Frame(status_frame, relief=RAISED, bd=2, bg="#8B0000").grid(
    row=1,  column=0, padx=5,  pady=5, sticky=N+S+E+W)
text_2 = Label(status_frame, text="REMOVE WEIGHT", font=(
    'Times 14')).grid(row=1, column=0,  padx=5, pady=5, sticky=N+S+E+W)

status_3 = Frame(status_frame, relief=RAISED, bd=2, bg="#8B0000").grid(
    row=2,  column=0, padx=5,  pady=5, sticky=N+S+E+W)
text_3 = Label(status_frame, text="RESULT", font=('Times 14')).grid(
    row=2, column=0,  padx=5, pady=5, sticky=N+S+E+W)

calibrate_frame = Frame(root, relief=RAISED, bd=2)
calibrate_frame.grid(row=1,  column=1, rowspan=2,
                     padx=10,  pady=10, sticky=N+S+E+W)
calibrate_frame.columnconfigure(0, weight=1)
calibrate_frame.rowconfigure(0, weight=1)
columns = ('Yawn', 'Pitch', 'Roll', 'X', 'Y', 'Z')
table_calibration = ttk.Treeview(
    calibrate_frame, columns=columns, show='headings')
table_calibration.heading('Yawn', text='Yawn')
table_calibration.heading('Pitch', text='Pitch')
table_calibration.heading('Roll', text='Roll')
table_calibration.heading('X', text='X')
table_calibration.heading('Y', text='Y')
table_calibration.heading('Z', text='Z')
table_calibration.grid(row=0, column=0, sticky=N+S+W+E)


while True:
    root.update()
    if serialInst.isOpen():
        connected_text = Label(port_frame, text="Force Balance Device \n is Connected", borderwidth=2).grid(
            row=3, column=0, columnspan=2, rowspan=2, padx=5, pady=5, sticky=N+S+W+E)
        input_data = serialInst.readline().strip().decode("utf-8")
        if len(input_data) != 0:
            print(input_data)
            if input_data == "TARE":
                status_1 = Frame(status_frame, relief=RAISED, bd=2, bg="green").grid(
                    row=0,  column=0,  padx=5,  pady=5, sticky=N+S+E+W)
                text_1 = Label(status_frame, text="TARE", font=('Times 14')
                               ).grid(row=0, column=0,  padx=5, pady=5, sticky=N+S+E+W)
            elif input_data == "REMOVE_WEIGHT":

                status_2 = Frame(status_frame, relief=RAISED, bd=2, bg="green").grid(
                    row=1,  column=0, padx=5,  pady=5, sticky=N+S+E+W)
                text_2 = Label(status_frame, text="REMOVE WEIGHT", font=(
                    'Times 14')).grid(row=1, column=0,  padx=5, pady=5, sticky=N+S+E+W)
            elif input_data == "RESULT":
                status_3 = Frame(status_frame, relief=RAISED, bd=2, bg="green").grid(
                    row=2,  column=0, padx=5,  pady=5, sticky=N+S+E+W)
                text_3 = Label(status_3, text="RESULT", font=('Times 14')).grid(
                    row=2, column=0,  padx=10, pady=10, sticky=N+S+W)
