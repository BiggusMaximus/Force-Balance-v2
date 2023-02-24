import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ser = serial.Serial('COM5', baudrate=9600)

ser.close()
ser.open()

fig = plt.figure()
axis = fig.subplots(2, 3)

x = []
RL = []
RD = []
RS = []
RR = []
RP = []
RY = []
i = 0


def animate():
    if ser.isOpen():
        if len(ser.readline().strip().decode("utf-8")) != 0:
            measure = [float(data) for data in ser.readline(
            ).strip().decode("utf-8").split(',')]

            x.append(i)
            RL.append(measure[0])
            RD.append(measure[1])
            RS.append(measure[2])
            RR.append(measure[3])
            RP.append(measure[4])
            RY.append(measure[5])

            print(x)
            print(RL)

            axis.clear()
            axis[0, 0].plot(x, RL)
            axis[0, 0].set_title("Lift")

            # For Cosine Function
            axis[0, 1].plot(x, RD)
            axis[0, 1].set_title("Drag")

            # For Tangent Function
            axis[0, 2].plot(x, RS)
            axis[0, 2].set_title("Side")

            # For Tanh Function
            axis[1, 0].plot(x, RR)
            axis[1, 0].set_title("Roll")

            axis[1, 1].plot(x, RP)
            axis[1, 1].set_title("Pitch")

            axis[1, 2].plot(x, RY)
            axis[1, 2].set_title("Yawn")

            i = i + 1


anim = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
