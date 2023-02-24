import time
import csv
import os
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from PIL import Image, ImageTk
import threading
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from matplotlib.ticker import MaxNLocator
import pandas as pd
matplotlib.use('Agg')

# Serial Com
serial_arduino = serial.Serial(baudrate=57600, timeout=0)

# RL = []
# RS = []
# RD = []
# RY = []
# RR = []
# RP = []
# x = []


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Force Balance Application (by Annastya and Tulus)")
        self.config(bg="#8B0000")
        self.iconbitmap('logoBRIN.ico')
        self.state('zoomed')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.mainFrame()
        self.protocol("WM_DELETE_WINDOW", self.closeWindow)

    def mainFrame(self):
        self.mainFrame = MainFrame(self)

    def closeWindow(self):
        MainFrame.isRead = False
        serial_arduino.close()
        print("close")
        self.quit()
        self.destroy()


class MainFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(
            self,
            master,
            relief=tk.RIDGE,
            bd=2,
            background="white",
            highlightbackground="black",
            highlightthickness=2
        )
        self.isRead = False
        self.master = master
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=15)
        self.rowconfigure(tuple(range(5)), weight=1)
        self.grid(row=0,  column=0, padx=10,  pady=10, sticky="nsew")

        # ==============================================================================
        '''
        Port Frame

        Showing Title, Choosing Port, And Calibration
        '''
        # PortFrame
        self.PortFrame = tk.Frame(
            self,
            relief=tk.RIDGE,
            bd=2,
            background="white",
            highlightbackground="black",
            highlightthickness=2,
            width=100
        )
        self.PortFrame.columnconfigure(0, weight=1)
        self.PortFrame.columnconfigure(1, weight=1)
        self.PortFrame.rowconfigure(tuple(range(99)), weight=1)
        self.PortFrame.grid(row=0,  column=0, rowspan=5,
                            padx=5,  pady=5, sticky="nsew")

        # ==============================================================================
        '''
        Table Frame

        '''
        self.TableFrame = tk.Frame(
            self,
            relief=tk.RIDGE,
            bd=2,
            background="white",
            highlightbackground="black",
            highlightthickness=2
        )
        self.TableFrame.columnconfigure(0, weight=1)
        self.TableFrame.rowconfigure(0, weight=1)
        self.TableFrame.grid(row=2,  column=1, rowspan=3,
                             padx=5,  pady=5, sticky="nsew")
        self.Table()

        # =====================================================================================

        # Show Title
        self.PortFrame.title = tk.Label(self.PortFrame, text="FORCE BALANCE", font=(
            'Times 12 bold'), background="yellow")
        self.PortFrame.title.grid(row=0, column=0, columnspan=2,
                                  padx=5,   pady=5, sticky="nswe")

        self.PortFrame.title_measure = tk.Label(self.PortFrame, text="MEASURE", font=(
            'Times 12 bold'), background="yellow")
        self.PortFrame.title_measure.grid(row=8, column=0, columnspan=2,
                                          padx=5,   pady=5, sticky="nswe")

        self.PortFrame.title_calibrate = tk.Label(self.PortFrame, text="CALIBRATE", font=(
            'Times 12 bold'), background="yellow")
        self.PortFrame.title_measure.grid(row=5, column=0, columnspan=2,
                                          padx=5,   pady=5, sticky="nswe")

        # Combobox showing ports
        self.select_port()
        self.PortFrame.choose_port.bind(
            '<<ComboboxSelected>>', self.update_text_port)
        # Text
        self.port_status = tk.Text(
            self.PortFrame,
            height=1,
            width=25,
            bg="white"
        )
        self.port_status.grid(
            row=3, column=0, columnspan=2, padx=5, sticky="ew")
        self.port_status.tag_configure("tag_name", justify='center')
        self.port_status.insert("1.0", 'Port is not selected')
        self.port_status.tag_add("tag_name", "1.0", "end")
        self.port_status.tag_add("center", "1.0", "end")

        self.serial_text = tk.Text(
            self.PortFrame,
            height=1,
            width=25,
            bg="white"
        )
        self.serial_text.grid(
            row=7, column=0, columnspan=2, padx=5, sticky="nsew")
        self.serial_text.tag_configure("tag_name", justify='center')
        self.serial_text.insert("1.0", 'Calibration Status')
        self.serial_text.tag_add("tag_name", "1.0", "end")
        self.serial_text.tag_add("center", "1.0", "end")

        # Image
        self.image = Image.open('logoBRIN2.jpeg')
        basewidth = 200
        wpercent = (basewidth/float(self.image.size[0]))
        hsize = int((float(self.image.size[1])*float(wpercent)))
        self.image = self.image.resize(
            (basewidth, hsize), Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        image_logo = tk.Label(self.PortFrame, image=self.image).grid(
            row=99, column=0, columnspan=2, sticky="swe")

        # Button
        self.CalibrationButton = tk.Button(
            self.PortFrame,
            text="Start Calibrate",
            relief="groove",
            highlightbackground="black",
            activebackground='red',
            bg='#00ff00',
            command=self.calibrate
        )
        self.CalibrationButton.grid(
            row=6, column=0,  sticky="nsew", pady=3, padx=(5, 1))

        self.restartCalibrateButton = tk.Button(
            self.PortFrame,
            text="Restart",
            relief="groove",
            highlightbackground="black",
            activebackground='#ffcccb',
            state=tk.DISABLED,
            bg='#ffcccb',
            disabledforeground='black',
            command=self.restartCalibrate
        )
        self.restartCalibrateButton.grid(
            row=6, column=1,  sticky="nsew", pady=3, padx=(1, 5))

        self.refreshPortButton = tk.Button(
            self.PortFrame,
            text="Refresh Ports",
            relief="groove",
            activebackground='#00ff00',
            highlightbackground="red",

            command=self.update_ports
        ).grid(row=2, columnspan=2, column=0, padx=5, sticky="we")

        self.startMeasureButton = tk.Button(
            self.PortFrame,
            text="Start Measure",
            relief="groove",
            highlightbackground="black",
            activebackground='red',
            bg='#ffcccb',
            state=tk.DISABLED,
            disabledforeground='black',
            command=self.start_measure
        )
        self.startMeasureButton.grid(
            row=9, column=0, padx=(5, 1), pady=3, sticky="we")

        self.stopMeasureButton = tk.Button(
            self.PortFrame,
            text="Stop",
            relief="groove",
            highlightbackground="black",
            activebackground='#ffcccb',
            state=tk.DISABLED,
            bg='#ffcccb',
            disabledforeground='black',
            command=self.stop_measure
        )
        self.stopMeasureButton.grid(
            row=9, column=1, padx=(1, 5), pady=3, sticky="we")

        self.saveExcelButton = tk.Button(
            self.TableFrame, text="Save To Excel",
            relief="groove",
            highlightbackground="black",
            activebackground='red',
            bg='#00ff00',
            command=self.save_as_file).grid(row=1, padx=5, column=0, sticky="we")

        # ==============================================================================
        '''
        Graph Frame

        Merely existance just for graph
        '''
        # GraphFrame
        self.GraphFrame = tk.Frame(
            self,
            relief=tk.RIDGE,
            bd=2,
            background="white",
            highlightbackground="black",
            highlightthickness=2,
            width=100
        )
        self.GraphFrame.columnconfigure(0, weight=1)
        self.GraphFrame.rowconfigure(0, weight=1)
        self.GraphFrame.grid(row=0,  column=1, rowspan=2,
                             padx=5,  pady=5, sticky="nsew")

        self.fig, self.ax = plt.subplots()
        self.plot_graph = FigureCanvasTkAgg(self.fig, self.GraphFrame)
        self.plot_graph.get_tk_widget().grid(column=0, row=0, sticky="nsew")
        self.GraphFrame.thread_plot = threading.Thread(
            target=self.plot)
        self.GraphFrame.thread_plot.setDaemon(True)
        self.GraphFrame.thread_plot.start()

        # Load Cell Variable
        self.count = 0
        self.RL = []
        self.RS = []
        self.RD = []
        self.RY = []
        self.RR = []
        self.RP = []
        self.X = []

    def select_port(self):
        ports = [str(port.device)
                 for port in serial.tools.list_ports.comports()]
        ports = tuple(ports)
        self.PortFrame.port_value = tk.StringVar(self.PortFrame)
        self.PortFrame.port_value.set("Select Ports")
        self.PortFrame.choose_port = ttk.Combobox(
            self.PortFrame, textvariable=self.PortFrame.port_value)
        self.PortFrame.choose_port['value'] = ports
        self.PortFrame.choose_port.grid(row=1, column=0, columnspan=2,
                                        padx=5, sticky="nswe")

    def update_ports(self):
        ports = [str(port.device)
                 for port in serial.tools.list_ports.comports()]
        ports = tuple(ports)
        self.PortFrame.choose_port['value'] = ports

    def update_text_port(self, *args):
        # if you want to remove the old data
        serial_arduino.port = self.PortFrame.port_value.get()
        try:
            serial_arduino.open()
            self.port_status.delete(1.0, tk.END)
            self.port_status.tag_configure(
                "tag_name", justify='center')
            self.port_status.insert(
                "1.0", 'Port : ' + self.PortFrame.choose_port.get() + " (Connected)")
            self.port_status.tag_add("tag_name", "1.0", "end")
            self.port_status.tag_add("center", "1.0", "end")
            return True

        except (FileNotFoundError, OSError):
            serial_arduino.close()
            self.port_status.delete(1.0, tk.END)
            self.port_status.tag_configure(
                "tag_name", justify='center')
            self.port_status.insert(
                "1.0", 'Port : ' + self.PortFrame.choose_port.get() + " (Not Connected)")
            self.port_status.tag_add("tag_name", "1.0", "end")
            self.port_status.tag_add("center", "1.0", "end")
        return False

    def calibrate(self):
        if serial_arduino.isOpen():
            serial_arduino.flushInput()
            val = serial_arduino.readline()
            while not '\\n' in str(val):
                time.sleep(.001)
                temp = serial_arduino.readline()
                if not not temp.decode():
                    val = (val.decode()+temp.decode()).encode()
            val = val.decode().rstrip().split(',')

            # RD d, RP , RY d, RS d, RR d, RL d
            self.C_RL = 0 - float(val[5])
            self.C_RY = 0 - float(val[2])
            self.C_RS = 0 - float(val[3])
            self.C_RD = 0 - float(val[0])
            self.C_RP = 0 - float(val[1])
            self.C_RR = 0 - float(val[4])

            # Calibration Force and Moment
            self.C_L = (float(val[5]) + self.C_RL) * -3.42466
            self.C_D = (float(val[0]) + self.C_RD) * 0.39809
            self.C_S = (float(val[3]) + self.C_RS) * 0.8726

            self.C_P = (((float(val[1]) + self.C_RP) * 0.01744) -
                        ((float(val[0]) + self.C_RD) * 0.54184))
            self.C_R = (((float(val[4]) + self.C_RR) * 0.01709) -
                        ((float(val[3]) + self.C_RS) * 0.602))
            self.C_Y = ((float(val[2]) + self.C_RY) * 0.01573)

            while ((self.C_RL == 0 or self.C_RY == 0 or self.C_RS == 0 or self.C_RD == 0 or self.C_RP == 0 or self.C_RR == 0)
                   and (self.C_L == 0 or self.C_Y == 0 or self.C_S == 0 or self.C_D == 0 or self.C_P == 0 or self.C_R == 0)
                   ):
                self.C_RL = 0 - float(val[5])
                self.C_RY = 0 - float(val[2])
                self.C_RS = 0 - float(val[3])
                self.C_RD = 0 - float(val[0])
                self.C_RP = 0 - float(val[1])
                self.C_RR = 0 - float(val[4])

                self.C_L = (float(val[5]) + self.C_RL) * -3.42466
                self.C_D = (float(val[0]) + self.C_RD) * 0.39809
                self.C_S = (float(val[3]) + self.C_RS) * 0.8726

                self.C_P = (
                    ((float(val[1]) + self.C_RP) * 0.01744) - ((float(val[0]) + self.C_RD) * 0.54184))
                self.C_R = (
                    ((float(val[4]) + self.C_RR) * 0.01709) - ((float(val[3]) + self.C_RS) * 0.602))
                self.C_Y = ((float(val[2]) + self.C_RY) * 0.01573)

            print(
                f"Calibration R : {self.C_RL}, {self.C_RY}, {self.C_RS}, {self.C_RD}, {self.C_RP}, {self.C_RR}")
            print(
                f"RL : {float(val[5]) + self.C_RL}, RY : {float(val[2]) + self.C_RY}, RS : {float(val[3]) + self.C_RS}, RD : {float(val[0]) + self.C_RD}, RP : {float(val[1]) + self.C_RP}, RR : {float(val[4]) + self.C_RR},"
            )
            print(
                f"Calibration F & M : {self.C_L}, {self.C_Y}, {self.C_S}, {self.C_D}, {self.C_P}, {self.C_R}")
            print(
                f"L : {(float(val[5]) + self.C_RL) + self.C_L}, Y : {(float(val[2]) + self.C_RY) + self.C_Y}, S : {(float(val[3]) + self.C_RS) + self.C_S}, D : {(float(val[0]) + self.C_RD) + self.C_D}, P : {(float(val[1]) + self.C_RP) + self.C_P}, R : {(float(val[4]) + self.C_RR) + self.C_R},"
            )

            self.CalibrationButton.configure(
                bg='#ffcccb', disabledforeground='black', state=tk.DISABLED)
            self.startMeasureButton.configure(
                bg='#00ff00', state=tk.NORMAL)
            self.stopMeasureButton.configure(
                bg='red', state=tk.NORMAL)
            self.restartCalibrateButton.configure(
                bg='red', state=tk.NORMAL)

        else:
            tk.messagebox.showerror(
                title="Port not Connected", message="Connect Force Balance Device First!")

    def restartCalibrate(self):
        self.RL = []
        self.RS = []
        self.RD = []
        self.RY = []
        self.RR = []
        self.RP = []
        self.X = []
        self.count = 0
        self.TableFrame.table.delete(*self.TableFrame.table.get_children())
        self.ax.clear()
        self.plot_graph.draw()

        self.CalibrationButton.configure(
            highlightbackground="black",
            activebackground='red',
            bg='#00ff00',
            state=tk.NORMAL
        )
        self.startMeasureButton.configure(
            highlightbackground="black",
            activebackground='red',
            bg='#ffcccb',
            state=tk.DISABLED,
            disabledforeground='black')
        self.stopMeasureButton.configure(
            highlightbackground="black",
            activebackground='#ffcccb',
            state=tk.DISABLED,
            bg='#ffcccb',
            disabledforeground='black')
        self.restartCalibrateButton.configure(
            highlightbackground="black",
            activebackground='#ffcccb',
            state=tk.DISABLED,
            bg='#ffcccb',
            disabledforeground='black')

        print("restart")

    def start_measure(self):
        self.isRead = True
        threading.Thread(target=self.read_serial).start()
        serial_arduino.write("Start Measure".encode('utf-8'))

    def stop_measure(self):
        self.isRead = False
        threading.Thread(target=self.read_serial).start()

    def plot(self):
        self.ax.clear()

        self.ax.plot(self.X, self.RY, label='Yaw', linewidth=1)
        self.ax.plot(self.X, self.RP, label='Pitch', linewidth=1)
        self.ax.plot(self.X, self.RL, label='Lift', linewidth=1)
        self.ax.plot(self.X, self.RD, label='Drag', linewidth=1)
        self.ax.plot(self.X, self.RR, label='Roll', linewidth=1)
        self.ax.plot(self.X, self.RS, label='Side', linewidth=1)
        # self.ax.set_xlim([0, 1000])
        # self.ax.set_ylim([-900, 900])
        self.ax.set_title("Force Balance")
        self.ax.legend(['Yaw', 'Pitch', 'Lift', 'Drag', 'Roll', 'Side'])
        self.ax.yaxis.set_major_locator(MaxNLocator(prune='lower'))
        self.plot_graph.draw()

    def Table(self):
        columns = ('n', 'Yaw', 'Pitch', 'Roll', 'Drag', 'Lift', 'Side')
        self.TableFrame.table = ttk.Treeview(
            self.TableFrame, columns=columns, show='headings')
        self.TableFrame.table.heading('n', text='n')
        self.TableFrame.table.heading('Yaw', text='Yaw')
        self.TableFrame.table.heading('Pitch', text='Pitch')
        self.TableFrame.table.heading('Roll', text='Roll')
        self.TableFrame.table.heading('Lift', text='Lift')
        self.TableFrame.table.heading('Drag', text='Drag')
        self.TableFrame.table.heading('Side', text='Side')
        col_width = self.TableFrame.table.winfo_width()
        self.TableFrame.table.column("# 1", anchor=tk.CENTER, width=2)
        self.TableFrame.table.column("# 2", anchor=tk.CENTER, width=col_width)
        self.TableFrame.table.column("# 3", anchor=tk.CENTER, width=col_width)
        self.TableFrame.table.column("# 4", anchor=tk.CENTER, width=col_width)
        self.TableFrame.table.column("# 5", anchor=tk.CENTER, width=col_width)
        self.TableFrame.table.column("# 6", anchor=tk.CENTER, width=col_width)
        self.TableFrame.table.column("# 7", anchor=tk.CENTER, width=col_width)
        self.TableFrame.table.grid(row=0,  column=0, sticky="nsew")
        self.TableFrame.scrollbar = tk.Scrollbar(
            self.TableFrame,
            orient=tk.VERTICAL,
            command=self.TableFrame.table.yview,
            activebackground='#00ff00'
        )

        self.TableFrame.table.configure(yscroll=self.TableFrame.scrollbar.set)
        self.TableFrame.scrollbar.grid(row=0, column=1, sticky="nse")

    def save_as_file(self):
        lst = []
        col = ['n', 'Yaw', 'Pitch', 'Roll', 'Lift', 'Drag', 'Side']
        if (len(self.TableFrame.table.get_children()) < 1):
            print("not save")
        else:
            print("Saving to Excel")
            filename = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save To Excel",
                filetypes=(("xlsx File", "*.xlsx"), ("All Files", "*.*"))
            )

            with open('temp.csv', mode='w', newline='') as f:
                csvwriter = csv.writer(f, delimiter=',')
                for row_id in self.TableFrame.table.get_children():
                    row = self.TableFrame.table.item(row_id, 'values')
                    lst.append(row)
                lst = list(map(list, lst))
                lst.insert(0, col)
                for row in lst:
                    csvwriter.writerow(row)
            writer = pd.ExcelWriter(filename + '.xlsx')
            df = pd.read_csv('temp.csv', delimiter=',')
            df.to_excel(writer, 'sheetname')
            writer.save()
            tk.messagebox.showinfo(
                title="Save To Excel", message="Success Saving To Excel")

    def read_serial(self):
        while self.isRead:
            if serial_arduino.isOpen():
                serial_arduino.flushInput()
                val = serial_arduino.readline()
                while not '\\n' in str(val):
                    time.sleep(.001)
                    temp = serial_arduino.readline()
                    if not not temp.decode():
                        val = (val.decode()+temp.decode()).encode()
                val = val.decode().rstrip().split(',')

                # RD, RP, RY, RS, RR, RL

                self.RL.append(
                    ((float(val[5]) + self.C_RL) * -3.42466) + self.C_L)
                self.RD.append(
                    ((float(val[0]) + self.C_RD) * -2.148 + self.C_D))

                self.RS.append(
                    ((float(val[3]) + self.C_RS) * 1.135) + self.C_S)

                self.RP.append((((float(val[1]) + self.C_RP) * 0.01744) -
                                ((float(val[0]) + self.C_RD) * 0.54184)) + self.C_P)
                self.RR.append(((((float(val[4]) + self.C_RR) * 0.01709) +
                                ((float(val[3]) + self.C_RS) * 0.602)) + self.C_R) * 100)
                self.RY.append(
                    ((float(val[2]) + self.C_RY) * 0.01573) + self.C_Y)

                self.X.append(self.count)
                self.count = self.count + 1
                self.plot()
                # ('n', 'Yaw', 'Pitch', 'Roll', 'Drag', 'Lift', 'Side')

                self.TableFrame.table.insert(
                    "",
                    'end',
                    values=tuple([self.X[-1], self.RY[-1], self.RP[-1],
                                  self.RR[-1], self.RD[-1], self.RL[-1], self.RS[-1]])
                )
                self.TableFrame.table.yview_moveto(1)


if __name__ == '__main__':
    window = Window()
    window.mainloop()
