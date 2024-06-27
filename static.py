import tkinter as tk
from tkinter import simpledialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import csv

# Global variables
points = []


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

# Function that displays the vendor info based on hover within detection radius.
def on_motion(event):
    x, y = event.xdata, event.ydata
    if x is not None and y is not None:
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        detection_radius = 0.01 * (xlim[1] - xlim[0])  # 1% of the current x-axis range
        colors = ['grey'] * len(points)
        highest_scores = []

        debug_message = f"Mouse hovering at ({x:.2f}, {y:.2f}):"

        for i, point in enumerate(points):
            if ((x - point['x']) ** 2 + (y - point['y']) ** 2) ** 0.5 < detection_radius:
                colors[i] = 'blue'
                highest_scores = find_highest_scores(point['x'], point['y'])
                debug_message += f"\n - Point ({point['x']:.2f}, {point['y']:.2f}): {point['vendor_info']}"
                break

        if highest_scores:
            vendor_info_label.config(text=f"Highest Vendor Scores:\n{', '.join(highest_scores)}")
            debug_message += f"\n - Highest Scores: {', '.join(highest_scores)}"
        else:
            vendor_info_label.config(text="No vendor scores found.")
            debug_message += "\n - No vendor scores found."

        scatter.set_color(colors)
        ax.figure.canvas.draw()

        # Print debug message to console
        # print(debug_message)

# Function to update the scatter plot
def update_scatter():
    colors = ['grey'] * len(points)
    scatter.set_offsets([[p['x'], p['y']] for p in points])
    scatter.set_color(colors)

def find_highest_scores(x, y):
    scores = []

    with open("points.txt", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                if len(row) >= 3:
                    x_val, y_val, vendor_info = float(row[0]), float(row[1]), row[2]
                    if x_val == x and y_val == y:
                        # Extract vendor scores starting from the 3rd index (index 2)
                        for item in row[3:]:
                            parts = item.split(': ')
                            if len(parts) == 2:
                                vendor, score = parts[0], float(parts[1])  # Extract vendor and score
                                scores.append((vendor, score))

            except (ValueError, IndexError):
                print(f"Skipping invalid line in points.txt: {','.join(row)}")

    # Sort scores by score value in descending order
    scores.sort(key=lambda item: item[1], reverse=True)

    # Retrieve top 5 scores
    highest_scores = []
    for vendor, score in scores[:5]:
        highest_scores.append(f"{vendor}: {score}")

    return highest_scores

# Function to handle scroll event for zooming
def on_scroll(event):
    x, y = event.xdata, event.ydata
    if event.button == 'up':
        scale_factor = 1.1  # Zoom in
    elif event.button == 'down':
        scale_factor = 0.9  # Zoom out
    else:
        return  # Exit if not scroll up or down

    if x is not None and y is not None:
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        new_xlim = (x - (x - xlim[0]) * scale_factor, x + (xlim[1] - x) * scale_factor)
        new_ylim = (y - (y - ylim[0]) * scale_factor, y + (ylim[1] - y) * scale_factor)

        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        ax.figure.canvas.draw()


# Function to load points from the TXT file
def load_points():
    global points
    points = []
    if os.path.exists("points.txt"):
        with open("points.txt", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if len(row) >= 3:
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
style.configure("TLabel", padding=10, font=("Helvetica", 12))

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
scatter = ax.scatter([], [], color='grey', s=50)

# Connect the click, motion, and scroll events
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('scroll_event', on_scroll)

# Convert the Matplotlib figure to a Tkinter Canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Create a frame for the side menu with a fixed size
side_frame = ttk.Frame(root, padding="10", width=300, height=600)
side_frame.pack_propagate(False)  # Prevent the frame from resizing
side_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

# Create a label for displaying vendor information with a fixed size
vendor_info_label = ttk.Label(side_frame, text="Hover over a point to see highest vendor scores.", anchor="nw",
                              justify="left", wraplength=280,
                              style="Info.TLabel")
vendor_info_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a reset button
reset_button = ttk.Button(side_frame, text="Reset View", command=reset_view)
reset_button.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Load existing points
load_points()

# Start the Tkinter event loop
tk.mainloop()
