# This program uses collected data from serial to fix parsing.

# Modified to run pygame zero

# Size of window
HEIGHT = 800
WIDTH = 800
TITLE = "STATE OF CONSCIOUSNESS (SEVEN)"

cell_range = 36 #number of potential cells we have

FILE_READ = 0 #toggle to read from a file, for debugging, default is read from serial. Need to uncomment some things to make this work.

from serial import Serial
import serial
import sys
import struct
import time
import pandas as pd
import re
import pygcurse

# CAN data
cd = {}

cd['p'] = {
    'v': 0,
    'i': 0,
    't': 0
}
cd['mpptC'] = {
    'sub': 0,
    'right': 0,
    'left': 0
}
cd['cells'] = [None] * cell_range
for i in range(0, cell_range): # update range.
    cd['cells'][i] = {
        'voltage': 0.0,
        'temp': 0.0
    }
cd['system'] = {
    'Current': 0,
    'Voltage': 0,
    'SoC':0
}

class Parser:
    table = None

    def __init__(self, fileName):
        self.table = pd.read_csv(fileName, converters={
                                 "ID": lambda x: int(x, 16)})
        self.table.set_index("ID", inplace=True)
        for i, r in self.table.iterrows():
            count = 0
            n = 1
            while type(r[n * 2]) is int:
                count += r[n * 2]
                n += 1
            if count > 64:
                raise Exception("Row " + hex(i) + " is not consistent! "
                                "Expected bit sum of at most 64, but got " + str(count) + ". ")

    def getName(self, id):
        return self.table.loc[id]["Name"]

    def getData(self, id, rawData):
        fieldNames = []
        fieldValues = []
        bitCount = 0
        pairIndex = 1
        try:
            while pairIndex <= self.table.shape[1] - 1 and type(self.table.loc[id][pairIndex]) is str:
                fieldNames = fieldNames + [self.table.loc[id][pairIndex]]
                bitLength = self.table.loc[id][pairIndex + 1]
                # Right shift so that the last byteLength bytes are our data
                val = rawData >> int(64 - bitLength - bitCount)
                # Mask off the bytes more significant than byteLength
                val = val & int((1 << int(bitLength)) - 1)
                fieldValues = fieldValues + [val]
                pairIndex += 2
                bitCount += bitLength
        except:
            print("Not in list?")
        return fieldNames, fieldValues

# List to dictionary
def l2d(names, vals):
    x = {}
    for i in range(len(names)):
        x[names[i]] = vals[i]
    return x

def centerify(text, width=-1):
  lines = text.split('\n')
  width = max(map(len, lines)) if width == -1 else width
  return '\n'.join(line.center(width) for line in lines)

def twos_complement_hex(hexstr,bits):
    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

def twos_complement_int(value,bits):
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

def draw():
    global cd
    screen.fill((0,0,0))

    for i in range(0,18):
        screen.draw.text("Cell number: "+str(i)+" "+ "Voltage: "+str(cd['cells'][i]['voltage'])+" "+"Temp: "+str(cd['cells'][i]['temp']), (10, 20*i), color="orange", fontsize=20)
    for i in range(18,cell_range):
        screen.draw.text("Cell number: "+str(i)+" "+ "Voltage: "+str(cd['cells'][i]['voltage'])+" "+"Temp: "+str(cd['cells'][i]['temp']), (400, 20*(i-18)), color="orange", fontsize=20)
    
    system_current = twos_complement_int(cd['system']['Current'],16)*0.1
    system_voltage = cd['system']['Voltage']*0.1

    screen.draw.text("Current: "+str(system_current)+" A "+"Voltage: "+str(system_voltage)+" V "+"SoC: "+str(cd['system']['SoC']),(100,450),color = "orange",fontsize=40)
    screen.draw.text("Sub: "+str(cd['mpptC']['sub']*8.72)+"mA "+"Right: "+str(cd['mpptC']['right']*8.72)+"mA "+"Left: "+str(cd['mpptC']['left']*8.72)+"mA",(100,550),color = "orange",fontsize=40)
    screen.draw.text("Temp: "+str(cd['p']['t']),(100,650),color = "orange",fontsize = 40)
def update(dt):
    # read serial here.
    global cd

    line = ser.read_until(b'\r')
    #print(line)
    #line = line[2:-1] # clean the line up remove b' and ''
    #line = ser.read_until().strip() #strip() removes the \r\n
    line = line.decode('UTF-8')
    print(line) # we should get something like this : t0368039C2000FE9C25BC 
    i = line[1:-1] # remove t and /r
    #print(i.decode('UTF-8'))
    #i = i.decode('UTF-8')
    print(len(i))
    try:
        localID = int(str(i)[0:3],16) #okay localid is now right
        data_len = int(str(i)[3],16) #length of data string
        end = data_len*2+4 #get local data
        #print(end)
        #localData = str(i)[4:end]
        localData = int(str(i)[3:end],16) # we have about 5 bits of random data at the end, cut them out.

        #print(localData)
        names, vals = p.getData(localID, localData)
        print(names)
        print(vals)
        nv = l2d(names, vals)
        print(nv)
        print(names)
        print(vals)
        if localID == 0x36:
            cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']
        elif localID == 0x5F0:
            # okay what is going on here.
            # offset = localID - 0x5F0
            #print(7 + offset * 8)
            #print( 7 + offset * 8 + 7)
            for n in range(1,6):
                cd['cells'][n]['temp']=nv['Mod %d' % n]
            cd['p']['t']=nv['Max Temp']
        elif localID >= 0x5F1 and localID <=0x5F3:
          # okay what is going on here.
            offset = localID - 0x5F1
            #print(7 + offset * 8)
            #print( 7 + offset * 8 + 7)
            #  1 - 6, 7 - 15, 15 - 23,23-31
            for n in range(7+ (offset)*8, 15+ (offset)*8): # might want to double check this math (Ben: is wrong)
                cd['cells'][n-1]['temp'] = nv['Mod %d' % n] 
        elif localID == 0x6B0:
            # current data
            cd['system']['Current'] = nv['Current']
            cd['system']['Voltage'] = nv['Voltage']
            cd['system']['SoC'] = nv['SoC']
        elif localID == 0x771:
            cd['mpptC']['sub'] = nv['Iin']
        elif localID == 0x772:
            cd['mpptC']['right'] = nv['Iin']
        elif localID == 0x773:
            cd['mpptC']['left'] = nv['Iin']


    except:
        print("length error?")
  


    if FILE_READ == 1:


        
        i = f.readline()
        #print(i)
        #print(len(i))
        #slice away unnessary parts here
        #print(i)
        #print(i[1:-1])
        i = i[1:-1] # remove t and /r
        print(i)
        localID = int(str(i)[0:3],16) #okay localid is now right
        data_len = int(str(i)[3],16) #length of data string
        end = data_len*2+4 #get local data
        #print(end)
        #localData = str(i)[4:end]
        localData = int(str(i)[3:end],16) # we have about 5 bits of random data at the end, cut them out.

        #print(localData)
        names, vals = p.getData(localID, localData)
        print(names)
        print(vals)
        nv = l2d(names, vals)
        print(nv)
        print(names)
        print(vals)
        if localID == 0x36:
            cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']
        elif localID == 0x5F0:
            # okay what is going on here.
            # offset = localID - 0x5F0
            #print(7 + offset * 8)
            #print( 7 + offset * 8 + 7)
            for n in range(1,6):
                cd['cells'][n]['temp']=nv['Mod %d' % n]
            cd['p']['t']=nv['Max Temp']
        elif localID >= 0x5F1 and localID <=0x5F3:
          # okay what is going on here.
            offset = localID - 0x5F1
            #print(7 + offset * 8)
            #print( 7 + offset * 8 + 7)
            #  1 - 6, 7 - 15, 15 - 23,23-31
            for n in range(7+ (offset)*8, 15+ (offset)*8): # might want to double check this math (Ben: is wrong)
                cd['cells'][n-1]['temp'] = nv['Mod %d' % n] #offset by 1, MOD starts from 1, but array counts from 0



        # for n in range( 6+ offset * 8, 6 + offset * 8): # might want to double check this math (Ben: is wrong)
        #     print()
        #     cd['cells'][n] = nv['Mod %d' % n]



#     if len(i)==24: # we currently have 24, but really we need to check len 20 - because we have string and original is byte encoded.
#         print(i)
#         localID = int(str(i)[1:4], 16) #slice away t  
#         print(localID) 
#         #print(str(localID))
#         #print(i[5:-2]) # slice away /r
#         localDat = int(str(i)[4:-1], 16)
#         #print(i) # print the packet length
#         names, vals = p.getData(localID, localDat)
#         nv = l2d(names, vals)
#         print(names)
#         print(vals)
#         if localID == 0x36:
#             cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']




# Create the virtual terminal
#window = pygcurse.PygcurseWindow(60, 33)




def drawUpdate():
    global cd
    print(cd)
    # reset the cursor and clear the screen
    window.cursory = 0
    window.cursorx = 0
    #Uncomment this line if there are issues with text not getting overwritten
    #window.setscreencolors('white', 'black', clear=True)

    # DRAW CELLS
    window.putchars(centerify("-----CELLS-----", 60))
    window.cursory += 1

    for i in range(0, 30):
        window.putchars(
            "%.2f  , %.2f" %
            (
                cd['cells'][i]['voltage']/1000,
                cd['cells'][i]['temp']/1000
            )
        )
        if i < 24:
            window.cursorx += 11
            window.putchar('|')
            window.cursorx -= 11
        window.cursory += 1
        if (i + 1) % 6 == 0:
            # window.curosrx = 0
            window.cursorx += 12
            window.cursory -= 6

    # DRAW MPPT CURRENTS
    # reset the cursor from the previous section
    window.cursorx = 0
    window.cursory += 6
    window.pygprint(centerify("-----MPPT CURRENT-----", 60))
    window.pygprint("%7s: %d" % ('Sub', cd['mpptC']['sub']))
    window.pygprint("%7s: %d" % ('Left', cd['mpptC']['left']))
    window.pygprint("%7s: %d\n\n" % ('Right', cd['mpptC']['right']))

    # DRAW PACK STAT
    window.pygprint(centerify("-----PACK-----", 60))
    window.pygprint("%9s: %d" % ('Current', cd['p']['i']))
    window.pygprint("%9s: %d" % ('Voltage', cd['p']['v']))
    window.pygprint("%9s: %d" % ('Max temp', cd['p']['t']))

    

# For testing: witness the data increase in size
# while True:
#     cd['cells'][0]['voltage'] += 1
#     time.sleep(1)
#     drawUpdate()


p = Parser("id-table.csv")

# if sys.argv[0]==0: #select serial
#     port = sys.argv[1]
#     ser = serial.Serial(port, 57600)
# elif sys.argv[0]==1:
#     f=open(sys.argv)

f = open('live_capture.txt')
ser = serial.Serial('COM82',57600)
# while True:
#     #msg = ser.read(1000)  # read data
#     #x = msg.split(b'\r')  # Segment data stream into packets

#     #for i in x:
#     #    print(i)
#     line = ser.read_until(b'\r')
#     #print(line)
#     #line = line[2:-1] # clean the line up remove b' and ''
#     #line = ser.read_until().strip() #strip() removes the \r\n
#     line = line.decode('UTF-8')
#     print(line) # we should get something like this : t0368039C2000FE9C25BC 
#     i = line[1:-1] # remove t and /r
#     #print(i.decode('UTF-8'))
#     #i = i.decode('UTF-8')
#     localID = int(str(i)[0:3],16) #okay localid is now right
#     data_len = int(str(i)[3],16) #length of data string
#     end = data_len*2+4 #get local data
#     #print(end)
#     #localData = str(i)[4:end]
#     localData = int(str(i)[3:end],16) # we have about 5 bits of random data at the end, cut them out.

#     #print(localData)
#     names, vals = p.getData(localID, localData)
#     print(names)
#     print(vals)
#     nv = l2d(names, vals)
#     print(nv)
#     print(names)
#     print(vals)
#     if localID == 0x36:
#         cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']
#     elif localID == 0x5F0:
#         # okay what is going on here.
#         # offset = localID - 0x5F0
#         #print(7 + offset * 8)
#         #print( 7 + offset * 8 + 7)
#         for n in range(1,6):
#             cd['cells'][n]['temp']=nv['Mod %d' % n]
#     elif localID >= 0x5F1 and localID <=0x5F3:
#       # okay what is going on here.
#         offset = localID - 0x5F1
#         #print(7 + offset * 8)
#         #print( 7 + offset * 8 + 7)
#         #  1 - 6, 7 - 15, 15 - 23,23-31
#         for n in range(7+ (offset)*8, 15+ (offset)*8): # might want to double check this math (Ben: is wrong)
#             cd['cells'][n-1]['temp'] = nv['Mod %d' % n] #offset by 1, MOD starts from 1, but array counts from 0



    # #while ser.in_waiting:
    #     line = ser.read_until().strip() #strip() removes the \r\n
    #     print(line) # we should get something like this : t0368039C2000FE9C25BC

#init code, I don't think we need this

# ser.write("\rZ0\r".encode("UTF-8"))

# ser.write("S5\r".encode("UTF-8"))

# ser.write("X1\r".encode("UTF-8"))

# ser.write("C\r".encode("UTF-8"))

# time.sleep(1)

# ser.write("O\rA\r".encode("UTF-8"))




#port = sys.argv[1]

#ser = serial.Serial(port, 57600)

#ser.write("\rZ0\r".encode("UTF-8"))

#ser.write("S5\r".encode("UTF-8"))

#ser.write("X1\r".encode("UTF-8"))

#ser.write("C\r".encode("UTF-8"))

#time.sleep(1)

#ser.write("O\rA\r".encode("UTF-8"))

#file = open("sim_data.txt","r")
#print(file.read())


# with open("live_capture.txt","r") as x:
#     # TODO: make this continuous optioon outside loop
#     #ser.write("P\r".encode("UTF-8"))
#     #msg = ser.read(1000)  # read data
#     #x = msg.split(b'\rt')  # Segment data stream into packets
#     #msg = re.findall('\'.*\'', msg)[0][1:-1]
#     #note we need to parse for this nonsense
#     #t036  80E 86D2 0161 8698 24 (7C23)
#     #xxxx(CAN ID) | x (DATA LENGTH/BYTES) | ????(DATA)
#     for i in x:
#         #slice away unnessary parts here
#         #print(i)
#         #print(i[1:-1])
#         i = i[1:-1] # remove t and /r
#         print(i)
#         localID = int(str(i)[0:3],16) #okay localid is now right
#         data_len = int(str(i)[3],16) #length of data string
#         end = data_len*2+4 #get local data
#         #print(end)
#         #localData = str(i)[4:end]
#         localData = int(str(i)[3:end],16) # we have about 5 bits of random data at the end, cut them out.

#         print(localData)
#         names, vals = p.getData(localID, localData)
#         print(names)
#         print(vals)

        

    

        #check if length is long enough
        #print(i[1:-1])
        #print(len(i[1:-1]))



        # if len(i)==26: # we currently have 24, but really we need to check len 20 - because we have string and original is byte encoded.
        #     print(i)
        #     localID = int(str(i)[2:4], 16) #slice away b'  
        #     print(localID) 
        #     #print(str(localID))
        #     #print(i[5:-2]) # slice away '/r
        #     localDat = int(str(i)[5:-1], 16)
        #     print()
        #     #print(i) # print the packet length
        #     names, vals = p.getData(localID, localDat)
        #     nv = l2d(names, vals)
        #     print(nv)
        #     print(names)
        #     print(vals)
        #     if localID == 0x36:
        #         cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']

            #drawUpdate()

        # ##print(i[2:-2])
        # i = i[2:-2]
        # #print(i) # this is the message, parse data using parser.

        # if len(i) == 20:
        #     localID = int(str(i)[0:3], 16) # bus | client identifier | identifier | F | L | Data
        #     print(localID)
        #     localDat = int(str(i)[4:-1], 16)
        #     print(localDat)
        #     names, vals = p.getData(localID, localDat)
        #     nv = l2d(names, vals)
        #     print(names)
        #     print(vals)



        #i = i[2:-2]
        #z = i.split(b'\rt')  # Segment data stream into packets
        # if len(i) == 20: # if the packet length is 20, then
        #     localID = int(str(i)[2:5], 16) # bus | client identifier | identifier | F | L | Data
        #     #print(str(localID))
        #     localDat = int(str(i)[5:-1], 16)
        #     print(i) # print the packet length
        #     names, vals = p.getData(localID, localDat)
        #     nv = l2d(names, vals)
        #     print(names)
        #     print(vals)
        #     print(localID)
        #     # Hacky ass fix - note that fails on cell 25
        #     #if localID == 54:
        #     #	cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']



        #     #all this are wrong - local ids are all the same!!


        #     # EXAMPLE: how to update the dictionary with a new values
        #     if localID == 0x32:
        #         cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']
        #     elif localID == 0x5F0:
        #         cd['p']['t'] = nv['Max Temp']
        #         for n in range(1, 6):
        #             cd['cells'][n] = nv['Mod %d' % n]
        #     elif localID >= 0x5F1 and localID <=0x5F3:
        #     	# okay what is going on here.
        #         offset = localID - 0x5F1
        #         #print(7 + offset * 8)
        #         #print( 7 + offset * 8 + 7)
        #         for n in range(7 + offset * 8, 7 + offset * 8 + 7): # might want to double check this math (Ben: is wrong)
        #             cd['cells'][n] = nv['Mod %d' % n]
        #     elif localID == 0x21:
        #         cd['p']['v'] = nv['Instant Voltage']
        #         # TODO: Add current (I couldn't find it)
        #     elif localID == 0x771:
        #         cd['mpptC']['sub'] = nv['Iin']
        #     elif localID == 0x772:
        #         cd['mpptC']['right'] = nv['Iin']
        #     elif localID == 0x773:
        #         cd['mpptC']['right'] = nv['Iin']
        #     #print(cd)
        #     drawUpdate()
        # # if extended IDs are needed, handle differently if needed
        # if len(i) == 25:
        #     pass
        

