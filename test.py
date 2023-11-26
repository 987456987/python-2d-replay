import os
import tkinter as tk
from tkinter import filedialog
import threading
import subprocess

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("DEM File Explorer")

        # Set the initial directory to the "data" folder within the app folder
        app_folder = os.path.dirname(os.path.abspath(__file__))
        initial_path = os.path.join(app_folder, "data")

        self.current_path = tk.StringVar()
        self.current_path.set(initial_path)

        self.create_widgets()

    def create_widgets(self):
        # Entry widget to display and edit the current path
        path_entry = tk.Entry(self.root, textvariable=self.current_path, width=50)
        path_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Button to change the current directory
        change_dir_button = tk.Button(self.root, text="Change Directory", command=self.change_directory)
        change_dir_button.grid(row=0, column=3, padx=5, pady=10)

        # Listbox to display .json file names
        self.file_listbox = tk.Listbox(self.root, width=70, height=20)
        self.file_listbox.grid(row=1, column=0, padx=10, pady=10, columnspan=4)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=1, column=4, sticky="ns")

        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Bind double click event to open the selected file or folder
        self.file_listbox.bind("<Double-Button-1>", self.double_click_event)

        # Button to run the replay.py script for the selected item
        run_script_button = tk.Button(self.root, text="Run Script", command=self.run_selected_script)
        run_script_button.grid(row=2, column=0, padx=10, pady=10)

        # Display .json file names in the current directory
        self.display_file_info()

    def display_file_info(self):
        path = self.current_path.get()
        self.file_listbox.delete(0, tk.END)  # Clear the listbox

        try:
            files = [file for file in os.listdir(path) if file.endswith(".json")]

            for file in files:
                self.file_listbox.insert(tk.END, file)
        except Exception as e:
            print(f"Error: {e}")

    def change_directory(self):
        new_path = filedialog.askdirectory(title="Select Directory")
        if new_path:
            self.current_path.set(new_path)
            self.display_file_info()

    def double_click_event(self, event):
        selected_item = self.file_listbox.get(self.file_listbox.curselection())
        current_path = self.current_path.get()
        selected_path = os.path.join(current_path, selected_item)

        if os.path.isfile(selected_path) and selected_path.endswith(".json"):
            # Run the replay.py script with the selected JSON file in a separate thread
            threading.Thread(target=self.run_replay_script, args=(selected_path,), daemon=True).start()

    def run_selected_script(self):
        selected_item = self.file_listbox.get(self.file_listbox.curselection())
        current_path = self.current_path.get()
        selected_path = os.path.join(current_path, selected_item)

        if os.path.isfile(selected_path) and selected_path.endswith(".json"):
            # Run the replay.py script with the selected JSON file in a separate thread
            threading.Thread(target=self.run_replay_script, args=(selected_path,), daemon=True).start()

    def run_replay_script(self, json_file_path):
        subprocess.run(["python", "replay.py", json_file_path])

if __name__ == "__main__":
    root = tk.Tk()
    file_explorer = FileExplorer(root)
    root.mainloop()
