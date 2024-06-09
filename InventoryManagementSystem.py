import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import hashlib

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("610x360")  # Adjust the initial window size
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)  # Make the window non-resizable

        self.inventory = {
            "Apple": [50],
            "Banana": [30],
            "Orange": [20],
            "Grapes": [45],
            "Pineapple": [15]
        }
        
        self.low_stock_threshold = 10  # Threshold for low stock alerts
        self.users = {"admin": hashlib.sha256("password".encode()).hexdigest()}  # User authentication

        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.login_frame.pack(pady=50)

        tk.Label(self.login_frame, text="Username:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, pady=5)
        tk.Label(self.login_frame, text="Password:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, pady=5)

        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=5)
        self.password_entry = tk.Entry(self.login_frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.authenticate, font=("Arial", 12), bg="#4CAF50", fg="#FFFFFF").grid(row=2, columnspan=2, pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username] == hashlib.sha256(password.encode()).hexdigest():
            self.login_frame.pack_forget()
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def create_main_screen(self):
        self.create_widgets()
        self.populate_tree()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 14), padding=10)
        style.configure("TFrame", background="#f0f0f0")
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 12))

        frame = ttk.Frame(self.root, style="TFrame")
        frame.pack(pady=10)

        self.tree = ttk.Treeview(frame, columns=("Product", "Quantity"), show="headings", height=10)
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.column("Product", width=150)
        self.tree.column("Quantity", width=100)
        self.tree.tag_configure('evenrow', background='#E8E8E8')
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        self.tree.pack()

        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="Add Product", command=self.add_product,
                                    font=("Arial", 12), bg="#4CAF50", fg="#FFFFFF", activebackground="#45a049", activeforeground="#000000")
        self.edit_button = tk.Button(button_frame, text="Edit Product", command=self.edit_product,
                                     font=("Arial", 12), bg="#4CAF50", fg="#FFFFFF", activebackground="#45a049", activeforeground="#000000")
        self.delete_button = tk.Button(button_frame, text="Delete Product", command=self.delete_product,
                                       font=("Arial", 12), bg="#4CAF50", fg="#FFFFFF", activebackground="#45a049", activeforeground="#000000")
        self.report_button = tk.Button(button_frame, text="Generate Report", command=self.generate_report,
                                       font=("Arial", 12), bg="#4CAF50", fg="#FFFFFF", activebackground="#45a049", activeforeground="#000000")

        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.edit_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.report_button.pack(side=tk.LEFT, padx=10, pady=10)

    def populate_tree(self):
        for index, (product, details) in enumerate(self.inventory.items()):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=(product, details[0]), tags=(tag,))

    def add_product(self):
        product = simpledialog.askstring("Input", "Enter product name:", parent=self.root)
        if product:
            if product in self.inventory:
                messagebox.showerror("Error", "Product already exists.", parent=self.root)
                return

            quantity = simpledialog.askinteger("Input", "Enter product quantity:", parent=self.root, minvalue=0)
            if quantity is not None:
                self.inventory[product] = [quantity]
                index = len(self.inventory) - 1
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.tree.insert("", tk.END, values=(product, quantity), tags=(tag,))
                messagebox.showinfo("Success", f"Product {product} added with quantity {quantity}.", parent=self.root)
            else:
                messagebox.showerror("Error", "Invalid quantity.", parent=self.root)
        else:
            messagebox.showerror("Error", "Invalid product name.", parent=self.root)

    def edit_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected.", parent=self.root)
            return

        item = self.tree.item(selected_item)
        product = item["values"][0]

        if product in self.inventory:
            quantity = simpledialog.askinteger("Input", "Enter new product quantity:", parent=self.root, minvalue=0)
            if quantity is not None:
                self.inventory[product] = [quantity]
                self.tree.item(selected_item, values=(product, quantity))
                messagebox.showinfo("Success", f"Product {product} updated with quantity {quantity}.", parent=self.root)
            else:
                messagebox.showerror("Error", "Invalid quantity.", parent=self.root)
        else:
            messagebox.showerror("Error", "Product not found.", parent=self.root)

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No product selected.", parent=self.root)
            return

        item = self.tree.item(selected_item)
        product = item["values"][0]

        if product in self.inventory:
            del self.inventory[product]
            self.tree.delete(selected_item)
            messagebox.showinfo("Success", f"Product {product} deleted.", parent=self.root)
        else:
            messagebox.showerror("Error", "Product not found.", parent=self.root)

    def generate_report(self):
        report = "Inventory Report:\n"
        low_stock = ""
        low_stock_flag = False  # Flag to check if there are any low stock items
        for product, details in self.inventory.items():
            report += f"{product}: {details[0]}\n"
            if details[0] < self.low_stock_threshold:
                low_stock += f"{product}: {details[0]}\n"
                low_stock_flag = True  # Set flag to True if any product is below threshold

        if low_stock_flag:
            messagebox.showinfo("Report", report, parent=self.root)
            messagebox.showwarning("Low Stock Alerts", low_stock, parent=self.root)
        else:
            messagebox.showinfo("Report", report + "\nAll products are sufficiently stocked.", parent=self.root)

root = tk.Tk()
app = InventoryManagementSystem(root)
root.mainloop()