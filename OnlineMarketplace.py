import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import os

class OnlineMarketplace:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Marketplace")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Initialize the main frames
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame, bg="#e0e0e0", width=200, relief=tk.RAISED, bd=2)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.SUNKEN, bd=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize buttons with cool colors
        self.add_product_button = tk.Button(self.left_frame, text="Add Product", command=self.add_product, bg="#00796B", fg="white", font=("Helvetica", 12, "bold"))
        self.view_products_button = tk.Button(self.left_frame, text="View Products", command=self.view_products, bg="#0288D1", fg="white", font=("Helvetica", 12, "bold"))
        self.search_product_button = tk.Button(self.left_frame, text="Search Product", command=self.search_product, bg="#8E24AA", fg="white", font=("Helvetica", 12, "bold"))

        self.add_product_button.pack(fill=tk.X, padx=20, pady=(20, 10))
        self.view_products_button.pack(fill=tk.X, padx=20, pady=10)
        self.search_product_button.pack(fill=tk.X, padx=20, pady=10)

        # Initialize product display area
        self.product_list_frame = tk.Frame(self.right_frame, bg="#ffffff")
        self.product_list_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.product_list_frame, bg="#ffffff")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.product_list_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.inner_frame = tk.Frame(self.canvas, bg="#ffffff")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Initialize product detail view
        self.product_detail_frame = tk.Frame(self.right_frame, bg="#ffffff", bd=2, relief=tk.RAISED)
        self.product_detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.product_detail_frame.pack_forget()

        self.product_name_label = tk.Label(self.product_detail_frame, text="", font=("Helvetica", 14, "bold"), bg="#ffffff")
        self.product_name_label.pack(pady=10, padx=10, anchor="w")

        self.product_price_label = tk.Label(self.product_detail_frame, text="", font=("Helvetica", 12), bg="#E0F7FA")
        self.product_price_label.pack(pady=5, padx=10, anchor="w")

        self.product_seller_label = tk.Label(self.product_detail_frame, text="", font=("Helvetica", 12), bg="#E0F7FA")
        self.product_seller_label.pack(pady=5, padx=10, anchor="w")

        self.product_description_label = tk.Label(self.product_detail_frame, text="", font=("Helvetica", 12), bg="#E0F7FA", wraplength=500)
        self.product_description_label.pack(pady=5, padx=10, anchor="w")

        self.product_image_label = tk.Label(self.product_detail_frame, text="", bg="#ffffff")
        self.product_image_label.pack(pady=5, padx=10, anchor="w")

        self.product_reviews_label = tk.Label(self.product_detail_frame, text="Reviews:", font=("Helvetica", 12, "bold"), bg="#ffffff")
        self.product_reviews_label.pack(pady=10, padx=10, anchor="w")

        self.product_reviews_list = ScrolledText(self.product_detail_frame, font=("Helvetica", 10), wrap=tk.WORD, height=10, bg="#E8EAF6", bd=2, relief=tk.SUNKEN)
        self.product_reviews_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.add_review_label = tk.Label(self.product_detail_frame, text="Add Review:", font=("Helvetica", 12, "bold"), bg="#ffffff")
        self.add_review_label.pack(pady=10, padx=10, anchor="w")

        self.add_review_text = tk.Text(self.product_detail_frame, height=4, font=("Helvetica", 10), bg="#E8EAF6", bd=2, relief=tk.SUNKEN)
        self.add_review_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.submit_review_button = tk.Button(self.product_detail_frame, text="Submit Review", command=self.submit_review, bg="#00796B", fg="white", font=("Helvetica", 12, "bold"), height=1)
        self.submit_review_button.pack(pady=10, fill=tk.X, padx=10)

        # Add default products
        self.marketplace = {
            "Laptop": {
                "price": 999.99,
                "seller": "TechStore",
                "description": "High-performance laptop with 16GB RAM and 512GB SSD.",
                "image": "default_laptop.jpg",
                "reviews": ["Excellent laptop!", "Worth every penny."]
            },
            "Headphones": {
                "price": 199.99,
                "seller": "AudioWorld",
                "description": "Noise-cancelling over-ear headphones.",
                "image": "default_headphones.jpg",
                "reviews": ["Great sound quality.", "Very comfortable."]
            },
            "Smartphone": {
                "price": 799.99,
                "seller": "MobileHub",
                "description": "Latest smartphone with stunning display and camera.",
                "image": "default_smartphone.jpg",
                "reviews": ["Amazing camera!", "Super fast."]
            }
        }

    def add_product(self):
        product_name = simpledialog.askstring("Input", "Enter product name:")
        if not product_name:
            return

        price = simpledialog.askfloat("Input", "Enter product price:")
        if price is None:
            return

        seller_name = simpledialog.askstring("Input", "Enter seller name:")
        if not seller_name:
            return

        description = simpledialog.askstring("Input", "Enter product description:")
        if not description:
            return

        image_path = filedialog.askopenfilename(title="Select product image",
                                                filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")))
        if not image_path:
            return

        # Add product to marketplace
        self.marketplace[product_name] = {
            "price": price,
            "seller": seller_name,
            "description": description,
            "image": image_path,
            "reviews": []
        }

        # Display success message
        messagebox.showinfo("Success", f"Product '{product_name}' added by seller '{seller_name}'.")
        
        # Update the product list display
        self.view_products()

    def view_products(self):
        self.product_detail_frame.pack_forget()

        # Clear previous content in inner_frame
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        for product, details in self.marketplace.items():
            product_frame = tk.Frame(self.inner_frame, bg="#ffffff", bd=2, relief=tk.RAISED)
            product_frame.pack(fill=tk.BOTH, padx=10, pady=10, ipadx=5, ipady=5)

            product_name_label = tk.Label(product_frame, text=f"Product: {product}", font=("Helvetica", 12, "bold"), bg="#ffffff")
            product_name_label.pack(anchor="w")

            price_label = tk.Label(product_frame, text=f"Price: ${details['price']}", bg="#ffffff")
            price_label.pack(anchor="w")

            seller_label = tk.Label(product_frame, text=f"Seller: {details['seller']}", bg="#ffffff")
            seller_label.pack(anchor="w")

            description_label = tk.Label(product_frame, text=f"Description: {details['description']}", bg="#ffffff", wraplength=300)
            description_label.pack(anchor="w")

            image_label = tk.Label(product_frame, text=f"Image: {os.path.basename(details['image'])}", bg="#ffffff")
            image_label.pack(anchor="w")

            reviews_label = tk.Label(product_frame, text="Reviews:", font=("Helvetica", 10, "bold"), bg="#ffffff")
            reviews_label.pack(anchor="w")

            reviews_text = ScrolledText(product_frame, wrap=tk.WORD, height=4, bg="#E8EAF6", bd=2, relief=tk.SUNKEN)
            reviews_text.pack(fill=tk.BOTH, expand=True)

            for review in details['reviews']:
                reviews_text.insert(tk.END, f"- {review}\n")

        self.canvas.update_idletasks()  # Update the canvas to compute scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))  # Set scroll region based on the inner_frame size

        # Add vertical scrollbar to canvas
        self.scrollbar.config(command=self.canvas.yview)

        # Display canvas and scrollbar
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Hide the product_detail_frame if visible
        self.product_detail_frame.pack_forget()

    def search_product(self):
        product_name = simpledialog.askstring("Input", "Enter product name to search:")
        if not product_name:
            return

        if product_name in self.marketplace:
            self.display_product_details(product_name)
        else:
            messagebox.showerror("Error", "Product not found.")

    def display_product_details(self, product_name):
        details = self.marketplace[product_name]
        self.product_name_label.config(text=f"Product: {product_name}")
        self.product_price_label.config(text=f"Price: ${details['price']}")
        self.product_seller_label.config(text=f"Seller: {details['seller']}")
        self.product_description_label.config(text=f"Description: {details['description']}")
        self.product_image_label.config(text=f"Image: {os.path.basename(details['image'])}")

        self.product_reviews_list.delete(1.0, tk.END)
        for review in details['reviews']:
            self.product_reviews_list.insert(tk.END, f"- {review}\n")

        self.product_list_frame.pack_forget()
        self.product_detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def submit_review(self):
        review_text = self.add_review_text.get("1.0", tk.END).strip()
        if review_text:
            product_name = self.product_name_label.cget("text").split(": ")[1]
            self.marketplace[product_name]["reviews"].append(review_text)
            messagebox.showinfo("Success", "Review submitted successfully.")
            self.display_product_details(product_name)
            self.add_review_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Review cannot be empty.")


root = tk.Tk()
app = OnlineMarketplace(root)
root.mainloop()
