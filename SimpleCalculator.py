import tkinter as tk
from tkinter import messagebox

# Function to update the expression in the text entry box
def update_expression(value):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + value)

# Function to evaluate the final expression
def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Function to clear the text entry box
def clear():
    entry.delete(0, tk.END)

# Function to add hover effect on buttons
def on_enter(e):
    e.widget['background'] = 'lightblue'

def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")
root.configure(bg="lightgray")

# Create and place the entry field for the expression
entry = tk.Entry(root, font=("Arial", 20), borderwidth=5, relief="sunken", bg="white", fg="black")
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

# Create buttons
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '00','.', '0',  '+'
]

button_style = {
    'font': ("Arial", 18),
    'borderwidth': 1,
    'relief': 'raised',
    'bg': 'lightgray',
    'activebackground': 'gray',
    'fg': 'black',
    'activeforeground': 'white',
}

# Create and place the number and operator buttons
row_val = 1
col_val = 0

for button in buttons:
    btn = tk.Button(root, text=button, **button_style, command=lambda x=button: update_expression(x))
    btn.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Create and place the clear button
btn_clear = tk.Button(root, text='C', **button_style, command=clear)
btn_clear.grid(row=row_val, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
btn_clear.bind("<Enter>", on_enter)
btn_clear.bind("<Leave>", on_leave)

# Create and place the equals button
btn_equals = tk.Button(root, text='=', **button_style, command=calculate)
btn_equals.grid(row=row_val, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)
btn_equals.bind("<Enter>", on_enter)
btn_equals.bind("<Leave>", on_leave)

# Configure row and column weights to make buttons expand
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Run the application
root.mainloop()
