import serial

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
print(ser.name)

try:
    while True:
        bytes = ser.readline()
        print("{0} ", bytes)
except KeyboardInterrupt:
    ser.close()



