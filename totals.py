import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
import csv
import subprocess

# Global variables
points = []
edit_mode = False
default_font_size = 8
slider = None  # Initialize slider as None globally

# Function to handle click event on the graph
def on_click(event):
    global points, edit_mode
    if edit_mode:
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            # Prompt for vendor info
            vendor_info = simpledialog.askstring("Input", "Enter vendor info:")
            if vendor_info:
                # Save point to points list
                points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
                update_scatter()  # Update scatter plot

# Function to update the scatter plot with points and text size
def update_scatter():
    global points, slider
    scatter.set_offsets([[p['x'], p['y']] for p in points])

    # Clear existing annotations
    for annotation in ax.texts:
        annotation.remove()

    # Ensure slider is defined before accessing it
    if slider:
        # Calculate font size based on slider value
        font_size = int(slider.get())
    else:
        font_size = default_font_size

    # Add new annotations with vendor totals
    for point in points:
        x = point['x']
        y = point['y']
        vendor_info = point['vendor_info']

        # Retrieve vendor total from totals.txt
        vendor_total = get_vendor_total(vendor_info)

        # Create text annotation with vendor total
        ax.text(x, y, f'Total: {vendor_total}', fontsize=font_size, ha='center', va='center', color='black')

    ax.figure.canvas.draw()

# Function to load points from the text file
def load_points_from_file():
    global points
    points = []
    try:
        with open("totals.txt", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:  # Ensure row has at least 3 elements
                    try:
                        x, y, vendor_info = float(row[0]), float(row[1]), row[2]
                        points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
                    except (ValueError, IndexError):
                        # Handle cases where conversion to float fails or index out of range
                        print(f"Ignoring invalid row: {row}")
                else:
                    print(f"Ignoring incomplete row: {row}")
        update_scatter()  # Update scatter plot after loading points
    except FileNotFoundError:
        # Handle case where file does not exist initially
        print("File 'totals.txt' not found!")

# Function to retrieve vendor total from totals.txt
def get_vendor_total(vendor_info):
    try:
        with open("totals.txt", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 4 and parts[2] == vendor_info:
                    return parts[3]
    except FileNotFoundError:
        print("File 'totals.txt' not found!")

    return "N/A"

# Function to toggle between edit mode and view mode
def toggle_edit_mode():
    global edit_mode
    edit_mode = not edit_mode
    if edit_mode:
        messagebox.showinfo("Edit Mode", "Edit Mode: Click to add points")
    else:
        messagebox.showinfo("View Mode", "View Mode: Clicks do not add points")

# Function to handle font size slider update
def update_font_size(value):
    update_scatter()

# Function to process data from data.csv based on objective classifications
def process_data_from_csv():
    try:
        subprocess.run(['python3', 'process_totals.py'])
    except FileNotFoundError:
        messagebox.showerror("Error", "process_totals.py not found!")

# Initialize tkinter
root = tk.Tk()
root.title("Vendor Points Tracker")

# Create a main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Load image for the chart
img = mpimg.imread('packaged/DoDFanChart_CLEARED.png')
img_height, img_width, _ = img.shape

# Create a figure and axis with locked aspect ratio
fig, ax = plt.subplots()
ax.imshow(img, extent=[0, img_width, 0, img_height])
ax.set_aspect('auto')  # Maintain the aspect ratio of the image
ax.set_axis_off()  # Hide axes to prevent the image from moving

# Initialize scatter plot for points
scatter = ax.scatter([], [], color='red', s=50)

# Connect the click event to the on_click function
fig.canvas.mpl_connect('button_press_event', on_click)

# Convert matplotlib figure to tkinter canvas
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Load existing points from the file
load_points_from_file()

# Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create a "Data Processing" menu
data_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Data Processing", menu=data_menu)
data_menu.add_command(label="Process Data", command=process_data_from_csv)

# Create an "Edit Mode" toggle button
edit_mode_button = ttk.Button(main_frame, text="Toggle Edit Mode", command=toggle_edit_mode)
edit_mode_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Create a label and scale widget for font size control
label = ttk.Label(main_frame, text="Data Point Text Size")
label.pack(side=tk.LEFT, padx=10, pady=10)

slider = tk.Scale(main_frame, from_=8, to=20, orient=tk.VERTICAL, command=update_font_size)
slider.set(default_font_size)
slider.pack(side=tk.LEFT, padx=10, pady=10)

# Function to handle closing the application
def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Bind closing event to on_close function
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the tkinter main loop
root.mainloop()
