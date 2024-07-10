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
default_font_size = 14  # Increased default font size
slider = None  # Initialize slider as None globally
vendor_totals = {}
vendor_data = []  # List to store vendor data
vendor_table = None  # Initialize vendor_table globally
color_enabled = False  # Global variable to control color state
num_vendors = 35  # Default number of vendors

# Custom colormap for point colors
def get_color_for_percentage(percentage):
    if percentage < 80:
        return (0.6, 0.8, 0.6)
    elif percentage <= 100:
        return (0, 1, 0)
    else:
        norm = Normalize(vmin=100, vmax=200)
        red_intensity = norm(percentage)
        return (1, 1 - red_intensity, 1 - red_intensity)

# Function to handle click event on the graph
def on_click(event):
    global points, edit_mode
    if edit_mode:
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            vendor_info = simpledialog.askstring("Input", "Enter vendor info:")
            if vendor_info:
                points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
                with open("totals.txt", "a") as f:
                    f.write(f"{x},{y},{vendor_info}\n")
                update_scatter()

# Function to update the scatter plot with points and text size
def update_scatter():
    global points, slider, vendor_totals, color_enabled
    font_size = int(slider.get()) if slider else default_font_size

    scatter.set_offsets([[0, 0]])
    for annotation in ax.texts:
        annotation.remove()

    if points:
        offsets = []
        colors = []
        for point in points:
            x = point['x']
            y = point['y']
            vendor_info = point['vendor_info']

            vendor_total_info = vendor_totals.get(vendor_info, {"total": "N/A", "gaps": "N/A"})
            vendor_total = vendor_total_info["total"]
            gap_info = vendor_total_info["gaps"]

            if vendor_total != "N/A":
                try:
                    vendor_total = vendor_total.replace('%', '')
                    percentage = float(vendor_total)
                except ValueError:
                    percentage = 0.0
            else:
                percentage = 0.0

            offsets.append([x, y])
            if color_enabled:
                colors.append(get_color_for_percentage(percentage))
            else:
                colors.append((0, 0, 0, 0))

            annotation_text = f'Total: {vendor_total}%'
            if ": Grand" in vendor_info:
                gap_text = ""
            else:
                if gap_info.strip() == "N/A" or gap_info.strip() == "0 ()":
                    gap_text = "Gaps: 0"
                else:
                    gap_count = gap_info.split(' ')[0]
                    gap_text = f"Gaps: {gap_count}"

            ax.text(x, y, annotation_text, fontsize=font_size, ha='center', va='center', color='black')
            if len(gap_text) >= 1:
                ax.text(x, y - 25, gap_text, fontsize=font_size, ha='center', va='center', color='black')

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
                if len(row) >= 3:
                    try:
                        x, y = float(row[0]), float(row[1])
                        vendor_info = row[2]
                        if len(row) == 4:
                            total = row[3]
                            gaps = "N/A"
                        else:
                            total = row[3]
                            gaps = ','.join(row[4:])
                        points.append({'x': x, 'y': y, 'vendor_info': vendor_info})
                        vendor_totals[vendor_info] = {"total": total, "gaps": gaps}
                        print(f"Loaded vendor info: {vendor_info}, Total: {total}, Gaps: {gaps}")
                    except (ValueError, IndexError):
                        print(f"Ignoring invalid row: {row}")
                else:
                    print(f"Ignoring incomplete row: {row}")
        update_scatter()
    except FileNotFoundError:
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
                    if len(parts) >= 3:
                        vendor_name = parts[2].strip()
                        percentages = [part.strip() for part in parts[3:]]
                        vendor_data.append({'vendor_name': vendor_name, 'percentages': percentages})
                    else:
                        print(f"Ignoring invalid line: {line}")
        update_vendor_table()
    except FileNotFoundError:
        print("File 'vendor_totals.txt' not found!")

# Function to update the vendor table with loaded data
def update_vendor_table():
    global vendor_table, num_vendors
    if vendor_table is None:
        return

    vendor_table.delete(*vendor_table.get_children())

    columns = ["Pillar Classification"]
    for i in range(1, num_vendors + 1):
        columns.append(f"Vendor Name {i}")
        columns.append(f"Percentage {i}")

    columns.insert(0, "Pillar Classification")

    vendor_table["columns"] = columns

    for i, col in enumerate(columns):
        vendor_table.heading(f"#{i}", text=col)

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

# Function to toggle color state
def toggle_color_state():
    global color_enabled
    color_enabled = not color_enabled
    update_scatter()

# Function to process data from data.csv based on objective classifications
def process_data_from_csv():
    try:
        subprocess.run(['python', 'process_totals.py'])
        load_points_from_file()
    except FileNotFoundError:
        messagebox.showerror("Error", "process_totals.py not found!")

def get_number_of_vendors():
    global num_vendors
    try:
        with open('data.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)
            num_vendors = len(header) - 1
    except FileNotFoundError:
        print("File 'data.csv' not found!")
    except Exception as e:
        print(f"Error reading 'data.csv': {e}")

def main():
    global root, canvas, fig, ax, scatter, vendor_table

    get_number_of_vendors()

    root = tk.Tk()
    root.title("Vendor Points Tracker")

    root.geometry("1200x800")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    img = mpimg.imread('packaged/DoDFanChart_CLEARED.png')
    img_height, img_width, _ = img.shape

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.imshow(img, extent=[0, img_width, 0, img_height])
    ax.set_aspect('auto')
    ax.set_axis_off()

    scatter = ax.scatter([], [], s=50)

    fig.canvas.mpl_connect('button_press_event', on_click)

    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    load_points_from_file()

    vendor_table_frame = ttk.Frame(main_frame)
    vendor_table_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    vendor_table_scroll = ttk.Scrollbar(vendor_table_frame, orient=tk.HORIZONTAL)
    vendor_table_scroll.pack(side=tk.BOTTOM, fill=tk.X)

    vendor_table = ttk.Treeview(vendor_table_frame, columns=(), show='headings', xscrollcommand=vendor_table_scroll.set)
    vendor_table_scroll.config(command=vendor_table.xview)
    vendor_table.pack(fill=tk.BOTH, expand=True)

    load_vendor_data_from_file()

    color_toggle_button = ttk.Button(main_frame, text="Toggle Color", command=toggle_color_state)
    color_toggle_button.pack(pady=10)

    edit_mode_button = ttk.Button(main_frame, text="Toggle Edit Mode", command=toggle_edit_mode)
    edit_mode_button.pack(pady=10)

    def on_close():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

if __name__ == "__main__":
    main()
