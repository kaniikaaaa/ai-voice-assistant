import customtkinter as ctk
import tkinter.messagebox as messagebox
import os
import threading
from assistant_core import run_babygirl_assistant
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Dummy in-memory user store
USER_DB = {"user@example.com": "password123"}

# Main App Window
class AssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Assistant Zen")
        self.geometry("500x400")
        self.resizable(False, False)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.current_user = None
        self.assistant_thread = None
        self.show_login_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()
        self.login_label = ctk.CTkLabel(self, text="Login to AI Assistant Zen", font=("Arial", 20))
        self.login_label.pack(pady=20)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_user)
        self.login_button.pack(pady=10)

        self.to_register_button = ctk.CTkButton(self, text="No account? Register", command=self.show_register_screen)
        self.to_register_button.pack(pady=10)

    def show_register_screen(self):
        self.clear_window()
        self.register_label = ctk.CTkLabel(self, text="Register New Account", font=("Arial", 20))
        self.register_label.pack(pady=20)

        self.new_email = ctk.CTkEntry(self, placeholder_text="Email")
        self.new_email.pack(pady=10)

        self.new_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.new_password.pack(pady=10)

        self.register_btn = ctk.CTkButton(self, text="Create Account", command=self.register_user)
        self.register_btn.pack(pady=10)

        self.back_to_login = ctk.CTkButton(self, text="Back to Login", command=self.show_login_screen)
        self.back_to_login.pack(pady=10)

    def register_user(self):
        email = self.new_email.get()
        password = self.new_password.get()
        if not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        if email in USER_DB:
            messagebox.showerror("Error", "User already exists!")
            return
        USER_DB[email] = password
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_screen()

    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email in USER_DB and USER_DB[email] == password:
            self.current_user = email
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password!")

    def logout_user(self):
        self.current_user = None
        self.show_login_screen()

    def show_dashboard(self):
        self.clear_window()
        self.dashboard_label = ctk.CTkLabel(self, text=f"Welcome, {self.current_user}", font=("Arial", 18))
        self.dashboard_label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start Voice Assistant", command=self.start_assistant)
        self.start_button.pack(pady=10)

        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.logout_user)
        self.logout_button.pack(pady=10)

    def start_assistant(self):
        self.clear_window()
        label = ctk.CTkLabel(self, text="🎤 AI Assistant Zen is active...\nSay the wake word to begin", font=("Arial", 16))
        label.pack(pady=50)

        stop_button = ctk.CTkButton(self, text="Stop Assistant", command=self.stop_assistant)
        stop_button.pack(pady=10)

        # Run assistant in a separate thread to prevent GUI freezing
        self.assistant_thread = threading.Thread(target=run_babygirl_assistant, daemon=True)
        self.assistant_thread.start()

    def stop_assistant(self):
        # Return to dashboard
        self.show_dashboard()
        # Note: You may need to implement a proper stopping mechanism in assistant_core
        # if run_babygirl_assistant doesn't have a way to gracefully stop

# Run GUI
if __name__ == "__main__":
    app = AssistantApp()
    app.mainloop()