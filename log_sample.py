import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import socket

# Fungsi untuk membuat tabel log di database
def create_log_table():
    conn = sqlite3.connect('app_log.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS log (
                 id INTEGER PRIMARY KEY,
                 timestamp TEXT,
                 activity TEXT,
                 method TEXT,
                 status TEXT,
                 user_id TEXT,
                 description TEXT,
                 ip_address TEXT,
                 device_info TEXT,
                 log_level TEXT,
                 reference_code TEXT,
                 additional_data TEXT)''')
    conn.commit()
    conn.close()

# Fungsi untuk membuat tabel users di database
def create_users_table():
    conn = sqlite3.connect('app_log.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY,
                 username TEXT,
                 password TEXT)''')
    conn.commit()
    conn.close()

# Fungsi untuk menambahkan log ke dalam database
def add_log(activity, method, status, user_id, description, ip_address='', device_info='', log_level='', reference_code='', additional_data=''):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('app_log.db')
    c = conn.cursor()
    c.execute("INSERT INTO log (timestamp, activity, method, status, user_id, description, ip_address, device_info, log_level, reference_code, additional_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (timestamp, activity, method, status, user_id, description, ip_address, device_info, log_level, reference_code, additional_data))
    conn.commit()
    conn.close()

# Fungsi untuk registrasi pengguna
def register():
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Periksa apakah password dan konfirmasi password sesuai
    if password != confirm_password:
        messagebox.showerror("Error", "Password tidak sesuai dengan konfirmasi password")
        add_log("Registrasi", "POST", "Failed", username, f"Registrasi gagal untuk pengguna '{username}': Password tidak sesuai dengan konfirmasi password", get_ip_address(), get_device_info())
        return

    # Cek apakah pengguna sudah terdaftar
    conn = sqlite3.connect('app_log.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        messagebox.showerror("Error", "Username sudah digunakan")
        conn.close()
        add_log("Registrasi", "POST", "Failed", username, f"Registrasi gagal untuk pengguna '{username}': Username sudah digunakan", get_ip_address(), get_device_info())
        return

    # Tambahkan pengguna baru ke database
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    # Catat kegiatan registrasi dalam tabel log
    add_log("Registrasi", "POST", "Success", username, f"Registrasi berhasil untuk pengguna '{username}'", get_ip_address(), get_device_info())

    messagebox.showinfo("Info", "Registrasi berhasil")

# Fungsi untuk login
def login():
    username = username_login_entry.get()
    password = password_login_entry.get()

    # Cek apakah username dan password cocok
    conn = sqlite3.connect('app_log.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if c.fetchone():
        messagebox.showinfo("Info", "Login berhasil")
        # Catat kegiatan login dalam tabel log
        add_log("Login", "POST", "Success", username, f"Pengguna '{username}' berhasil login", get_ip_address(), get_device_info())
    else:
        messagebox.showerror("Error", "Login gagal. Username atau password salah")
        add_log("Login", "POST", "Failed", username, f"Login gagal untuk pengguna '{username}': Username atau password salah", get_ip_address(), get_device_info())
    conn.close()

# Fungsi untuk mendapatkan alamat IP pengguna
def get_ip_address():
    try:
        # Mencoba mendapatkan alamat IP dari hostname
        ip_address = socket.gethostbyname(socket.gethostname())
    except:
        # Jika gagal, gunakan alamat loopback
        ip_address = '127.0.0.1'
    return ip_address

# Fungsi untuk mendapatkan informasi perangkat
def get_device_info():
    root = tk.Tk()
    device_info = root.call('tk', 'windowingsystem')
    root.destroy()
    return device_info

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title("Aplikasi Autentikasi")

# Registrasi Frame
register_frame = tk.Frame(root)
register_frame.pack(pady=10)

register_label = tk.Label(register_frame, text="Registrasi")
register_label.grid(row=0, column=0, columnspan=2)

username_label = tk.Label(register_frame, text="Username:")
username_label.grid(row=1, column=0)
username_entry = tk.Entry(register_frame)
username_entry.grid(row=1, column=1)

password_label = tk.Label(register_frame, text="Password:")
password_label.grid(row=2, column=0)
password_entry = tk.Entry(register_frame, show="*")
password_entry.grid(row=2, column=1)

confirm_password_label = tk.Label(register_frame, text="Konfirmasi Password:")
confirm_password_label.grid(row=3, column=0)
confirm_password_entry = tk.Entry(register_frame, show="*")
confirm_password_entry.grid(row=3, column=1)

register_button = tk.Button(register_frame, text="Registrasi", command=register)
register_button.grid(row=4, column=0, columnspan=2, pady=10)

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack(pady=10)

login_label = tk.Label(login_frame, text="Login")
login_label.grid(row=0, column=0, columnspan=2)

username_login_label = tk.Label(login_frame, text="Username:")
username_login_label.grid(row=1, column=0)
username_login_entry = tk.Entry(login_frame)
username_login_entry.grid(row=1, column=1)

password_login_label = tk.Label(login_frame, text="Password:")
password_login_label.grid(row=2, column=0)
password_login_entry = tk.Entry(login_frame, show="*")
password_login_entry.grid(row=2, column=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

# Membuat tabel users saat aplikasi dijalankan
create_users_table()

# Membuat tabel log saat aplikasi dijalankan
create_log_table()

root.mainloop()
