import serial
import time

com_port = 'COM7'
baud_rate = 9600
ser = serial.Serial(com_port, baud_rate)

i = 0
print('TEST')
x = 'k'+'\n'
ser.write(x.encode())
time.sleep(2)
while(i<100):
    print('TEST1')
    i = i + 1
    data = ser.readline()
    print(i)
    print(data)
    time.sleep(0.01)
    
ser.close()