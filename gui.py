from receiver import Receiver
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Frame):
    def __init__(self):
        super().__init__(tk.Tk())
        self._root().title('NUSolar Telemetry')
        self._root().configure()
        #Initialize tables
        self.battery_table = Table(self, (
            'Cell ID',
            'Instant Voltage',
            'Internal Resistence',
            'Open Voltage'),
            30, 'Battery Cells')
        self.mppt_table = Table(self,
            ('MPPT', 'Tamb', 'Vout', 'Iin', 'Vin'),
            3, 'MPPT ANS')
        self.vcsoc_table = Table(self,
            ('Current', 'Voltage', 'SoC'), 1, 'VCSOC')
        #Packing
        self.battery_table.pack()
        self.mppt_table.pack()
        self.vcsoc_table.pack()
        self.pack()
        #self.mainloop()

class Table:
    def __init__(self, parent, headers, height, name='Table'):
        self.parent = parent
        self.headers = headers
        self.height = height
        self.width = len(headers) 
        self.data =\
            [[tk.StringVar() for item in range(self.width)]\
            for row in range(height)]
        #Tk widgets
        self.frame = ttk.LabelFrame(parent, text=name, labelanchor='n')
        self.labels =\
            [[tk.Label(self.frame) for item in range(self.width)]
            for row in range(height+1)]
        #Couple data
        for row in range(height):
            for col in range(self.width):
                self.labels[row+1][col]['textvariable'] = self.data[row][col]
        #Populate headers
        for i, text in zip(range(self.width), headers):
            self.labels[0][i]['text'] = text
    def pack(self):
        self.frame.pack(fill='both', expand='yes', padx=10, pady=10)
        for row in range(self.height+1):
            for col in range(self.width):
                self.labels[row][col].grid(row=row, column=col)

if __name__ == "__main__":
    """Basic battery cell table GUI demo"""
    app = Application()
    for packet in Receiver().get_packets():
        #Update GUI
        mppt_mapping = {
            'MPPT ANS Sub': 0,
            'MPPT ANS Right': 1,
            'MPPT ANS Left': 2}
        if 'Name' in packet and packet['Name'] == 'Cell':
            for i in range(0, len(app.battery_table.headers)):
                app.battery_table.data[packet['Cell ID']][i]\
                    .set(packet[app.battery_table.headers[i]])
        elif 'Name' in packet and packet['Name'].startswith('MPPT ANS'):
            row = app.mppt_table.data[mppt_mapping[packet['Name']]]
            row[0].set(packet['Name'])
            for i in range(1, len(app.mppt_table.headers)):
                row[i].set(packet[app.mppt_table.headers[i]])
        elif 'Name' in packet and packet['Name'] == 'VCSOC':
            for i in range(1, len(app.vcsoc_table.headers)):
                app.vcsoc_table.data[0][i]\
                    .set(packet[app.vcsoc_table.headers[i]])
        #app.update_idletasks()
        app.update()
        sleep(0.2)
