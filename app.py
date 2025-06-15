import tkinter as tk
from tkinter import ttk
import json
import os


# Load street names from the JSON file
def load_street_names(json_file):
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"The file '{json_file}' does not exist.")
    with open(json_file, "r") as file:
        data = json.load(file)
    return data.get("streets", [])


# Main application
class StreetSearchApp:
    def __init__(self, master, street_names):
        self.master = master
        master.title("Street Name Search")

        self.street_names = street_names

        # Create main frame
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Search term label and entry
        search_label = tk.Label(main_frame, text="Search Term:")
        search_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.search_entry = tk.Entry(main_frame)
        self.search_entry.grid(row=0, column=1, sticky="we", padx=5, pady=5)

        # First letter label and entry
        first_letter_label = tk.Label(main_frame, text="First Character's:")
        first_letter_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.first_letter_entry = tk.Entry(main_frame)
        self.first_letter_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Results listbox with scrollbar
        self.result_listbox = tk.Listbox(main_frame)
        self.result_listbox.grid(
            row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5
        )
        scrollbar = tk.Scrollbar(
            main_frame, orient=tk.VERTICAL, command=self.result_listbox.yview
        )
        scrollbar.grid(row=2, column=2, sticky="ns")
        self.result_listbox.config(yscrollcommand=scrollbar.set)

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Bind events
        self.search_entry.bind("<KeyRelease>", self.update_list)
        self.first_letter_entry.bind("<KeyRelease>", self.update_list)

        # Initial update
        self.update_list()

    def update_list(self, event=None):
        search_term = self.search_entry.get().lower()
        first_letter = self.first_letter_entry.get().lower()

        # Clear the listbox
        self.result_listbox.delete(0, tk.END)

        # Filter and display results
        for name in self.street_names:
            name_lower = name.lower()
            if search_term in name_lower:
                if first_letter:
                    if name_lower.startswith(first_letter):
                        self.result_listbox.insert(tk.END, name)
                else:
                    self.result_listbox.insert(tk.END, name)


# Run the application
if __name__ == "__main__":
    json_file = "roads.json"
    street_names = load_street_names(json_file)


    root = tk.Tk()
    app = StreetSearchApp(root, street_names)
    root.mainloop()
