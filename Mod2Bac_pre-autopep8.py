
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mod
from mod import *
from mod import ModScanner
from bac import BAC0_Converter as bacon
import test
import re
import threading
from time import sleep

# Main Application/GUI class

points = 0
point_values = {}
present_values = {}
av_list = []
mapped_list = []
connection_established = False
tk_terminate = False

class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Mod2Bac')
        # Width height
        master.geometry("1200x600")
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
        # Fix row width
        self.rowconfigure(2,weight=10)

    def create_dropdown_widgets(self):
        # Set up Input dropdown
        self.input = StringVar(self.master)
        self.input_list = ('','rtu','mstp')
        self.input_choices = sorted(self.input_list)
        self.input.set('rtu')
        # Input Selection
        self.input_text = tk.StringVar()
        self.input_label = tk.Label(self.master, text='Input Protocol', font=('bold', 14), pady=20)
        self.input_label.grid(row=0, column=0,sticky=tk.E)
        self.input_menu = tk.ttk.OptionMenu(self.master,self.input,*self.input_choices)
        self.input_menu.grid(row=0,column=1,sticky=tk.W)
        # Set up Comm Port dropdown
        self.comm_port = StringVar(self.master)
        self.comm_port_list = ('','COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7','COM8','/dev/ttyUSB0')
        self.comm_choices = sorted(self.comm_port_list)
        self.comm_port.set('/dev/ttyUSB0')
        # Comm Port
        self.comm_text = tk.StringVar()
        self.comm_label = tk.Label(self.master, text='COM Port', font=('bold', 14), pady=20)
        self.comm_label.grid(row=1, column=0, sticky=tk.E)
        self.comm_menu = tk.ttk.OptionMenu(self.master,self.comm_port,*self.comm_choices)
        self.comm_menu.grid(row=1,column=1,sticky=tk.W)
        # Set up Baud Rate dropdown
        self.baud_rate = IntVar(self.master)
        self.baud_rate_list = (0,1200, 4800, 9600, 19200, 38400, 76800, 115200)
        self.baud_choices = sorted(self.baud_rate_list)
        self.baud_rate.set(9600)
        # Baud Rate
        self.baud_text = tk.StringVar()
        self.baud_label = tk.Label(self.master, text='Baud Rate', font=('bold', 14), pady=20)
        self.baud_label.grid(row=0, column=2, sticky=tk.E)
        self.baud_menu = tk.ttk.OptionMenu(self.master,self.baud_rate,*self.baud_choices)
        self.baud_menu.grid(row=0,column=3,sticky=tk.W)
        # Set up Parity dropdown
        self.parity = StringVar(self.master)
        self.parity_list = ('','N','E','O')
        self.parity_choices = sorted(self.parity_list)
        self.parity.set('N')
        # Parity
        self.parity_text = tk.StringVar()
        self.parity_label = tk.Label(self.master, text='Parity', font=('bold', 14), pady=20,width=6,padx=0)
        self.parity_label.grid(row=0, column=4, sticky=tk.E)
        self.parity_menu = tk.ttk.OptionMenu(self.master,self.parity,*self.parity_choices)
        self.parity_menu.grid(row=0,column=5, sticky=tk.W)
        # Set up Bytesize dropdown
        self.bytesize = IntVar(self.master)
        self.bytesize_list = (0,8,16,32)
        self.bytesize_choices = sorted(self.bytesize_list)
        self.bytesize.set(8)
        # Bytesize
        self.bytesize_text = tk.StringVar()
        self.bytesize_label = tk.Label(self.master, text='Bytesize', font=('bold', 14), pady=20)
        self.bytesize_label.grid(row=0, column=6, sticky=tk.E)
        self.bytesize_menu = tk.ttk.OptionMenu(self.master,self.bytesize,*self.bytesize_choices)
        self.bytesize_menu.grid(row=0,column=7, sticky=tk.W)
        # Set up Output Interface dropdown
        self.iface = tk.StringVar()
        self.iface_list = test.ethernet_keys
        self.iface_choices = sorted(self.iface_list)
        self.iface.set(test.ethernet_keys[1])
        # Output Interface
        self.iface_text = tk.StringVar()
        self.iface_label = tk.Label(self.master, text='Bacnet Iface', font=('bold', 14), pady=20)
        self.iface_label.grid(row=3, column=4, sticky=tk.E)
        self.iface_menu = tk.ttk.OptionMenu(self.master,self.iface,*self.iface_choices)
        self.iface_menu.grid(row=3,column=5, sticky=tk.W)
        # Set up Databits dropdown
        self.databits = IntVar(self.master)
        self.databits_list = (0,1,2,3,4,5,6,7,8)
        self.databits_choices = sorted(self.databits_list)
        self.databits.set(8)
        # Databits
        self.databits_text = tk.StringVar()
        self.databits_label = tk.Label(self.master, text='Data bits', font=('bold', 14), pady=20)
        self.databits_label.grid(row=1, column=2, sticky=tk.E)
        self.databits_menu = tk.ttk.OptionMenu(self.master,self.databits,*self.databits_choices)
        self.databits_menu.grid(row=1,column=3, sticky=tk.W)
        # Set up Stopbits dropdown
        self.stopbits = IntVar(self.master)
        self.stopbits_list = (0,1,2,3,4,5,6,7,8)
        self.stopbits_choices = sorted(self.stopbits_list)
        self.stopbits.set(1)
        # Stopbits
        self.stopbits_text = tk.StringVar()
        self.stopbits_label = tk.Label(self.master, text='Stop bits', font=('bold', 14), pady=20)
        self.stopbits_label.grid(row=1, column=4, sticky=tk.E)
        self.stopbits_menu = tk.ttk.OptionMenu(self.master,self.stopbits,*self.stopbits_choices)
        self.stopbits_menu.grid(row=1,column=5, sticky=tk.W)

    def create_entry_widgets(self):
        # Device ID
        self.device_text = tk.IntVar(self.master)
        self.device_label = tk.Label(self.master, text='Device ID', font=('bold', 14), pady=20, padx=4, width=8)
        self.device_label.grid(row=2, column=0,sticky=tk.E)
        self.device_entry = tk.Entry(self.master, textvariable=self.device_text)
        self.device_entry.insert(END,1)
        self.device_entry.grid(row=2, column=1,sticky=tk.W)
        # Starting Register
        self.start_text = tk.IntVar(self.master)
        self.start_label = tk.Label(self.master, text='Starting', font=('bold', 14), pady=20, padx=4, width=8)
        self.start_label.grid(row=2, column=2,sticky=tk.E)
        self.start_entry = tk.Entry(self.master, textvariable=self.start_text)
        self.start_entry.insert(END,0)
        self.start_entry.grid(row=2, column=3,sticky=tk.W)
        # Amount of registers
        self.amount_text = tk.IntVar(self.master)
        self.amount_label = tk.Label(self.master, text='Amount', font=('bold', 14), pady=20, padx=4, width=8)
        self.amount_label.grid(row=2, column=4,sticky=tk.E)
        self.amount_entry = tk.Entry(self.master, textvariable=self.amount_text)
        # self.amount_entry.insert(END,10)
        self.amount_entry.grid(row=2, column=5,sticky=tk.W)
        # Scan time
        self.time_text = tk.IntVar(self.master)
        self.time_label = tk.Label(self.master, text='Scantime(s)', font=('bold', 14), pady=20, padx=4, width=12)
        self.time_label.grid(row=2, column=6,sticky=tk.E)
        self.time_entry = tk.Entry(self.master, textvariable=self.time_text)
        self.time_entry.insert(END,.1)
        self.time_entry.grid(row=2, column=7,sticky=tk.W)
        # Output Instance
        self.instance_text = tk.StringVar()
        self.instance_label = tk.Label(self.master, text='Instance', font=('bold', 14), pady=20, padx=4, width=7)
        self.instance_label.grid(row=3, column=6, sticky=tk.E)
        self.instance_entry = tk.Entry(self.master, textvariable=self.instance_text)
        self.instance_entry.insert(END,"7200")
        self.instance_entry.grid(row=3, column=7,sticky=tk.W)

    def create_button_widgets(self):
        # Scan Button
        self.scan_button = tk.ttk.Button(self.master,text='Scan',width=6,command=self.scan)
        self.scan_button.grid(row=4,column=3,pady=30)
        # Map Analog Value Button
        self.map_analog_button = tk.ttk.Button(self.master,text='Map to Analog',width=12,command=self.map_analog)
        self.map_analog_button.grid(row=5,column=3,pady=25)
        # Map Binary Value Button
        self.map_binary_button = tk.ttk.Button(self.master,text='Map to Binary',width=12,command=self.map_binary)
        self.map_binary_button.grid(row=6,column=3,pady=25)

    def create_listbox_widgets(self):
        # Create listbox for input registers/points
        self.input_point_list = tk.Listbox(self.master, selectmode=MULTIPLE, exportselection=1, height=15, width=25, border=1)
        self.input_point_list.grid(row=4, column=0, columnspan=2,rowspan=5, pady=20,sticky=tk.E)

        # Create scrollbar for input listbox
        self.input_scrollbar = tk.Scrollbar(self.master)
        self.input_scrollbar.grid(row=4, column=2, rowspan=5,pady=20,sticky=N+S+W)

        # Attach scrollbar to input listbox
        self.input_point_list.config(yscrollcommand=self.input_scrollbar.set)
        self.input_scrollbar.config(command=self.input_point_list.yview)

        # Create listbox for output points
        self.output_point_list = tk.Listbox(self.master, selectmode=MULTIPLE, exportselection=1,height=15, width=25, border=1)
        self.output_point_list.grid(row=4, column=5, columnspan=2,rowspan=5, pady=20,sticky=tk.E)

        # Create scrollbar for output listbox
        self.output_scrollbar = tk.Scrollbar(self.master)
        self.output_scrollbar.grid(row=4, column=7, rowspan=5,pady=20,sticky=N+S+W)

        # Attach scrollbar to output listbox
        self.output_point_list.config(yscrollcommand=self.output_scrollbar.set)
        self.output_scrollbar.config(command=self.output_point_list.yview)


    def scan(self):
        global points
        global point_values
        global connection_established
        self.start = self.start_text.get()
        self.amount = self.amount_text.get()
        self.scan_time = self.time_text.get()
        self.device = self.device_text.get()
        if self.register.get() == 'Coil Status 0x':
            self.mode = 1
        elif self.register.get() == 'Input Status 1x':
            self.mode = 2
        elif self.register.get() == 'Input Register 3x':
            self.mode = 3
        elif self.register.get() == 'Holding Register 4x':
            self.mode = 4
        # Set up Bacnet connection
        print(test.ethernet_address[self.iface.get()])
        self.kevin = bacon(str(test.ethernet_address[self.iface.get()]),self.instance_text.get(),'Raspberry Pi3')
        attempt_connection = True
        initial_port = 47809
        while attempt_connection == True:
            try:
                self.kevin.start_device(initial_port)
                attempt_connection = False
            except:
                initial_port += 1
                sleep(1)
            
        if self.input.get() != self.protocol:
            self.input_point_list.delete(0,tk.END)
            points = 0
        self.protocol = self.input.get()
        # Create a new Modbus Scanner using pymodbus
        self.scanner = ModScanner(
            self.register.get(),
            self.input.get(),
            self.comm_port.get(),
            self.baud_rate.get(),
            self.stopbits.get(),
            self.databits.get(),
            self.parity.get(),
            1
            )
        # Connect to the desired device
        self.connection = self.scanner.connect()
        if self.connection:
            print("Establishing connection...")
            connection_established = True
        sleep(1)
        self.device_list = self.device_entry.get().split(',')
        for device in self.device_list:
            print(f"device is {device}")
            self.scanner.scan(self.start,self.amount,self.mode,self.device)
            self.total_point_list = mod.point_list
            print(f"point list is {self.total_point_list}")
            for point in range(self.amount):
                self.input_point_list.insert(END,"device{} point{}".format(device,point))
                try:
                    point_values[str(point)]=self.total_point_list[point]
                except IndexError:
                    print("No Device connected")
                    pass
        threading.Thread(target=self.scan_threader).start()
        
    def scan_threader(self):
        global connection_established
        global av_list
        global present_values
        global point_values
        global tk_terminate
        while connection_established == True and tk_terminate == False:
            self.total_point_list = mod.point_list
            for point in range(self.amount):
                try:
                    point_values[str(point)]=self.total_point_list[point]
                except IndexError:
                    print("No Device connected")
                    pass
            t = threading.Thread(target=self.scanner.scan,args=(self.start,self.amount,self.mode,self.device))
            t.start()
            t.join()
            for i in av_list:
                present_values[str(i)]=point_values[str(i)]
                self.kevin.update_analogs(f"register{i}",present_values[str(i)])
            sleep(self.scan_time)
            if tk_terminate:
                connection_established = False
                break
                
    def map_analog(self):
        global point_values
        global mapped_list
        global av_list
        self.analog_point_list = self.input_point_list.curselection()
        device_name = ""
        point = ""
        print(point_values)
        for k in point_values.keys():
            mapped_list.append(k)
        for i in self.analog_point_list:
            #self.output_point_list.insert(END,"Mapping point{} to AV_{}".format(point_values[str(i)],self.av))
            self.output_point_list.insert(END,"Mapping point{} to AV_{}".format(mapped_list[i],self.av))
            av_list.append(mapped_list[i])
            device_name = "{}".format(self.total_point_list[i])
            point = "register{}".format(mapped_list[i])
            self.av += 1
            print(point)
            self.kevin.build_analog(device_name,point)

    def map_binary(self):
        pass

    def select(self):
        pass

    def change_input_dropdown(self,*args):
        self.input.get()
        self.protocol = self.input.get()
        if self.protocol == 'rtu':
            # Set up Register dropdown
            self.register = tk.StringVar()
            self.register_list = ('','Coil Status 0x', 'Input Status 1x', 'Input Register 3x', 'Holding Register 4x')
            self.register_choices = sorted(self.register_list)
            self.register.set('Holding Register 4x')
            # Register dropdown
            self.register_text = tk.StringVar()
            self.register_label = tk.Label(self.master, text='Input Scan', font=('bold', 14), pady=20)
            self.register_label.grid(row=1, column=6, sticky=tk.E)
            self.register_menu = tk.ttk.OptionMenu(self.master,self.register,*self.register_choices)
            self.register_menu.grid(row=1,column=7, sticky=tk.W)
            

    def change_comm_dropdown(self,*args):
        self.comm_port.get()

    def change_baud_dropdown(self,*args):
        self.baud_rate.get()

# Handle window closure by terminating all threads
def _delete_window():
    global tk_terminate
    print("deleting frame")
    tk_terminate = True
    root.destroy()
    
def _destroy():
    print("destroy")
    
root = tk.Tk()
app = Application(master=root)
# bind function for thread termination to Frame closure
root.protocol("WM_DELETE_WINDOW",_delete_window)
root.bind("<Escape>",_destroy)
app.mainloop()