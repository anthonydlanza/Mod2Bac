from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import *
from time import sleep
import threading

point_list = []

class ModScanner:
    def __init__(self,function=4,protocol_input='rtu',comm_port='/dev/ttyUSB0',baudrate=9600,stop_bits=1,bytesize=8,parity='N',timeout=1):
        self.protocol_input = protocol_input
        self.comm_port = comm_port
        self.baud_rate = baudrate
        self.stop_bits = stop_bits
        self.bytesize = bytesize
        self.parity = parity
        self.function = function
        self.timeout = timeout

    def __repr__(self):
        return "Connecting via comm_port {} at a baudrate of {}".format(self.comm_port,self.baudrate)
    
    def connect(self):
        print(self.protocol_input)
        self.client = ModbusClient(
            method=self.protocol_input,
            port=self.comm_port,
            stopbits=self.stop_bits,
            bytesize=self.bytesize,
            parity=self.parity,
            baudrate=self.baud_rate,
            timeout=self.timeout
            )
        self.connection = self.client.connect()
        return self.connection
    
    def scan(self,start,amount,mode,device):
        global point_list
        if mode == 1:
            try:
                value = self.client.read_coil_status(start,amount,unit=device)
                print(value.status)
                point_list = value.status
            except AttributeError:
                print("device is down")
        elif mode == 2:
            try:
                value = self.client.read_input_status(start,amount,unit=device)
                print(value.status)
                point_list = value.status
            except AttributeError:
                print("device is down")
        elif mode == 3:
            try:
                value = self.client.read_input_registers(start,amount,unit=device)
                print(value.registers)
                point_list = value.registers
            except AttributeError:
                print("device is down")
        elif mode == 4:
            try:
                value = self.client.read_holding_registers(start,amount,unit=device)
                point_list = value.registers
                print(point_list)
            except AttributeError:
                print("device is down")