# This program uses collected data from serial to fix parsing.

# Modified to run pygame zero

HEIGHT = 600
WIDTH = 600
TITLE = "BASIC SOLAR TELEMETRY"
cell_range = 30

from serial import Serial
import serial
import sys
import struct
import time
import pandas as pd
import re
import pygcurse


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

def draw():
    screen.fill((0,0,0))
    for i in range(0,30):
        screen.draw.text("Voltage: "+str(cd['cells'][i]['voltage'])+" "+"Temp: "+str(cd['cells'][i]['temp']), (20, 20*i), color="orange", fontsize=20)

f = open('updated_cleaned.txt')

def update(dt):
    # read serial here.
    global f,cd
    i = f.readline()
    print(i)
    print(len(i))


    if len(i)==24: # we currently have 24, but really we need to check len 20 - because we have string and original is byte encoded.
        print(i)
        localID = int(str(i)[2:5], 16) #slice away b'  
        print(localID) 
        #print(str(localID))
        #print(i[5:-2]) # slice away '/r
        localDat = int(str(i)[5:-2], 16)
        #print(i) # print the packet length
        names, vals = p.getData(localID, localDat)
        nv = l2d(names, vals)
        print(names)
        print(vals)
        if localID == 0x36:
            cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']




# Create the virtual terminal
#window = pygcurse.PygcurseWindow(60, 33)

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
cd['cells'] = [None] * 30
for i in range(0, 30): # update range.
    cd['cells'][i] = {
        'voltage': 0.0,
        'temp': 0.0
    }


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


# with open("updated_cleaned.txt","r") as x:
#     # TODO: make this continuous optioon outside loop
#     #ser.write("P\r".encode("UTF-8"))
#     #msg = ser.read(1000)  # read data
#     #x = msg.split(b'\rt')  # Segment data stream into packets
#     #msg = re.findall('\'.*\'', msg)[0][1:-1]
#     for i in x:
#         #slice away unnessary parts

    

#         #check if length is long enough
#         print(i)
#         print(len(i))


#         if len(i)==24: # we currently have 24, but really we need to check len 20 - because we have string and original is byte encoded.
#             print(i)
#             localID = int(str(i)[2:5], 16) #slice away b'  
#             print(localID) 
#             #print(str(localID))
#             #print(i[5:-2]) # slice away '/r
#             localDat = int(str(i)[5:-2], 16)
#             #print(i) # print the packet length
#             names, vals = p.getData(localID, localDat)
#             nv = l2d(names, vals)
#             print(names)
#             print(vals)
#             if localID == 0x36:
#                 cd['cells'][nv['Cell ID']]['voltage'] = nv['Instant Voltage']

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
        

