import tkinter as tk
import tkinter.ttk as ttk

"""Work in Progress!"""

class Application(tk.Frame):
    def __init__(self):
        super().__init__(tk.Tk())
        self._root().title('NUSolar Telemetry')
        self._root().configure()
        self.cell_data = []
        #Widgets
        cell_table = ttk.LabelFrame(self, text='Test', labelanchor='n')
        cell_table_labels = []
        cell_table_labels.append(tk.Label(cell_table, text='ID'))
        cell_table_labels.append(tk.Label(cell_table, text='Instant Voltage'))
        cell_table_labels.append(tk.Label(cell_table, text='Internal Resistance'))
        cell_table_labels.append(tk.Label(cell_table, text='Open Voltage'))
        #Packing
        cell_table.pack(fill='both', expand='yes', padx=10, pady=10)
        for i in range(0, len(cell_table_labels)):
            cell_table_labels[i].grid(row=0, column=i)
        self.pack()
        self.mainloop()

if __name__ == "__main__":
    app = Application()
