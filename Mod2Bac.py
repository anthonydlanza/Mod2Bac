
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from mod import ModScanner as ms
from bac import BAC0_Converter as bacon
import re

# Main Application/GUI class

points = 0

class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Mod2Bac')
        # Width height
        master.geometry("850x1000")
        # Analog Value Map Initializer
        self.av = 0
        # Binary Value Map Initializer
        self.bv = 0
        # Create widgets/grid
        self.create_dropdown_widgets()
        # Create entry widgets()
        self.create_entry_widgets()
        # Create button widgets()
        self.create_button_widgets()
        # Create listbox widgets()
        self.create_listbox_widgets()
        # Init selected item var
        self.selected_item = 0
        # Get Input Protocol dropdown selection
        self.change_input_dropdown()
        # Get Comm Port dropdown selection
        self.change_comm_dropdown()
        # Get Baud Rate dropdown selection
        self.change_baud_dropdown()
        # Set up Bacnet device
        self.kevin = bacon('192.168.1.149/24',7001,'MACBOOK')
        self.kevin.start_device()

    def create_dropdown_widgets(self):
        # Set up Input dropdown
        self.input = StringVar(self.master)
        self.input_list = ('','Modbus RTU', 'Bacnet IP', 'Bacnet MSTP')
        self.input_choices = sorted(self.input_list)
        self.input.set('Modbus RTU')
        # Input Selection
        self.input_text = tk.StringVar()
        self.input_label = tk.Label(self.master, text='Input Protocol', font=('bold', 14), pady=20, padx=0)
        self.input_label.grid(row=0, column=0,sticky=tk.E)
        self.input_menu = tk.ttk.OptionMenu(self.master,self.input,*self.input_choices)
        self.input_menu.grid(row=0,column=1)
        # Set up Comm Port dropdown
        self.comm_port = StringVar(self.master)
        self.comm_port_list = ('','COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6')
        self.comm_choices = sorted(self.comm_port_list)
        self.comm_port.set('COM1')
        # Comm Port
        self.comm_text = tk.StringVar()
        self.comm_label = tk.Label(self.master, text='COM Port', font=('bold', 14), pady=20)
        self.comm_label.grid(row=1, column=2, sticky=tk.W)
        self.comm_menu = tk.ttk.OptionMenu(self.master,self.comm_port,*self.comm_choices)
        self.comm_menu.grid(row=1,column=3)
        # Set up Baud Rate dropdown
        self.baud_rate = IntVar(self.master)
        self.baud_rate_list = (0,1200, 4800, 9600, 19200, 38400, 76800, 115200)
        self.baud_choices = sorted(self.baud_rate_list)
        self.baud_rate.set(9600)
        # Baud Rate
        self.baud_text = tk.StringVar()
        self.baud_label = tk.Label(self.master, text='Baud Rate', font=('bold', 14), pady=20)
        self.baud_label.grid(row=1, column=4, sticky=tk.W)
        self.baud_menu = tk.ttk.OptionMenu(self.master,self.baud_rate,*self.baud_choices)
        self.baud_menu.grid(row=1,column=5)

    def create_entry_widgets(self):
        # Device ID
        self.device_text = tk.StringVar()
        self.device_label = tk.Label(self.master, text='Device ID', font=('bold', 14), pady=20, padx=4, width=8)
        self.device_label.grid(row=1, column=0, sticky=tk.W)
        self.device_entry = tk.Entry(self.master, textvariable=self.device_text)
        self.device_entry.grid(row=1, column=1)

    def create_button_widgets(self):
        # Scan Button
        self.scan_button = tk.ttk.Button(self.master,text='Scan',width=6,command=self.scan)
        self.scan_button.grid(row=2,column=0)
        # Map Analog Value Button
        self.map_analog_button = tk.ttk.Button(self.master,text='Map to Analog',width=12,command=self.map_analog)
        self.map_analog_button.grid(row=7,column=3)
        # Map Binary Value Button
        self.map_binary_button = tk.ttk.Button(self.master,text='Map to Binary',width=12,command=self.map_binary)
        self.map_binary_button.grid(row=10,column=3)
        # Detach Bacnet Button
        self.detach_bac_button = tk.ttk.Button(self.master,text='Detach Bacnet',width=12,command=self.detach_bac)
        self.detach_bac_button.grid(row=13,column=3)

    def create_listbox_widgets(self):
        # Create listbox for input registers/points
        self.input_point_list = tk.Listbox(self.master, selectmode=MULTIPLE, exportselection=1, height=40, width=25, border=1)
        self.input_point_list.grid(row=3, column=0, columnspan=2,rowspan=44, pady=20, padx=20)

        # Create scrollbar for input listbox
        self.input_scrollbar = tk.Scrollbar(self.master)
        self.input_scrollbar.grid(row=3, column=2, rowspan=44,pady=20,sticky=N+S+W)

        # Attach scrollbar to input listbox
        self.input_point_list.config(yscrollcommand=self.input_scrollbar.set)
        self.input_scrollbar.config(command=self.input_point_list.yview)

        # Create listbox for output points
        self.output_point_list = tk.Listbox(self.master, selectmode=MULTIPLE, exportselection=1,height=40, width=40, border=1)
        self.output_point_list.grid(row=3, column=4, columnspan=2,rowspan=44, pady=20, padx=20)

        # Create scrollbar for output listbox
        self.output_scrollbar = tk.Scrollbar(self.master)
        self.output_scrollbar.grid(row=3, column=6, rowspan=44,pady=20,sticky=N+S+W)

        # Attach scrollbar to output listbox
        self.output_point_list.config(yscrollcommand=self.output_scrollbar.set)
        self.output_scrollbar.config(command=self.output_point_list.yview)


    def scan(self):
        global points
        if self.input.get() != self.protocol:
            self.input_point_list.delete(0,tk.END)
            points = 0
        self.protocol = self.input.get()
        scanner = ms(self.input.get(),self.comm_port.get(),self.baud_rate.get())
        print(scanner)
        self.device_list = self.device_entry.get().split(',')
        self.total_point_list = []
        for device in self.device_list:
            for point in range(points,points+10):
                self.input_point_list.insert(END,f"device{device} point{point}")
                self.total_point_list.append(f"device{device} point{point}")
        points += 10

    def map_analog(self):
        self.analog_point_list = self.input_point_list.curselection()
        device_name = ""
        point = ""
        for i in self.analog_point_list:
            self.output_point_list.insert(END,f"Mapping point{self.total_point_list[i]} to AV_{self.av}")
            device_name = f"{self.total_point_list[i]}"
            point = f"register{self.av}"
            self.av += 1
            self.kevin.build_analog(device_name,point)

    def map_binary(self):
        pass

    def detach_bac(self):
        self.kevin.disconnect()

    def select(self):
        pass

    def change_input_dropdown(self,*args):
        self.input.get()
        self.protocol = self.input.get()

    def change_comm_dropdown(self,*args):
        self.comm_port.get()

    def change_baud_dropdown(self,*args):
        self.baud_rate.get()

root = tk.Tk()
app = Application(master=root)
app.mainloop()