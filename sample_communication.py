serialInst = serial.Serial()

serialInst.baudrate = 9600
serialInst.port = COM7
serialInst.open()

while True:
    command = input("Arduino Command: (ON/OFF): ")
    serialInst.write(command.encode('utf-8'))

    if command == 'exit':
        exit()