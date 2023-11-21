import tkinter as tk
from tkinter import filedialog


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            # Display the content in a text box or perform any other operation
            text_area.delete(1.0, tk.END)  # Clear previous content
            text_area.insert(tk.END, content)


# Create the main window
root = tk.Tk()
root.title("NFA to DFA Converter")

# Create a button to open the file dialog
open_button = tk.Button(root, text="Choose NFA description", command=open_file)
open_button.pack(pady=20)

# Create a text area to display the content of the JSON file
text_area = tk.Text(root, height=20, width=50)
text_area.pack(padx=20, pady=10)

root.mainloop()
