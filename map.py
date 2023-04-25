import tkinter as tk
import serial
import time
from threading import Event

# Add the required functions from Gcode_Streaming.py
BAUD_RATE = 115200

def remove_comment(string):
    if (string.find(';') == -1):
        return string
    else:
        return string[:string.index(';')]

def remove_eol_chars(string):
    return string.strip()

def send_wake_up(ser):
    ser.write(str.encode("\r\n\r\n"))
    time.sleep(2)
    ser.flushInput()

def wait_for_movement_completion(ser, cleaned_line):
    Event().wait(1)
    if cleaned_line != '$X' or '$$':
        idle_counter = 10
        while True:
            ser.reset_input_buffer()
            command = str.encode('?' + '\n')
            ser.write(command)
            grbl_out = ser.readline()
            grbl_response = grbl_out.strip().decode('utf-8')
            if grbl_response != 'ok':
                break
            if grbl_response.find('Idle') > 0:
                idle_counter += 1
            if idle_counter > 10:
                break

# Modify the existing functions
def pixel_to_gcode_x(x):
    return x / (canvas_width / x_units)

def pixel_to_gcode_y(y):
    return y / (canvas_height / y_units)

def draw_mark(canvas, x, y):
    canvas.create_oval(x-2, y-2, x+2, y+2, fill='black', outline='')

gcode_list = []

def generate_gcode(x, y, result_label):
    global gcode_list

    gcode_x = pixel_to_gcode_x(x)
    gcode_y = pixel_to_gcode_y(y)
    gcode_command = f'G1 X{gcode_x:.2f} Y{gcode_y:.2f}'
    print(gcode_command)
    result_label.config(text=f'G-Code Position: X{gcode_x:.2f} Y{gcode_y:.2f} f5000')

    # Append G-Code command to the list
    gcode_list.append(gcode_command)

def send_gcode_list():
    global gcode_list

    with serial.Serial('COM5', BAUD_RATE) as ser:
        send_wake_up(ser)

        for gcode_command in gcode_list:
            cleaned_line = remove_eol_chars(remove_comment(gcode_command))
            if cleaned_line:
                command = str.encode(cleaned_line.strip() + ' F5000\n')
                ser.write(command)
                wait_for_movement_completion(ser, cleaned_line)
                grbl_out = ser.readline()
                print(" : ", grbl_out.strip().decode('utf-8'))

    # Clear the G-Code list
    gcode_list = []

def on_canvas_press(event, result_label):
    global drawing
    global last_x, last_y

    drawing = True

    # Initialize the last_x and last_y variables when the user starts drawing
    last_x, last_y = event.x, event.y
    generate_gcode(event.x, event.y, result_label)

def on_canvas_release(event):
    global drawing
    drawing = False

def on_canvas_motion(event, result_label, canvas):
    global drawing

    if drawing:
        draw_mark(canvas, event.x, event.y)  # Pass canvas here
        generate_gcode(event.x, event.y, result_label)

def erase_drawing(canvas, result_label):
    canvas.delete('all')
    result_label.config(text='G-Code Position: X- Y-')


# Grid dimensions and units
canvas_width, canvas_height = 600, 400
x_units, y_units = 60, 40

# New function to create the map window
def create_map_window(parent_window):
    root = tk.Toplevel(parent_window)
    root.title('G-Code Map')

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='#FFB533')
    canvas.pack(pady=10)

    result_label = tk.Label(root, text='G-Code Position: X- Y-', font=('Arial', 12))
    result_label.pack(pady=5)

    erase_button = tk.Button(root, text='Erase', command=lambda: erase_drawing(canvas, result_label))
    erase_button.pack(pady=5)

    # Add the Close button
    close_button = tk.Button(root, text='Close', command=lambda: close_map_window(root, parent_window))
    close_button.pack(pady=5)

    send_gcode_button = tk.Button(root, text='Send G-Code', command=send_gcode_list)
    send_gcode_button.pack(pady=5)

    # Bind events
    drawing = False
    # Update the event bindings to use lambdas to include result_label and canvas
    canvas.bind('<ButtonPress-1>', lambda event: on_canvas_press(event, result_label))
    canvas.bind('<ButtonRelease-1>', on_canvas_release)
    # Pass the canvas variable as well
    canvas.bind('<B1-Motion>', lambda event: on_canvas_motion(event, result_label, canvas))
    # Open the serial connection
 

    return root

# New function to close the map window and return to the main_GUI

def close_map_window(window, parent_window):
    window.destroy()
    parent_window.deiconify()



# Replace the last lines with these lines to run the map window standalone or as a module
if __name__ == '__main__':
    standalone_window = tk.Tk()
    standalone_window.withdraw()
    window = create_map_window(standalone_window)
    window.protocol("WM_DELETE_WINDOW", lambda: close_map_window(window, standalone_window))
    window.mainloop()