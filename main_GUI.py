import tkinter as tk
import serial
import time
from threading import Event
from map import create_map_window
from Gcode_Streaming import stream_gcode

from tkinter import simpledialog

# Import colorchooser for the color picker
from tkinter.colorchooser import askcolor

BAUD_RATE = 115200  # Update the BAUD_RATE to match sample_communication.py

def open_led_control_window():
    import LED_control
    LED_control.open_window(window)
    window.withdraw()

def send_wake_up(ser):
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)
    ser.flushInput()

def send_home_sequence(ser):
    ser.write(str.encode("$h\n"))

def send_gcode(ser):
    ser.write(str.encode("G1 X25 Y20 f2000 \n"))

def open_pattern_window():
    pattern_window = tk.Toplevel(window)
    pattern_window.title("Pattern Selection")
    pattern_window.configure(bg='#222')

    screen_width = pattern_window.winfo_screenwidth()
    screen_height = pattern_window.winfo_screenheight()
    pattern_window.geometry("%dx%d+0+0" % (screen_width, screen_height))

    # Define button functions
    def sandify_button():
        stream_gcode('COM5', 'sandify.gcode')

    def square_button():
        stream_gcode('COM5', 'square.gcode')

    def star_button():
        stream_gcode('COM5', 'star.gcode')

    def tessellation_twist_button():
        stream_gcode('COM5', 'tessellation_twist.gcode')

    def exit_button():
        pattern_window.destroy()

    # Create buttons
    sandify = tk.Button(pattern_window, text="Sandify", font=("Helvetica", 16), bg='#115', fg='white', command=sandify_button)
    square = tk.Button(pattern_window, text="Square", font=("Helvetica", 16), bg='#115', fg='white', command=square_button)
    star = tk.Button(pattern_window, text="Star", font=("Helvetica", 16), bg='#115', fg='white', command=star_button)
    tessellation_twist = tk.Button(pattern_window, text="Tessellation Twist", font=("Helvetica", 16), bg='#115', fg='white', command=tessellation_twist_button)
    exit_button = tk.Button(pattern_window, text="Exit", font=("Helvetica", 16), bg='#115', fg='white', command=exit_button)

    # Position the buttons
    num_rows = 4
    num_columns = 5

    start_row = (num_rows - 1) // 2
    start_col = (num_columns - 5) // 2

    sandify.grid(in_=pattern_window, row=start_row, column=start_col, padx=10, pady=10, sticky="nsew")
    square.grid(in_=pattern_window, row=start_row, column=start_col + 1, padx=10, pady=10, sticky="nsew")
    star.grid(in_=pattern_window, row=start_row, column=start_col + 2, padx=10, pady=10, sticky="nsew")
    tessellation_twist.grid(in_=pattern_window, row=start_row, column=start_col + 3, padx=10, pady=10, sticky="nsew")
    exit_button.grid(in_=pattern_window, row=start_row + 1, column=start_col + 2, padx=10, pady=10, sticky="nsew")

    for i in range(num_rows):
        pattern_window.rowconfigure(i, weight=1)

    # Increase the weight of the first row to push the buttons slightly upwards
    pattern_window.rowconfigure(0, weight=2)

    for i in range(num_columns):
        pattern_window.columnconfigure(i, weight=1)


window = tk.Tk()
window.title("Kinetic Sand art")
window.configure(bg='#222')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.geometry("%dx%d+0+0" % (screen_width, screen_height))
window.attributes('-fullscreen', True)  # Add this line to open the window in fullscreen

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

content = tk.Frame(window, bg='#222')
content.grid(row=0, column=0, sticky="nsew")

label = tk.Label(window, text="", font=("Helvetica", 20), fg="white", bg='#222')
label.grid(in_=content, row=0, column=0, columnspan=5, pady=20)

def button1_clicked():
    label.configure(text="homing process")
    with serial.Serial('COM5', BAUD_RATE) as ser:
        send_wake_up(ser)
        send_home_sequence(ser)

def button2_clicked():
    open_pattern_window()

def button3_clicked():
    label.configure(text="Button 3 clicked")

def open_map_window():
    map_window = create_map_window(window)
    map_window.attributes('-fullscreen', True)
    window.withdraw()

def exit_main_window():
    window.destroy()


button_map = tk.Button(window, text="Map", font=("Helvetica", 16), bg='#115', fg='white', command=open_map_window)
button1 = tk.Button(window, text="Homing sequence", font=("Helvetica", 16), bg='#115', fg='white', command=button1_clicked)
button2 = tk.Button(window, text="Run Pattern", font=("Helvetica", 16), bg='#115', fg='white', command=button2_clicked)
button3 = tk.Button(window, text="Controller", font=("Helvetica", 16), bg='#115', fg='white', command=button3_clicked)
button4 = tk.Button(window, text="LED Control", font=("Helvetica", 16), bg='#115', fg='white', command=open_led_control_window)

num_rows = 4
num_columns = 5

start_row = (num_rows - 1) // 2
start_col = (num_columns - 5) // 2

exit_main = tk.Button(window, text="Exit", font=("Helvetica", 16), bg='#115', fg='white', command=exit_main_window)
exit_main.grid(in_=content, row=2, column=0, columnspan=5, pady=20)


button_map.grid(in_=content, row=start_row, column=start_col, padx=10, pady=10, sticky="nsew")
button1.grid(in_=content, row=start_row, column=start_col + 1, padx=10, pady=10, sticky="nsew")
button2.grid(in_=content, row=start_row, column=start_col + 2, padx=10, pady=10, sticky="nsew")
button3.grid(in_=content, row=start_row, column=start_col + 3, padx=10, pady=10, sticky="nsew")
button4.grid(in_=content, row=start_row, column=start_col + 4, padx=10, pady=10, sticky="nsew")

for i in range(num_rows):
    content.rowconfigure(i, weight=1)

for i in range(num_columns):
    content.columnconfigure(i, weight=1)
    
#content.columnconfigure(0, weight=1)
#content.columnconfigure(1, weight=1)
#content.columnconfigure(2, weight=1)
#content.columnconfigure(3, weight=1)
#content.columnconfigure(4, weight=1)

window.mainloop()
