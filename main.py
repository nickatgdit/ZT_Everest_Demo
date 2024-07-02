import tkinter as tk
from tkinter import ttk, messagebox
import static
import process_totals
import vendor_sync
import totals
import process_vendor_totals  # Import the module

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

# Initialize tkinter
root = tk.Tk()
root.title("Script Runner")

# Create a main frame
main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.pack()

# Button to run static.py
static_button = ttk.Button(main_frame, text="Run static.py", command=run_static)
static_button.grid(row=0, column=0, padx=10, pady=5)

# Button to run process_totals.py
process_totals_button = ttk.Button(main_frame, text="Run process_totals.py", command=run_process_totals)
process_totals_button.grid(row=0, column=1, padx=10, pady=5)

# Button to run vendor_sync.py
vendor_sync_button = ttk.Button(main_frame, text="Run vendor_sync.py", command=run_vendor_sync)
vendor_sync_button.grid(row=1, column=0, padx=10, pady=5)

# Button to run totals.py
totals_button = ttk.Button(main_frame, text="Run totals.py", command=run_totals)
totals_button.grid(row=1, column=1, padx=10, pady=5)

# Button to run process_vendor_totals.py
process_vendor_totals_button = ttk.Button(main_frame, text="Run process_vendor_totals.py", command=run_process_vendor_totals)
process_vendor_totals_button.grid(row=2, column=0, columnspan=2, pady=10)

# Function to handle closing the application
def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Bind closing event to on_close function
root.protocol("WM_DELETE_WINDOW", on_close)

# Start the tkinter main loop
root.mainloop()
