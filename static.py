import tkinter as tk
from tkinter import simpledialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import csv

# Global variable for storing the press event
press_event = None

# Store original x and y limits
original_xlim = None
original_ylim = None

# Function to handle the click event for left mouse button
def on_click(event):
    if event.button == 1:  # Left mouse button
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            # Prompt for vendor info
            vendor_info = simpledialog.askstring("Input", "Enter vendor info:", parent=root)
            if vendor_info:
                with open("points.txt", "a", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([x, y, vendor_info])
                points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
                update_scatter()  # Update scatter plot
                ax.figure.canvas.draw()  # Redraw the figure

# Function to update the scatter plot
def update_scatter():
    colors = ['grey'] * len(points)
    scatter.set_offsets([[p['x'], p['y']] for p in points])
    scatter.set_color(colors)

# Function to handle the motion event (hover)
def on_motion(event):
    x, y = event.xdata, event.ydata
    if x is not None and y is not None:
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        detection_radius = 0.01 * (xlim[1] - xlim[0])  # 1% of the current x-axis range
        colors = ['grey'] * len(points)
        for i, point in enumerate(points):
            if ((x - point['x'])**2 + (y - point['y'])**2) ** 0.5 < detection_radius:
                colors[i] = 'blue'
                vendor_info_label.config(text=f"Vendor Info:\n{point['vendor_info']}")
                break
        else:
            vendor_info_label.config(text="Vendor Info:")
        scatter.set_color(colors)
        ax.figure.canvas.draw()

# Function to handle the scroll event (zoom)
def on_scroll(event):
    scale_factor = 1.1 if event.button == 'up' else 0.9
    curr_xlim = ax.get_xlim()
    curr_ylim = ax.get_ylim()
    xdata = event.xdata  # get event x location
    ydata = event.ydata  # get event y location

    if xdata is None or ydata is None:
        return

    new_width = (curr_xlim[1] - curr_xlim[0]) * scale_factor
    new_height = (curr_ylim[1] - curr_ylim[0]) * scale_factor

    relx = (curr_xlim[1] - xdata) / (curr_xlim[1] - curr_xlim[0])
    rely = (curr_ylim[1] - ydata) / (curr_ylim[1] - curr_ylim[0])

    ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
    ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
    ax.figure.canvas.draw()

# Function to handle the drag event (pan)
def on_press(event):
    global press_event
    if event.button == 3:  # Right mouse button
        press_event = event

def on_release(event):
    global press_event
    press_event = None

def on_motion_pan(event):
    global press_event
    if press_event is None or event.button != 3:
        return

    if event.xdata is None or event.ydata is None or press_event.xdata is None or press_event.ydata is None:
        return

    dx = event.xdata - press_event.xdata
    dy = event.ydata - press_event.ydata
    curr_xlim = ax.get_xlim()
    curr_ylim = ax.get_ylim()

    ax.set_xlim(curr_xlim[0] - dx, curr_xlim[1] - dx)
    ax.set_ylim(curr_ylim[0] - dy, curr_ylim[1] - dy)
    ax.figure.canvas.draw()

    press_event.xdata = event.xdata
    press_event.ydata = event.ydata

# Function to load points from the TXT file
def load_points():
    if os.path.exists("points.txt"):
        with open("points.txt", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    x, y, vendor_info = float(row[0]), float(row[1]), row[2]
                    points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
                except ValueError:
                    print(f"Skipping invalid line in points.txt: {','.join(row)}")
    if points:
        update_scatter()  # Initialize scatter plot with points
    else:
        scatter.set_offsets([[]])  # Handle empty points with empty 2D array
    ax.figure.canvas.draw()

# Function to reset the view to the original limits
def reset_view():
    ax.set_xlim(original_xlim)
    ax.set_ylim(original_ylim)
    ax.figure.canvas.draw()

# Create the main window
root = tk.Tk()
root.title("Interactive Chart")

# Create a style for better appearance
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", padding=6, font="Helvetica 12")
style.configure("TButton", padding=6, font="Helvetica 12", background="#4CAF50", foreground="white")
style.configure("TFrame", background="#f5f5f5")

# Load the image
image_path = 'img/DoDFanChart.png'
img = mpimg.imread(image_path)
img_width, img_height = img.shape[1], img.shape[0]

# Create a figure and axis
fig, ax = plt.subplots()
ax.imshow(img, extent=[0, img_width, 0, img_height])
ax.set_aspect('auto')  # Maintain the aspect ratio of the image
ax.set_axis_off()  # Hide axes to prevent the image from moving

# Store the original limits
original_xlim = ax.get_xlim()
original_ylim = ax.get_ylim()

# Initialize scatter plot for points
points = []
scatter = ax.scatter([], [], color='grey', s=50)

# Connect the click, motion, scroll, and pan events
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('scroll_event', on_scroll)
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion_pan)

# Convert the Matplotlib figure to a Tkinter Canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create a frame for the side menu with a fixed size
side_frame = ttk.Frame(root, padding="10", width=300, height=600)
side_frame.pack_propagate(False)  # Prevent the frame from resizing
side_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

# Create a label for displaying vendor information with a fixed size
vendor_info_label = ttk.Label(side_frame, text="Vendor Info:", anchor="nw", justify="left", wraplength=280)
vendor_info_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a reset button
reset_button = ttk.Button(side_frame, text="Reset View", command=reset_view)
reset_button.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Load existing points
load_points()

# Start the Tkinter event loop
tk.mainloop()
