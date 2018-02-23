import serial

ser = serial.Serial('/dev/serial0')
ser.parity =serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 1

counter=0
while 1:
	x=ser.readline()
	print x