import customtkinter as ctk
import tkinter.messagebox as messagebox
import os
import sqlite3
import hashlib
import threading
import re
from assistant_core import run_babygirl_assistant
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Database setup
DB_NAME = "assistant_users.db"

def init_database():
    """Initialize SQLite database with users table"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"[OK] Database initialized: {DB_NAME}")

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash

def validate_email(email):
    """
    Validate email format using regex (RFC 5322 compliant)
    Returns True if email is valid, False otherwise
    """
    # Comprehensive email validation regex
    email_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]{0,63}@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$'
    
    # Additional validation checks
    if not email or len(email) > 254:  # Max email length per RFC 5321
        return False
    
    if email.count('@') != 1:  # Must have exactly one @ symbol
        return False
    
    local_part, domain = email.rsplit('@', 1)
    
    # Local part (before @) validation
    if len(local_part) > 64:  # Max local part length
        return False
    
    if local_part.startswith('.') or local_part.endswith('.'):
        return False
    
    if '..' in local_part:  # No consecutive dots
        return False
    
    # Domain validation
    if len(domain) > 253:  # Max domain length
        return False
    
    if domain.startswith('-') or domain.endswith('-'):
        return False
    
    # Apply regex pattern
    return re.match(email_pattern, email) is not None

def register_user_db(email, password):
    """Register a new user in the database"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    
    except sqlite3.IntegrityError:
        return False, "User already exists!"
    except Exception as e:
        return False, f"Database error: {str(e)}"

def login_user_db(email, password):
    """Verify user login credentials"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT password_hash FROM users WHERE email = ?",
            (email,)
        )
        
        result = cursor.fetchone()
        
        if result:
            password_hash = result[0]
            if verify_password(password, password_hash):
                # Update last login time
                cursor.execute(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE email = ?",
                    (email,)
                )
                conn.commit()
                conn.close()
                return True, "Login successful!"
            else:
                conn.close()
                return False, "Incorrect password!"
        else:
            conn.close()
            return False, "User not found!"
    
    except Exception as e:
        return False, f"Database error: {str(e)}"

def get_user_stats(email):
    """Get user statistics from database"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT created_at, last_login FROM users WHERE email = ?",
            (email,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'created_at': result[0],
                'last_login': result[1]
            }
        return None
    
    except Exception as e:
        print(f"Error fetching user stats: {e}")
        return None

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
        
        # Initialize database
        init_database()
        
        self.show_login_screen()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()
        self.login_label = ctk.CTkLabel(self, text="Login to AI Assistant Zen", font=("Arial", 20))
        self.login_label.pack(pady=20)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=300)
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_user, width=300)
        self.login_button.pack(pady=10)

        self.to_register_button = ctk.CTkButton(
            self, 
            text="No account? Register", 
            command=self.show_register_screen,
            width=300,
            fg_color="transparent",
            border_width=2
        )
        self.to_register_button.pack(pady=10)

    def show_register_screen(self):
        self.clear_window()
        self.register_label = ctk.CTkLabel(self, text="Register New Account", font=("Arial", 20))
        self.register_label.pack(pady=20)

        self.new_email = ctk.CTkEntry(self, placeholder_text="Email", width=300)
        self.new_email.pack(pady=10)

        self.new_password = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=300)
        self.new_password.pack(pady=10)

        self.confirm_password = ctk.CTkEntry(self, placeholder_text="Confirm Password", show="*", width=300)
        self.confirm_password.pack(pady=10)

        self.register_btn = ctk.CTkButton(self, text="Create Account", command=self.register_user, width=300)
        self.register_btn.pack(pady=10)

        self.back_to_login = ctk.CTkButton(
            self, 
            text="Back to Login", 
            command=self.show_login_screen,
            width=300,
            fg_color="transparent",
            border_width=2
        )
        self.back_to_login.pack(pady=10)

    def register_user(self):
        email = self.new_email.get().strip()
        password = self.new_password.get()
        confirm_password = self.confirm_password.get()
        
        # Validation
        if not email or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        # Register in database
        success, message = register_user_db(email, password)
        
        if success:
            messagebox.showinfo("Success", message)
            self.show_login_screen()
        else:
            messagebox.showerror("Error", message)

    def login_user(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address!")
            return
        
        # Verify credentials from database
        success, message = login_user_db(email, password)
        
        if success:
            self.current_user = email
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", message)

    def logout_user(self):
        self.current_user = None
        self.show_login_screen()

    def show_dashboard(self):
        self.clear_window()
        
        # Welcome message
        self.dashboard_label = ctk.CTkLabel(
            self, 
            text=f"Welcome, {self.current_user}", 
            font=("Arial", 18, "bold")
        )
        self.dashboard_label.pack(pady=20)
        
        # Get and display user stats
        stats = get_user_stats(self.current_user)
        if stats:
            stats_text = f"Last Login: {stats.get('last_login', 'Never')}"
            self.stats_label = ctk.CTkLabel(self, text=stats_text, font=("Arial", 12))
            self.stats_label.pack(pady=5)

        self.start_button = ctk.CTkButton(
            self, 
            text="🎤 Start Voice Assistant", 
            command=self.start_assistant,
            width=300,
            height=40,
            font=("Arial", 14)
        )
        self.start_button.pack(pady=20)

        self.logout_button = ctk.CTkButton(
            self, 
            text="Logout", 
            command=self.logout_user,
            width=300,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.logout_button.pack(pady=10)

    def start_assistant(self):
        self.clear_window()
        
        label = ctk.CTkLabel(
            self, 
            text="🎤 AI Assistant Zen is active...\nSay the wake word to begin", 
            font=("Arial", 16)
        )
        label.pack(pady=50)
        
        status_label = ctk.CTkLabel(
            self, 
            text="Status: Listening for wake word...", 
            font=("Arial", 12),
            text_color="green"
        )
        status_label.pack(pady=10)

        stop_button = ctk.CTkButton(
            self, 
            text="Stop Assistant", 
            command=self.stop_assistant,
            width=200,
            fg_color="red",
            hover_color="darkred"
        )
        stop_button.pack(pady=20)

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