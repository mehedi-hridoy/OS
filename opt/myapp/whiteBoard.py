import tkinter as tk
from tkinter.colorchooser import askcolor

# Variables to manage the current drawing state
current_tool = "pencil"
current_color = "black"
tool_size = 5
previous_point = None

# Draw function for smooth drawing
def draw(event, canvas):
    global previous_point
    if previous_point is not None:
        if current_tool in ["pencil", "brush"]:
            canvas.create_line(
                previous_point[0], previous_point[1], event.x, event.y,
                width=tool_size, fill=current_color, capstyle="round", smooth=True
            )
        elif current_tool == "eraser":
            # Erase only the drawn content, not the background
            erase(event, canvas)
    previous_point = (event.x, event.y)

# Erase function: only erase the color of the drawn content
def erase(event, canvas):
    overlapping_items = canvas.find_overlapping(event.x - tool_size, event.y - tool_size,
                                                event.x + tool_size, event.y + tool_size)
    for item in overlapping_items:
        item_color = canvas.itemcget(item, "fill")
        if item_color == current_color:
            canvas.delete(item)

# Reset the previous point on mouse release
def reset_previous_point(event):
    global previous_point
    previous_point = None

# Function to pick a drawing color
def choose_color():
    global current_color
    color = askcolor()[1]
    if color:
        current_color = color

# Function to change the canvas background color
def change_background(canvas):
    color = askcolor()[1]
    if color:
        canvas.config(bg=color)

# Tool selection functions
def use_pencil():
    global current_tool
    current_tool = "pencil"

def use_brush():
    global current_tool
    current_tool = "brush"

def use_eraser():
    global current_tool
    current_tool = "eraser"

# Clear the canvas
def clear_canvas(canvas):
    canvas.delete("all")

# Create a new canvas window with its own toolbar
def open_new_canvas():
    new_window = tk.Toplevel(root)
    new_window.title("New Whiteboard")

    # Canvas for the new window
    new_canvas = tk.Canvas(new_window, bg="white")
    new_canvas.pack(side="right", fill="both", expand=True)

    # Toolbar for the new window
    toolbar = tk.Frame(new_window, bg="gray", width=50)
    toolbar.pack(side="left", fill="y", padx=5, pady=5)

    # Add buttons to the new toolbar
    pencil_button = tk.Button(toolbar, text="Pencil", command=use_pencil, bg="gray", fg="white", bd=0)
    pencil_button.pack(pady=5)

    brush_button = tk.Button(toolbar, text="Brush", command=use_brush, bg="gray", fg="white", bd=0)
    brush_button.pack(pady=5)

    eraser_button = tk.Button(toolbar, text="Eraser", command=use_eraser, bg="gray", fg="white", bd=0)
    eraser_button.pack(pady=5)

    color_button = tk.Button(toolbar, text="Color", command=choose_color, bg="gray", fg="white", bd=0)
    color_button.pack(pady=5)

    background_button = tk.Button(toolbar, text="Background", command=lambda: change_background(new_canvas), bg="gray", fg="white", bd=0)
    background_button.pack(pady=5)

    clear_button = tk.Button(toolbar, text="Clear", command=lambda: clear_canvas(new_canvas), bg="gray", fg="white", bd=0)
    clear_button.pack(pady=5)

    # Add a size slider to adjust tool size
    size_slider = tk.Scale(toolbar, from_=1, to=20, orient="horizontal", label="Size", bg="gray", fg="white", length=120)
    size_slider.pack(pady=5)

    # Update tool size dynamically from slider
    def update_tool_size():
        global tool_size
        tool_size = size_slider.get()
        new_window.after(50, update_tool_size)

    update_tool_size()

    # Bind mouse events to the new canvas
    new_canvas.bind("<B1-Motion>", lambda event: draw(event, new_canvas))
    new_canvas.bind("<ButtonRelease-1>", reset_previous_point)

# Create the main application window
root = tk.Tk()
root.title("Whiteboard")
root.geometry("900x600")
root.configure(bg="white")

# Main canvas for drawing
canvas = tk.Canvas(root, bg="white")
canvas.pack(side="right", fill="both", expand=True)

# Main toolbar on the left, centered vertically
toolbar = tk.Frame(root, bg="gray", width=50)
toolbar.pack(side="left", fill="y", padx=5, pady=5)

# Add buttons to the toolbar
pencil_button = tk.Button(toolbar, text="Pencil", command=use_pencil, bg="gray", fg="white", bd=0)
pencil_button.pack(pady=5)

brush_button = tk.Button(toolbar, text="Brush", command=use_brush, bg="gray", fg="white", bd=0)
brush_button.pack(pady=5)

eraser_button = tk.Button(toolbar, text="Eraser", command=use_eraser, bg="gray", fg="white", bd=0)
eraser_button.pack(pady=5)

color_button = tk.Button(toolbar, text="Color", command=choose_color, bg="gray", fg="white", bd=0)
color_button.pack(pady=5)

background_button = tk.Button(toolbar, text="Background", command=lambda: change_background(canvas), bg="gray", fg="white", bd=0)
background_button.pack(pady=5)

clear_button = tk.Button(toolbar, text="Clear", command=lambda: clear_canvas(canvas), bg="gray", fg="white", bd=0)
clear_button.pack(pady=5)

# Button to open a new whiteboard
new_canvas_button = tk.Button(toolbar, text="New", command=open_new_canvas, bg="gray", fg="white", bd=0)
new_canvas_button.pack(pady=5)

# Add a size slider to adjust tool size
size_slider = tk.Scale(toolbar, from_=1, to=20, orient="horizontal", label="Size", bg="gray", fg="white", length=120)
size_slider.pack(pady=5)

# Update tool size dynamically from slider
def update_tool_size():
    global tool_size
    tool_size = size_slider.get()
    root.after(50, update_tool_size)

update_tool_size()

# Bind mouse events to the main canvas
canvas.bind("<B1-Motion>", lambda event: draw(event, canvas))
canvas.bind("<ButtonRelease-1>", reset_previous_point)

# Run the Tkinter main loop
root.mainloop()

