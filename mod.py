class ModScanner:
	def __init__(self,protocol_input,comm_port,baudrate):
		self.input = protocol_input
		self.comm_port = comm_port
		self.stop_bits = 1
		self.bytesize = 8
		self.parity = 'N'
		self.baudrate = baudrate

	def __repr__(self):
		return "Connecting via comm_port {} at a baudrate of {}".format(self.comm_port,self.baudrate)