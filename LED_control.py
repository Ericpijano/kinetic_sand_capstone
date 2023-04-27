import serial
import tkinter as tk
from tkinter.colorchooser import askcolor

def set_brightness(value):
    brightness = int(value)
    brightness_command = f"B{brightness}"
    serialInst.write(brightness_command.encode('utf-8'))

def set_color():
    color = askcolor()[0]
    if color:
        r, g, b = [int(c) for c in color]
        color_command = f"C{r},{g},{b}"
        serialInst.write(color_command.encode('utf-8'))

def set_pattern(pattern_number):
    pattern_command = f"P{pattern_number}"
    serialInst.write(pattern_command.encode('utf-8'))
    
def close_app():
    window.quit()

def main_menu_button():
    window.destroy()
    window.deiconify()

serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = "COM12"  # Replace "COM7" with the correct port for your Arduino
serialInst.open()

def open_window(main_window):
    global window
    window = tk.Toplevel(main_window)
    window.title("LED Control")
    window.configure(bg='#222')

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry("%dx%d+0+0" % (screen_width, screen_height))
    window.attributes('-fullscreen', True)  # Add this line to open the window in fullscreen

    brightness_label = tk.Label(window, text="Brightness", font=("Helvetica", 16), fg="white", bg='#222')
    brightness_scale = tk.Scale(window, from_=0, to=255, orient=tk.HORIZONTAL, command=set_brightness, bg='#115', fg='white')
    color_button = tk.Button(window, text="Select Color", font=("Helvetica", 16), bg='#115', fg='white', command=set_color)
    pattern_button1 = tk.Button(window, text="Pattern 1 (Solid Color)", font=("Helvetica", 16), bg='#115', fg='white', command=lambda: set_pattern(1))
    pattern_button2 = tk.Button(window, text="Pattern 2 (Color Cycle)", font=("Helvetica", 16), bg='#115', fg='white', command=lambda: set_pattern(2))
    pattern_button3 = tk.Button(window, text="Pattern 3 (Twinkle)", font=("Helvetica", 16), bg='#115', fg='white', command=lambda: set_pattern(3))
    #exit_button = tk.Button(window, text="Exit", font=("Helvetica", 16), bg='#115', fg='white', command=close_app)
    main_menu = tk.Button(window, text="Main Menu", font=("Helvetica", 16), bg='#115', fg='white', command=main_menu_button)

    brightness_label.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
    brightness_scale.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
    color_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    pattern_button1.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
    pattern_button2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    pattern_button3.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
     #exit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    main_menu.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    
    window.mainloop()

