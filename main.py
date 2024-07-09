import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import static
import process_totals
import vendor_sync
import totals
import process_vendor_totals  # Import the module
import os
import pandas as pd
import re

# Function to execute static.py
def run_static():
    try:
        static.main()
    except Exception as e:
        messagebox.showerror("Error", f"Error running static.py: {e}")

# Function to execute process_totals.py
def run_process_totals():
    try:
        process_totals.main()
    except Exception as e:
        messagebox.showerror("Error", f"Error running process_totals.py: {e}")

# Function to execute vendor_sync.py
def run_vendor_sync():
    try:
        vendor_sync.main()
    except Exception as e:
        messagebox.showerror("Error", f"Error running vendor_sync.py: {e}")

# Function to execute totals.py
def run_totals():
    try:
        totals.main()
    except Exception as e:
        messagebox.showerror("Error", f"Error running totals.py: {e}")

# Function to execute process_vendor_totals.py
def run_process_vendor_totals():
    try:
        process_vendor_totals.main()
    except Exception as e:
        messagebox.showerror("Error", f"Error running process_vendor_totals.py: {e}")

# Function to run all scripts
def run_all_scripts():
    try:
        run_totals()
        run_static()
        run_process_totals()
        run_vendor_sync()
        run_process_vendor_totals()
    except Exception as e:
        messagebox.showerror("Error", f"Error running all scripts: {e}")

# Function to clean vendor names for processing
def clean_vendor_name(name):
    return re.sub(r'\s*\([^)]*\)', '', name).strip()  # Cleans the vendor name with regex formatting logic

# Function to select and replace "data.csv"
def select_data_file():
    file_path = filedialog.askopenfilename(title="Select Data File", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            # Read the Excel file
            df = pd.read_excel(file_path, header=None)

            # Extract vendor names
            vendor_names = []
            col_index = 2
            while col_index < df.shape[1] and not pd.isna(df.iloc[1, col_index]):
                vendor_name = clean_vendor_name(df.iloc[1, col_index])
                vendor_names.append(vendor_name)
                col_index += 1

            # Create the header for the CSV
            header = ["Objective"] + vendor_names

            # Extract the data from the specified ranges
            ranges = [
                (14, 41),  # A15:A42
                (43, 66),  # A44:A67
                (68, 85),  # A69:A86
                (87, 117),  # A88:A118
                (119, 130),  # A120:A131
                (132, 151),  # A133:A152
                (153, 169)  # A154:A170
            ]

            data = []
            for start, end in ranges:
                for i in range(start, end + 1):
                    if i < df.shape[0]:  # Check if the row index is within bounds
                        row = [df.iloc[i, 0]]  # First column is the Objective
                        row.extend(df.iloc[i, 2:col_index])  # Vendor columns within bounds
                        data.append(row)

            # Create a DataFrame from the data and write to CSV
            data_df = pd.DataFrame(data, columns=header)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            target_file_path = os.path.join(script_dir, "data.csv")
            data_df.to_csv(target_file_path, index=False)
        except Exception as e:
            print(e)

# Initialize tkinter
root = tk.Tk()
root.title("Script Runner")

# Create a main frame
main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.pack()

# Button to run all scripts
run_all_button = ttk.Button(main_frame, text="Run All Scripts", command=run_all_scripts)
run_all_button.grid(row=0, column=0, columnspan=2, pady=10)

# Button to select data file
select_data_button = ttk.Button(main_frame, text="Select Data File", command=select_data_file)
select_data_button.grid(row=1, column=0, columnspan=2, pady=10)

# Dropdown menu to run individual scripts
script_var = tk.StringVar()
script_var.set("Select Script")

def run_selected_script():
    script = script_var.get()
    if script == "Run static.py":
        run_static()
    elif script == "Run process_totals.py":
        run_process_totals()
    elif script == "Run vendor_sync.py":
        run_vendor_sync()
    elif script == "Run totals.py":
        run_totals()
    elif script == "Run process_vendor_totals.py":
        run_process_vendor_totals()
    else:
        messagebox.showerror("Error", "No script selected")

script_menu = ttk.OptionMenu(main_frame, script_var, "Select Script",
                             "Run static.py", "Run process_totals.py",
                             "Run vendor_sync.py", "Run totals.py",
                             "Run process_vendor_totals.py")
script_menu.grid(row=2, column=0, columnspan=1, pady=10)

run_script_button = ttk.Button(main_frame, text="Run Selected Script", command=run_selected_script)
run_script_button.grid(row=2, column=1, pady=10)

# Function to handle closing the application
def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Bind closing event to on_close function
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the tkinter main loop
root.mainloop()
