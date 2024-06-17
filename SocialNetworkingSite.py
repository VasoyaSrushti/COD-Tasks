import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, scrolledtext
from datetime import datetime

class SocialNetworkingSite:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Networking Site")
        self.root.geometry("1150x400")  # Adjusted window size
        self.root.configure(bg="#f8f9fa")

        self.users = {
            "user1": {"password": "password1", "messages": [], "friends": ["user2"], "posts": [
                {"user": "user1", "content": "Hello World!", "timestamp": "2024-06-18 09:30:00"},
                {"user": "user2", "content": "Hi there!", "timestamp": "2024-06-18 09:45:00"}
            ]},
            "user2": {"password": "password2", "messages": [], "friends": ["user1"], "posts": [
                {"user": "user2", "content": "Having a great day!", "timestamp": "2024-06-18 10:00:00"}
            ]}
        }
        self.current_user = None

        self.create_navigation_bar()

        self.content_frame = tk.Frame(self.root, bg="#ffffff")
        self.content_frame.pack(fill='both', expand=True)

    def create_navigation_bar(self):
        nav_bar = tk.Frame(self.root, bg="#343a40", height=50)
        nav_bar.pack(side='top', fill='x')

        button_style = {"font": ("Helvetica", 14), "bg": "#343a40", "fg": "white", "bd": 0}

        self.home_button = tk.Button(nav_bar, text="Home", command=self.view_news_feed, **button_style)
        self.home_button.pack(side='left', padx=20, pady=10)

        self.profile_button = tk.Button(nav_bar, text="Profile", command=self.view_profile, **button_style)
        self.profile_button.pack(side='left', padx=20, pady=10)

        self.share_button = tk.Button(nav_bar, text="Share Post", command=self.open_share_post_window, **button_style)
        self.share_button.pack(side='left', padx=20, pady=10)

        self.message_button = tk.Button(nav_bar, text="Messages", command=self.view_messages, **button_style)
        self.message_button.pack(side='left', padx=20, pady=10)

        self.view_feeds_button = tk.Button(nav_bar, text="View Feeds", command=self.view_news_feed, **button_style)
        self.view_feeds_button.pack(side='left', padx=20, pady=10)

        self.add_friend_button = tk.Button(nav_bar, text="Add Friend", command=self.add_friend, **button_style)
        self.add_friend_button.pack(side='left', padx=20, pady=10)

        self.logout_button = tk.Button(nav_bar, text="Log Out", command=self.log_out, **button_style)
        self.logout_button.pack(side='right', padx=20, pady=10)

        self.sign_up_button = tk.Button(nav_bar, text="Sign Up", command=self.sign_up, **button_style)
        self.sign_up_button.pack(side='right', padx=20, pady=10)

        self.login_button = tk.Button(nav_bar, text="Log In", command=self.log_in, **button_style)
        self.login_button.pack(side='right', padx=20, pady=10)

    def open_share_post_window(self):
        if not self.current_user:
            messagebox.showerror("Error", "You must log in first.")
            return
        
        child = tk.Toplevel(self.root)
        child.title("Share Post")
        child.geometry("400x200")
        child.configure(bg="#f0f0f0")

        shared_post_label = tk.Label(child, text="Your Post:", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
        shared_post_label.pack(pady=5)

        self.shared_post_entry = tk.Entry(child, font=("Helvetica", 12))
        self.shared_post_entry.pack(pady=5)

        share_button = ttk.Button(child, text="Share", command=self.perform_share_post)
        share_button.pack(pady=20)

    def perform_share_post(self):
        if self.current_user:
            shared_post = self.shared_post_entry.get()
            if shared_post:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.users[self.current_user]["posts"].append({
                    "user": self.current_user,
                    "content": shared_post,
                    "timestamp": timestamp
                })
                messagebox.showinfo("Success", "Post shared successfully.")
                self.clear_content_frame()
                self.view_news_feed()
            else:
                messagebox.showerror("Error", "Please enter your post.")
        else:
            messagebox.showerror("Error", "You must log in first.")

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def sign_up(self):
        child = self.open_child_window("Sign Up")
        tk.Label(child, text="Enter username:", bg="#f0f0f0", font=("Helvetica", 12, "bold")).pack(pady=5)
        username_entry = tk.Entry(child, font=("Helvetica", 12))
        username_entry.pack(pady=5)
        tk.Label(child, text="Enter password:", bg="#f0f0f0", font=("Helvetica", 12, "bold")).pack(pady=5)
        password_entry = tk.Entry(child, show="*", font=("Helvetica", 12))
        password_entry.pack(pady=5)
        ttk.Button(child, text="Sign Up", command=lambda: self.perform_signup(username_entry.get(), password_entry.get())).pack(pady=20)

    def perform_signup(self, username, password):
        if username in self.users:
            messagebox.showerror("Error", "Username already taken.")
        else:
            self.users[username] = {"password": password, "messages": [], "friends": [], "posts": []}
            messagebox.showinfo("Success", f"User {username} signed up.")

    def log_in(self):
        child = self.open_child_window("Log In")
        tk.Label(child, text="Select username:", bg="#f0f0f0", font=("Helvetica", 12, "bold")).pack(pady=5)
        username_combobox = ttk.Combobox(child, font=("Helvetica", 12), values=list(self.users.keys()))
        username_combobox.pack(pady=5)
        tk.Label(child, text="Enter password:", bg="#f0f0f0", font=("Helvetica", 12, "bold")).pack(pady=5)
        password_entry = tk.Entry(child, show="*", font=("Helvetica", 12))
        password_entry.pack(pady=5)
        ttk.Button(child, text="Log In", command=lambda: self.perform_login(username_combobox.get(), password_entry.get())).pack(pady=20)

    def perform_login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            messagebox.showinfo("Success", f"User {username} logged in.")
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def log_out(self):
        if self.current_user:
            messagebox.showinfo("Success", f"User {self.current_user} logged out.")
            self.current_user = None
        else:
            messagebox.showerror("Error", "No user currently logged in.")

    def view_profile(self):
        self.clear_content_frame()
        if self.current_user:
            user_data = self.users[self.current_user]
            friends = ", ".join(user_data["friends"])
            messages = "\n".join([f"{msg['sender']}: {msg['content']}" for msg in user_data["messages"]])
            profile_info = f"Username: {self.current_user}\nFriends: {friends}\nMessages:\n{messages}"

            tk.Label(self.content_frame, text=profile_info, bg="#ffffff", font=("Helvetica", 12, "bold")).pack(pady=20)
        else:
            messagebox.showerror("Error", "You must log in first.")

    def view_messages(self):
        self.clear_content_frame()
        if self.current_user:
            self.message_frame = tk.Frame(self.content_frame, bg="#ffffff")
            self.message_frame.pack(fill='both', expand=True)

            # Adjust height of scrolled text area and move it up by reducing padding
            self.message_list = scrolledtext.ScrolledText(self.message_frame, font=("Helvetica", 12), bg="#f0f0f0", height=15)
            self.message_list.pack(side='top', fill='both', expand=True, padx=10, pady=(10, 5))

            self.message_entry_frame = tk.Frame(self.message_frame, bg="#ffffff")
            self.message_entry_frame.pack(side='top', fill='x', pady=(5, 10))

            # Get list of usernames
            usernames = [user for user in self.users if user != self.current_user]

            # Create Combobox for selecting recipient
            self.recipient_combobox = ttk.Combobox(self.message_entry_frame, values=usernames, font=("Helvetica", 12))
            self.recipient_combobox.pack(side='left', padx=10, pady=10)
            self.recipient_combobox.set("Select Recipient")

            self.message_entry = tk.Entry(self.message_entry_frame, font=("Helvetica", 12))
            self.message_entry.pack(side='left', fill='x', expand=True, padx=10, pady=10)

            self.send_button = ttk.Button(self.message_entry_frame, text="Send", command=self.send_message)
            self.send_button.pack(side='right', padx=10, pady=(5, 10))  # Adjusted padding to move the button up

            self.load_messages()
        else:
            messagebox.showerror("Error", "You must log in first.")



    def load_messages(self):
        self.message_list.delete('1.0', tk.END)
        if self.current_user:
            for msg in self.users[self.current_user]["messages"]:
                self.message_list.insert(tk.END, f"{msg['sender']}: {msg['content']}\n")

    def send_message(self):
        recipient = self.recipient_combobox.get().strip()
        message = self.message_entry.get().strip()

        if recipient and message:
            if recipient in self.users:
                self.users[recipient]["messages"].append({"sender": self.current_user, "content": message})
                self.users[self.current_user]["messages"].append({"sender": self.current_user, "content": message})
                self.load_messages()
                self.message_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Message sent.")
            else:
                messagebox.showerror("Error", "Recipient not found.")
        else:
            messagebox.showerror("Error", "Recipient and message cannot be empty.")

    def view_news_feed(self):
        self.clear_content_frame()
        news_feed = []
        if self.current_user:
            for friend in self.users[self.current_user]["friends"]:
                news_feed.extend(self.users[friend]["posts"])
            news_feed.extend(self.users[self.current_user]["posts"])
            news_feed.sort(key=lambda post: post["timestamp"], reverse=True)

            for post in news_feed:
                post_frame = tk.Frame(self.content_frame, bg="#ffffff", pady=10)
                post_frame.pack(fill='x', padx=10, pady=5)
                post_user = tk.Label(post_frame, text=post["user"], font=("Helvetica", 12, "bold"), bg="#ffffff")
                post_user.pack(side='top', anchor='w')
                post_content = tk.Label(post_frame, text=post["content"], font=("Helvetica", 12), bg="#ffffff")
                post_content.pack(side='top', anchor='w')
                post_timestamp = tk.Label(post_frame, text=post["timestamp"], font=("Helvetica", 10, "italic"), bg="#ffffff")
                post_timestamp.pack(side='top', anchor='w')
        else:
            messagebox.showerror("Error", "You must log in first.")

    def add_friend(self):
        if self.current_user:
            child = self.open_child_window("Add Friend")
            tk.Label(child, text="Select username:", bg="#f0f0f0", font=("Helvetica", 12, "bold")).pack(pady=5)
            friend_combobox = ttk.Combobox(child, font=("Helvetica", 12), values=[user for user in self.users.keys() if user != self.current_user])
            friend_combobox.pack(pady=5)
            ttk.Button(child, text="Add", command=lambda: self.perform_add_friend(friend_combobox.get())).pack(pady=20)
        else:
            messagebox.showerror("Error", "You must log in first.")

    def perform_add_friend(self, new_friend):
        if new_friend:
            if new_friend in self.users and new_friend != self.current_user:
                if new_friend not in self.users[self.current_user]["friends"]:
                    self.users[self.current_user]["friends"].append(new_friend)
                    self.users[new_friend]["friends"].append(self.current_user)
                    messagebox.showinfo("Success", f"{new_friend} added as a friend.")
                else:
                    messagebox.showerror("Error", "This user is already your friend.")
            else:
                messagebox.showerror("Error", "User not found.")
        else:
            messagebox.showerror("Error", "Please select a user.")

    def open_child_window(self, title):
        child = tk.Toplevel(self.root)
        child.title(title)
        child.geometry("300x200")
        child.configure(bg="#f0f0f0")
        return child

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkingSite(root)
    root.mainloop()
