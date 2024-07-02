import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
import csv
import subprocess
from matplotlib.colors import Normalize

# Global variables
points = []
edit_mode = False
default_font_size = 10
slider = None  # Initialize slider as None globally
vendor_totals = {}
vendor_data = []  # List to store vendor data
vendor_table = None  # Initialize vendor_table globally

# Custom colormap for point colors
def get_color_for_percentage(percentage):
    if percentage < 80:
        # Desaturated green
        return (0.6, 0.8, 0.6)
    elif percentage <= 100:
        # Green
        return (0, 1, 0)
    else:
        # Increasingly red
        norm = Normalize(vmin=100, vmax=200)
        red_intensity = norm(percentage)  # Normalize to 0-1 range
        return (1, 1 - red_intensity, 1 - red_intensity)

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
    global points, slider, vendor_totals
    # Calculate font size based on slider value
    font_size = int(slider.get()) if slider else default_font_size

    # Clear existing points and annotations
    scatter.set_offsets([[0, 0]])
    for annotation in ax.texts:
        annotation.remove()

    if points:
        # Create new points and annotations
        offsets = []
        colors = []
        for point in points:
            x = point['x']
            y = point['y']
            vendor_info = point['vendor_info']

            # Retrieve vendor total from vendor_totals
            vendor_total = vendor_totals.get(vendor_info, "N/A")
            if vendor_total != "N/A":
                try:
                    vendor_total = vendor_total.replace('%', '')
                    percentage = float(vendor_total)
                except ValueError:
                    percentage = 0.0
            else:
                percentage = 0.0

            # Append point data
            offsets.append([x, y])
            colors.append(get_color_for_percentage(percentage))

            # Create text annotation with vendor total
            ax.text(x, y, f'Total: {vendor_total}%', fontsize=font_size, ha='center', va='center', color='black')

        scatter.set_offsets(offsets)
        scatter.set_color(colors)

    ax.figure.canvas.draw()

# Function to load points from the text file
def load_points_from_file():
    global points, vendor_totals
    points = []
    vendor_totals = {}
    try:
        with open("totals.txt", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:  # Ensure row has at least 3 elements
                    try:
                        x, y, vendor_info = float(row[0]), float(row[1]), row[2]
                        points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
                        if len(row) >= 4:
                            vendor_totals[vendor_info] = row[3]
                    except (ValueError, IndexError):
                        # Handle cases where conversion to float fails or index out of range
                        print(f"Ignoring invalid row: {row}")
                else:
                    print(f"Ignoring incomplete row: {row}")
        update_scatter()  # Update scatter plot after loading points
    except FileNotFoundError:
        # Handle case where file does not exist initially
        print("File 'totals.txt' not found!")

# Function to load vendor data from the text file
def load_vendor_data_from_file():
    global vendor_data
    vendor_data = []
    try:
        with open("vendor_totals.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        vendor_name = parts[2].strip()  # Third entry as vendor name
                        percentages = [part.strip() for part in parts[3:]]  # Remaining entries as percentages
                        vendor_data.append({'vendor_name': vendor_name, 'percentages': percentages})
                    else:
                        print(f"Ignoring invalid line: {line}")
        update_vendor_table()  # Update vendor table after loading data
    except FileNotFoundError:
        print("File 'vendor_totals.txt' not found!")

# Function to update the vendor table with loaded data
def update_vendor_table():
    global vendor_table
    if vendor_table is None:
        return

    # Clear existing table rows and columns
    vendor_table.delete(*vendor_table.get_children())

    # Define column structure
    columns = ["Pillar Classification"]
    for i in range(1, 36):
        columns.append(f"Vendor Name {i}")
        columns.append(f"Percentage {i}")

    # Insert Pillar Label
    columns.insert(0, "Pillar Classification")

    # Set columns and headings
    vendor_table["columns"] = columns

    for i, col in enumerate(columns):
        vendor_table.heading(f"#{i}", text=col)

    # Insert data into the table
    for i, data in enumerate(vendor_data):
        vendor_name = data['vendor_name']
        percentages = data['percentages']
        values = [vendor_name] + percentages
        vendor_table.insert("", tk.END, iid=i, values=values)

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
        subprocess.run(['python', 'process_totals.py'])
        load_points_from_file()  # Reload points after processing
    except FileNotFoundError:
        messagebox.showerror("Error", "process_totals.py not found!")

def main():
    global root, canvas, fig, ax, scatter, vendor_table

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
    scatter = ax.scatter([], [], s=50)

    # Connect the click event to the on_click function
    fig.canvas.mpl_connect('button_press_event', on_click)

    # Convert matplotlib figure to tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Load existing points from the file
    load_points_from_file()

    # Create a Treeview widget for the vendor data table with horizontal scrollbar
    vendor_table_frame = ttk.Frame(main_frame)
    vendor_table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    vendor_table_scroll = ttk.Scrollbar(vendor_table_frame, orient=tk.HORIZONTAL)
    vendor_table_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    vendor_table = ttk.Treeview(vendor_table_frame, columns=(), show='headings', xscrollcommand=vendor_table_scroll.set)
    vendor_table_scroll.config(command=vendor_table.xview)
    vendor_table.pack(fill=tk.BOTH, expand=True)

    # Load vendor data from file
    load_vendor_data_from_file()

    # Function to handle closing the application
    def on_close():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    # Bind closing event to on_close function
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Start the tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
