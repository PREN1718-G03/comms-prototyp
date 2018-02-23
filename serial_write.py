import time
import serial

# UART serial interface has changed
# https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3
ser = serial.Serial('/dev/serial0')
ser.parity =serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.bytesize = serial.EIGHTBITS
ser.timeout = 1

counter=0

while 1:
	ser.write('Count %d time(s)\n'%(counter))
	time.sleep(1)
	counter += 1