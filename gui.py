from receiver import Receiver
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Frame):
    def __init__(self):
        super().__init__(tk.Tk())
        self._root().title('NUSolar Telemetry')
        self._root().configure()
        #Initialize battery cell table data & labels
        cell_table = ttk.LabelFrame(self, text='Battery Cells', labelanchor='n')
        cell_table.pack(fill='both', expand='yes', padx=10, pady=10)
        self.cell_data =\
            [[tk.IntVar() for item in range(4)]\
            for row in range(30)]
        cell_labels =\
            [[tk.Label(cell_table) for item in range(len(self.cell_data[0]))]\
            for row in range(len(self.cell_data)+1)]
        for i, text in zip(range(len(cell_labels[0])), (\
            'Cell ID',\
            'Instant Voltage',\
            'Internal Resistence',\
            'Open Voltage')):
            cell_labels[0][i]['text'] = text
            cell_labels[0][i].grid(row=0, column=i)
        for i in range(len(self.cell_data)):
            for j in range(len(self.cell_data[0])):
                self.cell_data[i][j].set(i)\
                    if j == 0 else\
                    self.cell_data[i][j].set(0)
                cell_labels[i+1][j]['textvariable'] = self.cell_data[i][j]
                cell_labels[i+1][j].grid(row=i+1, column=j)
        self.pack()
        #self.mainloop()

if __name__ == "__main__":
    """Basic battery cell table GUI demo"""
    app = Application()
    for packet in Receiver().get_packets_from_file('examples/live_capture.txt'):
        #Update GUI
        if 'Cell ID' in packet:
            row = app.cell_data[packet['Cell ID']]
            row[1].set(packet['Instant Voltage'])
            row[2].set(packet['Internal Resistence'])
            row[3].set(packet['Open Voltage'])
        app.update_idletasks()
        app.update()
        sleep(0.2)
