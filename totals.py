import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.image as mpimg
import csv

# Global variables
points = []

# Function to handle click event on the graph
def on_click(event):
    global points
    x, y = event.xdata, event.ydata
    if x is not None and y is not None:
        # Prompt for vendor info
        vendor_info = simpledialog.askstring("Input", "Enter vendor info:")
        if vendor_info:
            # Save point to points list
            points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
            update_scatter()  # Update scatter plot
            save_points_to_file()  # Save points to file

# Function to update the scatter plot with points
def update_scatter():
    global points
    scatter.set_offsets([[p['x'], p['y']] for p in points])
    ax.figure.canvas.draw()

# Function to save points to a text file
def save_points_to_file():
    global points
    with open("totals.txt", "w") as f:
        writer = csv.writer(f)
        for point in points:
            writer.writerow([point['x'], point['y'], point['vendor_info']])

# Function to load points from the text file
def load_points_from_file():
    global points
    points = []
    try:
        with open("totals.txt", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                x, y, vendor_info = float(row[0]), float(row[1]), row[2]
                points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
        update_scatter()  # Update scatter plot after loading points
    except FileNotFoundError:
        # Handle case where file does not exist initially
        pass

# Function to process data from data.csv based on objective classifications
def process_data_from_csv():
    # Load classifications from objective_classifications.txt.txt
    classifications = {}
    try:
        with open("objective_classifications.txt.txt", "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    classifications[parts[0].strip()] = parts[1].strip()
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "objective_classifications.txt.txt not found!")

    # Process data from data.csv
    try:
        with open("data.csv", "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                objective = row['Objective']
                vendor = row['Vendor']
                score = float(row['Score'])

                # Determine pillar based on objective classification
                if objective.startswith('1') and classifications.get(objective) != 'ADVANCED':
                    pillar = "User Pillar: Target"
                elif objective.startswith('2'):
                    pillar = "Device Pillar"
                elif objective.startswith('3'):
                    pillar = "Application & Workload Pillar"
                elif objective.startswith('4'):
                    pillar = "Data Pillar"
                elif objective.startswith('5'):
                    pillar = "Network & Environment Pillar"
                elif objective.startswith('6'):
                    pillar = "Automation & Orchestration Pillar"
                elif objective.startswith('7'):
                    pillar = "Visibility & Analytics Pillar"
                else:
                    pillar = "Unknown"

                # Update total for the vendor in the respective pillar
                # This is a simplified example, you may need to adjust the data structure based on your needs
                print(f"Updating total for Vendor: {vendor}, Pillar: {pillar}, Score: {score}")

    except FileNotFoundError:
        messagebox.showerror("File Not Found", "data.csv not found!")

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

# Function to handle closing the application
def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Bind closing event to on_close function
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the tkinter main loop
root.mainloop()
