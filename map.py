import tkinter as tk

# Conversion functions
def pixel_to_gcode_x(x):
    return x / (canvas_width / x_units)

def pixel_to_gcode_y(y):
    return y / (canvas_height / y_units)

def draw_mark(x, y):
    canvas.create_oval(x-2, y-2, x+2, y+2, fill='black', outline='')

def generate_gcode(x, y):
    gcode_x = pixel_to_gcode_x(x)
    gcode_y = pixel_to_gcode_y(y)
    print(f'G1 X{gcode_x:.2f} Y{gcode_y:.2f}')
    result_label.config(text=f'G-Code Position: X{gcode_x:.2f} Y{gcode_y:.2f}')

def on_canvas_press(event):
    global drawing
    drawing = True
    generate_gcode(event.x, event.y)

def on_canvas_release(event):
    global drawing
    drawing = False

def on_canvas_motion(event):
    if drawing:
        draw_mark(event.x, event.y)
        generate_gcode(event.x, event.y)

def erase_drawing():
    canvas.delete('all')
    result_label.config(text='G-Code Position: X- Y-')

# Grid dimensions and units
canvas_width, canvas_height = 600, 400
x_units, y_units = 60, 40

# Create main window and canvas
root = tk.Tk()
root.title('G-Code Map')

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='#FFB533')
canvas.pack(pady=10)

# Create a label to display the result
result_label = tk.Label(root, text='G-Code Position: X- Y-', font=('Arial', 12))
result_label.pack(pady=5)

# Create an erase button
erase_button = tk.Button(root, text='Erase', command=erase_drawing)
erase_button.pack(pady=5)

# Bind events
drawing = False
canvas.bind('<ButtonPress-1>', on_canvas_press)
canvas.bind('<ButtonRelease-1>', on_canvas_release)
canvas.bind('<B1-Motion>', on_canvas_motion)

# Run the main loop
root.mainloop()
