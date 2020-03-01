import random
import queue
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as anim
from matplotlib import style
from receiver import Receiver
import sys

fig, ax = plt.subplots(2,2) #Current, RPM
axC = ax[0,0]
axCC = ax[0,1]
axR = ax[1,0]
axRR = ax[1,1]

fig2, a2x = plt.subplots(2,2) #MPPT1 In
a2x1I = a2x[0,0]
a2xM1I = a2x[0,1]
a2x2I = a2x[1,0]
a2xM2I = a2x[1,1]

#x and y axes
xs = [0,1,2,3,4,5,6,7,8,9,10]
xst = [0, 1, 2, 3, 4 ,5, 6, 7, 8, 9, 10]
ys = queue.Queue(maxsize = 12)

otherClass = Receiver()
packets = list(otherClass.get_packets_from_file('examples\live_capture.txt'))

#x and y axes for plotting
#for 10 secs at a time
ry = []  #current
ry2 = [] #rpm
ry3 = [] #M1IN
ry6 = [] #M2In
rx = xs
# the entire thing
rxt = xst
ryt = [] #current
ryt2 = [] #rpm
ryt3 = [] #M1In
ryt6 = [] #M2In

infoRev = []
infoCurrent = []
info1Iin = []
info2Iin = []

def grab_class(want):
    if want == 'Current':
        for i in packets:
            if want in i:
                infoCurrent.append(i[want])
    if want == 'Rev':
        for i in packets:
            if want in i:
                infoRev.append(i[want])
    if want == 'M1Iin':
        for i in packets:
            if "Name" in i:
                if i["Name"] == "MPPT ANS Right":
                    info1Iin.append(i["Iin"])
    if want == "M2Iin":
        for i in packets:
            if "Name" in i:
                if i["Name"] == "MPPT ANS Left":
                    info2Iin.append(i["Iin"])
          


style.use("seaborn-whitegrid")

#to fill the y-axis
def filly(n):
    if n == 1:
        grab_class("Current")
        print("lenC: " + str(len(infoCurrent))) #164
        for i in infoCurrent[0:11]:
            ys.put(i)
    if n == 2:
        for i in range(11):
            randy = random.randint(0,20)
            ys.put(randy)
    if n == 3:
        grab_class("M1Iin")
        print("len1Iin: " + str(len(info1Iin))) #34
        for i in info1Iin[0:11]:
            ys.put(i)
    if n == 6:
        grab_class("M2Iin")
        print("len2Iin: " + str(len(info2Iin))) #34
        for i in info2Iin[0:11]:
            ys.put(i)

indx = 12
#add one y-value
def oney(n):
    global indx #need this in order to change global variable
    
    if n == 1:
        ys.put(infoCurrent[indx])
    if n == 2:
        randy = random.randint(0,20)  #rpm
        ys.put(randy)
    if n == 3:
        ys.put(info1Iin[indx])
    if n == 6:
        ys.put(info2Iin[indx])

# make first 11 y-values
def strt():
    filly(1)
    for i in range(11):
        t = ys.get()
    
        #plot stuff
        ryt.append(t)
        ry.append(t)
    filly(2)
    for i in range(11):
        t = ys.get()
    
        #plot stuff
        ryt2.append(t)
        ry2.append(t)
    filly(3)
    for i in range(11):
        t = ys.get()
    
        #plot stuff
        ryt3.append(t)
        ry3.append(t)
    filly(6)
    for i in range(11):
        t = ys.get()
    
        #plot stuff
        ryt6.append(t)
        ry6.append(t)

strt()

def toomuch():
    
    #10 seconds
    #first figure
    
    #Current (1)
    axC.clear()
    axC.plot(rx, ry[0:11], color="purple")
    axC.set_title("Current - 10 Seconds (s)")
    axC.set_ylabel("Main Current(amps)")
    
    #RPM (2)
    axR.clear()
    axR.plot(rx, ry2[0:11], color="purple")
    axR.set_title("RPM - 10 Seconds (s)")
    axR.set_xlabel("Time(s)")
    axR.set_ylabel("RPM (rev/min)")
    
    #second figure
    
    #MPPT1 Iin (3)
    a2x1I.clear()
    a2x1I.plot(rx, ry3[0:11], color="purple")
    a2x1I.set_title("MPPT1 Current - 10 Seconds (s)")
    a2x1I.set_ylabel("MPPT1 Iin(amps)")
    
    #MPPT2 Iin (6)
    a2x2I.clear()
    a2x2I.plot(rx, ry6[0:11], color="purple")
    a2x2I.set_title("MPPT2 Current - 10 Seconds (s)")
    a2x2I.set_xlabel("Time(s)")
    a2x2I.set_ylabel("MPPT2 Iin(amps)")
    
    rx.pop(0)
    ry.pop(0)
    ry2.pop(0)
    ry3.pop(0)
    ry6.pop(0)
    rx.append(xs[-1] + 1)
    
    #All time
    #first figure
    
    #Current (1)
    axCC.clear()
    axCC.plot(rxt, ryt, color="purple")
    axCC.set_title("Cuurent - All Time (s)")
    
    #RPM (2)
    axRR.clear()
    axRR.plot(rxt, ryt2, color="purple")
    axRR.set_title("RPM - All Time (s)")
    axRR.set_xlabel("Time(s)")
    
    
    #Second Figure
    
    #MPPT1 Iin (3)
    a2xM1I.clear()
    a2xM1I.plot(rxt, ryt3, color="purple")
    a2xM1I.set_title("MPPT1 Current - All Time (s)")
    
    #MPPT2 Iin (6)
    a2xM2I.clear()
    a2xM2I.plot(rxt, ryt6, color="purple")
    a2xM2I.set_title("MPPT2 - All Time (s)")
    a2xM2I.set_xlabel("Time(s)")
    

def temp_animate(i):
    #add new point onto the end of each y list
    oney(1)
    t1 = ys.get()
    oney(2)
    t2 = ys.get()
    oney(3)
    t3 = ys.get()
    oney(6)
    t6 = ys.get()
    
    global indx
    indx = indx + 1
    
    ry.append(t1)
    ry2.append(t2)
    ry3.append(t3)
    ry6.append(t6)
    
    axCC.figure.canvas.draw_idle()
    axRR.figure.canvas.draw_idle()
    a2xM1I.figure.canvas.draw_idle()
    a2xM2I.figure.canvas.draw_idle()
    
    toomuch()
    
    ryt.append(t1)
    ryt2.append(t2)
    ryt3.append(t3)
    ryt6.append(t6)
    
    rxt.append(rxt[-1] + 1)
    

ani = anim.FuncAnimation(fig, temp_animate, interval=1000) #supposed to be every second (1000)
plt.show()

    
