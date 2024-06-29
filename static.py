import tkinter as tk
from tkinter import simpledialog, ttk
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import csv

# Global variables
points = []
debug_mode = False  # Initially debug mode is off
num_top_vendors = 5  # Default number of top vendors to display
edit_mode = False  # Initially in view mode

# Function to handle the click event for left mouse button
def on_click(event):
    if edit_mode and event.button == 1:  # Left mouse button in edit mode
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
            vendor_info_text.config(state=tk.NORMAL)
            vendor_info_text.delete(1.0, tk.END)
            vendor_info_text.insert(tk.END, "Highest Vendor Scores:\n" + "\n".join(highest_scores))
            vendor_info_text.config(state=tk.DISABLED)
            debug_message += f"\n - Highest Scores: {', '.join(highest_scores)}"

            # Update vendor comparison plot
            update_vendor_comparison_plot(highest_scores)
        else:
            vendor_info_text.config(state=tk.NORMAL)
            vendor_info_text.delete(1.0, tk.END)
            vendor_info_text.insert(tk.END, "No vendor scores found.")
            vendor_info_text.config(state=tk.DISABLED)
            debug_message += "\n - No vendor scores found."

            # Clear vendor comparison plot if no scores found
            clear_vendor_comparison_plot()

        scatter.set_color(colors)
        ax.figure.canvas.draw()

        # Print debug message to console if debug mode is enabled
        if debug_mode:
            print(debug_message)

# Function to update the scatter plot
def update_scatter():
    colors = ['grey'] * len(points)
    scatter.set_offsets([[p['x'], p['y']] for p in points])
    scatter.set_color(colors)

# Function to update the vendor comparison plot
def update_vendor_comparison_plot(highest_scores):
    # Clear previous plot
    vendor_comparison_plot.clear()

    # Extract vendors and scores
    vendors = []
    scores = []
    for score in highest_scores:
        parts = score.split(': ')
        vendors.append(parts[0])
        scores.append(float(parts[1]))

    # Plot data in vendor comparison plot
    vendor_comparison_plot.bar(vendors, scores, color='skyblue')
    vendor_comparison_plot.set_xlabel('Vendors')
    vendor_comparison_plot.set_ylabel('Scores')
    vendor_comparison_plot.set_title('Top Vendors Comparison')
    vendor_comparison_plot.set_xticklabels(vendors, rotation=45, ha='right')
    vendor_comparison_plot.grid(True)

    # Update canvas
    vendor_comparison_canvas.draw()

    # Print debug message to console if debug mode is enabled
    if debug_mode:
        debug_message = f"Updated vendor comparison plot with scores: {highest_scores}"
        print(debug_message)

# Function to clear the vendor comparison plot
def clear_vendor_comparison_plot():
    # Clear plot and redraw canvas
    vendor_comparison_plot.clear()
    vendor_comparison_canvas.draw()

    # Print debug message to console if debug mode is enabled
    if debug_mode:
        print("Cleared vendor comparison plot.")

# Function to find the highest scores for a given point
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
                                vendor, score = parts[0].strip(), float(parts[1].strip())  # Extract vendor and score, strip spaces
                                scores.append((vendor, score))

            except (ValueError, IndexError):
                print(f"Skipping invalid line in points.txt: {','.join(row)}")

    # Sort scores by score value in descending order
    scores.sort(key=lambda item: item[1], reverse=True)

    # Retrieve top scores based on selected number
    highest_scores = []
    for vendor, score in scores[:num_top_vendors]:
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

        # Print debug message to console if debug mode is enabled
        if debug_mode:
            debug_message = f"Zoomed in at ({x:.2f}, {y:.2f}) with scale factor {scale_factor:.2f}"
            print(debug_message)

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

    # Print debug message to console if debug mode is enabled
    if debug_mode:
        print("Loaded points from points.txt file.")

# Function to reset the view to the original limits
def reset_view():
    ax.set_xlim(original_xlim)
    ax.set_ylim(original_ylim)
    ax.figure.canvas.draw()

    # Print debug message to console if debug mode is enabled
    if debug_mode:
        print("Reset view to original limits.")

# Function to find the coordinates of an objective
def find_coordinates(objective):
    for point in points:
        if point['vendor_info'] == objective:
            return point['x'], point['y']
    return None, None

# Function to move mouse pointer to the given coordinates
def move_pointer_to_coordinates(x, y):
    if x is not None and y is not None:
        ax.plot([x], [y], marker='o', markersize=10, color='red')
        ax.figure.canvas.draw()
        # Display message in console
        if debug_mode:
            debug_message = f"Moved to objective at ({x}, {y})"
            print(debug_message)
    else:
        print("Invalid objective.")

# Function to search for an objective
def on_search():
    objective = search_entry.get()
    x, y = find_coordinates(objective)
    move_pointer_to_coordinates(x, y)

# Function to toggle debug mode
def toggle_debug_mode():
    global debug_mode
    debug_mode = not debug_mode
    if debug_mode:
        print("Debug mode enabled.")
    else:
        print("Debug mode disabled.")

# Function to toggle edit mode
def toggle_edit_mode():
    global edit_mode
    edit_mode = not edit_mode
    if edit_mode:
        edit_mode_label.config(text="Edit Mode")
        print("Edit mode enabled.")
    else:
        edit_mode_label.config(text="View Mode")
        print("View mode enabled.")

# Function to update the number of top vendors to display
def update_num_top_vendors(event):
    global num_top_vendors
    num_top_vendors = int(num_top_vendors_combobox.get())
    if debug_mode:
        print(f"Number of top vendors to display updated to: {num_top_vendors}")

# Initialize Tkinter
root = tk.Tk()
root.title("Interactive Vendor Map")

# Create a main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a main paned window
main_pane = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
main_pane.pack(fill=tk.BOTH, expand=True)

# Create a frame for chart
chart_frame = ttk.Frame(main_pane)
chart_frame.grid_rowconfigure(0, weight=1)
chart_frame.grid_columnconfigure(0, weight=1)
main_pane.add(chart_frame, weight=2)  # Larger pane for the chart

# Load an image for the chart
img = mpimg.imread('img/DoDFanChart.png')
img_height, img_width, _ = img.shape

# Create a figure and axis with locked aspect ratio
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
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create a frame for dialog and vendor comparison plot
dialog_and_vendor_frame = ttk.Frame(main_pane)
dialog_and_vendor_frame.grid_rowconfigure(0, weight=1)
dialog_and_vendor_frame.grid_columnconfigure(0, weight=1)
dialog_and_vendor_frame.grid_columnconfigure(1, weight=1)
main_pane.add(dialog_and_vendor_frame, weight=1)  # Smaller pane for dialog and vendor comparison plot

# Create a frame for the dialog
dialog_frame = ttk.Frame(dialog_and_vendor_frame, padding="10")
dialog_frame.grid(row=0, column=0, sticky="nsew")

# Create a label for vendor information
vendor_info_label = ttk.Label(dialog_frame, text="Vendor Information", style="TLabel")
vendor_info_label.pack(fill=tk.X, pady=10)

# Create a scrolled text widget for displaying vendor information
vendor_info_text = ScrolledText(dialog_frame, wrap=tk.WORD, height=10, font=("Helvetica", 10))
vendor_info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
vendor_info_text.insert(tk.END, "Hover over a point to see highest vendor scores.")
vendor_info_text.config(state=tk.DISABLED)

# Create a reset button
reset_button = ttk.Button(dialog_frame, text="Reset View", command=reset_view)
reset_button.pack(fill=tk.X, padx=10, pady=10)

# Add a search box and button to the dialog frame
search_label = ttk.Label(dialog_frame, text="Search Objective:", style="TLabel")
search_label.pack(fill=tk.X, padx=10, pady=5)

search_entry = ttk.Entry(dialog_frame, width=25)
search_entry.pack(fill=tk.X, padx=10, pady=5)

search_button = ttk.Button(dialog_frame, text="Search", command=on_search)
search_button.pack(fill=tk.X, padx=10, pady=5)

# Add a combobox for selecting the number of top vendors to display
num_top_vendors_label = ttk.Label(dialog_frame, text="Number of Top Vendors:", style="TLabel")
num_top_vendors_label.pack(fill=tk.X, padx=10, pady=5)

num_top_vendors_combobox = ttk.Combobox(dialog_frame, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], state='readonly')
num_top_vendors_combobox.set(num_top_vendors)
num_top_vendors_combobox.pack(fill=tk.X, padx=10, pady=5)
num_top_vendors_combobox.bind('<<ComboboxSelected>>', update_num_top_vendors)

# Create a frame for vendor comparison plot
vendor_comparison_frame = ttk.Frame(dialog_and_vendor_frame, padding="10")
vendor_comparison_frame.grid(row=0, column=1, sticky="nsew")

# Create a subplot for vendor comparison plot with locked aspect ratio
vendor_comparison_fig, vendor_comparison_plot = plt.subplots()
vendor_comparison_plot.set_xlabel('Vendors')
vendor_comparison_plot.set_ylabel('Scores')
vendor_comparison_plot.set_title('Top Vendors Comparison')
vendor_comparison_plot.grid(True)

# Convert the subplot to a Tkinter Canvas
vendor_comparison_canvas = FigureCanvasTkAgg(vendor_comparison_fig, master=vendor_comparison_frame)
vendor_comparison_canvas.draw()
vendor_comparison_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Load existing points
load_points()

# Create a frame for buttons at the bottom
button_frame = ttk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create a debug mode button
debug_button = ttk.Button(button_frame, text="Debug Mode", command=toggle_debug_mode)
debug_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Create an edit mode toggle button and label
edit_mode_button = ttk.Button(button_frame, text="Toggle Edit Mode", command=toggle_edit_mode)
edit_mode_button.pack(side=tk.RIGHT, padx=10, pady=10)

edit_mode_label = ttk.Label(button_frame, text="View Mode")
edit_mode_label.pack(side=tk.RIGHT, padx=10, pady=10)

# Start the Tkinter event loop
root.mainloop()
