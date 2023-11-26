import tkinter as tk
from tkinter import filedialog
import subprocess
import sys
import os

def run_go_script(demo_path):
    try:
        # Run the Go script with the demo file path as an argument
        subprocess.run(["go", "run", "parser.go", demo_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the Go script: {e}")
        sys.exit(1)

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select .dem file",
        filetypes=[("Demo files", "*.dem"), ("All files", "*.*")]
    )
    if file_path:
        run_go_script(file_path)

if __name__ == "__main__":
    # Create a simple tkinter window for the file dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Check if the Go script file exists
    if not os.path.exists("parser.go"):
        print("Error: parser.go not found.")
        sys.exit(1)

    # Open file dialog to select a .dem file
    select_file()
