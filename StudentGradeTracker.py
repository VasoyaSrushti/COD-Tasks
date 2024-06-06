import tkinter as tk
from tkinter import messagebox

# Function to initialize subjects
def initialize_subjects():
    try:
        global num_subjects
        num_subjects = int(num_subjects_entry.get())
        if num_subjects <= 0:
            raise ValueError("Number of subjects should be greater than 0")

        subjects_frame.pack_forget()
        add_subjects()
    except ValueError:
        messagebox.showerror("Error", "Invalid number of subjects")

# Function to add entry fields for subjects
def add_subjects():
    for widget in subjects_entries_frame.winfo_children():
        widget.destroy()

    for i in range(num_subjects):
        tk.Label(subjects_entries_frame, text=f"Subject {i+1} Name:", bg=bg_color, fg=label_fg_color, font=("Arial", 14)).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        subject_name_entry = tk.Entry(subjects_entries_frame, font=("Arial", 14), bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
        subject_name_entry.grid(row=i, column=1, padx=5, pady=5)
        subject_name_entries.append(subject_name_entry)

        tk.Label(subjects_entries_frame, text=f"Obtained Marks:", bg=bg_color, fg=label_fg_color, font=("Arial", 14)).grid(row=i, column=2, padx=5, pady=5, sticky='e')
        obtained_entry = tk.Entry(subjects_entries_frame, font=("Arial", 14), bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
        obtained_entry.grid(row=i, column=3, padx=5, pady=5)
        obtained_entries.append(obtained_entry)

        tk.Label(subjects_entries_frame, text=f"Total Marks:", bg=bg_color, fg=label_fg_color, font=("Arial", 14)).grid(row=i, column=4, padx=5, pady=5, sticky='e')
        total_entry = tk.Entry(subjects_entries_frame, font=("Arial", 14), bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
        total_entry.grid(row=i, column=5, padx=5, pady=5)
        total_entries.append(total_entry)

    tk.Button(subjects_entries_frame, text="Calculate Average", font=("Arial", 14), bg=button_bg_color, fg=button_fg_color, command=calculate_average).grid(row=num_subjects, column=0, columnspan=6, padx=5, pady=5)
    subjects_entries_frame.pack(pady=10)

# Function to calculate average percentage and determine letter grade
def calculate_average():
    try:
        total_obtained = 0
        total_possible = 0

        for i in range(num_subjects):
            subject_name = subject_name_entries[i].get()
            if not subject_name:
                raise ValueError("Subject name cannot be empty")

            obtained = float(obtained_entries[i].get())
            total = float(total_entries[i].get())
            total_obtained += obtained
            total_possible += total

        if total_possible == 0:
            raise ValueError("Total marks should be greater than 0")

        average_percentage = (total_obtained / total_possible) * 100

        if average_percentage >= 90:
            letter_grade = 'A'
        elif average_percentage >= 80:
            letter_grade = 'B'
        elif average_percentage >= 70:
            letter_grade = 'C'
        elif average_percentage >= 60:
            letter_grade = 'D'
        else:
            letter_grade = 'F'

        result_label.config(text=f"Average Percentage: {average_percentage:.2f}%\nLetter Grade: {letter_grade}")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Create the main window
root = tk.Tk()
root.title("Student Grade Tracker")
bg_color = "#f0f0f0"
root.configure(bg=bg_color)

num_subjects = 0
subject_name_entries = []
obtained_entries = []
total_entries = []

# Styles
entry_bg_color = "lightgray"
entry_fg_color = "black"
button_bg_color = "lightgreen"
button_fg_color = "black"
label_fg_color = "black"

# Function to add hover effect on buttons
def on_enter(e):
    e.widget['background'] = "lightgreen"

def on_leave(e):
    e.widget['background'] = button_bg_color

# Create and place initial input fields and labels
tk.Label(root, text="Enter Number of Subjects:", bg=bg_color, fg=label_fg_color, font=("Arial", 14)).pack(pady=10)
num_subjects_entry = tk.Entry(root, font=("Arial", 14), bg=entry_bg_color, fg=entry_fg_color, insertbackground=entry_fg_color)
num_subjects_entry.pack(pady=5)

initialize_button = tk.Button(root, text="Initialize Subjects", font=("Arial", 14), bg=button_bg_color, fg=button_fg_color, command=initialize_subjects)
initialize_button.pack(pady=5)
initialize_button.bind("<Enter>", on_enter)
initialize_button.bind("<Leave>", on_leave)

# Frame for entering subjects marks
subjects_entries_frame = tk.Frame(root, bg=bg_color)

# Frame for adding subjects button
subjects_frame = tk.Frame(root, bg=bg_color)
subjects_frame.pack(pady=10)

# Create and place the result label
result_label = tk.Label(root, text="Average Percentage: \nLetter Grade: ", bg=bg_color, fg=label_fg_color, font=("Arial", 14))
result_label.pack(pady=10)

# Run the application
root.mainloop()
