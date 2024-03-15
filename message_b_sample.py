import tkinter as tk
from tkinter import messagebox

def show_message(message_type):
    if message_type == "info":
        # Menampilkan pesan informasi
        messagebox.showinfo("Informasi", "Ini adalah pesan informasi.")
    elif message_type == "error":
        # Menampilkan pesan kesalahan
        messagebox.showerror("Kesalahan", "Ini adalah pesan kesalahan.")
    elif message_type == "warning":
        # Menampilkan pesan peringatan
        messagebox.showwarning("Peringatan", "Ini adalah pesan peringatan.")
    elif message_type == "question":
        # Menampilkan pesan pertanyaan
        response = messagebox.askquestion("Pertanyaan", "Apakah Anda yakin?")
        if response == "yes":
            messagebox.showinfo("Berhasil", "Anda memilih 'Yes'.")
        else:
            messagebox.showinfo("Gagal", "Anda memilih 'No'.")
    elif message_type == "yesno":
        # Menampilkan pesan yes/no
        response = messagebox.askyesno("Yes/No", "Apakah Anda setuju?")
        if response:
            messagebox.showinfo("Berhasil", "Anda memilih 'Yes'.")
        else:
            messagebox.showinfo("Gagal", "Anda memilih 'No'.")

# Membuat jendela aplikasi
root = tk.Tk()
root.title("Aplikasi Desktop")

# Membuat tombol untuk menampilkan pesan informasi
info_button = tk.Button(root, text="Info", command=lambda: show_message("info"))
info_button.pack(pady=5)

# Membuat tombol untuk menampilkan pesan kesalahan
error_button = tk.Button(root, text="Error", command=lambda: show_message("error"))
error_button.pack(pady=5)

# Membuat tombol untuk menampilkan pesan peringatan
warning_button = tk.Button(root, text="Warning", command=lambda: show_message("warning"))
warning_button.pack(pady=5)

# Membuat tombol untuk menampilkan pesan pertanyaan
question_button = tk.Button(root, text="Question", command=lambda: show_message("question"))
question_button.pack(pady=5)

# Membuat tombol untuk menampilkan pesan yes/no
yesno_button = tk.Button(root, text="Yes/No", command=lambda: show_message("yesno"))
yesno_button.pack(pady=5)

# Memulai loop utama aplikasi
root.mainloop()
