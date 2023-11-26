import tkinter as tk
from tkinter import filedialog
import subprocess
import sys

def run_go_script(demo_path):
    try:
        # Run the Go script with the demo file path as an argument
        subprocess.run(["python", "run_go_script.py", demo_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the Go script: {e}")
        sys.exit(1)

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Demo Files", "*.dem"), ("All Files", "*.*")]
    )
    if file_path:
        print("Selected file:", file_path)
        run_go_script(file_path)

# Create the main window
root = tk.Tk()
root.title("Demo File Explorer")

# Create and pack a button for file selection
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
