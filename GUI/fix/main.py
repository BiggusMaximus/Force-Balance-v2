import re
from root import *
from PIL import Image, ImageTk
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from matplotlib.ticker import MaxNLocator
import pandas as pd

# Serial Com
serial_arduino = serial.Serial(baudrate=57600, timeout=0)

# Port Frame Base
main_port_frame = Frame(
    root,
    relief=RIDGE,
    bd=2,
    background="white",
    highlightbackground="black",
    highlightthickness=2
)
main_port_frame.columnconfigure(0, weight=1)
main_port_frame.columnconfigure(1, weight=8)
main_port_frame.rowconfigure(tuple(range(5)), weight=1)
main_port_frame.grid(row=0,  column=0, padx=10,  pady=10, sticky=N+S+E+W)


# Left Side Port Frame
port_frame = Frame(
    main_port_frame,
    relief=RIDGE,
    bd=2,
    background="white",
    highlightbackground="black",
    highlightthickness=2,
    width=100
)
port_frame.grid(row=0,  column=0, rowspan=5, padx=5,  pady=5, sticky=N+S+E+W)
port_frame.columnconfigure(0, weight=1)
port_frame.columnconfigure(1, weight=1)
port_frame.rowconfigure(tuple(range(99)), weight=1)

# Title App
title_app = Label(port_frame, text="FORCE BALANCE", font=(
    'Times 16 bold'), background="yellow").grid(row=0, column=0, columnspan=2, padx=5,   pady=5, sticky=N+W+E)

# Option Ports
ports = [str(port.device) for port in serial.tools.list_ports.comports()]
ports = tuple(ports)
port_value = StringVar(port_frame)
port_value.set("Select Ports")
port_selection = ttk.Combobox(port_frame, textvariable=port_value)
port_selection['value'] = ports
port_selection.grid(row=1, column=0, columnspan=2,
                    padx=5, sticky=N+E+W)

# Image
image = Image.open('G:/Program/All/Force Balance/GUI/fix/logoBRIN2.jpeg')
basewidth = 200
wpercent = (basewidth/float(image.size[0]))
hsize = int((float(image.size[1])*float(wpercent)))
image = image.resize((basewidth, hsize), Image.Resampling.LANCZOS)
image = ImageTk.PhotoImage(image)
brin_img = Label(port_frame, image=image).grid(
    row=99, column=0, columnspan=2, sticky=S+W+E)


# Refresh ports Button
def update_ports():
    ports = [str(port.device) for port in serial.tools.list_ports.comports()]
    ports = tuple(ports)
    port_selection['value'] = ports


refresh_port_button = Button(
    port_frame, text="Refresh Ports", activebackground='#00ff00', highlightbackground="red", command=update_ports).grid(row=2, columnspan=2, column=0, padx=5, sticky=W+E)


# Showing Ports Text
showing_port_text = Text(
    port_frame,
    height=1,
    width=25,
    bg="white"
)
showing_port_text.grid(row=3, column=0, columnspan=2, padx=5, sticky=E+W)
showing_port_text.tag_configure("tag_name", justify='center')
showing_port_text.insert("1.0", 'Port is not selected')
showing_port_text.tag_add("tag_name", "1.0", "end")
showing_port_text.tag_add("center", "1.0", "end")


def update_text_port(event):
    # if you want to remove the old data
    showing_port_text.delete(1.0, END)
    serial_arduino.port = port_value.get()
    try:
        serial_arduino.open()
        showing_port_text.tag_configure("tag_name", justify='center')
        showing_port_text.insert(
            "1.0", 'Port : ' + port_value.get() + " (Connected)")
        showing_port_text.tag_add("tag_name", "1.0", "end")
        showing_port_text.tag_add("center", "1.0", "end")
        return True
    except (FileNotFoundError, OSError):
        serial_arduino.close()
        showing_port_text.tag_configure("tag_name", justify='center')
        showing_port_text.insert(
            "1.0", 'Port : ' + port_value.get() + " (Not Connected)")
        showing_port_text.tag_add("tag_name", "1.0", "end")
        showing_port_text.tag_add("center", "1.0", "end")
        return False


port_selection.bind('<<ComboboxSelected>>', update_text_port)

# Calibration Status

showing_status_calibrate_text = Text(
    port_frame,
    height=1,
    width=25,
    bg="yellow",
    font=("Times 14 bold")
)
showing_status_calibrate_text.grid(
    row=5, columnspan=2, column=0, padx=5, sticky=E+W)
showing_status_calibrate_text.tag_configure("tag_name", justify='center')
showing_status_calibrate_text.insert("1.0", 'CALIBRATION')
showing_status_calibrate_text.tag_add("tag_name", "1.0", "end")
showing_status_calibrate_text.config(state=DISABLED)
showing_status_calibrate_text.tag_add("center", "1.0", "end")

load_cell_check_condition_frame = Frame(
    port_frame,
    relief=RIDGE,
    bd=2,
    background="white",
    highlightbackground="black",
    highlightthickness=2
)
load_cell_check_condition_frame.grid(
    row=7,  column=0, columnspan=2, padx=5,  sticky=N+S+E+W)
load_cell_check_condition_frame.columnconfigure(tuple(range(6)), weight=1)
load_cell_check_condition_frame.rowconfigure(0, weight=1)


def calibrate_RL():
    print("RL click")
    serial_arduino.write("RL".encode('utf-8'))
    RL_button.config(bg='#00ff00')


def calibrate_RY():
    print("RY click")
    serial_arduino.write("RY".encode('utf-8'))
    RY_button.config(bg='#00ff00')


def calibrate_RS():
    print("RS click")
    serial_arduino.write("RS".encode('utf-8'))
    RS_button.config(bg='#00ff00')


def calibrate_RD():
    print("RD click")
    serial_arduino.write("RD".encode('utf-8'))
    RD_button.config(bg='#00ff00')


def calibrate_RP():
    print("RP click")
    serial_arduino.write("RP".encode('utf-8'))
    RP_button.config(bg='#00ff00')


def calibrate_RR():
    print("RR click")
    serial_arduino.write("RR".encode('utf-8'))
    RR_button.config(bg='#00ff00')


RL_button = Button(
    load_cell_check_condition_frame,
    text="RL",
    relief="groove",
    bg="red",
    command=calibrate_RL
)
RL_button.grid(row=0, column=0, sticky=N+S+E+W)

RS_button = Button(
    load_cell_check_condition_frame,
    text="RS",
    relief="groove",
    bg="red",
    command=calibrate_RS
)
RS_button.grid(row=0, column=1, sticky=N+S+E+W)

RD_button = Button(
    load_cell_check_condition_frame,
    text="RD",
    relief="groove",
    bg="red",
    command=calibrate_RD
)
RD_button.grid(row=0, column=2, sticky=N+S+E+W)
RR_button = Button(
    load_cell_check_condition_frame,
    text="RR",
    relief="groove",
    bg="red",
    command=calibrate_RR
)
RR_button.grid(row=0, column=3, sticky=N+S+E+W)
RP_button = Button(
    load_cell_check_condition_frame,
    text="RP",
    relief="groove",
    bg="red",
    command=calibrate_RP
)
RP_button.grid(row=0, column=4, sticky=N+S+E+W)
RY_button = Button(
    load_cell_check_condition_frame,
    text="RY",
    relief="groove",
    bg="red",
    command=calibrate_RY
)
RY_button.grid(row=0, column=5, sticky=N+S+E+W)

# Showing text status calibrate
calibration_status_text = Text(
    port_frame,
    height=1,
    width=25,
    bg="white"
)
calibration_status_text.grid(
    row=10, column=0, columnspan=2, padx=5, sticky=E+W)
calibration_status_text.tag_configure("tag_name", justify='center')
calibration_status_text.insert("1.0", 'Calibration Status')
calibration_status_text.tag_add("tag_name", "1.0", "end")
calibration_status_text.tag_add("center", "1.0", "end")

# Measure Text
showing_status_measure_text = Text(
    port_frame,
    height=1,
    width=25,
    bg="yellow",
    font=("Times 14 bold")
)
showing_status_measure_text.grid(
    row=14, columnspan=2, rowspan=3, column=0, padx=5, sticky=E+W)
showing_status_measure_text.tag_configure("tag_name", justify='center')
showing_status_measure_text.insert("1.0", 'MEASURE')
showing_status_measure_text.tag_add("tag_name", "1.0", "end")
showing_status_measure_text.config(state=DISABLED)
showing_status_measure_text.tag_add("center", "1.0", "end")

# # Combobox iteration
# n_data = (10, 50, 100, 500, 1000)
# n_value = StringVar(port_frame)
# n_value.set("Insert n-iteration :")
# n_selection = ttk.Combobox(port_frame, textvariable=n_value)
# n_selection['value'] = n_data
# n_selection.grid(row=17, column=0, sticky=N+E+W, padx=5)

# n_data_var = StringVar(port_frame)
# n_data_var.set("select iteration !")
# show_n_data = Label(
#     port_frame,
#     relief="groove",
#     textvariable=n_data_var
# ).grid(row=18, column=0, sticky=N+E+W, padx=5)


# def update_text_n_iteration(event):
#     # if you want to remove the old data
#     print(n_value.get())
#     n_data_var.set("n iteration : " + str(n_value.get()))


# n_selection.bind('<<ComboboxSelected>>', update_text_n_iteration)


# # Combobox time
# time_data = (1, 5, 10, 15, 30, 60)
# time_value = StringVar(port_frame)
# time_value.set("Insert time (minute) :")
# time_selection = ttk.Combobox(port_frame, textvariable=time_value)
# time_selection['value'] = time_data
# time_selection.grid(row=17, column=1, sticky=N+E+W, padx=5)

# time_var = StringVar(port_frame)
# time_var.set("select iteration !")
# show_time = Label(
#     port_frame,
#     relief="groove",
#     textvariable=time_var
# ).grid(row=18, column=1, sticky=N+S+E+W, padx=5)


# def update_text_time(event):
#     # if you want to remove the old data
#     print(time_value.get())
#     time_var.set("time range (minute) : " + str(time_value.get()))


# time_selection.bind('<<ComboboxSelected>>', update_text_time)

# Button Measure

show_cal_status = True


def start_measure():
    global show_cal_status
    show_cal_status = False
    RL = []
    RS = []
    RD = []
    RR = []
    RP = []
    RY = []
    serial_arduino.write("MEASURE".encode('utf-8'))
    start_measure_button.config(bg='red')
    table_calibration.delete(*table_calibration.get_children())


start_measure_button = Button(
    port_frame, text="Start Measure",
    activebackground='#00ff00',
    command=start_measure
)
start_measure_button.grid(row=17,  columnspan=2, padx=5, column=0, sticky=W+E)


# Upper Right Side For Status
upper_frame = Frame(
    main_port_frame,
    relief=RIDGE,
    bd=2,
    background="white",
    highlightbackground="black",
    highlightthickness=2
)
upper_frame.grid(row=0,  column=1, rowspan=2, padx=5,  pady=5, sticky=N+S+E+W)
upper_frame.columnconfigure(0, weight=1)
upper_frame.rowconfigure(0, weight=1)

# create the graph
x = []
RL = []
RS = []
RD = []
RR = []
RP = []
RY = []

fig, ax = plt.subplots()
plt.xlim(0, 1000)
plt.ylim(0, 150)
plt.subplots_adjust(hspace=0)


def animate(RL, RS, RD, RR, RP, RY):

    ax.clear()
    ax.plot(x, RY, label='Yaw', linewidth=1)
    ax.plot(x, RP, label='Pitch', linewidth=1)
    ax.plot(x, RL, label='Lift', linewidth=1)
    ax.plot(x, RD, label='Drag', linewidth=1)
    ax.plot(x, RR, label='Roll', linewidth=1)
    ax.plot(x, RS, label='Side', linewidth=1)
    ax.set_xlim([0, 1000])
    ax.set_ylim([0, 150])
    ax.set_title("Force Balance")
    ax.legend(['Yaw', 'Pitch', 'Lift', 'Drag', 'Roll', 'Side'])
    ax.yaxis.set_major_locator(MaxNLocator(prune='lower'))
    plotcanvas.draw()


plotcanvas = FigureCanvasTkAgg(fig, upper_frame)
plotcanvas.get_tk_widget().grid(column=0, row=0, sticky=N+S+E+W)


# Bottom Right Side For Status
bottom_frame = Frame(
    main_port_frame,
    relief=RIDGE,
    bd=2,
    background="white",
    highlightbackground="black",
    highlightthickness=2
)
bottom_frame.grid(row=2,  column=1, rowspan=3, padx=5,  pady=5, sticky=N+S+E+W)
bottom_frame.columnconfigure(0, weight=1)
bottom_frame.rowconfigure(0, weight=1)

# Table
columns = ('Yaw', 'Pitch', 'Roll', 'Lift', 'Drag', 'Side')
table_calibration = ttk.Treeview(
    bottom_frame, columns=columns, show='headings')
table_calibration.heading('Yaw', text='Yaw')
table_calibration.heading('Pitch', text='Pitch')
table_calibration.heading('Roll', text='Roll')
table_calibration.heading('Lift', text='Lift')
table_calibration.heading('Drag', text='Drag')
table_calibration.heading('Side', text='Side')
col_width = table_calibration.winfo_width()
table_calibration.column("# 1", anchor=CENTER, width=col_width)
table_calibration.column("# 2", anchor=CENTER, width=col_width)
table_calibration.column("# 3", anchor=CENTER, width=col_width)
table_calibration.column("# 4", anchor=CENTER, width=col_width)
table_calibration.column("# 5", anchor=CENTER, width=col_width)
table_calibration.column("# 6", anchor=CENTER, width=col_width)
table_calibration.grid(row=0,  column=0, sticky=N+S+E+W)


scrollbar = Scrollbar(
    bottom_frame,
    orient=VERTICAL,
    command=table_calibration.yview,
    activebackground='#00ff00'
)
table_calibration.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=0, sticky=N+S+E)

# Save To Excel


def save_as_file():
    lst = []
    col = ['Yaw', 'Pitch', 'Lift', 'Drag']
    if (len(table_calibration.get_children()) < 1):
        messagebox.showinfo("Empty Data")
    else:
        filename = filedialog.asksaveasfilename(
            initialdir=os.getcwd(),
            title="Save To Excel",
            filetypes=(("xlsx File", "*.xlsx"), ("All Files", "*.*"))
        )

        with open('temp.csv', mode='w', newline='') as f:
            csvwriter = csv.writer(f, delimiter=',')
            for row_id in table_calibration.get_children():
                row = table_calibration.item(row_id, 'values')
                lst.append(row)
            lst = list(map(list, lst))
            lst.insert(0, col)
            for row in lst:
                csvwriter.writerow(row)
        writer = pd.ExcelWriter(filename + '.xlsx')
        df = pd.read_csv('temp.csv', delimiter=',')
        df.to_excel(writer, 'sheetname')
        writer.save()


save_to_excel_button = Button(
    bottom_frame, text="Save To Excel", activebackground='#00ff00', command=save_as_file).grid(row=1, padx=5, column=0, sticky=W+E)

i = 0
# Update loop


def is_empty_or_blank(msg):
    """ This function checks if given string is empty
     or contain only shite spaces"""
    return re.search("^\s*$", msg)


temp = []
stat = False
while True:
    main_port_frame.update()
    if serial_arduino.isOpen():
        input_data = serial_arduino.readline().strip().decode("utf-8")
        if len(input_data) != 0:
            print(input_data)
            # if you want to remove the old data
            calibration_status_text.delete("1.0", "end")
            calibration_status_text.insert(END, input_data)

            if input_data == "Finish":
                calibration_status_text.delete("1.0", "end")
                calibration_status_text.insert(END, "Finish Calibrate")

            input_data = str(input_data)
            parsing_val = input_data.split(",")
            if any([is_empty_or_blank(elem)for elem in parsing_val]):
                parsing_val.remove("")

            if len(parsing_val) == 6:
                table_calibration.insert(
                    "",
                    'end',
                    values=tuple(parsing_val)
                )
                # RS, RP, RL, RR, RY, RD
                RS.append(parsing_val[0])
                RP.append(parsing_val[1])
                RL.append(parsing_val[2])
                RR.append(parsing_val[3])
                RY.append(parsing_val[4])
                RD.append(parsing_val[5])
                x.append(i)
                i = i + 1

            if len(temp) == 6:
                table_calibration.insert(
                    "",
                    'end',
                    values=tuple(temp)
                )
                # RS, RP, RL, RR, RY, RD
                RS.append(temp[0])
                RP.append(temp[1])
                RL.append(temp[2])
                RR.append(temp[3])
                RY.append(temp[4])
                RD.append(temp[5])
                x.append(i)
                temp = []
                i = i + 1

            if len(parsing_val) == 4:
                temp = temp + parsing_val

            if len(parsing_val) == 2:
                temp = temp + parsing_val
    animate(RL, RS, RD, RR, RP, RY)
