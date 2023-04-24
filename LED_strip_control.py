import serial

serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = "COM7" # Replace "COM7" with the correct port for your Arduino
serialInst.open()

while True:
    brightness = input("Enter brightness level (0-255): ")

    if brightness == "exit":
        break

    brightness_command = f"B{brightness}"
    serialInst.write(brightness_command.encode('utf-8'))

serialInst.close()
