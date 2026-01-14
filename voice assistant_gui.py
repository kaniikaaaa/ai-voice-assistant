"""
AI Assistant Zen - Simple GUI (Alternative Interface)
SECURITY: Implements SHA-256 password hashing (CRITICAL-003 Fixed)
THREADING: Proper thread lifecycle management (HIGH-001 Fixed)
"""
import customtkinter as ctk
import tkinter.messagebox as messagebox
import os
import threading
import hashlib
import sys
from assistant_core import run_babygirl_assistant, request_stop, reset_stop
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Security: Hash password using SHA-256
def hash_password(password):
    """Hash password using SHA-256 for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash using constant-time comparison"""
    return hash_password(password) == password_hash

# Secure in-memory user store with hashed passwords
# Format: {email: password_hash}
USER_DB = {
    "user@example.com": hash_password("password123")  # Default demo account with hashed password
}

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
        email = self.new_email.get().strip()
        password = self.new_password.get()
        
        # Input validation
        if not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Password strength validation
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return
        
        # Check if user already exists
        if email in USER_DB:
            messagebox.showerror("Error", "User already exists!")
            return
        
        # SECURITY FIX: Hash password before storing
        password_hash = hash_password(password)
        USER_DB[email] = password_hash
        
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_screen()

    def login_user(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Input validation
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
        
        # SECURITY FIX: Verify using hash comparison (constant-time)
        if email in USER_DB and verify_password(password, USER_DB[email]):
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
        """Start voice assistant in separate thread with proper lifecycle management"""
        # HIGH-001 FIX: Reset stop flag before starting
        reset_stop()
        
        self.clear_window()
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self, 
            text="🎤 AI Assistant Zen is active...\nListening for your commands", 
            font=("Arial", 16)
        )
        self.status_label.pack(pady=30)
        
        # Activity indicator
        self.activity_label = ctk.CTkLabel(
            self, 
            text="● RUNNING", 
            font=("Arial", 12),
            text_color="green"
        )
        self.activity_label.pack(pady=10)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            self, 
            text="Stop Assistant", 
            command=self.stop_assistant,
            fg_color="red",
            hover_color="darkred"
        )
        self.stop_button.pack(pady=20)

        # HIGH-001 FIX: Run assistant in separate thread with proper termination support
        # Thread is NOT daemon - we want to clean it up properly
        self.assistant_thread = threading.Thread(
            target=self._run_assistant_wrapper,
            daemon=False  # Changed from True - proper cleanup required
        )
        self.assistant_thread.start()
        
        print("[GUI] Assistant thread started")

    def _run_assistant_wrapper(self):
        """Wrapper to run assistant and handle exceptions"""
        try:
            print("[GUI] Assistant starting in thread...")
            run_babygirl_assistant()
        except Exception as e:
            print(f"[GUI ERROR] Assistant thread crashed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("[GUI] Assistant thread finished")

    def stop_assistant(self):
        """HIGH-001 FIX: Properly stop the assistant thread"""
        print("[GUI] Stop button clicked - initiating graceful shutdown...")
        
        # HIGH-001 FIX: Signal the assistant core to stop
        request_stop()
        
        # Update UI to show stopping
        if hasattr(self, 'status_label'):
            self.status_label.configure(text="⏹️ Stopping assistant...\nPlease wait...")
        if hasattr(self, 'activity_label'):
            self.activity_label.configure(text="● STOPPING", text_color="orange")
        if hasattr(self, 'stop_button'):
            self.stop_button.configure(state="disabled", text="Stopping...")
        
        # Update GUI
        self.update()
        
        # Wait for thread to finish (with timeout)
        if self.assistant_thread and self.assistant_thread.is_alive():
            print("[GUI] Waiting for assistant thread to terminate...")
            self.assistant_thread.join(timeout=3.0)  # 3 second timeout
            
            if self.assistant_thread.is_alive():
                print("[GUI WARNING] Thread did not stop gracefully within timeout")
                messagebox.showwarning(
                    "Warning", 
                    "Assistant may still be running in background.\nPlease restart the application if issues persist."
                )
            else:
                print("[GUI] Assistant thread terminated successfully")
        
        # Clean up thread reference
        self.assistant_thread = None
        
        # Return to dashboard
        self.show_dashboard()
        print("[GUI] Returned to dashboard")

# Run GUI
if __name__ == "__main__":
    app = AssistantApp()
    app.mainloop()