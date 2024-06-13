import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.library = {}

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title label
        title_label = tk.Label(main_frame, text="Library Management System", bg="#4682b4", fg="white", font=("Helvetica", 18, "bold"), pady=10)
        title_label.pack(fill=tk.X)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f0f8ff")
        button_frame.pack(pady=10)

        # Add buttons
        button_style = {"font": ("Helvetica", 12), "bg": "#4682b4", "fg": "white", "activebackground": "#5a9bd4", "activeforeground": "white"}
        self.add_button = tk.Button(button_frame, text="Add Item", command=self.add_item, **button_style)
        self.checkout_button = tk.Button(button_frame, text="Check Out Item", command=self.checkout_item, **button_style)
        self.return_button = tk.Button(button_frame, text="Return Item", command=self.return_item, **button_style)
        self.search_button = tk.Button(button_frame, text="Search Item", command=self.search_item, **button_style)
        self.delete_button = tk.Button(button_frame, text="Delete Item", command=self.delete_item, **button_style)

        self.add_button.grid(row=0, column=0, padx=10, pady=5)
        self.checkout_button.grid(row=0, column=1, padx=10, pady=5)
        self.return_button.grid(row=0, column=2, padx=10, pady=5)
        self.search_button.grid(row=0, column=3, padx=10, pady=5)
        self.delete_button.grid(row=0, column=4, padx=10, pady=5)

        # Treeview frame
        tree_frame = tk.Frame(main_frame, bg="#f0f8ff")
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Treeview for displaying library items
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Helvetica', 12))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Helvetica', 14, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Category", "Status"), show='headings', style="mystyle.Treeview")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def add_item(self):
        add_item_window = tk.Toplevel(self.root)
        add_item_window.title("Add Item")
        add_item_window.geometry("300x200")
        add_item_window.config(bg="#f0f8ff")

        tk.Label(add_item_window, text="Item Name:", bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=10)
        item_name_entry = tk.Entry(add_item_window)
        item_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_item_window, text="Category:", bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=10)
        category_combobox = ttk.Combobox(add_item_window, values=["Book", "DVD", "Magazine"])
        category_combobox.grid(row=1, column=1, padx=10, pady=10)

        def save_item():
            item_name = item_name_entry.get().strip()
            category = category_combobox.get()
            if item_name and category:
                if item_name in self.library:
                    messagebox.showerror("Error", f"Item {item_name} already exists.")
                else:
                    self.library[item_name] = {"category": category, "checked_out": False}
                    self.update_treeview()
                    messagebox.showinfo("Success", f"Item {item_name} added under category {category}.")
                    add_item_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter both item name and category.")

        save_button = tk.Button(add_item_window, text="Save", command=save_item)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)


    def checkout_item(self):
        item = simpledialog.askstring("Input", "Enter item name to check out:")
        if item:
            item = item.strip()
            if item in self.library and not self.library[item]["checked_out"]:
                self.library[item]["checked_out"] = True
                self.update_treeview()
                messagebox.showinfo("Success", f"Item {item} checked out.")
            elif item in self.library and self.library[item]["checked_out"]:
                messagebox.showerror("Error", f"Item {item} is already checked out.")
            else:
                messagebox.showerror("Error", f"Item {item} not found.")

    def return_item(self):
        item = simpledialog.askstring("Input", "Enter item name to return:")
        if item:
            item = item.strip()
            if item in self.library and self.library[item]["checked_out"]:
                self.library[item]["checked_out"] = False
                self.update_treeview()
                messagebox.showinfo("Success", f"Item {item} returned.")
            elif item in self.library and not self.library[item]["checked_out"]:
                messagebox.showerror("Error", f"Item {item} is not checked out.")
            else:
                messagebox.showerror("Error", f"Item {item} not found.")

    def search_item(self):
        item = simpledialog.askstring("Input", "Enter item name to search:")
        if item:
            item = item.strip()
            if item in self.library:
                status = "Checked out" if self.library[item]["checked_out"] else "Available"
                category = self.library[item]["category"]
                messagebox.showinfo("Found", f"Item: {item}\nCategory: {category}\nStatus: {status}")
            else:
                messagebox.showerror("Error", f"Item {item} not found.")

    def delete_item(self):
        item = simpledialog.askstring("Input", "Enter item name to delete:")
        if item:
            item = item.strip()
            if item in self.library:
                del self.library[item]
                self.update_treeview()
                messagebox.showinfo("Success", f"Item {item} deleted.")
            else:
                messagebox.showerror("Error", f"Item {item} not found.")

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for item, info in self.library.items():
            status = "Checked out" if info["checked_out"] else "Available"
            self.tree.insert("", "end", values=(item, info["category"], status))

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
