import serial
import time
from threading import Event

BAUD_RATE = 115200

def remove_comment(string):
    if (string.find(';') == -1):
        return string
    else:
        return string[:string.index(';')]


def remove_eol_chars(string):
    # removed \n or traling spaces
    return string.strip()


def send_wake_up(ser):
    # Wake up
    # Hit enter a few times to wake the Printrbot
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)   # Wait for Printrbot to initialize
    ser.flushInput()  # Flush startup text in serial input


def wait_for_movement_completion(ser, cleaned_line):
    Event().wait(1)
    if cleaned_line != '$X' or '$$':
        idle_counter = 10 # to skip count up 10 to
        while True:
            # Event().wait(0.01)
            ser.reset_input_buffer()
            command = str.encode('?' + '\n')
            ser.write(command)
            grbl_out = ser.readline() 
            grbl_response = grbl_out.strip().decode('utf-8')
            if grbl_response != 'ok':
                break # skip idler 
                if grbl_response.find('Idle') > 0:
                    idle_counter += 1
            if idle_counter > 10:
                break


def stream_gcode(GRBL_port_path,gcode_path):
    with open(gcode_path, "r") as file, serial.Serial(GRBL_port_path, BAUD_RATE) as ser:
        send_wake_up(ser)
        first_line = True  # flag to check if it is the first line
        for line in file:
            # cleaning up gcode from file
            cleaned_line = remove_eol_chars(remove_comment(line))
            if cleaned_line:  # checks if string is empty
                print("Sending gcode:" + str(cleaned_line))
                if first_line:
                    command = str.encode(cleaned_line.strip() + '\n')
                    first_line = False
                else:
                    # converts string to byte encoded string and append newline
                    command = str.encode(cleaned_line.strip() + ' F5000\n')
                ser.write(command)  # Send g-code

                wait_for_movement_completion(ser, cleaned_line)

                grbl_out = ser.readline()  # Wait for response with carriage return
                print(" : " , grbl_out.strip().decode('utf-8'))

        print('End of gcode')


if __name__ == "__main__":
    # GRBL_port_path = '/dev/tty.usbserial-A906L14X'
    GRBL_port_path = '/dev/ttyACM0'
    gcode_path = 'grbl_test.gcode'

    print("USB Port: ", GRBL_port_path)
    print("Gcode file: ", gcode_path)
    stream_gcode(GRBL_port_path,gcode_path)

    print('EOF')
