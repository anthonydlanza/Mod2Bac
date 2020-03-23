import BAC0
from BAC0.core.utils.notes import note_and_log

from bacpypes.local.object import (AnalogValueCmdObject,BinaryValueCmdObject)
from bacpypes.object import register_object_type
from bacpypes.basetypes import EngineeringUnits
from bacpypes.primitivedata import CharacterString

import time

objects = []

class BAC0_Converter():

    analog_value_num = 0
    analog_value_list = []
    binary_value_num = 0
    binary_value_list = []

    def __init__(self,ip,instance_number,obj_name):
        self.ip = ip
        self.instance_number = instance_number
        self.obj_name = obj_name

    def start_device(self,init_port):
        self.device = BAC0.lite(
            ip=self.ip,
            deviceId=self.instance_number,
            localObjName=self.obj_name,
            port=init_port
            )

    def build_analog(self,input_device,input_dev_point):
        global objects
        self.input_device = input_device
        self.input_dev_point = input_dev_point
        register_object_type(AnalogValueCmdObject, vendor_id=842)
        av_object = AnalogValueCmdObject(
            objectIdentifier=("analogValue",BAC0_Converter.analog_value_num),
            objectName=self.input_dev_point,
            presentValue=666,
            description=CharacterString(f"imported from {self.input_device}: {self.input_dev_point} "))
        BAC0_Converter.analog_value_num += 1
        BAC0_Converter.analog_value_list.append(av_object)
        self.device.this_application.add_object(av_object)
        return av_object
    
    def update_analogs(self,name,value):
        global objects
        av = self.device.this_application.get_object_name(name)
        if av:
            av.presentValue = value
            print(f"AV present Value: {av.presentValue}")
            

    def build_binary(self,input_device,input_dev_point):
        self.input_device = input_device
        self.input_dev_point = input_dev_point
        register_object_type(BinaryValueCmdObject, vendor_id=842)
        bv_object = BinaryValueCmdObject(
            objectIdentifier=("binaryValue",BAC0_Converter.binary_value_num),
            objectName=self.input_dev_point,
            presentValue='inactive',
            description=CharacterString(f"imported from {self.input_device}: {self.input_dev_point} "))
        BAC0_Converter.binary_value_num += 1
        BAC0_Converter.binary_value_list.append(bv_object)
        self.device.this_application.add_object(bv_object)
        return bv_object

def start():
    Toast = BAC0_Converter('192.168.1.151/24',7002,'Pi')
    Toast.start_device()
    Toast.build_analog('modbus_dev_1','register_1')
    Toast.build_analog('modbus_dev_1','register_2')
    Toast.build_binary('modbus_dev_1','register_3')
    Toast.build_binary('modbus_dev_1','register_4')
    for i in Toast.analog_value_list:
        print(i)
    for i in Toast.binary_value_list:
        print(i)
    while True:
        time.sleep(10)

if __name__=='__main__':
    start()











