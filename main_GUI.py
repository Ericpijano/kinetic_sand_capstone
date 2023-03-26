import tkinter as tk

# Create a new window
window = tk.Tk()
window.title("My App")
window.configure(bg='#222')

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set window size and position
window.geometry("%dx%d+0+0" % (screen_width, screen_height))

# Create a label
label = tk.Label(window, text="", font=("Helvetica", 20), fg="white", bg='#222')
label.pack(pady=20)

# Define the button callback functions
def button1_clicked():
    print("Button 1 clicked")

def button2_clicked():
    print("Button 2 clicked")

def button3_clicked():
    print("Button 3 clicked")

# Create the buttons
button1 = tk.Button(window, text="Button 1", font=("Helvetica", 16), bg='#115', fg='white', command=button1_clicked)
button2 = tk.Button(window, text="Button 2", font=("Helvetica", 16), bg='#115', fg='white', command=button2_clicked)
button3 = tk.Button(window, text="Button 3", font=("Helvetica", 16), bg='#115', fg='white', command=button3_clicked)

# Position the buttons
button1.pack(side=tk.LEFT, padx=20)
button2.pack(side=tk.LEFT, padx=20)
button3.pack(side=tk.LEFT, padx=20)

# Center the buttons in the window
window.update_idletasks()
x = (window.winfo_width() - button1.winfo_reqwidth() - button2.winfo_reqwidth() - button3.winfo_reqwidth() - 60) / 2
button1.place(relx=0, x=x, y=100)
button2.place(relx=0, x=x+button1.winfo_reqwidth()+20, y=100)
button3.place(relx=0, x=x+button1.winfo_reqwidth()+button2.winfo_reqwidth()+40, y=100)

# Start the main event loop
window.mainloop()
