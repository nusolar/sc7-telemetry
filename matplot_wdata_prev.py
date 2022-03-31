#the same graphong thing but opens in  separate windows

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

fig2, a2x = plt.subplots(3,2) #MPPT1 In, Vin, Vout
a2x1I = a2x[0,0]
a2xM1I = a2x[0,1]
a2x1Vin = a2x[1,0]
a2xM1Vin = a2x[1,1]
a2x1Vo = a2x[2,0]
a2xM1Vo = a2x[2,1]

fig3, a3x = plt.subplots(3,2) #MPPT2 In, Vin, Vout
a3x2I = a3x[0,0]
a3xM2I = a3x[0,1]
a3x2Vin = a3x[1,0]
a3xM2Vin = a3x[1,1]
a3x2Vo = a3x[2,0]
a3xM2Vo = a3x[2,1]


#x and y axes
xs = [0,1,2,3,4,5,6,7,8,9,10] # for 10 seconds at a time
xst = [0, 1, 2, 3, 4 ,5, 6, 7, 8, 9, 10] #for the entire time
ys = queue.Queue(maxsize = 12)

otherClass = Receiver()
packets = list(otherClass.get_packets_from_file('examples\live_capture.txt'))

#x and y axes for plotting
#for 10 secs at a time
ry = []  #current
ry2 = [] #rpm
ry3 = [] #M1IN
ry4 = [] #M1Vin
ry5 = [] #M1Vo
ry6 = [] #M2In
ry7 = [] #M2Vin
ry8 = [] #M2Vout
rx = xs
# the entire thing
rxt = xst
ryt = [] #current
ryt2 = [] #rpm
ryt3 = [] #M1In
ryt4 = [] #M1Vin
ryt5 = [] #M1Vout
ryt6 = [] #M2In
ryt7 = [] #M2Vin
ryt8 = [] #M2Vout

infoRev = []
infoCurrent = []
info1Iin = []
info2Iin = []
info1Vin = []
info2Vin = []
info1Vo = []
info2Vo = []

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
    if want == 'M1Vin':
        for i in packets:
            if "Name" in i:
                if i["Name"] == "MPPT ANS Right":
                    info1Vin.append(i["Vin"])
    if want == 'M1Vo':
        for i in packets:
            if "Name" in i:
                if i["Name"] == "MPPT ANS Right":
                    info1Vo.append(i["Vout"])
    if want == "M2Iin":
        for i in packets:
            if "Name" in i:
                if i["Name"] == "MPPT ANS Left":
                    info2Iin.append(i["Iin"])
    if want == 'M2Vin':
        for i in packets:
            if "Name" in i:
                if i["Name"] == "MPPT ANS Left":
                    info2Vin.append(i["Vin"])
    if want == 'M2Vo':
        for i in packets:
            if "Name" in i:
                if i["Name"] == "MPPT ANS Left":
                    info2Vo.append(i["Vout"])
          

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
    if n == 4:
        grab_class("M1Vin")
        print("len2Vin: " + str(len(info1Vin))) #34
        for i in info1Vin[0:11]:
            ys.put(i)
    if n == 5:
        grab_class("M1Vo")
        print("len1Vo: " + str(len(info1Vo))) #34
        for i in info1Vo[0:11]:
            ys.put(i)
    if n == 6:
        grab_class("M2Iin")
        print("len2Iin: " + str(len(info2Iin))) #34
        for i in info2Iin[0:11]:
            ys.put(i)
    if n == 7:
        grab_class("M2Vin")
        print("len2Vin: " + str(len(info2Vin))) #34
        for i in info2Vin[0:11]:
            ys.put(i)
    if n == 8:
        grab_class("M2Vo")
        print("len2Vo: " + str(len(info2Vo))) #34
        for i in info2Vo[0:11]:
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
    if n == 4:
        ys.put(info1Vin[indx])
    if n == 5:
        ys.put(info1Vo[indx])
    if n == 6:
        ys.put(info2Iin[indx])
    if n == 7:
        ys.put(info2Vin[indx])
    if n == 8:
        ys.put(info2Vo[indx])

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
    filly(4)
    for i in range(11):
        t = ys.get()
    
        #plot stuff
        ryt4.append(t)
        ry4.append(t)
    filly(5)
    for i in range(11):
        t = ys.get()
    
        #plot stuff
        ryt5.append(t)
        ry5.append(t)
    filly(6)
    for i in range(11):
        t = ys.get()
    
        #plot stuff
        ryt6.append(t)
        ry6.append(t)
    filly(7)
    for i in range(11):
        t = ys.get()
    
        #plot stuff
        ryt7.append(t)
        ry7.append(t)
    filly(8)
    for i in range(11):
        t = ys.get()
        
        #plot stuff
        ryt8.append(t)
        ry8.append(t)

strt()

def toomuch():
    
    #10 seconds
    #first figure
    
    #Current (1)
    axC.clear()
    axC.plot(rx, ry[0:11], color="green")
    axC.set_title("10 Seconds (s)")
    #axC.set_xlabel("Time(s)")
    axC.set_ylabel("Main Current(amps)")
    
    #RPM (2)
    axR.clear()
    axR.plot(rx, ry2[0:11], color="green")
    #axR.set_xlabel("Time(s)")
    axR.set_ylabel("RPM (rev/min)")
    
    #second figure
    
    #MPPT1 Iin (3)
    a2x1I.clear()
    a2x1I.plot(rx, ry3[0:11], color="green")
    a2x1I.set_title("10 Seconds (s)")
    #a2x1I.set_xlabel("Time(s)")
    a2x1I.set_ylabel("MPPT1 Iin(amps)")
    
    #MPPT1 Vin (4)
    a2x1Vin.clear()
    a2x1Vin.plot(rx, ry4[0:11], color="green")
    #a2x1Vin.set_title("10 Seconds (s)")
    #a2x1Vin.set_xlabel("Time(s)")
    a2x1Vin.set_ylabel("MPPT1 Vin(V)")
    
    #MPPT1 Vo (5)
    a2x1Vo.clear()
    a2x1Vo.plot(rx, ry5[0:11], color="green")
    #a2x1Vo.set_title("10 Seconds (s)")
    #a2x1Vo.set_xlabel("Time(s)")
    a2x1Vo.set_ylabel("MPPT1 Vo(V)")
    
    
    #third figure
    
    #MPPT2 Iin (6)
    a3x2I.clear()
    a3x2I.plot(rx, ry6[0:11], color="green")
    a3x2I.set_title("10 Seconds (s)")
    #a3x2I.set_xlabel("Time(s)")
    a3x2I.set_ylabel("MPPT2 Iin(amps)")
    
    #MPPT2 Vin (7)
    a3x2Vin.clear()
    a3x2Vin.plot(rx, ry7[0:11], color="green")
    #a3x2Vin.set_title("10 Seconds (s)")
    #a3x2Vin.set_xlabel("Time(s)")
    a3x2Vin.set_ylabel("MPPT2 Vin(V)")
    
    #MPPT2 Vo (8)
    a3x2Vo.clear()
    a3x2Vo.plot(rx, ry8[0:11], color="green")
    #a3x2Vo.set_title("10 Seconds (s)")
    #a3x2Vo.set_xlabel("Time(s)")
    a3x2Vo.set_ylabel("MPPT2 Vo(V)")
    
    rx.pop(0)
    ry.pop(0)
    ry2.pop(0)
    ry3.pop(0)
    ry4.pop(0)
    ry5.pop(0)
    ry6.pop(0)
    ry7.pop(0)
    ry8.pop(0)
    rx.append(xs[-1] + 1)
    
    #All time
    #first figure
    
    #Current (1)
    axCC.clear()
    axCC.plot(rxt, ryt, color="green")
    axCC.set_title("All Time (s)")
    #axCC.set_xlabel("Time(s)")
    #axCC.set_ylabel("Temp(C)")
    
    #RPM (2)
    axRR.clear()
    axRR.plot(rxt, ryt2, color="green")
    #axRR.set_xlabel("Time(s)")
    #axRR.set_ylabel("RPM (rev/min)")
    
    
    #Second Figure
    
    #MPPT1 Iin (3)
    a2xM1I.clear()
    a2xM1I.plot(rxt, ryt3, color="green")
    a2xM1I.set_title("All Time (s)")
    #axM1I.set_xlabel("Time(s)")
    #axM1I.set_ylabel("MPPT1 (amps)")
    
    #MPPT1 Vin (4)
    a2xM1Vin.clear()
    a2xM1Vin.plot(rxt, ryt4, color="green")
    #a2xM1Vin.set_xlabel("Time(s)")
    #a2xM1Vin.set_ylabel("MPPT1 Vin(V)")
    
    #MPPT1 Vo (5)
    a2xM1Vo.clear()
    a2xM1Vo.plot(rxt, ryt5, color="green")
    #a2xM1Vin.set_xlabel("Time(s)")
    #a2xM1Vin.set_ylabel("MPPT1 Vo(V)")
    
    #Third Figure
    
    #MPPT2 Iin (6)
    a3xM2I.clear()
    a3xM2I.plot(rxt, ryt6, color="green")
    a3xM2I.set_title("All Time (s)")
    #a3xM2I.set_xlabel("Time(s)")
    #a3xM2I.set_ylabel("MPPT2 (amps)")
    
    #MPPT2 Vin (7)
    a3xM2Vin.clear()
    a3xM2Vin.plot(rxt, ryt7, color="green")
    #a3xM2Vin.set_xlabel("Time(s)")
    #a3xM2Vin.set_ylabel("MPPT2 Vin(V)")
    
    #MPPT2 Vo (8)
    a3xM2Vo.clear()
    a3xM2Vo.plot(rxt, ryt8, color="green")
    #a3xM2Vin.set_xlabel("Time(s)")
    #a3xM2Vin.set_ylabel("MPPT2 Vo(V)")
    
    

def temp_animate(i):
    #add new point onto the end of each y list
    oney(1)
    t1 = ys.get()
    oney(2)
    t2 = ys.get()
    oney(3)
    t3 = ys.get()
    oney(4)
    t4 = ys.get()
    oney(5)
    t5 = ys.get()
    oney(6)
    t6 = ys.get()
    oney(7)
    t7 = ys.get()
    oney(8)
    t8 = ys.get()
    
    global indx
    indx = indx + 1
    
    
    ry.append(t1)
    ry2.append(t2)
    ry3.append(t3)
    ry4.append(t4)
    ry5.append(t5)
    ry6.append(t6)
    ry7.append(t7)
    ry8.append(t8)
    
    axCC.figure.canvas.draw_idle()
    axRR.figure.canvas.draw_idle()
    a2xM1I.figure.canvas.draw_idle()
    a2xM1Vin.figure.canvas.draw_idle()
    a2xM1Vo.figure.canvas.draw_idle()
    a3xM2I.figure.canvas.draw_idle()
    a3xM2Vin.figure.canvas.draw_idle()
    a3xM2Vo.figure.canvas.draw_idle()
    
    toomuch()
    
    ryt.append(t1)
    ryt2.append(t2)
    ryt3.append(t3)
    ryt4.append(t4)
    ryt5.append(t5)
    ryt6.append(t6)
    ryt7.append(t7)
    ryt8.append(t8)
    
    rxt.append(rxt[-1] + 1)

ani = anim.FuncAnimation(fig, temp_animate, interval=1000) #supposed to be every second (1000)
plt.show()